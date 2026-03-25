from langchain_core.prompts import PromptTemplate
from langchain_core.outputparsers import StrOutputParser
from langchain.chains import LLMChain
from sqlalchemy import text
from supabase import create_client, Client
from app.config import settings
from app.agents.router import get_llm
from app.agents.sql_security import SQLSecurityChecker
from typing import List, Dict, Any


class SQLAgent:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        self.llm = get_llm()
        self.security_checker = SQLSecurityChecker()

    def generate_sql(self, question: str, schema: str = "") -> str:
        """根据自然语言生成 SQL"""
        prompt = PromptTemplate(
            template=f"""你是一个 SQL 专家。根据用户问题生成 SQL 查询。

数据库表结构:
{schema}

用户问题: {question}

请只返回 SQL 语句，不要其他解释。""",
            input_variables=["question", "schema"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        output_parser = StrOutputParser()
        chain = chain | output_parser
        return chain.invoke({"question": question, "schema": schema}).strip()

    def execute_sql(self, sql: str) -> List[Dict[str, Any]]:
        """执行 SQL 查询"""
        self.security_checker.validate_and_sanitize(sql)
        response = self.supabase.rpc("exec_sql", {"query": sql}).execute()
        if response.data:
            return response.data
        return []

    def query(self, question: str, schema: str = "") -> Dict[str, Any]:
        """执行完整的查询流程"""
        sql = self.generate_sql(question, schema)
        results = self.execute_sql(sql)
        return {
            "sql": sql,
            "results": results,
            "row_count": len(results)
        }
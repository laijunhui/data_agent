from typing import Dict, Any, List
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from app.agents.router import get_llm
from app.agents.sql_agent import SQLAgent
from app.agents.file_agent import FileAgent
from app.agents.tools.anomaly import detect_anomaly, detect_change_point
from app.agents.tools.yoy_mom import calculate_yoy, calculate_mom
from app.services.logger import AgentLogger
from app.services.chart_generator import ChartGenerator
import pandas as pd
import uuid
import json


# 定义 LangChain Tools
@tool
def sql_query(question: str, schema: str = "") -> str:
    """执行 SQL 查询数据库"""
    agent = SQLAgent()
    result = agent.query(question, schema)
    return json.dumps(result, ensure_ascii=False, default=str)


@tool
def analyze_anomaly(data_json: str, column: str, method: str = "zscore") -> str:
    """异动分析 - 检测异常值。输入为 JSON 字符串格式的数据列表。"""
    df_data = json.loads(data_json) if isinstance(data_json, str) else data_json
    df = pd.DataFrame(df_data)
    result = detect_anomaly(df, column, method)
    return json.dumps(result, ensure_ascii=False, default=str)


@tool
def analyze_yoy(data_json: str, date_col: str, value_col: str) -> str:
    """同比分析。输入为 JSON 字符串格式的数据列表。"""
    df_data = json.loads(data_json) if isinstance(data_json, str) else data_json
    df = pd.DataFrame(df_data)
    result = calculate_yoy(df, date_col, value_col)
    return result.to_json(orient="records", force_ascii=False)


@tool
def analyze_mom(data_json: str, date_col: str, value_col: str) -> str:
    """环比分析。输入为 JSON 字符串格式的数据列表。"""
    df_data = json.loads(data_json) if isinstance(data_json, str) else data_json
    df = pd.DataFrame(df_data)
    result = calculate_mom(df, date_col, value_col)
    return result.to_json(orient="records", force_ascii=False)


@tool
def generate_chart(data_json: str, chart_type: str, x_key: str, y_key: str) -> str:
    """生成图表配置。输入为 JSON 字符串格式的数据列表。"""
    df_data = json.loads(data_json) if isinstance(data_json, str) else data_json
    generator = ChartGenerator()
    result = generator.generate_chart(df_data, chart_type, x_key, y_key)
    return json.dumps(result, ensure_ascii=False, default=str)


TOOLS = [sql_query, analyze_anomaly, analyze_yoy, analyze_mom, generate_chart]


class DataAnalysisAgent:
    def __init__(self):
        self.llm = get_llm()
        self.sql_agent = SQLAgent()
        self.file_agent = FileAgent()
        self.logger = AgentLogger()
        self.chart_generator = ChartGenerator()
        self.agent = create_react_agent(self.llm, TOOLS)

    def analyze(self, question: str, session_id: str = None, file_data: list = None) -> Dict[str, Any]:
        """执行数据分析 - 使用 LangGraph ReAct 模式"""
        request_id = str(uuid.uuid4())
        session_id = session_id or str(uuid.uuid4())

        self.logger.log_input(session_id, request_id, question)

        if file_data:
            context = f"\n\n用户上传了数据：{json.dumps(file_data[:5], ensure_ascii=False)}"
            question = question + context

        try:
            response = self.agent.invoke({
                "messages": [HumanMessage(content=question)]
            })

            sql_queries = self._extract_sql_queries(response)
            charts = self._generate_charts(response)
            final_response = self._format_response(response)

            result = {
                "response": final_response,
                "charts": charts,
                "sql_queries": sql_queries
            }
        except Exception as e:
            result = {
                "response": f"分析出错: {str(e)}",
                "charts": [],
                "sql_queries": []
            }

        self.logger.log_result(session_id, request_id, result)

        return {
            "session_id": session_id,
            "request_id": request_id,
            **result
        }

    def _extract_sql_queries(self, response: Dict) -> List[str]:
        queries = []
        messages = response.get("messages", [])
        for msg in messages:
            if hasattr(msg, "tool_calls"):
                for tc in msg.tool_calls:
                    if tc.get("name") == "sql_query":
                        args = tc.get("args", {})
                        queries.append(args.get("question", ""))
        return queries

    def _generate_charts(self, response: Dict) -> List[Dict]:
        return []

    def _format_response(self, response: Dict) -> str:
        messages = response.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content:
                return msg.content
        return "分析完成"

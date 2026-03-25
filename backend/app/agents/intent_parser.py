from typing import Dict, Any, List, Literal
from enum import Enum
import re


class IntentType(str, Enum):
    DATA_QUERY = "data_query"       # 数据查询
    DATA_ANALYSIS = "data_analysis" # 数据分析
    FILE_UPLOAD = "file_upload"     # 文件上传
    MULTI_STEP = "multi_step"       # 多步骤复杂任务
    UNKNOWN = "unknown"


class IntentParser:
    """意图解析器 - 识别用户意图并提取关键实体"""

    def __init__(self, llm=None):
        self.llm = llm  # 可选，如果使用 LLM 增强意图识别

    def parse(self, question: str) -> Dict[str, Any]:
        """解析用户意图"""
        # 1. 关键词匹配
        intent = self._keyword_match(question)
        # 2. 实体提取
        entities = self._extract_entities(question)
        # 3. 生成策略
        strategy = self._generate_strategy(intent, entities)

        return {
            "intent": intent,
            "entities": entities,
            "strategy": strategy
        }

    def _keyword_match(self, question: str) -> IntentType:
        """基于关键词匹配判断意图类型"""
        question_lower = question.lower()

        # 文件上传关键词
        if any(kw in question_lower for kw in ["上传", "upload", "文件", "file"]):
            return IntentType.FILE_UPLOAD

        # 数据查询关键词
        if any(kw in question_lower for kw in ["查询", "query", "统计", "count", "sum", "avg"]):
            return IntentType.DATA_QUERY

        # 数据分析关键词
        if any(kw in question_lower for kw in ["分析", "analyze", "异动", "anomaly", "同比", "yoy", "环比", "mom"]):
            return IntentType.DATA_ANALYSIS

        # 多步骤关键词
        if any(kw in question_lower for kw in ["趋势", "trend", "报告", "report", "比较", "compare"]):
            return IntentType.MULTI_STEP

        return IntentType.UNKNOWN

    def _extract_entities(self, question: str) -> Dict[str, Any]:
        """提取关键实体（表名、字段、时间范围等）"""
        entities = {
            "tables": [],
            "columns": [],
            "date_range": {},
            "metrics": []
        }

        # 提取时间范围
        date_patterns = [
            (r"(\d{4})年", "year"),
            (r"(\d{4})年(\d{1,2})月", "month"),
            (r"(\d{4})-(\d{2})-(\d{2})", "date"),
        ]
        for pattern, date_type in date_patterns:
            match = re.search(pattern, question)
            if match:
                entities["date_range"][date_type] = match.groups()

        # 提取指标关键词
        metric_keywords = ["销售额", "销量", "利润", "增长", "转化率", "用户数"]
        for metric in metric_keywords:
            if metric in question:
                entities["metrics"].append(metric)

        return entities

    def _generate_strategy(self, intent: IntentType, entities: Dict) -> str:
        """生成执行策略"""
        strategies = {
            IntentType.DATA_QUERY: "使用 SQL Agent 执行查询",
            IntentType.DATA_ANALYSIS: "使用 Python Agent + 分析工具",
            IntentType.FILE_UPLOAD: "使用 File Agent 解析文件",
            IntentType.MULTI_STEP: "使用 Coordinator Agent 协调多步骤",
            IntentType.UNKNOWN: "使用默认 Agent 处理"
        }
        return strategies.get(intent, "使用默认 Agent 处理")
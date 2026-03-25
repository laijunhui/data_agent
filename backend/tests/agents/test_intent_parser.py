import pytest
from app.agents.intent_parser import IntentParser, IntentType


def test_intent_parser_query():
    parser = IntentParser()
    result = parser.parse("查询2024年每月销售额")
    assert result["intent"] == IntentType.DATA_QUERY
    assert "销售额" in result["entities"]["metrics"]


def test_intent_parser_analysis():
    parser = IntentParser()
    result = parser.parse("分析销售异动月份")
    assert result["intent"] == IntentType.DATA_ANALYSIS


def test_intent_parser_file():
    parser = IntentParser()
    result = parser.parse("上传CSV文件分析")
    assert result["intent"] == IntentType.FILE_UPLOAD
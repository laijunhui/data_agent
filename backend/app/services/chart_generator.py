from typing import Dict, Any, List
import json


class ChartGenerator:
    """图表生成器 - 生成 ECharts 配置"""

    def generate_chart(
        self,
        data: List[Dict],
        chart_type: str,
        x_key: str,
        y_key: str
    ) -> Dict[str, Any]:
        """生成图表配置"""
        if not data:
            return {}

        base_config = {
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": [item.get(x_key) for item in data]},
            "yAxis": {"type": "value"},
        }

        if chart_type == "line":
            base_config["series"] = [{
                "type": "line",
                "data": [item.get(y_key) for item in data]
            }]
        elif chart_type == "bar":
            base_config["series"] = [{
                "type": "bar",
                "data": [item.get(y_key) for item in data]
            }]
        elif chart_type == "pie":
            base_config["series"] = [{
                "type": "pie",
                "data": [{"name": item.get(x_key), "value": item.get(y_key)} for item in data]
            }]
        else:
            base_config["series"] = [{
                "type": "line",
                "data": [item.get(y_key) for item in data]
            }]

        return base_config

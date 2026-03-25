import pandas as pd
import numpy as np
from typing import Dict, List, Any


def detect_anomaly(
    df: pd.DataFrame,
    column: str,
    method: str = "zscore",
    threshold: float = 3.0
) -> Dict[str, Any]:
    """异动分析 - 检测异常值"""
    data = df[column].dropna()

    if method == "zscore":
        mean = data.mean()
        std = data.std()
        z_scores = np.abs((data - mean) / std)
        anomalies = data[z_scores > threshold]
        anomaly_indices = z_scores[z_scores > threshold].index.tolist()

        return {
            "method": "zscore",
            "column": column,
            "mean": float(mean),
            "std": float(std),
            "threshold": threshold,
            "anomaly_count": len(anomalies),
            "anomaly_values": anomalies.tolist(),
            "anomaly_indices": anomaly_indices
        }

    elif method == "iqr":
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr

        anomalies = data[(data < lower) | (data > upper)]
        anomaly_indices = anomalies.index.tolist()

        return {
            "method": "iqr",
            "column": column,
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lower_bound": float(lower),
            "upper_bound": float(upper),
            "anomaly_count": len(anomalies),
            "anomaly_values": anomalies.tolist(),
            "anomaly_indices": anomaly_indices
        }

    else:
        raise ValueError(f"Unknown method: {method}")


def detect_change_point(data: List[float], window: int = 3) -> List[int]:
    """突变检测 - 识别数据突变点"""
    change_points = []
    for i in range(window, len(data)):
        prev_mean = np.mean(data[i-window:i])
        curr_val = data[i]
        if abs(curr_val - prev_mean) / (prev_mean + 1e-10) > 0.5:
            change_points.append(i)
    return change_points
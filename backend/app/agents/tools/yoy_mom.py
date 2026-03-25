import pandas as pd
from typing import Dict, Any


def calculate_yoy(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    date_format: str = "%Y-%m"
) -> pd.DataFrame:
    """同比分析 (Year over Year)"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], format=date_format, errors="coerce")
    df = df.dropna(subset=[date_col])

    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month

    result = df.groupby(["year", "month"])[value_col].sum().reset_index()
    result = result.sort_values(["year", "month"])

    result["yoy_growth"] = result[value_col].pct_change(periods=12) * 100

    return result


def calculate_mom(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    date_format: str = "%Y-%m"
) -> pd.DataFrame:
    """环比分析 (Month over Month)"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], format=date_format, errors="coerce")
    df = df.dropna(subset=[date_col])

    df = df.sort_values(date_col)
    result = df.groupby(df[date_col].dt.to_period("M"))[value_col].sum().reset_index()
    result["mom_growth"] = result[value_col].pct_change() * 100

    return result
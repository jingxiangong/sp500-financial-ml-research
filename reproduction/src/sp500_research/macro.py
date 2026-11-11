"""Descriptive FRED-style CSV parsing (not release-date-safe predictive features)."""
from __future__ import annotations
from pathlib import Path
import pandas as pd


def read_fred_observations(path: str | Path) -> pd.Series:
    """Load historical observation PERIOD labels; not actual availability dates."""
    frame = pd.read_csv(path)
    date_name = next((x for x in ("DATE", "Date", "date") if x in frame.columns), None)
    if date_name is None:
        raise ValueError("Missing DATE column")
    value_cols = [c for c in frame.columns if c != date_name]
    if len(value_cols) != 1:
        raise ValueError("Expected one data series per FRED-style CSV")
    series = pd.Series(pd.to_numeric(frame[value_cols[0]],errors="coerce").to_numpy(),
                       index=pd.to_datetime(frame[date_name],errors="coerce"), name=value_cols[0])
    return series.dropna().loc[lambda s: s.index.notna()].sort_index()


def observation_period_overlay(prices: pd.DataFrame, series: pd.Series) -> pd.DataFrame:
    """Monthly descriptive display only; NOT a feature available for trading."""
    monthly_close = prices["Close"].resample("MS").last().rename("SP500_Close_MonthEnd")
    macro = series.resample("MS").ffill().rename(series.name or "Economic_Series")
    return pd.concat((monthly_close, macro), axis=1).dropna()

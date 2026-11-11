"""Load and plot economic series by their observation periods."""
from __future__ import annotations
from pathlib import Path
import pandas as pd


def read_fred_observations(path: str | Path) -> pd.Series:
    """Read a single FRED-style series indexed by its observation date."""
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
    """Align monthly series for plotting, without assuming release-date availability."""
    monthly_close = prices["Close"].resample("MS").last().rename("SP500_Close_MonthEnd")
    macro = series.resample("MS").ffill().rename(series.name or "Economic_Series")
    return pd.concat((monthly_close, macro), axis=1).dropna()

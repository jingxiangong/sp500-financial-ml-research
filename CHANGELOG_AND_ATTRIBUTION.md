"""Illustrative historical trading-signal examples; never evidence of ML strategy profit."""
from __future__ import annotations
import pandas as pd
import numpy as np


def illustrative_sma_strategy(close: pd.Series, short=50, long=200,
                              cost_per_turnover=0.001) -> pd.DataFrame:
    """Signal known after close t, position used from t+1 (one-bar delay).

    Simplifies execution, ignores borrow fees and index instrument tracking,
    and is not a production backtest.
    """
    if short >= long or short < 2:
        raise ValueError("Must have 2 <= short < long")
    px = pd.Series(close, dtype=float).dropna().sort_index()
    slow = px.rolling(long, min_periods=long).mean()
    fast = px.rolling(short, min_periods=short).mean()
    signal = pd.Series(np.where(fast > slow, 1.0, 0.0), index=px.index)
    signal = signal.where(slow.notna(), 0.0)
    exposure = signal.shift(1).fillna(0.0)
    pct = px.pct_change(fill_method=None).fillna(0)
    turnover = exposure.diff().abs().fillna(exposure.abs())
    strategy_ret = (exposure*pct - turnover*cost_per_turnover)
    return pd.DataFrame({"close":px,"signal_after_close":signal,"next_bar_exposure":exposure,
                         "buy_hold_cumulative":(1+pct).cumprod(),
                         "sma_cumulative":(1+strategy_ret).cumprod()})

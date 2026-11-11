"""Causal (past/present-only) features for predicting the next observed close.

Forecast timing: after close on trading date t, predict close on trading date t+1.
This is NOT a pre-market forecast and makes no investment claims.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from .market import clean_ohlcv


def _rsi(close: pd.Series, n: int = 14) -> pd.Series:
    changes = close.diff()
    gain = changes.clip(lower=0)
    loss = -changes.clip(upper=0)
    avg_up = gain.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    avg_dn = loss.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    rs = avg_up / avg_dn.replace(0, np.nan)
    result = 100 - (100 / (1 + rs))
    result = result.mask(avg_dn.eq(0) & avg_up.gt(0), 100.0)
    result = result.mask(avg_up.eq(0) & avg_dn.gt(0), 0.0)
    result = result.mask(avg_up.eq(0) & avg_dn.eq(0), 50.0)
    return result


def build_supervised_frame(ohlcv: pd.DataFrame) -> pd.DataFrame:
    """Build an aligned t -> t+1 next-close dataset.

    `target_date` is a real future trading date, *not* a feature. Split on
    target_date to ensure no training label crosses into validation/test.
    Features use data through market close at t only.
    """
    p = clean_ohlcv(ohlcv)
    c = p["Close"]
    feat = pd.DataFrame(index=p.index)
    feat["close_t"] = c
    feat["lag_7"] = c.shift(7)
    feat["lag_30"] = c.shift(30)
    feat["lag_90"] = c.shift(90)
    feat["return_1d"] = c.pct_change(fill_method=None)
    feat["return_5d"] = c.pct_change(5, fill_method=None)
    for n in (12, 26, 90):
        feat[f"ema_{n}"] = c.ewm(span=n, adjust=False).mean()
    feat["macd"] = feat["ema_12"] - feat["ema_26"]
    feat["macd_signal"] = feat["macd"].ewm(span=9, adjust=False).mean()
    feat["rsi_14"] = _rsi(c)
    prev_close = c.shift(1)
    true_range = pd.concat([
        p["High"] - p["Low"],
        (p["High"] - prev_close).abs(),
        (p["Low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    feat["atr_14"] = true_range.rolling(14, min_periods=14).mean()
    if p["Volume"].notna().mean() > 0.95 and (p["Volume"].fillna(0) > 0).sum() > 90:
        feat["obv"] = (np.sign(c.diff()).fillna(0) * p["Volume"]).cumsum()
    feat["target_next_close"] = c.shift(-1)
    feat["target_date"] = pd.Series(p.index, index=p.index).shift(-1)
    feat = feat.replace([np.inf, -np.inf], np.nan).dropna()
    if feat.empty:
        raise ValueError("Insufficient usable data: need >90 daily observations")
    if not (feat["target_date"] > feat.index.to_series()).all():
        raise ValueError("Target dates must be after feature dates")
    return feat


def model_features(frame: pd.DataFrame) -> list[str]:
    """Exclude target/date identifiers and any nonexistent volume feature."""
    exclude = {"target_next_close", "target_date"}
    return [c for c in frame.columns if c not in exclude]

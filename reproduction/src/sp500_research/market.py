"""Market-data loading. User supplies a licensed, unmodified OHLCV CSV or downloads it.

Index OHLCV data is for research, not necessarily a directly tradable product.
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd


REQUIRED = ("Open", "High", "Low", "Close")


def clean_ohlcv(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize a daily market frame to UTC-naive, strictly increasing dates.

    A missing Volume is represented as NaN, not zero: 0 would masquerade as
    genuine volume and make OBV silently meaningless.
    """
    frame = data.copy()
    # yfinance sometimes returns a 2-level header such as ('Close', '^GSPC').
    if isinstance(frame.columns, pd.MultiIndex):
        available = frame.columns.get_level_values(0)
        if all(col in available for col in REQUIRED):
            frame.columns = frame.columns.get_level_values(0)
            frame = frame.loc[:, ~frame.columns.duplicated()]
        else:
            raise ValueError("Unsupported MultiIndex OHLCV column arrangement")
    frame = frame.rename(columns=lambda c: str(c).strip())
    missing = set(REQUIRED).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing daily OHLCV columns: {sorted(missing)}")
    if not isinstance(frame.index, pd.DatetimeIndex):
        frame.index = pd.to_datetime(frame.index, errors="coerce", utc=True)
    else:
        frame.index = pd.to_datetime(frame.index, errors="coerce", utc=True)
    frame.index = frame.index.tz_convert("UTC").tz_localize(None)
    frame = frame.loc[frame.index.notna()].sort_index()
    frame = frame.loc[~frame.index.duplicated(keep="last")]
    if "Volume" not in frame.columns:
        frame["Volume"] = float("nan")
    frame = frame.loc[:, [*REQUIRED, "Volume"]]
    for col in frame.columns:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.dropna(subset=list(REQUIRED))
    if frame.empty:
        raise ValueError("No usable market rows")
    if (frame["Close"] <= 0).any():
        raise ValueError("Prices must be positive")
    frame.index.name = "Date"
    return frame


def load_prices(csv_path: str | Path) -> pd.DataFrame:
    """Read a user-supplied historical OHLCV CSV with a Date column."""
    data = pd.read_csv(csv_path)
    date_key = next((c for c in ("Date", "Datetime", "date") if c in data.columns), None)
    if date_key is None:
        raise ValueError("Expected a Date column in market CSV")
    return clean_ohlcv(data.set_index(date_key))


def download_sp500(start="2000-01-01", end="2025-01-01") -> pd.DataFrame:
    """Explicit opt-in fresh download. No access or point-in-time guarantees."""
    try:
        import yfinance as yf
    except ImportError as exc:
        raise ImportError("Install the optional yfinance package first") from exc
    raw = yf.download("^GSPC", start=start, end=end, auto_adjust=False, progress=False)
    if raw is None or raw.empty:
        raise ValueError("No Yahoo Finance results; verify connection and ticker")
    return clean_ohlcv(raw)

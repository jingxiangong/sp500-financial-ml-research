# Market data

Put a historical S&P 500 OHLCV CSV here as `sp500_ohlcv.csv`. The loader expects a date column plus `Open`, `High`, `Low`, and `Close`; `Volume` is optional. Keep one row per trading date.

No market data are included in the repository. If this CSV is missing, the notebooks will try to download a fresh `^GSPC` series through `yfinance`. That requires internet access, and downloaded values may differ from the data used in the 2024 research.

You can also add GDP, CPI, or unemployment CSVs for the descriptive comparisons in Notebook 05. Those files usually date observations by economic period, not by the day the data became public. The notebook does not use them as historical forecasting inputs for that reason. Check the relevant provider's terms before redistributing any data.

# Reproduction workspace — independent 2026 reference code

Run from this directory:

```bash
python -m pip install -e .
python -m pip install pytest jupyterlab yfinance
python -m pytest -q
jupyter lab notebooks
```

Use a licensed S&P 500 OHLCV CSV in `data/sp500_ohlcv.csv`, or optionally
allow the notebook to download Yahoo Finance index data. Install tensorflow,
statsmodels and xgboost separately to run optional model examples.

- Never use entire-dataset scaling before a chronological split.
- Never treat FRED observation-period dates as actual publication dates.
- Never reuse 2024 paper metrics as outputs from this separate project.
- Always report a naive last-close price baseline.

Five new notebooks are intentionally different from the original coauthored
`RoughCode*.ipynb` files. Original notebook authorship is not transferred by a
later rewrite. Source methods are newly authored reference implementations;
no saved research output is fabricated.

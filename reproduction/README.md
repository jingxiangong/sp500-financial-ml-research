# Running the research examples

This folder contains five notebooks and a small Python package for S&P 500 modeling experiments. The project is a 2026 follow-up to the earlier university research; it does not reproduce the paper's original code or scores.

From this folder, install the package and open Jupyter:

```bash
python -m venv .venv
# Activate .venv, then run:
python -m pip install -e .
python -m pip install jupyterlab pytest yfinance
python -m pytest -q
jupyter lab notebooks
```

The notebooks look for `data/sp500_ohlcv.csv`. If it is missing, they try a fresh `yfinance` download. The first four notebooks deal with market-derived features and next-session price prediction; the fifth examines macroeconomic data descriptively and uses a simplified moving-average strategy.

TensorFlow, XGBoost, and `statsmodels` are optional dependencies for specific examples. Use the [root README](../README.md) for the notebook guide and evaluation limitations.

# S&P 500 Forecasting — Independent Research Reimplementation

**2026 reference implementation · Python/Jupyter · Historical research attribution preserved**

This repository documents and independently reimplements selected methods from an academic study of S&P 500 forecasting with technical and macroeconomic indicators. The original coursework took place in 2024 and led to a five-author paper at IEEE BigData 2025. **The code in `reproduction/` is newly written educational reference code, not the source code that produced the published figures or results.**

## Research question

Do technical indicators and macroeconomic information offer useful signals for forecasting S&P 500 prices? How do different model classes compare against a simple persistence baseline when evaluated chronologically?

The 2024 work explored historical price/volume, moving averages, MACD, RSI, ATR and OBV; GDP, CPI and unemployment were studied for additional economic context. The early two-author manuscript's discussion reported **no substantial additional gain from GDP** for its selected-feature comparison. That finding does not establish causality or a universal result.

## 2026 implementation: what is included

```text
reproduction/
  notebooks/
    01_data_and_features.ipynb
    02_classical_models.ipynb
    03_lstm_sequences.ipynb
    04_feature_selection_and_arima.ipynb
    05_exploratory_macro_and_strategies.ipynb
  src/sp500_research/
    market.py, features.py, evaluation.py, macro.py, strategies.py
  tests/test_market_features.py
  data/README.md
  pyproject.toml, requirements.txt
paper/citation.bib
docs/PUBLIC_REPOSITORY_CHECK.md
source_sha256.txt
```

Five notebooks have been **independently implemented** as a readable teaching/research workflow. They do not contain the collaborative `RoughCode1.ipynb`–`RoughCode4.ipynb` or `roughCode5.ipynb` from 2024, and are **not** edits or aliases of those files. The original `coding.ipynb` (personally authored in the earlier project) is not included in this reimplementation package. No original copyrighted PDF or third-party market-data CSV is bundled.

### What the independent notebooks do

| Notebook | Main purpose | Important constraint |
|---|---|---|
| 01 | OHLCV normalization, past-only indicators and next-session label | Features at close *t* → label at close *t+1* |
| 02 | Naive last-close baseline, Ridge, Random Forest and gradient boosting; optional XGBoost | Split by **target date**, rank on validation |
| 03 | Optional TensorFlow LSTM over lookback sequences | Train-only scaling; new metrics, not IEEE results |
| 04 | Validation-only permutation importance; optional ARIMA one-step walk-forward | No feature-selection tuning on test |
| 05 | Descriptive GDP/CPI/UNRATE overlays and SMA illustration | Observation dates are **not release dates**; no ML trading claims |

## Local setup

Requires Python 3.10+; tested locally with preinstalled Python tooling on synthetic data. Network-dependent data acquisition, TensorFlow LSTM training and paper-result reproduction **were not tested** in this code review.

```bash
cd reproduction
python -m venv .venv
# Activate the virtual environment on your operating system.
python -m pip install -e .
python -m pip install jupyterlab pytest yfinance
python -m pytest -q
jupyter lab notebooks
```

Optional libraries: `pip install xgboost statsmodels tensorflow`. These are not required for the core unit tests; some individual notebooks require them. Installing dependencies does not guarantee that model services and data feeds are always available.

**Input data:** Put your own appropriately licensed `sp500_ohlcv.csv` in `reproduction/data/` with a `Date,Open,High,Low,Close,Volume` schema, or let the notebooks explicitly fetch a new Yahoo Finance sample with `yfinance`. New downloads use different historical data vintages from the original experiments. See [`reproduction/data/README.md`](reproduction/data/README.md).

Run notebooks from the `reproduction/notebooks/` working directory (Jupyter Lab does this when opened from the supplied path). Python modules must first be installed with `pip install -e .` from `reproduction/`.

## Evaluation boundaries

- Forecast target: next **observed trading day** close, after the current day's close is already known. This is not a market-open forecast.
- Model inputs include current market close and past indicators, not future-shifted price columns.
- Train/validation/test segmentation uses chronological **target dates**, so target outcomes do not cross split boundaries.
- Scalers and feature-selection models fit on training data only; diagnostic importance is measured on validation data.
- Errors produced by these notebooks are in **index points** and **cannot be directly compared** with MAE/RMSE values from the paper's different scaling, dataset and evaluation design.
- Macroeconomic CSVs contain **observation-period dates**, not verified historical release dates or vintage information. They are shown descriptively and are excluded from the predictive models in this release.
- Strategy illustrations are not market-executable profit reports or ML model backtests.
- The LSTM and ARIMA examples are educational examples with explicit optional dependencies; they do not reproduce the 2024 experiment settings.

See [`docs/PUBLIC_REPOSITORY_CHECK.md`](docs/PUBLIC_REPOSITORY_CHECK.md) for tests and unresolved limitations.

## Historic research and attribution

The research that motivated this repository was collaborative. In the earlier coursework project, Jing Xiang Ong reports primary personal ownership of `coding.ipynb` (historic market and macro preprocessing, feature exploration, data visualization), and joint work with Abhinav Jain on the separate experimental modeling notebooks. The later 2025 paper lists **Abhinav Jain, Carson K. Leung, Thanh Trung Jack Nguyen, Jing Xiang Ong and Alfredo Cuzzocrea** as coauthors. **Rewriting a method in new code does not change who contributed to the underlying research or who authored the publication.**

**Paper:** A. Jain, C. K. Leung, T. T. J. Nguyen, J. X. Ong, and A. Cuzzocrea, “Machine Learning on Big Economic Data for Predictive Financial Analytics,” *2025 IEEE International Conference on Big Data (BigData)*, pp. 4613–4622. [DOI: 10.1109/BigData66926.2025.11402545](https://doi.org/10.1109/BigData66926.2025.11402545).

Saved historical selected-feature LSTM values (MAE **0.1798**, RMSE **0.1873**) come from the earlier research artifacts; they have **not** been independently reproduced in this repository and should never be presented as outcomes from these new notebooks.

## Source availability and license

The original five collaborative exploratory notebooks have intentionally **not been redistributed** in this public reimplementation. Third-party market-data terms and publisher rights should be reviewed before uploading snapshots or PDFs. No LICENSE is assigned in this package; lack of a license is not a grant of unrestricted reuse. The new code was drafted using AI-assisted development for a distinct implementation and should be reviewed before public release or professional use.

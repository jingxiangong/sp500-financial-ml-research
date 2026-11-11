# Repository review

*Checked November 11, 2026 against the public `main` branch of [sp500-financial-ml-research](https://github.com/jingxiangong/sp500-financial-ml-research).*

## What is in the repository

The directory structure has been checked following the upload cleanup in commit [`f2dba32`](https://github.com/jingxiangong/sp500-financial-ml-research/commit/f2dba323d6d7c484837a38b9b7ab48d34ca6c293).

The root contains `README.md`, `.gitignore`, `source_sha256.txt`, and three directories: `docs/`, `paper/`, and `reproduction/`. The five notebooks are under `reproduction/notebooks/`. The Python package, tests, and installation files are under `reproduction/`. There are **22 tracked files** in the reviewed snapshot.

The earlier upload had several files in the wrong locations. Those duplicates have since been removed; the root layout above is the one to use.

## Checks completed

| Check | Result |
|---|---|
| Repository structure and file paths | Confirmed on GitHub `main` |
| All five notebook files present | Confirmed |
| Notebook JSON and Python cell syntax | Checked on the prepared source package |
| Python module syntax | Checked on the prepared source package |
| Offline unit tests | 5 passed using synthetic OHLCV data |
| File-integrity manifest | Included as `source_sha256.txt`; regenerate it if files change |

The offline tests cover the next-session target, lag construction, chronological partitioning, a basic model run, and moving-average strategy behavior. They do **not** establish performance on real market data.

## What has not been verified

- A clean end-to-end run of all five notebooks using a fixed, licensed historical market dataset.
- TensorFlow LSTM training and the optional XGBoost and ARIMA examples in a fully pinned environment.
- Agreement with the 2025 IEEE publication's numerical results. The new code uses a different setup and does not claim to reproduce those results.
- Historical availability dates and revisions for GDP, CPI, and unemployment data. Those series are descriptive in this repository, not predictors.
- Market execution costs, financing, and other details needed for a realistic trading-system evaluation.

The repository includes no original collaborative `RoughCode` notebooks, no publisher PDF, and no third-party price-data snapshot. The 2026 reference implementation is separate from the original research. The paper's authorship is recorded in the README and citation file.

## Before using this as a demonstration

Open the five notebooks on GitHub to check that they render. For a working demonstration, install the project from `reproduction/`, run the tests, and record the market-data source and run date before quoting any new results. The research notebooks are not a deployed forecasting or trading product.

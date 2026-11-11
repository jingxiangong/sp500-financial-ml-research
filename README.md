# S&P 500 Forecasting: Research Notes and Reimplementation

In 2024, I worked with Abhinav Jain on a University of Manitoba research project exploring S&P 500 prices, technical indicators, and economic data such as GDP, CPI, and unemployment. The work later contributed to a paper published at IEEE BigData 2025.

This repository is a **2026 follow-up implementation** of some of those research ideas. It revisits the analysis in Python with a clearly defined forecast target, chronological evaluation, and a simple baseline. It is not the original code used to produce the published results.

## The question

Can technical indicators help predict the next S&P 500 closing value? And how much do more complicated models add over simply using the last known close?

The original project also explored whether macroeconomic indicators provide information beyond market-derived features. An important finding in the early research manuscript was that adding GDP to a selected set of technical features did **not** produce a clear additional improvement in that comparison. That result is worth keeping alongside the more promising model experiments.

## What's here

| Notebook | Focus |
|---|---|
| [01 · Data and features](reproduction/notebooks/01_data_and_features.ipynb) | Prepare daily market data, calculate indicators, and define a next-session target |
| [02 · Model comparison](reproduction/notebooks/02_classical_models.ipynb) | Compare a last-close baseline with Ridge, Random Forest, and gradient boosting; XGBoost is optional |
| [03 · LSTM](reproduction/notebooks/03_lstm_sequences.ipynb) | Build 30-session sequences and train an optional TensorFlow model |
| [04 · Feature selection and ARIMA](reproduction/notebooks/04_feature_selection_and_arima.ipynb) | Inspect permutation importance on validation data and try an ARIMA example |
| [05 · Macroeconomics and strategies](reproduction/notebooks/05_exploratory_macro_and_strategies.ipynb) | Compare economic series descriptively and examine a simple moving-average rule |

The reusable data-processing and evaluation functions live in [`reproduction/src/sp500_research/`](reproduction/src/sp500_research/). The accompanying [tests](reproduction/tests/) use synthetic price data. You'll also find a [short repository review](docs/PUBLIC_REPOSITORY_CHECK.md), [project history and attribution](docs/CHANGELOG_AND_ATTRIBUTION.md), and the [paper citation](paper/citation.bib).

## Running the notebooks

Use Python 3.10 or newer. From the repository root:

```bash
cd reproduction
python -m venv .venv
# Activate .venv using the command for your operating system.
python -m pip install -e .
python -m pip install jupyterlab pytest yfinance
python -m pytest -q
jupyter lab notebooks
```

The first notebook looks for `reproduction/data/sp500_ohlcv.csv`. If the file is missing, the notebooks try to download a historical sample of `^GSPC` using `yfinance`; that path requires an internet connection. You can supply your own CSV instead. See the [data notes](reproduction/data/README.md) for the expected columns and data-use considerations.

TensorFlow, `statsmodels`, and XGBoost are optional. Install the relevant package only if you want to run the corresponding example:

```bash
python -m pip install tensorflow statsmodels xgboost
```

Run Jupyter from the `reproduction/` folder so that the notebook data paths resolve as written. The notebooks are saved without training outputs; running them will generate results for the data available in your environment.

## How the new experiments are evaluated

The forecast is made **after market close on day t** for the closing value of the next observed trading session. Features can use prices and indicators known at the end of day t, but not information from the next session. Training, validation, and test periods are ordered by target date.

A last-close forecast is included throughout because predicting a price level is a problem where a simple baseline can be difficult to beat. Model selection uses validation results; the code also prints test scores for the candidate models, so the test table should be treated as a diagnostic comparison rather than a basis for further tuning. Errors are reported in index points.

Economic data need an extra precaution: a GDP or CPI observation can be dated before it was publicly released. This implementation uses those series for **descriptive plots only**, not as historical forecasting inputs. A fair macroeconomic backtest would need release dates and data vintages, not just observation dates.

These examples have been checked on synthetic market data. They have **not** been run here as a complete reproduction of the published paper. In particular, the old research material reported an LSTM MAE of **0.1798** and RMSE of **0.1873**, but those values belong to the earlier experiments, with different data preparation and evaluation. They are not results from these notebooks.

## Research history and contributions

- **2024 coursework:** I wrote `coding.ipynb`, which covered market and economic data preparation, exploratory features, and visual analysis. I also contributed to the modeling experiments with Abhinav Jain. Those original collaborative notebooks are not included here.
- **2025 publication:** The resulting paper has five coauthors: Abhinav Jain, Carson K. Leung, Thanh Trung Jack Nguyen, Jing Xiang Ong, and Alfredo Cuzzocrea.
- **2026 follow-up:** The code in `reproduction/` is a separate implementation written with coding assistance and reviewed against synthetic-data tests. It revisits the methods, rather than claiming to recover the exact publication pipeline.

**Publication:** A. Jain, C. K. Leung, T. T. J. Nguyen, J. X. Ong, and A. Cuzzocrea, “Machine Learning on Big Economic Data for Predictive Financial Analytics,” *2025 IEEE International Conference on Big Data (BigData)*, pp. 4613–4622. [DOI: 10.1109/BigData66926.2025.11402545](https://doi.org/10.1109/BigData66926.2025.11402545).

This is a research project, not an investment recommendation or trading service. No third-party market dataset or publisher PDF is distributed here, and the repository currently has no open-source license.

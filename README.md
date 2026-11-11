# S&P 500 Financial ML — Research Archive

**Original coursework research:** 2024 · **Related peer-reviewed publication:** IEEE BigData 2025 · **Archive review:** November 11, 2026

This is an **attributed historical research archive**, not a production stock-prediction product or a validated trading system. It examines the relationship between historical S&P 500 data, technical indicators, and macroeconomic series (GDP, CPI, unemployment), including collaborative Random Forest, Gradient Boosting, XGBoost, ARIMA and LSTM experiments.

## Research question and outcome

**Question:** Do economic indicators add useful information to technical-price features for S&P 500 modeling?

The historical experiments investigate this question using data acquisition, alignment, feature engineering, visual comparisons and multiple regressors. The earlier two-author draft explicitly notes that adding GDP to selected technical features did **not** produce a substantial additional performance gain in the recorded comparisons. The later IEEE paper is a distinct five-author publication; do not assume the draft and the published version have identical metrics or text.

One archived `RoughCode1.ipynb` output records an LSTM **MAE 0.1798 / RMSE 0.1873** with selected `EMA_90` and `OBV` features. This is a **saved historical output**, not an independently reproduced result. The cell's currently saved source is incomplete; it cannot establish an end-to-end macro-enhanced LSTM run. See [Results provenance](docs/RESULTS_PROVENANCE.md).

## Contributors and scope

- **Jing Xiang Ong:** independently wrote `coding.ipynb` (data acquisition, time-frequency transformation, exploratory feature engineering, visualizations, descriptive risk/strategy comparisons) and contributed Methodology, Data Preprocessing and Feature Engineering prose to the research paper, according to the developer's historical first-person account.
- **Abhinav Jain:** major collaborator and primary model-training/Results-writing contributor, according to the same account.
- The five `RoughCode*.ipynb`/`roughCode5.ipynb` notebooks contain **collaborative exploratory work**. Individual code lines cannot be reliably attributed from this archive. Other IEEE coauthors are credited in the paper; publication authorship is not the same as code authorship.

This repository does not assert sole authorship of the full modeling system.

## What is included

```text
archive/2024-coursework/coding/
  coding.ipynb                 # historical personal notebook
  RoughCode1.ipynb             # collaborative technical / selected-feature experiments
  RoughCode2.ipynb             # collaborative macroeconomic-model experiments
  RoughCode3.ipynb             # collaborative alternate models and tuning
  RoughCode4.ipynb             # collaborative next-day/failed explorations
  roughCode5.ipynb             # collaborative extended economics & strategies
  GDP.csv, us_monthly_gdp.csv, CPIAUCSL.csv, UNRATE.csv
  readme.txt                   # original package note, retained unchanged
figures/archived-personal-notebook/
  *.png                        # exact PNG outputs embedded in coding.ipynb
paper/                         # citation and version distinctions; no publisher PDF
scripts/notebook_inventory.py # static inspection only; does not execute notebooks
docs/                           # provenance, limitations, contribution boundaries
source_sha256.txt               # SHA-256 hashes of preserved original files
```

The CSV snapshots remain **beside** the notebooks in the preserved `coding/` directory because the original code reads local relative paths. The original notebooks and CSVs were copied without modifying their bytes. `desktop.ini` was excluded as operating-system metadata.

## Viewing the work

Start with [EXPERIMENT_INDEX.md](docs/EXPERIMENT_INDEX.md), then open `archive/2024-coursework/coding/coding.ipynb` for the principal personally authored analysis. The other five notebooks document experiments, **including incomplete cells and saved exceptions**.

Historical environment: Python 3.11 and Jupyter on a university computing platform are reported in the notebook outputs. Source imports include pandas, NumPy, yfinance, matplotlib, scikit-learn, TensorFlow/Keras, statsmodels, XGBoost, pandas-datareader, quantstats and seaborn. **No validated, pinned cross-notebook environment or clean end-to-end run is currently available.** Do not treat `Run All` as a published reproduction protocol.

Inspect a notebook statically without running its cells:

```bash
python scripts/notebook_inventory.py archive/2024-coursework/coding
```

For a new leakage-controlled benchmark, create a separate `reproduction/` folder and report new results separately; do not overwrite the original 2024 cells or output values.

## Important evaluation limitations

1. Some model notebooks fit feature scalers on the **whole dataset before chronological splitting**.
2. Macro series are aligned to **observation-period dates**, not independently verified release dates and data vintages.
3. Some regressors predict a same-day close from indicators computed with that same close; this is not equivalent to an actionable next-day forecast.
4. Some experimental cells use randomized train/test splits or non-temporal cross-validation.
5. Saved Notebook output is **historical evidence**, not proof the currently saved code can reproduce the exact values. `RoughCode1` selected-feature cell 3 is notably incomplete.
6. Historical Sharpe values describe the index returns, **not** measured P&L of a trained ML trading policy.

See [Full audit](docs/AUDIT_AND_LIMITATIONS.md) before citing performance numbers.

## Data and publication

The provided CSV files are archived *snapshots* of economic data. `GDP.csv` contains the FRED `GDP` series (nominal GDP); it is **not the same series** as `GDPC1` (real GDP) cited in the early report references. CPIAUCSL is a **price index level**, not a precomputed inflation-rate column. For future point-in-time experiments, obtain date-of-release and vintage documentation.

**Published paper:** A. Jain, C. K. Leung, T. T. J. Nguyen, J. X. Ong and A. Cuzzocrea, "Machine Learning on Big Economic Data for Predictive Financial Analytics," *2025 IEEE International Conference on Big Data*, pp. 4613–4622, DOI: [10.1109/BigData66926.2025.11402545](https://doi.org/10.1109/BigData66926.2025.11402545).

The early two-author manuscript and the IEEE publisher PDF are **not** included in this repository package. Sharing either requires the relevant coauthors' agreement and compliance with publication rights.

## Publication status / permissions

**Prepared for review, not yet approved for a public push.** The code is collaborative, and the archived economic/market data and embedded outputs require a final data-use and collaborator check. No open-source license is assigned here. Do not publish or redistribute the collaborative code under a new license without permission.

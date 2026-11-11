# Public repository and implementation review — November 11, 2026

## Remote GitHub snapshot (checked using the linked GitHub repository API)

Repository: `https://github.com/jingxiangong/sp500-financial-ml-research`

- GitHub reported visibility: **public**.
- Git tree on `main` contained only `.gitignore`, `README.md`, `source_sha256.txt` at the time of this check.
- The old README described `archive/`, `docs/`, `figures/`, `paper/`, `scripts/` as though already present, but those directories were **not** in the remote Git tree.
- The old README claimed the material was "prepared for review, not yet approved for a public push", contradictory with visibility already public.
- The original `source_sha256.txt` referred to code/data not present in that remote. It should be replaced with the new implementation's file hashes or removed.
- The connected GitHub account has read access but **not push permissions** to this repository, so no files have been uploaded or changed remotely by this review.

## What this release changes

- Fully independent, new 2026 notebooks covering data preparation, classical
  models, optional LSTM, feature inspection/ARIMA and descriptive macro/strategy
  exploration. **No original collaborative notebooks are included.**
- Current-market-data acquisition is opt-in. No market snapshot is redistributed.
- Features and next-day labels have explicit time semantics; splits use target
  dates; scaling and importance modeling are trained on the training period.
- Uses a naive last-close persistence benchmark, which matters when comparing
  index-level price errors.
- Macroeconomic values are not incorporated into forecasting without observed
  release dates and vintages; descriptive graphs are clearly labeled.
- Results do not represent reproduced 2025 IEEE BigData experimental outcomes.

## Tests and open items

- The new Python core is tested with deterministic synthetic OHLCV data.
- All new Jupyter files were generated as valid `.ipynb` documents and checked
  for Python syntax; new notebooks are intentionally saved **without outputs**.
- Any model execution on real historical market data remains unverified because
  no licensed OHLCV CSV or available market-data network feed was used for it.
- TensorFlow LSTM and optional ARIMA/XGBoost full notebook runs are not part of
  the core unit tests; library availability, version pinning and run logs remain
  follow-up work.
- This code is research-oriented and not financial advice, a live signal service
  or reliable trading strategy.

## Before making the README your portfolio evidence link

1. Replace the old root README with the new one and upload **all** directories.
2. Replace the old `source_sha256.txt` or delete it; do not leave original
   unpublished-file checksums as if those files were present.
3. Open every notebook on GitHub and check that it renders.
4. Verify no original collaborative notebook or publisher PDF is included.
5. Run `pytest` locally and disclose unexecuted examples as such.
6. Keep the 2024 research authors and paper citation visible.
7. Do not write "paper results reproduced" without a matching clean execution.

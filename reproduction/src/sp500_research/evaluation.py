"""Chronological, leakage-controlled benchmark utilities.

No paper reproduction claim. Results depend on dataset, provider vintage, period,
feature timing, and evaluation protocol.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .features import model_features


@dataclass(frozen=True)
class ChronoSplit:
    train: pd.DataFrame
    valid: pd.DataFrame
    test: pd.DataFrame


def chronological_split(frame: pd.DataFrame, train_fraction: float = 0.70,
                        valid_fraction: float = 0.15) -> ChronoSplit:
    """Split by target dates, never with a randomized train/test split."""
    if not 0.5 <= train_fraction <= 0.9:
        raise ValueError("train_fraction outside accepted range")
    if not 0.05 <= valid_fraction <= 0.3 or train_fraction + valid_fraction >= 0.95:
        raise ValueError("Invalid validation/test fractions")
    if len(frame) < 120:
        raise ValueError("At least 120 labeled dates are required for this example")
    ordered = frame.sort_values("target_date").copy()
    if not ordered["target_date"].is_monotonic_increasing or ordered["target_date"].duplicated().any():
        raise ValueError("target_date must be unique")
    n = len(ordered)
    first, second = int(train_fraction*n), int((train_fraction+valid_fraction)*n)
    parts = ChronoSplit(ordered.iloc[:first].copy(),
                        ordered.iloc[first:second].copy(),
                        ordered.iloc[second:].copy())
    assert parts.train["target_date"].max() < parts.valid["target_date"].min()
    assert parts.valid["target_date"].max() < parts.test["target_date"].min()
    return parts


def regression_metrics(actual, predicted) -> dict[str, float]:
    a = np.asarray(actual, dtype=float).ravel()
    p = np.asarray(predicted, dtype=float).ravel()
    if len(a) == 0 or a.shape != p.shape:
        raise ValueError("Metric inputs must be nonempty, equal-length arrays")
    return {"MAE": float(np.mean(np.abs(a-p))),
            "RMSE": float(np.sqrt(np.mean((a-p)**2)))}


def candidate_models(include_xgboost: bool = False) -> dict:
    # Fixed example parameters, not a tuned search or published recipe.
    models = {
        "Ridge": make_pipeline(StandardScaler(), Ridge(alpha=10)),
        "Random Forest": RandomForestRegressor(n_estimators=100, min_samples_leaf=4,
                                              random_state=42, n_jobs=-1),
        "HistGradientBoosting": HistGradientBoostingRegressor(max_iter=100,
                                  learning_rate=0.05, max_leaf_nodes=15,
                                  early_stopping=False, random_state=42),
    }
    if include_xgboost:
        try:
            from xgboost import XGBRegressor
        except ImportError as exc:
            raise ImportError("XGBoost is optional; install it explicitly") from exc
        models["XGBoost"] = XGBRegressor(n_estimators=100, max_depth=3,
                       learning_rate=0.05, subsample=0.9, random_state=42,
                       objective="reg:squarederror", n_jobs=2)
    return models


def train_and_compare(parts: ChronoSplit, include_xgboost: bool = False):
    """Fit on train, rank on validation, evaluate test once (without refit).

    All scores are in original price units, unlike potentially scaled paper
    results. Do NOT interpret them as independently reproduced paper tables.
    """
    cols = model_features(parts.train)
    xtr, ytr = parts.train[cols], parts.train["target_next_close"]
    xv, yv = parts.valid[cols], parts.valid["target_next_close"]
    xt, yt = parts.test[cols], parts.test["target_next_close"]
    results = []
    # Strong price-level baseline; knows the market close at feature date t.
    for stage, d in (("valid", parts.valid), ("test", parts.test)):
        score = regression_metrics(d["target_next_close"], d["close_t"])
        results.append({"model": "Naive last close", "split": stage, **score})
    models = candidate_models(include_xgboost)
    for name, model in models.items():
        model.fit(xtr, ytr)
        results.append({"model": name, "split": "valid", **regression_metrics(yv, model.predict(xv))})
        results.append({"model": name, "split": "test", **regression_metrics(yt, model.predict(xt))})
    table = pd.DataFrame(results)
    best_valid = table[table.split == "valid"].sort_values("RMSE").iloc[0]["model"]
    return table, best_valid, models

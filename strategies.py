"""Independent educational reimplementation of historical S&P 500 research methods.

Not the original code used for the 2025 IEEE BigData paper.
"""

from .market import load_prices, download_sp500
from .features import build_supervised_frame, model_features
from .evaluation import chronological_split, train_and_compare, regression_metrics

__all__ = [
    "load_prices", "download_sp500", "build_supervised_frame", "model_features",
    "chronological_split", "train_and_compare", "regression_metrics",
]

"""Reusable evaluation helpers for Stage 11."""

import numpy as np


def mean_impute(values: np.ndarray) -> np.ndarray:
    result = values.copy()
    result[np.isnan(result)] = np.nanmean(result)
    return result


def median_impute(values: np.ndarray) -> np.ndarray:
    result = values.copy()
    result[np.isnan(result)] = np.nanmedian(result)
    return result


class SimpleLinReg:
    def fit(self, X, y):
        design = np.c_[np.ones(len(X)), X.ravel()]
        beta = np.linalg.pinv(design) @ y
        self.intercept_ = float(beta[0])
        self.coef_ = np.array([float(beta[1])])
        return self

    def predict(self, X):
        return self.intercept_ + self.coef_[0] * X.ravel()


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))


def bootstrap_metric(y_true, y_pred, fn, n_boot=500, seed=111, alpha=0.05):
    rng = np.random.default_rng(seed)
    indices = np.arange(len(y_true))
    statistics = []
    for _ in range(n_boot):
        sample = rng.choice(indices, size=len(indices), replace=True)
        statistics.append(fn(y_true[sample], y_pred[sample]))
    low, high = np.percentile(
        statistics,
        [100 * alpha / 2, 100 * (1 - alpha / 2)],
    )
    return {
        'mean': float(np.mean(statistics)),
        'lo': float(low),
        'hi': float(high),
    }


def fit_fn(X, y):
    return SimpleLinReg().fit(X, y)

"""
Helper dùng chung cho bộ demo Chương 8.

Chỉ cần numpy + matplotlib (không cần scipy/pandas/sklearn).
Chạy:  python common.py   # tự kiểm tra nhanh
"""

import sys
from pathlib import Path

import matplotlib
import numpy as np


def in_notebook():
    """True khi đang chạy trong Jupyter / VS Code / Colab."""
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell is not None and shell.__class__.__name__ in {"ZMQInteractiveShell", "Shell"}:
            return True
    except Exception:
        pass
    return "ipykernel" in sys.modules


IN_NOTEBOOK = in_notebook()

# Trong notebook để backend mặc định (inline) để hình hiện ngay dưới cell.
# Khi chạy script / server không màn hình thì dùng Agg để xuất PNG.
if not IN_NOTEBOOK:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

FIG_DIR = Path(__file__).resolve().parent / "figures"
FIG_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Thiết lập hình
# ---------------------------------------------------------------------------
def setup():
    """Style thống nhất cho mọi hình xuất ra."""
    plt.rcParams.update(
        {
            "figure.dpi": 130,
            "savefig.dpi": 130,
            "font.size": 11,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.autolayout": True,
        }
    )


def save(fig, name, close=None):
    """Lưu hình vào code-demo/figures/<name>.

    - Trong notebook: mặc định giữ figure mở để Jupyter hiển thị inline.
    - Trong script: mặc định đóng figure sau khi lưu.
    """
    path = FIG_DIR / name
    fig.savefig(path, bbox_inches="tight")
    if close is None:
        close = not IN_NOTEBOOK
    if close:
        plt.close(fig)
    print(f"  → đã lưu hình: figures/{name}")
    return path


# ---------------------------------------------------------------------------
# Logistic regression tối giản (đủ để minh hoạ, không cần sklearn)
# ---------------------------------------------------------------------------
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60.0, 60.0)))


def _as_2d(X):
    X = np.asarray(X, dtype=float)
    return X[:, None] if X.ndim == 1 else X


def train_logreg(X, y, lr=0.1, epochs=800, l2=1e-3, sample_weight=None, w0=None):
    """Train logistic regression bằng gradient descent.

    w0 khác None → warm start (dùng cho stateful / fine-tuning).
    """
    X = _as_2d(X)
    Xb = np.c_[np.ones(len(X)), X]
    y = np.asarray(y, dtype=float)
    w = np.zeros(Xb.shape[1]) if w0 is None else np.asarray(w0, dtype=float).copy()

    sw = np.ones(len(y)) if sample_weight is None else np.asarray(sample_weight, float)
    sw = sw / sw.mean()

    for _ in range(epochs):
        p = sigmoid(Xb @ w)
        grad = Xb.T @ (sw * (p - y)) / len(y)
        grad[1:] += l2 * w[1:]
        w -= lr * grad
    return w


def predict_proba(X, w):
    return sigmoid(np.c_[np.ones(len(_as_2d(X))), _as_2d(X)] @ w)


def predict(X, w, threshold=0.5):
    return (predict_proba(X, w) >= threshold).astype(int)


def accuracy(y_true, y_pred):
    return float(np.mean(np.asarray(y_true) == np.asarray(y_pred)))


# ---------------------------------------------------------------------------
# Thống kê mô tả
# ---------------------------------------------------------------------------
def summary_stats(x):
    x = np.asarray(x, dtype=float)
    mean = x.mean()
    std = x.std(ddof=0)
    q = np.quantile(x, [0.05, 0.25, 0.5, 0.75, 0.95])
    skew = float(np.mean(((x - mean) / std) ** 3)) if std > 0 else 0.0
    kurt = float(np.mean(((x - mean) / std) ** 4) - 3.0) if std > 0 else 0.0
    return {
        "min": float(x.min()),
        "q05": float(q[0]),
        "q25": float(q[1]),
        "median": float(q[2]),
        "mean": float(mean),
        "q75": float(q[3]),
        "q95": float(q[4]),
        "max": float(x.max()),
        "std": float(std),
        "skew": skew,
        "kurtosis": kurt,
    }


def print_stats_table(a, b, label_a="train", label_b="production", features=("mean", "std", "q05", "median", "q95", "skew")):
    sa, sb = summary_stats(a), summary_stats(b)
    print(f"  {'stat':>10} | {label_a:>12} | {label_b:>12} | {'Δ':>9}")
    print("  " + "-" * 52)
    for k in features:
        print(f"  {k:>10} | {sa[k]:>12.4f} | {sb[k]:>12.4f} | {sb[k] - sa[k]:>+9.4f}")


# ---------------------------------------------------------------------------
# Two-sample tests (tự cài, không cần scipy)
# ---------------------------------------------------------------------------
def ks_stat(a, b):
    """Kolmogorov–Smirnov statistic cho dữ liệu 1 chiều."""
    a = np.sort(np.asarray(a, dtype=float))
    b = np.sort(np.asarray(b, dtype=float))
    grid = np.sort(np.concatenate([a, b]))
    cdf_a = np.searchsorted(a, grid, side="right") / len(a)
    cdf_b = np.searchsorted(b, grid, side="right") / len(b)
    return float(np.max(np.abs(cdf_a - cdf_b)))


def ks_perm_test(a, b, n_perm=2000, seed=0):
    """KS + permutation p-value. p nhỏ → hai tập khác phân phối."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    obs = ks_stat(a, b)
    rng = np.random.default_rng(seed)
    pool = np.concatenate([a, b])
    n = len(a)
    count = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        if ks_stat(pool[:n], pool[n:]) >= obs:
            count += 1
    return obs, (count + 1) / (n_perm + 1)


def _sq_dists(X, Y):
    return np.sum(X**2, axis=1)[:, None] + np.sum(Y**2, axis=1)[None, :] - 2.0 * X @ Y.T


def mmd2(X, Y, gamma=None):
    """MMD^2 (biased estimator) với RBF kernel, dùng được cho dữ liệu đa biến."""
    X = _as_2d(X)
    Y = _as_2d(Y)
    Z = np.vstack([X, Y])
    if gamma is None:
        d2 = _sq_dists(Z, Z)
        med = np.median(d2[d2 > 0])
        gamma = 1.0 / med if med > 0 else 1.0
    K = np.exp(-gamma * _sq_dists(Z, Z))
    n = len(X)
    return float(K[:n, :n].mean() - 2.0 * K[:n, n:].mean() + K[n:, n:].mean())


def mmd_perm_test(X, Y, n_perm=500, seed=0):
    X = _as_2d(X)
    Y = _as_2d(Y)
    obs = mmd2(X, Y)
    rng = np.random.default_rng(seed)
    pool = np.vstack([X, Y])
    n = len(X)
    count = 0
    for _ in range(n_perm):
        idx = rng.permutation(len(pool))
        if mmd2(pool[idx[:n]], pool[idx[n:]]) >= obs:
            count += 1
    return obs, (count + 1) / (n_perm + 1)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    setup()
    rng = np.random.default_rng(0)
    a = rng.normal(0, 1, 500)
    b = rng.normal(0, 1, 500)
    c = rng.normal(1.0, 1.5, 500)

    print("KS cùng phân phối :", ks_perm_test(a, b))
    print("KS khác phân phối :", ks_perm_test(a, c))
    print("MMD cùng phân phối:", mmd_perm_test(a[:, None], b[:, None], n_perm=200))
    print("MMD khác phân phối:", mmd_perm_test(a[:, None], c[:, None], n_perm=200))

"""
Demo 2 — Slide 6: Edge case vs outlier (Figure 8-1)

Một outlier nhãn sai có thể kéo lệch decision boundary và làm model
sai hàng loạt trên dữ liệu sạch.

Chạy: python 02_edge_case_outlier.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import accuracy, predict, save, setup, train_logreg


def make_data(rng, n=200):
    # Hai lớp Gaussian tách nhau vừa phải
    X0 = rng.normal([-1.0, -1.0], 0.7, (n, 2))
    X1 = rng.normal([1.0, 1.0], 0.7, (n, 2))
    X = np.vstack([X0, X1])
    y = np.r_[np.zeros(n), np.ones(n)].astype(int)
    return X, y


def boundary_line(w, xlim):
    """w = [b, w1, w2]; vẽ w1*x + w2*y + b = 0."""
    xs = np.linspace(*xlim, 200)
    if abs(w[2]) < 1e-9:
        return xs, np.full_like(xs, np.nan)
    return xs, -(w[0] + w[1] * xs) / w[2]


def main():
    setup()
    rng = np.random.default_rng(7)
    # Tập train nhỏ (10 mẫu/lớp) để một outlier có đủ trọng lượng
    X, y = make_data(rng, n=10)

    # Một outlier: nằm sâu trong vùng lớp 1 nhưng bị gán nhãn 0
    outlier = np.array([[5.0, 5.0]])
    y_out = np.array([0])
    X_clean, y_clean = X, y
    X_dirty = np.vstack([X, outlier])
    y_dirty = np.r_[y, y_out]

    w_clean = train_logreg(X_clean, y_clean, lr=0.2, epochs=2000, l2=1e-4)
    w_dirty = train_logreg(X_dirty, y_dirty, lr=0.2, epochs=2000, l2=1e-4)

    # Đánh giá trên tập test sạch, cùng phân phối train
    X_test, y_test = make_data(np.random.default_rng(99))
    acc_clean = accuracy(y_test, predict(X_test, w_clean))
    acc_dirty = accuracy(y_test, predict(X_test, w_dirty))

    print("=== DEMO 2: một outlier có thể phá decision boundary ===")
    print(f"Accuracy trên test sạch — không outlier : {acc_clean:.3f}")
    print(f"Accuracy trên test sạch — có 1 outlier : {acc_dirty:.3f}  ← giảm {acc_clean - acc_dirty:.3f}")
    print()
    print("Outlier  = mẫu khác biệt về DỮ LIỆU.")
    print("Edge case= mẫu model làm TỆ ĐI ĐÁNG KỂ về HIỆU NĂNG.")
    print("Outlier có thể gây edge case, nhưng không phải outlier nào cũng vậy.")
    print()
    print("Ví dụ 99,99% an toàn: 1 triệu chuyến → 100 chuyến lỗi.")
    print("Nếu 0,01% đó gây tai nạn chết người, bạn có dùng xe tự lái không?")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharex=True, sharey=True)
    xlim = (-3.5, 6.5)
    ylim = (-3.5, 6.5)

    for ax, (w, title, acc) in zip(
        axes,
        [
            (w_clean, "Không có outlier", acc_clean),
            (w_dirty, "Có 1 outlier nhãn sai", acc_dirty),
        ],
    ):
        ax.scatter(X[y == 0, 0], X[y == 0, 1], s=14, alpha=0.55, label="Lớp 0", color="#1f77b4")
        ax.scatter(X[y == 1, 0], X[y == 1, 1], s=14, alpha=0.55, label="Lớp 1", color="#ff7f0e")
        xs, ys = boundary_line(w, xlim)
        ax.plot(xs, ys, "k-", lw=2, label="Decision boundary")
        if "outlier" in title:
            ax.scatter(*outlier[0], s=220, marker="X", color="#d62728", edgecolor="k", zorder=5, label="Outlier (nhãn 0)")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_title(f"{title}\nAccuracy test = {acc:.2f}")
        ax.set_xlabel("x₁")

    axes[0].set_ylabel("x₂")
    axes[0].legend(loc="upper left", fontsize=8)
    save(fig, "02_edge_case_outlier.png")


if __name__ == "__main__":
    main()

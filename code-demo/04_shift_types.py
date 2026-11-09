"""
Demo 4 — Slide 9–13: ba loại data distribution shift

Cùng một model logistic train trên source, đánh giá trên target:
  1. Covariate shift : P(X) đổi, P(Y|X) giữ nguyên
  2. Label shift     : P(Y) đổi, P(X|Y) giữ nguyên
  3. Concept drift   : P(Y|X) đổi, P(X) giữ nguyên

Chạy: python 04_shift_types.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import accuracy, predict, save, setup, sigmoid, train_logreg

N = 4000


def empirical_p_y_given_x(x, y, bins=18):
    edges = np.linspace(np.quantile(x, 0.01), np.quantile(x, 0.99), bins + 1)
    idx = np.clip(np.digitize(x, edges) - 1, 0, bins - 1)
    centers, probs = [], []
    for b in range(bins):
        mask = idx == b
        if mask.sum() >= 20:
            centers.append(x[mask].mean())
            probs.append(y[mask].mean())
    return np.array(centers), np.array(probs)


def make_covariate(rng):
    # Quy luật thật: y=1 khi |x| > 1 (hình chữ U).
    # Train chỉ thấy vùng x âm, production chỉ có vùng x dương.
    def true_p(x):
        return sigmoid(6.0 * (np.abs(x) - 1.0))

    Xs = rng.normal(-1.6, 0.35, N)
    ys = rng.binomial(1, true_p(Xs))
    Xt = rng.normal(1.6, 0.35, N)
    yt = rng.binomial(1, true_p(Xt))
    return Xs, ys, Xt, yt


def make_label(rng):
    def sample(prior):
        y = rng.binomial(1, prior, N)
        X = np.where(y == 1, rng.normal(1.0, 1.0, N), rng.normal(-1.0, 1.0, N))
        return X, y

    Xs, ys = sample(0.5)
    Xt, yt = sample(0.1)
    return Xs, ys, Xt, yt


def make_concept(rng):
    Xs = rng.normal(0, 1, N)
    ys = (Xs > 0).astype(int)
    Xt = rng.normal(0, 1, N)
    yt = (Xt < 0).astype(int)          # quy luật bị đảo
    return Xs, ys, Xt, yt


def main():
    setup()
    rng = np.random.default_rng(11)

    scenarios = [
        ("Covariate shift\nP(X) đổi, P(Y|X) giữ nguyên", make_covariate(rng), "P(X)"),
        ("Label shift\nP(Y) đổi, P(X|Y) giữ nguyên", make_label(rng), "P(X | Y)"),
        ("Concept drift\nP(Y|X) đổi, P(X) giữ nguyên", make_concept(rng), "P(Y | X)"),
    ]

    print("=== DEMO 4: ba loại shift ===")
    print(f"{'loại':>18} | {'acc source':>10} | {'acc target':>10} | {'giảm':>6}")
    print("  " + "-" * 54)

    fig, axes = plt.subplots(2, 3, figsize=(13, 6.5))

    for col, (title, data, _) in enumerate(scenarios):
        Xs, ys, Xt, yt = data
        w = train_logreg(Xs, ys, lr=0.2, epochs=1200)
        acc_s = accuracy(ys, predict(Xs, w))
        acc_t = accuracy(yt, predict(Xt, w))
        print(f"{title.splitlines()[0]:>18} | {acc_s:>10.3f} | {acc_t:>10.3f} | {acc_s - acc_t:>+6.3f}")
        print(
            f"   → P(y=1): source={ys.mean():.2f}, target={yt.mean():.2f}; "
            f"model dự đoán positive={predict(Xt, w).mean():.2f}"
        )

        # Hàng trên: phân phối input
        ax = axes[0, col]
        bins = np.linspace(-5.5, 5.5, 45)
        ax.hist(Xs, bins=bins, density=True, alpha=0.55, label="source (train)", color="#1f77b4")
        ax.hist(Xt, bins=bins, density=True, alpha=0.55, label="target (production)", color="#d62728")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("x")
        ax.set_ylabel("mật độ")
        ax.legend(fontsize=8)

        # Hàng dưới: xác suất y=1 theo x (empirical)
        ax = axes[1, col]
        xs_c, xs_p = empirical_p_y_given_x(Xs, ys)
        xt_c, xt_p = empirical_p_y_given_x(Xt, yt)
        ax.plot(xs_c, xs_p, "o-", label="source", color="#1f77b4", ms=3)
        ax.plot(xt_c, xt_p, "o-", label="target", color="#d62728", ms=3)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("x")
        ax.set_ylabel("P(y=1 | x)")
        ax.set_title(f"Accuracy: {acc_s:.2f} → {acc_t:.2f}", fontsize=10)
        ax.legend(fontsize=8)

    print("\nLabel shift thường không làm accuracy sụt mạnh, nhưng làm model dự đoán sai TỶ LỆ nhãn.")
    print("Vì vậy cần monitor cả P(Y) và positive rate, không chỉ accuracy.")

    fig.suptitle("Cùng một model, ba kiểu lệch phân phối khác nhau", fontsize=13)
    save(fig, "04_shift_types.png")


if __name__ == "__main__":
    main()

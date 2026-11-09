"""
Demo 7 — Slide 16 & 17: ứng phó shift bằng retrain

Phần A: chọn cửa sổ dữ liệu để retrain (7 / 30 / 90 / 180 ngày).
Phần B: stateless (train lại từ đầu) vs stateful (fine-tune từ checkpoint)
         trên bài toán 5 chiều với ít dữ liệu mới.

Dữ liệu có concept drift: boundary dịch dần theo thời gian.
Chạy: python 07_retrain_window.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import accuracy, predict, save, setup, sigmoid, train_logreg

DAYS = 180
PER_DAY = 200


def boundary(day):
    """Decision boundary thật dịch dần từ 0 → 2."""
    return 2.0 * day / (DAYS - 1)


def sample(day, rng, n=PER_DAY):
    x = rng.normal(0.0, 1.0, n)
    p = sigmoid(3.0 * (x - boundary(day)))
    y = rng.binomial(1, p)
    return x, y


def main():
    setup()
    rng = np.random.default_rng(41)

    data = [sample(d, rng) for d in range(DAYS)]
    X_all = np.concatenate([d[0] for d in data])
    y_all = np.concatenate([d[1] for d in data])
    day_of = np.repeat(np.arange(DAYS), PER_DAY)

    # Test tại "hôm nay" (day 180)
    X_test, y_test = sample(DAYS, rng, n=3000)

    print("=== DEMO 7: chọn cửa sổ retrain ===")
    print("Boundary thật đã dịch từ 0 → 2 sau 180 ngày.")
    print(f"{'cửa sổ':>10} | {'số mẫu':>7} | {'accuracy':>9}")
    print("  " + "-" * 34)

    windows = [7, 30, 90, 180]
    accs = []
    for w in windows:
        mask = day_of >= DAYS - w
        model = train_logreg(X_all[mask], y_all[mask], lr=0.2, epochs=1200)
        acc = accuracy(y_test, predict(X_test, model))
        accs.append(acc)
        print(f"{w:>8} ngày | {mask.sum():>7} | {acc:>9.3f}")

    best_w = windows[int(np.argmax(accs))]
    print(f"→ Cửa sổ tốt nhất trong thí nghiệm: {best_w} ngày. Phải thực nghiệm, không có công thức chung.")

    # ------------------------------------------------------------------
    # Stateless vs stateful (fine-tune) — bài toán 5 chiều, ít dữ liệu mới
    # ------------------------------------------------------------------
    rng2 = np.random.default_rng(7)
    D = 5
    PER_DAY_HARD = 20

    def sample_hard(day, rng, n=PER_DAY_HARD):
        X = rng.normal(0, 1, (n, D))
        logit = (
            3.0 * (X[:, 0] - boundary(day))
            + 1.0 * X[:, 1]
            - 1.0 * X[:, 2]
            + 0.5 * X[:, 3]
        )
        y = rng.binomial(1, sigmoid(logit))
        return X, y

    data_h = [sample_hard(d, rng2) for d in range(DAYS)]
    X_h = np.vstack([d[0] for d in data_h])
    y_h = np.concatenate([d[1] for d in data_h])
    day_h = np.repeat(np.arange(DAYS), PER_DAY_HARD)
    X_test_h, y_test_h = sample_hard(DAYS, rng2, n=3000)

    w_base = train_logreg(X_h[day_h < 90], y_h[day_h < 90], lr=0.2, epochs=1500)

    adapt_days = [1, 2, 3, 7, 15, 30]
    acc_stateless, acc_stateful = [], []
    for ad in adapt_days:
        mask = day_h >= DAYS - ad
        w_s = train_logreg(X_h[mask], y_h[mask], lr=0.2, epochs=1500)
        w_f = train_logreg(X_h[mask], y_h[mask], lr=0.05, epochs=500, w0=w_base)
        acc_stateless.append(accuracy(y_test_h, predict(X_test_h, w_s)))
        acc_stateful.append(accuracy(y_test_h, predict(X_test_h, w_f)))

    print("\n=== Stateless vs Stateful (5 chiều, 20 mẫu/ngày) ===")
    print(f"{'dữ liệu mới':>12} | {'stateless':>9} | {'stateful':>9}")
    print("  " + "-" * 38)
    for ad, a_s, a_f in zip(adapt_days, acc_stateless, acc_stateful):
        print(f"{ad:>8} ngày | {a_s:>9.3f} | {a_f:>9.3f}")
    print("Khi dữ liệu mới rất ít, stateful (fine-tune) tốt hơn nhờ trọng số cũ.")
    print("Khi có đủ dữ liệu mới, stateless có thể bắt kịp hoặc vượt.")
    print("→ Không có lựa chọn đúng cho mọi trường hợp; phải thực nghiệm.")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    ax = axes[0]
    colors = ["#2ca02c" if a == max(accs) else "#1f77b4" for a in accs]
    ax.bar([f"{w} ngày" for w in windows], accs, color=colors)
    for i, a in enumerate(accs):
        ax.text(i, a + 0.005, f"{a:.3f}", ha="center", fontsize=10)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Accuracy trên dữ liệu hiện tại")
    ax.set_title("Cửa sổ retrain: cũ quá → học quy luật lỗi thời")

    ax = axes[1]
    ax.plot(adapt_days, acc_stateless, "o-", lw=2, label="Stateless (train lại từ đầu)", color="#ff7f0e")
    ax.plot(adapt_days, acc_stateful, "s-", lw=2, label="Stateful (fine-tune)", color="#2ca02c")
    ax.set_xscale("log")
    ax.set_xticks(adapt_days, [str(d) for d in adapt_days])
    ax.set_xlabel("Số ngày dữ liệu mới dùng để adapt")
    ax.set_ylabel("Accuracy")
    ax.set_title("Ít dữ liệu mới → stateful có lợi thế")
    ax.legend(fontsize=8)

    save(fig, "07_retrain_window.png")


if __name__ == "__main__":
    main()

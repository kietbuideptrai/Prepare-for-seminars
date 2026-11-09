"""
Demo 6 — Slide 18–21: monitoring 4 artifact

Mô phỏng sự cố pipeline:
  - Giờ 150: 40% feature bị NaN, pipeline fill bằng 0.
  - Feature mean tụt, prediction positive-rate tụt, accuracy tụt (nhãn trễ 24h).

Minh hoạ: phát hiện sớm nhờ feature/prediction, trước khi có accuracy.
Chạy: python 06_monitoring.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import save, setup, sigmoid

HOURS = 240
SAMPLES = 600
BUG_START = 150
BUG_RATE = 0.40
LABEL_DELAY = 24


def main():
    setup()
    rng = np.random.default_rng(31)

    x_true = rng.normal(10.0, 2.0, (HOURS, SAMPLES))
    p_true = sigmoid(4.0 * (x_true - 10.0))
    y_true = rng.binomial(1, p_true)

    x_model = x_true.copy()
    missing = np.zeros_like(x_true, dtype=bool)
    missing[BUG_START:] = rng.random((HOURS - BUG_START, SAMPLES)) < BUG_RATE
    x_model[missing] = 0.0                     # fill NaN bằng 0

    pred = (sigmoid(4.0 * (x_model - 10.0)) >= 0.5).astype(int)

    missing_rate = missing.mean(axis=1)
    feature_mean = x_model.mean(axis=1)
    positive_rate = pred.mean(axis=1)

    # Accuracy có nhãn trễ 24 giờ
    acc = np.full(HOURS, np.nan)
    for h in range(HOURS):
        if h - LABEL_DELAY >= 0:
            acc[h] = np.mean(pred[h - LABEL_DELAY] == y_true[h - LABEL_DELAY])

    # ------------------------------------------------------------------
    # Alert policy đơn giản
    # ------------------------------------------------------------------
    baseline = feature_mean[:100]
    mu, sd = baseline.mean(), baseline.std()
    z = (feature_mean - mu) / sd

    def first_sustained(condition, need=2):
        run = 0
        for i, ok in enumerate(condition):
            run = run + 1 if ok else 0
            if run >= need:
                return i - need + 1
        return None

    alert_feature = first_sustained(np.abs(z) > 3, need=2)
    alert_pred = first_sustained(positive_rate < 0.35, need=2)
    alert_acc = first_sustained(~np.isnan(acc) & (acc < 0.75), need=2)

    print("=== DEMO 6: monitoring 4 artifact ===")
    print(f"Sự cố thật bắt đầu ở giờ {BUG_START} (40% feature NaN, fill = 0).")
    print(f"Alert feature mean (|z|>3, 2 giờ)      : giờ {alert_feature}")
    print(f"Alert prediction rate (<0.35, 2 giờ)   : giờ {alert_pred}")
    print(f"Alert accuracy (<0.75, nhãn trễ 24h)   : giờ {alert_acc}")
    print("→ Feature/prediction phát hiện trước accuracy vài giờ đến vài chục giờ.")
    print()
    print("Bốn artifact: raw inputs → features → predictions → accuracy metrics.")
    print("Càng sâu pipeline càng gần ground truth nhưng càng trễ và càng khó.")
    print()
    print("SLO tham khảo: 99,99% ≈ 4,3 phút downtime/tháng; 99,999% ≈ 26 giây/tháng.")
    print("Hệ thống 'up' chưa đủ — dự đoán rác vẫn là hệ thống hỏng.")

    # ------------------------------------------------------------------
    # Hình
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 6.5), sharex=True)
    hours = np.arange(HOURS)

    ax = axes[0, 0]
    ax.plot(hours, missing_rate, color="#d62728")
    ax.axvline(BUG_START, color="k", ls=":", lw=1)
    ax.set_ylabel("Tỷ lệ NaN")
    ax.set_title("(1) Raw input / feature: missing rate")

    ax = axes[0, 1]
    ax.plot(hours, feature_mean, color="#1f77b4")
    ax.axhline(mu, color="gray", ls="--", lw=1, label=f"baseline mean={mu:.1f}")
    ax.axvline(BUG_START, color="k", ls=":", lw=1)
    ax.set_ylabel("Giá trị trung bình")
    ax.set_title("(2) Feature mean tụt sau khi fill NaN = 0")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.plot(hours, positive_rate, color="#ff7f0e")
    ax.axhline(0.5, color="gray", ls="--", lw=1, label="baseline ~0.5")
    ax.axvline(BUG_START, color="k", ls=":", lw=1)
    ax.set_ylabel("Tỷ lệ dự đoán = 1")
    ax.set_xlabel("Giờ")
    ax.set_title("(3) Prediction distribution: positive rate tụt")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    ax.plot(hours, acc, color="#2ca02c")
    ax.axhline(0.85, color="gray", ls="--", lw=1, label="baseline ~0.85")
    ax.axvline(BUG_START + LABEL_DELAY, color="k", ls=":", lw=1)
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Giờ")
    ax.set_title("(4) Accuracy — chỉ thấy sau khi nhãn về (trễ 24h)")
    ax.legend(fontsize=8)

    for ax in axes.flat:
        ax.axvspan(BUG_START, HOURS, alpha=0.06, color="#d62728")

    fig.suptitle("Cùng một sự cố, nhìn từ 4 tầng artifact", fontsize=13)
    save(fig, "06_monitoring.png")


if __name__ == "__main__":
    main()

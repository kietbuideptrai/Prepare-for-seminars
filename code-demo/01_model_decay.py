"""
Demo 1 — Slide 2 & 5: "Model tốt vẫn chết sau một năm"

Mô phỏng model dự báo nhu cầu hàng hoá:
  - Train 12 tháng đầu, deploy.
  - Thế giới thay đổi dần (đối thủ mới + promo có tác dụng khác đi).
  - MAE tăng dần → retrain ở tháng 18 → MAE giảm.

Chạy: python 01_model_decay.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import save, setup


def make_features(months, promo):
    return np.c_[months, np.sin(2 * np.pi * months / 12), np.cos(2 * np.pi * months / 12), promo]


def fit_linear(X, y):
    Xb = np.c_[np.ones(len(X)), X]
    w, *_ = np.linalg.lstsq(Xb, y, rcond=None)
    return w


def predict_linear(X, w):
    return np.c_[np.ones(len(X)), X] @ w


def main():
    setup()
    rng = np.random.default_rng(42)

    months = np.arange(24)
    promo = rng.integers(0, 2, len(months))
    season = 15 * np.sin(2 * np.pi * months / 12)

    # Sau tháng 10: đối thủ mới làm cầu giảm dần; promo lại càng ngày càng hiệu quả.
    drift = np.where(months >= 10, -3.0 * (months - 9), 0.0)
    promo_effect = 8.0 + np.where(months >= 10, 1.5 * (months - 9), 0.0)
    demand = 100 + 1.5 * months + season + promo_effect * promo + drift
    demand = demand + rng.normal(0, 3, len(months))

    X = make_features(months, promo)

    # --- Train lần 1: 12 tháng đầu ---
    w1 = fit_linear(X[:12], demand[:12])
    pred1 = predict_linear(X, w1)

    # --- Retrain ở tháng 18: dùng 12 tháng gần nhất (6–17) ---
    w2 = fit_linear(X[6:18], demand[6:18])
    pred2 = predict_linear(X, w2)

    mae1 = np.abs(pred1 - demand)
    mae2 = np.abs(pred2 - demand)

    print("=== DEMO 1: model suy giảm theo thời gian ===")
    print(f"MAE 6 tháng đầu sau deploy : {mae1[12:18].mean():6.2f}")
    print(f"MAE 6 tháng cuối           : {mae1[18:24].mean():6.2f}  ← tăng {mae1[18:24].mean() / mae1[12:18].mean():.1f}×")
    print(f"MAE sau retrain (tháng 18) : {mae2[18:24].mean():6.2f}")
    print("Bài học: deploy là bắt đầu; drift làm sai số tăng, retrain kéo lại.")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, height_ratios=[2, 1])

    ax1.plot(months, demand, "o-", label="Nhu cầu thực tế", color="#1f77b4")
    ax1.plot(months, pred1, "--", label="Dự báo (model train 12 tháng đầu)", color="#d62728")
    ax1.plot(months[6:], pred2[6:], "-.", label="Dự báo (retrain tháng 18)", color="#2ca02c")
    ax1.axvline(12, color="gray", ls=":", lw=1.5)
    ax1.text(12.2, ax1.get_ylim()[1] * 0.95, "deploy", color="gray", fontsize=9)
    ax1.axvline(18, color="gray", ls=":", lw=1.5)
    ax1.text(18.2, ax1.get_ylim()[1] * 0.95, "retrain", color="gray", fontsize=9)
    ax1.set_ylabel("Nhu cầu")
    ax1.set_title("Model tốt lúc bàn giao vẫn hỏng dần vì thế giới thay đổi")
    ax1.legend(loc="upper left", fontsize=9)

    ax2.bar(months, mae1, color="#d62728", alpha=0.6, label="MAE model cũ")
    ax2.plot(months[18:], mae2[18:], "o-", color="#2ca02c", label="MAE sau retrain")
    ax2.set_xlabel("Tháng")
    ax2.set_ylabel("MAE")
    ax2.legend(fontsize=9)

    save(fig, "01_model_decay.png")


if __name__ == "__main__":
    main()

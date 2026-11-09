"""
Demo 5 — Slide 14 & 15: phát hiện shift

Phần A: summary statistics + KS test + MMD (1D và đa biến).
Phần B: cùng dữ liệu, chọn cửa sổ khác nhau → kết luận khác nhau.
Phần C: sliding statistics vs cumulative statistics (Figure 8-4).

Chạy: python 05_detect_shift.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import (
    ks_perm_test,
    mmd_perm_test,
    print_stats_table,
    save,
    setup,
)


def main():
    setup()
    rng = np.random.default_rng(21)

    # ------------------------------------------------------------------
    # A. Summary stats + two-sample tests
    # ------------------------------------------------------------------
    print("=== DEMO 5A: summary statistics & two-sample test ===")
    source = rng.normal(0.0, 1.0, 1500)
    same = rng.normal(0.0, 1.0, 1500)
    shifted = rng.normal(0.6, 1.3, 1500)

    print("\n[Không shift] source vs target cùng phân phối")
    print_stats_table(source, same)

    print("\n[Có shift] source vs target khác phân phối")
    print_stats_table(source, shifted)

    for name, target in [("cùng phân phối", same), ("khác phân phối", shifted)]:
        ks, p_ks = ks_perm_test(source, target, n_perm=1000)
        mmd, p_mmd = mmd_perm_test(source[:, None], target[:, None], n_perm=300)
        print(f"\n{name:>16}: KS D={ks:.4f}, p={p_ks:.4f} | MMD²={mmd:.5f}, p={p_mmd:.4f}")

    print("\nLưu ý: p-value nhỏ → bác bỏ 'cùng phân phối'.")
    print("Nhưng ý nghĩa thống kê ≠ ý nghĩa thực tiễn: mẫu càng lớn, test càng nhạy.")

    # ------------------------------------------------------------------
    # B. Time-scale window: cửa sổ bỏ sót thứ 2 vs cửa sổ đủ chu kỳ tuần
    # ------------------------------------------------------------------
    weekly = np.array([1.5, 0.0, -0.5, -1.0, -0.8, -0.3, 0.5])  # Thứ 2 → CN
    n_weeks = 12
    n_days = n_weeks * 7 + 1
    days = np.arange(1, n_days + 1)
    weekday = (days - 1) % 7

    daily_mean = weekly[weekday] + rng.normal(0, 0.15, n_days)
    daily_mean[-1] = weekly[0]          # ngày cuối là thứ 2 "bình thường"

    short_mask = (days < n_days) & (weekday != 0)   # cửa sổ bỏ sót thứ 2
    long_mask = days < n_days                       # đủ 12 tuần
    last = np.array([daily_mean[-1]])

    _, p_short = ks_perm_test(daily_mean[short_mask], last, n_perm=500)
    _, p_long = ks_perm_test(daily_mean[long_mask], last, n_perm=500)

    print("\n=== DEMO 5B: cửa sổ thời gian ===")
    print(f"Cửa sổ bỏ sót thứ 2 (Tue–Sun) vs ngày cuối: KS p = {p_short:.4f}  → {'BÁO SHIFT' if p_short < 0.05 else 'không shift'}")
    print(f"Cửa sổ đủ 12 tuần            vs ngày cuối: KS p = {p_long:.4f}  → {'BÁO SHIFT' if p_long < 0.05 else 'không shift'}")
    print("Cùng dữ liệu, chỉ đổi cửa sổ baseline → kết luận trái ngược.")
    print("Vì dữ liệu có chu kỳ tuần; cửa sổ ngắn bỏ sót chu kỳ → false alarm.")

    # ------------------------------------------------------------------
    # C. Sliding vs cumulative accuracy
    # ------------------------------------------------------------------
    hours = np.arange(24)
    acc_true = np.full(24, 0.90)
    acc_true[16:19] = 0.60          # sự cố giờ 16–18
    samples_per_hour = 800

    observed = np.array([rng.binomial(samples_per_hour, p) / samples_per_hour for p in acc_true])

    window = 4
    sliding = np.array(
        [observed[max(0, h - window + 1) : h + 1].mean() for h in hours]
    )
    cumulative = np.array([observed[: h + 1].mean() for h in hours])

    print("\n=== DEMO 5C: sliding vs cumulative ===")
    print(f"Accuracy thật giờ 17          : {acc_true[17]:.2f}")
    print(f"Sliding (4h) tại giờ 18       : {sliding[18]:.2f}  ← thấy cú sụt")
    print(f"Cumulative tại giờ 18         : {cumulative[18]:.2f}  ← che mất cú sụt")
    print("→ Cumulative bị pha loãng bởi dữ liệu cũ.")

    # ------------------------------------------------------------------
    # Hình
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))

    ax = axes[0]
    ax.plot(days, daily_mean, "o-", ms=3, lw=1, color="#1f77b4", label="Trung bình ngày")
    ax.scatter(days[-1], daily_mean[-1], s=90, color="#d62728", zorder=5, label="Ngày cuối (thứ 2)")
    ax.axhline(weekly[0], color="gray", ls="--", lw=1, label="Mức thứ 2 bình thường")
    ax.set_xlabel("Ngày (12 tuần + 1 ngày)")
    ax.set_ylabel("Giá trị trung bình")
    ax.set_title(f"Cửa sổ thiếu thứ 2: p={p_short:.3f} | đủ chu kỳ: p={p_long:.3f}")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.plot(hours, observed, "o", alpha=0.45, label="accuracy từng giờ", color="gray")
    ax.plot(hours, sliding, "-", lw=2, label="sliding 4 giờ", color="#d62728")
    ax.plot(hours, cumulative, "--", lw=2, label="cumulative", color="#2ca02c")
    ax.axvspan(16, 18, alpha=0.12, color="#d62728")
    ax.set_xlabel("Giờ")
    ax.set_ylabel("Accuracy")
    ax.set_title("Cumulative che mất sự cố ngắn hạn")
    ax.legend(fontsize=9)

    save(fig, "05_detect_shift.png")


if __name__ == "__main__":
    main()

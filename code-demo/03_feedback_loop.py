"""
Demo 3 — Slide 7 & 8: Degenerate feedback loop

Phần A: hai bài hát chất lượng NHƯ NHAU. Chỉ vì A được hiển thị trước,
A được click nhiều hơn → model càng xếp A cao → popularity bias.
So sánh greedy vs epsilon-greedy (randomization).

Phần B: hit rate theo bucket popularity — model giỏi hơn hẳn ở item phổ biến.

Chạy: python 03_feedback_loop.py
"""

import numpy as np
import matplotlib.pyplot as plt

from common import save, setup

TRUE_CTR = np.array([0.10, 0.10])      # chất lượng thật bằng nhau
POS_MULT = np.array([1.0, 0.4])        # vị trí 1 được click nhiều gấp 2,5 lần


def simulate(eps=0.0, rounds=100, users=2000, seed=0):
    """eps=0 → greedy; eps>0 → epsilon-greedy (randomize order)."""
    rng = np.random.default_rng(seed)
    clicks = np.zeros(2)
    exposures = np.zeros(2)
    weighted_exposures = np.zeros(2)   # exposures × position multiplier
    first_share = []
    naive_gap = []

    for r in range(rounds):
        est = (clicks + 1) / (exposures + 20)  # smoothing
        if rng.random() < eps:
            order = rng.permutation(2)
        else:
            order = np.argsort(-est)
            if r == 0:
                order = np.array([0, 1])       # tie-break: A đứng đầu

        for pos, item in enumerate(order):
            p = TRUE_CTR[item] * POS_MULT[pos]
            clicks[item] += rng.binomial(users, p)
            exposures[item] += users
            weighted_exposures[item] += users * POS_MULT[pos]

        first_share.append(1.0 if order[0] == 0 else 0.0)
        naive = clicks / exposures
        naive_gap.append(naive[0] - naive[1])

    naive = clicks / exposures
    debiased = clicks / weighted_exposures
    return {
        "first_share": np.array(first_share),
        "naive_gap": np.array(naive_gap),
        "naive": naive,
        "debiased": debiased,
    }


def popularity_buckets(n_items=1000, n_buckets=3, seeds=5):
    """Item phổ biến có nhiều dữ liệu → model ước lượng chính xác hơn.

    Chia item theo độ phổ biến: 50% ít phổ biến, 30% trung bình, 20% phổ biến.
    Lấy trung bình nhiều seed để hit rate ổn định.
    """
    fracs = (0.5, 0.3, 0.2)
    all_rates = []

    for seed in range(seeds):
        rng = np.random.default_rng(seed)
        popularity = rng.pareto(1.5, n_items) + 1.0
        true_ctr = 0.05 + 0.10 * popularity / popularity.max()

        exposures = popularity * 1000
        clicks = rng.binomial(exposures.astype(int), true_ctr)
        estimated = (clicks + 1) / (exposures + 20)

        order = np.argsort(popularity)
        cuts = (np.cumsum(fracs)[:-1] * n_items).astype(int)
        buckets = np.split(order, cuts)

        rates = []
        for bucket in buckets:
            k = max(3, len(bucket) // 5)
            true_top = set(bucket[np.argsort(-true_ctr[bucket])[:k]])
            est_top = bucket[np.argsort(-estimated[bucket])[:k]]
            rates.append(len(true_top & set(est_top)) / k)
        all_rates.append(rates)

    return np.mean(all_rates, axis=0)


def main():
    setup()
    greedy = simulate(eps=0.0, seed=2)
    epsilon = simulate(eps=0.3, seed=3)
    hit_rates = popularity_buckets()

    print("=== DEMO 3: degenerate feedback loop ===")
    print("Hai bài A/B có chất lượng thật như nhau (CTR thật = 0.10).")
    print()
    print(f"{'policy':>16} | {'A đứng đầu':>10} | {'CTR naive A':>11} | {'CTR naive B':>11} | {'gap':>7}")
    print("  " + "-" * 66)
    for name, res in [("greedy", greedy), ("epsilon-greedy", epsilon)]:
        print(
            f"{name:>16} | {res['first_share'].mean():>9.0%} | "
            f"{res['naive'][0]:>11.3f} | {res['naive'][1]:>11.3f} | "
            f"{res['naive'][0] - res['naive'][1]:>+7.3f}"
        )
    print()
    print("Sau 100 vòng, greedy kết luận A tốt hơn B — dù sự thật là bằng nhau.")
    print(f"Debiased (chia cho position multiplier): A={greedy['debiased'][0]:.3f}, B={greedy['debiased'][1]:.3f}")
    print("→ Naive CTR học luôn cả bias vị trí; debiased khôi phục chất lượng thật.")
    print()
    print("Hit rate theo bucket popularity (thấp → cao):")
    for i, hr in enumerate(hit_rates, 1):
        print(f"  bucket {i}: {hr:.2f}")
    print("→ Model giỏi hơn hẳn ở item phổ biến = dấu hiệu popularity bias.")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))

    # (1) Tỷ lệ A được đặt vị trí 1
    ax = axes[0]
    ax.plot(greedy["first_share"], label="Greedy", color="#d62728", lw=2)
    ax.plot(epsilon["first_share"], label="ε-greedy (30% random)", color="#2ca02c", lw=2)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("Vòng")
    ax.set_ylabel("Tỷ lệ A đứng vị trí 1")
    ax.set_title("Vị trí hiển thị bị khoá bởi model")
    ax.legend(fontsize=9)

    # (2) Naive vs debiased CTR
    ax = axes[1]
    x = np.arange(2)
    width = 0.2
    ax.bar(x - 1.5 * width, greedy["naive"], width, label="Naive (greedy)", color="#d62728")
    ax.bar(x - 0.5 * width, greedy["debiased"], width, label="Debiased (greedy)", color="#2ca02c")
    ax.bar(x + 0.5 * width, epsilon["naive"], width, label="Naive (ε-greedy)", color="#ff9896")
    ax.bar(x + 1.5 * width, epsilon["debiased"], width, label="Debiased (ε-greedy)", color="#98df8a")
    ax.axhline(0.10, color="k", ls=":", lw=1, label="CTR thật = 0.10")
    ax.set_xticks(x, ["Bài A", "Bài B"])
    ax.set_ylabel("CTR ước lượng")
    ax.set_title("Bias vị trí làm sai lệch CTR")
    ax.legend(fontsize=7, ncol=1)

    # (3) Hit rate theo popularity bucket
    ax = axes[2]
    labels = ["Ít phổ biến\n(50% item)", "Trung bình\n(30%)", "Phổ biến\n(20%)"]
    colors = ["#d62728", "#ff7f0e", "#2ca02c"]
    ax.bar(labels, hit_rates, color=colors)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Hit rate")
    ax.set_title("Hit rate theo bucket popularity")
    ax.tick_params(axis="x", rotation=15)

    save(fig, "03_feedback_loop.png")


if __name__ == "__main__":
    main()

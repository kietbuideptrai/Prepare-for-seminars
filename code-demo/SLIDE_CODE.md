# Snippet code để dán lên slide

Mỗi snippet dưới đây là bản rút gọn **5–15 dòng** để chiếu lên slide. Code đầy đủ chạy được nằm ở các file `01_*.py` … `07_*.py`, và bản notebook ở `../notebooks/`.

> **Nguyên tắc:** slide chỉ giữ đúng 1 ý. Snippet để chứng minh ý đó là thật, không phải để dạy lập trình.
> Hướng dẫn tạo slide đầy đủ: [../README.md](../README.md).

---

## Slide 2 & 5 — Model hỏng dần sau deploy

```python
# Train 12 tháng đầu, deploy, rồi đo MAE theo thời gian
w1 = fit_linear(X[:12], demand[:12])

mae_dau  = np.abs(predict_linear(X[12:18], w1) - demand[12:18]).mean()
mae_cuoi = np.abs(predict_linear(X[18:24], w1) - demand[18:24]).mean()

print(f"{mae_dau:.1f} → {mae_cuoi:.1f}")   # 4.9 → 18.8
```

**Nói:** “Model không đổi, nhưng thế giới đổi. Sai số tăng gần 4 lần chỉ sau một năm.”

---

## Slide 3 & 4 — Failure taxonomy (pseudo-code)

```python
def is_failure(latency_ms, accuracy, slo_latency=200, slo_acc=0.90):
    operational_failure = latency_ms > slo_latency
    ml_failure = accuracy < slo_acc
    return operational_failure, ml_failure

# ML thường fail silently: accuracy cần ground truth mới biết
```

**Nói:** “Hệ thống không sập chưa chắc là hệ thống đúng. Không có nhãn thì model có thể sai hàng loạt mà không ai biết.”

---

## Slide 6 — Một outlier phá decision boundary

```python
w_clean = train_logreg(X, y)
w_dirty = train_logreg(
    np.vstack([X, outlier]),   # outlier = [[5, 5]]
    np.r_[y, 0],               # nhưng bị gán nhãn 0
)

print(accuracy(y_test, predict(X_test, w_clean)))  # 0.99
print(accuracy(y_test, predict(X_test, w_dirty)))  # 0.82
```

**Nói:** “Chỉ một mẫu cực đoan cũng đủ kéo boundary và làm model sai hàng loạt trên dữ liệu sạch.”

---

## Slide 7 & 8 — Degenerate feedback loop

```python
for round in range(100):
    est = clicks / exposures
    order = np.argsort(-est)          # greedy: xếp theo CTR ước lượng

    for pos, item in enumerate(order):
        p = true_ctr[item] * pos_mult[pos]   # vị trí 1 được click nhiều hơn
        clicks[item] += rng.binomial(users, p)
        exposures[item] += users
```

**Sửa bias vị trí:**

```python
naive    = clicks / exposures
debiased = clicks / (exposures * pos_mult)   # chia cho position multiplier

print(naive)      # A=0.099, B=0.040  → sai
print(debiased)   # A=0.099, B=0.100  → đúng
```

**Nói:** “A và B chất lượng bằng nhau. Greedy kết luận A tốt hơn chỉ vì A được hiển thị trước.”

---

## Slide 9 — Công thức phân rã

```latex
P(X,Y) = P(Y \mid X)\,P(X) = P(X \mid Y)\,P(Y)
```

| Thành phần | Nghĩa |
|---|---|
| $P(X)$ | phân phối input |
| $P(Y)$ | phân phối nhãn |
| $P(Y \mid X)$ | quy luật input → output |
| $P(X \mid Y)$ | phân phối input trong từng lớp |

---

## Slide 10 — Covariate shift & importance weighting

```python
# P(X) đổi, P(Y|X) giữ nguyên
# Nếu biết trước phân phối target:
w = p_target(x) / p_train(x)          # density ratio

model.fit(X_train, y_train, sample_weight=w)
```

**Nói:** “Trọng số giúp mẫu train giống thế giới thật hơn. Nhưng thực tế thường không biết trước phân phối sẽ đổi thế nào.”

---

## Slide 11 — Label shift

```python
# P(Y) đổi, P(X|Y) giữ nguyên
y_source = rng.binomial(1, 0.50, n)
y_target = rng.binomial(1, 0.10, n)

def sample(y):
    return np.where(y == 1,
                    rng.normal(1.0, 1.0, n),
                    rng.normal(-1.0, 1.0, n))

X_source, X_target = sample(y_source), sample(y_target)
```

**Nói:** “Tỷ lệ nhãn đổi từ 50% xuống 10%, nhưng bên trong mỗi lớp dữ liệu vẫn như cũ.”

---

## Slide 12 — Concept drift

```python
# Cùng X, quy luật đổi
y_source = (X > 0).astype(int)
y_target = (X < 0).astype(int)   # đảo nhãn

print(accuracy(y_target, predict(X, w_source)))   # ~0.00
```

**Nói:** “Căn nhà không đổi, nhưng thị trường định giá nó khác đi. Cùng input, output đã khác.”

---

## Slide 13 — Label schema change

```python
# 3 lớp → 4 lớp: tách NEGATIVE thành SAD / ANGRY
label_map_3 = {"POSITIVE": 0, "NEGATIVE": 1, "NEUTRAL": 2}
label_map_4 = {"POSITIVE": 0, "SAD": 1, "ANGRY": 2, "NEUTRAL": 3}

# Softmax layer cuối: [hidden_units × n_classes]
# 3 → 4 lớp ⇒ đổi kích thước + relabel + retrain from scratch
```

**Nói:** “Không chỉ phân phối đổi — đôi khi chính cấu trúc nhãn đổi, và model phải đổi theo.”

---

## Slide 14 — Accuracy không đủ: summary statistics

```python
for name in ["min", "max", "mean", "median",
             "var", "q05", "q95", "skew", "kurtosis"]:
    print(name, summary_stats(x_prod)[name])
```

**Nói:** “Accuracy cần nhãn và thường đến muộn. Summary statistics cho tín hiệu sớm hơn — nhưng giống nhau không đảm bảo không shift.”

---

## Slide 15 — KS test, MMD & time window

```python
ks, p_ks = ks_perm_test(train_feature, prod_feature)
mmd, p_mmd = mmd_perm_test(train_features_2d, prod_features_2d)

print(f"KS  D={ks:.3f}, p={p_ks:.4f}")     # 1 chiều
print(f"MMD  ={mmd:.4f}, p={p_mmd:.4f}")  # đa biến
```

**Sliding vs cumulative:**

```python
sliding    = [acc[max(0, h-3):h+1].mean() for h in range(24)]
cumulative = [acc[:h+1].mean() for h in range(24)]
```

**Nói:** “Cùng dữ liệu, chọn cửa sổ khác nhau có thể ra kết luận trái ngược.”

---

## Slide 16 & 17 — Retrain: chọn cửa sổ

```python
for window_days in [7, 30, 90, 180]:
    mask = day >= DAYS - window_days
    model = train_logreg(X[mask], y[mask])
    print(window_days, accuracy(y_test, predict(X_test, model)))

# 7 ngày: 0.967 | 30 ngày: 0.970 | 90 ngày: 0.949 | 180 ngày: 0.867
```

**Stateless vs stateful:**

```python
w_base = train_logreg(X_old, y_old)          # checkpoint cũ
w_new  = train_logreg(X_new, y_new, w0=w_base)  # fine-tune
```

**Nói:** “Không có cửa sổ retrain đúng cho mọi bài toán. Cũ quá thì học quy luật lỗi thời; mới quá thì thiếu dữ liệu.”

---

## Slide 18 — SLO / uptime

```python
for uptime in [99.99, 99.999]:
    downtime = (100 - uptime) / 100 * 30 * 24 * 60
    print(f"{uptime}% → {downtime:.1f} phút/tháng")

# 99.99%  → 4.3 phút/tháng
# 99.999% → 0.4 phút ≈ 26 giây/tháng
```

**Nói:** “Hệ thống ‘up’ chưa đủ — nếu dự đoán rác thì vẫn là hệ thống hỏng.”

---

## Slide 19 — Bốn artifact cần monitor

```python
artifacts = [
    ("raw_inputs",  monitor_raw_inputs),
    ("features",    monitor_features),
    ("predictions", monitor_predictions),
    ("accuracy",    monitor_accuracy),
]

for name, monitor in artifacts:
    monitor()   # càng sâu pipeline càng gần ground truth, nhưng càng trễ
```

**Nói:** “Bốn tầng: raw → features → predictions → accuracy. Càng sâu càng đúng, nhưng càng khó và càng trễ.”

---

## Slide 20 — Alert template

```python
alert = {
    "policy": "accuracy < 0.90 trong 10 phút",
    "channels": ["slack:#mlops-monitoring", "pagerduty"],
    "description": "Recommender accuracy dropped",
    "runbook": "kiểm tra schema → version model → feature consistency",
}
```

**Nói:** “Giám sát không chỉ là vẽ graph — mà là biết ai sẽ bị gọi lúc 2 giờ sáng, và alert đó có thật sự quan trọng không.”

---

## Slide 21 — Observability: tag để slice

```python
log = {
    "request_id": rid,
    "user_id": uid,
    "zip_code": zip_code,
    "model": "A",
    "prediction": pred,
    "latency_ms": ms,
}

# Query: user nào model A dự đoán sai 1 giờ qua, group by zip code?
```

**Nói:** “Monitoring trả lời ‘khi nào’. Observability trả lời ‘cái gì, ở đâu, tại sao’.”

---

## Backup — Importance weighting đầy đủ

```python
# Ước lượng density ratio bằng histogram (minh hoạ)
p_train, edges = np.histogram(x_train, bins=30, density=True)
p_target, _    = np.histogram(x_target, bins=edges, density=True)

bin_id = np.clip(np.digitize(x_train, edges) - 1, 0, len(p_train) - 1)
w = p_target[bin_id] / np.maximum(p_train[bin_id], 1e-12)

model.fit(X_train, y_train, sample_weight=w)
```

## Backup — Feature validation (pseudo-code)

```python
assert df["age"].between(0, 120).all()
assert df["income"] >= 0
assert df["country"].isin(["VN", "US", "JP"]).all()
assert df["end_date"] >= df["start_date"]
# Great Expectations / Deequ làm đúng những việc này ở production
```

## Backup — MMD với RBF kernel

```python
def mmd2(X, Y, gamma):
    K = lambda A, B: np.exp(-gamma * ((A[:,None,:] - B[None,:,:])**2).sum(-1))
    return K(X,X).mean() - 2*K(X,Y).mean() + K(Y,Y).mean()
```

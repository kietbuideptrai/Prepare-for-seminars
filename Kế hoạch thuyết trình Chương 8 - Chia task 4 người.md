---
title: "Kế hoạch thuyết trình Chương 8 — Chia task 4 người"
tags:
  - thuyet-trinh
  - ml-system
  - ke-hoach
  - data-distribution-shift
nguồn: "[[Chương 8 - Data Distribution Shifts và Monitoring]]"
thời-lượng: "30 phút + 5 phút Q&A"
---

# Kế hoạch thuyết trình Chương 8 — Chia task 4 người

> [!info] Tóm tắt
> **4 người — 22 slide — 30 phút thuyết trình + 5 phút Q&A.**
> Mỗi người phụ trách một “chương con” có mở đầu và kết thúc rõ ràng, bàn giao bằng một câu chuyển ý để cả bài liền mạch.
> Sơ đồ tổng thể: [[Ch8 - Data Distribution Shifts.excalidraw|Sơ đồ tư duy Chương 8]].

> [!important] Thông điệp xuyên suốt
> **Deploy không phải là đích.** Model sẽ giảm hiệu năng vì dữ liệu production khác dữ liệu train, vì edge cases, và vì chính dự đoán của model tạo ra vòng lặp phản hồi. Muốn giữ model hoạt động phải **monitor → hiểu → retrain**.

> [!tip] Dàn ý slide chi tiết
> Tiêu đề + bullet + visual + lời dẫn cho từng slide: [[Dàn ý slide thuyết trình Chương 8 - 22 slide]].

---

## 1. Mục tiêu & ba điều khán giả phải nhớ

Sau buổi thuyết trình, khán giả cần nhớ được:

1. **Model hỏng trong production là chuyện bình thường**, không phải ngoại lệ. Có hai nhóm nguyên nhân: **software system failures** và **ML-specific failures**; ML thường **fail silently**.
2. **Ba cái bẫy ML-specific**: dữ liệu production khác dữ liệu train (**train-serving skew**), **edge cases**, và **degenerate feedback loops**. Trong đó data shift gồm **covariate shift**, **label shift**, **concept drift** (và các dạng như feature/label schema change).
3. **Quy trình giữ model sống**: phát hiện shift bằng metric/thống kê → chọn cách ứng phó (retrain, domain adaptation, thiết kế robust) → **monitoring + observability** để biết “khi nào” và “tại sao”.

**Phong cách trình bày:** kể chuyện → ví dụ → kết luận. Không đọc slide, không đọc định nghĩa nguyên văn.

---

## 2. Phân công tổng quan

| Thành viên | Phần phụ trách | Slide | Thời lượng | Vai trò phụ |
|---|---|---|---|---|
| **Người 1** | Mở đầu, failure taxonomy, software failures, train-serving skew | 1–5 | ~6 phút | MC, giữ nhịp, mở và kết nối |
| **Người 2** | Edge cases + degenerate feedback loops (phát hiện & sửa) | 6–8 | ~7 phút | Phụ trách ví dụ/demo, hình ảnh |
| **Người 3** | Data distribution shifts + cách phát hiện | 9–15 | ~9 phút | Fact-check công thức, số liệu, thuật ngữ |
| **Người 4** | Ứng phó shift + monitoring/observability + tổng kết + Q&A | 16–22 | ~8 phút | Slide master, điều phối Q&A, nộp bài |

> [!tip] Vì sao Người 3 nhiều thời gian hơn?
> Phần shift + detection có **công thức, 5 loại shift và 4 nhóm phương pháp thống kê** — nặng nhất về khái niệm. Người 1 và Người 2 bù lại bằng phần kể chuyện và ví dụ trực quan. Nếu muốn cân bằng tuyệt đối, cắt bớt phần **importance weighting** và **MMD/LSDD** của Người 3, chuyển thành backup slide.

---

## 3. Kịch bản 22 slide

| # | Nội dung | Người | Phút | Visual / ghi chú |
|---|---|---|---|---|
| 1 | Title, thành viên, agenda, câu hỏi hook | 1 | 0,5 | Ảnh grocery / câu hỏi “Deploy xong là xong chưa?” |
| 2 | Câu chuyện model dự báo nhu cầu tạp hoá | 1 | 1,5 | Timeline: 6 tháng xây → 1 năm sau hỏng → 3 lựa chọn |
| 3 | Failure là gì? Operational vs ML performance; fail silently | 1 | 1 | 2 cột; ví dụ dịch Anh–Pháp |
| 4 | Software failures vs ML-specific failures; 60/96 vụ Google | 1 | 1,5 | Bảng 4 loại software failure; donut 60/96 |
| 5 | Train-serving skew: giả định stationary sai vì đâu | 1 | 1,5 | 2 lý do; ví dụ “Wuhan”; sudden/gradual/seasonal; 80% lỗi người |
| 6 | Edge cases vs outliers; xe tự lái 99,99% | 2 | 2 | Poll “Bạn có dùng không?”; bảng outlier vs edge case |
| 7 | Degenerate feedback loops: định nghĩa + ví dụ bài hát/CV | 2 | 3 | Sơ đồ vòng lặp; ranking A/B; CV + feature X |
| 8 | Phát hiện & sửa feedback loops | 2 | 2 | Popularity bucket; TikTok pool; bảng positional features |
| 9 | Data shift là gì? Source/target + công thức | 3 | 1,5 | $P(X,Y)=P(Y \vert X)P(X)=P(X \vert Y)P(Y)$ |
| 10 | Covariate shift | 3 | 1 | Ví dụ ung thư vú; importance weighting |
| 11 | Label shift | 3 | 1 | Ví dụ ung thư vú; thuốc phòng ngừa |
| 12 | Concept drift | 3 | 0,5 | Giá nhà SF; mùa vụ ride-hailing |
| 13 | Feature change + label schema change | 3 | 1 | Age năm→tháng; credit score; sentiment 3→4 lớp |
| 14 | Phát hiện: accuracy metrics + summary statistics | 3 | 2 | Accuracy cần nhãn/trễ; min/max/mean/quantile; hạn chế |
| 15 | Two-sample test + time-scale windows | 3 | 2 | KS 1D; MMD/LSDD/Alibi Detect; sliding vs cumulative |
| 16 | Ba hướng ứng phó + retrain stateless/stateful | 4 | 1,5 | Bảng 3 hướng; câu hỏi “train lại từ đầu hay train tiếp?” |
| 17 | Thiết kế robust: feature ổn định, model theo thị trường | 4 | 1 | App ranking bucket; SF vs rural Arizona |
| 18 | Monitoring vs observability; operational metrics; SLO/SLA | 4 | 1,5 | 99,99% ≈ 4 phút/tháng; 99,999% ≈ 26 giây |
| 19 | 4 artifact: accuracy → predictions → features → raw inputs | 4 | 1,5 | Pipeline 4 tầng; YouTube CTR/completion; Great Expectations |
| 20 | Toolbox: logs, dashboards, alerts | 4 | 1 | Badoo 20 tỷ event/ngày; dashboard rot; alert fatigue |
| 21 | Observability: telemetry, tag, slicing, interpretability | 4 | 1 | Câu query “group by zip code”; feature importance |
| 22 | Tổng kết 3 điều mang đi + mind map + Q&A | 4 | 0,5 | Dùng lại sơ đồ tư duy; mời đặt câu hỏi |

> [!note] Tổng thời gian
> 6 + 7 + 9 + 8 = **30 phút**. Nếu chạy thử thấy lố, cắt theo thứ tự: chi tiết software failures → chi tiết logs → importance weighting → MMD/LSDD (đưa vào backup).

---

## 4. Nhiệm vụ chi tiết từng người

### Người 1 — “Vì sao model chết sau deploy?”

**Mục tiêu phần:** hook khán giả, chứng minh deploy chỉ là bắt đầu, phân biệt hai nhóm failure, dẫn vào train-serving skew.

**Nội dung bắt buộc:**

- Câu chuyện mở đầu:
  - Công ty thuê tư vấn 6 tháng xây model dự báo nhu cầu hàng tạp hoá.
  - Một năm sau: mặt hàng bị dự báo cao → hết hạn; bị dự báo thấp → mất doanh thu.
  - Sửa tay không cứu được; 3 lựa chọn: trả tiền tư vấn cũ, thuê tư vấn mới, hoặc tự lập đội in-house.
  - Bài học: **deploy không phải đích; hiệu năng giảm theo thời gian**.
- Failure:
  - Failure = vi phạm một kỳ vọng.
  - **Operational expectation** (latency, throughput) vs **ML performance expectation** (accuracy 99%).
  - Ví dụ dịch Anh–Pháp: không có bản dịch → operational failure; sai liên tục → ML performance failure.
  - **Fail silently**: không có nhãn thì không biết model sai.
- Software system failures:
  - Dependency, deployment, hardware, downtime/crashing.
  - Google 2020: **60/96 vụ** pipeline ML hỏng có nguyên nhân không trực tiếp liên quan ML.
  - Kết luận: **ML engineering chủ yếu là engineering**.
- ML-specific failures:
  - Data collection/processing, hyperparameter, train/inference pipeline lệch nhau, data shift, edge cases, feedback loops.
  - Chỉ chiếm phần nhỏ nhưng **khó phát hiện, khó sửa, có thể làm hệ thống không dùng được**.
- Train-serving skew:
  - Giả định train/test cùng phân phối stationary là sai vì:
    1. Dữ liệu thật đa dạng, tập train hữu hạn + selection/sampling bias.
    2. Thế giới không stationary: đột ngột, dần dần, theo mùa.
  - Ví dụ “Wuhan” trước và sau COVID-19.
  - Cảnh báo: **~80% drift** trên dashboard có thể là lỗi con người/pipeline, không phải shift thật.

**Ví dụ/visual nên dùng:**

- Timeline câu chuyện (6 tháng → 1 năm → 3 lựa chọn).
- Bảng 2 cột Operational vs ML performance.
- Donut **60/96**.
- Sơ đồ đơn giản: “Training distribution” và “Production distribution” lệch nhau → **train-serving skew**.

**Câu chốt:**

> “Deploy là bắt đầu, không phải kết thúc. Model sẽ hỏng — câu hỏi là hỏng vì đâu.”

**Câu chuyển ý sang Người 2:**

> “Ngoài dữ liệu lệch, còn hai cái bẫy rất ‘ML’: những mẫu cực đoan và những vòng lặp do chính model tạo ra.”

**Checklist:**

- [ ] Kể story trong **90 giây**, không lan man.
- [ ] Phân biệt rõ operational vs ML performance bằng 1 ví dụ.
- [ ] Nêu đúng **60/96** và ý nghĩa.
- [ ] Giải thích train-serving skew bằng 2 lý do, không đọc định nghĩa.
- [ ] Nói rõ **80% drift có thể là lỗi người** để chuẩn bị cho phần sau.

---

### Người 2 — “Hai cái bẫy ML-specific: edge cases & feedback loops”

**Mục tiêu phần:** khán giả thấy được vì sao model tốt trên trung bình vẫn có thể không dùng được, và vì sao model có thể tự làm hỏng dữ liệu train của chính nó.

**Nội dung bắt buộc:**

#### Edge cases

- Câu hỏi mở: xe tự lái an toàn **99,99%**, 0,01% còn lại có thể gây tai nạn chết người — bạn có dùng?
- Định nghĩa: mẫu dữ liệu **cực đoan** khiến model mắc lỗi **thảm khốc**.
- **Outlier vs edge case**:
  - Outlier nói về **dữ liệu** (khác biệt).
  - Edge case nói về **hiệu năng** (model làm tệ hơn đáng kể).
  - Người đi bộ sang đường trái phép là outlier, nhưng không phải edge case nếu xe nhận ra và xử lý an toàn.
- Trong train có thể loại outlier; trong inference **không thể loại bỏ** truy vấn lạ.
- Phạm vi: safety-critical (y tế, giao thông, e-discovery) và cả brand risk (chatbot nói nội dung phân biệt).

#### Degenerate feedback loops

- Định nghĩa: **output của hệ thống → input tương lai → output tương lai**.
- Ví dụ bài hát:
  - A và B chênh nhau rất ít.
  - A được xếp cao hơn → hiển thị trước → click nhiều → model càng xếp A cao.
  - Hệ quả: **popularity bias / filter bubble / echo chamber**; item mới khó chen vào.
- Ví dụ CV:
  - Model thấy feature X dự đoán tốt → đề xuất CV có X.
  - Recruiter chỉ phỏng vấn người có X → công ty chỉ tuyển người có X → model càng tin X.
  - X có thể là “Stanford”, “Google”, hoặc “là nam” → **khuếch đại bias**.
- Phát hiện:
  - Đo **popularity diversity** / độ phủ long-tail.
  - **Hit rate against popularity**: chia item theo bucket độ phổ biến, so accuracy từng bucket; giỏi hơn hẳn ở item phổ biến → popularity bias.
  - Trên production: dự đoán **ngày càng đồng nhất** → nghi ngờ feedback loop.
- Sửa:
  - **Randomization**: TikTok gán mỗi video mới một pool traffic ngẫu nhiên (có thể đến hàng trăm impression) để đánh giá chất lượng không thiên lệch.
  - Đánh đổi: randomization làm giảm trải nghiệm người dùng → dùng **contextual bandits**, randomization nhỏ + **causal inference** (Schnabel et al.).
  - **Positional features**: thêm feature “có ở vị trí 1 hay không” khi train; khi inference đặt `False` để dự đoán click bất kể vị trí.
  - Cách tinh vi: **2 model** — model 1 dự đoán user có nhìn thấy/cân nhắc (có vị trí), model 2 dự đoán click (không vị trí).

**Ví dụ/visual nên dùng:**

- Poll nhanh: “Nếu bài A được hiển thị đầu tiên, bạn có click không?” → cho thấy bias vị trí.
- Sơ đồ vòng lặp: Prediction → User behavior → Training data → Prediction.
- Bảng 8-1 rút gọn (5 dòng) để minh hoạ positional features.
- Logo/ảnh TikTok (nếu được phép) hoặc mô phỏng “pool traffic”.

**Câu chốt:**

> “Model không chỉ học từ dữ liệu — nó còn tạo ra dữ liệu cho chính nó. Nếu không cẩn thận, nó sẽ tự khuếch đại bias của mình.”

**Câu chuyển ý sang Người 3:**

> “Feedback loop là shift do chính hệ thống gây ra. Còn khi thế giới bên ngoài thay đổi, ta gọi đó là gì và đo bằng cách nào?”

**Checklist:**

- [ ] Poll xe tự lái hoặc chatbot độc hại — chọn **một** ví dụ, không kể cả hai.
- [ ] Phân biệt outlier/edge case bằng ví dụ sang đường.
- [ ] Vẽ được vòng lặp trong **10 giây**.
- [ ] Nêu 2 cách sửa, nhấn mạnh **đánh đổi UX** của randomization.
- [ ] Không sa vào chi tiết code/Toán.

---

### Người 3 — “Data distribution shift: bản đồ & cách phát hiện”

**Mục tiêu phần:** khán giả phân biệt được 3 loại shift, hiểu vì sao phải monitor nhiều thứ khác ngoài accuracy, và biết các công cụ thống kê cơ bản.

**Nội dung bắt buộc:**

#### Định nghĩa & toán học

- **Source distribution** (train) vs **target distribution** (inference).
- Data shift: dữ liệu thay đổi theo thời gian → dự đoán kém chính xác dần.
- Công thức:

$$
P(X,Y) = P(Y \vert X)P(X) = P(X \vert Y)P(Y)
$$

- $P(Y \vert X)$: xác suất output khi biết input; $P(X)$: phân phối input; $P(Y)$: phân phối output.

#### Ba loại shift

| Loại | Điều kiện | Ví dụ |
|---|---|---|
| **Covariate shift** | $P(X)$ đổi, $P(Y \vert X)$ giữ nguyên | Tuổi trong dữ liệu ung thư vú; marketing kéo user giàu hơn |
| **Label shift** | $P(Y)$ đổi, $P(X \vert Y)$ giữ nguyên | Tỷ lệ ung thư dương tính giảm; prior của lớp đổi |
| **Concept drift** | $P(Y \vert X)$ đổi, $P(X)$ giữ nguyên | Giá nhà SF thời COVID; giá ride-hailing theo mùa |

- **Covariate shift**:
  - Ví dụ ung thư vú: train nhiều phụ nữ > 40 hơn inference, nhưng với cùng độ tuổi, xác suất bệnh không đổi.
  - Nguyên nhân: selection bias, oversample lớp hiếm, active learning, thay đổi môi trường production.
  - Xử lý: **importance weighting** — ước lượng tỷ lệ mật độ target/train rồi gán trọng số cho mẫu train.
- **Label shift**:
  - Ví dụ: train có nhiều nhãn dương hơn; nhưng với người đã mắc bệnh, phân phối tuổi vẫn như cũ.
  - Ví dụ thuốc phòng ngừa: $P(Y \vert X)$ giảm ở mọi tuổi → không còn covariate shift, nhưng $P(X \vert Y)$ vẫn giữ → vẫn là label shift.
- **Concept drift**:
  - Cùng input, output khác. Giá nhà SF từ 2 triệu → 1,5 triệu USD.
  - Có thể cyclic/seasonal → dùng model riêng cho ngày thường/cuối tuần.

#### Các dạng khác

- **Feature change**: feature `age` đổi từ năm sang tháng; bug khiến feature toàn NaN.
- **Label schema change**:
  - Credit score đổi range 300–850 → 250–900.
  - Sentiment 3 lớp → 4 lớp (tách NEGATIVE thành SAD/ANGRY).
  - Softmax layer đổi kích thước `[hidden_units × số lớp]` → có thể phải relabel + retrain from scratch.
  - Phổ biến ở **high-cardinality tasks**.

#### Phát hiện

- **Accuracy metrics**: trực tiếp nhất nhưng cần nhãn; nhãn thường **trễ**. Nếu có natural labels thì tận dụng.
- Các phân phối có thể monitor: $P(X)$, $P(Y)$, $P(X \vert Y)$, $P(Y \vert X)$.
  - $P(X)$ không cần nhãn.
  - $P(Y)$ và các phân phối có điều kiện cần nhãn.
  - Industry tập trung vào **phân phối input/feature**.
- **Summary statistics**:
  - min, max, mean, median, variance, quantile 5/25/75/95, skewness, kurtosis.
  - TFX (10/2021) vẫn chỉ dùng summary statistics.
  - Hạn chế: khác nhau → có thể shift; giống nhau → **không đảm bảo** không shift.
- **Two-sample test**:
  - Kiểm định hai tập có cùng phân phối không.
  - Ý nghĩa thống kê ≠ ý nghĩa thực tiễn; heuristic: mẫu nhỏ đã phát hiện → đáng lo; mẫu lớn mới phát hiện → có thể bỏ qua.
  - **KS test**: nonparametric, 1 chiều, tốt cho label/prediction scalar; có thể tốn kém và nhiều false positive.
  - **LSDD**, **MMD** (kernel, đa biến), **Learned Kernel MMD**, **Alibi Detect**.
  - Nên **giảm chiều** trước khi test feature nhiều chiều, nhưng giảm chiều có thể làm test kém hiệu quả.
- **Time-scale windows**:
  - Shift đột ngột dễ phát hiện hơn shift chậm.
  - Spatial shift (user/device mới) vs temporal shift (theo thời gian).
  - Dữ liệu có chu kỳ tuần: cửa sổ < 1 tuần sẽ không thấy chu kỳ.
  - Ví dụ ngày 9–14 vs ngày 1–14: cùng dữ liệu, kết luận khác nhau.
  - **Sliding** (reset mỗi cửa sổ) vs **cumulative** (cộng dồn, có thể che cú sụt giờ 16–18).
  - Thực hành: lấy train làm baseline, monitor theo giờ/ngày; cửa sổ ngắn phát hiện nhanh nhưng dễ false alarm; merge thống kê; RCA tự tìm cửa sổ.

**Ví dụ/visual nên dùng:**

- 3 panel cho covariate/label/concept (cùng một trục input/output).
- Bảng 3 loại shift — **in to**, chỉ giữ 3 dòng.
- Biểu đồ time-series minh hoạ Figure 8-3 (ngày 9–14 vs 1–14).
- Biểu đồ sliding vs cumulative (Figure 8-4).

**Câu chốt:**

> “Shift không chỉ là ‘dữ liệu đổi’. Phải biết **loại nào**, đo bằng **gì**, trong **cửa sổ thời gian nào** — nếu không, rất dễ báo động sai.”

**Câu chuyển ý sang Người 4:**

> “Phát hiện được shift rồi thì làm gì? Câu trả lời không phải ‘train lại là xong’ — mà là chọn đúng cách ứng phó và giám sát hệ thống đủ sâu.”

**Checklist:**

- [ ] Viết đúng công thức, không nhầm $P(Y \vert X)$ với $P(X \vert Y)$.
- [ ] Mỗi loại shift có **đúng 1 ví dụ** — không kể quá nhiều.
- [ ] Nêu được vì sao accuracy không đủ.
- [ ] Phân biệt KS (1D) và MMD (đa biến).
- [ ] Giải thích sliding vs cumulative bằng hình, không bằng định nghĩa.

---

### Người 4 — “Cứu model & giám sát nó”

**Mục tiêu phần:** khán giả biết các hướng ứng phó, hiểu monitoring/observability là gì, và nhớ 4 artifact + 3 công cụ chính.

**Nội dung bắt buộc:**

#### Ứng phó shift

- 3 hướng:
  1. Train trên **dữ liệu khổng lồ** — thống trị nghiên cứu.
  2. **Domain adaptation** không cần nhãn — Zhang 2013, Zhao 2020; chưa phổ biến trong industry.
  3. **Retrain trên nhãn của target distribution** — phổ biến nhất.
- Retrain:
  - **Stateless**: train lại từ đầu trên dữ liệu cũ + mới.
  - **Stateful / fine-tuning**: train tiếp từ checkpoint.
  - Chọn dữ liệu: 24 giờ, 1 tuần, 6 tháng, hay từ lúc bắt đầu drift?
  - Không có công thức chung; phải **chạy thực nghiệm**. Nhiều công ty vẫn chọn tần suất bằng cảm tính; công ty nhỏ nên dùng **lịch cố định** vì ít dữ liệu.
- Thiết kế robust:
  - **Feature ổn định**: app store ranking dự báo tốt nhưng đổi nhanh → bucket thành top 10, 11–100, 101–1.000…
  - **Model riêng theo thị trường**: SF thay đổi nhanh hơn rural Arizona → tách model để cập nhật đúng nơi cần.
  - **Kiểm tra lỗi con người trước**: nhiều suy giảm không cần giải pháp ML.

#### Monitoring & observability

- **Monitoring**: theo dõi/đo/log metric để biết **khi nào** có vấn đề.
- **Observability**: thiết lập hệ thống để suy ra **trạng thái bên trong** từ output, trả lời **cái gì/ở đâu/tại sao**. Là một phần của monitoring; không có observability thì monitoring không đầy đủ.
- **Operational metrics**:
  - Network / machine / application.
  - Latency, throughput, số request, % 2xx, CPU/GPU, memory.
- **Availability / uptime / SLO / SLA**:
  - SLA ví dụ: median latency < 200 ms, p99 < 2 s.
  - 99,99% ≈ **hơn 4 phút/tháng**; 99,999% ≈ **26 giây/tháng**.
  - AWS EC2 (10/2021) cam kết 99,99%/tháng, dưới mức thì service credit.
  - Nhưng hệ thống “up” mà dự đoán rác thì vẫn là hệ thống hỏng.
- **4 artifact**:
  1. **Accuracy-related metrics** — cần nhãn; dùng feedback: click, completion rate, upvote/downvote.
  2. **Predictions** — ít chiều, dễ monitor, là proxy cho input shift; phát hiện “toàn False”.
  3. **Features** — schema validation, table testing/unit tests for data; Great Expectations, Deequ; two-sample test sau khi giảm chiều.
  4. **Raw inputs** — nhiều nguồn/format; thường do data platform team quản lý.
- **4 vấn đề của feature monitoring**:
  - Hàng trăm model × hàng trăm feature → tốn compute/memory/latency.
  - Feature shift thường lành tính → **alert fatigue**; khó biết shift nào critical.
  - Provenance phức tạp: nhiều bước, nhiều thư viện, nhiều service.
  - Schema thay đổi → cần version schema.
- **Toolbox**:
  - **Logs**: event; Badoo **20 tỷ event/ngày** (2019); distributed tracing bằng unique ID + metadata; batch (Spark/Hadoop/Hive) vs stream (Kafka/Kinesis, KSQL/Flink SQL); ML cho anomaly detection/phân loại event.
  - **Dashboards**: trực quan hoá, giúp non-engineer; nhưng graph không đủ; **dashboard rot** khi quá nhiều metric.
  - **Alerts**: 3 thành phần — policy, notification channels, description + runbook; **alert fatigue**.
  - **Observability**: telemetry (tele = remote, metron = measure); tag để slice theo user/input/thời gian; câu query “group by zip code”; **interpretability** nằm trong observability.
- Tổng kết:
  - **Monitor để biết, observability để hiểu, retrain để thích nghi.**
  - Deploy là bắt đầu; phải giả định model sẽ hỏng.

**Ví dụ/visual nên dùng:**

- Bảng 3 hướng ứng phó + “stateless vs stateful”.
- Dashboard giả lập: accuracy, latency, CPU, prediction distribution.
- Alert mẫu:

```text
## Recommender model accuracy below 90%
${timestamp}: This alert originated from ${service-name}
```

- Pipeline 4 artifact (raw → features → predictions → accuracy).
- Dùng lại **sơ đồ tư duy** ở slide cuối.

**Câu chốt:**

> “Monitor để biết, observability để hiểu, retrain để thích nghi. Và đừng quên: phần lớn sự cố vẫn bắt đầu từ những lỗi rất ‘người’.”

**Vai trò Q&A:**

- Điều phối: “Câu hỏi này thuộc phần của bạn nào?” → chuyển đúng người.
- Giữ thời gian: tối đa **5 phút**, ưu tiên câu hỏi về ứng dụng/thực tế.
- Nếu câu hỏi khó, ghi lại và hẹn trả lời sau — không improvise số liệu.

**Checklist:**

- [ ] Nêu đúng 3 hướng ứng phó, không sa vào chi tiết domain adaptation.
- [ ] Phân biệt stateless/stateful bằng 1 câu.
- [ ] Có ví dụ feature ổn định (app ranking).
- [ ] Nêu 4 artifact theo đúng thứ tự pipeline.
- [ ] Có 1 alert mẫu + nhắc alert fatigue.
- [ ] Kết bằng 3 điều mang đi, không đọc lại toàn bộ slide.

---

## 5. Việc chung & timeline

### 5.1 Quy ước slide

- Một file slide chung, **16:9**, template thống nhất:
  - Font tiêu đề ≥ 32 pt, nội dung ≥ 22–24 pt.
  - Footer: `Designing Machine Learning Systems — Chương 8`.
  - Màu nhấn: đỏ cho failure, xanh cho shift, xanh lá cho giải pháp.
- Mỗi slide **một ý**, tối đa **6 dòng**, ưu tiên hình/bảng hơn chữ.
- Mỗi người **tự soạn slide của mình**, nhưng gửi trước để Người 4 ráp và kiểm tra mạch.
- **Backup slide** (không trình bày, để Q&A):
  - Công thức phân rã + importance weighting.
  - Bảng đầy đủ 5 loại shift.
  - Chi tiết KS/MMD/LSDD.
  - 4 vấn đề feature monitoring.
  - Bảng số liệu 60/96, 80%, 20 tỷ event, 99,99%.

### 5.2 Timeline 3 buổi

| Buổi | Mục tiêu | Việc cần làm | Ai |
|---|---|---|---|
| **Buổi 1 — 60–90 phút** | Chốt đề cương | Thống nhất 22 slide; mỗi người nói thử 2 phút; chọn ví dụ chính; tạo file slide | Cả nhóm |
| **Buổi 2 — 60 phút** | Ráp nội dung | Ghép slide; kiểm tra handoff; thống nhất thuật ngữ; kiểm tra số liệu | Cả nhóm; Người 3 fact-check |
| **Buổi 3 — 45–60 phút** | Tổng duyệt | Chạy 2 lần, bấm giờ; cắt 10–15% chữ; tập Q&A; kiểm tra file PDF dự phòng | Cả nhóm; Người 1 giữ giờ |

> [!tip] Mốc bắt buộc
> - **Trước buổi 2:** mỗi người gửi outline 5 bullet + ảnh/bảng dự kiến.
> - **Trước buổi 3:** slide đã ghép xong, không sửa cấu trúc.
> - **Trước giờ 30 phút:** mở thử file trên máy trình chiếu; chuẩn bị PDF backup + clicker.

### 5.3 Phân công việc chung

| Việc | Người phụ trách |
|---|---|
| Tạo file slide, agenda, điều phối buổi tập | Người 1 |
| Thiết kế hình feedback loop, poll, ảnh minh hoạ | Người 2 |
| Fact-check công thức, số liệu, thuật ngữ; giữ backup slide | Người 3 |
| Ráp slide, thống nhất template, nộp bài, điều phối Q&A | Người 4 |

---

## 6. Ngân hàng câu hỏi Q&A

| Câu hỏi | Người trả lời | Ý trả lời ngắn |
|---|---|---|
| Không có nhãn thì làm sao biết model tệ? | Người 4 | Monitor predictions/features làm proxy; user feedback; observability; nhãn có thể trễ nhưng vẫn cần thu thập. |
| Làm sao phân biệt drift thật với bug pipeline? | Người 3 / 4 | Kiểm tra schema, version model, feature consistency trước; ~80% drift có thể do lỗi người. |
| Covariate shift và label shift có thể xảy ra cùng lúc không? | Người 3 | Có. Khi $P(X)$ đổi, $P(Y)$ thường cũng đổi; ví dụ ung thư vú. |
| Randomization có làm giảm trải nghiệm người dùng không? | Người 2 | Có. Giảm thiểu bằng contextual bandits, randomization nhỏ + causal inference, positional features. |
| Bao lâu nên retrain một lần? | Người 4 | Không có con số chung; thực nghiệm với cửa sổ dữ liệu; stateless/stateful; công ty nhỏ dùng lịch cố định. |
| Edge case khác outlier thế nào? | Người 2 | Outlier nói về dữ liệu; edge case nói về hiệu năng. Outlier có thể là edge case, nhưng không phải tất cả. |
| Vì sao KS test chỉ dùng 1 chiều? | Người 3 | KS dựa trên ECDF; feature nhiều chiều cần MMD/LSDD hoặc giảm chiều trước. |
| Monitoring khác observability thế nào? | Người 4 | Monitoring trả lời “khi nào”; observability trả lời “cái gì/ở đâu/tại sao”. Observability là phần sâu hơn của monitoring. |

> [!note] Mẹo trả lời
> Trả lời **1 câu trực tiếp** → 1 ví dụ → 1 câu kết. Nếu không chắc, nói rõ “phần này nằm ngoài chương, nhưng trong sách…” thay vì đoán số liệu.

---

## 7. Phương án thời lượng

### Nếu chỉ có 20 phút

- Người 1: **4 phút** — bỏ chi tiết 4 loại software failure, chỉ nêu tên.
- Người 2: **5 phút** — bỏ ví dụ CV, giữ bài hát + TikTok.
- Người 3: **6 phút** — bỏ importance weighting, gộp 3 loại shift vào 1 bảng, chỉ nêu KS/MMD.
- Người 4: **5 phút** — bỏ chi tiết logs/dashboards, giữ 4 artifact + alert.
- Tổng: 20 phút, không có Q&A hoặc Q&A 2 phút.

### Nếu có 40 phút

- Giữ 30 phút như kịch bản.
- Thêm **5 phút demo/poll**:
  - Poll xe tự lái.
  - Mô phỏng feedback loop bằng 2 bài hát.
  - Hoặc walkthrough một dashboard giả lập.
- Thêm **5 phút Q&A** hoặc bài tập tình huống: “Nếu là kỹ sư, bạn kiểm tra gì đầu tiên khi accuracy giảm?”

---

## 8. Checklist tổng duyệt

- [ ] Mỗi người nói đúng thời lượng **±30 giây**.
- [ ] 4 câu chuyển ý được tập thuộc, không “à, tiếp theo là bạn…”.
- [ ] Không slide nào quá **6 dòng** hoặc font < 22 pt.
- [ ] Số liệu thống nhất: **60/96**, **~80%**, **99,99% ≈ 4 phút**, **99,999% ≈ 26 giây**, **20 tỷ event/ngày**.
- [ ] Thuật ngữ thống nhất: “data distribution shift”, “covariate shift”, “label shift”, “concept drift”, “monitoring”, “observability”.
- [ ] Có **PDF backup** và slide gốc trên cloud.
- [ ] Tập trả lời 8 câu Q&A trong mục 6.
- [ ] Kết bài bằng **3 điều mang đi**, không kết bằng “hết”.

---

## 9. Tiêu chí chấm (tham khảo)

| Tiêu chí | Trọng số | Mô tả |
|---|---|---|
| **Nội dung** | 40% | Đúng, đủ ý chính; phân biệt được các loại shift; có ví dụ. |
| **Trình bày** | 20% | Rõ ràng, tự tin, không đọc slide, đúng giờ. |
| **Slide** | 20% | Một ý/slide; trực quan; dễ đọc; nhất quán. |
| **Phối hợp** | 10% | Chuyển ý mượt; không trùng lặp; hỗ trợ nhau khi Q&A. |
| **Q&A** | 10% | Trả lời đúng trọng tâm; biết giới hạn; không đoán bừa. |

> [!success] Chốt kế hoạch
> **Người 1 mở câu chuyện — Người 2 chỉ ra hai cái bẫy — Người 3 vẽ bản đồ shift — Người 4 cứu model và giám sát.**
> Cả nhóm thống nhất một câu xuyên suốt: *“Deploy là bắt đầu; monitor để biết, observability để hiểu, retrain để thích nghi.”*

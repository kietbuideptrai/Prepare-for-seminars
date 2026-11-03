---
title: "Dàn ý slide thuyết trình Chương 8 — 22 slide"
tags:
  - thuyet-trinh
  - slide
  - ml-system
  - data-distribution-shift
nguồn: "[[Kế hoạch thuyết trình Chương 8 - Chia task 4 người]]"
---

# Dàn ý slide thuyết trình Chương 8 — 22 slide

> [!info] Cách dùng
> Mỗi mục dưới đây là **một slide**. Copy **Tiêu đề** và **Bullet** vào PowerPoint/Google Slides; phần **Visual** là gợi ý hình/bảng; phần **Lời dẫn** để tập nói, không cần đọc nguyên văn.
> Khi lên slide thật, cắt bullet còn **5–8 từ khóa** — outline này giữ nội dung đầy đủ để người nói hiểu.

> [!note] Phân bổ
> **Người 1:** slide 1–5 (6 phút) · **Người 2:** slide 6–8 (7 phút) · **Người 3:** slide 9–15 (9 phút) · **Người 4:** slide 16–22 (8 phút).
> Tổng: **30 phút + 5 phút Q&A**.

---

## Phần 1 — Người 1: “Vì sao model chết sau deploy?” (6 phút)

### Slide 1 — Title

**Tiêu đề:** Chương 8 — Data Distribution Shifts & Monitoring

**Phụ đề:** Khi model bắt đầu hỏng sau khi deploy

**Bullet:**
- *Designing Machine Learning Systems* — Chip Huyen
- Nhóm 4 người · [Tên các thành viên]
- Agenda: Vì sao hỏng → Hai cái bẫy → Các loại shift → Ứng phó & giám sát

**Visual:** Sơ đồ tư duy chương 8 hoặc ảnh một app dự báo nhu cầu hàng hoá.

**Lời dẫn:** “Hôm nay nhóm mình kể câu chuyện về một model rất tốt lúc bàn giao, nhưng một năm sau không còn dùng được. Câu hỏi mở đầu: deploy xong đã là xong chưa?”

---

### Slide 2 — Một model tốt có thể chết sau một năm

**Tiêu đề:** Một model tốt có thể chết sau một năm

**Bullet:**
- 6 tháng xây model dự báo nhu cầu hàng tạp hoá
- 1 năm sau: dự báo cao → hàng hết hạn; dự báo thấp → mất doanh thu
- Sửa tay từng dự báo → model tệ dần → không dùng được
- 3 lựa chọn: trả tiền tư vấn cũ / thuê tư vấn mới / tự lập đội in-house

**Visual:** Timeline 3 mốc: “6 tháng xây” → “Deploy, chạy tốt” → “1 năm sau, hỏng”.

**Lời dẫn:** “Điểm mấu chốt không phải model dở lúc đầu. Nó giỏi lúc đầu, rồi hỏng dần vì dữ liệu và thế giới thay đổi.”

---

### Slide 3 — Failure là gì? Khi nào model “hỏng”?

**Tiêu đề:** Failure là gì? Khi nào model “hỏng”?

**Bullet:**
- Failure = một kỳ vọng của hệ thống bị vi phạm
- **Operational:** latency, throughput, không crash
- **ML performance:** accuracy/F1 đạt ngưỡng
- Ví dụ dịch Anh–Pháp: không có bản dịch vs dịch sai liên tục
- ML thường **fail silently** vì thiếu ground truth

**Visual:** Hai cột “Operational expectation” và “ML performance expectation”; icon “im lặng”.

**Lời dẫn:** “Hệ thống không sập chưa chắc là hệ thống đúng. Nếu không có nhãn, model có thể sai hàng loạt mà không ai biết.”

---

### Slide 4 — Không phải lỗi nào cũng là lỗi ML

**Tiêu đề:** Không phải lỗi nào cũng là lỗi ML

**Bullet:**
- **Software failures:** dependency, deployment, hardware, downtime
- Google 2020: **60/96 vụ** pipeline ML hỏng **không trực tiếp do ML**
- **ML-specific:** data, hyperparameter, pipeline lệch, shift, edge cases, feedback loops
- ML-specific ít nhưng **khó phát hiện, khó sửa**
- ML engineering chủ yếu là engineering

**Visual:** Bảng 2 nhóm lỗi; donut **60/96**.

**Lời dẫn:** “Trước khi đổ lỗi cho model, hãy kiểm tra hệ thống phần mềm và pipeline. Phần lớn sự cố thực tế không phải lỗi ML.”

---

### Slide 5 — Train-serving skew: dữ liệu train không đại diện thế giới thật

**Tiêu đề:** Train-serving skew — dữ liệu train không đại diện thế giới thật

**Bullet:**
- Giả định “train/test cùng phân phối stationary” thường sai
- Dữ liệu thật đa dạng; train hữu hạn + **selection/sampling bias**
- Thế giới thay đổi: **đột ngột, dần dần, theo mùa**
- Ví dụ: tìm “Wuhan” trước và sau COVID-19
- **~80% “drift”** trên dashboard có thể là lỗi pipeline/con người

**Visual:** Hai phân phối lệch nhau (train vs production); timeline “Wuhan”.

**Lời dẫn:** “Model không hỏng vì code đổi, mà vì thế giới đổi. Và đôi khi ‘drift’ chỉ là một bug trong pipeline.”

**Chuyển ý sang Người 2:**
> “Ngoài dữ liệu lệch, còn hai cái bẫy rất ‘ML’: những mẫu cực đoan và những vòng lặp do chính model tạo ra.”

---

## Phần 2 — Người 2: “Hai cái bẫy ML-specific” (7 phút)

### Slide 6 — Edge case: 99,99% vẫn có thể là không đủ

**Tiêu đề:** Edge case — 99,99% vẫn có thể là không đủ

**Bullet:**
- Xe tự lái an toàn **99,99%**; 0,01% có thể gây tai nạn chết người — bạn có dùng?
- **Edge case** = mẫu cực đoan khiến model sai thảm khốc
- **Outlier** nói về dữ liệu; **edge case** nói về hiệu năng
- Train có thể bỏ outlier; inference **không thể bỏ** truy vấn lạ
- Safety-critical + brand risk (chatbot nói nội dung phân biệt)

**Visual:** Poll giơ tay “Có/Không”; bảng outlier vs edge case.

**Lời dẫn:** “Nếu một hệ thống đúng 99,99% nhưng 0,01% gây chết người, bạn có dám dùng? Đó là lý do edge case có thể chặn cả một sản phẩm.”

---

### Slide 7 — Degenerate feedback loop: model tự tạo dữ liệu cho chính nó

**Tiêu đề:** Degenerate feedback loop — model tự tạo dữ liệu cho chính nó

**Bullet:**
- **Output → hành vi người dùng → dữ liệu train → output**
- Bài hát A/B: A xếp cao hơn một chút → hiện trước → click nhiều → càng xếp cao
- Hệ quả: **popularity bias, filter bubble, echo chamber**
- CV: feature X (Stanford/Google/nam) → chỉ tuyển X → model càng tin X
- Bias được **khuếch đại** theo thời gian

**Visual:** Sơ đồ vòng lặp; ranking A/B; pipeline CV.

**Lời dẫn:** “Model không chỉ học từ dữ liệu — nó tạo ra dữ liệu cho vòng sau. Nếu không cẩn thận, nó tự khuếch đại bias của mình.”

---

### Slide 8 — Phát hiện & phá vòng lặp

**Tiêu đề:** Phát hiện & phá vòng lặp

**Bullet:**
- Đo **popularity diversity** / độ phủ long-tail
- **Hit rate theo bucket popularity:** giỏi hơn hẳn ở item phổ biến → popularity bias
- **Randomization:** TikTok gán pool traffic ngẫu nhiên cho video mới
- **Positional features:** thêm “vị trí 1” khi train; inference đặt `False`
- Hai model: dự đoán exposure (có vị trí) → dự đoán click (không vị trí)
- Đánh đổi: randomization giảm UX → dùng contextual bandits/causal inference

**Visual:** Bảng 8-1 rút gọn; sơ đồ 2 model; logo TikTok (nếu được phép).

**Lời dẫn:** “Có hai cách: làm loãng thiên lệch bằng randomization, hoặc dạy model biết vị trí hiển thị ảnh hưởng đến click thế nào.”

**Chuyển ý sang Người 3:**
> “Feedback loop là shift do chính hệ thống gây ra. Còn khi thế giới bên ngoài thay đổi, ta gọi đó là gì và đo bằng cách nào?”

---

## Phần 3 — Người 3: “Data distribution shift: bản đồ & cách phát hiện” (9 phút)

### Slide 9 — Data distribution shift là gì?

**Tiêu đề:** Data distribution shift — khi phân phối dữ liệu thay đổi

**Bullet:**
- **Source distribution** (train) vs **target distribution** (inference)
- Công thức: $P(X,Y)=P(Y \vert X)P(X)=P(X \vert Y)P(Y)$
- Shift = dữ liệu thay đổi theo thời gian → dự đoán kém dần
- Không phải mọi thay đổi đều là shift thật
- Cần biết: **loại nào, đo bằng gì, cửa sổ nào**

**Visual:** Hai phân phối chồng lệch; công thức phân rã.

**Lời dẫn:** “Shift không phải một khái niệm duy nhất — nó có nhiều loại, và mỗi loại cần cách đo khác nhau.”

---

### Slide 10 — Covariate shift: input đổi, quy luật giữ nguyên

**Tiêu đề:** Covariate shift — input đổi, quy luật giữ nguyên

**Bullet:**
- $P(X)$ đổi, $P(Y \vert X)$ giữ nguyên
- Ung thư vú: train nhiều phụ nữ >40 hơn inference; xác suất bệnh **theo tuổi** không đổi
- Nguyên nhân: selection bias, oversampling, active learning, marketing
- Xử lý: **importance weighting** — ước lượng tỷ lệ mật độ target/train
- Hạn chế: không biết trước phân phối sẽ đổi thế nào

**Visual:** Hai histogram tuổi; công thức weight.

**Lời dẫn:** “Đầu vào đổi nhưng quy luật ‘tuổi → nguy cơ bệnh’ vẫn vậy. Vì vậy ta có thể hiệu chỉnh bằng trọng số.”

---

### Slide 11 — Label shift: tỷ lệ nhãn đổi, input trong từng lớp giữ nguyên

**Tiêu đề:** Label shift — tỷ lệ nhãn đổi, input trong từng lớp giữ nguyên

**Bullet:**
- $P(Y)$ đổi, $P(X \vert Y)$ giữ nguyên
- Train có nhiều positive hơn; nhưng người đã bệnh vẫn cùng phân phối tuổi
- Ví dụ thuốc phòng ngừa: $P(Y \vert X)$ giảm → không covariate, nhưng vẫn label shift
- Có thể xảy ra **đồng thời** với covariate shift
- Phương pháp thích nghi tương tự covariate shift

**Visual:** Hai biểu đồ prior trước/sau; mũi tên “prior shift”.

**Lời dẫn:** “Ở label shift, tỷ lệ các lớp đổi, nhưng bên trong mỗi lớp thì dữ liệu vẫn như cũ.”

---

### Slide 12 — Concept drift: cùng input, output khác

**Tiêu đề:** Concept drift — cùng input, output khác

**Bullet:**
- $P(Y \vert X)$ đổi, $P(X)$ giữ nguyên
- Giá nhà SF: **2 triệu → 1,5 triệu USD** trong COVID
- Có thể cyclic/seasonal: ride-hailing ngày thường/cuối tuần; vé máy bay lễ
- Có thể dùng **model riêng theo mùa**
- “Same input, different output”

**Visual:** Scatter giá nhà trước/sau; lịch mùa.

**Lời dẫn:** “Căn nhà không đổi, nhưng thị trường định giá nó khác đi. Cùng input, output đã khác.”

---

### Slide 13 — Feature change & label schema change

**Tiêu đề:** Feature change & label schema change

**Bullet:**
- **Feature change:** `age` đổi từ năm sang tháng; bug khiến feature toàn NaN
- **Label schema:** credit score 300–850 → 250–900
- Sentiment 3 lớp → 4 lớp (tách SAD/ANGRY)
- Softmax layer đổi kích thước `[hidden_units × số lớp]` → có thể relabel + retrain from scratch
- Phổ biến ở **high-cardinality tasks**

**Visual:** Bảng tóm tắt 5 loại shift (3 loại chính + 2 dạng mở rộng).

**Lời dẫn:** “Không chỉ phân phối đổi — đôi khi chính cấu trúc dữ liệu và nhãn cũng đổi, và model phải đổi theo.”

---

### Slide 14 — Phát hiện shift: accuracy không đủ

**Tiêu đề:** Phát hiện shift — accuracy không đủ

**Bullet:**
- Accuracy cần nhãn; nhãn production thường **trễ**
- Monitor $P(X)$, $P(Y)$, $P(X \vert Y)$, $P(Y \vert X)$; $P(X)$ không cần nhãn
- Summary stats: min/max/mean/median/var/quantile/skew/kurtosis
- TFX (10/2021) vẫn chỉ dùng **summary statistics**
- Hạn chế: giống nhau **không đảm bảo** không shift

**Visual:** Bảng “phân phối nào cần nhãn”; dashboard summary stats.

**Lời dẫn:** “Accuracy là metric đúng nhất nhưng thường đến muộn — nên phải nhìn vào phân phối để phát hiện sớm.”

---

### Slide 15 — Two-sample test & time-scale windows

**Tiêu đề:** Two-sample test & time-scale windows

**Bullet:**
- **Two-sample test:** hai tập có cùng phân phối?
- **KS:** nonparametric, 1D, tốt cho label/prediction; nhiều false positive
- **MMD/LSDD/Alibi Detect:** đa biến; **giảm chiều** trước khi test
- Time window: chu kỳ tuần; ngày 9–14 vs ngày 1–14 cho kết luận khác nhau
- **Sliding vs cumulative:** cumulative có thể che cú sụt giờ 16–18
- Cửa sổ ngắn phát hiện nhanh nhưng dễ false alarm

**Visual:** KS ECDF; Figure 8-3; sliding vs cumulative (Figure 8-4).

**Lời dẫn:** “Cùng một chuỗi dữ liệu, chọn cửa sổ khác nhau có thể ra kết luận trái ngược. Vì vậy phải chọn cửa sổ theo chu kỳ của dữ liệu.”

**Chuyển ý sang Người 4:**
> “Phát hiện được shift rồi thì làm gì? Câu trả lời không phải ‘train lại là xong’ — mà là chọn đúng cách ứng phó và giám sát đủ sâu.”

---

## Phần 4 — Người 4: “Cứu model & giám sát nó” (8 phút)

### Slide 16 — Ứng phó: ba hướng, một lựa chọn phổ biến

**Tiêu đề:** Ứng phó — ba hướng, một lựa chọn phổ biến

**Bullet:**
- Train **dữ liệu khổng lồ** (research)
- **Domain adaptation** không cần nhãn (Zhang 2013, Zhao 2020; chưa phổ biến)
- **Retrain trên target labels** (industry)
- **Stateless:** train lại từ đầu; **Stateful:** fine-tune từ checkpoint
- Chọn cửa sổ dữ liệu: 24h / 1 tuần / 6 tháng / từ lúc drift → **phải thực nghiệm**

**Visual:** Bảng 3 hướng; flowchart “phát hiện → chọn hướng → retrain”.

**Lời dẫn:** “Không có một cách đúng cho mọi công ty — nhưng industry chủ yếu chọn retrain có nhãn, và câu hỏi khó là retrain bằng dữ liệu nào.”

---

### Slide 17 — Thiết kế để ít phải retrain

**Tiêu đề:** Thiết kế để ít phải retrain

**Bullet:**
- **Feature ổn định:** app ranking → bucket top 10 / 11–100 / 101–1.000...
- Trade-off: feature dự báo tốt nhưng đổi nhanh → retrain liên tục
- **Model riêng theo thị trường:** SF thay đổi nhanh hơn rural Arizona
- Kiểm tra **lỗi con người** trước khi kết luận shift
- “Không phải mọi suy giảm cần giải pháp ML”

**Visual:** Trục “performance vs stability”; hai box model SF/Arizona.

**Lời dẫn:** “Cách tốt nhất để ít retrain là thiết kế feature và model phù hợp ngay từ đầu — và kiểm tra lỗi người trước.”

---

### Slide 18 — Monitoring vs Observability

**Tiêu đề:** Monitoring vs Observability

**Bullet:**
- **Monitoring:** theo dõi/đo/log để biết **khi nào** có vấn đề
- **Observability:** suy ra trạng thái bên trong để biết **cái gì/ở đâu/tại sao**
- Operational metrics: network / machine / application
- Latency, throughput, 2xx, CPU/GPU, memory
- SLO/SLA: **99,99% ≈ 4 phút/tháng**; **99,999% ≈ 26 giây**
- AWS EC2 99,99% (10/2021)

**Visual:** Hai cột; đồng hồ uptime.

**Lời dẫn:** “Hệ thống ‘up’ chưa đủ — nếu dự đoán rác thì vẫn là hệ thống hỏng. Vì vậy cần cả operational metrics và ML metrics.”

---

### Slide 19 — Bốn artifact cần monitor

**Tiêu đề:** Bốn artifact cần monitor

**Bullet:**
- **Accuracy metrics:** feedback; YouTube CTR + completion; Google Translate vote
- **Predictions:** ít chiều, proxy cho input shift, phát hiện “toàn False”
- **Features:** schema validation; Great Expectations/Deequ; 4 vấn đề (cost, alert fatigue, provenance, schema versioning)
- **Raw inputs:** nhiều nguồn/format; thường do data platform team
- Càng sâu pipeline càng dễ monitor nhưng càng dễ do lỗi biến đổi

**Visual:** Pipeline 4 tầng: raw → features → predictions → accuracy.

**Lời dẫn:** “Bốn tầng artifact: càng gần ground truth càng đúng, nhưng càng khó và càng trễ.”

---

### Slide 20 — Bộ công cụ: logs, dashboards, alerts

**Tiêu đề:** Bộ công cụ — logs, dashboards, alerts

**Bullet:**
- **Logs:** Badoo **20 tỷ event/ngày**; distributed tracing bằng unique ID; batch vs stream
- **Dashboards:** trực quan, cho non-engineer; nhưng graph không đủ; **dashboard rot**
- **Alerts:** policy + notification channel + description/runbook
- **Alert fatigue:** quá nhiều alert → mất nhạy cảm với alert quan trọng
- ML cho log: anomaly detection, phân loại event, ước lượng service ảnh hưởng

**Visual:** Log stream; dashboard mock; alert template.

**Lời dẫn:** “Giám sát không chỉ là vẽ graph — mà là biết ai sẽ bị gọi lúc 2 giờ sáng, và alert đó có thật sự quan trọng không.”

---

### Slide 21 — Observability: nhìn vào bên trong hệ thống

**Tiêu đề:** Observability — nhìn vào bên trong hệ thống

**Bullet:**
- **Telemetry:** tele (xa) + metron (đo) = đo từ xa
- Tag output để **slice** theo user/input/thời gian
- Query: “user nào model A dự đoán sai 1 giờ qua, group by zip code?”
- **Interpretability** nằm trong observability
- Monitoring bị động; **continual learning** chủ động (Chương 9)

**Visual:** Sơ đồ tag/slice; câu query mẫu.

**Lời dẫn:** “Observability trả lời câu hỏi mà monitoring không trả lời được: ‘tại sao?’.”

---

### Slide 22 — Tổng kết: 3 điều mang đi

**Tiêu đề:** Tổng kết — 3 điều mang đi

**Bullet:**
- **Deploy là bắt đầu**; model sẽ hỏng
- Ba cái bẫy: train-serving skew, edge cases, degenerate feedback loops
- Ba loại shift: covariate, label, concept (+ schema)
- **Monitor để biết, observability để hiểu, retrain để thích nghi**
- Q&A

**Visual:** Sơ đồ tư duy chương 8; 3 icon: mắt (monitor), kính lúp (observability), vòng lặp (retrain).

**Lời dẫn:** “Nếu chỉ nhớ một câu: deploy là bắt đầu, và phải giám sát để biết khi nào cần cập nhật.”

---

## Checklist chuyển outline sang PPT

- [ ] Mỗi slide **≤ 6 dòng**, font nội dung **≥ 24 pt**.
- [ ] Mỗi slide chỉ **một thông điệp chính**; bullet dài cắt còn 5–8 từ.
- [ ] Slide 1 có **tên đủ 4 thành viên**, agenda và thời lượng.
- [ ] Slide 5, 8, 15, 17 có **câu chuyển ý** đúng như outline.
- [ ] Slide 22 dùng lại **sơ đồ tư duy** để kết.
- [ ] Footer thống nhất: `Designing Machine Learning Systems — Chương 8`.
- [ ] Đánh số slide ở góc phải.
- [ ] Chuẩn bị **backup slide**: công thức, bảng 5 loại shift, chi tiết KS/MMD, 4 vấn đề feature monitoring.
- [ ] Xuất **PDF dự phòng** trước khi thuyết trình.

> [!success] Mẹo lên slide
> Nếu một bullet không thể đọc trong **3 giây**, nó quá dài. Hãy giữ từ khoá trên slide và nói phần giải thích — đừng biến slide thành tài liệu đọc.

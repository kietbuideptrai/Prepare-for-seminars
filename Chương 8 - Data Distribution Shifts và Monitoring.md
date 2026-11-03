---
title: "Chương 8 — Data Distribution Shifts & Monitoring"
tags:
  - ml-system
  - mlops
  - data-distribution-shift
  - monitoring
  - observability
  - designing-ml-systems
nguồn: "[[chapter8.pdf]]"
sách: "Designing Machine Learning Systems — Chip Huyen (O'Reilly)"
chương: 8
trang: "225–262"
---

# Chương 8 — Data Distribution Shifts & Monitoring

> [!info] Nguồn tài liệu
> Trích từ **[[chapter8.pdf]]** — Chương 8 của *Designing Machine Learning Systems* (Chip Huyen, O'Reilly), tr. 225–262.
> Đây là bản **ghi chú diễn giải và hệ thống hoá** kiến thức trong chương, không phải bản dịch nguyên văn.

> [!abstract] Tóm tắt một câu
> **Deploy không phải là đích.** Model sẽ giảm hiệu năng trong production vì dữ liệu production khác dữ liệu train và thế giới liên tục thay đổi. Phải **monitor** để phát hiện, **chẩn đoán** đúng nguyên nhân, rồi **retrain hoặc thiết kế lại hệ thống** để thích nghi.

> [!tip] Thuyết trình
> Kế hoạch chia task 4 người, kịch bản 22 slide và ngân hàng câu hỏi Q&A: [[Kế hoạch thuyết trình Chương 8 - Chia task 4 người]].

![[Ch8 - Data Distribution Shifts.excalidraw]]

*Sơ đồ tư duy: từ nguyên nhân hỏng → các loại shift → phát hiện → ứng phó → giám sát.*

---

## 0. Câu chuyện mở đầu: model tốt lúc bàn giao, hỏng sau một năm

Một công ty thuê tư vấn xây model dự báo nhu cầu hàng tạp hoá theo tuần để nhập hàng. Sau 6 tháng, model được bàn giao và chạy tốt. Một năm sau, con số bắt đầu lệch:

- Một số mặt hàng **bị dự báo cao** → nhập thừa → hàng hết hạn.
- Một số mặt hàng **bị dự báo thấp** → hết hàng → mất doanh thu.

Đội vận hành ban đầu sửa tay từng dự báo, nhưng cuối cùng model tệ đến mức không dùng được nữa. Công ty đứng trước ba lựa chọn: trả tiền cho công ty tư vấn cũ cập nhật model, thuê công ty mới (đắt hơn vì mất thời gian làm quen), hoặc tự lập đội in-house để bảo trì model.

> [!important] Bài học
> **Hiệu năng model suy giảm theo thời gian trong production.** Sau khi deploy vẫn phải **monitor liên tục** để phát hiện vấn đề và **cập nhật** để sửa. Đây là lý do tồn tại của MLOps.

---

## 1. ML system failure là gì?

**Failure** xảy ra khi một hoặc nhiều **kỳ vọng (expectation)** của hệ thống bị vi phạm.

| Loại kỳ vọng | Nội dung | Ví dụ hệ dịch Anh → Pháp |
|---|---|---|
| **Operational expectation** | Hệ thống chạy đúng các chỉ số vận hành: latency, throughput, không crash… | Trả bản dịch trong **< 1 giây** |
| **ML performance expectation** | Chất lượng dự đoán đạt ngưỡng mong muốn | Bản dịch **đúng 99%** |

- Nhập một câu tiếng Anh mà **không nhận được bản dịch** → vi phạm kỳ vọng vận hành → **system failure**.
- Nhận bản dịch sai **một lần** → chưa chắc là failure, vì ngưỡng cho phép sai số.
- Nhưng **liên tục** nhận bản dịch sai → vi phạm kỳ vọng chất lượng → **system failure**.

### Vì sao ML system thường "fail silently"?

- **Operational failure dễ phát hiện**: timeout, lỗi 404, out-of-memory, segmentation fault… thường có tín hiệu rõ ràng.
- **ML performance failure khó phát hiện**: muốn biết bản dịch có đúng 99% hay không thì phải biết **ground truth**. Nếu không có nhãn, hệ thống có thể trả kết quả sai hàng loạt mà không ai biết.

> [!warning] Đặc trưng nguy hiểm
> ML system thường **fail silently**. Người dùng có thể dùng một bản dịch sai mà không hề biết nó sai.

### Hai nhóm nguyên nhân gốc

```
ML system failures
├── Software system failures  (không đặc thù ML)
└── ML-specific failures      (đặc thù ML)
```

---

## 2. Software system failures

Là những lỗi **cũng sẽ xảy ra với hệ thống không-ML**.

| Loại | Mô tả |
|---|---|
| **Dependency failure** | Package/codebase phụ thuộc bị hỏng → hệ thống hỏng. Nguy hiểm khi dependency do bên thứ ba bảo trì, nhất là khi bên đó không còn tồn tại. |
| **Deployment failure** | Lỗi khi deploy: deploy nhầm binary của model cũ, thiếu quyền đọc/ghi file… |
| **Hardware failure** | CPU/GPU nóng quá, hỏng, hoặc lỗi phần cứng (kể cả cosmic ray). |
| **Downtime / crashing** | Server (AWS, hosted service…) hoặc một component bị down → hệ thống down theo. |

### Con số đáng chú ý (Google, 2020)

Daniel Papasian và Todd Underwood phân tích **96 vụ** một pipeline ML lớn tại Google bị hỏng trong hơn 15 năm:

- **60/96 vụ** có nguyên nhân **không trực tiếp liên quan đến ML**.
- Phần lớn liên quan đến **distributed systems** (scheduler/orchestrator sai) hoặc **data pipeline** (join dữ liệu sai, dùng sai cấu trúc dữ liệu).

> [!note] Hệ quả nghề nghiệp
> Xử lý software system failure cần **kỹ năng software engineering truyền thống**, không phải kỹ năng ML. Vì vậy có thể nói: **ML engineering chủ yếu là engineering, không phải ML.**

Khi tooling và best practice cho ML production trưởng thành hơn, tỷ lệ software failure được dự đoán sẽ giảm và tỷ lệ **ML-specific failure** sẽ tăng lên.

---

## 3. ML-specific failures

Là lỗi đặc thù của hệ ML:

- Vấn đề **thu thập và xử lý dữ liệu**.
- **Hyperparameter** kém.
- **Training pipeline thay đổi nhưng inference pipeline không được cập nhật** (hoặc ngược lại).
- **Data distribution shift** khiến hiệu năng giảm dần.
- **Edge cases**.
- **Degenerate feedback loops**.

> [!important] Vì sao đáng lo dù chỉ chiếm phần nhỏ?
> ML-specific failures **khó phát hiện, khó sửa**, và có thể khiến toàn bộ hệ ML **không thể dùng được**. Ba vấn đề mới được chương này tập trung:
> 1. Dữ liệu production khác dữ liệu train.
> 2. Edge cases.
> 3. Degenerate feedback loops.

---

## 4. Nguyên nhân 1 — Dữ liệu production khác dữ liệu train

### 4.1 Giả định "stationary distribution" và vì sao nó sai

ML học **phân phối của dữ liệu train** để dự đoán trên **dữ liệu chưa thấy**. Ta nói model **generalize** tốt nếu dự đoán đúng trên dữ liệu chưa thấy. Test set được thiết kế để đại diện cho dữ liệu chưa thấy đó.

Giả định quen thuộc trong các khóa ML:

> Dữ liệu train và dữ liệu chưa thấy đến từ **cùng một phân phối**, và phân phối đó là **stationary** (không đổi theo thời gian).

Giả định này **sai trong phần lớn trường hợp**, vì hai lý do:

1. **Dữ liệu thực tế không giống hệt dữ liệu train.**
   - Thế giới thực đa dạng và gần như vô hạn; tập train hữu hạn, bị giới hạn bởi thời gian, compute và nguồn lực con người.
   - Có nhiều **selection bias / sampling bias** (đã bàn ở Chương 4).
   - Khác biệt có thể rất nhỏ, ví dụ cách **encode emoji** khác nhau.
   - → Sinh ra **train-serving skew**: model làm rất tốt khi phát triển nhưng kém khi deploy.

2. **Thế giới thực không đứng yên.**
   - Phân phối dữ liệu **dịch chuyển theo thời gian**.
   - Ví dụ: năm 2019, tìm "Wuhan" có thể là tìm thông tin du lịch; sau COVID-19, tìm "Wuhan" có thể là tìm nơi khởi phát dịch.
   - → Model tốt lúc mới deploy nhưng **giảm dần** khi phân phối thay đổi. Phải monitor **suốt vòng đời** model.

### 4.2 Data shift xảy ra thường xuyên, không chỉ khi có "sự kiện lớn"

| Kiểu | Ví dụ |
|---|---|
| **Đột ngột (sudden)** | Đối thủ đổi chính sách giá → phải cập nhật dự báo giá; ra mắt sản phẩm ở vùng mới; người nổi tiếng nhắc đến sản phẩm → lượng user mới tăng vọt. |
| **Dần dần (gradual)** | Chuẩn mực xã hội, văn hoá, ngôn ngữ, xu hướng, ngành nghề thay đổi theo thời gian. |
| **Theo mùa (seasonal)** | Nhu cầu gọi xe cao hơn vào mùa đông lạnh/có tuyết; giá vé máy bay tăng vào dịp lễ. |

### 4.3 Cảnh báo: nhiều "shift" trên dashboard thực ra là lỗi nội bộ

Theo ước lượng của CTO một công ty monitoring, **khoảng 80% drift** mà dịch vụ của họ bắt được là do **lỗi con người**, không phải thay đổi phân phối thật sự. Ví dụ:

- Bug trong **data pipeline**.
- **Missing values** được đưa vào sai cách.
- **Feature lúc train và lúc inference không nhất quán**.
- Chuẩn hoá feature bằng thống kê từ **sai tập dữ liệu**.
- Dùng **sai phiên bản model**.
- Bug ở **app interface** khiến người dùng đổi hành vi.

> [!tip] Thực hành
> Trước khi kết luận "data drift", hãy kiểm tra **pipeline, schema, phiên bản model, feature consistency**. Đây thường là nguyên nhân rẻ và nhanh sửa hơn nhiều.

---

## 5. Nguyên nhân 2 — Edge cases

**Edge case** là những mẫu dữ liệu **cực đoan đến mức khiến model mắc lỗi thảm khốc**.

Ví dụ mở đầu: một chiếc xe tự lái an toàn **99,99%** thời gian, nhưng **0,01%** còn lại có thể gây tai nạn chết người. Bạn có dùng không? Phần lớn người được hỏi trả lời **không**. Vì vậy các công ty xe tự lái tập trung rất nhiều vào edge cases.

### Edge case vs Outlier

| | **Outlier** | **Edge case** |
|---|---|---|
| Nói về | **Dữ liệu** | **Hiệu năng của model** |
| Định nghĩa | Mẫu khác biệt đáng kể so với các mẫu còn lại | Mẫu mà model làm **tệ hơn đáng kể** so với các mẫu khác |
| Quan hệ | Outlier **có thể** gây ra edge case | Không phải outlier nào cũng là edge case |

Ví dụ: một người đi bộ sang đường trái phép trên cao tốc là **outlier**, nhưng **không phải edge case** nếu xe tự lái vẫn phát hiện đúng và xử lý an toàn.

### Vì sao edge case nguy hiểm?

- Trong **huấn luyện**, có thể loại bỏ outlier để model học boundary tốt hơn và generalize tốt hơn.
- Trong **inference**, thường **không thể loại bỏ** truy vấn lạ. Có thể chuẩn hoá/transform (ví dụ Google Search gợi ý "mechin learnin" → "machine learning"), nhưng nhìn chung phải xây model **chịu được input bất thường**.
- Nếu số mẫu model làm kém **tăng đột ngột**, đó có thể là dấu hiệu **phân phối nền đã dịch chuyển**.

### Phạm vi ảnh hưởng

- **Safety-critical**: chẩn đoán y tế, điều khiển giao thông, e-discovery…
- **Không safety-critical nhưng ảnh hưởng thương hiệu**: chatbot chăm sóc khách hàng trả lời hợp lý phần lớn thời gian nhưng thỉnh thoảng đưa ra nội dung phân biệt chủng tộc/giới tính → không công ty nào dám dùng.

---

## 6. Nguyên nhân 3 — Degenerate feedback loops

### 6.1 Định nghĩa

**Feedback loop** (đã bàn ở mục Natural Labels) là vòng: dự đoán được hiển thị → người dùng phản hồi → phản hồi được dùng làm nhãn để đánh giá và huấn luyện vòng sau.

**Degenerate feedback loop** xảy ra khi **chính dự đoán ảnh hưởng đến phản hồi**, và phản hồi đó lại ảnh hưởng đến vòng huấn luyện tiếp theo. Nói cách khác:

> **Output của hệ thống được dùng để tạo input tương lai của chính hệ thống**, rồi input này lại ảnh hưởng đến output tương lai.

Đặc biệt phổ biến ở các bài toán có **natural labels từ người dùng**: recommender systems, dự đoán CTR quảng cáo.

### 6.2 Ví dụ 1 — Gợi ý bài hát

Giả sử hệ thống xếp hạng bài hát để gợi ý. Bài được xếp hạng cao được hiển thị trước → user click nhiều hơn → hệ thống "tin" rằng bài đó hay hơn → xếp hạng càng cao.

Ban đầu A và B chênh nhau rất ít. Chỉ vì A được xếp cao hơn một chút, A được hiển thị trước, được click nhiều hơn, nên hạng của A tăng dần. Sau một thời gian, A **vượt xa** B.

Đây là một lý do khiến phim/sách/bài hát nổi tiếng **ngày càng nổi tiếng**, và item mới khó chen vào bảng xếp hạng. Hiện tượng này có nhiều tên gọi:

- **Exposure bias**
- **Popularity bias**
- **Filter bubble**
- **Echo chamber**

### 6.3 Ví dụ 2 — Sàng lọc CV

Model dự đoán ứng viên có phù hợp không. Nó phát hiện feature $X$ dự đoán tốt → đề xuất CV có $X$. Recruiter chỉ phỏng vấn người được model đề xuất → công ty chỉ tuyển người có $X$ → model càng tin $X$ là quan trọng.

$X$ có thể là "từng học Stanford", "từng làm ở Google", hoặc "là nam". Hậu quả:

- Model **ngày càng thiên lệch** theo $X$.
- Bias trong dữ liệu được **duy trì và khuếch đại**; ứng viên không có $X$ bị loại oan.

> [!tip] Cách phát hiện sớm
> Đo **feature importance** (Chương 5) để xem model có đang dồn trọng số bất thường vào một feature không.

### 6.4 Phát hiện degenerate feedback loop

- Khi hệ thống **offline**, rất khó phát hiện vì chưa có người dùng thật.
- Với recommender system, có thể đo **độ đa dạng popularity** của output ngay cả khi offline:
  - Độ phổ biến của item thường theo **long-tail distribution**: một ít item được tương tác rất nhiều, phần lớn item rất ít được tương tác.
  - Các metric như **aggregate diversity**, **average coverage of long-tail items** (Brynjolfsson et al. 2011; Fleder & Hosanagar 2009; Abdollahpouri et al. 2019) đo độ đa dạng đầu ra.
  - Điểm thấp → output **đồng nhất**, có thể do **popularity bias**.

- **Hit rate against popularity** (Chia et al., 2021):
  1. Chia item thành các **bucket** theo độ phổ biến, ví dụ bucket 1 = được tương tác < 100 lần; bucket 2 = 100–1.000 lần; …
  2. Đo **độ chính xác dự đoán** của recommender trên từng bucket.
  3. Nếu model **giỏi hơn hẳn** ở item phổ biến so với item ít phổ biến → khả năng cao bị **popularity bias**.

- Khi đã lên production: nếu dự đoán **ngày càng đồng nhất** theo thời gian → khả năng cao có degenerate feedback loop.

### 6.5 Sửa degenerate feedback loop

#### Cách 1 — Randomization

Thay vì chỉ hiển thị item được xếp hạng cao, **đưa một phần item ngẫu nhiên** vào và dùng phản hồi để đánh giá chất lượng thật của chúng.

- **TikTok**: mỗi video mới được gán ngẫu nhiên một **pool traffic ban đầu** (có thể lên đến hàng trăm impression). Pool này dùng để đánh giá chất lượng **không thiên lệch** của video, rồi quyết định đẩy sang pool lớn hơn hay đánh dấu không liên quan.

- **Đánh đổi**: randomization làm tăng diversity nhưng **giảm trải nghiệm người dùng** nếu làm quá tay.
  - Dùng **exploration strategy thông minh** như **contextual bandits** (Chương 9) để tăng diversity mà chỉ mất một ít accuracy.
  - **Schnabel et al.**: dùng một lượng nhỏ randomization + **causal inference** để ước lượng giá trị **không thiên lệch** của từng bài hát; thuật toán này sửa được recommender để gợi ý **công bằng với creator**.

#### Cách 2 — Positional features

Phản hồi của người dùng **bị thiên lệch bởi vị trí hiển thị**. Ví dụ mỗi lần gợi ý 5 bài: bài ở vị trí đầu dễ được click hơn nhiều. Không rõ model giỏi chọn bài đầu, hay user click bài nào ở đầu cũng được.

**Cách làm cơ bản:** thêm feature **vị trí** vào dữ liệu train. Feature vị trí có thể là **số** (1, 2, 3…) hoặc **Boolean** (có/không ở vị trí đầu).

| ID | Song | Genre | Year | Artist | User | 1st Position | Click |
|---|---|---|---|---|---|---|---|
| 1 | Shallow | Pop | 2020 | Lady Gaga | listenr32 | False | No |
| 2 | Good Vibe | Funk | 2019 | Funk Overlord | listenr32 | False | No |
| 3 | Beat It | Rock | 1989 | Michael Jackson | fancypants | False | No |
| 4 | In Bloom | Rock | 1991 | Nirvana | fancypants | True | Yes |
| 5 | Shallow | Pop | 2020 | Lady Gaga | listenr32 | True | Yes |

- **Khi train**: thêm feature "có phải vị trí 1 hay không" để model học mức ảnh hưởng của vị trí đến khả năng click.
- **Khi inference**: đặt `1st Position = False` để dự đoán khả năng click **bất kể vị trí**, rồi mới tự chọn thứ tự hiển thị.

**Cách tinh vi hơn — hai model:**

1. Model 1: dự đoán xác suất user **nhìn thấy và cân nhắc** gợi ý, có tính đến **vị trí hiển thị**.
2. Model 2: dự đoán xác suất user **click** nếu đã nhìn thấy/cân nhắc; model này **không dùng vị trí**.

> [!note] Phân biệt thuật ngữ
> **Positional features** (feature vị trí) khác với **positional embeddings** (embedding vị trí trong Transformer, Chương 5).

---

## 7. Data distribution shifts

### 7.1 Định nghĩa

**Data distribution shift** (data shift) là hiện tượng dữ liệu model gặp **thay đổi theo thời gian**, khiến dự đoán **kém chính xác dần**.

- **Source distribution**: phân phối dữ liệu dùng để **train**.
- **Target distribution**: phân phối dữ liệu model **chạy inference**.

> [!note] Lịch sử
> Data shift đã được nghiên cứu từ **1986** (Schlimmer & Granger). Sách *Dataset Shift in Machine Learning* (Quiñonero-Candela et al., MIT Press, 2008) là tài liệu chuyên sâu.

### 7.2 Toán học nền tảng

Gọi $X$ là input, $Y$ là output. Trong supervised learning, dữ liệu train là các mẫu từ **phân phối đồng thời** $P(X,Y)$, và ML thường học $P(Y \vert X)$.

Phân phối đồng thời có thể phân rã theo hai cách:

$$
P(X,Y) = P(Y|X)\,P(X)
$$

$$
P(X,Y) = P(X|Y)\,P(Y)
$$

Trong đó:

- $P(Y \vert X)$: xác suất có điều kiện của output khi biết input (ví dụ xác suất email là spam khi biết nội dung).
- $P(X)$: mật độ xác suất của input.
- $P(Y)$: mật độ xác suất của output.

### 7.3 Ba loại shift chính

| Loại | Điều kiện | Trực giác | Ví dụ |
|---|---|---|---|
| **Covariate shift** | $P(X)$ đổi, $P(Y \vert X)$ giữ nguyên | Input đổi, quy luật input → output không đổi | Tuổi trong dữ liệu ung thư vú; chiến dịch marketing kéo user giàu hơn |
| **Label shift** (prior shift, target shift) | $P(Y)$ đổi, $P(X \vert Y)$ giữ nguyên | Tỷ lệ nhãn đổi, phân phối input trong từng lớp không đổi | Tỷ lệ ung thư dương tính giảm; prior của lớp thay đổi |
| **Concept drift** (posterior shift) | $P(Y \vert X)$ đổi, $P(X)$ giữ nguyên | Cùng input, output khác | Giá nhà San Francisco thời COVID; giá ride-hailing theo mùa |

> [!warning] Không loại trừ nhau
> Một model có thể chịu **nhiều loại shift cùng lúc**. Ngoài ra, khi $P(X)$ đổi thì $P(Y)$ thường cũng đổi, nên **covariate shift và label shift có thể xảy ra đồng thời**.

### 7.4 Covariate shift

**Covariate** là biến độc lập có thể ảnh hưởng đến kết quả nhưng không phải biến ta quan tâm trực tiếp. Ví dụ: nghiên cứu giá nhà theo vị trí — giá nhà là biến quan tâm, diện tích là covariate. Trong supervised ML, **label là biến quan tâm**, **input features là covariate**.

**Định nghĩa:** $P(X)$ thay đổi nhưng $P(Y \vert X)$ giữ nguyên.

**Ví dụ ung thư vú:**

- Nguy cơ ung thư vú cao hơn ở phụ nữ **trên 40 tuổi**, nên dùng biến `age`.
- Dữ liệu train có **nhiều phụ nữ > 40** hơn dữ liệu inference → $P(X)$ khác nhau.
- Nhưng với một người **cụ thể ở độ tuổi > 40**, xác suất ung thư vẫn **không đổi** → $P(Y \vert X)$ giữ nguyên.

**Nguyên nhân covariate shift:**

1. **Selection bias khi thu thập dữ liệu**: ví dụ lấy dữ liệu từ phòng khám nơi phụ nữ > 40 được khuyến khích khám → dữ liệu bị lệch về nhóm tuổi này.
2. **Chỉnh sửa dữ liệu có chủ đích**: oversample lớp hiếm để model dễ học (Chương 4), làm phân phối train khác thực tế.
3. **Quá trình học**: **active learning** chọn mẫu "hữu ích nhất" theo heuristic → phân phối input train bị thay đổi so với thực tế.
4. **Production thay đổi**: marketing chạy campaign kéo về nhóm user **giàu hơn**; feature `income` đổi phân phối, nhưng xác suất convert với cùng mức thu nhập vẫn như cũ.

**Cách xử lý — Importance weighting:**

Nếu **biết trước** phân phối thực tế sẽ khác phân phối train:

1. Ước lượng **density ratio** giữa phân phối input thực tế và phân phối input train:

$$
w(x) = \frac{p_{\text{real-world}}(x)}{p_{\text{train}}(x)}
$$

2. Gán trọng số $w(x)$ cho từng mẫu train rồi huấn luyện trên dữ liệu có trọng số.

> [!caution] Hạn chế
> Trong thực tế **không biết trước** phân phối sẽ thay đổi thế nào, nên rất khó huấn luyện phòng trước cho phân phối chưa biết. Có nghiên cứu học **biểu diễn latent bất biến** qua các phân phối, nhưng chưa thấy ứng dụng rộng trong industry.

### 7.5 Label shift

Còn gọi là **prior shift**, **prior probability shift**, **target shift**.

**Định nghĩa:** $P(Y)$ thay đổi nhưng $P(X \vert Y)$ giữ nguyên.

**Ví dụ 1 — kế thừa từ ung thư vú:**

- Train có nhiều phụ nữ > 40 hơn inference → **tỷ lệ nhãn POSITIVE cao hơn** khi train.
- Nhưng nếu chọn ngẫu nhiên một người **đã mắc ung thư** từ train (A) và một người **đã mắc ung thư** từ test (B), xác suất A/B **trên 40 tuổi** là như nhau.
- Tức $P(X \vert Y)$ giữ nguyên → đây **đồng thời** là label shift.

**Ví dụ 2 — không phải covariate shift:**

- Có một loại **thuốc phòng ngừa** mà mọi phụ nữ dùng, làm giảm xác suất mắc ung thư ở **mọi độ tuổi**.
- $P(Y \vert X)$ giảm → **không còn** là covariate shift.
- Nhưng với một người **đã mắc ung thư**, phân phối tuổi vẫn như cũ → $P(X \vert Y)$ giữ nguyên → **vẫn là label shift**.

> [!important] Điểm tinh tế
> **Không phải mọi covariate shift đều kéo theo label shift**, và ngược lại. Khi input distribution đổi, output distribution cũng thường đổi → hai loại shift có thể cùng xuất hiện.

Phương pháp phát hiện và thích nghi label shift **tương tự covariate shift** (ví dụ importance weighting, Black Box Shift Estimation).

### 7.6 Concept drift

Còn gọi là **posterior shift**.

**Định nghĩa:** $P(X)$ giữ nguyên nhưng $P(Y \vert X)$ thay đổi — **cùng input, khác output**.

**Ví dụ giá nhà San Francisco:**

- Trước COVID-19: căn hộ 3 phòng ngủ ở SF có thể giá **2.000.000 USD**.
- Đầu COVID-19: nhiều người rời SF, cùng căn hộ chỉ còn **1.500.000 USD**.
- Phân phối **feature của căn nhà** (diện tích, số phòng, vị trí…) không đổi, nhưng **giá theo feature** đã đổi.

**Concept drift có tính chu kỳ/mùa vụ:**

- Giá ride-hailing khác nhau **ngày thường vs cuối tuần**.
- Giá vé máy bay tăng **mùa lễ**.
- Công ty có thể dùng **model riêng** cho từng chế độ: một model cho ngày thường, một model cho cuối tuần.

### 7.7 Các dạng shift khác (general data distribution shifts)

Ngoài ba loại được nghiên cứu nhiều, còn có:

#### Feature change

- Thêm feature mới, bỏ feature cũ, hoặc **tập giá trị khả dĩ của feature thay đổi**.
- Ví dụ: feature `age` trước dùng **năm**, nay dùng **tháng** → range giá trị dịch chuyển.
- Ví dụ thực tế: bug trong pipeline khiến một feature **toàn NaN** → hiệu năng sụt mạnh.
- Về mặt phân phối: có thể xem là **cả $P(X)$ và $P(Y \vert X)$ đều đổi**.

#### Label schema change

- **Tập giá trị khả dĩ của $Y$ thay đổi**.
- Với label shift: $P(Y)$ đổi nhưng $P(X \vert Y)$ giữ nguyên.
- Với label schema change: **cả $P(Y)$ và $P(X \vert Y)$ đều đổi**. Schema mô tả **cấu trúc** của dữ liệu/nhãn, ví dụ dictionary `{"POSITIVE": 0, "NEGATIVE": 1}`.

**Ví dụ regression — range nhãn đổi:**

- Hệ thống điểm tín dụng cũ: **300–850**.
- Chuyển sang hệ thống mới: **250–900**.

**Ví dụ classification — số lớp đổi:**

- Bài toán chẩn đoán bệnh, xuất hiện **bệnh mới** cần chẩn đoán.
- Sentiment analysis trên tweet: ban đầu 3 lớp `POSITIVE / NEGATIVE / NEUTRAL`; marketing muốn tách `NEGATIVE` thành `SAD` và `ANGRY` → còn **4 lớp**.
- Khi số lớp đổi, **kiến trúc model có thể phải đổi**. Ví dụ softmax layer cuối của neural network có kích thước `[số hidden units × số lớp]`; số lớp đổi → số tham số đổi.
- Có thể phải **relabel dữ liệu** và **retrain from scratch**.

> [!note] Nơi dễ gặp
> Label schema change đặc biệt phổ biến ở **high-cardinality tasks** — bài toán có rất nhiều lớp, như phân loại sản phẩm hoặc phân loại tài liệu.

---

## 8. Phát hiện data distribution shift

### 8.1 Ý tưởng đầu tiên: monitor accuracy-related metrics

Các metric như **accuracy, F1, recall, AUC-ROC** so sánh dự đoán với **ground truth**. Nếu chúng giảm (hoặc tăng/dao động bất thường), cần điều tra.

**Vấn đề:**

- Production **không phải lúc nào cũng có nhãn**.
- Có nhãn nhưng **bị trễ** (natural labels, Chương 4).
- Nếu có nhãn trong thời gian hợp lý → giúp quan sát hiệu năng rất tốt.

### 8.2 Khi không có nhãn: monitor các phân phối liên quan

Các phân phối đáng quan tâm:

- $P(X)$ — phân phối input.
- $P(Y)$ — phân phối nhãn.
- $P(X \vert Y)$ và $P(Y \vert X)$ — các phân phối có điều kiện.

| Phân phối | Có cần nhãn $Y$? |
|---|---|
| $P(X)$ | **Không** |
| $P(Y)$ | **Có** |
| $P(X \vert Y)$ | **Có** |
| $P(Y \vert X)$ | **Có** |

- Nghiên cứu có nỗ lực phát hiện label shift **không cần nhãn** ở target distribution, ví dụ **Black Box Shift Estimation** (Lipton et al., 2018).
- Trong industry, phần lớn phương pháp tập trung vào **phát hiện thay đổi phân phối input**, đặc biệt là **phân phối của feature**.

### 8.3 Phương pháp thống kê đơn giản: so sánh summary statistics

Nhiều công ty so sánh các thống kê:

- `min`, `max`, `mean`, `median`, `variance`.
- Các **quantile**: 5th, 25th, 75th, 95th…
- **Skewness**, **kurtosis**.

Ví dụ: tính median và variance của một feature lúc inference, so với lúc train.

> [!example] Thực tế
> Tính đến **tháng 10/2021**, công cụ data validation tích hợp của **TensorFlow Extended (TFX)** vẫn chỉ dùng **summary statistics** để phát hiện skew giữa train và serving, và shift giữa các ngày train.

**Hạn chế:**

- Mean/median/variance chỉ hữu ích khi chúng là **tóm tắt có ý nghĩa** cho phân phối đó.
- Nếu các thống kê **khác nhau đáng kể** → có thể đã shift.
- Nếu các thống kê **giống nhau** → **không đảm bảo** không có shift.

### 8.4 Two-sample hypothesis test

**Two-sample test** kiểm định xem hai tập dữ liệu có đến từ **cùng một phân phối** hay không.

- Nếu khác biệt **có ý nghĩa thống kê** → xác suất khác biệt chỉ do ngẫu nhiên rất thấp → hai tập đến từ **hai phân phối khác nhau**.
- Áp dụng: coi dữ liệu **hôm qua** là source population, **hôm nay** là target population.

> [!warning] Ý nghĩa thống kê ≠ ý nghĩa thực tiễn
> Khác biệt có thể **statistically significant** nhưng **không quan trọng** trong thực tế.
>
> **Heuristic hữu ích:** nếu chỉ cần **mẫu nhỏ** đã phát hiện khác biệt → khả năng cao là khác biệt nghiêm trọng. Nếu phải dùng **rất nhiều mẫu** mới phát hiện → có thể không đáng lo.

#### Kolmogorov–Smirnov test (KS test)

- Là **nonparametric test**: không cần giả định dạng phân phối, không cần tham số của phân phối.
- Dùng được cho **mọi phân phối**.
- **Nhược điểm lớn: chỉ dùng cho dữ liệu 1 chiều.**
  - Hữu ích để phát hiện **label shift** hoặc **prediction shift** khi nhãn/dự đoán là số vô hướng.
  - **Không dùng được cho feature thường có số chiều cao.**
- Có thể **tốn kém** và tạo **quá nhiều false positive**.

#### Các test khác

| Phương pháp | Đặc điểm |
|---|---|
| **Least-Squares Density Difference** | Dựa trên ước lượng density-difference bằng least squares; tác giả cho rằng dùng được cho input đa chiều. |
| **MMD (Maximum Mean Discrepancy)** | Kỹ thuật **kernel-based** cho two-sample testing **đa biến** (Gretton et al., 2012). |
| **Learned Kernel MMD** | Biến thể của MMD (Liu et al., 2020). |
| **Alibi Detect** | Package open-source với nhiều thuật toán drift detection. |

> [!note] Thực tế
> MMD phổ biến trong nghiên cứu, nhưng tại thời điểm viết sách, tác giả **chưa biết công ty nào dùng MMD trong industry**.

> [!tip] Giảm chiều trước khi test
> Two-sample test thường hoạt động tốt hơn trên dữ liệu **ít chiều**. Nên **giảm chiều** feature trước khi test. Tuy nhiên, giảm chiều cũng có thể làm test **kém hiệu quả hơn**.

### 8.5 Time scale windows — chọn cửa sổ thời gian để phát hiện shift

Không phải shift nào cũng dễ phát hiện như nhau:

- **Thay đổi đột ngột** dễ phát hiện hơn **thay đổi chậm, dần dần**.
- Shift có thể xảy ra theo hai chiều:
  - **Spatial shift**: giữa các **điểm truy cập** — nhóm user mới, loại thiết bị mới…
  - **Temporal shift**: theo **thời gian**.

Để phát hiện temporal shift, coi input như **time-series data**.

#### Vấn đề chu kỳ và cửa sổ thời gian

Nếu dữ liệu có **chu kỳ tuần**, cửa sổ **ngắn hơn 1 tuần** sẽ **không thấy được chu kỳ** và dễ báo động sai.

Ví dụ trong sách:

- Nếu lấy **ngày 9 → 14** làm source distribution, thì **ngày 15** trông như một shift.
- Nếu lấy **ngày 1 → 14** làm source distribution, thì các điểm ngày 15 **có thể vẫn thuộc cùng phân phối**.

→ Phát hiện temporal shift rất khó khi shift bị **confound bởi seasonal variation**.

#### Sliding statistics vs Cumulative statistics

| | **Sliding statistics** | **Cumulative statistics** |
|---|---|---|
| Cách tính | Trong **một cửa sổ thời gian**, ví dụ 1 giờ | **Cập nhật liên tục** với nhiều dữ liệu hơn |
| Reset? | **Có** — đầu mỗi cửa sổ reset | **Không** |
| Ưu điểm | Thấy rõ thay đổi trong từng cửa sổ | Ổn định, có nhiều dữ liệu |
| Nhược điểm | Có thể nhiễu | **Che khuất** sự kiện ngắn hạn |

Ví dụ trong sách: **cumulative accuracy** có thể **che mất cú sụt accuracy đột ngột từ giờ 16 đến 18**.

#### Thực hành chọn cửa sổ

- Nhiều công ty lấy **phân phối của dữ liệu train làm baseline**, rồi monitor phân phối production theo **giờ** hoặc **ngày**.
- **Cửa sổ càng ngắn → phát hiện càng nhanh**, nhưng **càng dễ false alarm**.
- Một số platform hỗ trợ **merge** thống kê từ cửa sổ nhỏ thành cửa sổ lớn (ví dụ tính theo giờ rồi merge thành ngày).
- Platform tiên tiến có **Root Cause Analysis (RCA)**: tự phân tích thống kê ở nhiều kích thước cửa sổ để tìm **đúng cửa sổ thời gian xảy ra thay đổi**.

> [!note] Độ phức tạp
> Làm việc với dữ liệu thời gian đòi hỏi kiến thức **time-series analysis**, ví dụ **time-series decomposition** (tách trend, seasonality, residual). Nội dung này nằm ngoài phạm vi sách.

---

## 9. Ứng phó với data distribution shift

### 9.1 Ba hướng tiếp cận

| Hướng | Cách làm | Mức độ phổ biến |
|---|---|---|
| **1. Train trên dữ liệu khổng lồ** | Hy vọng dữ liệu đủ lớn để bao phủ phân phối thực tế; model sẽ gặp dữ liệu "nằm trong phân phối đã học". | Thống trị **nghiên cứu** |
| **2. Thích nghi model mà không cần nhãn mới** | **Domain adaptation**: học biểu diễn bất biến với thay đổi phân phối. | Ít phổ biến, **chưa được ứng dụng rộng** |
| **3. Retrain trên dữ liệu có nhãn của target distribution** | Thu thập nhãn mới rồi huấn luyện lại / fine-tune. | **Phổ biến trong industry** |

**Một số nghiên cứu về hướng 2:**

- **Zhang et al. (2013)**: dùng **causal interpretation** + **kernel embedding** của phân phối có điều kiện và marginal để sửa dự đoán cho cả covariate shift và label shift **mà không cần nhãn** từ target distribution.
- **Zhao et al. (2020)**: **domain-invariant representation learning** — học biểu diễn dữ liệu **bất biến** với thay đổi phân phối, là một dạng **unsupervised domain adaptation**.

> [!caution] Khoảng trống nghiên cứu
> Lĩnh vực này **chưa được khai thác nhiều** và chưa được industry áp dụng rộng rãi.

### 9.2 Retrain: stateless vs stateful

Khi retrain (theo hướng 3), có hai câu hỏi:

**Câu hỏi 1 — Train lại từ đầu hay train tiếp?**

| | **Stateless retraining** | **Stateful training** |
|---|---|---|
| Cách làm | Train **từ đầu** trên dữ liệu cũ + mới | Train tiếp từ **checkpoint** gần nhất |
| Tên khác | — | **Fine-tuning** |
| Ưu điểm | Sạch, không phụ thuộc lịch sử | Nhanh, tận dụng trọng số cũ |
| Nhược điểm | Tốn compute hơn | Có thể mang theo bias cũ |

**Câu hỏi 2 — Dùng dữ liệu trong khoảng thời gian nào?**

- 24 giờ gần nhất?
- 1 tuần?
- 6 tháng?
- Từ thời điểm bắt đầu drift?

> [!tip] Không có công thức chung
> Cần **chạy thực nghiệm** để biết chiến lược retrain nào tốt nhất. Tần suất retrain hiện nay ở nhiều công ty vẫn dựa trên **cảm tính** thay vì dữ liệu thực nghiệm. Công ty nhỏ có ít dữ liệu về model → nên dùng **lịch cố định theo thời gian** thay vì cố overfit lịch retrain vào dữ liệu ít ỏi.

### 9.3 Liên hệ với domain adaptation và transfer learning

- Nếu coi **distribution = domain**, thì thích nghi model với phân phối mới giống **domain adaptation**.
- Nếu coi **học phân phối đồng thời $P(X,Y)$ = task**, thì thích nghi từ phân phối này sang phân phối khác là một dạng **transfer learning**.
- **Khác biệt:** transfer learning thường **không retrain base model from scratch** cho task mới; còn thích nghi với phân phối mới **có thể cần retrain from scratch**.

### 9.4 Thiết kế hệ thống robust với shift ngay từ đầu

Không nhất thiết phải đợi shift xảy ra rồi mới xử lý. Có thể **thiết kế để giảm thiểu tác động**:

#### Chọn feature ổn định

Các feature **shift với tốc độ khác nhau**. Cần cân nhắc **trade-off giữa performance và stability**:

- Ví dụ dự đoán user có tải app không:
  - `app store ranking` rất **dự báo tốt** nhưng **thay đổi rất nhanh** → model phải retrain liên tục.
  - Có thể **bucket** ranking thành nhóm: top 10, 11–100, 101–1.000, 1.001–10.000… → ổn định hơn.
  - `app category` thay đổi **chậm hơn** nhưng **ít predictive power hơn**.

#### Tách model theo thị trường

- Giá nhà ở **San Francisco** thay đổi nhanh hơn nhiều so với **rural Arizona**.
- Nếu dùng **một model chung**, phải cập nhật với tần suất mà SF yêu cầu → tốn kém cho cả hai.
- Nếu dùng **model riêng cho từng thị trường**, mỗi model chỉ cần cập nhật khi cần.

> [!important] Đừng quên lỗi con người
> Không phải mọi suy giảm hiệu năng đều cần giải pháp ML. Nhiều lỗi ML hiện nay vẫn do **con người**. Nếu do lỗi con người, phải **tìm ra lỗi trước** rồi mới sửa. Phát hiện shift đã khó, **xác định nguyên nhân shift còn khó hơn**.

---

## 10. Monitoring và Observability

### 10.1 Phân biệt monitoring và observability

| | **Monitoring** | **Observability** |
|---|---|---|
| Định nghĩa | **Theo dõi, đo lường, ghi log** các metric để biết **khi nào** có vấn đề | Thiết lập hệ thống để **có thể nhìn vào bên trong** và điều tra **cái gì** đã xảy ra |
| Câu hỏi trả lời | "Hệ thống có đang ổn không?" | "Tại sao nó hỏng? Hỏng ở đâu? Với nhóm nào?" |
| Quan hệ | — | **Là một phần của monitoring**; không có observability thì không thể monitoring |
| Ví dụ | Dashboard accuracy, latency | Thêm timer vào function, đếm NaN, trace input qua hệ thống, log input dài bất thường |

Quá trình thiết lập observability còn gọi là **instrumentation**.

> [!note] Định nghĩa từ lý thuyết điều khiển
> **Observability** là khả năng suy ra **trạng thái bên trong** của hệ thống từ **các output thu được lúc runtime**. Đây là giả định **mạnh hơn** monitoring truyền thống.

### 10.2 Operational metrics

Vì ML system là software system, lớp metric đầu tiên cần monitor là **operational metrics** — sức khoẻ của hệ thống. Chia 3 cấp:

1. **Network** — mạng hệ thống chạy trên đó.
2. **Machine** — máy chủ chạy hệ thống.
3. **Application** — ứng dụng.

Ví dụ:

- **Latency**, **throughput**.
- Số **prediction request** nhận được trong phút/giờ/ngày.
- **% request trả về 2xx**.
- **CPU/GPU utilization**, **memory utilization**.

> [!important] Thứ tự ưu tiên
> "No matter how good your ML model is, if the system is down, you're not going to benefit from it." — Model có tốt đến đâu cũng vô nghĩa nếu hệ thống down.

### 10.3 Availability, uptime, SLO, SLA

- **Availability**: hệ thống sẵn sàng phục vụ với hiệu năng hợp lý đến mức nào.
- **Uptime**: **% thời gian** hệ thống "up".
- Điều kiện "up" được định nghĩa trong **SLO (Service Level Objective)** hoặc **SLA (Service Level Agreement)**.

Ví dụ SLA: dịch vụ được coi là "up" nếu **median latency < 200 ms** và **p99 < 2 s**.

Nhà cung cấp có thể cam kết uptime:

- **99,99%** ("four nines") mỗi tháng → chỉ được down **hơn 4 phút/tháng**.
- **99,999%** ("five nines") → chỉ được down **khoảng 26 giây/tháng**.

Ví dụ thực tế (tháng 10/2021): **AWS EC2** cam kết uptime tối thiểu **99,99%/tháng**; nếu thấp hơn, khách được **service credit** cho các kỳ thanh toán EC2 sau.

> [!warning] Với ML system, "up" là chưa đủ
> Hệ thống có thể **up** nhưng dự đoán **rác** → người dùng vẫn không hài lòng. Vì vậy cần thêm **ML-specific metrics**.

---

## 11. ML-specific metrics: 4 artifact cần monitor

Bốn artifact ở bốn giai đoạn của pipeline:

```
Raw inputs  →  Features  →  Predictions  →  Accuracy-related metrics
   (1)           (2)            (3)                  (4)
```

> [!important] Quy luật đánh đổi
> Artifact **càng sâu trong pipeline**:
> - Càng qua **nhiều bước biến đổi** → thay đổi ở đó **càng dễ do lỗi ở một bước biến đổi**.
> - Nhưng càng **có cấu trúc** và càng **gần metric ta thực sự quan tâm** → **càng dễ monitor**.

### 11.1 Accuracy-related metrics

- Nếu hệ thống nhận **bất kỳ feedback nào** từ người dùng — click, hide, purchase, upvote, downvote, favorite, bookmark, share… → **phải log và theo dõi**.
- Feedback có thể dùng để suy ra **natural labels**, rồi tính accuracy/F1/recall…
- Đây là metric **trực tiếp nhất** để biết model có giảm hiệu năng không.

**Ví dụ YouTube:**

- Theo dõi **click-through rate (CTR)**.
- Đồng thời theo dõi **thời gian xem** và **completion rate**.
- Nếu CTR giữ nguyên nhưng completion rate giảm → recommender có thể đang **tệ đi**.

> [!caution] Bẫy metric
> Dùng **completion rate** làm mục tiêu tối ưu có thể khiến recommender **thiên về video ngắn**.

**Ví dụ Google Translate:**

- Cho phép user **upvote/downvote** bản dịch.
- Nếu số downvote tăng đột ngột → có thể có vấn đề.
- Downvote còn **hướng dẫn quá trình gán nhãn**: chuyên gia tạo bản dịch mới cho các mẫu bị downvote để train vòng sau.

### 11.2 Predictions

- **Regression**: mỗi dự đoán là **số liên tục** (giá nhà).
- **Classification**: mỗi dự đoán là **giá trị rời rạc** (lớp dự đoán).
- Mỗi dự đoán thường **ít chiều** → dễ visualize, dễ tính summary statistics.

**Lợi ích:**

- Dễ chạy **two-sample test** để phát hiện **prediction distribution shift**.
- Là **proxy cho input distribution shift**: nếu model không đổi (weights/bias giữ nguyên) mà phân phối dự đoán đổi → nhiều khả năng **phân phối input đã đổi**.
- Phát hiện **điều bất thường**: ví dụ model dự đoán **toàn False** trong 10 phút liên tiếp.
- **Phát hiện sớm hơn accuracy**: nhãn có thể trễ hàng ngày/tuần, nhưng "toàn False trong 10 phút" thấy ngay.

### 11.3 Features

Industry tập trung monitor **feature** — cả feature đầu vào model và **các biến đổi trung gian** từ raw input thành feature cuối.

**Vì sao?** Feature **có cấu trúc**, theo **schema định trước**, dễ kiểm tra hơn raw input.

#### Feature validation

Bước đầu tiên: đảm bảo feature tuân theo **schema mong đợi**. Schema thường sinh từ **dữ liệu train** hoặc **common sense**.

Các kiểm tra phổ biến:

- Min/max/median của feature nằm trong **khoảng chấp nhận**.
- Giá trị feature khớp **regular expression**.
- Mọi giá trị thuộc **tập giá trị định trước**.
- Feature A **luôn lớn hơn** feature B.

Vì feature thường ở dạng **bảng** (cột = feature, dòng = mẫu), feature validation còn gọi là:

- **Table testing** / **table validation**.
- **Unit tests for data**.

**Công cụ open-source phổ biến:**

- **Great Expectations**
- **Deequ** (AWS)

#### Phát hiện shift bằng two-sample test

- Có thể dùng two-sample test cho **một feature** hoặc **một nhóm feature**.
- Feature có thể **nhiều chiều** → có thể cần **giảm chiều** trước, nhưng giảm chiều có thể làm test **kém hiệu quả**.

### 11.4 Bốn vấn đề lớn khi feature monitoring

1. **Chi phí và độ trễ**
   - Một công ty có thể có **hàng trăm model**, mỗi model dùng **hàng trăm/hàng nghìn feature**.
   - Tính summary statistics cho tất cả feature mỗi giờ có thể **rất tốn compute và memory**.
   - Theo dõi quá nhiều metric có thể **làm chậm hệ thống**, tăng latency cho user và tăng thời gian phát hiện anomaly.

2. **Feature shift không đồng nghĩa model hỏng + alert fatigue**
   - Về lý thuyết, shift nhỏ có thể gây lỗi thảm khốc; nhưng thực tế **thay đổi nhỏ của một feature riêng lẻ thường không ảnh hưởng**.
   - Feature **shift liên tục**, phần lớn **lành tính**.
   - Nếu alert mỗi khi feature "có vẻ" drift → **quá nhiều false positive** → đội monitoring **mất tập trung** vì **alert fatigue**.
   - Bài toán trở thành: **xác định shift nào là critical**.

3. **Provenance phức tạp**
   - Feature extraction thường qua **nhiều bước** (fill missing, standardization), dùng **nhiều thư viện** (pandas, Spark), trên **nhiều service** (BigQuery, Snowflake).
   - Input có thể là **relational database**, output là **NumPy array**.
   - Khi phát hiện thay đổi có hại, **khó biết** đó là do **phân phối input gốc đổi** hay do **lỗi ở một bước xử lý**.

4. **Schema thay đổi theo thời gian**
   - Nếu không có cách **version schema** và map mỗi feature với schema mong đợi, alert có thể do **schema không khớp**, không phải do dữ liệu đổi.

> [!note] Kết luận
> Những vấn đề trên **không phủ nhận** giá trị của feature monitoring. Thay đổi trong feature space vẫn là **nguồn tín hiệu hữu ích** để hiểu sức khoẻ hệ ML — nhưng cần chọn giải pháp phù hợp.

### 11.5 Raw inputs

- Thay đổi ở feature có thể do **bước xử lý**, không phải do dữ liệu. Vậy monitor **raw input trước khi xử lý** thì sao?
- Raw input **không dễ monitor hơn**: đến từ **nhiều nguồn**, **nhiều format**, **nhiều cấu trúc**.
- Trong nhiều workflow, ML engineer **không có quyền truy cập trực tiếp** raw input. Dữ liệu thường do **data platform team** quản lý, xử lý rồi đưa vào **data warehouse**; ML engineer chỉ query được dữ liệu **đã xử lý một phần**.
- → Monitor raw input thường là **trách nhiệm của data platform team**, không phải data science/ML team; nằm ngoài phạm vi sách.

---

## 12. Monitoring toolbox: Logs — Dashboards — Alerts

Industry hay nói **metrics, logs, traces** là "ba trụ cột của monitoring". Tác giả thấy cách phân biệt này **mơ hồ**:

- **Traces** là một dạng **logs**.
- **Metrics** có thể **tính từ logs**.

Thay vào đó, chương này nhìn từ góc độ **người dùng** hệ thống monitoring: **logs, dashboards, alerts**.

### 12.1 Logs

**Event** là bất cứ điều gì đáng quan tâm với developer, tại lúc xảy ra hoặc sau này để debug/phân tích:

- Container khởi động, lượng memory dùng.
- Function được gọi, chạy xong.
- Các function khác được gọi.
- Input/output của function.
- Crash, stack trace, error code…

> [!quote] Ian Malpass (Etsy)
> "If it moves, we track it." — Và họ còn track cả những thứ **chưa** thay đổi, phòng khi sau này nó thay đổi.

**Quy mô:**

- Năm 2019, app hẹn hò **Badoo** xử lý **20 tỷ event/ngày**.
- Khi có sự cố, phải query log để tìm chuỗi sự kiện → như **tìm kim đáy bể**.

**Vì sao khó:**

- Hệ thống hiện đại gồm nhiều component: container, scheduler, microservice, polyglot persistence, mesh routing, auto-scaling instance, serverless Lambda…
- Một request có thể qua **20–30 hop** từ lúc gửi đến lúc nhận response.
- Khó không chỉ là **khi nào** xảy ra, mà là **ở đâu**.

#### Distributed tracing

- Gán **unique ID** cho mỗi process/request.
- Khi lỗi, error message (hy vọng) chứa ID đó → search ra các log liên quan.
- Ghi kèm **metadata**: thời điểm, service, function, user liên quan…

#### Thị trường và ứng dụng ML

- Thị trường **log management** ước tính **2,3 tỷ USD (2021)** → dự kiến **4,1 tỷ USD (2026)**.
- Phân tích hàng tỷ event thủ công là vô nghĩa → nhiều công ty dùng ML:
  - **Anomaly detection**: phát hiện event bất thường.
  - **Phân loại event** theo mức ưu tiên: usual, abnormal, exception, error, fatal.
  - **Ước lượng xác suất service liên quan bị ảnh hưởng** khi một service fail — hữu ích khi bị **tấn công mạng**.

#### Batch vs Stream processing

| | **Batch** | **Stream** |
|---|---|---|
| Cách làm | Gom nhiều log, query định kỳ bằng SQL hoặc xử lý bằng Spark/Hadoop/Hive | Xử lý event **ngay khi được log** |
| Ưu điểm | Hiệu quả, tận dụng distributed/MapReduce, throughput cao | Phát hiện anomaly **ngay** |
| Nhược điểm | Chỉ phát hiện vấn đề **định kỳ** | Phức tạp hơn |
| Công cụ | Spark, Hadoop, Hive | **Kafka**, **Amazon Kinesis** để transport; **KSQL**, **Flink SQL** để query streaming |

### 12.2 Dashboards

- "A picture is worth a thousand words." Một dãy số có thể vô nghĩa, nhưng **visualize** lên graph có thể lộ ra quan hệ.
- Dashboard giúp monitoring **tiếp cận được với non-engineer**: product manager, business developer…
- **Nhưng graph không đủ**: cần **kinh nghiệm và kiến thức thống kê**. Ví dụ hai graph loss dao động mạnh — rất khó nói có shift hay không.
- **Dashboard rot**: quá nhiều metric trên dashboard **phản tác dụng**. Cần chọn **đúng metric** hoặc **abstract metric cấp thấp** thành **tín hiệu cấp cao** có ý nghĩa hơn.

### 12.3 Alerts

Một alert gồm **3 thành phần**:

1. **Alert policy** — điều kiện kích hoạt.
   - Ví dụ: accuracy < 90%; HTTP latency > 1 giây **kéo dài ít nhất 10 phút**.
2. **Notification channels** — ai/nơi nào nhận.
   - Hiển thị trong monitoring service (Amazon CloudWatch, GCP Cloud Monitoring).
   - Đồng thời gửi email (`mlops-monitoring@...`), Slack (`#mlops-monitoring`), **PagerDuty**…
3. **Description** — giúp người nhận hiểu chuyện gì đang xảy ra.
   - Càng chi tiết càng tốt: timestamp, service name…
   - Nên kèm **hướng dẫn xử lý** hoặc **runbook** — tập hợp quy trình/thao tác thường gặp để xử lý alert.

> [!danger] Alert fatigue
> **Alert fatigue** là hiện tượng có thật và nguy hiểm:
> - **Làm nản lòng**: không ai thích bị gọi dậy lúc nửa đêm vì việc ngoài trách nhiệm.
> - **Nguy hiểm**: tiếp xúc nhiều alert vô nghĩa khiến người ta **mất nhạy cảm** với alert quan trọng.
>
> → Chỉ nên gửi alert khi thật sự **critical**, với **điều kiện có ý nghĩa**.

---

## 13. Observability — nhìn sâu vào bên trong hệ thống

### 13.1 Vì sao cần observability?

- **Monitoring** không giả định gì về quan hệ giữa **trạng thái bên trong** và **output**. Ta chỉ nhìn output bên ngoài để đoán khi nào bên trong hỏng — **không đảm bảo** output đủ để tìm ra nguyên nhân.
- Ngày trước, hệ thống đơn giản: vài component, team kiểm soát toàn bộ codebase → có thể sửa và thử để tìm lỗi.
- Ngày nay, hệ thống gồm **nhiều component**, nhiều component là **service của công ty khác** (cloud-native) → team **không kiểm soát** phần bên trong.
- Khi có sự cố, không thể "mổ" hệ thống ra xem → phải dựa vào **output bên ngoài**.

### 13.2 Định nghĩa

**Observability** (từ **control theory**) là việc tạo **khả năng nhìn thấy rõ hơn** để hiểu hành vi phức tạp của phần mềm, dựa trên **output thu được lúc runtime**.

Giả định mạnh hơn monitoring:

> **Trạng thái bên trong** của hệ thống có thể được **suy ra** từ hiểu biết về **output bên ngoài**.

Trạng thái bên trong gồm:

- **Current state**: GPU utilization **ngay bây giờ**.
- **Historical state**: GPU utilization **trung bình ngày hôm qua**.

Khi hệ thống **observable**, có thể tìm ra lỗi bằng **logs và metrics** mà **không cần ship code mới**.

### 13.3 Telemetry

**Telemetry** = output của hệ thống thu thập lúc runtime.

- Gốc Hy Lạp: **tele** = "remote", **metron** = "measure" → "đo từ xa".
- Trong monitoring: **logs và metrics** thu từ các component ở xa (cloud service, app trên thiết bị người dùng…).

### 13.4 Observability cho ML

- Monitoring quanh **metric tổng hợp (aggregated)**.
- Observability cho phép metric **fine-grained** hơn: biết model giảm hiệu năng **với loại input nào, nhóm user nào, trong khoảng thời gian nào**.
- Cần **log output với tag** và các định danh để sau này **slice/dice** theo nhiều chiều.

Ví dụ câu query mong muốn:

- "Cho tôi tất cả user mà model A dự đoán sai trong 1 giờ qua, **group by zip code**."
- "Cho tôi các **request outlier** trong 10 phút qua."
- "Cho tôi **toàn bộ intermediate output** của input này qua hệ thống."

> [!important] Observability bao gồm interpretability
> Trong ML, **observability bao trùm interpretability**:
> - **Interpretability** giúp hiểu **model** hoạt động thế nào.
> - **Observability** giúp hiểu **toàn bộ hệ thống ML** (gồm model) hoạt động thế nào.
>
> Ví dụ: khi hiệu năng giảm trong 1 giờ qua, biết **feature nào đóng góp nhiều nhất vào các dự đoán sai** sẽ giúp tìm nguyên nhân và cách sửa.

> [!caution] Monitoring là bị động
> Monitoring **chờ** shift xảy ra rồi mới phát hiện; nó **phát hiện vấn đề nhưng không sửa**. Bước tiếp theo — **continual learning** — chủ động cập nhật model để thích nghi (Chương 9).

---

## 14. Tổng kết chương

### 14.1 Sơ đồ nguyên nhân → phát hiện → xử lý

```text
Model giảm hiệu năng trong production
│
├── Software system failures (60/96 vụ tại Google)
│   ├── Dependency / Deployment / Hardware / Downtime
│   └── Xử lý: kỹ năng software engineering
│
└── ML-specific failures
    ├── Dữ liệu production khác dữ liệu train
    │   ├── Train-serving skew
    │   ├── Data distribution shift
    │   │   ├── Covariate shift  P(X) đổi
    │   │   ├── Label shift      P(Y) đổi
    │   │   ├── Concept drift    P(Y|X) đổi
    │   │   ├── Feature change
    │   │   └── Label schema change
    │   └── Nhiều "shift" thực ra là lỗi pipeline/con người (~80%)
    ├── Edge cases (khác outlier)
    └── Degenerate feedback loops
        ├── Phát hiện: popularity diversity, hit rate theo popularity bucket
        └── Sửa: randomization, positional features

Phát hiện shift
├── Accuracy metrics (cần nhãn, thường trễ)
├── Summary statistics (min/max/mean/median/var/quantile/skew/kurtosis)
├── Two-sample tests (KS 1D; MMD, LSDD đa biến; Alibi Detect)
└── Time-scale windows (sliding vs cumulative; seasonal confound)

Ứng phó
├── Train dữ liệu khổng lồ
├── Domain adaptation không cần nhãn (chưa phổ biến)
├── Retrain trên target labels (phổ biến)
│   └── Stateless vs Stateful; chọn cửa sổ dữ liệu
└── Thiết kế robust: feature ổn định, model riêng theo thị trường

Giám sát
├── Operational metrics: latency, throughput, CPU/GPU, uptime, SLO/SLA
├── 4 artifact: accuracy → predictions → features → raw inputs
└── Toolbox: logs (distributed tracing, batch/stream)
             dashboards (dashboard rot)
             alerts (policy, channel, description/runbook)
             observability (telemetry, tag, slicing, interpretability)
```

### 14.2 Những con số cần nhớ

| Con số | Ý nghĩa |
|---|---|
| **96 vụ** pipeline ML hỏng tại Google | **60 vụ** không liên quan trực tiếp ML |
| **~80%** drift | Ước lượng do **lỗi con người** (CTO một công ty monitoring) |
| **99,99% uptime/tháng** | Được phép down **hơn 4 phút/tháng** |
| **99,999% uptime/tháng** | Được phép down **~26 giây/tháng** |
| **20 tỷ event/ngày** | Badoo xử lý năm 2019 |
| **2,3 → 4,1 tỷ USD** | Thị trường log management 2021 → 2026 |
| **20–30 hop** | Một request có thể đi qua trong hệ microservice hiện đại |

### 14.3 Các hình trong PDF

| Hình | Nội dung |
|---|---|
| **8-1** | Decision boundary khi không có outlier vs khi có một outlier — outlier có thể làm boundary lệch rõ rệt và kém chính xác hơn. |
| **8-2** | Một số thuật toán drift detection được Alibi Detect triển khai (ảnh chụp GitHub repo). |
| **8-3** | Cùng một chuỗi dữ liệu, việc kết luận "có drift" hay không phụ thuộc vào **cửa sổ thời gian** được chọn. |
| **8-4** | **Cumulative accuracy** che mất cú sụt accuracy đột ngột giữa giờ 16 và 18. |
| **8-5** | Bốn artifact trong pipeline (raw inputs → features → predictions → accuracy metrics) và mức độ biến đổi của chúng. |
| **8-6** | Google Translate cho phép người dùng upvote/downvote bản dịch. |
| **8-7** | Một số hàm feature validation tích hợp của Great Expectations và ví dụ sử dụng. |
| **8-8** | Hai graph loss dao động mạnh — graph hữu ích nhưng **không đủ** để kết luận có shift. |

### 14.4 Checklist thực hành

- [ ] Định nghĩa rõ **operational expectation** và **ML performance expectation**; đặt SLO/SLA.
- [ ] Log **mọi user feedback** có thể dùng làm natural label.
- [ ] Monitor **4 artifact**: accuracy → predictions → features → raw inputs; ưu tiên metric gần ground truth.
- [ ] Dùng **two-sample test** trên dữ liệu ít chiều; **giảm chiều** trước khi test feature nhiều chiều.
- [ ] Chọn **cửa sổ thời gian** phù hợp chu kỳ (tuần/tháng); dùng cả **sliding** và **cumulative**.
- [ ] **Version schema** feature và label; kiểm tra schema trước khi kết luận drift.
- [ ] Kiểm tra **lỗi pipeline / phiên bản model / feature consistency** trước khi đổ lỗi cho data shift.
- [ ] Thiết kế **feature ổn định**, cân nhắc **model riêng theo thị trường**.
- [ ] Alert có **policy, channel, description, runbook**; tránh **alert fatigue**.
- [ ] Đầu tư **observability**: tag, trace ID, log đủ chi tiết để slice theo user/input/thời gian.
- [ ] Chạy **thực nghiệm** để chọn chiến lược retrain (stateless/stateful, cửa sổ dữ liệu, tần suất).

---

## 15. Câu hỏi tự kiểm tra

> [!question]- 1. Phân biệt operational expectation và ML performance expectation. Vì sao ML system "fail silently"?
> Operational expectation là các chỉ số vận hành (latency, throughput, không crash). ML performance expectation là chất lượng dự đoán (accuracy, F1…). ML performance khó phát hiện vì cần **ground truth**; nếu không có nhãn, model có thể sai hàng loạt mà không ai biết → fail silently.

> [!question]- 2. Kể tên 4 loại software system failure và 6 loại ML-specific failure.
> Software: dependency failure, deployment failure, hardware failure, downtime/crashing.
> ML-specific: vấn đề thu thập/xử lý dữ liệu, hyperparameter kém, training/inference pipeline không nhất quán, data distribution shift, edge cases, degenerate feedback loops.

> [!question]- 3. Vì sao giả định "train và test cùng phân phối stationary" thường sai?
> Vì (1) dữ liệu thực tế đa dạng, tập train hữu hạn và bị selection/sampling bias → không đại diện; (2) thế giới không stationary, phân phối thay đổi đột ngột/dần dần/theo mùa.

> [!question]- 4. Outlier và edge case khác nhau thế nào?
> Outlier nói về **dữ liệu** (mẫu khác biệt). Edge case nói về **hiệu năng** (mẫu model làm tệ hơn đáng kể). Outlier có thể là edge case, nhưng không phải outlier nào cũng là edge case.

> [!question]- 5. Degenerate feedback loop là gì? Nêu một ví dụ và hai cách giảm thiểu.
> Là vòng lặp mà output của hệ thống ảnh hưởng đến input tương lai, rồi input này lại ảnh hưởng output. Ví dụ: recommender xếp bài A cao → user click nhiều → model càng xếp A cao. Giảm thiểu: (1) randomization/exploration (TikTok, contextual bandits); (2) positional features hoặc mô hình hai bước exposure → click.

> [!question]- 6. Điền điều kiện phân phối cho covariate shift, label shift, concept drift.
> Covariate: $P(X)$ đổi, $P(Y \vert X)$ giữ nguyên.
> Label: $P(Y)$ đổi, $P(X \vert Y)$ giữ nguyên.
> Concept: $P(Y \vert X)$ đổi, $P(X)$ giữ nguyên.

> [!question]- 7. Vì sao không nên chỉ dùng summary statistics để phát hiện shift?
> Vì mean/median/variance chỉ là tóm tắt hữu ích cho một số phân phối. Nếu chúng khác nhau có thể có shift, nhưng nếu giống nhau **không đảm bảo** không có shift. Cần two-sample test hoặc kiểm tra kỹ hơn.

> [!question]- 8. KS test mạnh và yếu ở đâu?
> Mạnh: nonparametric, không giả định phân phối, dùng được cho mọi phân phối 1 chiều; hữu ích cho label/prediction shift dạng scalar. Yếu: chỉ 1 chiều, không dùng được cho feature nhiều chiều; có thể tốn kém và nhiều false positive.

> [!question]- 9. Sliding statistics khác cumulative statistics thế nào? Cho ví dụ về tác hại của cumulative.
> Sliding tính trong một cửa sổ và reset đầu mỗi cửa sổ; cumulative cập nhật liên tục, không reset. Cumulative có thể che mất cú sụt accuracy ngắn hạn (ví dụ từ giờ 16–18) vì bị pha loãng bởi dữ liệu cũ.

> [!question]- 10. Monitoring và observability khác nhau thế nào?
> Monitoring theo dõi/đo/log metric để biết **khi nào** có vấn đề. Observability thiết lập hệ thống để có thể **suy ra trạng thái bên trong từ output** và điều tra **cái gì/ở đâu/tại sao**. Observability là một phần của monitoring; không có observability thì không monitoring được đầy đủ.

> [!question]- 11. Bốn artifact cần monitor trong ML system là gì? Vì sao càng sâu pipeline càng dễ monitor nhưng cũng càng dễ bị lỗi biến đổi?
> Raw inputs → features → predictions → accuracy metrics. Càng sâu, càng qua nhiều bước biến đổi nên thay đổi dễ do lỗi ở một bước; nhưng càng có cấu trúc và càng gần metric quan tâm nên càng dễ monitor.

> [!question]- 12. Ba thành phần của một alert là gì?
> Alert policy (điều kiện), notification channels (ai/nơi nhận), description (mô tả + runbook/hướng xử lý).

---

## 16. Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| **Train-serving skew** | Model tốt khi train nhưng kém khi serving do dữ liệu/feature lúc train và inference khác nhau. |
| **Covariate shift** | $P(X)$ đổi, $P(Y \vert X)$ không đổi. |
| **Label shift / prior shift / target shift** | $P(Y)$ đổi, $P(X \vert Y)$ không đổi. |
| **Concept drift / posterior shift** | $P(Y \vert X)$ đổi, $P(X)$ không đổi. |
| **Feature change** | Tập feature hoặc miền giá trị của feature thay đổi. |
| **Label schema change** | Cấu trúc/tập giá trị của nhãn thay đổi (thêm lớp, đổi range…). |
| **Source / target distribution** | Phân phối dùng để train / phân phối lúc inference. |
| **Importance weighting** | Gán trọng số mẫu train theo tỷ lệ mật độ target/source để hiệu chỉnh covariate shift. |
| **Two-sample test** | Kiểm định hai tập dữ liệu có đến từ cùng phân phối hay không. |
| **KS test** | Kolmogorov–Smirnov, nonparametric, chỉ 1 chiều. |
| **MMD** | Maximum Mean Discrepancy, kernel-based, đa biến. |
| **Sliding / cumulative statistics** | Thống kê theo cửa sổ có reset / thống kê tích luỹ không reset. |
| **Stateless / stateful retraining** | Train lại từ đầu / train tiếp từ checkpoint (fine-tuning). |
| **Degenerate feedback loop** | Output ảnh hưởng input tương lai, tạo vòng tự khuếch đại. |
| **Popularity bias / filter bubble** | Thiên lệch về item phổ biến, làm giảm đa dạng. |
| **Positional feature** | Feature mã hoá vị trí hiển thị để giảm bias do vị trí. |
| **SLO / SLA** | Service Level Objective / Agreement — cam kết mức dịch vụ. |
| **Uptime** | % thời gian hệ thống sẵn sàng. |
| **Telemetry** | Dữ liệu output thu lúc runtime (logs, metrics…). |
| **Instrumentation** | Việc thêm logging/metric/tracing vào hệ thống để quan sát. |
| **Alert fatigue** | Mất nhạy cảm với alert do quá nhiều cảnh báo không quan trọng. |
| **Dashboard rot** | Dashboard quá nhiều metric, làm giảm hiệu quả monitoring. |
| **Observability** | Khả năng suy ra trạng thái bên trong từ output runtime. |

---

> [!success] Chốt lại
> **Deploy là bắt đầu, không phải kết thúc.** Hãy giả định model sẽ hỏng, dữ liệu sẽ đổi, và người dùng sẽ phản hồi theo cách làm lệch chính model. Xây **monitoring + observability** đủ tốt để phát hiện sớm, phân biệt **lỗi pipeline** với **shift thật**, rồi **retrain có kỷ luật** — đó là nội dung cốt lõi của chương này và là nền cho **continual learning** ở Chương 9.

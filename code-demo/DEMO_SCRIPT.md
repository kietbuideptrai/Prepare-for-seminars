# Kịch bản demo — nói gì khi chiếu code

Mỗi demo dài **30–60 giây**. Không đọc code; chỉ nói 1 ý và chỉ vào 1 con số/hình.

> **Bản notebook:** mỗi demo có một notebook tương ứng trong `../notebooks/` (ví dụ `03_Feedback_Loop.ipynb`). Mở notebook, **Run All**, rồi chiếu hình inline — không cần gõ lệnh terminal.
> Hướng dẫn tạo slide đầy đủ: [../README.md](../README.md).

| Demo | Script | Notebook |
|---|---|---|
| 1 | `01_model_decay.py` | `01_Model_Decay.ipynb` |
| 2 | `02_edge_case_outlier.py` | `02_Edge_Case_Outlier.ipynb` |
| 3 | `03_feedback_loop.py` | `03_Feedback_Loop.ipynb` |
| 4 | `04_shift_types.py` | `04_Shift_Types.ipynb` |
| 5 | `05_detect_shift.py` | `05_Detect_Shift.ipynb` |
| 6 | `06_monitoring.py` | `06_Monitoring.ipynb` |
| 7 | `07_retrain_window.py` | `07_Retrain_Window.ipynb` |

---

## Demo 1 — Model hỏng dần (slide 2 & 5)

```bash
python3 01_model_decay.py
```

**Chiếu:** `figures/01_model_decay.png`

**Nói:**
> “Model train 12 tháng đầu, MAE khoảng 4,9. Một năm sau, cùng model đó, MAE lên 18,8 — gần gấp 4. Model không đổi; thế giới đổi. Retrain ở tháng 18 kéo MAE về 8,4.”

**Chốt:** deploy là bắt đầu, không phải kết thúc.

---

## Demo 2 — Một outlier phá boundary (slide 6)

```bash
python3 02_edge_case_outlier.py
```

**Chiếu:** `figures/02_edge_case_outlier.png`

**Nói:**
> “Bên trái: accuracy 0,99. Bên phải: thêm đúng một outlier nhãn sai, accuracy còn 0,82. Một mẫu cực đoan đủ để kéo boundary và làm sai hàng loạt.”

**Chốt:** outlier nói về dữ liệu; edge case nói về hiệu năng.

---

## Demo 3 — Feedback loop (slide 7 & 8)

```bash
python3 03_feedback_loop.py
```

**Chiếu:** `figures/03_feedback_loop.png`

**Nói:**
> “A và B chất lượng thật bằng nhau, đều CTR 0,10. Greedy cho A đứng đầu 100% vòng, rồi kết luận A tốt hơn — CTR naive 0,099 so với 0,040. Chia cho position multiplier thì cả hai về 0,10. Đó là popularity bias.”

**Chốt:** model tự tạo dữ liệu cho vòng sau; randomization hoặc positional features phá vòng lặp.

---

## Demo 4 — Ba loại shift (slide 9–13)

```bash
python3 04_shift_types.py
```

**Chiếu:** `figures/04_shift_types.png`

**Nói:**
> “Cùng một model. Covariate shift: accuracy 0,91 xuống 0,10 vì model chưa từng thấy vùng input mới. Label shift: accuracy không giảm mạnh, nhưng model dự đoán positive 0,24 trong khi tỷ lệ thật chỉ 0,11. Concept drift: quy luật đảo, accuracy gần 0.”

**Chốt:** mỗi loại shift cần cách đo và cách ứng phó khác nhau.

---

## Demo 5 — Phát hiện shift (slide 14 & 15)

```bash
python3 05_detect_shift.py
```

**Chiếu:** `figures/05_detect_shift.png`

**Nói:**
> “KS và MMD bắt đúng ca khác phân phối, p xấp xỉ 0,001. Nhưng cùng dữ liệu, nếu cửa sổ baseline bỏ sót thứ 2, p = 0,026 — báo shift sai; cửa sổ đủ 12 tuần, p = 0,156 — không shift. Và sliding thấy cú sụt còn 0,67, cumulative chỉ còn 0,85.”

**Chốt:** phải biết loại nào, đo bằng gì, trong cửa sổ nào.

---

## Demo 6 — Monitoring (slide 18–21)

```bash
python3 06_monitoring.py
```

**Chiếu:** `figures/06_monitoring.png`

**Nói:**
> “Sự cố thật ở giờ 150. Alert feature mean và prediction rate bắt ngay giờ 150. Accuracy chỉ báo ở giờ 174 vì nhãn trễ 24 giờ. Vì vậy phải monitor cả 4 tầng artifact, không chờ accuracy.”

**Chốt:** monitor để biết, observability để hiểu, retrain để thích nghi.

---

## Demo 7 — Retrain (slide 16 & 17)

```bash
python3 07_retrain_window.py
```

**Chiếu:** `figures/07_retrain_window.png`

**Nói:**
> “Cửa sổ 7 ngày được 0,967; 30 ngày 0,970; nhưng 180 ngày chỉ còn 0,867 vì học quy luật cũ. Với ít dữ liệu mới, fine-tune tốt hơn train lại từ đầu; có đủ dữ liệu mới thì stateless bắt kịp. Không có con số chung — phải thực nghiệm.”

**Chốt:** chọn cửa sổ retrain là bài toán thực nghiệm, không phải cảm tính.

---

## Phương án dự phòng

| Tình huống | Xử lý |
|---|---|
| Máy chiếu không chạy được terminal | Chỉ chiếu hình PNG trong `figures/` |
| Hết thời gian | Bỏ demo 1 và 7, giữ demo 3 và 6 vì trực quan nhất |
| Bị hỏi “code đâu?” | Mở `code-demo/` hoặc notebook tương ứng; chỉ vào file/slide |
| Không có Python trên máy trình chiếu | Dùng hình đã xuất sẵn; code chỉ để tham khảo |
| Cần demo live | Chạy trước một lần; mỗi demo chỉ mất 1–5 giây. Hoặc mở notebook đã Run All sẵn |

# Code demo — Chương 8: Data Distribution Shifts & Monitoring

Bộ code chạy được để minh hoạ các ý chính trong 22 slide. Mỗi file in kết quả ra terminal và xuất **một hình PNG** vào `figures/` để chèn thẳng vào slide.

> **Có hai cách dùng:**
> - **Notebook (khuyên dùng khi thuyết trình):** mở `../notebooks/00_Index.ipynb` — có markdown giải thích, hình inline, số liệu kỳ vọng và “ý nghĩa cho slide”.
> - **Script (khuyên dùng khi cần xuất lại toàn bộ hình):** chạy `python3 run_all.py`.

## Chạy nhanh

### Cách 1 — Notebook

```bash
cd "30 Projects/ML - Seminar"
pip install -r code-demo/requirements.txt
pip install jupyterlab
jupyter lab
```

Mở `notebooks/00_Index.ipynb` → chọn demo → **Run All**.

### Cách 2 — Script

```bash
cd "30 Projects/ML - Seminar/code-demo"
python3 run_all.py
```

Hoặc chạy từng demo:

```bash
python3 01_model_decay.py
python3 03_feedback_loop.py
```

## Yêu cầu

- Python 3.10+
- `numpy`, `matplotlib`
- **Không cần** `scipy`, `pandas`, `scikit-learn` — KS test, MMD, logistic regression đều được cài tối giản trong `common.py`.

Kiểm tra môi trường:

```bash
python3 -c "import numpy, matplotlib; print('OK')"
```

## Cấu trúc

```text
code-demo/
├── common.py                  # helper: logistic regression, KS, MMD, summary stats
├── run_all.py                 # chạy tất cả demo
├── 01_model_decay.py          # slide 2, 5  — model hỏng dần sau deploy
├── 02_edge_case_outlier.py    # slide 6     — outlier phá decision boundary
├── 03_feedback_loop.py        # slide 7, 8  — popularity bias, randomization
├── 04_shift_types.py          # slide 9–13  — covariate / label / concept
├── 05_detect_shift.py         # slide 14, 15 — KS, MMD, time window
├── 06_monitoring.py           # slide 18–21 — 4 artifact, alert trễ
├── 07_retrain_window.py       # slide 16, 17 — cửa sổ retrain, stateless/stateful
├── SLIDE_CODE.md              # snippet ngắn để dán lên slide
├── DEMO_SCRIPT.md             # nói gì khi chiếu từng demo
├── requirements.txt
└── figures/                   # hình xuất ra

../notebooks/                  # bản notebook của 7 demo
├── README.md                  # hướng dẫn chạy notebook
├── 00_Index.ipynb             # bắt đầu từ đây
├── 01_Model_Decay.ipynb
├── 02_Edge_Case_Outlier.ipynb
├── 03_Feedback_Loop.ipynb
├── 04_Shift_Types.ipynb
├── 05_Detect_Shift.ipynb
├── 06_Monitoring.ipynb
└── 07_Retrain_Window.ipynb
```

## Map slide → demo → hình → notebook

| Slide | Nội dung | Demo | Hình | Notebook |
|---|---|---|---|---|
| 2 | Model tốt chết sau một năm | `01_model_decay.py` | `01_model_decay.png` | `01_Model_Decay.ipynb` |
| 5 | Train-serving skew / drift | `01_model_decay.py`, `04_shift_types.py` | `01`, `04` | `01`, `04` |
| 6 | Edge case vs outlier | `02_edge_case_outlier.py` | `02_edge_case_outlier.png` | `02_Edge_Case_Outlier.ipynb` |
| 7 | Degenerate feedback loop | `03_feedback_loop.py` | `03_feedback_loop.png` | `03_Feedback_Loop.ipynb` |
| 8 | Phát hiện & phá vòng lặp | `03_feedback_loop.py` | `03_feedback_loop.png` | `03_Feedback_Loop.ipynb` |
| 9–13 | Ba loại shift + schema change | `04_shift_types.py` | `04_shift_types.png` | `04_Shift_Types.ipynb` |
| 14 | Accuracy không đủ; summary stats | `05_detect_shift.py` | `05_detect_shift.png` | `05_Detect_Shift.ipynb` |
| 15 | Two-sample test & time window | `05_detect_shift.py` | `05_detect_shift.png` | `05_Detect_Shift.ipynb` |
| 16 | Retrain: cửa sổ, stateless/stateful | `07_retrain_window.py` | `07_retrain_window.png` | `07_Retrain_Window.ipynb` |
| 17 | Thiết kế để ít retrain | `07_retrain_window.py` | `07_retrain_window.png` | `07_Retrain_Window.ipynb` |
| 18–21 | Monitoring 4 artifact, alert | `06_monitoring.py` | `06_monitoring.png` | `06_Monitoring.ipynb` |

## Kết quả chính từng demo

### 01 — Model hỏng dần
- MAE 6 tháng đầu sau deploy: **~4.9**
- MAE 6 tháng cuối: **~18.8** (tăng **~3.8×**)
- Sau retrain ở tháng 18: MAE còn **~8.4**

**Câu chốt:** deploy là bắt đầu; drift làm sai số tăng, retrain kéo lại.

### 02 — Một outlier phá boundary
- Accuracy test sạch, không outlier: **~0.99**
- Thêm **1 outlier nhãn sai**: accuracy còn **~0.82**
- 99,99% an toàn trên 1 triệu chuyến = **100 chuyến lỗi**

**Câu chốt:** outlier nói về dữ liệu; edge case nói về hiệu năng. Một mẫu cực đoan có thể làm model sai hàng loạt.

### 03 — Feedback loop
- Hai bài A/B chất lượng thật bằng nhau (CTR = 0.10)
- Greedy: A đứng đầu **100%**, CTR naive A **0.099** vs B **0.040** → kết luận sai
- Debiased: A **0.099**, B **0.100** → khôi phục đúng
- ε-greedy 30%: gap giảm còn **~0.042**
- Hit rate theo popularity: ít phổ biến **~0.17**, trung bình **~0.22**, phổ biến **~0.64**

**Câu chốt:** model tự tạo dữ liệu cho vòng sau; randomization và positional features phá vòng lặp.

### 04 — Ba loại shift
| Loại | Accuracy source | Accuracy target |
|---|---|---|
| Covariate shift | 0.91 | **0.10** |
| Label shift | 0.85 | 0.84 (nhưng dự đoán positive 0.24 vs thật 0.11) |
| Concept drift | 1.00 | **0.00** |

**Câu chốt:** covariate shift làm model extrapolate sai; label shift làm lệch tỷ lệ nhãn; concept drift làm quy luật cũ vô dụng.

### 05 — Phát hiện shift
- Cùng phân phối: KS p ≈ 0.44, MMD p ≈ 0.28 → không báo shift
- Khác phân phối: KS p ≈ 0.001, MMD p ≈ 0.003 → báo shift
- Cửa sổ bỏ sót thứ 2: KS p ≈ 0.026 → **báo shift sai**
- Cửa sổ đủ 12 tuần: KS p ≈ 0.156 → **không shift**
- Sliding 4h thấy cú sụt còn **0.67**; cumulative chỉ còn **0.85** → che mất sự cố

**Câu chốt:** phải biết loại nào, đo bằng gì, trong cửa sổ nào.

### 06 — Monitoring
- Sự cố thật bắt đầu giờ **150** (40% feature NaN, fill = 0)
- Alert feature mean: giờ **150**
- Alert prediction rate: giờ **150**
- Alert accuracy: giờ **174** (nhãn trễ 24h)

**Câu chốt:** feature/prediction phát hiện trước accuracy; monitoring phải nhìn cả 4 tầng artifact.

### 07 — Retrain
- Cửa sổ 7 ngày: **0.967**; 30 ngày: **0.970**; 90 ngày: **0.949**; 180 ngày: **0.867**
- Với ít dữ liệu mới (1–7 ngày), stateful (fine-tune) tốt hơn stateless
- Khi có đủ dữ liệu mới (30 ngày), stateless bắt kịp

**Câu chốt:** không có cửa sổ retrain đúng cho mọi bài toán; phải thực nghiệm.

## Gợi ý khi trình bày

1. **Không chạy live nếu không cần.** Mở sẵn hình PNG và terminal đã chạy trước; nếu chạy live, mỗi demo chỉ mất 1–5 giây.
2. **Mỗi demo chỉ nói 1 ý.** Ví dụ demo 3: chỉ nói “A và B bằng nhau, nhưng greedy kết luận A tốt hơn vì vị trí”.
3. **Dùng số liệu trong output**, không đọc code. Code chỉ để chứng minh mô phỏng là thật.
4. **Chuẩn bị backup:** nếu máy chiếu lỗi, vẫn còn hình trong `figures/` và snippet trong `SLIDE_CODE.md`.
5. **Ưu tiên notebook khi cần giải thích từng bước.** Notebook có markdown + hình inline + số liệu kỳ vọng; script chỉ để xuất lại hình hàng loạt.

Kịch bản nói chi tiết cho từng demo: xem `DEMO_SCRIPT.md`.

## Ghi chú kỹ thuật

- Logistic regression dùng gradient descent, có `w0` để minh hoạ **stateful/fine-tuning**.
- KS test dùng **permutation p-value** thay vì công thức asymptotic, để không phụ thuộc SciPy.
- MMD dùng **RBF kernel**, cũng permutation test; phù hợp minh hoạ đa biến.
- Mọi demo đặt `seed` cố định nên kết quả lặp lại được.
- `common.py` tự chọn backend: **Agg** khi chạy script/server, **inline** khi chạy trong Jupyter. Vì vậy cùng một file dùng được cho cả `run_all.py` và notebook.
- Hàm `save(fig, name)` giữ figure mở trong notebook để hiển thị inline; trong script thì đóng figure sau khi lưu.

## Tài liệu liên quan

- Hướng dẫn tạo slide: [../README.md](../README.md)
- Notebook index: [../notebooks/00_Index.ipynb](../notebooks/00_Index.ipynb)
- Dàn ý 22 slide: [../Chương 8 - Dàn ý 22 slide.md](<../Chương 8 - Dàn ý 22 slide.md>)
- Kế hoạch thuyết trình: [../Chương 8 - Kế hoạch thuyết trình.md](<../Chương 8 - Kế hoạch thuyết trình.md>)
- Ghi chú chính: [../Chương 8 - Data Distribution Shifts & Monitoring.md](<../Chương 8 - Data Distribution Shifts & Monitoring.md>)

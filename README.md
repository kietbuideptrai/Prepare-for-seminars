# Chương 8 — Data Distribution Shifts & Monitoring

**Hướng dẫn tạo slide thuyết trình cho cả nhóm.**

> Đọc file này trước khi làm slide. Mục tiêu: **bất kỳ ai trong nhóm cũng có thể tự tạo đúng slide của mình**, đúng nội dung, đúng hình, đúng thời lượng — mà không cần hỏi lại.

---

## 0. TL;DR — 6 bước nhanh

1. **Đọc phần của mình** trong [Chương 8 - Dàn ý 22 slide](<./Chương 8 - Dàn ý 22 slide.md>) và [Chương 8 - Kế hoạch thuyết trình](<./Chương 8 - Kế hoạch thuyết trình.md>).
2. **Mở PowerPoint / Google Slides**, tạo deck **16:9**, dùng template chung ở mục 5.
3. **Copy tiêu đề + 5–8 từ khoá** cho từng slide. Không copy cả đoạn văn.
4. **Chèn visual** từ `code-demo/figures/` hoặc chạy notebook trong `notebooks/` để lấy hình.
5. **Dán “Lời dẫn” vào Speaker Notes**, không đưa lên mặt slide.
6. **Xuất PDF dự phòng** + chạy thử đúng thời lượng trước buổi thuyết trình.

---

## 1. Bản đồ dự án — file nào dùng để làm gì?

```text
30 Projects/ML - Seminar/
├── README.md                                  ← file này: hướng dẫn tạo slide
├── chapter8.pdf                               ← nguồn gốc, chỉ để local (không push GitHub)
│
├── Chương 8 - Data Distribution Shifts & Monitoring.md
│       └── Ghi chú kiến thức đầy đủ — tra cứu khi cần giải thích sâu
├── Chương 8 - Dàn ý 22 slide.md
│       └── Tiêu đề + bullet + visual + lời dẫn cho TỪNG slide
├── Chương 8 - Kế hoạch thuyết trình.md
│       └── Chia task 4 người + thời lượng + checklist + Q&A
├── Chương 8 - Sơ đồ tư duy.excalidraw.md
│       └── Sơ đồ tư duy — dùng cho slide 1 và slide 22
│
├── code-demo/
│   ├── README.md          ← cách chạy code + map demo → slide
│   ├── SLIDE_CODE.md      ← snippet 5–15 dòng để dán lên slide
│   ├── DEMO_SCRIPT.md     ← nói gì khi chiếu từng demo
│   ├── 01_*.py … 07_*.py  ← script chạy hàng loạt
│   ├── figures/           ← 7 hình PNG đã xuất sẵn
│   └── common.py          ← helper dùng chung
│
└── notebooks/
    ├── README.md                  ← hướng dẫn chạy notebook
    ├── 00_Index.ipynb             ← bắt đầu từ đây
    ├── 01_Model_Decay.ipynb       ← slide 2, 5
    ├── 02_Edge_Case_Outlier.ipynb ← slide 6
    ├── 03_Feedback_Loop.ipynb     ← slide 7, 8
    ├── 04_Shift_Types.ipynb       ← slide 9–13
    ├── 05_Detect_Shift.ipynb      ← slide 14, 15
    ├── 06_Monitoring.ipynb        ← slide 18–21
    └── 07_Retrain_Window.ipynb    ← slide 16, 17
```

**Quy tắc vàng:** nội dung lấy từ **Dàn ý**, số liệu lấy từ **notebook**, hình lấy từ **figures**, câu nói lấy từ **DEMO_SCRIPT**.

---

## 2. Phân công & thời lượng

| Thành viên | Phần | Slide | Thời lượng | Vai trò phụ |
|---|---|---|---|---|
| **Người 1** | Mở đầu, failure taxonomy, software failures, train-serving skew | 1–5 | ~6 phút | MC, giữ nhịp |
| **Người 2** | Edge cases + degenerate feedback loops | 6–8 | ~7 phút | Ví dụ/demo, hình ảnh |
| **Người 3** | Data distribution shifts + cách phát hiện | 9–15 | ~9 phút | Fact-check công thức, số liệu |
| **Người 4** | Ứng phó shift + monitoring/observability + tổng kết + Q&A | 16–22 | ~8 phút | Slide master, nộp bài |

**Tổng: 30 phút thuyết trình + 5 phút Q&A.**

> Chi tiết từng phần, câu chuyển ý và checklist cá nhân: xem [Chương 8 - Kế hoạch thuyết trình](<./Chương 8 - Kế hoạch thuyết trình.md>).

---

## 3. Bảng map 22 slide — làm gì, lấy gì ở đâu

| # | Nội dung | Người | Visual / hình | Nguồn hình | Notebook | Snippet |
|---|---|---|---|---|---|---|
| 1 | Title + agenda + hook | 1 | Sơ đồ tư duy | `Chương 8 - Sơ đồ tư duy.excalidraw.md` | — | — |
| 2 | Model tốt chết sau một năm | 1 | Timeline + MAE tăng | `01_model_decay.png` | `01_Model_Decay` | Slide 2 |
| 3 | Failure là gì? | 1 | 2 cột Operational vs ML | tự vẽ | — | Slide 3 |
| 4 | Không phải lỗi nào cũng là lỗi ML | 1 | Donut 60/96 | tự vẽ | — | Slide 4 |
| 5 | Train-serving skew | 1 | 2 phân phối lệch | `01_model_decay.png`, `04_shift_types.png` | `01`, `04` | Slide 5 |
| 6 | Edge case vs outlier | 2 | Boundary trước/sau | `02_edge_case_outlier.png` | `02_Edge_Case_Outlier` | Slide 6 |
| 7 | Degenerate feedback loop | 2 | Vòng lặp + ranking A/B | `03_feedback_loop.png` | `03_Feedback_Loop` | Slide 7 |
| 8 | Phát hiện & phá vòng lặp | 2 | Popularity bucket | `03_feedback_loop.png` | `03_Feedback_Loop` | Slide 8 |
| 9 | Data distribution shift là gì? | 3 | Công thức phân rã | `04_shift_types.png` | `04_Shift_Types` | Slide 9 |
| 10 | Covariate shift | 3 | 2 histogram + accuracy sụt | `04_shift_types.png` | `04_Shift_Types` | Slide 10 |
| 11 | Label shift | 3 | Prior trước/sau | `04_shift_types.png` | `04_Shift_Types` | Slide 11 |
| 12 | Concept drift | 3 | Quy luật bị đảo | `04_shift_types.png` | `04_Shift_Types` | Slide 12 |
| 13 | Feature change & label schema change | 3 | Bảng 5 loại shift | `04_shift_types.png` | `04_Shift_Types` | Slide 13 |
| 14 | Accuracy không đủ; summary stats | 3 | Bảng thống kê | `05_detect_shift.png` | `05_Detect_Shift` | Slide 14 |
| 15 | Two-sample test & time window | 3 | KS/MMD + sliding vs cumulative | `05_detect_shift.png` | `05_Detect_Shift` | Slide 15 |
| 16 | Ứng phó: 3 hướng + retrain | 4 | Bảng 3 hướng + cửa sổ retrain | `07_retrain_window.png` | `07_Retrain_Window` | Slide 16 |
| 17 | Thiết kế để ít phải retrain | 4 | Stateless vs stateful | `07_retrain_window.png` | `07_Retrain_Window` | Slide 17 |
| 18 | Monitoring vs Observability | 4 | SLO/uptime | `06_monitoring.png` | `06_Monitoring` | Slide 18 |
| 19 | 4 artifact cần monitor | 4 | Pipeline 4 tầng | `06_monitoring.png` | `06_Monitoring` | Slide 19 |
| 20 | Logs, dashboards, alerts | 4 | Alert template | `06_monitoring.png` | `06_Monitoring` | Slide 20 |
| 21 | Observability: tag & slice | 4 | Query mẫu | `06_monitoring.png` | `06_Monitoring` | Slide 21 |
| 22 | Tổng kết 3 điều mang đi | 4 | Sơ đồ tư duy | `Chương 8 - Sơ đồ tư duy.excalidraw.md` | — | — |

**Đường dẫn hình:** `code-demo/figures/<tên>.png`
**Snippet:** `code-demo/SLIDE_CODE.md`
**Lời dẫn từng slide:** `Chương 8 - Dàn ý 22 slide.md`

---

## 4. Lấy visual — 3 cách

### Cách 1 — Dùng hình đã xuất sẵn (nhanh nhất, khuyên dùng)

Mở thư mục `code-demo/figures/`:

| File | Dùng cho slide |
|---|---|
| `01_model_decay.png` | 2, 5 |
| `02_edge_case_outlier.png` | 6 |
| `03_feedback_loop.png` | 7, 8 |
| `04_shift_types.png` | 5, 9–13 |
| `05_detect_shift.png` | 14, 15 |
| `06_monitoring.png` | 18–21 |
| `07_retrain_window.png` | 16, 17 |

Kéo thẳng file PNG vào PowerPoint/Google Slides.

### Cách 2 — Chạy notebook để lấy hình mới

```bash
cd "30 Projects/ML - Seminar"
pip install -r code-demo/requirements.txt
pip install jupyterlab
jupyter lab
```

Mở `notebooks/00_Index.ipynb`, chọn notebook cần dùng, **Run All**. Hình sẽ hiện inline và tự lưu vào `code-demo/figures/`.

> Notebook có sẵn markdown giải thích + số liệu kỳ vọng + “Ý nghĩa cho slide”. Đây là nơi tốt nhất để hiểu hình trước khi lên slide.

### Cách 3 — Chạy script hàng loạt

```bash
cd "30 Projects/ML - Seminar/code-demo"
python3 run_all.py
```

Cách này chỉ in số liệu và xuất lại 7 hình PNG, không mở notebook.

### Cách 4 — Sơ đồ tư duy (slide 1 và 22)

1. Mở `Chương 8 - Sơ đồ tư duy.excalidraw.md` trong Obsidian (cần plugin **Excalidraw**).
2. Chọn **More options → Export to PNG** (hoặc dùng command palette: `Excalidraw: Export image`).
3. Lưu thành `code-demo/figures/00_mindmap.png` để dùng lại.
4. Nếu không có plugin: dùng ảnh chụp màn hình hoặc nhờ Người 4 export sẵn.

### Nếu hình không khớp số trên slide

1. Restart kernel / chạy lại `python3 run_all.py`.
2. Không đổi `seed` trong code.
3. Đối chiếu bảng “số liệu kỳ vọng” ở cuối mỗi notebook.
4. Nếu vẫn lệch: dùng số trong notebook, **không tự bịa số**.

---

## 5. Template & thiết kế slide

### 5.1. Khổ slide

- **16:9 widescreen** (1920×1080 hoặc 13.333×7.5 inch).
- PowerPoint: `Design → Slide Size → Widescreen (16:9)`.
- Google Slides: `File → Page setup → Widescreen (16:9)`.

### 5.2. Master slide — làm một lần, dùng cho cả deck

Tạo trong `View → Slide Master` (PowerPoint) hoặc `Slide → Edit theme` (Google Slides):

| Thành phần | Quy ước |
|---|---|
| **Font tiêu đề** | Sans-serif, đậm, **32–40 pt** |
| **Font nội dung** | Sans-serif, **24–28 pt** |
| **Font code** | Monospace (Consolas / Courier New), **14–18 pt** |
| **Màu chính** | Xanh đậm `#1F4E79` |
| **Màu nhấn** | Đỏ `#D62728` cho cảnh báo, xanh lá `#2CA02C` cho “đúng” |
| **Nền** | Trắng hoặc xám rất nhạt `#F7F7F7` |
| **Footer** | `Designing Machine Learning Systems — Chương 8` |
| **Số trang** | Góc phải dưới |
| **Logo/trường** | Góc trái dưới (nếu có) |

### 5.3. Quy tắc nội dung

- **Mỗi slide = 1 thông điệp.** Nếu có 2 ý lớn, tách thành 2 slide.
- **Tối đa 6 dòng bullet**, mỗi dòng **5–8 từ khoá**. Không viết câu hoàn chỉnh.
- **Không đọc slide.** Slide giữ từ khoá; lời giải thích nằm ở Speaker Notes.
- **Một hình lớn tốt hơn 4 hình nhỏ.** Hình phải đọc được từ cuối phòng.
- **Màu có ý nghĩa:** đỏ = lỗi/rủi ro, xanh lá = đúng/đã sửa, xám = baseline.
- **Không dùng hiệu ứng chuyển slide cầu kỳ.** Chỉ dùng fade hoặc không hiệu ứng.

### 5.4. Bố cục gợi ý

```text
┌─────────────────────────────────────────────┐
│  Tiêu đề slide (32–40 pt, đậm)              │
│                                             │
│  • 3–6 bullet từ khoá (24–28 pt)            │
│  • Mỗi bullet ≤ 8 từ                        │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │                                       │  │
│  │        HÌNH LỚN (chiếm 50–60%)        │  │
│  │                                       │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  Footer                              Slide #│
└─────────────────────────────────────────────┘
```

---

## 6. Quy trình chi tiết — 8 bước

### Bước 1 — Chuẩn bị nội dung (15 phút/người)

1. Mở [Chương 8 - Dàn ý 22 slide](<./Chương 8 - Dàn ý 22 slide.md>).
2. Tìm các slide thuộc phần mình.
3. Với mỗi slide, ghi ra giấy 3 thứ:
   - **1 câu thông điệp** (không phải tiêu đề).
   - **3–6 từ khoá** sẽ hiện trên slide.
   - **1 visual** sẽ dùng.
4. Đọc phần “Lời dẫn” — đây là nội dung Speaker Notes, không phải nội dung slide.

### Bước 2 — Tạo deck & master (Người 4 làm trước)

1. Tạo file mới, đặt tên theo quy ước ở mục 8.
2. Thiết lập 16:9.
3. Tạo master slide theo mục 5.2.
4. Tạo sẵn các layout:
   - **Title** — slide 1.
   - **Section** — chuyển người (nếu muốn).
   - **Content + figure** — phần lớn slide.
   - **Full figure** — slide có hình lớn.
   - **Quote** — câu chốt.
   - **Backup** — công thức, bảng chi tiết.

### Bước 3 — Điền từng slide

Với mỗi slide:

1. **Tiêu đề:** copy từ Dàn ý (có thể rút gọn).
2. **Bullet:** copy ý chính, rồi **cắt còn 5–8 từ**. Ví dụ:
   - Dàn ý: “Model train 12 tháng đầu, MAE khoảng 4,9. Một năm sau, cùng model đó, MAE lên 18,8.”
   - Trên slide: `MAE 4,9 → 18,8 sau 1 năm` · `Model không đổi — thế giới đổi`.
3. **Visual:** chèn hình theo bảng map ở mục 3.
4. **Caption:** thêm 1 dòng nhỏ dưới hình nếu cần — ví dụ `Nguồn: mô phỏng, seed=42`.
5. **Speaker Notes:** dán nguyên “Lời dẫn” từ Dàn ý. Có thể thêm số liệu kỳ vọng từ notebook.
6. **Số trang + footer:** kiểm tra tự động qua master.

### Bước 4 — Chèn code snippet (nếu slide cần)

Chỉ dùng khi thật sự giúp chứng minh ý. Lấy từ `code-demo/SLIDE_CODE.md`.

**Trên PowerPoint:**

1. `Insert → Text Box`.
2. Dán snippet.
3. Font `Consolas` 14–18 pt.
4. Nền text box màu tối `#1E1E1E`, chữ trắng `#D4D4D4`.
5. Chỉ giữ **5–15 dòng**. Cắt phần không cần.
6. Không chèn cả file `.py`.

**Trên Google Slides:**

1. `Insert → Text box`.
2. Dán snippet.
3. Font `Roboto Mono` hoặc `Courier New`.
4. Dùng shape nền tối nếu muốn.

> **Nguyên tắc:** slide chỉ giữ đúng 1 ý. Code để chứng minh, không để dạy lập trình.

### Bước 5 — Viết Speaker Notes

- Mỗi slide **30–60 giây nói**.
- Ghi 3 phần:
  1. **Mở:** 1 câu dẫn.
  2. **Ý chính:** 1–2 câu giải thích.
  3. **Chốt/chuyển ý:** 1 câu.
- Không viết nguyên văn dài; chỉ ghi ý để tự nhiên.
- Với slide có demo: thêm `Chiếu: figures/...` và `Nói: ...` từ `DEMO_SCRIPT.md`.

### Bước 6 — Review chéo

Trước khi gộp deck:

- [ ] Đúng số slide được giao.
- [ ] Mỗi slide có tiêu đề + ≤ 6 bullet.
- [ ] Hình đúng file, không mờ, không méo.
- [ ] Số liệu khớp notebook/README.
- [ ] Có Speaker Notes.
- [ ] Có câu chuyển ý sang người tiếp theo.
- [ ] Không có lỗi chính tả tiếng Việt.
- [ ] Thống nhất footer + font + màu.

### Bước 7 — Gộp deck & kiểm tra tổng thể

1. Người 4 gộp tất cả slide theo đúng thứ tự 1–22.
2. Kiểm tra **chuyển ý** giữa 4 phần.
3. Kiểm tra **tổng thời lượng** bằng đồng hồ.
4. Thêm slide backup (không tính vào 22 slide chính).
5. Xuất PDF.

### Bước 8 — Xuất PDF & backup

**PowerPoint:**

```text
File → Export → Create PDF/XPS → chọn thư mục → Publish
```

**Google Slides:**

```text
File → Download → PDF Document (.pdf)
```

**Quy ước tên file xuất:**

```text
Chuong8_DataDistributionShifts_Monitoring_v1_20261110.pdf
```

Lưu **cùng thư mục** với file `.pptx`. Mang theo **USB + bản cloud** để dự phòng.

---

## 7. Dùng demo & notebook khi thuyết trình

### Phương án A — Chiếu hình PNG (khuyên dùng)

- Mở sẵn `code-demo/figures/`.
- Chèn hình vào slide từ trước.
- Không cần chạy code live.
- **An toàn nhất** khi máy chiếu không có Python.

### Phương án B — Chiếu notebook live

1. Trước buổi thuyết trình **30 phút**:
   ```bash
   cd "30 Projects/ML - Seminar"
   jupyter lab
   ```
2. Mở notebook tương ứng.
3. **Run All trước** để chắc chắn không lỗi.
4. Khi trình bày: chỉ cuộn đến cell cần chiếu, **không gõ code live**.
5. Nếu kernel chết: chuyển ngay sang hình PNG.

### Phương án C — Chiếu script trong terminal

```bash
cd "30 Projects/ML - Seminar/code-demo"
python3 03_feedback_loop.py
```

Mỗi demo chạy **1–5 giây**. Chỉ dùng khi khán giả muốn thấy code thật.

### Kịch bản nói cho từng demo

Xem `code-demo/DEMO_SCRIPT.md`. Mỗi demo có:

- Lệnh chạy.
- Hình cần chiếu.
- Câu nói 30–60 giây.
- Câu chốt.

### Phương án dự phòng

| Tình huống | Xử lý |
|---|---|
| Máy chiếu không chạy terminal | Chỉ chiếu PNG trong `figures/` |
| Hết thời gian | Bỏ demo 1 và 7; giữ demo 3 và 6 |
| Bị hỏi “code đâu?” | Mở `code-demo/`, chỉ file tương ứng slide |
| Không có Python trên máy trình chiếu | Dùng PNG + snippet trong `SLIDE_CODE.md` |
| Notebook lỗi kernel | Restart kernel → Run All; nếu vẫn lỗi, dùng PNG |

---

## 8. Quy ước đặt tên file

### File ghi chú (đã thống nhất)

| Loại | Tên |
|---|---|
| Ghi chú chính | `Chương 8 - Data Distribution Shifts & Monitoring.md` |
| Dàn ý slide | `Chương 8 - Dàn ý 22 slide.md` |
| Kế hoạch | `Chương 8 - Kế hoạch thuyết trình.md` |
| Sơ đồ tư duy | `Chương 8 - Sơ đồ tư duy.excalidraw.md` |

> Không đổi tên các file này nếu chưa cập nhật toàn bộ wiki link trong vault.

### File slide

```text
Chuong8_DataDistributionShifts_Monitoring_v1.pptx
Chuong8_DataDistributionShifts_Monitoring_v1_20261110.pdf
```

- `v1`, `v2`… tăng khi có thay đổi lớn.
- Ngày xuất theo `YYYYMMDD`.
- Không dùng dấu cách, tiếng Việt có dấu trong tên file slide.

### Hình & notebook

- **Không đổi tên** file trong `code-demo/figures/` và `notebooks/`.
- Số đầu file (`01_`, `02_`…) map với thứ tự demo và slide.
- Nếu cần thêm hình mới, đặt `08_ten_mo_ta.png` và ghi vào bảng map.

---

## 9. Luyện tập & giữ thời lượng

### Lịch luyện gợi ý

| Buổi | Nội dung | Mục tiêu |
|---|---|---|
| **Lần 1** | Từng người nói phần mình | Đúng nội dung, không đọc slide |
| **Lần 2** | Ghép 4 phần | Đúng chuyển ý, tổng ≤ 32 phút |
| **Lần 3** | Tổng duyệt có bấm giờ | 30 phút + 5 phút Q&A |
| **Lần 4** | Chạy trên máy chiếu thật | Không lỗi font, hình, PDF |

### Cách cắt thời gian khi lố

Cắt theo thứ tự:

1. Chi tiết software failures (slide 4).
2. Chi tiết logs (slide 20).
3. Importance weighting (slide 10).
4. MMD/LSDD (slide 15) → đưa vào backup slide.

### Câu chuyển ý bắt buộc

| Sau slide | Người | Câu chuyển |
|---|---|---|
| 5 | 1 → 2 | “Ngoài dữ liệu lệch, còn hai cái bẫy rất ‘ML’: mẫu cực đoan và vòng lặp do chính model tạo ra.” |
| 8 | 2 → 3 | “Feedback loop là shift do chính hệ thống gây ra. Còn khi thế giới bên ngoài thay đổi, ta gọi đó là gì và đo bằng cách nào?” |
| 15 | 3 → 4 | “Đã biết phát hiện. Vậy khi phát hiện rồi, ta ứng phó thế nào?” |

---

## 10. Q&A — chuẩn bị trước

- Ngân hàng câu hỏi + câu trả lời mẫu: xem mục Q&A trong [Chương 8 - Kế hoạch thuyết trình](<./Chương 8 - Kế hoạch thuyết trình.md>).
- Mỗi người chuẩn bị **3 câu hỏi** cho phần mình.
- Câu hỏi khó nên có **1 slide backup** với số liệu/công thức.
- Người 4 điều phối Q&A: ghi câu hỏi, chỉ định người trả lời, giữ thời gian.

**Câu hỏi thường gặp:**

| Câu hỏi | Người trả lời | Ý trả lời |
|---|---|---|
| Data drift khác concept drift thế nào? | Người 3 | Drift = $P(X)$ đổi; concept = $P(Y \mid X)$ đổi. |
| Vì sao accuracy không đủ? | Người 3 | Cần nhãn, thường trễ; không thấy shift sớm. |
| Retrain bao lâu một lần? | Người 4 | Không có công thức chung; thực nghiệm theo cửa sổ. |
| Làm sao phát hiện feedback loop? | Người 2 | Popularity diversity, hit rate theo bucket, dự đoán đồng nhất. |
| Monitoring khác observability thế nào? | Người 4 | Monitoring trả lời “khi nào”; observability trả lời “tại sao”. |

---

## 11. Checklist nộp bài

### Trước khi nộp

- [ ] Deck đúng **22 slide** (+ backup).
- [ ] Đúng thứ tự và đúng người phụ trách.
- [ ] Mỗi slide có tiêu đề, bullet ngắn, hình rõ.
- [ ] Có Speaker Notes cho tất cả slide.
- [ ] Có câu chuyển ý giữa 4 phần.
- [ ] Số liệu khớp notebook/README.
- [ ] Footer + số trang thống nhất.
- [ ] Đã xuất **PDF**.
- [ ] Đã test trên máy chiếu thật.
- [ ] Có bản backup trên USB/cloud.

### Cấu trúc thư mục nộp gợi ý

```text
NopBai_Chuong8/
├── Chuong8_DataDistributionShifts_Monitoring_v1.pptx
├── Chuong8_DataDistributionShifts_Monitoring_v1_20261110.pdf
└── figures/
    ├── 01_model_decay.png
    ├── 02_edge_case_outlier.png
    ├── 03_feedback_loop.png
    ├── 04_shift_types.png
    ├── 05_detect_shift.png
    ├── 06_monitoring.png
    └── 07_retrain_window.png
```

---

## 12. Xử lý sự cố thường gặp

| Vấn đề | Nguyên nhân | Cách sửa |
|---|---|---|
| Hình bị mờ | Chèn ảnh nhỏ rồi phóng to | Chèn lại PNG gốc, kéo góc để scale đều |
| Font tiếng Việt bị lỗi | Máy chiếu thiếu font | Dùng font phổ biến (Arial, Calibri, Roboto); xuất PDF |
| Slide bị tràn chữ | Copy quá nhiều | Cắt còn 5–8 từ khoá; tăng font |
| Số liệu không khớp | Đổi seed / chạy sai notebook | Restart kernel → Run All; đối chiếu notebook |
| Notebook không import được `common` | Chạy ngoài thư mục dự án | Mở từ `notebooks/` hoặc chạy lại cell “Thiết lập” |
| `ModuleNotFoundError: numpy` | Chưa cài requirements | `pip install -r code-demo/requirements.txt` |
| Không mở được `.excalidraw` | Thiếu plugin Excalidraw | Cài plugin trong Obsidian, hoặc dùng ảnh export PNG |
| PDF bị lệch layout | Font thay thế khi export | Dùng font chuẩn; kiểm tra PDF trước khi nộp |

---

## 13. Liên kết nhanh

### Tài liệu chính

- [Chương 8 - Data Distribution Shifts & Monitoring](<./Chương 8 - Data Distribution Shifts & Monitoring.md>) — ghi chú đầy đủ
- [Chương 8 - Dàn ý 22 slide](<./Chương 8 - Dàn ý 22 slide.md>) — nội dung từng slide
- [Chương 8 - Kế hoạch thuyết trình](<./Chương 8 - Kế hoạch thuyết trình.md>) — chia task + Q&A
- [Chương 8 - Sơ đồ tư duy](<./Chương 8 - Sơ đồ tư duy.excalidraw.md>) — mind map

### Code & demo

- [Code demo — README](<./code-demo/README.md>) — cách chạy, map demo → slide, số liệu kỳ vọng
- [Snippet code cho slide](<./code-demo/SLIDE_CODE.md>) — đoạn code ngắn để dán
- [Kịch bản demo](<./code-demo/DEMO_SCRIPT.md>) — nói gì khi chiếu
- [Notebook index](<./notebooks/00_Index.ipynb>) — bắt đầu từ đây

### Nguồn

- `chapter8.pdf` — Chapter 8, *Designing Machine Learning Systems* (Chip Huyen, O'Reilly), tr. 225–262. **File này chỉ lưu local**, không đưa lên GitHub (bản quyền + kích thước). Ai cần thì xin bản PDF qua nhóm.

---

## 14. Một câu cuối

> **Deploy là bắt đầu, không phải kết thúc.**
> Slide tốt không phải slide có nhiều chữ, mà là slide khiến khán giả nhớ đúng **một ý** và tin rằng ý đó là thật.

Nếu còn thắc mắc: hỏi người phụ trách phần đó, hoặc mở notebook tương ứng để xem số liệu gốc.

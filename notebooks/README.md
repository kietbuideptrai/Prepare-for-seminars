# Notebooks — Chương 8 demos

Bản Jupyter Notebook của 7 demo trong `../code-demo/`. Mỗi notebook có:

- Markdown map slide + ý chính.
- Code cell chạy được, seed cố định.
- Hình hiển thị inline và tự lưu vào `../code-demo/figures/`.
- Bảng số liệu kỳ vọng + “Ý nghĩa cho slide” ở cuối.

## Chạy

```bash
cd "30 Projects/ML - Seminar"
pip install -r code-demo/requirements.txt
pip install jupyterlab
jupyter lab
```

Mở `00_Index.ipynb` → chọn notebook → **Run All**.

Hoặc mở bằng VS Code: cài extension **Jupyter**, chọn kernel Python 3, bấm **Run All**.

## Danh sách

| Notebook | Slide | Nội dung |
|---|---|---|
| `00_Index.ipynb` | — | Hướng dẫn chạy + map slide |
| `01_Model_Decay.ipynb` | 2, 5 | Model hỏng dần sau deploy |
| `02_Edge_Case_Outlier.ipynb` | 6 | Outlier phá decision boundary |
| `03_Feedback_Loop.ipynb` | 7, 8 | Popularity bias, randomization |
| `04_Shift_Types.ipynb` | 9–13 | Covariate / label / concept shift |
| `05_Detect_Shift.ipynb` | 14, 15 | KS, MMD, cửa sổ thời gian |
| `06_Monitoring.ipynb` | 18–21 | 4 tầng artifact, alert trễ |
| `07_Retrain_Window.ipynb` | 16, 17 | Cửa sổ retrain, stateless/stateful |

## Lưu ý

- Không đổi `seed` nếu muốn số liệu khớp `../code-demo/README.md` và `../code-demo/DEMO_SCRIPT.md`.
- Nếu notebook không import được `common`, chạy lại cell **“Thiết lập”** hoặc mở notebook từ đúng thư mục `notebooks/`.
- Hình đã có sẵn trong `../code-demo/figures/`; không cần chạy notebook nếu chỉ cần chèn hình vào slide.

## Liên kết

- Hướng dẫn tạo slide: [../README.md](../README.md)
- Code + hình + snippet: [../code-demo/README.md](../code-demo/README.md)
- Dàn ý 22 slide: [../Chương 8 - Dàn ý 22 slide.md](<../Chương 8 - Dàn ý 22 slide.md>)

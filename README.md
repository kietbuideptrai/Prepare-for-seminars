# Prepare for seminars

Tài liệu chuẩn bị seminar cho **Chương 8 — Data Distribution Shifts & Monitoring**, trích từ *Designing Machine Learning Systems* của Chip Huyen (O'Reilly), tr. 225–262.

## Nội dung

| File | Mô tả |
|---|---|
| `Chương 8 - Data Distribution Shifts và Monitoring.md` | Ghi chú kiến thức đầy đủ của chương: failure taxonomy, train-serving skew, edge cases, feedback loops, các loại data shift, cách phát hiện và ứng phó, monitoring & observability. |
| `Kế hoạch thuyết trình Chương 8 - Chia task 4 người.md` | Kế hoạch thuyết trình 30 phút + 5 phút Q&A: chia task cho 4 người, kịch bản 22 slide, timeline 3 buổi, ngân hàng câu hỏi Q&A, tiêu chí chấm. |
| `Dàn ý slide thuyết trình Chương 8 - 22 slide.md` | Dàn ý từng slide: tiêu đề, bullet, visual gợi ý và lời dẫn để tập nói. |
| `Ch8 - Data Distribution Shifts.excalidraw.md` | Sơ đồ tư duy chương 8 (Obsidian Excalidraw): nguyên nhân hỏng → các loại shift → phát hiện → ứng phó → giám sát. |

## Cách dùng

1. Đọc file ghi chú chương để nắm nội dung.
2. Mở file kế hoạch để biết phần mình phụ trách, thời lượng và câu chuyển ý.
3. Dùng file dàn ý để dựng slide (PowerPoint / Google Slides). Mỗi slide giữ 5–8 từ khoá, phần giải thích để ở lời dẫn.
4. Slide cuối dùng lại sơ đồ tư duy để tổng kết.

## Cấu trúc thuyết trình

| Người | Phần | Slide | Thời lượng |
|---|---|---|---|
| Người 1 | Mở đầu, failure taxonomy, software failures, train-serving skew | 1–5 | ~6 phút |
| Người 2 | Edge cases + degenerate feedback loops | 6–8 | ~7 phút |
| Người 3 | Data distribution shifts + cách phát hiện | 9–15 | ~9 phút |
| Người 4 | Ứng phó shift + monitoring/observability + tổng kết + Q&A | 16–22 | ~8 phút |

> **Thông điệp xuyên suốt:** Deploy là bắt đầu, không phải kết thúc. Monitor để biết, observability để hiểu, retrain để thích nghi.

## Ghi chú

- Các file dùng cú pháp **Obsidian Flavored Markdown** (wiki-link, callout, công thức LaTeX). Đọc trực tiếp trên GitHub sẽ mất một phần định dạng; mở bằng Obsidian để xem đầy đủ.
- Nội dung là bản **ghi chú diễn giải và hệ thống hoá**, không phải bản dịch nguyên văn từ sách.

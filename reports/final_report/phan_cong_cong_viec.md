# Bảng phân công công việc — Nhóm 12 — Đề tài 16

Bảng dưới đây là phần dùng cho báo cáo: nêu phần việc chính, phần việc hỗ trợ và tỷ lệ đóng góp của từng
thành viên. Tỷ lệ đóng góp cộng lại bằng 100%.

| Thành viên | Công việc chính | Công việc hỗ trợ | Tỷ lệ đóng góp (%) |
|:--|:--|:--|:--:|
| Hà Mạnh Trường (2045240326, nhóm trưởng) | Thu thập và tiền xử lý dữ liệu 5 năm; dựng bảng dữ liệu trung gian; kiểm soát khả năng chạy lại của mã nguồn; điều phối tiến độ và ghép báo cáo; viết mục 1-4 | Rà soát phần thuật toán gom cụm; đối chiếu số liệu giữa các năm; hỗ trợ nạp dữ liệu cho demo | 34 |
| Huỳnh Tâm Trí (2045240315) | Tự cài đặt thuật toán gom cụm (K-Means, phân cấp Ward, DBSCAN), giảm chiều PCA và các độ đo đánh giá; chạy thực nghiệm 5 cấu hình × 5 năm; khảo sát tham số; viết mục 5-7 | Rà soát bộ nạp dữ liệu; kiểm chứng các độ đo bằng thư viện; rà soát phần nối dữ liệu của demo | 33 |
| Ngô Quang Trung (2045240325) | Phân tích khám phá dữ liệu; diễn giải kết quả gom cụm; ghép cụm giữa các năm và lập bảng dịch chuyển cụm; xây dựng demo Streamlit; làm slide; viết mục 8-11 | Rà soát notebook 01; kiểm tra chất lượng dữ liệu theo năm; kiểm tra bản đồ; điều hành buổi tổng duyệt | 33 |

---

## Phần nội bộ của nhóm (không đưa vào báo cáo)

### Phân chia theo giai đoạn phân tích

| Giai đoạn | Nội dung | Chính | Hỗ trợ | Nơi thể hiện |
|:--|:--|:--|:--|:--|
| 1 | Xác định bài toán và câu hỏi khai thác | Trường | cả nhóm | `notebooks/01` mục 1, `README.md` |
| 2 | Tìm hiểu dữ liệu (5 năm, schema lệch) | Trường | Trung | `notebooks/01` mục 2, `src/data/data_loader.py` |
| 3 | Đánh giá chất lượng dữ liệu theo từng năm | Trung | Trường | `notebooks/01` mục 3 |
| 4 | Tiền xử lý, chuẩn hóa tên cột và tên quốc gia, dựng bảng trung gian | Trường | Trí | `notebooks/01`, `data/interim/` |
| 5 | Phân tích khám phá dữ liệu | Trung | Trí | `notebooks/02`, `reports/figures/` |
| 6 | Biến đổi dữ liệu cho thuật toán (Z-score, Min-Max, không chuẩn hóa) | Trí | Trường | `src/features/feature_engineering.py`, `notebooks/03` |
| 7 | Chạy thuật toán và chọn tham số (số cụm tối ưu mỗi năm, cấu hình ba cụm đối chứng, quét DBSCAN) | Trí | Trung | `notebooks/03`, `reports/tables/k_sensitivity_by_year.csv` |
| 8 | So sánh các cấu hình gom cụm và đo độ ổn định | Trí | Trường | `notebooks/03`, `reports/tables/model_comparison_metrics_by_year.csv` |
| 9 | Diễn giải kết quả: chân dung cụm, ghép cụm liên năm, bảng dịch chuyển cụm, hậu kiểm điểm hạnh phúc | Trung | Trí | `notebooks/04`, `data/processed/country_cluster_shift.csv` |
| 10 | Sản phẩm demo (chọn năm, thuật toán, cách chuẩn hóa, số cụm) | Trung | Trường | `app/app.py` |
| 11 | Kết luận và hướng phát triển | Trung | cả nhóm | `notebooks/04` mục 3, mục 9 của báo cáo |

### Yêu cầu chung của nhóm

- Mỗi thành viên nắm toàn bộ quy trình phân tích, không chỉ phần việc cá nhân: sau mỗi phần việc hoàn thành, người thực hiện trình bày lại 20 phút cho hai thành viên còn lại và ghi biên bản vào `ke_hoach_nhom.md`.
- Trước buổi báo cáo, cả nhóm tổng duyệt và đổi vai: Trường trình bày phần phương pháp, Trí trình bày phần demo, Trung trình bày phần tiền xử lý dữ liệu.
- Mỗi thành viên phải chạy được cả bốn notebook, giải thích được công thức Silhouette, chân dung một cụm của một năm bất kỳ và một đoạn mã bất kỳ trong `src/models/clustering.py`.
- Phân chia khi báo cáo tại lớp: Trường trình bày bài toán, dữ liệu và tiền xử lý; Trí trình bày phương pháp, tham số và kết quả; Trung trình bày phần diễn giải, demo và kết luận.

### Checklist ký xác nhận nội dung báo cáo

Mọi con số trong báo cáo phải truy được về `reports/tables/*.csv` hoặc `reports/figures/*`. Trước khi nộp,
mỗi thành viên đọc lại phần mình phụ trách và ký xác nhận.

| Mục báo cáo | Người biên tập | Đã đọc | Đã đối chiếu số với CSV | Giải thích được | Ngày ký |
|:--|:--|:--:|:--:|:--:|:--|
| 1-4 (bài toán, dữ liệu, tiền xử lý) | Trường | ☐ | ☐ | ☐ | |
| 5-7 (phương pháp, tham số, kết quả so sánh) | Trí | ☐ | ☐ | ☐ | |
| 8-11 (diễn giải, demo, kết luận, hạn chế) | Trung | ☐ | ☐ | ☐ | |
| Slide thuyết trình | cả nhóm | ☐ | ☐ | ☐ | |

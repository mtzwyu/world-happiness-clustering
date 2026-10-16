# Bộ slide thuyết trình — Đề tài 16 — Nhóm 12

**Học phần:** Khai thác dữ liệu (Data Mining)
**Đề tài 16:** Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report 2015–2019)

> Mọi số liệu trong bộ slide này truy vết về `reports/tables/*.csv`, `data/processed/*.csv` và `data/interim/happiness_merged.csv`.

---

## Slide 1: Trang bìa

- Học phần: Khai thác dữ liệu — Lớp: sinh viên năm 3, ngành Khoa học dữ liệu
- Đề tài 16: Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report 2015–2019)
- Nhóm 12:
  - Hà Mạnh Trường — MSSV 2045240326 — nhóm trưởng
  - Huỳnh Tâm Trí — MSSV 2045240315
  - Ngô Quang Trung — MSSV 2045240325
- Giảng viên hướng dẫn: Giảng viên học phần Khai thác dữ liệu
- Sản phẩm nộp: mã nguồn, 4 notebook, demo Streamlit, báo cáo Word, video báo cáo không quá 12 phút
- Dữ liệu: 5 năm khảo sát Gallup World Poll (2015–2019), 781 bản ghi quốc gia–năm sau tiền xử lý

---

## Slide 2: Lý do chọn đề tài và ý nghĩa của Báo cáo Hạnh phúc Thế giới

- World Happiness Report (WHR) công bố từ năm 2012 dưới sự chủ trì của Mạng lưới Giải pháp Phát triển Bền vững Liên Hợp Quốc
- Điểm hạnh phúc lấy từ khảo sát Gallup World Poll, đo bằng thang Cantril Ladder từ 0 đến 10
- Điểm tổng hợp là một số duy nhất nên khó thấy quốc gia mạnh yếu ở trụ cột nào
- Bài toán phù hợp với gom cụm không giám sát: không có nhãn mục tiêu, cần phát hiện nhóm tự nhiên
- Ý nghĩa thực tiễn: nhận diện nhóm quốc gia cần ưu tiên hỗ trợ về kinh tế, y tế và thể chế
- Ý nghĩa học thuật: thực hiện trọn vẹn quy trình khai phá dữ liệu 11 bước trên dữ liệu thực tế

---

## Slide 3: Tổng quan kiến trúc pipeline 11 bước

- Bước 1–2: Xác định bài toán và tìm hiểu dữ liệu — `notebooks/01_data_understanding_and_cleaning.ipynb`
- Bước 3–4: Đánh giá chất lượng và tiền xử lý — `src/data/data_loader.py`, `data/interim/happiness_merged.csv`
- Bước 5: Khám phá dữ liệu có mục tiêu (EDA) — `notebooks/02_exploratory_data_analysis.ipynb`, `src/visualization/plots.py`
- Bước 6–7: Biến đổi đặc trưng và lựa chọn tham số — `src/features/feature_engineering.py`, `reports/tables/k_sensitivity_by_year.csv`
- Bước 8: Đánh giá và so sánh cấu hình — `notebooks/03_clustering_experiments_and_comparison.ipynb`
- Bước 9: Diễn giải tri thức, ghép cụm liên năm — `notebooks/04_cluster_profiling_and_evaluation.ipynb`
- Bước 10–11: Demo tương tác và kết luận — `app/app.py`, `docs/nghien_cuu/whr_nguon_du_lieu.md`

---

## Slide 4: Thu thập và Tiền xử lý dữ liệu

- Nguồn: bộ dữ liệu World Happiness Report trên Kaggle, 5 tệp CSV cho 2015–2019
- Cỡ mẫu dữ liệu thô: 158 / 157 / 155 / 156 / 156, tổng 782 dòng
- Loại 1 dòng United Arab Emirates năm 2018 vì khuyết hoàn toàn chỉ số `Perceptions of corruption`
- Loại các cột sai số khảo sát: `Standard Error`, `Lower/Upper Confidence Interval`, `Whisker.high/low`
- Chuẩn hóa tên cột về 13 cột snake_case, đồng bộ tên quốc gia (Macedonia, Swaziland, Taiwan, Hong Kong)
- Bổ sung mã ISO-3: 781/781 dòng hợp lệ, 164 quốc gia duy nhất, 162 mã phân biệt
- Kết quả: `data/interim/happiness_merged.csv` gồm 781 dòng (158/157/155/155/156 theo năm)

---

## Slide 5: Khám phá dữ liệu (EDA)

- Phân bố lệch rõ ở hai trụ cột: `generosity` skewness 1,04 và `corruption_perception` skewness 1,52 (lệch phải)
- Các trụ cột còn lại lệch nhẹ về bên trái: GDP −0,34; hỗ trợ xã hội −0,69; tuổi thọ −0,50; tự do −0,52
- Tương quan mạnh: GDP bình quân đầu người với tuổi thọ khỏe mạnh đạt r = 0,79 (vượt ngưỡng 0,7)
- Điểm hạnh phúc tương quan cao với GDP (0,79) và tuổi thọ (0,74), thấp với `generosity` (−0,01)
- Phát hiện ngoại lai bằng quy tắc 1,5 × IQR, tập trung ở các nước thu nhập cao và một số nước châu Phi
- Kết luận: chênh lệch thang đo giữa 6 trụ cột bắt buộc phải chuẩn hóa trước khi gom cụm
- Nguồn: `reports/figures/feature_distributions.png`, `correlation_heatmap.png`, `boxplots_outliers.png`

---

## Slide 6: Cơ sở thực nghiệm lựa chọn phương pháp chuẩn hóa

- Z-score: z = (x − mean) / std; Min-Max: x' = (x − min) / (max − min)
- Min-Max rất nhạy với ngoại lai nên nén các quốc gia trung bình vào một khoảng hẹp
- Silhouette của K-Means k = 3: Z-score 0,293 – 0,344; Min-Max 0,308 – 0,347; dữ liệu thô 0,314 – 0,340
- Chênh lệch giữa ba phương án dưới 0,05 nên quyết định dựa vào bản chất phép biến đổi
- Z-score cho 6 trụ cột đóng góp công bằng vào khoảng cách Euclidean, giữ được cấu trúc tương quan
- Độ ổn định qua 10 seed của K-Means/Z-score: ARI trung bình 0,979 – 1,000
- Nguồn: `reports/tables/model_comparison_metrics_by_year.csv`, `stability_ari.csv`

---

## Slide 7: Tự cài đặt thuật toán từ đầu (From Scratch)

- `SimpleKMeans`: khởi tạo K-Means++ theo xác suất tỉ lệ khoảng cách bình phương, `n_init = 10`, lưu `inertia_history` và `n_iter_`
- `SimpleHierarchicalClustering`: liên kết Ward thật bằng cập nhật Lance–Williams kèm bộ nhớ đệm tâm cụm, lưu `merge_history`
- `SimpleDBSCAN`: duyệt vùng lân cận theo `eps` và `min_samples`, gán nhãn −1 cho điểm nhiễu
- `SimplePCA`: ma trận hiệp phương sai và `np.linalg.eigh`, không dùng `sklearn.decomposition.PCA`
- Các độ đo Silhouette, Davies–Bouldin, Calinski–Harabasz và ARI đều tự cài đặt bằng vòng lặp và công thức cơ bản
- `scikit-learn` và `scipy` chỉ dùng trong `scripts/verify_scratch_implementations.py` để đối chứng, không dùng trong pipeline chính
- Thời gian chạy K-Means dưới 1 giây mỗi năm, Ward 0,8 – 1,4 giây mỗi năm cho 156 điểm

---

## Slide 8: Thẩm định số cụm tối ưu k*

- Khảo sát k trong đoạn [2, 9] cho từng năm bằng Elbow (Inertia) kết hợp Silhouette
- Bảng khảo sát gồm 40 dòng: 8 giá trị k nhân 5 năm — `reports/tables/k_sensitivity_by_year.csv`
- Kết quả: k* = 3 được cả 5 năm đồng thuận
- Silhouette cực đại theo năm: 0,2931 (2015); 0,3037 (2016); 0,3133 (2017); 0,3365 (2018); 0,3436 (2019)
- Số cụm tối ưu k* = 3 khớp với cấu trúc ba tầng của dữ liệu: phát triển, trung bình, khó khăn
- Cấu hình ba cụm được giữ làm mục đối chứng xuyên năm vì là cấu hình duy nhất so sánh được giữa các năm

---

## Slide 9: So sánh đối chứng các thuật toán và khảo sát DBSCAN

- K-Means/Standard: Silhouette 0,293 – 0,344; Davies–Bouldin 1,07 – 1,22; Calinski–Harabasz 74,9 – 86,0
- Ward/Standard: Silhouette 0,254 – 0,310; Davies–Bouldin 1,00 – 1,26; Calinski–Harabasz 59,9 – 71,0
- Ward là thuật toán tất định nên ghi ARI = 1,0 kèm giải thích thay vì chạy 10 seed hình thức
- DBSCAN quét đầy đủ: eps thuộc {0,6; 0,8; 1,0; 1,2} × min_samples thuộc {3, 4, 5}, tổng 60 dòng
- Với eps = 1,2 và min_samples = 4, DBSCAN chỉ tạo 1 đến 2 cụm và đánh dấu 24 đến 35 điểm nhiễu
- Nguyên nhân: 6 đặc trưng sau chuẩn hóa có mật độ khá đồng đều, không có vùng dày đặc trưng để DBSCAN khai thác
- Kết luận: chọn nhóm phương pháp dựa trên khoảng cách (K-Means làm chính, Ward làm đối chứng)
- Nguồn: `reports/tables/model_comparison_metrics_by_year.csv`, `dbscan_sweep.csv`

---

## Slide 10: Xây dựng chân dung 3 cụm kinh tế — xã hội

- Cụm 1 — Phát triển toàn diện: vượt trội đồng thời về GDP, tuổi thọ, hỗ trợ xã hội và nhận thức tham nhũng cao
- Cụm 2 — Đang phát triển phụ thuộc kinh tế: các chỉ số mức trung bình khá, chiếm đông quốc gia nhất
- Cụm 3 — Dễ bị tổn thương và Khó khăn: điểm rất thấp ở hầu hết trụ cột kinh tế, y tế, tự do
- Số quốc gia mỗi cụm theo năm: Cụm 1 là 29/27/29/24/28; Cụm 2 là 79/84/80/85/82; Cụm 3 là 50/46/46/46/46
- Điểm hạnh phúc trung bình thực tế: Cụm 1 đạt 6,73 – 6,85; Cụm 2 đạt 5,57 – 5,61; Cụm 3 đạt 4,10 – 4,26
- Chân dung dựng từ giá trị trung bình 6 đặc trưng, không dùng điểm hạnh phúc để gom cụm
- Nguồn: `reports/tables/cluster_trends.csv`, `reports/figures/radar_chart_clusters.png`

---

## Slide 11: Hậu kiểm độc lập với Điểm Hạnh phúc thực tế

- Quy tắc vàng: `happiness_score` không nằm trong ma trận đặc trưng X, chỉ dùng ở bước hậu kiểm
- Biểu đồ hộp điểm hạnh phúc theo cụm và theo năm cho thấy ba cụm tách biệt rõ rệt
- Chênh lệch điểm hạnh phúc trung bình giữa cụm cao nhất và thấp nhất của K-Means là 2,46 – 2,72 điểm
- Thứ tự phân hóa giữ nguyên qua cả 5 năm dù mỗi năm gom cụm độc lập
- Cấu hình đối chứng k = 3 cho ARI so với k* bằng 1,0 ở mọi năm, tức phân hoạch ổn định
- Kết luận: các cụm hình thành từ 6 trụ cột khách quan vẫn phản ánh đúng mức sống thực tế
- Nguồn: `reports/figures/validation_happiness_score_by_cluster.png`, `reports/tables/contrast_k3_by_year.csv`

---

## Slide 12: Theo dõi Dịch chuyển cụm của 156 quốc gia qua 5 năm

- Ghép cụm liên năm bằng `match_clusters_greedy`: ghép theo khoảng cách tâm cụm nhỏ nhất, hòa thì xét điểm hạnh phúc
- Khoảng cách tâm cụm của các cặp được ghép nằm trong 0,057 – 0,420 — `reports/tables/cross_year_matching.csv`
- Bảng dịch chuyển 156 quốc gia × 5 năm — `data/processed/country_cluster_shift.csv`
- 142 quốc gia ổn định tuyệt đối (91,0 phần trăm), 8 quốc gia biến động trung gian
- 4 quốc gia thăng hạng: Botswana, Georgia, Indonesia, Myanmar
- 2 quốc gia tụt hạng: Kuwait, Uruguay
- Nhận xét: cấu trúc phân tầng hạnh phúc bền vững; dịch chuyển chủ yếu do biến động vài trụ cột riêng lẻ
- Lưu ý dữ liệu: bảng có 17 ô khuyết do quốc gia vắng mặt ở một số năm, cộng UAE 2018 loại có chủ đích

---

## Slide 13: Giới thiệu Ứng dụng Demo Streamlit 4 Tab tương tác

- Chạy bằng lệnh `streamlit run app/app.py`, đọc trực tiếp dữ liệu đã sinh ở M1–M3
- Tab 1 — Tổng quan cụm và Radar Chart: chọn năm (2015–2019) và thuật toán (K-Means hoặc Ward), xem thẻ KPI Silhouette, Davies–Bouldin, Calinski–Harabasz
- Tab 2 — Bản đồ thế giới: Choropleth tô màu theo cụm bằng mã ISO-3, hover hiện tên quốc gia, mã ISO-3, nhóm cụm và điểm hạnh phúc
- Tab 3 — Tra cứu quốc gia: chọn một trong 156 quốc gia, xem lịch sử phân cụm và biểu đồ biến thiên 6 chỉ số
- Tab 4 — Thử nghiệm gán nhãn: kéo 6 thanh trượt, hệ thống z-score hóa và tính khoảng cách Euclid tới 3 tâm cụm K-Means 2019
- Các hàm đọc dữ liệu được bọc `@st.cache_data` nên đổi năm hoặc thuật toán không phải nạp lại từ đĩa
- Mọi con số trong ứng dụng lấy từ CSV/JSON, không hardcode

---

## Slide 14: Đóng góp chính, Kết luận và Hạn chế

- Đóng góp: pipeline 5 năm chạy lại được, thuật toán gom cụm và độ đo tự cài đặt, bảng ghép cụm liên năm, demo tương tác
- Kết luận 1: k* = 3 đồng thuận cả 5 năm, Silhouette 0,293 – 0,344
- Kết luận 2: ba cụm có chân dung kinh tế — xã hội rõ ràng và hậu kiểm điểm hạnh phúc phân hóa sâu sắc
- Kết luận 3: 142/156 quốc gia giữ nguyên nhóm trong 2015–2019
- Hạn chế dữ liệu: thiếu chỉ số văn hóa và thể chế chuyên sâu, cỡ mẫu mỗi năm khác nhau, UAE khuyết 2018
- Hạn chế phương pháp: gom cụm không có nhãn chuẩn để đối chiếu, tên cụm mang tính diễn giải chủ quan
- Hạn chế dữ liệu ngoại lai: biến động kinh tế và thể chế của một số quốc gia không được phản ánh kịp trong khảo sát

---

## Slide 15: Hướng phát triển và Lời cảm ơn

- Mở rộng chuỗi thời gian sang 2020–2024 để kiểm tra cấu trúc cụm sau đại dịch COVID-19
- Bổ sung đặc trưng ngoài 6 trụ cột: bất bình đẳng Gini, chi tiêu y tế, chỉ số chất lượng quản trị
- So sánh thêm thuật toán phân cụm mờ (Fuzzy C-Means) cho các quốc gia đang chuyển tiếp
- Phân tích độ nhạy theo trọng số trụ cột khi ưu tiên thể chế hoặc kinh tế
- Đưa demo lên dashboard công khai và bổ sung chức năng xuất báo cáo PDF theo từng quốc gia
- Nhóm 12 xin chân thành cảm ơn Hội đồng chấm đồ án đã lắng nghe và góp ý
- Phần hỏi đáp: cả ba thành viên cùng tham gia trả lời

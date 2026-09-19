# BẢN PHÂN TÍCH CHI TIẾT NHIỆM VỤ THÀNH VIÊN — NHÓM 12
## Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)

> **Học phần:** Khai thác dữ liệu (Data Mining)  
> **Giảng viên hướng dẫn:** Bộ môn Khoa học dữ liệu / Trí tuệ nhân tạo  
> **Thời gian thực hiện:** 28 ngày (4 tuần thực nghiệm + tổng duyệt)  
> **Căn cứ tài liệu gốc:** [`ke_hoach_nhom.md`](./ke_hoach_nhom.md), [`phan_cong_cong_viec.md`](./phan_cong_cong_viec.md), [`CONTEXT.md`](../../CONTEXT.md)

---

## 📌 BẢNG TỔNG HỢP VAI TRÒ & TỶ LỆ ĐÓNG GÓP

| STT | Thành viên | Mã sinh viên | Vai trò chính trong dự án | Tỷ lệ đóng góp | Giai đoạn phụ trách chính (Mục đề cương) |
|:---:|:---|:---:|:---|:---:|:---|
| 1 | **Hà Mạnh Trường** *(Nhóm trưởng)* | 2045240326 | Quản lý dự án, Kỹ thuật dữ liệu 5 năm (Data Engineering), Kiểm soát chất lượng & Tái lập, Ghép báo cáo Word | **34%** | Giai đoạn 1, 2, 4 (Xác định bài toán, Hiểu dữ liệu, Tiền xử lý dữ liệu) |
| 2 | **Huỳnh Tâm Trí** | 2045240315 | Kỹ sư Thuật toán & Mô hình hóa (From-Scratch Clustering & Evaluation), Thực nghiệm 5 cấu hình × 5 năm | **33%** | Giai đoạn 6, 7, 8 (Biến đổi đặc trưng, Huấn luyện mô hình, So sánh & Đánh giá) |
| 3 | **Ngô Quang Trung** | 2045240325 | Phân tích Khám phá (EDA), Diễn giải tri thức & Dịch chuyển liên năm, Ứng dụng Demo Streamlit, Thiết kế Slide | **33%** | Giai đoạn 3, 5, 9, 10, 11 (Chất lượng dữ liệu, EDA, Diễn giải tri thức, Demo tương tác, Kết luận) |

---

## 👤 1. HÀ MẠNH TRƯỜNG (Nhóm trưởng — 34%)

### 🎯 Trách nhiệm trọng tâm:
Chịu trách nhiệm về tính toàn vẹn của dữ liệu đầu vào cho cả 5 năm (2015–2019), xây dựng module nạp/làm sạch dữ liệu, kiểm soát tính tái lập (*reproducibility*) của mã nguồn và tích hợp tự động báo cáo tổng kết của dự án.

### 📅 Chi tiết nhiệm vụ theo 5 Mốc thời gian:

#### • Mốc M0: Chốt kiến trúc & Ghi nhận quyết định (Ngày 1–2)
- [x] Chủ trì buổi họp chốt baseline kỹ thuật: thống nhất thực nghiệm 5 năm độc lập, số cụm $k^*$ là kết quả chính, $k=3$ là đối chứng xuyên năm.
- [x] Soạn thảo kiến trúc [`docs/adr/0002-gom-cum-theo-nam-va-ghep-cum-lien-nam.md`](../../docs/adr/0002-gom-cum-theo-nam-va-ghep-cum-lien-nam.md).
- [x] Chuẩn hóa thuật ngữ nghiệp vụ và ranh giới bất biến trong [`CONTEXT.md`](../../CONTEXT.md).
- [x] Hoàn thiện kế hoạch 28 ngày và bảng phân công công việc của nhóm.

#### • Mốc M1: Xây dựng nền dữ liệu 5 năm & Kiểm soát chất lượng (Ngày 3–7)
- [ ] **Phát triển module [`src/data/data_loader.py`](../../src/data/data_loader.py):**
  - Xây dựng từ điển ánh xạ cột chuẩn hóa `COLUMN_MAPPING` qua 5 năm.
  - Viết hàm `build_interim_dataset(years=[2015..2019])` gộp 5 năm dữ liệu với schema thống nhất.
  - Cài đặt cơ chế xử lý đồng bộ tên quốc gia `harmonize_country_names`, bảng sửa lỗi `COUNTRY_NAME_FIXES` (như *Macedonia* vs *North Macedonia*, *Swaziland* vs *Eswatini*) và chuyển đổi mã `country_to_iso3`.
- [ ] **Hoàn thiện [`notebooks/01_data_understanding_and_cleaning.ipynb`](../../notebooks/01_data_understanding_and_cleaning.ipynb):**
  - Trình bày mục 1 (Bài toán & mục tiêu) và mục 2 (Tìm hiểu cấu trúc 5 năm).
  - Loại bỏ các cột sai số đo lường (`Standard Error`, khoảng tin cậy `Whisker`) và ghi rõ luận điểm bảo vệ.
  - Xử lý trường hợp khuyết dữ liệu UAE năm 2018 (loại khỏi phân tích chính).
  - Xuất tệp dữ liệu trung gian sạch [`data/interim/happiness_merged.csv`](../../data/interim/happiness_merged.csv).
- [ ] **Quản trị môi trường & kho mã nguồn:**
  - Chốt danh mục phiên bản thư viện cố định trong [`requirements.txt`](../../requirements.txt).
  - Cập nhật [`README.md`](../../README.md) hướng dẫn thiết lập và chạy dự án từ đầu.
  - Cập nhật [`.gitignore`](../../.gitignore) để theo dõi các tài liệu quan trọng.

#### • Mốc M2: Kiểm thử chất lượng & Tối ưu hiệu năng (Ngày 8–14)
- [ ] Soát lỗi mã nguồn và docstring tiếng Việt của các hàm trong `src/data/`.
- [ ] Phối hợp cùng Trí gỡ lỗi hiệu năng thuật toán phân cấp Ward (tối ưu cấu trúc dữ liệu để đạt thời gian chạy < 30 giây cho 156 điểm).
- [ ] Kiểm tra tính tương đối của các đường dẫn trong notebook (tránh hardcode đường dẫn tuyệt đối máy cá nhân).

#### • Mốc M3: Kiểm soát tính nhất quán của số liệu thực nghiệm (Ngày 15–21)
- [ ] Thẩm định các tệp CSV xuất ra từ thực nghiệm của Trí: đối chiếu số lượng dòng, tính hợp lệ của số cụm $k^* \in [2, 5]$ qua các năm.
- [ ] Rà soát tính toàn vẹn của bảng dịch chuyển cụm 156 quốc gia × 5 năm (đảm bảo không bị phân mảnh dòng do lệch tên).
- [ ] Kiểm tra 12 hình vẽ của nhóm đáp ứng chuẩn độ phân giải 300 DPI.

#### • Mốc M4: Tự động hóa tạo báo cáo Word & Soạn thảo Mục 1–4 (Ngày 22–26)
- [ ] **Xây dựng công cụ [`reports/final_report/build_report.py`](./build_report.py):**
  - Xây dựng backend tạo tài liệu Word `.docx` thuần Python (dựa trên chuẩn Open Packaging Conventions / OOXML) không phụ thuộc mạng internet.
  - Tự động nhúng trang bìa chuẩn, mục lục tự động (TOC), chú thích bảng (Bảng X), chú thích hình (Hình Y), và tự động đọc dữ liệu từ `reports/tables/*.csv`.
- [ ] **Soạn thảo và chịu trách nhiệm nội dung các Mục 1, 2, 3, 4 trong báo cáo:**
  - Mục 1: Bảng phân công công việc và cam kết đóng góp.
  - Mục 2: Giới thiệu đề tài, bối cảnh World Happiness Report, 4 câu hỏi khai thác.
  - Mục 3: Dữ liệu (nguồn gốc, ý nghĩa 6 biến cơ sở, phân tích chất lượng dữ liệu).
  - Mục 4: Tiền xử lý dữ liệu (đồng nhất schema, làm sạch, chuẩn hóa tên quốc gia).

#### • Mốc M5: Tổng duyệt, Rehearsal & Đóng gói nộp bài (Ngày 27–28)
- [ ] Chạy kiểm thử toàn diện toàn bộ pipeline từ đầu trên môi trường sạch (*end-to-end reproducibility*).
- [ ] Chuẩn bị trả lời vấn đáp phần: Xác định bài toán, Nguồn gốc dữ liệu Cantril Ladder, Quy trình tiền xử lý và đồng bộ dữ liệu.
- [ ] **Rehearsal đổi vai:** Đảm nhiệm thuyết trình phần **Phương pháp thuật toán & Tham số** (thay cho Trí) để chứng minh nắm toàn diện đồ án.
- [ ] Gắn nhãn phiên bản `git tag v1.0`, kiểm tra lần cuối checklist 10 tiêu chí nộp bài và bàn giao file nộp.

### 📦 Danh mục sản phẩm bàn giao (Deliverables):
1. Mã nguồn: [`src/data/data_loader.py`](../../src/data/data_loader.py) (đầy đủ các hàm tiền xử lý 5 năm).
2. Dữ liệu: [`data/interim/happiness_merged.csv`](../../data/interim/happiness_merged.csv).
3. Notebook: [`notebooks/01_data_understanding_and_cleaning.ipynb`](../../notebooks/01_data_understanding_and_cleaning.ipynb).
4. Công cụ báo cáo: [`reports/final_report/build_report.py`](./build_report.py).
5. Văn bản báo cáo: Mục 1, 2, 3, 4 trong [`bao_cao.md`](./bao_cao.md) và file [`Bao_cao_De_tai_16_Nhom_12.docx`](./Bao_cao_De_tai_16_Nhom_12.docx).

---

## 👤 2. HUỲNH TÂM TRÍ (Thành viên — 33%)

### 🎯 Trách nhiệm trọng tâm:
Chịu trách nhiệm toàn bộ về phần **Cốt lõi thuật toán học máy (*From-Scratch*)**, triển khai ma trận thực nghiệm 5 cấu hình gom cụm trên 5 năm độc lập, khảo sát tham số tối ưu và đo lường độ ổn định của các giải thuật.

### 📅 Chi tiết nhiệm vụ theo 5 Mốc thời gian:

#### • Mốc M0: Nghiên cứu công thức & Thiết kế chữ ký hàm (Ngày 1–2)
- [x] Nghiên cứu cơ sở lý thuyết toán học: Khoảng cách Euclidean, khởi tạo K-Means++, cập nhật tâm cụm K-Means, công thức Lance–Williams cho phân cấp liên kết Ward, giải thuật DBSCAN dựa trên mật độ.
- [x] Nghiên cứu công thức toán các độ đo nội tại: Silhouette Coefficient, Davies-Bouldin Index, Calinski-Harabasz Index, Adjusted Rand Index (ARI).
- [x] Thống nhất chữ ký hàm (*API signature*) và cấu trúc trả về phẳng cho `evaluate_clustering`.
- [x] Soạn thảo [`docs/adr/0003-mo-rong-tu-cai-dat-pca-dbscan-json.md`](../../docs/adr/0003-mo-rong-tu-cai-dat-pca-dbscan-json.md).

#### • Mốc M1: Xây dựng khung kiểm chứng thuật toán đối chứng (Ngày 3–7)
- [ ] **Viết bộ kiểm thử [`scripts/verify_scratch_implementations.py`](../../scripts/verify_scratch_implementations.py):**
  - Viết assert kiểm tra bất biến quy tắc vàng: Ma trận đặc trưng $X$ tuyệt đối không giao với `{happiness_score, happiness_rank}`.
  - Viết các bài test so sánh kết quả hàm tự viết với thư viện chuẩn `scikit-learn` và `scipy` (với dung sai toán học xác định).

#### • Mốc M2: Tự cài đặt thuật toán & Các độ đo đánh giá from-scratch (Ngày 8–14)
- [ ] **Tự cài đặt trong [`src/models/clustering.py`](../../src/models/clustering.py):**
  - Lớp `SimpleKMeans`: cơ chế khởi tạo `kmeans++`, lặp `n_init=10` lần chọn kết quả có `inertia` nhỏ nhất, lưu vết `inertia_history` và số vòng lặp `n_iter_`.
  - Lớp `SimpleHierarchicalClustering`: phân cấp tích tụ sử dụng tiêu chí **Ward thật** thông qua công thức Lance–Williams và kỹ thuật cache khoảng cách.
  - Lớp `SimpleDBSCAN`: tự cài đặt tìm láng giềng bán kính $\epsilon$, lan truyền cụm (*core points*, *border points*), đánh nhãn điểm nhiễu $-1$.
  - Hàm wrapper tiện ích: `run_kmeans`, `run_hierarchical`, `run_dbscan`.
  - Hàm đánh giá mô hình `evaluate_clustering`: tính toán và trả về từ điển phẳng gồm 7 chỉ số (silhouette, davies_bouldin, calinski_harabasz, inertia, n_clusters, n_noise, sizes).
  - Các hàm độ đo độc lập: `calculate_silhouette_score_simple`, `calculate_davies_bouldin_score_simple`, `calculate_calinski_harabasz_score_simple`, `calculate_adjusted_rand_index`.
  - Hàm lưu và nạp mô hình: `save_cluster_artifacts` và `load_cluster_artifacts` (dưới định dạng chuẩn JSON).
- [ ] **Tự cài đặt trong [`src/features/feature_engineering.py`](../../src/features/feature_engineering.py):**
  - Tự code thuật toán giảm chiều `SimplePCA` dựa trên ma trận hiệp phương sai và hàm trị riêng `np.linalg.eigh`, giữ nguyên chữ ký hàm `apply_pca`.
- [ ] **Nghiệm thu kiểm thử:** Chạy `verify_scratch_implementations.py` đạt **PASS 20/20 hạng mục**.

#### • Mốc M3: Thực thi ma trận thực nghiệm 5 năm × 5 cấu hình (Ngày 15–21)
- [ ] **Hoàn thiện [`notebooks/03_clustering_experiments_and_comparison.ipynb`](../../notebooks/03_clustering_experiments_and_comparison.ipynb):**
  - **Khảo sát chọn $k$:** Chạy vòng lặp qua 5 năm (2015–2019), tính toán Elbow (Inertia) và Silhouette cho $k \in [2, 9]$, tìm ra số cụm tối ưu $k^*$ của từng năm ➔ xuất file [`reports/tables/k_sensitivity_by_year.csv`](../../reports/tables/k_sensitivity_by_year.csv).
  - **Ma trận so sánh 5 cấu hình lõi:** Chạy K-Means Z-score, K-Means Min-Max, K-Means Raw, Ward Z-score, DBSCAN Z-score trên cả 5 năm ➔ xuất file [`reports/tables/model_comparison_metrics_by_year.csv`](../../reports/tables/model_comparison_metrics_by_year.csv).
  - **Quét siêu tham số DBSCAN:** Chạy toàn diện 4 giá trị $\epsilon \in \{0.6, 0.8, 1.0, 1.2\}$ kết hợp 3 giá trị `min_samples` $\in \{3, 4, 5\}$ cho 5 năm ➔ xuất file [`reports/tables/dbscan_sweep.csv`](../../reports/tables/dbscan_sweep.csv).
  - **Đánh giá độ ổn định cụm:** Chạy K-Means trên 10 seed ngẫu nhiên khác nhau, tính chỉ số ARI trung bình; ghi nhận ARI = 1.0 cho Ward và DBSCAN kèm luận điểm toán học ➔ xuất file [`reports/tables/stability_ari.csv`](../../reports/tables/stability_ari.csv).
  - **Cấu hình đối chứng $k=3$:** Chạy gom cụm 3 nhóm cho cả 5 năm để phục vụ đối chiếu liên năm ➔ xuất [`reports/tables/contrast_k3_by_year.csv`](../../reports/tables/contrast_k3_by_year.csv).
  - Lưu trữ toàn bộ trọng tâm cụm và tham số chuẩn hóa vào thư mục [`models/*.json`](../../models).

#### • Mốc M4: Soạn thảo Mục 5–7 của báo cáo & Đóng góp tài liệu (Ngày 22–26)
- [ ] Viết đầy đủ docstrings giải thích công thức toán học và nguyên lý thuật toán bằng tiếng Việt cho toàn bộ file code.
- [ ] **Soạn thảo và chịu trách nhiệm nội dung Mục 5, 6, 7 trong báo cáo:**
  - Mục 5: Phương pháp luận gom cụm (nguyên lý K-Means, Ward, DBSCAN, PCA, công thức các chỉ số đánh giá).
  - Mục 6: Khảo sát tham số (chọn $k$ theo Elbow/Silhouette, quét lưới DBSCAN, phân tích độ ổn định ARI).
  - Mục 7: So sánh các phương án (so sánh 3 cách chuẩn hóa, so sánh hiệu năng 3 thuật toán, đánh giá thời gian chạy).

#### • Mốc M5: Tổng duyệt, Rehearsal & Vấn đáp (Ngày 27–28)
- [ ] Chuẩn bị trả lời vấn đáp chuyên sâu về: Công thức toán học, tại sao chọn Ward thay vì Single/Complete Linkage, lý do DBSCAN nhạy cảm với mật độ dữ liệu WHR, cách thức tính điểm Silhouette.
- [ ] **Rehearsal đổi vai:** Đảm nhiệm thuyết trình phần **Ứng dụng Demo Streamlit** (thay cho Trung) để chứng minh khả năng làm chủ toàn bộ sản phẩm của nhóm.

### 📦 Danh mục sản phẩm bàn giao (Deliverables):
1. Mã nguồn thuật toán: [`src/models/clustering.py`](../../src/models/clustering.py) và [`src/features/feature_engineering.py`](../../src/features/feature_engineering.py).
2. Kiểm thử: [`scripts/verify_scratch_implementations.py`](../../scripts/verify_scratch_implementations.py) (với 20 assertions đối chứng).
3. Notebook thực nghiệm: [`notebooks/03_clustering_experiments_and_comparison.ipynb`](../../notebooks/03_clustering_experiments_and_comparison.ipynb).
4. Tệp mô hình: 10 tệp JSON lưu trữ trong [`models/`](../../models) (`kmeans_2015..2019.json`, `hierarchical_2015..2019.json`).
5. Các bảng số liệu thực nghiệm: 5 file CSV trong `reports/tables/`.
6. Văn bản báo cáo: Mục 5, 6, 7 trong [`bao_cao.md`](./bao_cao.md) và file Word.

---

## 👤 3. NGÔ QUANG TRUNG (Thành viên — 33%)

### 🎯 Trách nhiệm trọng tâm:
Chịu trách nhiệm về **Phân tích khám phá dữ liệu (EDA)**, **Diễn giải tri thức kinh tế - xã hội**, thực hiện thuật toán **Ghép cụm liên năm & Bảng dịch chuyển cụm 156 quốc gia**, xây dựng sản phẩm **Demo tương tác Streamlit** và thiết kế slide bảo vệ.

### 📅 Chi tiết nhiệm vụ theo 5 Mốc thời gian:

#### • Mốc M0: Thiết kế giao diện & Danh mục trực quan hóa (Ngày 1–2)
- [x] Lên danh mục cố định 12 hình vẽ trực quan hóa chất lượng cao (300 DPI) cho báo cáo.
- [x] Lập bản phác thảo giao diện ứng dụng Streamlit 4 tab phục vụ hội đồng chấm đồ án.
- [x] Liệt kê các câu hỏi nghiệp vụ và hạn chế của mô hình cần làm rõ trong mục kết luận.

#### • Mốc M1: Đánh giá chất lượng dữ liệu & Nghiên cứu bối cảnh (Ngày 3–7)
- [ ] Thực hiện đánh giá chất lượng dữ liệu 5 năm (tỷ lệ khuyết thiếu, trùng lặp, độ phân tán, số lượng quốc gia từng năm).
- [ ] Thu thập tài liệu chuyên sâu về báo cáo Hạnh phúc thế giới: Phương pháp khảo sát Cantril Ladder, khái niệm Dystopia, sự tương quan giữa điểm hạnh phúc và 6 yếu tố.
- [ ] Kiểm tra và đối chiếu danh sách mã ISO-3 của các quốc gia để phục vụ vẽ bản đồ thế giới.
- [ ] Soạn thảo bản nháp bộ 20 câu hỏi vấn đáp bảo vệ đồ án.

#### • Mốc M2: Xây dựng biểu đồ trực quan & Phân tích EDA (Ngày 8–14)
- [ ] **Hoàn thiện module [`src/visualization/plots.py`](../../src/visualization/plots.py):**
  - Viết các hàm vẽ chuẩn 300 DPI: `plot_feature_distributions` (KDE/Histogram), `plot_correlation_heatmap`, `plot_outliers_boxplot`, `plot_clusters_2d`, `plot_cluster_radar`, `plot_dendrogram`, `plot_happiness_score_by_cluster`.
- [ ] **Hoàn thiện [`notebooks/02_exploratory_data_analysis.ipynb`](../../notebooks/02_exploratory_data_analysis.ipynb):**
  - Khám phá hình thái phân phối (độ lệch skewness) của 6 đặc trưng.
  - Phân tích đa cộng tuyến và tương quan tuyến tính giữa GDP, Tuổi thọ và Hỗ trợ xã hội.
  - Phát hiện các quốc gia ngoại lai (*outliers*) và đưa ra khuyến nghị lựa chọn bộ chuẩn hóa dữ liệu phù hợp (chọn Standard Scaler làm cấu hình chính).
  - Xuất các hình EDA chuẩn 300 DPI vào thư mục [`reports/figures/`](../../reports/figures).

#### • Mốc M3: Diễn giải tri thức, Ghép cụm liên năm & Dịch chuyển quốc gia (Ngày 15–21)
- [ ] **Cập nhật và hoàn thiện [`notebooks/04_cluster_profiling_and_evaluation.ipynb`](../../notebooks/04_cluster_profiling_and_evaluation.ipynb):**
  - **Trực quan hóa PCA 2D lưới 5 năm:** Chiếu dữ liệu 5 năm lên không gian 2 thành phần chính để quan sát ranh giới cụm (`pca_clusters_grid.png`).
  - **Xây dựng chân dung cụm (*Cluster Profiling*):** Tính giá trị trung bình 6 yếu tố, vẽ Radar chart theo từng năm; đặt tên định tính có ý nghĩa kinh tế - xã hội (ví dụ: *Cụm Phát triển toàn diện*, *Cụm Đang phát triển phụ thuộc kinh tế*, *Cụm Dễ bị tổn thương*).
  - **Hậu kiểm độc lập (*Post-clustering Validation*):** Đối chiếu nhãn cụm với `happiness_score` và `happiness_rank`, vẽ biểu đồ boxplot chứng minh các cụm có sự phân hóa điểm số hạnh phúc rõ rệt (dù không đưa biến này vào quá trình gom cụm).
  - **Thuật toán ghép cụm liên năm (`match_clusters_greedy`):** Ghép cặp các cụm giữa các năm liền kề theo khoảng cách tâm cụm nhỏ nhất; nếu hòa thì dùng điểm hạnh phúc trung bình làm tiêu chí phụ.
  - **Lập bảng dịch chuyển cụm 156 quốc gia qua 5 năm:** Theo dõi quốc gia nào tăng hạng cụm, quốc gia nào tụt hạng cụm ➔ xuất file [`data/processed/country_cluster_shift.csv`](../../data/processed).
  - **Phân tích xu hướng:** Vẽ biểu đồ biến động số lượng quốc gia trong từng cụm qua thời gian (`cluster_count_trend.png`).
- [ ] Soạn thảo mục 8, 9, 10, 11 của báo cáo Word.

#### • Mốc M4: Phát triển Ứng dụng Demo Streamlit & Thiết kế Slide (Ngày 22–26)
- [ ] **Nâng cấp và hoàn thiện ứng dụng [`app/app.py`](../../app/app.py) thành 4 tab tương tác hoàn chỉnh:**
  - *Tab 1 — Tổng quan cụm & Radar Chart:* Cho phép người dùng chọn năm (2015–2019), chọn thuật toán, số cụm $k$, hiển thị biểu đồ Radar so sánh các nhóm và các chỉ số đo lường.
  - *Tab 2 — Bản đồ thế giới (Choropleth Map):* Trực quan hóa màu sắc các cụm lên bản đồ địa lý theo mã quốc gia ISO-3.
  - *Tab 3 — Tra cứu quốc gia & Lịch sử dịch chuyển:* Tìm kiếm một quốc gia bất kỳ (như Việt Nam, Na Uy) để xem biểu đồ biến động chỉ số và lịch sử dịch chuyển nhóm qua 5 năm.
  - *Tab 4 — Thử nghiệm gán nhãn cho quốc gia mới (*What-if Analysis*):* Cho phép người dùng trượt 6 thanh giá trị giả định để thuật toán gán ngay vào cụm phù hợp và hiển thị khoảng cách tới các tâm cụm.
  - Tối ưu bộ nhớ đệm Streamlit `@st.cache_data` theo thời gian sửa file (`mtime`).
- [ ] **Xây dựng Slide thuyết trình:** Soạn thảo khung nội dung 12–15 slide chuẩn, cô đọng phục vụ báo cáo trong 10 phút.

#### • Mốc M5: Tổng duyệt, Điều hành Rehearsal & Vấn đáp (Ngày 27–28)
- [ ] Đóng vai trò điều phối buổi tổng duyệt đổi vai giữa 3 thành viên.
- [ ] Chuẩn bị trả lời vấn đáp phần: Ý nghĩa kinh tế - xã hội của từng cụm, giải thích tại sao một số quốc gia bị dịch chuyển cụm, các hạn chế của bộ dữ liệu và hướng phát triển.
- [ ] **Rehearsal đổi vai:** Đảm nhiệm thuyết trình phần **Thu thập và Tiền xử lý dữ liệu** (thay cho Trường) để sẵn sàng trước mọi câu hỏi của hội đồng.

### 📦 Danh mục sản phẩm bàn giao (Deliverables):
1. Mã nguồn trực quan hóa: [`src/visualization/plots.py`](../../src/visualization/plots.py).
2. Ứng dụng demo: [`app/app.py`](../../app/app.py) (4 tab tương tác).
3. Notebook: [`notebooks/02_exploratory_data_analysis.ipynb`](../../notebooks/02_exploratory_data_analysis.ipynb) và [`notebooks/04_cluster_profiling_and_evaluation.ipynb`](../../notebooks/04_cluster_profiling_and_evaluation.ipynb).
4. Dữ liệu xử lý: [`data/processed/country_cluster_shift.csv`](../../data/processed) và các file processed liên quan.
5. Hình ảnh báo cáo: 12 hình vẽ độ phân giải 300 DPI trong [`reports/figures/`](../../reports/figures).
6. Slide thuyết trình và Mục 8, 9, 10, 11 trong báo cáo Word.

---

## 🔄 4. CƠ CHẾ BẢO ĐẢM NẮM TOÀN DIỆN & VẤN ĐÁP (CROSS-UNDERSTANDING)

Nhằm đảm bảo cả 3 thành viên không bị làm việc theo kiểu "ốc đảo" và tự tin đạt điểm tối đa ở phần vấn đáp cá nhân trước hội đồng chấm:

1. **Quy tắc Walkthrough 20 phút:** Sau khi bất kỳ thành viên nào hoàn thành một module, phải dành 20 phút chia sẻ màn hình giải thích từng dòng code và công thức toán học cho 2 thành viên còn lại.
2. **Nguyên tắc "3 Yêu cầu tối thiểu" cho từng người:**
   - Cả 3 người đều phải tự tay chạy được toàn bộ 4 notebook và khởi chạy được app Streamlit trên máy tính của mình.
   - Cả 3 người đều phải viết và giải thích được công thức tính toán **Silhouette Score**.
   - Cả 3 người đều phải nêu và giải thích được đặc trưng của một cụm bất kỳ trong một năm ngẫu nhiên do giảng viên yêu cầu.
3. **Rehearsal đổi vai trước ngày bảo vệ:**
   - **Hà Mạnh Trường:** Thuyết trình chéo phần *Phương pháp gom cụm & Khảo sát tham số*.
   - **Huỳnh Tâm Trí:** Thuyết trình chéo phần *Demo tương tác Streamlit*.
   - **Ngô Quang Trung:** Thuyết trình chéo phần *Khám phá dữ liệu & Tiền xử lý*.
4. **Cam kết số liệu:** Mọi thành viên đều phải đối chiếu các số liệu trong phần báo cáo mình phụ trách về tệp CSV gốc trong `reports/tables/` trước khi ký tên xác nhận nộp đồ án.

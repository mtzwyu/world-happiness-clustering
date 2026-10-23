# BẢNG KIỂM ĐỊNH & NGHIỆM THU 10 TIÊU CHÍ NỘP BÀI (RUBRIC 10.0)

**Học phần:** Khai thác dữ liệu (Data Mining) — Học kỳ I, Năm học 2026–2027  
**Đề tài 16:** Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report)  
**Nhóm sinh viên thực hiện:** Nhóm 12 — Lớp KHDL Khóa 2023–2027  
**Sinh viên phụ trách nghiệm thu:** Hà Mạnh Trường (MSSV: 2045240326, Nhóm trưởng)  
**Tài liệu đối soát:** [`docs/huong_dan/De_tai_nhom_Khai_thac_du_lieu_SV_KHDL_nam_3.md`](../huong_dan/De_tai_nhom_Khai_thac_du_lieu_SV_KHDL_nam_3.md) (Mục 3.1 & 3.2, Thang điểm 10,0)  
**Thời điểm kiểm định:** Mốc M5 — Ngày 27 trong kế hoạch 28 ngày  
**Kết quả tổng quan:** **10/10 tiêu chí ĐẠT CHUẨN XUẤT SẮC (Dự kiến đạt 10,0 / 10,0 điểm)**

---

## I. BẢNG TỔNG HỢP ĐỐI SOÁT ĐIỂM SỐ THEO RUBRIC

| STT | Nhóm tiêu chí | Nội dung tiêu chí | Điểm tối đa | Tự đánh giá | Mức độ tự tin | Người phụ trách chính |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Báo cáo Word | Xác định bài toán và hiểu dữ liệu | 0,50 | 0,50 | 100% | Hà Mạnh Trường |
| **2** | Báo cáo Word | Tiền xử lý và chuẩn bị dữ liệu | 1,00 | 1,00 | 100% | Hà Mạnh Trường |
| **3** | Báo cáo Word | Phương pháp khai thác dữ liệu & From-scratch | 1,50 | 1,50 | 100% | Huỳnh Tâm Trí |
| **4** | Báo cáo Word | Thực nghiệm và đánh giá đa độ đo | 1,50 | 1,50 | 100% | Huỳnh Tâm Trí & Hà Mạnh Trường |
| **5** | Báo cáo Word | Diễn giải kết quả và insight kinh tế - xã hội | 1,00 | 1,00 | 100% | Ngô Quang Trung |
| **6** | Báo cáo Word | Chất lượng báo cáo và khả năng tái lập | 0,50 | 0,50 | 100% | Hà Mạnh Trường |
| **7** | Báo cáo & Demo | Trình bày vấn đề và pipeline báo cáo | 0,50 | 0,50 | 100% | Hà Mạnh Trường (Phần 1, Slide 1–4) |
| **8** | Báo cáo & Demo | Demo sản phẩm tương tác Streamlit 4 tab | 1,50 | 1,50 | 100% | Ngô Quang Trung (Phần 3, Slide 12–16) |
| **9** | Báo cáo & Demo | Giải thích kết quả và công thức kỹ thuật | 1,00 | 1,00 | 100% | Huỳnh Tâm Trí (Phần 2, Slide 5–11) |
| **10** | Báo cáo & Demo | Trả lời câu hỏi vấn đáp và phối hợp nhóm | 1,00 | 1,00 | 100% | Cả 3 thành viên (0,50đ Q&A + 0,50đ phối hợp) |
| **TỔNG**| **TOÀN DIỆN** | **TỔNG ĐIỂM ĐỒ ÁN** | **10,00** | **10,00** | **100%** | **Nhóm 12** |

---

## II. CHI TIẾT ĐỐI SOÁT 10 TIÊU CHÍ KÈM MINH CHỨNG ĐỊNH LƯỢNG

### Tiêu chí 1: Xác định bài toán và hiểu dữ liệu (0,50 điểm)
- **Yêu cầu đề cương:** Mục tiêu rõ ràng; mô tả dữ liệu, thuộc tính, nguồn Kaggle và câu hỏi khai thác đúng bản chất.
- **Hiện trạng đồ án:**
  - Mục tiêu nghiên cứu: Phân nhóm tự nhiên các quốc gia trên thế giới dựa trên 6 trụ cột chất lượng cuộc sống mà không phụ thuộc vào thứ hạng chủ quan (`Happiness Score` / `Happiness Rank`).
  - Nguồn dữ liệu: Bộ dữ liệu World Happiness Report (2015–2019) từ Kaggle, gồm 5 bảng CSV hàng năm với tổng cộng 782 quan sát thô.
  - Phân tích thuộc tính: Bảng mô tả chi tiết 6 biến cơ sở (`gdp_per_capita`, `social_support`, `healthy_life_expectancy`, `freedom`, `generosity`, `corruption_perception`) kèm đơn vị đo và phân phối thống kê.
- **Minh chứng định lượng:**
  - Tệp báo cáo Word: `reports/final_report/Nhom12_BaoCao.docx` (Mục 1.1, 1.2, 2.1).
  - Notebook 01: `notebooks/01_data_understanding_and_cleaning.ipynb` (Phần 1 & 2).
  - Slide thuyết trình: `reports/presentation/Nhom12_BaoCao_Slides.pptx` (Slide 2: Bối cảnh, Mục tiêu & Câu hỏi nghiên cứu).

---

### Tiêu chí 2: Tiền xử lý và chuẩn bị dữ liệu (1,00 điểm — Hà Mạnh Trường phụ trách)
- **Yêu cầu đề cương:** Phát hiện và xử lý vấn đề dữ liệu hợp lý; giải thích quyết định; tạo đúng representation cho clustering.
- **Hiện trạng đồ án:**
  - Đồng nhất cấu trúc cột: Xây dựng bảng từ điển ánh xạ `COLUMN_MAPPING` đồng nhất 5 cấu trúc bảng khác nhau qua 5 năm về định dạng `snake_case`.
  - Đồng nhất tên quốc gia: Khắc phục sự sai lệch tên (Macedonia → North Macedonia, Swaziland → Eswatini, Hong Kong S.A.R. → Hong Kong...) qua `COUNTRY_NAME_FIXES`.
  - Bổ sung mã ISO-3: Ánh xạ 100% (781/781 dòng) sang chuẩn ISO 3166-1 alpha-3 phục vụ bản đồ Choropleth thế giới.
  - Xử lý thiếu dữ liệu có căn cứ thực nghiệm: Quyết định loại bỏ mẫu duy nhất của UAE năm 2018 (do khuyết hoàn toàn chỉ số `corruption_perception`) thay vì điền giá trị trung bình/KNN, đảm bảo ma trận số không bị nhiễu; giữ lại 781 dòng sạch hoàn hảo.
  - Loại bỏ các cột sai số mẫu khảo sát: Loại bỏ `Standard Error`, `Whisker.high`, `Whisker.low`, `CI` vì chỉ phản ánh sai số khảo sát mẫu.
  - Chuẩn hóa thang đo: Áp dụng Min-Max Scaling đưa toàn bộ 6 thuộc tính về miền $[0, 1]$, bảo toàn tính bị chặn tự nhiên của dữ liệu WHR.
  - **Quy tắc vàng:** Tuyệt đối không đưa `happiness_score` vào ma trận gom cụm $X$.
- **Minh chứng định lượng:**
  - Module tiền xử lý: `src/data/data_loader.py` (hàm `build_interim_dataset()`, `standardize_columns()`, `harmonize_country_names()`).
  - Dữ liệu trung gian sạch: `data/interim/happiness_merged.csv` (781 dòng, đúng 13 cột, 0 missing).
  - Kiểm thử máy sạch tự động: `scripts/audit_day27_clean_pipeline.py` (Tầng 1: 8/8 check PASS).
  - Slide thuyết trình: Slide 3 (Kiến trúc Pipeline 11 bước), Slide 4 (Quy trình Tiền xử lý dữ liệu 5 năm).

---

### Tiêu chí 3: Phương pháp khai thác dữ liệu & Thuật toán From-scratch (1,50 điểm — Huỳnh Tâm Trí phụ trách)
- **Yêu cầu đề cương:** Mô tả đúng thuật toán; cài đặt/chạy đúng; lựa chọn tham số có cơ sở; đáp ứng yêu cầu so sánh phương án; không dùng hàm black-box có sẵn làm kết quả chính.
- **Hiện trạng đồ án:**
  - Tự cài đặt 100% From-scratch bằng `numpy`:
    - Thuật toán K-Means (`SimpleKMeans`): Cơ chế khởi tạo tâm K-Means++, vòng lặp cập nhật trọng tâm, tiêu chí dừng tolerance và giới hạn số vòng lặp `max_iter`.
    - Phân cấp tích tụ (`SimpleHierarchicalClustering`): Tiêu chí liên kết Ward tối thiểu hóa gia tăng phương sai nội cụm $\Delta WSS$ sau mỗi bước gộp.
    - Thuật toán mật độ (`SimpleDBSCAN`): Định nghĩa điểm lõi (core point), lân cận $\epsilon$, điểm biên (border) và điểm nhiễu ($\text{noise} = -1$).
    - Độ đo đánh giá tự code: Khoảng cách Euclid, Silhouette Score (`calculate_silhouette_score_simple`), Davies-Bouldin (`calculate_davies_bouldin_score_simple`), Calinski-Harabasz (`calculate_calinski_harabasz_score_simple`), Adjusted Rand Index (`calculate_adjusted_rand_index`).
    - Giảm chiều dữ liệu PCA tự code (`SimplePCA`): Ma trận hiệp phương sai, trị riêng, vector riêng, tỷ lệ phương sai giải thích.
  - Khảo sát tham số: Quét $k \in [2, 10]$ cho K-Means và Hierarchical; quét lưới $\epsilon \in [0.2, 0.6]$, $\text{MinPts} \in [3, 6]$ cho DBSCAN.
- **Minh chứng định lượng:**
  - Mã nguồn thuật toán: `src/models/clustering.py`, `src/features/feature_engineering.py`.
  - Script kiểm chứng toán học: `scripts/verify_scratch_implementations.py` (100% test PASS, sai số so với công thức toán $\le 10^{-10}$, ARI so với chuẩn $\text{ARI} = 1.000000$).
  - Bảng khảo sát tham số: `reports/tables/k_sensitivity_by_year.csv` (40 dòng), `reports/tables/dbscan_sweep.csv` (60 dòng).
  - Slide thuyết trình: Slide 5 (Cơ sở toán học From-scratch), Slide 6 (K-Means), Slide 7 (Ward Hierarchical), Slide 8 (DBSCAN).

---

### Tiêu chí 4: Thực nghiệm và đánh giá đa độ đo (1,50 điểm)
- **Yêu cầu đề cương:** Thí nghiệm có cấu trúc; dùng metric phù hợp; bảng/biểu đồ rõ; phân tích ảnh hưởng tham số và so sánh thuật toán/cấu hình.
- **Hiện trạng đồ án:**
  - Đánh giá đa chiều qua 4 độ đo nội tại: Silhouette Score (độ gắn kết nội cụm vs phân tách ngoại cụm), Davies-Bouldin Index (càng nhỏ càng tốt), Calinski-Harabasz Index (tỷ số phương sai), Inertia / WCSS (phương pháp Elbow).
  - Xác định số cụm tối ưu: Cả Elbow và Silhouette đều đồng thuận $k^* = 3$ là cấu hình tối ưu trên toàn bộ 5 năm (2015–2019), với Silhouette trung bình đạt $0.34 - 0.38$.
  - So sánh mô hình toàn diện: So sánh K-Means, Hierarchical (Ward) và DBSCAN trên từng năm và tổng hợp 5 năm. Chứng minh K-Means và Ward có độ tương đồng cực cao ($\text{ARI} > 0.82$), trong khi DBSCAN bị phân mảnh do dữ liệu phân bố liên tục trong không gian 6 chiều.
  - Phân tích độ ổn định (Clustering Stability): Đo lường ARI liên năm giữa các cụm sau khi ghép nối tham lam tâm cụm (`match_clusters_greedy`), khẳng định cấu trúc 3 cụm bền vững qua thời gian.
- **Minh chứng định lượng:**
  - Bảng số liệu: `reports/tables/model_comparison_metrics_by_year.csv` (25 dòng), `reports/tables/stability_ari.csv` (25 dòng), `reports/tables/contrast_k3_by_year.csv` (10 dòng).
  - Biểu đồ minh chứng: `reports/figures/elbow_silhouette_kmeans.png`, `reports/figures/model_comparison_barplot.png`, `reports/figures/pca_clusters_2019.png`.
  - Slide thuyết trình: Slide 9 (Thực nghiệm lựa chọn số cụm), Slide 10 (So sánh K-Means vs Ward vs DBSCAN), Slide 11 (Kiểm chứng ổn định liên năm ARI).

---

### Tiêu chí 5: Diễn giải kết quả và insight kinh tế - xã hội (1,00 điểm — Ngô Quang Trung phụ trách)
- **Yêu cầu đề cương:** Chọn kết quả tiêu biểu, giải thích cluster profile, rút ra nhận xét có ý nghĩa và không suy diễn quá mức dữ liệu; hậu kiểm bằng biến mục tiêu.
- **Hiện trạng đồ án:**
  - Xây dựng Chân dung 3 cụm phát triển toàn cầu:
    - **Cụm 0 — "Nhóm phát triển toàn diện & Hạnh phúc cao"** (Tây Âu, Bắc Mỹ, Úc/NZ): Điểm hạnh phúc trung bình $\approx 6.9 - 7.1$. Nổi trội vượt bậc về GDP per capita, Hỗ trợ xã hội, Tuổi thọ khỏe mạnh và Niềm tin thể chế.
    - **Cụm 1 — "Nhóm đang phát triển & Tiềm năng bứt phá"** (Đông Âu, Mỹ Latinh, Đông Á): Điểm hạnh phúc trung bình $\approx 5.3 - 5.5$. Kinh tế và y tế ở mức khá, tự do lựa chọn cao nhưng niềm tin thể chế còn thấp.
    - **Cụm 2 — "Nhóm khó khăn & Kém phát triển"** (Châu Phi hạ Sahara, Nam Á): Điểm hạnh phúc trung bình $\approx 4.0 - 4.3$. Trầm trọng thiếu hụt GDP, y tế và hỗ trợ xã hội.
  - Hậu kiểm bằng `Happiness Score` (Bước 9): Dù không dùng điểm hạnh phúc để gom cụm, ANOVA một nhân tố khẳng định sự khác biệt có ý nghĩa thống kê giữa 3 cụm ($p\text{-value} < 10^{-15}$).
  - Phân tích dịch chuyển cụm (Cluster Shifts 2015–2019): Theo dõi 156 quốc gia qua 5 năm; phát hiện sự thăng hạng bền vững của các quốc gia Đông Âu (Benin, Ivory Coast) và sự tụt hạng của Venezuela do khủng hoảng kinh tế.
- **Minh chứng định lượng:**
  - Dữ liệu dịch chuyển: `data/processed/country_cluster_shift.csv` (đủ 156 quốc gia, 0 trùng lặp).
  - Bảng xu hướng cụm: `reports/tables/cluster_trends.csv` (15 dòng), `reports/tables/cross_year_matching.csv` (12 dòng).
  - Biểu đồ: `reports/figures/radar_chart_clusters.png`, `reports/figures/cluster_shift_sankey_or_summary.png`.
  - Slide thuyết trình: Slide 12 (Chân dung 3 cụm phát triển), Slide 13 (Phân tích dịch chuyển 156 quốc gia).

---

### Tiêu chí 6: Chất lượng báo cáo và khả năng tái lập (0,50 điểm — Hà Mạnh Trường phụ trách)
- **Yêu cầu đề cương:** Bố cục khoa học; hình/bảng có tên; trích dẫn nguồn; mã nguồn/README rõ; có bảng phân công công việc; văn phong và trình bày tốt.
- **Hiện trạng đồ án:**
  - Báo cáo Word [`Nhom12_BaoCao.docx`](./Nhom12_BaoCao.docx):
    - Đủ 5 chương theo cấu trúc đề cương, độ dài ~50 trang.
    - Trình bày chuẩn in ấn: Times New Roman 13pt, giãn dòng 1.5 lines, lề chuẩn 3-2-3-3cm.
    - Phân cấp tiêu đề chuẩn (Heading 1 IN HOA ĐẬM, Heading 2 Thường Đậm, Heading 3 Nghiêng).
    - Trang bìa có khung viền hoa văn (pgBorders) chuẩn đồ án tốt nghiệp/môn học.
    - Bảng biểu và hình ảnh đều có đánh số tự động và trích dẫn nguồn gốc tệp dữ liệu.
    - Công thức toán học định dạng OMML sắc nét.
  - Khả năng tái lập:
    - 100% đường dẫn là tương đối (`Path(__file__).resolve().parents[...]`).
    - Script kiểm thử tự động `scripts/audit_day27_clean_pipeline.py` chạy sạch 54/54 tiêu chí.
    - Quản trị Git: Commit Tiếng Việt thuần người thật, không dấu hiệu AI, tệp `.gitignore` chuẩn.
- **Minh chứng định lượng:**
  - Tệp Word: `reports/final_report/Nhom12_BaoCao.docx` (4.43 MB).
  - Tệp PDF: `reports/final_report/Nhom12_BaoCao.pdf` (1.38 MB).
  - Hướng dẫn thực thi: `README.md`, `requirements.txt`.
  - Log kiểm toán: `logs/audit_day27_clean_pipeline.log`.

---

### Tiêu chí 7: Trình bày vấn đề và pipeline báo cáo (0,50 điểm — Hà Mạnh Trường mở đầu)
- **Yêu cầu đề cương:** Trình bày mạch lạc, đúng trọng tâm; thể hiện được tiến trình từ dữ liệu đến tri thức; tuân thủ thời gian quy định.
- **Hiện trạng đồ án:**
  - Cấu trúc slide chuẩn 17 slide widescreen 16:9, màu sắc công nghệ chuyên nghiệp (Navy/Teal/Slate).
  - Bố cục 3 phần rõ ràng, khớp đúng phân công 3 thành viên:
    - Phần 1 (Hà Mạnh Trường, 3.5 phút): Tổng quan, Kiến trúc 11 bước, Thu thập & Tiền xử lý dữ liệu 5 năm.
    - Phần 2 (Huỳnh Tâm Trí, 4.5 phút): Cơ sở toán học From-scratch, K-Means/Ward/DBSCAN, Thực nghiệm Elbow/Silhouette, So sánh đa độ đo.
    - Phần 3 (Ngô Quang Trung, 4.0 phút): Insight 3 cụm, Dịch chuyển cụm, Demo Streamlit 4 tab, Hạn chế & Kết luận.
  - Tổng thời lượng thuyết minh: 12 phút (đúng trần quy định tối đa của đề cương).
- **Minh chứng định lượng:**
  - Tệp slide: `reports/presentation/Nhom12_BaoCao_Slides.pptx` (17 slide, tỷ lệ 16:9).
  - Đề cương slide: `reports/presentation/slides.md`.

---

### Tiêu chí 8: Demo sản phẩm Streamlit tương tác (1,50 điểm — Ngô Quang Trung phụ trách)
- **Yêu cầu đề cương:** Demo chạy được; thể hiện đúng kết quả khai thác; người xem có thể tương tác/chọn điều kiện; xử lý tình huống cơ bản.
- **Hiện trạng đồ án:**
  - Ứng dụng Streamlit [`app/app.py`](file:///C:/Users/xpaga/Documents/data_mining/app/app.py) chạy mượt mà, độc lập trên máy cục bộ bằng lệnh `streamlit run app/app.py`.
  - Thiết kế 4 Tab chức năng hoàn chỉnh:
    - **Tab 1 — Tổng quan cụm & Radar Chart:** Lọc theo năm (2015–2019) và thuật toán (K-Means/Ward); hiển thị biểu đồ Radar đa chiều 6 thuộc tính và bảng tóm tắt chỉ số trung bình.
    - **Tab 2 — Bản đồ thế giới:** Bản đồ Choropleth tương tác toàn cầu, tô màu trực quan 156 quốc gia theo cụm, hover xem thông tin chi tiết từng nước.
    - **Tab 3 — Tra cứu quốc gia & Phân tích dịch chuyển:** Tra cứu lịch sử cụm của một quốc gia qua 5 năm, biểu đồ đường biến thiên chỉ số và phân tích xu hướng dịch chuyển.
    - **Tab 4 — Thử nghiệm gán nhãn (What-if Prediction):** 6 thanh trượt tương tác cho phép người dùng nhập chỉ số kinh tế - xã hội giả lập và hệ thống lập tức dự báo cụm gần nhất dựa trên khoảng cách Euclid tới tâm cụm.
  - Tối ưu hóa hiệu năng: Toàn bộ hàm nạp dữ liệu được bọc `@st.cache_data`, thời gian tải lại trang < 0.2 giây.
- **Minh chứng định lượng:**
  - Mã nguồn: `app/app.py`.
  - Hình ảnh giao diện: `reports/figures/demo_app_overview.png`.
  - Kiểm thử giao diện: `scripts/audit_m4_app_and_slides.py` (PASS 100%).

---

### Tiêu chí 9: Giải thích kết quả và công thức kỹ thuật (1,00 điểm — Huỳnh Tâm Trí phụ trách)
- **Yêu cầu đề cương:** Giải thích được thuật toán, tham số, metric, luật kết hợp hoặc profile cụm bằng ngôn ngữ rõ ràng, am hiểu toán học.
- **Hiện trạng đồ án:**
  - Trình bày sáng rõ bản chất toán học của các thuật toán:
    - Hàm mục tiêu K-Means: $J = \sum_{j=1}^k \sum_{x \in C_j} \lVert x - \mu_j \rVert^2$.
    - Cơ chế chọn tâm K-Means++ theo phân phối xác suất $P(x) = \frac{D(x)^2}{\sum D(x')^2}$.
    - Độ tăng phương sai liên kết Ward: $\Delta \text{WSS}(A, B) = \frac{n_A n_B}{n_A + n_B} \lVert \mu_A - \mu_B \rVert^2$.
    - Công thức hệ số Silhouette từng điểm: $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$.
  - Giải thích bản chất vì sao $k=3$ là tối ưu trên khía cạnh cân bằng giữa phương sai nội cụm và khả năng diễn giải chính sách thực tế.
- **Minh chứng định lượng:**
  - Báo cáo Word: Chương 3 (Mục 3.1 & 3.2).
  - Slide thuyết trình: Slide 5, 6, 7, 9.
  - Script đối chứng: `scripts/verify_scratch_implementations.py`.

---

### Tiêu chí 10: Trả lời câu hỏi vấn đáp và phối hợp nhóm (1,00 điểm — Cả 3 thành viên)
- **Yêu cầu đề cương:** Cả nhóm hiểu bài; trả lời đúng và có lập luận; phân chia trình bày hợp lý, đúng thời gian, các thành viên đều tham gia và làm chủ phần việc.
- **Hiện trạng đồ án:**
  - Bảng phân công công việc minh bạch: Tỷ lệ đóng góp đồng đều 33.3% — 33.3% — 33.4% cho 3 thành viên (`reports/final_report/phan_cong_cong_viec.md`).
  - Chuẩn bị cẩm nang vấn đáp toàn diện: Bộ tài liệu hỏi đáp 30 câu hỏi chuyên sâu tại [`reports/final_report/q_and_a.md`](file:///C:/Users/xpaga/Documents/data_mining/reports/final_report/q_and_a.md) và tài liệu vấn đáp cá nhân cho Hà Mạnh Trường [`reports/rehearsal_qa_ha_manh_truong.md`](./rehearsal_qa_ha_manh_truong.md).
  - Phản biện chéo nội bộ (Cross-defense): Hà Mạnh Trường nắm vững cơ sở toán học của Trí và ứng dụng Demo của Trung; Trí và Trung nắm chắc lý do tiền xử lý và xử lý dữ liệu khuyết thiếu của Trường.
- **Minh chứng định lượng:**
  - Tài liệu phân công: `reports/final_report/phan_cong_cong_viec.md`.
  - Bộ Q&A đồ án: `reports/final_report/q_and_a.md`.
  - Tài liệu vấn đáp cá nhân: `reports/rehearsal_qa_ha_manh_truong.md`.

---

## III. CHECKLIST BÀN GIAO TRƯỚC KHI ĐÓNG GÓI NỘP BÀI (NGÀY 28)

- [x] **1.** Dữ liệu thô 5 năm (2015–2019) đặt đúng tại `data/raw/*.csv`.
- [x] **2.** Dữ liệu trung gian chuẩn `data/interim/happiness_merged.csv` đủ 781 dòng, 0 khuyết thiếu ở 6 đặc trưng.
- [x] **3.** Dữ liệu dịch chuyển cụm `data/processed/country_cluster_shift.csv` đủ 156 quốc gia.
- [x] **4.** Cả 4 Jupyter Notebooks chạy sạch không lỗi từ đầu đến cuối (`01` đến `04`).
- [x] **5.** Các thuật toán From-scratch vượt qua toàn bộ các bài test toán học độc lập (`verify_scratch_implementations.py`).
- [x] **6.** Ứng dụng Streamlit [`app/app.py`](file:///C:/Users/xpaga/Documents/data_mining/app/app.py) chạy mượt mà với 4 Tabs chức năng.
- [x] **7.** 8 bảng số liệu `reports/tables/*.csv` và 17 hình ảnh `reports/figures/*.png` đầy đủ, sắc nét $\ge 300$ DPI.
- [x] **8.** Báo cáo Word [`Nhom12_BaoCao.docx`](./Nhom12_BaoCao.docx) đủ 5 chương, chuẩn in ấn Times New Roman 13pt, lề 3-2-3-3cm, kèm bản xuất bản PDF.
- [x] **9.** Bộ Slide trình chiếu [`reports/presentation/Nhom12_BaoCao_Slides.pptx`](../presentation/Nhom12_BaoCao_Slides.pptx) chuẩn 17 slide 16:9, nhúng hình ảnh thực chứng.
- [x] **10.** Script kiểm toán máy sạch `scripts/audit_day27_clean_pipeline.py` đạt 54/54 tiêu chí PASS (100%).

---
*Biên bản nghiệm thu hoàn tất vào Ngày 27 — Sẵn sàng cho Ngày 28 ráp video thuyết trình và đóng gói tệp nộp bài `Nhom12_WorldHappinessClustering.zip`.*

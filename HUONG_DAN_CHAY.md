# HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY ĐỒ ÁN KHAI THÁC DỮ LIỆU
## ĐỀ TÀI 16: PHÂN NHÓM QUỐC GIA THEO CÁC YẾU TỐ HẠNH PHÚC (WORLD HAPPINESS REPORT 2015–2019)

---

### THÔNG TIN ĐỒ ÁN VÀ THÀNH VIÊN THỰC HIỆN (NHÓM 12)
* **Học phần:** Khai thác dữ liệu (Data Mining) — Ngành Khoa học dữ liệu (Data Science)
* **Giảng viên hướng dẫn:** Bộ môn Khoa học dữ liệu
* **Danh sách sinh viên thực hiện (Nhóm 12):**
  1. **Hà Mạnh Trường** (MSSV: 2045240326) — Nhóm trưởng (Phụ trách Tổng quan, Tiền xử lý dữ liệu & Báo cáo)
  2. **Huỳnh Tâm Trí** (MSSV: 2045240315) — Thành viên (Phụ trách Thuật toán From-scratch & Thực nghiệm)
  3. **Ngô Quang Trung** (MSSV: 2045240325) — Thành viên (Phụ trách Diễn giải tri thức, Theo dõi dịch chuyển & Demo Streamlit)

---

### 1. CẤU TRÚC GÓI NỘP BÀI (`Nhom12_WorldHappinessClustering.rar`)

Gói nộp bài hoàn chỉnh của nhóm bao gồm:
1. **`Ma_nguon/`**: Thư mục chứa toàn bộ mã nguồn khép kín của đồ án:
   - `app/app.py`: Mã nguồn ứng dụng web phân tích tương tác Streamlit 4 tab.
   - `data/`: Dữ liệu thô 5 năm (`data/raw/`) và dữ liệu trung gian sạch 781 bản ghi (`data/interim/happiness_merged.csv`).
   - `notebooks/`: 4 tệp Jupyter Notebooks chuẩn hóa theo 11 bước pipeline nghiên cứu (có thể *Run All* từ đầu đến cuối không lỗi).
   - `src/`: Thư viện thuật toán tự cài đặt (*from-scratch*) bằng `NumPy`/`Pandas` (K-Means, Ward, DBSCAN, PCA, Silhouette, Davies-Bouldin, Calinski-Harabasz, ARI) và thư viện tiền xử lý, trực quan hóa.
   - `models/`: Trọng số tâm cụm và scaler lưu dạng JSON.
   - `reports/`: Bảng số liệu thực nghiệm (`reports/tables/`), biểu đồ khoa học 300 DPI (`reports/figures/`) và tài liệu phân tích.
   - `scripts/`: Kịch bản kiểm tra môi trường, đối chứng thuật toán và kiểm thử máy sạch toàn diện.
   - `logs/`: Nhật ký kiểm định chất lượng các mốc thực nghiệm đạt chuẩn 100% PASS.
   - `requirements.txt`: Danh sách thư viện phụ thuộc.
   - `README.md` & `LICENSE`: Tài liệu dự án và giấy phép mã nguồn mở MIT.
2. **`Nhom12_BaoCao.docx`**: Toàn văn Báo cáo đồ án khoa học hoàn chỉnh 5 Chương được biên soạn chuẩn hình thức Times New Roman 13pt, lề 3-2-3-3 cm, giãn dòng 1.5 lines, số liệu khớp 100% với thực nghiệm.
3. **`Nhom12_BaoCao.pdf`**: Bản xuất bản định dạng PDF chất lượng cao giúp Thầy/Cô mở đọc nhanh chóng, chuẩn định dạng và hình ảnh sắc nét.
4. **`Nhom12_BaoCao_Slides.pptx`**: Bộ slide thuyết trình 17 trang định dạng Widescreen 16:9, tích hợp hình ảnh chụp thực chứng và kịch bản phân công thuyết trình rành mạch của từng thành viên (thời lượng $\le$ 12 phút).
5. **`HUONG_DAN_CHAY.md`**: Bản hướng dẫn chi tiết quy trình thiết lập môi trường và vận hành các thành phần của đồ án.

---

### 2. YÊU CẦU MÔI TRƯỜNG & HƯỚNG DẪN CÀI ĐẶT

* **Yêu cầu hệ thống:** Python phiên bản `3.10`, `3.11` hoặc `3.12` (Khuyến nghị sử dụng Python 3.11 hoặc 3.12 trên hệ điều hành Windows, Linux hoặc macOS).
* **Quy trình thiết lập môi trường trong thư mục `Ma_nguon/`:**

#### Bước 1: Mở Terminal và di chuyển vào thư mục mã nguồn
```bash
cd Ma_nguon
```

#### Bước 2: Tạo môi trường ảo (Virtual Environment)
* Trên hệ điều hành Windows (Command Prompt hoặc PowerShell):
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
* Trên hệ điều hành macOS / Linux:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

#### Bước 3: Cài đặt toàn bộ thư viện phụ thuộc
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*(Các thư viện chính bao gồm: `numpy`, `pandas`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `streamlit`, `plotly`, `openpyxl`, `jupyter`, `pypdf`, `python-docx`, `python-pptx`)*.

---

### 3. HƯỚNG DẪN KHỞI CHẠY CÁC THÀNH PHẦN CHÍNH

#### 3.1. Kiểm tra nhanh môi trường cài đặt
Trước khi vận hành, chạy script sau để kiểm tra tính sẵn sàng của môi trường, phiên bản Python và các thư viện:
```bash
python scripts/check_environment.py
```
*Kết quả kỳ vọng: 100% các mục kiểm tra hiển thị trạng thái `PASS` và kết luận `môi trường đạt chuẩn`.*

#### 3.2. Chạy kiểm chứng tính đúng đắn của Thuật toán From-scratch
Nhóm đã tự lập trình 100% các thuật toán `SimpleKMeans`, `SimpleHierarchicalClustering` (Ward Lance-Williams), `SimpleDBSCAN`, `SimplePCA` và các độ đo đánh giá (`Silhouette`, `Davies-Bouldin`, `Calinski-Harabasz`, `ARI`). Để đối chứng trực tiếp với thư viện chuẩn `scikit-learn` và `scipy`:
```bash
python scripts/verify_scratch_implementations.py
```
*Kết quả đầu ra sẽ xác nhận 100% bài test PASS với sai số số học $\le 10^{-12}$ và chỉ số tương đồng $\text{ARI} = 1.000000$.*

#### 3.3. Kiểm thử toàn diện Pipeline trên máy sạch (54/54 tiêu chí)
Để kiểm tra tính toàn vẹn khép kín của toàn bộ đồ án (từ dữ liệu thô, 4 notebook, thuật toán from-scratch, ứng dụng Streamlit, biểu đồ 300 DPI, văn bản Word/PDF đến bộ Slide PowerPoint):
```bash
python scripts/audit_day27_clean_pipeline.py
```
*Kết quả kỳ vọng: `TỔNG KẾT KIỂM THỬ MÁY SẠCH NGÀY 27: 54/54 TIÊU CHÍ PASS (100.0%)`.*

#### 3.4. Khởi chạy Ứng dụng Demo tương tác Streamlit (Tab Demo sản phẩm)
Ứng dụng tương tác được xây dựng hoàn chỉnh với 4 tab chuyên sâu phục vụ khai phá và diễn giải tri thức:
```bash
streamlit run app/app.py
```
*Sau khi chạy lệnh, trình duyệt web sẽ tự động mở tại địa chỉ `http://localhost:8501`*.
* **Tab 1 — Tổng quan cụm & Radar Chart:** Tùy chọn xem từng năm (2015–2019) hoặc thuật toán (K-Means/Ward); xem thẻ KPI (Silhouette, DB, CH) và biểu đồ mạng nhện 6 chiều.
* **Tab 2 — Bản đồ thế giới:** Bản đồ Choropleth tương tác toàn cầu phân bố 156 quốc gia theo chuẩn mã địa lý ISO-3.
* **Tab 3 — Tra cứu quốc gia:** Tra cứu chi tiết 156 quốc gia (ví dụ: Việt Nam) để xem lịch sử gán nhãn cụm và xu hướng biến thiên 6 chỉ số qua nửa thập kỷ.
* **Tab 4 — Thử nghiệm gán nhãn giả định (What-if Prediction):** Kéo 6 thanh trượt chỉ số, hệ thống tự động chuẩn hóa Z-score và gán cụm thời gian thực theo khoảng cách Euclid trong thời gian dưới 0.1 giây.

#### 3.5. Khởi chạy và thực thi 4 Jupyter Notebooks
Quy trình 11 bước của đồ án được đóng gói rành mạch qua 4 tệp notebook có thể chạy lại từ đầu đến cuối (*Run All*):
```bash
jupyter notebook notebooks/
```
* **`notebooks/01_data_understanding_and_cleaning.ipynb`**: Nạp 5 năm dữ liệu thô (782 mẫu), xử lý dị biệt schema, loại mẫu khuyết UAE 2018, chuẩn hóa danh pháp địa lý ISO-3 và xuất tệp dữ liệu trung gian sạch 100% `data/interim/happiness_merged.csv` (781 bản ghi).
* **`notebooks/02_exploratory_data_analysis.ipynb`**: Phân tích thống kê mô tả, phân tích độ lệch skewness, ma trận tương quan và minh chứng cơ sở khoa học lựa chọn chuẩn hóa Z-score.
* **`notebooks/03_clustering_experiments_and_comparison.ipynb`**: Khảo sát độ nhạy tham số $k \in [2, 9]$ bằng Elbow và Silhouette, thẩm định số cụm tối ưu $k^* = 3$ đồng thuận cả 5 năm, thực nghiệm đối chứng K-Means vs Ward vs DBSCAN và kiểm định độ ổn định qua 10 Random Seeds (ARI đạt 0.98 – 1.00).
* **`notebooks/04_cluster_profiling_and_evaluation.ipynb`**: Xây dựng chân dung 3 cụm kinh tế - xã hội, hậu kiểm độc lập với điểm hạnh phúc thực tế qua ANOVA ($F > 107$, $p\text{-value} < 10^{-15}$), và thuật toán ghép cụm tham lam theo dõi dịch chuyển 156 quốc gia qua 5 năm.

---

### 4. BẢO ĐẢM TÍNH TÁI LẬP (REPRODUCIBILITY)
* **Quy tắc vàng:** Điểm số hạnh phúc (`happiness_score`) và thứ hạng (`happiness_rank`) **tuyệt đối không tham gia vào ma trận gom cụm $X$**, chỉ dùng ở bước hậu kiểm độc lập tại Notebook 04 và ứng dụng web.
* **Độc lập môi trường:** Mọi đường dẫn trong mã nguồn dự án đều sử dụng đường dẫn tương đối phân giải động qua thư viện `pathlib.Path`, bảo đảm đồ án có thể chạy trơn tru ngay lập tức trên máy của Thầy/Cô mà không yêu cầu chỉnh sửa thủ công bất kỳ cấu hình hay đường dẫn tuyệt đối nào.

# World Happiness Clustering — Phân Nhóm Quốc Gia Theo Các Yếu Tố Hạnh Phúc Toàn Cầu

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Algorithms](https://img.shields.io/badge/Algorithms-From--Scratch%20(NumPy%2FPandas)-00599C?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Verification](https://img.shields.io/badge/Verification-100%25%20PASS%20vs%20sklearn-success?style=for-the-badge&logo=checkmarx&logoColor=white)](scripts/verify_scratch_implementations.py)
[![License](https://img.shields.io/badge/License-MIT-blue.style=for-the-badge)](LICENSE)

**Hệ thống khai phá dữ liệu đa chiều và học máy không giám sát (Unsupervised Learning) phân tích động thái phát triển và phân tầng chất lượng sống của các quốc gia trên thế giới qua dữ liệu World Happiness Report (2015 – 2019).**

> 📺 **Video thuyết trình báo cáo (YouTube, ≤ 12 phút):** [https://youtu.be/YbmrPYctDg0?si=w0s5sPbvQadSknc6](https://youtu.be/YbmrPYctDg0?si=w0s5sPbvQadSknc6)

[Khởi động nhanh](#cài-đặt--khởi-động-nhanh) • [Tính năng cốt lõi](#tính-năng-nổi-bật) • [Kiến trúc thuật toán](#kiến-trúc-thuật-toán-from-scratch) • [Kết quả thực nghiệm](#kết-quả-thực-nghiệm--phát-hiện-chính) • [Ứng dụng tương tác](#ứng-dụng-demo-tương-tác-streamlit)

</div>

---

## Mục Lục

- [Giới thiệu](#giới-thiệu)
- [Nguyên tắc cốt lõi: Zero Data Leakage](#nguyên-tắc-cốt-lõi-zero-data-leakage)
- [Tính năng nổi bật](#tính-năng-nổi-bật)
- [Kiến trúc thuật toán (From-Scratch)](#kiến-trúc-thuật-toán-from-scratch)
- [Cấu trúc mã nguồn](#cấu-trúc-mã-nguồn)
- [Cài đặt & Khởi động nhanh](#cài-đặt--khởi-động-nhanh)
- [Quy trình thực thi Pipeline](#quy-trình-thực-thi-pipeline)
- [Kết quả thực nghiệm & Phát hiện chính](#kết-quả-thực-nghiệm--phát-hiện-chính)
- [Ứng dụng demo tương tác (Streamlit)](#ứng-dụng-demo-tương-tác-streamlit)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Đóng góp & Phát triển](#đóng-góp--phát-triển)
- [Giấy phép (License)](#giấy-phép-license)

---

## Giới Thiệu

Dự án **World Happiness Clustering** tập trung giải quyết bài toán phân nhóm các quốc gia trên thế giới dựa trên các khía cạnh kinh tế, xã hội và thể chế, sử dụng chuỗi dữ liệu 5 năm liên tục (2015 – 2019) từ [World Happiness Report (WHR)](https://worldhappiness.report/).

Mục tiêu chính của dự án:
1. **Phân tầng tự nhiên:** Nhận diện các cấu trúc nhóm quốc gia tương đồng về chất lượng sống mà không phụ thuộc vào ranh giới địa lý hành chính thuần túy.
2. **Minh bạch thuật toán (Explainable AI):** Toàn bộ các thuật toán gom cụm, thuật toán giảm chiều và bộ độ đo đánh giá đều được **tự lập trình từ nền tảng toán học (from-scratch)** bằng `NumPy` và `Pandas`, giúp giải thích tường minh từng bước tính toán.
3. **Phân tích động thái theo thời gian (Longitudinal Analysis):** Theo dõi sự dịch chuyển cụm của các quốc gia qua chuỗi thời gian 5 năm, nhận diện các quốc gia bứt phá hoặc suy thoái về năng lực an sinh.
4. **Trực quan hóa đa chiều:** Tích hợp Web Dashboard tương tác cho phép khám phá biểu đồ Radar đa chiều, bản đồ thế giới Choropleth và mô phỏng kịch bản What-if cho các quốc gia giả định theo thời gian thực.

---

## Nguyên Tắc Cốt Lõi: Zero Data Leakage

Điểm mấu chốt mang tính nguyên tắc khoa học của bài toán:

> **Quy tắc vàng:** Ma trận đặc trưng gom cụm $X$ **tuyệt đối không chứa** điểm số hạnh phúc (`Happiness Score`) hoặc thứ hạng (`Happiness Rank`).

Quá trình gom cụm hoàn toàn độc lập và chỉ dựa trên **6 yếu tố nền tảng xã hội**:
- **GDP per Capita:** Đóng góp của năng lực sản xuất và thu nhập bình quân đầu người.
- **Social Support:** Mức độ tương trợ xã hội và mạng lưới an sinh khi người dân gặp biến cố.
- **Healthy Life Expectancy:** Kỳ vọng số năm sống khỏe mạnh của người dân.
- **Freedom:** Quyền tự do lựa chọn và tự quyết định con đường cuộc sống.
- **Generosity:** Mức độ thiện nguyện và lòng hảo tâm trong cộng đồng.
- **Perceptions of Corruption:** Cảm nhận về tính minh bạch và sự liêm chính của thể chế chính quyền / doanh nghiệp.

`Happiness Score` chỉ được sử dụng ở bước **hậu kiểm (post-hoc validation)** để đối chiếu độc lập xem cấu trúc cụm hình thành tự nhiên có phản ánh đúng mức độ hạnh phúc thực tế hay không.

---

## Tính Năng Nổi Bật

- **100% Thuật toán tự phát triển:** Tự xây dựng K-Means (Lloyd's), Phân cấp Ward (Hierarchical Agglomerative), DBSCAN, PCA và 4 chỉ số đo lường chất lượng cụm không sử dụng API huấn luyện black-box.
- **Kiểm chứng số học chặt chẽ:** Tích hợp bộ kiểm thử đối chứng tự động (`scripts/verify_scratch_implementations.py`) kiểm tra tính tương đương số học với `scikit-learn` và `SciPy` (đạt chỉ số ARI = 1.0 và sai số $\le 10^{-14}$).
- **Chuẩn hóa dữ liệu liên năm:** Hợp nhất và đồng bộ danh pháp quốc gia (chuẩn hóa tên nước, mã ISO-3, xử lý khuyết thiếu cục bộ có căn cứ học thuật).
- **Phân tích dịch chuyển liên năm (Cross-Year Shift Tracking):** Thuật toán ghép cụm tối ưu khoảng cách tâm cụm liên năm (`match_clusters_greedy`) giúp bảo toàn ngữ nghĩa nhãn cụm xuyên suốt 2015 – 2019.
- **Dashboard Streamlit 4 trong 1:** Ứng dụng phân tích dữ liệu tương tác hoàn chỉnh hỗ trợ tra cứu quốc gia, biểu đồ Radar, phân tích PCA không gian 2D/3D và giả lập chỉ số phát triển What-if.
- **Độc lập môi trường (100% Reproducible):** Toàn bộ đường dẫn dữ liệu và tài nguyên đều được quản lý tương đối linh hoạt, cam kết khả năng chạy lại trơn tru trên mọi hệ điều hành.

---

## Kiến Trúc Thuật Toán (From-Scratch)

Mọi thuật toán cốt lõi trong thư mục `src/` đều được lập trình dựa trên đại số tuyến tính cơ bản:

| Thuật toán / Mô-đun | Tệp nguồn | Cơ sở toán học & Đặc tả kỹ thuật |
| :--- | :--- | :--- |
| **K-Means Clustering** | [`src/models/clustering.py`](src/models/clustering.py) | Cực tiểu hóa khoảng cách Euclid và độ biến thiên nội cụm (Inertia/WCSS), kiểm soát hội tụ tâm tự động. |
| **Ward Hierarchical** | [`src/models/clustering.py`](src/models/clustering.py) | Gom cụm phân cấp tích tụ theo tiêu chuẩn tăng phương sai tối thiểu Ward's minimum variance criterion. |
| **DBSCAN** | [`src/models/clustering.py`](src/models/clustering.py) | Gom cụm dựa trên mật độ không gian với bán kính $\varepsilon$ và số lân cận tối thiểu `min_samples`, phát hiện điểm nhiễu (noise). |
| **Simple PCA** | [`src/features/feature_engineering.py`](src/features/feature_engineering.py) | Giảm chiều dữ liệu dựa trên phân tích suy biến ma trận SVD / Ma trận hiệp phương sai, tính toán tỷ lệ phương sai giải thích. |
| **Silhouette Score** | [`src/models/clustering.py`](src/models/clustering.py) | Đánh giá độ gắn kết nội cụm $a(i)$ và độ tách biệt cụm láng giềng $b(i)$. |
| **Davies-Bouldin Index** | [`src/models/clustering.py`](src/models/clustering.py) | Tỷ số giữa độ phân tán trong cụm và khoảng cách giữa các tâm cụm (chỉ số càng nhỏ cụm càng tốt). |
| **Calinski-Harabasz** | [`src/models/clustering.py`](src/models/clustering.py) | Tỷ số giữa phương sai liên cụm và phương sai nội cụm (chỉ số càng lớn cụm càng rõ nét). |
| **Adjusted Rand Index** | [`src/models/clustering.py`](src/models/clustering.py) | Đánh giá độ ổn định và mức độ tương đồng giữa hai tập nhãn có hiệu chỉnh ngẫu nhiên. |

---

## Cấu Trúc Mã Nguồn

```text
data_mining/
├── app/
│   └── app.py                     # Ứng dụng phân tích dữ liệu tương tác Streamlit (4 Tabs)
├── data/
│   ├── raw/                       # Dữ liệu gốc WHR từng năm (2015.csv ... 2019.csv)
│   ├── interim/                   # Dữ liệu 5 năm đã làm sạch và hợp nhất (happiness_merged.csv)
│   └── processed/                 # Kết quả phân nhóm, bảng dịch chuyển cụm và ma trận đối chứng
├── logs/                          # Nhật ký kiểm định chất lượng các mốc thực nghiệm đạt chuẩn 100% PASS
├── models/                        # Tham số mô hình đã huấn luyện, tâm cụm và scaler (JSON)
├── notebooks/                     # Quy trình nghiên cứu thực nghiệm theo chuẩn Khoa học dữ liệu (4 Notebooks)
│   ├── 01_data_understanding_and_cleaning.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_clustering_experiments_and_comparison.ipynb
│   └── 04_cluster_profiling_and_evaluation.ipynb
├── reports/
│   ├── figures/                   # Biểu đồ khoa học xuất độ phân giải cao (300 DPI)
│   ├── tables/                    # Bảng thống kê định lượng và độ đo benchmark (CSV)
│   └── final_report/              # Tài liệu báo cáo phân tích chi tiết (Word / PDF)
├── scripts/
│   ├── check_environment.py              # Script kiểm tra nhanh môi trường cài đặt
│   ├── verify_scratch_implementations.py # Script kiểm chứng thuật toán From-scratch vs Scikit-Learn
│   ├── audit_day27_clean_pipeline.py     # Script kiểm thử toàn diện máy sạch 7 tầng (54/54 tiêu chí)
│   └── audit_m*.py                       # Kịch bản kiểm toán chi tiết từng mốc nghiên cứu
├── src/
│   ├── data/                      # Module tải và tiền xử lý dữ liệu
│   ├── features/                  # Module chuẩn hóa thang đo và PCA tự viết
│   ├── models/                    # Cài đặt K-Means, Ward, DBSCAN và các metrics from-scratch
│   └── visualization/             # Thư viện hàm vẽ biểu đồ trực quan hóa
├── Nhom12_BaoCao.docx             # Báo cáo đồ án khoa học hoàn chỉnh 5 Chương (file chính thức)
├── Nhom12_BaoCao.pdf              # Bản xuất bản PDF chất lượng cao (file chính thức)
├── Nhom12_BaoCao_Slides.pptx      # Slide thuyết trình 17 trang Widescreen 16:9 (file chính thức)
├── HUONG_DAN_CHAY.md              # Bản hướng dẫn chi tiết quy trình cài đặt và vận hành đồ án
├── requirements.txt               # Danh sách thư viện phụ thuộc
└── README.md                      # Tài liệu tổng quan dự án
```

---

## Cài Đặt & Khởi Động Nhanh

### 1. Yêu cầu hệ thống
- **Python:** Phiên bản `3.10`, `3.11` hoặc `3.12`.
- **Git** đã được cài đặt trên máy.

### 2. Thiết lập môi trường

```bash
# Clone repository
git clone https://github.com/your-username/world-happiness-clustering.git
cd world-happiness-clustering

# Khởi tạo môi trường ảo Python
python -m venv .venv

# Kích hoạt môi trường ảo:
# Trên Windows PowerShell:
.venv\Scripts\Activate.ps1
# Trên Linux / macOS:
source .venv/bin/activate

# Nâng cấp pip và cài đặt thư viện phụ thuộc
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Xác minh tính đúng đắn của thuật toán

Trước khi chạy pipeline, chạy script sau để kiểm thử bộ thuật toán tự cài đặt:

```bash
python scripts/verify_scratch_implementations.py
```

*Kết quả kỳ vọng: 100% bài kiểm tra hiển thị trạng thái `PASS`.*

---

## Quy Trình Thực Thi Pipeline

Dự án được cấu trúc theo chu trình nghiên cứu dữ liệu tuần tự:

```text
[Dữ liệu thô 2015-2019] 
         ↓
(01) Data Understanding & Cleaning ──> data/interim/happiness_merged.csv
         ↓
(02) Exploratory Data Analysis (EDA) ──> Khám phá tương quan, phân phối, ma trận scatter
         ↓
(03) Clustering Experiments ──────────> K-Means vs Ward vs DBSCAN (Tối ưu hóa k=3)
         ↓
(04) Cluster Profiling & Evaluation ──> Phân tích chân dung cụm & dịch chuyển liên năm
         ↓
[Streamlit Interactive Web Dashboard] ─> Trực quan hóa và mô phỏng kịch bản What-if
```

### Thứ tự thực hiện:

1. **Khám phá qua Jupyter Notebooks:**
   Mở và chạy lần lượt các notebook trong thư mục `notebooks/`:
   ```bash
   jupyter notebook notebooks/
   ```
   - `01_data_understanding_and_cleaning.ipynb`: Nạp 5 tệp dữ liệu, giải quyết bất tương thích schema, xử lý missing data và đồng bộ chuẩn hóa quốc gia.
   - `02_exploratory_data_analysis.ipynb`: Khảo sát phân phối 6 yếu tố, phân tích đa cộng tuyến (VIF), kiểm tra phân phối đơn biến / đa biến.
   - `03_clustering_experiments_and_comparison.ipynb`: Thử nghiệm Elbow method, Silhouette analysis từ $k=2$ đến $k=8$; so sánh định lượng K-Means, Ward và DBSCAN.
   - `04_cluster_profiling_and_evaluation.ipynb`: Xây dựng chân dung định tính từng cụm, hậu kiểm độc lập với `Happiness Score`, đối chiếu ma trận dịch chuyển quốc gia.

2. **Khởi chạy ứng dụng Web tương tác:**
   ```bash
   streamlit run app/app.py
   ```
   Truy cập trình duyệt tại địa chỉ mặc định: `http://localhost:8501`.

---

## Kết Quả Thực Nghiệm & Phát Hiện Chính

### 1. So sánh định lượng các thuật toán (Dữ liệu 2019)

Thực nghiệm so sánh trên cùng tập đặc trưng 6 chiều chuẩn hóa Z-score:

| Thuật toán | Số cụm ($k$) | Silhouette Score ↑ | Davies-Bouldin ↓ | Calinski-Harabasz ↑ | Inertia (WCSS) ↓ | Phân bố kích thước cụm |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **K-Means (Chọn làm chính)** | **3** | **0.3436** | **1.0703** | **86.02** | **440.58** | **28 / 82 / 46** |
| **Hierarchical Ward** | 3 | 0.3104 | 1.0019 | 68.23 | 494.75 | 16 / 105 / 35 |
| **DBSCAN** ($\varepsilon = 1.8, \text{MinPts} = 4$) | 2 (+nhiễu) | -0.0809 | 1.6489 | 1.60 | 576.89 | 121 / 3 (32 điểm nhiễu) |

> **Nhận định chuyên môn:** K-Means với $k=3$ cho chất lượng phân cụm tối ưu nhất: hệ số Silhouette cao nhất (0.344), chỉ số phương sai Calinski-Harabasz vượt trội (86.02) và kích thước các cụm có độ cân bằng cao, phản ánh chân thực các tầng nấc phát triển xã hội.

### 2. Chân dung 3 nhóm quốc gia điển hình ($k=3$)

Kết quả phân cụm tự nhiên từ 6 yếu tố kinh tế - thể chế phân hóa rõ nét khi đối chiếu với điểm hạnh phúc thực tế:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ CỤM 1: Nhóm Phát triển toàn diện (Hạnh phúc cao) — ~28 quốc gia                        │
│ • Đặc trưng: GDP bình quân đầu người cao, hệ thống an sinh xã hội vượt trội,          │
│   tuổi thọ khỏe mạnh cao nhất thế giới, niềm tin vào sự liêm chính thể chế cao.       │
│ • Quốc gia điển hình: Phần Lan, Đan Mạch, Na Uy, New Zealand, Thụy Sĩ, Canada.         │
│ • Điểm hạnh phúc trung bình thực tế: ~6.73 / 10.0                                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ CỤM 2: Nhóm Đang phát triển / Nền kinh tế chuyển dịch (Hạnh phúc khá) — ~82 quốc gia   │
│ • Đặc trưng: An sinh xã hội và tuổi thọ ở mức khá, khát vọng tự do cá nhân cao,        │
│   tuy nhiên cảm nhận về tham nhũng còn thấp và thu nhập phân hóa.                      │
│ • Quốc gia điển hình: Việt Nam, Thái Lan, Brazil, Mexico, Ba Lan, Romania.             │
│ • Điểm hạnh phúc trung bình thực tế: ~5.60 / 10.0                                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ CỤM 3: Nhóm Khó khăn & Thách thức lớn (Hạnh phúc thấp) — ~46 quốc gia                  │
│ • Đặc trưng: Nền tảng kinh tế yếu, an sinh xã hội mong manh, tuổi thọ kỳ vọng thấp,    │
│   nhiều quốc gia chịu ảnh hưởng bởi xung đột hoặc thể chế bất ổn định.                 │
│ • Quốc gia điển hình: Afghanistan, Nam Sudan, Yemen, Haiti, Rwanda.                    │
│ • Điểm hạnh phúc trung bình thực tế: ~4.26 / 10.0                                      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Động thái dịch chuyển liên năm (2015 – 2019)
- **Độ ổn định cao:** Đa số các quốc gia thuộc Cụm 1 (Bắc Âu, Tây Âu, Bắc Mỹ, Úc) và Cụm 3 (khu vực Châu Phi Hạ Sahara) duy trì vị trí ổn định qua 5 năm.
- **Biến động tại Cụm 2:** Một số quốc gia đang phát triển ghi nhận sự dịch chuyển tích cực nhờ cải thiện chỉ số tuổi thọ và dịch vụ xã hội; ngược lại, các quốc gia trải qua bất ổn chính trị hoặc siêu lạm phát (như Venezuela) bị rơi từ nhóm trung bình xuống nhóm thấp.

---

## Ứng Dụng Demo Tương Tác (Streamlit)

Ứng dụng web được tổ chức thành 4 không gian phân tích trực quan chuyên sâu:

1. **Tab 1 — Tổng quan cụm & Phân tích Radar:**
   - Trực quan hóa hình thái đa chiều của 3 cụm thông qua biểu đồ Radar (Spider Chart).
   - Biểu diễn không gian giảm chiều PCA 2D và 3D với độ tương tác xoay/phóng to thu nhỏ.
2. **Tab 2 — Bản đồ thế giới Choropleth:**
   - Bản đồ địa lý thế giới hiển thị màu sắc theo cụm của từng quốc gia theo từng năm khảo sát.
   - Hỗ trợ lọc theo khu vực địa lý và năm dữ liệu.
3. **Tab 3 — Tra cứu quốc gia & Dịch chuyển cụm:**
   - Tra cứu chi tiết từng quốc gia (thứ hạng, điểm các yếu tố, cụm qua từng năm).
   - Biểu đồ đường diễn biến chỉ số và bảng ma trận theo dõi dịch chuyển cụm (2015 – 2019).
4. **Tab 4 — Thử nghiệm What-if (Gán nhãn quốc gia mới):**
   - Cho phép người dùng tùy biến 6 thanh trượt tương ứng với 6 chỉ số kinh tế - xã hội.
   - Mô hình K-Means thời gian thực chuẩn hóa đầu vào và tự động dự đoán cụm phân loại, vẽ trực tiếp vị trí của quốc gia giả định lên biểu đồ Radar và không gian PCA.

---

## Công Nghệ Sử Dụng

- **Ngôn ngữ:** Python 3.10+
- **Thư viện tính toán lõi:** `NumPy`, `Pandas`, `SciPy`
- **Trực quan hóa:** `Plotly`, `Matplotlib`, `Seaborn`
- **Giao diện tương tác:** `Streamlit`
- **Kiểm chứng & Đánh giá:** `scikit-learn` (chỉ dùng trong script test kiểm chứng tính chính xác của thuật toán)

---

## Đóng Góp & Phát Triển

Mọi ý kiến đóng góp, báo cáo lỗi hoặc đề xuất cải tiến thuật toán luôn được chào đón:

1. Fork dự án trên GitHub.
2. Tạo nhánh tính năng mới (`git checkout -b feature/AmazingFeature`).
3. Commit các thay đổi (`git commit -m 'feat: them tinh nang phan tich moi'`).
4. Push lên nhánh của bạn (`git push origin feature/AmazingFeature`).
5. Tạo một Pull Request mô tả chi tiết nội dung đã hoàn thiện.

---

## Giấy Phép (License)

Dự án được phân phối dưới giấy phép **MIT License**. Chi tiết xem tại tệp [`LICENSE`](LICENSE).

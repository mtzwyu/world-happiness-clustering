# 🌍 Phân Nhóm Quốc Gia Theo Các Yếu Tố Tạo Nên Mức Độ Hạnh Phúc (World Happiness Report)

> **Học phần:** Khai thác dữ liệu (Data Mining)  
> **Chuyên ngành:** Khoa học dữ liệu (Data Science) - Năm 3  
> **Đề tài số:** 16  
> **Nhóm thực hiện:** Nhóm 12  

---

## 👥 Thành Viên Nhóm

| STT | Mã số SV | Họ và tên | Vai trò | Tỷ lệ đóng góp |
|:---:|:---:|:---|:---:|:---:|
| 1 | 2045240326 | **Hà Mạnh Trường** | Nhóm trưởng | 100% |
| 2 | 2045240315 | **Huỳnh Tâm Trí** | Thành viên | 100% |
| 3 | 2045240325 | **Ngô Quang Trung** | Thành viên | 100% |

---

## 📌 Giới Thiệu Đề Tài

Dự án tập trung vào việc nghiên cứu và phân nhóm các quốc gia trên thế giới dựa trên 6 trụ cột cơ bản tạo nên chất lượng cuộc sống (theo khảo sát **Gallup World Poll** và Báo cáo **World Happiness Report** từ 2015 - 2019):
1. **Kinh tế** (`GDP per Capita`)
2. **Hỗ trợ xã hội** (`Social support` / `Family`)
3. **Sức khỏe & Tuổi thọ** (`Healthy Life Expectancy`)
4. **Tự do cá nhân** (`Freedom to make life choices`)
5. **Độ hào phóng cộng đồng** (`Generosity`)
6. **Nhận thức về tham nhũng** (`Perceptions of corruption` / `Trust in government`)

> [!IMPORTANT]
> **Quy Tắc Vàng Của Đề Tài 16:**  
> Tuyệt đối **KHÔNG** đưa thuộc tính `Happiness Score` hay `Happiness Rank` vào làm đặc trưng đầu vào để gom cụm. Quá trình phân nhóm phải hoàn toàn khách quan dựa trên 6 yếu tố cơ sở; sau đó mới sử dụng `Happiness Score` để hậu kiểm và so sánh mức độ hạnh phúc giữa các cụm.

---

## 🎯 Tuân Thủ 11 Bước Pipeline Bắt Buộc (Mục 1.2 Quy Định Môn Học)

Dự án được cấu trúc để tuân thủ trọn vẹn và tường minh 11 bước trong quy trình chuẩn:

| Bước | Tên bước trong Mục 1.2 | Nơi triển khai cụ thể trong Repo |
|:---:|:---|:---|
| **1** | **Xác định bài toán & câu hỏi khai thác** | `notebooks/01_...ipynb` (Mục 1) & `README.md` |
| **2** | **Tìm hiểu dữ liệu** | `notebooks/01_...ipynb` (Mục 2) & `src/data/data_loader.py` |
| **3** | **Đánh giá chất lượng dữ liệu** | `notebooks/01_...ipynb` (Mục 3) |
| **4** | **Tiền xử lý dữ liệu** | `notebooks/01_...ipynb` & `notebooks/03_...ipynb` |
| **5** | **Khám phá dữ liệu (EDA) có mục tiêu** | `notebooks/02_...ipynb` & `reports/figures/` |
| **6** | **Biến đổi dữ liệu phù hợp thuật toán** | `notebooks/03_...ipynb` (Mục 1) & `src/features/` |
| **7** | **Thực hiện thuật toán & chọn tham số** | `notebooks/03_...ipynb` (Mục 2, 3) (Elbow, Silhouette) |
| **8** | **Đánh giá và so sánh phương án** | `notebooks/03_...ipynb` (Mục 4, 5, 6) (K-Means vs Hierarchical vs DBSCAN) |
| **9** | **Diễn giải tri thức** | `notebooks/04_...ipynb` (Mục 1, 2, 3) (Radar Chart, PCA, Hậu kiểm Score) |
| **10** | **Xây dựng sản phẩm demo** | `app/app.py` (Streamlit tương tác trực quan) |
| **11** | **Kết luận và khả năng mở rộng** | `notebooks/04_...ipynb` (Mục 4) |

---

## 🗂️ Cấu Trúc Dự Án (Project Structure)

Dự án được xây dựng theo tiêu chuẩn quốc tế **Cookiecutter Data Science** kết hợp quy trình chuẩn **CRISP-DM**, tối ưu cho việc làm việc nhóm trên GitHub và môi trường **Jupyter Notebook**:

```text
data_mining/
│
├── .gitignore                                      # Loại bỏ file tạm, checkpoint jupyter, môi trường ảo
├── README.md                                       # Tài liệu tổng quan dự án trên GitHub
├── requirements.txt                                # Danh sách thư viện Python phục vụ tái lập môi trường
│
├── data/                                           # Quản lý dữ liệu phân tầng bất biến
│   ├── raw/                                        # Dữ liệu gốc tải về (2015.csv -> 2019.csv)
│   ├── interim/                                    # Dữ liệu trung gian sau khi chuẩn hóa tên cột & merge
│   ├── processed/                                  # Dữ liệu sạch, đã scale/gán nhãn cụm sẵn sàng phân tích
│   └── Aboutdataset.md                             # Mô tả metadata và lưu ý bản quyền bộ dữ liệu
│
├── notebooks/                                      # Chuỗi Jupyter Notebooks đánh số theo quy trình phân tích
│   ├── README.md                                   # Hướng dẫn chi tiết thứ tự chạy
│   ├── 01_data_understanding_and_cleaning.ipynb    # Hiểu dữ liệu, đồng bộ hóa schema các năm, xử lý missing
│   ├── 02_exploratory_data_analysis.ipynb          # EDA phân phối, tương quan giữa các biến, phân tích outlier
│   ├── 03_clustering_experiments_and_comparison.ipynb # Thực nghiệm K-Means (Elbow, Silhouette), Hierarchical, DBSCAN
│   └── 04_cluster_profiling_and_evaluation.ipynb   # Giảm chiều PCA 2D/3D, Radar Chart profile cụm, hậu kiểm Score
│
├── src/                                            # Thư viện module Python tái sử dụng (Clean Code)
│   ├── __init__.py
│   ├── data/                                       # Script load dữ liệu & chuẩn hóa tên cột
│   │   ├── __init__.py
│   │   └── data_loader.py
│   ├── features/                                   # Script chuẩn hóa (StandardScaler, MinMaxScaler) & PCA
│   │   ├── __init__.py
│   │   └── feature_engineering.py
│   ├── models/                                     # Script thuật toán gom cụm & tính toán metrics nội tại
│   │   ├── __init__.py
│   │   └── clustering.py
│   └── visualization/                              # Hàm vẽ biểu đồ chuyên nghiệp (Radar chart, 2D PCA, Elbow)
│       ├── __init__.py
│       └── plots.py
│
├── models/                                         # Nơi lưu trữ artifact mô hình (Scaler, Centroids, Models)
│   └── .gitkeep
│
├── app/                                            # Sản phẩm tương tác trực quan (Phục vụ điểm Demo 4.0)
│   └── app.py                                      # Ứng dụng Web tương tác Streamlit
│
├── reports/                                        # Tài liệu nộp và báo cáo cuối kỳ (Phục vụ điểm Báo cáo 6.0)
│   ├── figures/                                    # Xuất đồ thị phân giải cao (300 DPI) chèn vào file Word
│   └── final_report/                               # File báo cáo Word (.docx) và Slide thuyết trình
│
└── docs/                                           # Tài liệu tham khảo, slide môn học và đề cương hướng dẫn
    ├── Slide_bai_giang/
    └── huong_dan/
```

---

## 🚀 Hướng Dẫn Cài Đặt và Sử Dụng

### 1. Khởi tạo môi trường ảo Python
Khuyến nghị sử dụng **Python 3.10+**:

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo (trên Windows PowerShell)
.venv\Scripts\Activate.ps1

# Hoặc trên Linux / macOS
source .venv/bin/activate
```

### 2. Cài đặt các thư viện cần thiết
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Thực thi chuỗi Jupyter Notebook
Khởi chạy Jupyter Notebook hoặc JupyterLab:
```bash
jupyter lab
# hoặc
jupyter notebook
```
Mở thư mục `notebooks/` và chạy tuần tự từ `01_` đến `04_`.

### 4. Khởi chạy Ứng dụng Demo Tương Tác (Streamlit)
```bash
streamlit run app/app.py
```
Sau khi chạy, ứng dụng sẽ tự động mở trên trình duyệt tại `http://localhost:8501`.

---

## 🎯 Đáp Ứng Tiêu Chí Đánh Giá Môn Học

| Tiêu chí | Trọng số | Địa điểm thể hiện trong Repository |
|:---|:---:|:---|
| **Báo cáo Word** | **6.0 điểm** | Chi tiết các phân tích trong `notebooks/`, hình ảnh chất lượng cao lưu tại `reports/figures/`, tài liệu hoàn chỉnh tại `reports/final_report/`. |
| **Demo tương tác tại lớp** | **4.0 điểm** | Giao diện tương tác Streamlit tại `app/app.py` cho phép chọn năm, thuật toán, điều chỉnh số cụm, hiển thị Radar Chart và tra cứu quốc gia. |
| **Khả năng tái lập (Reproducibility)** | Tiêu chí then chốt | `requirements.txt` cố định, `src/` module hóa sạch sẽ, đường dẫn dữ liệu dạng tương đối (Relative path) độc lập hệ điều hành. |

---

## 📚 Nguồn Dữ Liệu Tham Khảo

- Bộ dữ liệu World Happiness Report: [Kaggle Dataset](https://www.kaggle.com/datasets/synful/world-happiness-report)
- Báo cáo gốc Liên Hợp Quốc: [World Happiness Report Official Site](https://worldhappiness.report/)

# Hướng Dẫn Quy Trình Chạy Jupyter Notebooks

Thư mục này chứa chuỗi các Jupyter Notebook được thiết kế và đánh số theo đúng chuẩn **11 bước bắt buộc của một đồ án khai thác dữ liệu** (theo quy định tại **Mục 1.2** của tài liệu hướng dẫn đề tài).

---

## 📋 Bảng Đối Chiếu 11 Bước Pipeline Bắt Buộc (Mục 1.2)

| Bước | Nội dung theo yêu cầu Mục 1.2 | Vị trí triển khai trong Project | Trọng tâm thực hiện |
|:---:|:---|:---|:---|
| **1** | **Xác định bài toán và câu hỏi khai thác dữ liệu** | `notebooks/01_...ipynb` (Mục 1) & `README.md` | Bài toán gom cụm (Unsupervised), câu hỏi nghiên cứu phân hóa chất lượng sống giữa các quốc gia, quy tắc không đưa `happiness_score` vào gom cụm. |
| **2** | **Tìm hiểu dữ liệu** | `notebooks/01_...ipynb` (Mục 2) & `src/data/` | Mô tả nguồn Kaggle, kích thước dòng/cột, ý nghĩa 6 thuộc tính cơ sở, đơn vị đo, đọc dữ liệu 5 năm (2015-2019). |
| **3** | **Đánh giá chất lượng dữ liệu** | `notebooks/01_...ipynb` (Mục 3) | Kiểm tra missing values (giá trị thiếu), bản ghi trùng lặp (duplicates), sự bất đồng bộ về tên cột qua các năm. |
| **4** | **Tiền xử lý dữ liệu** | `notebooks/01_...ipynb` & `notebooks/03_...ipynb` | Chuẩn hóa tên cột về snake_case, xử lý missing, chọn 6 thuộc tính cơ sở (loại trừ score/rank), chuẩn hóa thang đo. |
| **5** | **Khám phá dữ liệu (EDA) có mục tiêu** | `notebooks/02_...ipynb` | Thống kê mô tả (mean, std, skewness), phân phối (histogram/KDE), ma trận tương quan (heatmap), phát hiện ngoại lệ (boxplot). |
| **6** | **Biến đổi dữ liệu sang biểu diễn phù hợp với thuật toán** | `notebooks/03_...ipynb` (Mục 1) & `src/features/` | Tạo ma trận đặc trưng số `X_scaled` bằng `StandardScaler`/`RobustScaler` cho thuật toán tính khoảng cách Euclidean. |
| **7** | **Thực hiện thuật toán và lựa chọn tham số** | `notebooks/03_...ipynb` (Mục 2, 3) | Khảo sát $k \in [2, 9]$ bằng Elbow (Inertia) và Silhouette Score, giải thích lý do chọn $k=3$, chạy K-Means baseline. |
| **8** | **Đánh giá và so sánh ít nhất hai phương án** | `notebooks/03_...ipynb` (Mục 4, 5, 6) | So sánh K-Means với Hierarchical Clustering (Ward linkage) và DBSCAN qua bộ chỉ số Silhouette, Davies-Bouldin, Calinski-Harabasz. |
| **9** | **Diễn giải tri thức** | `notebooks/04_...ipynb` (Mục 1, 2, 3) | Giảm chiều PCA 2D/3D trực quan hóa ranh giới cụm; vẽ biểu đồ Radar Chart profile cụm; hậu kiểm phân bố `happiness_score` giữa các cụm. |
| **10** | **Xây dựng sản phẩm demo** | `app/app.py` (Streamlit) | Giao diện web tương tác: chọn năm, chọn thuật toán, chỉnh số cụm, hiển thị Radar chart và tra cứu quốc gia. |
| **11** | **Kết luận và khả năng mở rộng** | `notebooks/04_...ipynb` (Mục 4) & `README.md` | Nêu rõ kết luận cốt lõi, hạn chế của dữ liệu Gallup Poll/Cantril Ladder, hạn chế thuật toán và đề xuất mở rộng theo chuỗi thời gian. |

---

## 🚀 Thứ Tự Thực Thi Khuyến Nghị

```text
01_data_understanding_and_cleaning.ipynb
    ↓ (sinh ra data/interim/happiness_merged.csv)
02_exploratory_data_analysis.ipynb
    ↓ (sinh ra biểu đồ EDA trong reports/figures/)
03_clustering_experiments_and_comparison.ipynb
    ↓ (thực nghiệm K-Means, Hierarchical, DBSCAN & so sánh metric)
04_cluster_profiling_and_evaluation.ipynb
    ↓ (sinh ra data/processed/final_clustered_happiness.csv & biểu đồ Radar)
streamlit run app/app.py
    ↓ (trình diễn tương tác sản phẩm demo)
```

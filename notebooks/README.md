# Hướng dẫn chạy notebook

Bốn notebook phải chạy theo đúng thứ tự, vì notebook sau đọc kết quả do notebook trước sinh ra.

| Thứ tự | Notebook | Nội dung | Kết quả sinh ra |
|:---:|:---|:---|:---|
| 1 | `01_data_understanding_and_cleaning.ipynb` | Bài toán, tìm hiểu dữ liệu, đánh giá chất lượng dữ liệu, dựng bảng trung gian 5 năm | `data/interim/happiness_merged.csv`, `reports/tables/data_quality_by_year.csv`, `reports/tables/interim_preview.csv` |
| 2 | `02_exploratory_data_analysis.ipynb` | Phân phối, tương quan và ngoại lệ của sáu yếu tố cơ sở | các hình trong `reports/figures/` |
| 3 | `03_clustering_experiments_and_comparison.ipynb` | Chuẩn hóa dữ liệu, khảo sát số cụm, chạy các cấu hình gom cụm, so sánh bằng các độ đo | bảng trong `reports/tables/`, hình trong `reports/figures/`, tham số mô hình trong `models/` |
| 4 | `04_cluster_profiling_and_evaluation.ipynb` | Chân dung từng cụm, ghép cụm giữa các năm, hậu kiểm bằng điểm hạnh phúc, kết luận | `data/processed/`, hình trong `reports/figures/` |

## Chuẩn bị môi trường

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ipykernel install --user --name world-happiness-clustering --display-name "Python (world-happiness-clustering)"
```

## Cách chạy

Mở Jupyter rồi chạy lần lượt từng notebook:

```powershell
jupyter lab
```

Hoặc chạy không cần giao diện (kết quả ghi thẳng vào notebook):

```powershell
.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace notebooks\01_data_understanding_and_cleaning.ipynb
```

## Lưu ý

- Notebook tự dò gốc repo nên chạy được dù mở từ thư mục nào.
- Nếu chưa có `data/interim/happiness_merged.csv`, phải chạy notebook 01 trước; các notebook 02-04 sẽ báo lỗi thiếu tệp.
- Biến môi trường khi chạy script có tiếng Việt trên Windows: `$env:PYTHONIOENCODING='utf-8'`.

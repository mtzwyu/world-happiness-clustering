# 0003. Mở rộng phạm vi tự cài đặt sang PCA, DBSCAN và artifact JSON

ADR 0001 mới giới hạn phạm vi tự cài đặt ở K-Means, phân cấp tích tụ và các độ đo khoảng cách Euclid, WCSS/Inertia, Silhouette. Đề tài mở rộng phạm vi đó sang **giảm chiều PCA**, thuật toán gom cụm theo mật độ **DBSCAN**, các độ đo **Davies-Bouldin, Calinski-Harabasz, Adjusted Rand Index**, và lưu tham số mô hình bằng **JSON** thay vì pickle; `scikit-learn` và `scipy` chỉ được dùng trong `scripts/verify_scratch_implementations.py` để đối chứng kết quả, tuyệt đối không xuất hiện trong notebook hay ứng dụng demo.

## Status

Accepted

## Consequences

- `apply_pca` không còn gọi `sklearn.decomposition.PCA`; notebook 02-04 và app không import `scikit-learn`.
- Tâm cụm, tham số chuẩn hóa và metric được ghi ra `models/*.json` để đọc lại, kiểm tra và giải thích được trước giảng viên, thay vì tệp nhị phân không đọc được.
- Script kiểm chứng phải có assert bất biến: ma trận đặc trưng không chứa `happiness_score` và `happiness_rank`.

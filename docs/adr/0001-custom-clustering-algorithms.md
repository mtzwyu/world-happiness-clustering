# 0001. Tự cài đặt thuật toán gom cụm From Scratch

Dự án quyết định tự cài đặt toàn bộ thuật toán gom cụm (K-Means, Hierarchical Clustering) và các hàm đánh giá (WCSS/Inertia, khoảng cách Euclidean, Silhouette Score) từ đầu bằng `numpy` và `pandas`, thay vì gọi API có sẵn từ thư viện `sklearn.cluster`. Quyết định này nhằm đáp ứng mục tiêu học tập, giúp sinh viên làm chủ bản chất toán học của thuật toán và tự tin trả lời vấn đáp khi bảo vệ đồ án.

## Status

Accepted

## Considered Options

- **Option 1: Sử dụng thư viện ngoài (`sklearn.cluster.KMeans`)**: Triển khai nhanh, tối ưu tốc độ tính toán nhưng hoạt động như một "hộp đen" (black-box), không đáp ứng được yêu cầu đánh giá năng lực cài đặt thuật toán trong môn học Khai thác dữ liệu.
- **Option 2: Tự cài đặt from-scratch (Được chọn)**: Viết rõ ràng từng bước cập nhật tâm cụm, tính khoảng cách, điều kiện dừng và độ đo Silhouette. Code có chú thích công thức toán học minh bạch.

## Consequences

- Mọi mã nguồn mô hình chính phải nằm trong thư mục `src/models/` và do dự án tự triển khai.
- Thư viện `scikit-learn` chỉ được phép sử dụng ở bước kiểm thử thứ cấp để làm đối chứng (benchmark) đánh giá độ chính xác của hàm tự viết, tuyệt đối không dùng làm kết quả chính trong báo cáo và notebook.

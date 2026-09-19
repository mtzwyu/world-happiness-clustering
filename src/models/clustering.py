"""
Các thuật toán gom cụm (K-Means, Hierarchical) và đánh giá chất lượng cụm
ĐƯỢC CÀI ĐẶT THUẦN TÚY BẰNG CÁC HÀM CƠ BẢN (VÒNG LẶP FOR, TOÁN HỌC CĂN BẢN).

Mục đích:
- Phục vụ quá trình tự học và hiểu sâu từng bước của thuật toán.
- Dễ dàng diễn giải, bảo vệ và trả lời vấn đáp trước giảng viên.
"""

import math
import random
from typing import List, Dict, Tuple, Any
import numpy as np
import pandas as pd


# ==============================================================================
# 1. HÀM TÍNH KHOẢNG CÁCH CƠ BẢN
# ==============================================================================

def euclidean_distance(point1: List[float], point2: List[float]) -> float:
    """
    Tính khoảng cách Euclidean giữa 2 điểm trong không gian d chiều:
    d(p1, p2) = sqrt( sum( (p1[i] - p2[i])^2 ) )
    Sử dụng vòng lặp for cơ bản.
    """
    sum_squared = 0.0
    for i in range(len(point1)):
        diff = point1[i] - point2[i]
        sum_squared += diff * diff
    return math.sqrt(sum_squared)


# ==============================================================================
# 2. THUẬT TOÁN K-MEANS BẰNG CÁC HÀM CƠ BẢN (FROM SCRATCH)
# ==============================================================================

class SimpleKMeans:
    """
    Thuật toán K-Means thuần túy:
    - Bước 1: Khởi tạo k tâm cụm ngẫu nhiên từ tập dữ liệu.
    - Bước 2: Duyệt từng điểm, tính khoảng cách đến từng tâm, gán vào tâm gần nhất.
    - Bước 3: Tính lại tọa độ tâm cụm bằng trung bình cộng các điểm trong cụm.
    - Bước 4: Lặp lại đến khi nhãn cụm không đổi hoặc đạt số vòng lặp tối đa.
    """
    def __init__(self, k: int = 3, max_iter: int = 100, random_state: int = 42):
        self.k = k
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = []
        self.labels = []
        self.inertia = 0.0

    def fit(self, data):
        # Chuyển dữ liệu sang danh sách các điểm (mỗi điểm là một list số)
        if isinstance(data, np.ndarray):
            points = data.tolist()
        elif hasattr(data, "values"):
            points = data.values.tolist()
        else:
            points = [list(row) for row in data]

        n_samples = len(points)
        n_features = len(points[0])

        if self.random_state is not None:
            random.seed(self.random_state)

        # Bước 1: Chọn ngẫu nhiên k vị trí điểm làm tâm cụm ban đầu
        sample_indices = random.sample(range(n_samples), self.k)
        self.centroids = [list(points[idx]) for idx in sample_indices]

        # Vòng lặp tối ưu hóa
        for iteration in range(self.max_iter):
            # Bước 2: Gán nhãn cho từng điểm vào tâm gần nhất
            new_labels = []
            for point in points:
                min_dist = float("inf")
                best_cluster = 0
                for cluster_idx in range(self.k):
                    dist = euclidean_distance(point, self.centroids[cluster_idx])
                    if dist < min_dist:
                        min_dist = dist
                        best_cluster = cluster_idx
                new_labels.append(best_cluster)

            # Kiểm tra hội tụ: nếu nhãn không đổi so với vòng lặp trước thì dừng
            if new_labels == self.labels:
                break
            self.labels = new_labels

            # Bước 3: Cập nhật lại tâm cụm
            for cluster_idx in range(self.k):
                # Gom các điểm thuộc cụm cluster_idx
                cluster_points = [points[i] for i in range(n_samples) if self.labels[i] == cluster_idx]

                if len(cluster_points) > 0:
                    new_center = []
                    for col in range(n_features):
                        # Tính trung bình cộng của từng thuộc tính
                        col_sum = sum(pt[col] for pt in cluster_points)
                        new_center.append(col_sum / len(cluster_points))
                    self.centroids[cluster_idx] = new_center
                else:
                    # Nếu cụm bị rỗng, lấy ngẫu nhiên 1 điểm gán lại
                    self.centroids[cluster_idx] = list(points[random.randint(0, n_samples - 1)])

        # Bước 4: Tính Inertia (WCSS - Tổng bình phương khoảng cách đến tâm cụm)
        total_inertia = 0.0
        for i in range(n_samples):
            assigned_center = self.centroids[self.labels[i]]
            dist = euclidean_distance(points[i], assigned_center)
            total_inertia += dist * dist
        self.inertia = total_inertia

        return self

    def predict(self, data) -> List[int]:
        """Gán nhãn cụm cho dữ liệu mới."""
        if isinstance(data, np.ndarray):
            points = data.tolist()
        elif hasattr(data, "values"):
            points = data.values.tolist()
        else:
            points = [list(row) for row in data]

        predictions = []
        for point in points:
            min_dist = float("inf")
            best_cluster = 0
            for cluster_idx in range(self.k):
                dist = euclidean_distance(point, self.centroids[cluster_idx])
                if dist < min_dist:
                    min_dist = dist
                    best_cluster = cluster_idx
            predictions.append(best_cluster)
        return predictions

    def fit_predict(self, data) -> List[int]:
        return self.fit(data).labels


# ==============================================================================
# 3. THUẬT TOÁN PHÂN CỤM PHÂN CẤP (HIERARCHICAL AGGLOMERATIVE) TỰ CODE
# ==============================================================================

class SimpleHierarchicalClustering:
    """
    Thuật toán gom cụm phân cấp tích tụ (Agglomerative Hierarchical Clustering):
    - Ban đầu coi mỗi điểm là một cụm riêng biệt (n cụm).
    - Ở mỗi bước, tìm 2 cụm có khoảng cách giữa hai tâm nhỏ nhất và hợp nhất lại.
    - Lặp lại cho đến khi số cụm giảm đúng bằng k.
    """
    def __init__(self, k: int = 3):
        self.k = k
        self.labels = []
        self.cluster_centroids = []

    def fit_predict(self, data) -> List[int]:
        if isinstance(data, np.ndarray):
            points = data.tolist()
        elif hasattr(data, "values"):
            points = data.values.tolist()
        else:
            points = [list(row) for row in data]

        n_samples = len(points)
        n_features = len(points[0])

        # Khởi tạo: mỗi cụm là một danh sách chứa các chỉ số (index) của điểm
        clusters = [[i] for i in range(n_samples)]

        def get_centroid(cluster_indices):
            center = []
            for col in range(n_features):
                col_sum = sum(points[idx][col] for idx in cluster_indices)
                center.append(col_sum / len(cluster_indices))
            return center

        # Vòng lặp hợp nhất cho đến khi chỉ còn k cụm
        while len(clusters) > self.k:
            min_dist = float("inf")
            merge_i, merge_j = -1, -1

            # Tìm 2 cụm gần nhau nhất
            for i in range(len(clusters)):
                center_i = get_centroid(clusters[i])
                for j in range(i + 1, len(clusters)):
                    center_j = get_centroid(clusters[j])
                    dist = euclidean_distance(center_i, center_j)
                    if dist < min_dist:
                        min_dist = dist
                        merge_i, merge_j = i, j

            # Hợp nhất cụm merge_j vào cụm merge_i
            clusters[merge_i].extend(clusters[merge_j])
            clusters.pop(merge_j)

        # Gán nhãn cho từng điểm ban đầu
        self.labels = [0] * n_samples
        self.cluster_centroids = []
        for cluster_id, cluster_indices in enumerate(clusters):
            self.cluster_centroids.append(get_centroid(cluster_indices))
            for idx in cluster_indices:
                self.labels[idx] = cluster_id

        return self.labels


# ==============================================================================
# 4. HÀM TÍNH HỆ SỐ SILHOUETTE SCORE TỰ CODE (CÔNG THỨC TOÁN CƠ BẢN)
# ==============================================================================

def calculate_silhouette_score_simple(data, labels: List[int]) -> float:
    """
    Tính hệ số Silhouette trung bình bằng công thức toán căn bản:
    Với mỗi điểm i trong cụm C_A:
    - a(i): Khoảng cách trung bình từ i đến tất cả các điểm khác trong cùng cụm C_A (độ kết dính).
    - b(i): Khoảng cách trung bình nhỏ nhất từ i đến các điểm trong cụm láng giềng khác (độ phân tách).
    - s(i) = (b(i) - a(i)) / max(a(i), b(i))
    Silhouette Score = trung bình s(i) của toàn bộ tập dữ liệu.
    """
    if isinstance(data, np.ndarray):
        points = data.tolist()
    elif hasattr(data, "values"):
        points = data.values.tolist()
    else:
        points = [list(row) for row in data]

    n_samples = len(points)
    unique_clusters = list(set(labels))

    if len(unique_clusters) < 2 or len(unique_clusters) >= n_samples:
        return 0.0

    silhouette_coefficients = []

    for i in range(n_samples):
        current_cluster = labels[i]

        # 1. Tính a(i): khoảng cách nội cụm
        same_cluster_indices = [idx for idx in range(n_samples) if labels[idx] == current_cluster and idx != i]
        if len(same_cluster_indices) == 0:
            a_i = 0.0
        else:
            total_dist_same = sum(euclidean_distance(points[i], points[idx]) for idx in same_cluster_indices)
            a_i = total_dist_same / len(same_cluster_indices)

        # 2. Tính b(i): khoảng cách đến cụm láng giềng gần nhất
        b_i = float("inf")
        for other_cluster in unique_clusters:
            if other_cluster == current_cluster:
                continue
            other_indices = [idx for idx in range(n_samples) if labels[idx] == other_cluster]
            if len(other_indices) > 0:
                total_dist_other = sum(euclidean_distance(points[i], points[idx]) for idx in other_indices)
                avg_dist_other = total_dist_other / len(other_indices)
                if avg_dist_other < b_i:
                    b_i = avg_dist_other

        # 3. Tính s(i)
        max_ab = max(a_i, b_i)
        if max_ab == 0.0:
            s_i = 0.0
        else:
            s_i = (b_i - a_i) / max_ab
        silhouette_coefficients.append(s_i)

    return sum(silhouette_coefficients) / len(silhouette_coefficients)


# ==============================================================================
# 5. KHẢO SÁT K TỐI ƯU (ELBOW & SILHOUETTE) DÙNG CÁC HÀM CƠ BẢN
# ==============================================================================

def find_optimal_k_scratch(data, k_range: range = range(2, 9), random_state: int = 42) -> List[Dict[str, Any]]:
    """
    Khảo sát k tối ưu bằng thuật toán SimpleKMeans và hàm tính Silhouette tự viết.
    Trả về danh sách kết quả gồm {k, inertia, silhouette}.
    """
    results = []
    for k in k_range:
        km = SimpleKMeans(k=k, random_state=random_state)
        km.fit(data)
        sil = calculate_silhouette_score_simple(data, km.labels)
        results.append({
            "k": k,
            "inertia": km.inertia,
            "silhouette": sil
        })
    return results

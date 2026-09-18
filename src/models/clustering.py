"""
Các thuật toán gom cụm và độ đo đánh giá — TỰ CÀI ĐẶT TỪ ĐẦU.

Nguyên tắc của đề tài: mọi thuật toán và độ đo dùng để ra kết quả đều được viết bằng vòng lặp và
các phép toán số học cơ bản (cộng, trừ, nhân, chia, căn bậc hai). Không gọi thư viện học máy.
`scikit-learn` và `scipy` chỉ được phép xuất hiện trong `scripts/verify_scratch_implementations.py`
để đối chứng kết quả (xem docs/adr/0001 và docs/adr/0003).

Nội dung:
1. Khoảng cách Euclid và ma trận khoảng cách.
2. K-Means: khởi tạo k-means++, chạy nhiều lần khởi tạo để giảm phụ thuộc điểm khởi tạo.
3. Phân cấp tích tụ theo tiêu chí Ward, cập nhật khoảng cách bằng công thức Lance-Williams.
4. DBSCAN: gom cụm theo mật độ, phát hiện điểm nhiễu.
5. Các độ đo: WCSS/Inertia, Silhouette, Davies-Bouldin, Calinski-Harabasz, Adjusted Rand Index.
6. Tiện ích: khảo sát số cụm, đánh giá tổng hợp, ghép cụm giữa hai năm, lưu/đọc tham số dạng JSON.
"""

import json
import math
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd


# ======================================================================================
# 0. TIỆN ÍCH DÙNG CHUNG
# ======================================================================================

def to_points(data: Union[np.ndarray, pd.DataFrame, Sequence[Sequence[float]]]) -> List[List[float]]:
    """Chuyển dữ liệu đầu vào (numpy array, DataFrame hoặc list) về list các điểm."""
    if isinstance(data, np.ndarray):
        return data.tolist()
    if hasattr(data, "values"):
        return data.values.tolist()
    return [list(row) for row in data]


def euclidean_distance(point1: Sequence[float], point2: Sequence[float]) -> float:
    """
    Khoảng cách Euclid giữa hai điểm trong không gian d chiều:
        d(p, q) = sqrt( sum( (p_i - q_i)^2 ) )
    """
    total = 0.0
    for i in range(len(point1)):
        difference = point1[i] - point2[i]
        total += difference * difference
    return math.sqrt(total)


def squared_euclidean_distance(point1: Sequence[float], point2: Sequence[float]) -> float:
    """
    Bình phương khoảng cách Euclid: sum( (p_i - q_i)^2 ).

    Dùng trong các vòng lặp so sánh khoảng cách (tìm tâm gần nhất, tìm cặp cụm gần nhất) vì
    bình phương không làm thay đổi thứ tự so sánh nhưng bỏ được phép căn bậc hai.
    """
    total = 0.0
    for i in range(len(point1)):
        difference = point1[i] - point2[i]
        total += difference * difference
    return total


def compute_distance_matrix(points: Sequence[Sequence[float]]) -> List[List[float]]:
    """Ma trận khoảng cách Euclid giữa mọi cặp điểm (ma trận đối xứng, đường chéo bằng 0)."""
    n_samples = len(points)
    matrix = [[0.0] * n_samples for _ in range(n_samples)]
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            distance = euclidean_distance(points[i], points[j])
            matrix[i][j] = distance
            matrix[j][i] = distance
    return matrix


def cluster_centroids(points: Sequence[Sequence[float]], labels: Sequence[int]) -> List[List[float]]:
    """Tâm của từng cụm = trung bình cộng toạ độ các điểm trong cụm; bỏ qua nhãn -1 (nhiễu)."""
    unique_labels = sorted(set(labels))
    centroids = []
    for cluster in unique_labels:
        if cluster == -1:
            continue
        members = [points[i] for i in range(len(points)) if labels[i] == cluster]
        centroid = []
        for dimension in range(len(points[0])):
            total = 0.0
            for member in members:
                total += member[dimension]
            centroid.append(total / len(members))
        centroids.append(centroid)
    return centroids


# ======================================================================================
# 1. K-MEANS
# ======================================================================================

class SimpleKMeans:
    """
    K-Means tự cài đặt.

    Bốn bước lặp:
        1. Khởi tạo k tâm cụm (mặc định bằng k-means++ để tâm ban đầu rải đều dữ liệu).
        2. Gán mỗi điểm vào tâm gần nhất.
        3. Cập nhật tâm cụm = trung bình cộng các điểm trong cụm.
        4. Lặp lại tới khi nhãn không đổi hoặc hết số vòng lặp.

    Vì kết quả phụ thuộc điểm khởi tạo, thuật toán chạy n_init lần với các điểm khởi tạo khác nhau
    rồi giữ nghiệm có tổng bình phương khoảng cách trong cụm (inertia) nhỏ nhất.
    """

    def __init__(
        self,
        k: int = 3,
        max_iter: int = 100,
        n_init: int = 10,
        init: str = "kmeans++",
        random_state: Optional[int] = 42,
    ):
        self.k = k
        self.max_iter = max_iter
        self.n_init = n_init
        self.init = init
        self.random_state = random_state
        self.centroids: List[List[float]] = []
        self.labels: List[int] = []
        self.inertia = 0.0
        self.inertia_history: List[float] = []
        self.n_iter_ = 0

    # ---------------------------------------------------------------- khởi tạo tâm cụm
    def _init_centroids(self, points: List[List[float]], generator: random.Random) -> List[List[float]]:
        """
        Khởi tạo k-means++:
        - Tâm thứ nhất chọn ngẫu nhiên trong dữ liệu.
        - Mỗi tâm tiếp theo chọn ngẫu nhiên nhưng ưu tiên điểm xa các tâm đã chọn:
          xác suất chọn điểm i tỉ lệ với bình phương khoảng cách từ i tới tâm gần nhất.
        """
        n_samples = len(points)
        first_index = generator.randrange(n_samples)
        centroids = [list(points[first_index])]
        closest_squared = [squared_euclidean_distance(point, centroids[0]) for point in points]

        while len(centroids) < self.k:
            total = sum(closest_squared)
            if total <= 0.0:
                pick = generator.randrange(n_samples)
            else:
                threshold = generator.random() * total
                cumulative = 0.0
                pick = n_samples - 1
                for index, value in enumerate(closest_squared):
                    cumulative += value
                    if cumulative >= threshold:
                        pick = index
                        break
            centroids.append(list(points[pick]))
            for index, point in enumerate(points):
                distance = squared_euclidean_distance(point, centroids[-1])
                if distance < closest_squared[index]:
                    closest_squared[index] = distance

        return centroids

    # ---------------------------------------------------------------- một lần chạy
    def _fit_once(self, points: List[List[float]], generator: random.Random):
        """Chạy K-Means một lần với một bộ tâm khởi tạo; trả về (inertia, labels, centroids, history, n_iter)."""
        centroids = self._init_centroids(points, generator)
        labels: List[int] = []
        history: List[float] = []
        n_samples = len(points)
        n_features = len(points[0])

        for iteration in range(self.max_iter):
            # Bước 2: gán nhãn theo tâm gần nhất
            new_labels = []
            for point in points:
                best_cluster, best_distance = 0, float("inf")
                for cluster_index in range(self.k):
                    distance = squared_euclidean_distance(point, centroids[cluster_index])
                    if distance < best_distance:
                        best_distance, best_cluster = distance, cluster_index
                new_labels.append(best_cluster)

            # Bước 3: cập nhật tâm cụm
            for cluster_index in range(self.k):
                members = [points[i] for i in range(n_samples) if new_labels[i] == cluster_index]
                if members:
                    updated = []
                    for dimension in range(n_features):
                        total = 0.0
                        for member in members:
                            total += member[dimension]
                        updated.append(total / len(members))
                    centroids[cluster_index] = updated
                else:
                    # Cụm rỗng: gán lại tâm vào một điểm ngẫu nhiên để cụm không bị "chết"
                    centroids[cluster_index] = list(points[generator.randrange(n_samples)])

            inertia = 0.0
            for i in range(n_samples):
                inertia += squared_euclidean_distance(points[i], centroids[new_labels[i]])
            history.append(inertia)

            converged = new_labels == labels
            labels = new_labels
            if converged:
                break

        inertia = 0.0
        for i in range(n_samples):
            inertia += squared_euclidean_distance(points[i], centroids[labels[i]])
        return inertia, labels, centroids, history, len(history)

    def fit(self, data) -> "SimpleKMeans":
        points = to_points(data)
        generator = random.Random(self.random_state)

        best = None
        for _ in range(self.n_init):
            result = self._fit_once(points, generator)
            if best is None or result[0] < best[0]:
                best = result

        self.inertia, self.labels, self.centroids, self.inertia_history, self.n_iter_ = best
        return self

    def predict(self, data) -> List[int]:
        """Gán nhãn cụm cho dữ liệu mới dựa trên các tâm cụm đã học."""
        points = to_points(data)
        predictions = []
        for point in points:
            best_cluster, best_distance = 0, float("inf")
            for cluster_index, centroid in enumerate(self.centroids):
                distance = squared_euclidean_distance(point, centroid)
                if distance < best_distance:
                    best_distance, best_cluster = distance, cluster_index
            predictions.append(best_cluster)
        return predictions

    def fit_predict(self, data) -> List[int]:
        return self.fit(data).labels

    def distances_to_centroids(self, point: Sequence[float]) -> List[float]:
        """Khoảng cách Euclid từ một điểm tới từng tâm cụm (dùng cho demo gán quốc gia mới)."""
        return [euclidean_distance(point, centroid) for centroid in self.centroids]


# ======================================================================================
# 2. PHÂN CẤP TÍCH TỤ THEO TIÊU CHÍ WARD
# ======================================================================================

class SimpleHierarchicalClustering:
    """
    Phân cấp tích tụ tự cài đặt.

    Ban đầu mỗi điểm là một cụm. Ở mỗi bước, hợp nhất hai cụm sao cho tổng bình phương sai số
    (SSE) tăng ít nhất — đó là tiêu chí Ward. Độ tăng SSE khi hợp nhất hai cụm A, B là:

        delta_SSE = SSE(A hop B) - SSE(A) - SSE(B)

    và cũng bằng (|A| * |B| / (|A| + |B|)) * d^2(A, B) với d^2(A, B) là bình phương khoảng cách
    giữa hai tâm cụm. Giá trị delta_SSE được lưu vào merge_history làm độ cao của nút trên
    biểu đồ cây; độ cao này tăng dần theo từng lần hợp nhất. Sau khi hợp nhất, bình phương
    khoảng cách từ cụm mới tới cụm C được cập nhật bằng công thức Lance-Williams:

        d^2(A hop B, C) = ((|A|+|C|) d^2(A,C) + (|B|+|C|) d^2(B,C) - |C| d^2(A,B)) / (|A|+|B|+|C|)

    Nhờ công thức này không phải tính lại toàn bộ khoảng cách sau mỗi lần hợp nhất.

    Tham số `linkage`:
    - "ward": tiêu chí Ward như trên (mặc định của đề tài).
    - "centroid": khoảng cách giữa hai tâm cụm (giữ lại để so sánh, đây là cách cài đặt cũ).
    """

    def __init__(self, n_clusters: int = 3, linkage: str = "ward"):
        if linkage not in ("ward", "centroid"):
            raise ValueError(f"Linkage không được hỗ trợ: {linkage}")
        self.n_clusters = n_clusters
        self.linkage = linkage
        self.labels: List[int] = []
        self.cluster_centroids: List[List[float]] = []
        self.merge_history: List[Dict[str, Any]] = []

    def fit_predict(self, data) -> List[int]:
        points = to_points(data)
        n_samples = len(points)
        n_features = len(points[0])

        # Mỗi điểm là một cụm; cụm mới sau khi hợp nhất nhận chỉ số n_samples, n_samples + 1, ...
        clusters: Dict[int, Dict[str, Any]] = {}
        for index in range(n_samples):
            clusters[index] = {
                "indices": [index],
                "centroid": list(points[index]),
                "size": 1,
                "sse": 0.0,  # tổng bình phương khoảng cách từ các điểm trong cụm tới tâm cụm
            }
        active = list(range(n_samples))
        next_label = n_samples

        # Ma trận bình phương khoảng cách giữa các tâm cụm (tối đa 2n - 1 cụm)
        max_clusters = 2 * n_samples - 1
        squared = [[0.0] * max_clusters for _ in range(max_clusters)]
        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                distance = squared_euclidean_distance(points[i], points[j])
                squared[i][j] = distance
                squared[j][i] = distance

        self.merge_history = []

        while len(active) > self.n_clusters:
            # Tìm cặp cụm gần nhau nhất (theo bình phương khoảng cách tâm cụm)
            best_distance = float("inf")
            best_pair = (-1, -1)
            for a_position in range(len(active)):
                for b_position in range(a_position + 1, len(active)):
                    candidate = squared[active[a_position]][active[b_position]]
                    if candidate < best_distance:
                        best_distance = candidate
                        best_pair = (a_position, b_position)

            a_position, b_position = best_pair
            label_a, label_b = active[a_position], active[b_position]
            cluster_a, cluster_b = clusters[label_a], clusters[label_b]
            size_a, size_b = cluster_a["size"], cluster_b["size"]

            # Tâm cụm mới = trung bình có trọng số theo số điểm
            centroid = []
            for dimension in range(n_features):
                weighted = (
                    cluster_a["centroid"][dimension] * size_a
                    + cluster_b["centroid"][dimension] * size_b
                )
                centroid.append(weighted / (size_a + size_b))

            members = cluster_a["indices"] + cluster_b["indices"]
            sse_new = 0.0
            for index in members:
                sse_new += squared_euclidean_distance(points[index], centroid)

            if self.linkage == "ward":
                # Độ tăng tổng bình phương sai số khi hợp nhất = tiêu chí Ward.
                # Tính trực tiếp từ toạ độ thay vì suy ra từ khoảng cách tâm đã cập nhật nhiều lần,
                # nhờ vậy độ cao luôn tăng dần và biểu đồ cây đọc được đúng.
                height = max(0.0, sse_new - cluster_a["sse"] - cluster_b["sse"])
            else:
                height = math.sqrt(best_distance)

            clusters[next_label] = {
                "indices": members,
                "centroid": centroid,
                "size": size_a + size_b,
                "sse": sse_new,
            }
            self.merge_history.append(
                {
                    "left": label_a,
                    "right": label_b,
                    "new": next_label,
                    "height": height,
                    "size": size_a + size_b,
                }
            )

            # Cập nhật khoảng cách từ cụm mới tới các cụm còn lại
            for other in active:
                if other in (label_a, label_b):
                    continue
                if self.linkage == "ward":
                    size_c = clusters[other]["size"]
                    numerator = (
                        (size_a + size_c) * squared[label_a][other]
                        + (size_b + size_c) * squared[label_b][other]
                        - size_c * squared[label_a][label_b]
                    )
                    squared[next_label][other] = numerator / (size_a + size_b + size_c)
                else:
                    squared[next_label][other] = squared_euclidean_distance(
                        centroid, clusters[other]["centroid"]
                    )
                squared[other][next_label] = squared[next_label][other]

            for position in sorted((a_position, b_position), reverse=True):
                active.pop(position)
            active.append(next_label)
            next_label += 1

        # Gán nhãn cuối cùng cho từng điểm
        self.labels = [0] * n_samples
        self.cluster_centroids = []
        for cluster_label, cluster_id in enumerate(active):
            self.cluster_centroids.append(clusters[cluster_id]["centroid"])
            for index in clusters[cluster_id]["indices"]:
                self.labels[index] = cluster_label

        return self.labels


# ======================================================================================
# 3. DBSCAN
# ======================================================================================

class SimpleDBSCAN:
    """
    DBSCAN tự cài đặt (Density-Based Spatial Clustering of Applications with Noise).

    Hai tham số:
    - eps: bán kính lân cận.
    - min_samples: số điểm tối thiểu trong bán kính eps để một điểm được coi là điểm lõi.

    Cách làm: với mỗi điểm lõi chưa được thăm, tạo một cụm mới rồi mở rộng dần sang các điểm
    lân cận; điểm không thuộc cụm nào được gán nhãn -1 (nhiễu).
    """

    def __init__(self, eps: float = 1.2, min_samples: int = 4):
        self.eps = eps
        self.min_samples = min_samples
        self.labels: List[int] = []
        self.n_clusters = 0
        self.n_noise = 0

    def _neighbors(self, distance_matrix: List[List[float]], index: int) -> List[int]:
        """Các điểm nằm trong bán kính eps của điểm index."""
        return [
            other
            for other in range(len(distance_matrix))
            if distance_matrix[index][other] <= self.eps
        ]

    def fit_predict(self, data) -> List[int]:
        points = to_points(data)
        n_samples = len(points)
        distance_matrix = compute_distance_matrix(points)
        neighbors = [self._neighbors(distance_matrix, index) for index in range(n_samples)]

        # None = chưa thăm, -1 = nhiễu
        labels: List[Optional[int]] = [None] * n_samples
        cluster_id = -1

        for index in range(n_samples):
            if labels[index] is not None:
                continue
            if len(neighbors[index]) < self.min_samples:
                labels[index] = -1  # tạm coi là nhiễu, có thể thành điểm biên của cụm sau
                continue

            cluster_id += 1
            labels[index] = cluster_id
            seeds = list(neighbors[index])
            in_seeds = set(seeds)
            position = 0

            while position < len(seeds):
                current = seeds[position]
                position += 1

                if labels[current] == -1:
                    labels[current] = cluster_id  # điểm nhiễu trước đó trở thành điểm biên

                if labels[current] is not None:
                    continue

                labels[current] = cluster_id
                if len(neighbors[current]) >= self.min_samples:
                    for candidate in neighbors[current]:
                        if candidate not in in_seeds:
                            in_seeds.add(candidate)
                            seeds.append(candidate)

        self.labels = list(labels)
        self.n_clusters = cluster_id + 1
        self.n_noise = sum(1 for label in self.labels if label == -1)
        return self.labels


# ======================================================================================
# 4. CÁC ĐỘ ĐO ĐÁNH GIÁ
# ======================================================================================

def calculate_silhouette_score_simple(data, labels: Sequence[int]) -> float:
    """
    Hệ số Silhouette trung bình, tự cài đặt.

    Với mỗi điểm i:
    - a(i) = khoảng cách trung bình tới các điểm cùng cụm (độ kết dính).
    - b(i) = khoảng cách trung bình nhỏ nhất tới các điểm của một cụm khác (độ tách biệt).
    - s(i) = (b(i) - a(i)) / max(a(i), b(i)); nếu cụm chỉ có một điểm thì quy ước s(i) = 0.
    Silhouette = trung bình s(i) trên toàn bộ dữ liệu; càng gần 1 càng tốt.
    """
    points = to_points(data)
    n_samples = len(points)
    unique_labels = sorted(set(labels))

    if len(unique_labels) < 2 or len(unique_labels) >= n_samples:
        return 0.0

    distance_matrix = compute_distance_matrix(points)
    total = 0.0

    for index in range(n_samples):
        same_cluster = [j for j in range(n_samples) if labels[j] == labels[index] and j != index]
        if same_cluster:
            a_i = sum(distance_matrix[index][j] for j in same_cluster) / len(same_cluster)
        else:
            a_i = 0.0

        b_i = float("inf")
        for cluster in unique_labels:
            if cluster == labels[index] or cluster == -1:
                continue
            other_cluster = [j for j in range(n_samples) if labels[j] == cluster]
            if not other_cluster:
                continue
            average = sum(distance_matrix[index][j] for j in other_cluster) / len(other_cluster)
            if average < b_i:
                b_i = average

        if b_i == float("inf"):
            b_i = 0.0

        denominator = max(a_i, b_i)
        total += 0.0 if denominator == 0.0 else (b_i - a_i) / denominator

    return total / n_samples


def calculate_davies_bouldin_score_simple(data, labels: Sequence[int]) -> float:
    """
    Chỉ số Davies-Bouldin, tự cài đặt; càng nhỏ càng tốt.

    Với cụm i: S_i = khoảng cách trung bình từ các điểm trong cụm tới tâm cụm (độ tán xạ).
    Với hai cụm i, j: M_ij = khoảng cách giữa hai tâm cụm.
    R_ij = (S_i + S_j) / M_ij; DB = trung bình của max_j R_ij theo từng cụm i.
    """
    points = to_points(data)
    unique_labels = sorted({label for label in labels if label != -1})
    n_clusters = len(unique_labels)
    if n_clusters < 2:
        return 0.0

    centroids = cluster_centroids(points, labels)

    scatter = []
    for position, cluster in enumerate(unique_labels):
        members = [points[i] for i in range(len(points)) if labels[i] == cluster]
        total = 0.0
        for member in members:
            total += euclidean_distance(member, centroids[position])
        scatter.append(total / len(members))

    total_ratio = 0.0
    for i in range(n_clusters):
        worst = 0.0
        for j in range(n_clusters):
            if i == j:
                continue
            separation = euclidean_distance(centroids[i], centroids[j])
            if separation == 0.0:
                continue
            ratio = (scatter[i] + scatter[j]) / separation
            if ratio > worst:
                worst = ratio
        total_ratio += worst

    return total_ratio / n_clusters


def calculate_calinski_harabasz_score_simple(data, labels: Sequence[int]) -> float:
    """
    Chỉ số Calinski-Harabasz (tỉ lệ phương sai giữa cụm và trong cụm), tự cài đặt; càng lớn càng tốt.

        CH = (SSB / (k - 1)) / (SSW / (n - k))

    với SSB = tổng bình phương khoảng cách từ tâm cụm tới tâm toàn bộ dữ liệu (có trọng số theo cụm),
    SSW = tổng bình phương khoảng cách từ mỗi điểm tới tâm cụm của nó.
    """
    points = to_points(data)
    n_samples = len(points)
    n_features = len(points[0])
    unique_labels = sorted({label for label in labels if label != -1})
    n_clusters = len(unique_labels)
    if n_clusters < 2 or n_clusters >= n_samples:
        return 0.0

    overall_centroid = []
    for dimension in range(n_features):
        total = 0.0
        for point in points:
            total += point[dimension]
        overall_centroid.append(total / n_samples)

    centroids = cluster_centroids(points, labels)
    between = 0.0
    within = 0.0

    for position, cluster in enumerate(unique_labels):
        members = [points[i] for i in range(n_samples) if labels[i] == cluster]
        between += len(members) * squared_euclidean_distance(centroids[position], overall_centroid)
        for member in members:
            within += squared_euclidean_distance(member, centroids[position])

    if within == 0.0:
        return 0.0
    return (between / (n_clusters - 1)) / (within / (n_samples - n_clusters))


def calculate_adjusted_rand_index(labels_a: Sequence[int], labels_b: Sequence[int]) -> float:
    """
    Chỉ số Adjusted Rand Index (ARI) giữa hai cách gán nhãn, tự cài đặt.

    Đếm số cặp điểm cùng/different nhãn trong hai cách gán, so với kỳ vọng ngẫu nhiên:
        ARI = (Index - Expected) / (Max - Expected)
    ARI = 1 khi hai cách gán trùng khớp (kể cả khác số thứ tự nhãn), xấp xỉ 0 khi ngẫu nhiên.
    """
    if len(labels_a) != len(labels_b):
        raise ValueError("Hai dãy nhãn phải có cùng độ dài")

    n_samples = len(labels_a)
    total_pairs = n_samples * (n_samples - 1) / 2
    if total_pairs == 0:
        return 1.0

    contingency: Dict[Tuple[int, int], int] = {}
    for a, b in zip(labels_a, labels_b):
        contingency[(a, b)] = contingency.get((a, b), 0) + 1

    count_a: Dict[int, int] = {}
    count_b: Dict[int, int] = {}
    for a, b in zip(labels_a, labels_b):
        count_a[a] = count_a.get(a, 0) + 1
        count_b[b] = count_b.get(b, 0) + 1

    def combinations_two(value: int) -> float:
        return value * (value - 1) / 2

    index = sum(combinations_two(size) for size in contingency.values())
    sum_a = sum(combinations_two(size) for size in count_a.values())
    sum_b = sum(combinations_two(size) for size in count_b.values())

    expected = sum_a * sum_b / total_pairs
    maximum = (sum_a + sum_b) / 2
    if maximum == expected:
        return 1.0
    return (index - expected) / (maximum - expected)


def evaluate_clustering(data, labels: Sequence[int]) -> Dict[str, Any]:
    """
    Đánh giá một cách gom cụm bằng bộ độ đo nội tại.

    Trả về dict giá trị phẳng để có thể đưa thẳng vào bảng so sánh:
    n_clusters, n_noise, inertia, silhouette, davies_bouldin, calinski_harabasz, sizes.
    """
    points = to_points(data)
    unique_labels = sorted(set(labels))
    valid_labels = [label for label in unique_labels if label != -1]

    inertia = 0.0
    centroids = cluster_centroids(points, labels)
    for position, cluster in enumerate(valid_labels):
        for index in range(len(points)):
            if labels[index] == cluster:
                inertia += squared_euclidean_distance(points[index], centroids[position])

    sizes = "/".join(
        str(sum(1 for label in labels if label == cluster)) for cluster in valid_labels
    )

    return {
        "n_clusters": len(valid_labels),
        "n_noise": int(sum(1 for label in labels if label == -1)),
        "inertia": round(inertia, 4),
        "silhouette": round(calculate_silhouette_score_simple(points, labels), 6),
        "davies_bouldin": round(calculate_davies_bouldin_score_simple(points, labels), 6),
        "calinski_harabasz": round(calculate_calinski_harabasz_score_simple(points, labels), 4),
        "sizes": sizes,
    }


# ======================================================================================
# 5. HÀM CHẠY THUẬT TOÁN VÀ KHẢO SÁT THAM SỐ
# ======================================================================================

def run_kmeans(
    data,
    n_clusters: int = 3,
    n_init: int = 10,
    random_state: Optional[int] = 42,
) -> Tuple[List[int], SimpleKMeans]:
    """Chạy K-Means và trả về (nhãn cụm, mô hình đã huấn luyện)."""
    model = SimpleKMeans(k=n_clusters, n_init=n_init, random_state=random_state)
    model.fit(data)
    return model.labels, model


def run_hierarchical(
    data,
    n_clusters: int = 3,
    linkage: str = "ward",
) -> Tuple[List[int], SimpleHierarchicalClustering]:
    """Chạy phân cấp tích tụ (mặc định tiêu chí Ward) và trả về (nhãn cụm, mô hình)."""
    model = SimpleHierarchicalClustering(n_clusters=n_clusters, linkage=linkage)
    model.fit_predict(data)
    return model.labels, model


def run_dbscan(
    data,
    eps: float = 1.2,
    min_samples: int = 4,
) -> Tuple[List[int], SimpleDBSCAN]:
    """Chạy DBSCAN và trả về (nhãn cụm, mô hình)."""
    model = SimpleDBSCAN(eps=eps, min_samples=min_samples)
    model.fit_predict(data)
    return model.labels, model


def find_optimal_k_kmeans(
    data,
    k_range: Optional[Sequence[int]] = None,
    n_init: int = 10,
    random_state: Optional[int] = 42,
) -> List[Dict[str, float]]:
    """
    Khảo sát số cụm k: với mỗi k chạy K-Means rồi ghi lại inertia (WCSS) và Silhouette.

    Trả về list các dict {k, inertia, silhouette} để chuyển thẳng thành DataFrame và vẽ biểu đồ.
    """
    if k_range is None:
        k_range = range(2, 10)

    results = []
    for k in k_range:
        labels, model = run_kmeans(data, n_clusters=k, n_init=n_init, random_state=random_state)
        results.append(
            {
                "k": k,
                "inertia": round(model.inertia, 4),
                "silhouette": round(calculate_silhouette_score_simple(data, labels), 6),
            }
        )
    return results


# Giữ tên cũ để không phá vỡ các đoạn mã đang gọi hàm này
find_optimal_k_scratch = find_optimal_k_kmeans


# ======================================================================================
# 6. GHÉP CỤM GIỮA CÁC NĂM VÀ LƯU THAM SỐ
# ======================================================================================

def match_clusters_greedy(
    centroids_a: Sequence[Sequence[float]],
    centroids_b: Sequence[Sequence[float]],
    scores_a: Optional[Sequence[float]] = None,
    scores_b: Optional[Sequence[float]] = None,
) -> Tuple[List[Dict[str, Any]], List[int], List[int]]:
    """
    Ghép cụm giữa hai năm vì nhãn cụm của hai lần gom độc lập không so sánh trực tiếp được.

    Cách ghép: xét lần lượt các cặp cụm theo khoảng cách tâm cụm tăng dần, nếu hai cụm chưa được
    ghép thì ghép chúng; khi khoảng cách bằng nhau thì ưu tiên cặp có chênh lệch điểm hạnh phúc
    trung bình nhỏ hơn (tham số scores_a, scores_b).

    Trả về (danh sách cặp đã ghép, các cụm của năm A không có cặp, các cụm của năm B không có cặp).
    """
    pairs = []
    for i, centroid_a in enumerate(centroids_a):
        for j, centroid_b in enumerate(centroids_b):
            distance = euclidean_distance(centroid_a, centroid_b)
            if scores_a is not None and scores_b is not None:
                score_gap = abs(scores_a[i] - scores_b[j])
            else:
                score_gap = 0.0
            pairs.append((distance, score_gap, i, j))
    pairs.sort(key=lambda item: (item[0], item[1]))

    used_a, used_b = set(), set()
    matches = []
    for distance, score_gap, i, j in pairs:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        matches.append(
            {
                "cluster_a": i,
                "cluster_b": j,
                "centroid_distance": round(distance, 6),
                "score_gap": round(score_gap, 6),
            }
        )

    unmatched_a = [i for i in range(len(centroids_a)) if i not in used_a]
    unmatched_b = [j for j in range(len(centroids_b)) if j not in used_b]
    return matches, unmatched_a, unmatched_b


def save_cluster_artifacts(
    path: Union[str, Path],
    year: int,
    method: str,
    scaler: str,
    n_clusters: int,
    centroids: Sequence[Sequence[float]],
    feature_columns: Optional[Sequence[str]] = None,
    metrics: Optional[Dict[str, Any]] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Path:
    """
    Lưu tham số mô hình ra JSON (tâm cụm, cách chuẩn hóa, metric) để đọc lại và giải thích được,
    thay vì lưu tệp nhị phân không đọc được như pickle.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "year": year,
        "method": method,
        "scaler": scaler,
        "n_clusters": n_clusters,
        "feature_columns": list(feature_columns) if feature_columns is not None else None,
        "centroids": [list(map(float, centroid)) for centroid in centroids],
        "metrics": metrics or {},
        "extra": extra or {},
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_cluster_artifacts(path: Union[str, Path]) -> Dict[str, Any]:
    """Đọc lại tệp tham số mô hình đã lưu bằng save_cluster_artifacts."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp tham số mô hình: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

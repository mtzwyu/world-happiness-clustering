"""
Các hàm tiền xử lý dữ liệu và chuẩn hóa thang đo viết bằng CÁC HÀM CƠ BẢN.
Không dùng black-box, giúp sinh viên hiểu rõ bản chất toán học của từng phép biến đổi.
"""

import math
import random
from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]


# ==============================================================================
# 1. TÍNH TOÁN THỐNG KÊ CƠ BẢN BẰNG VÒNG LẶP (MEAN, STD, MIN, MAX)
# ==============================================================================

def calculate_mean(values: List[float]) -> float:
    """Tính giá trị trung bình bằng vòng lặp cơ bản: mu = (1/n) * sum(x_i)"""
    total = 0.0
    for v in values:
        total += v
    return total / len(values) if len(values) > 0 else 0.0


def calculate_std(values: List[float], mean_val: float) -> float:
    """Tính độ lệch chuẩn bằng vòng lặp cơ bản: sigma = sqrt((1/n) * sum((x_i - mu)^2))"""
    sum_sq_diff = 0.0
    for v in values:
        diff = v - mean_val
        sum_sq_diff += diff * diff
    variance = sum_sq_diff / len(values) if len(values) > 0 else 0.0
    return math.sqrt(variance)


def calculate_min_max(values: List[float]) -> Tuple[float, float]:
    """Tìm giá trị nhỏ nhất và lớn nhất bằng vòng lặp cơ bản"""
    min_val = float('inf')
    max_val = float('-inf')
    for v in values:
        if v < min_val:
            min_val = v
        if v > max_val:
            max_val = v
    return min_val, max_val


# ==============================================================================
# 2. CHUẨN HÓA THANG ĐO BẰNG CÔNG THỨC CƠ BẢN
# ==============================================================================

class SimpleStandardScaler:
    """
    Chuẩn hóa Z-score thuần túy: z = (x - mean) / std
    Viết bằng các vòng lặp cơ bản để sinh viên dễ giải thích trước giảng viên.
    """
    def __init__(self):
        self.means = []
        self.stds = []

    def fit(self, data: List[List[float]]):
        """Học giá trị mean và std của từng cột đặc trưng."""
        n_features = len(data[0])
        self.means = []
        self.stds = []

        for col_idx in range(n_features):
            col_values = [row[col_idx] for row in data]
            mean_val = calculate_mean(col_values)
            std_val = calculate_std(col_values, mean_val)
            # Tránh chia cho 0 nếu tất cả giá trị trong cột giống nhau
            if std_val == 0.0:
                std_val = 1.0

            self.means.append(mean_val)
            self.stds.append(std_val)
        return self

    def transform(self, data: List[List[float]]) -> List[List[float]]:
        """Áp dụng công thức z = (x - mean) / std cho từng phần tử."""
        scaled_data = []
        for row in data:
            scaled_row = []
            for col_idx in range(len(row)):
                z = (row[col_idx] - self.means[col_idx]) / self.stds[col_idx]
                scaled_row.append(z)
            scaled_data.append(scaled_row)
        return scaled_data

    def fit_transform(self, data: List[List[float]]) -> List[List[float]]:
        return self.fit(data).transform(data)


class SimpleMinMaxScaler:
    """
    Chuẩn hóa Min-Max thuần túy: x_norm = (x - min) / (max - min)
    Đưa giá trị về khoảng [0, 1].
    """
    def __init__(self):
        self.mins = []
        self.maxs = []

    def fit(self, data: List[List[float]]):
        n_features = len(data[0])
        self.mins = []
        self.maxs = []

        for col_idx in range(n_features):
            col_values = [row[col_idx] for row in data]
            min_val, max_val = calculate_min_max(col_values)
            self.mins.append(min_val)
            self.maxs.append(max_val)
        return self

    def transform(self, data: List[List[float]]) -> List[List[float]]:
        scaled_data = []
        for row in data:
            scaled_row = []
            for col_idx in range(len(row)):
                range_val = self.maxs[col_idx] - self.mins[col_idx]
                if range_val == 0.0:
                    scaled_val = 0.0
                else:
                    scaled_val = (row[col_idx] - self.mins[col_idx]) / range_val
                scaled_row.append(scaled_val)
            scaled_data.append(scaled_row)
        return scaled_data

    def fit_transform(self, data: List[List[float]]) -> List[List[float]]:
        return self.fit(data).transform(data)


def scale_features(
    df: pd.DataFrame,
    feature_cols: List[str] = None,
    method: str = "standard"
) -> Tuple[np.ndarray, Any]:
    """
    Hàm tiện ích chuyển đổi DataFrame sang dạng list và chuẩn hóa.
    method: 'standard' (Z-score) hoặc 'minmax' (Min-Max [0, 1])
    """
    if feature_cols is None:
        feature_cols = [c for c in FEATURE_COLUMNS if c in df.columns]

    raw_data = df[feature_cols].values.tolist()

    if method == "standard":
        scaler = SimpleStandardScaler()
    elif method == "minmax":
        scaler = SimpleMinMaxScaler()
    else:
        raise ValueError(f"Phương pháp không hỗ trợ: {method}")

    scaled_list = scaler.fit_transform(raw_data)
    return np.array(scaled_list), scaler


# ==============================================================================
# 3. GIẢM CHIỀU PCA TỰ CÀI ĐẶT (PHƯƠNG PHÁP LŨY THỪA)
# ==============================================================================

def to_list_of_lists(data) -> List[List[float]]:
    """Chuyển dữ liệu đầu vào (numpy array, DataFrame hoặc list) về list các list số."""
    if isinstance(data, np.ndarray):
        return data.tolist()
    if hasattr(data, "values"):
        return data.values.tolist()
    return [list(row) for row in data]


def mat_vec_mul(matrix: List[List[float]], vector: List[float]) -> List[float]:
    """Nhân ma trận với vector bằng vòng lặp: (C v)_i = sum_j C[i][j] * v[j]"""
    result = []
    for row in matrix:
        total = 0.0
        for j in range(len(vector)):
            total += row[j] * vector[j]
        result.append(total)
    return result


def vector_norm(vector: List[float]) -> float:
    """Độ dài Euclid của vector: ||v|| = sqrt(sum(v_i^2))"""
    return math.sqrt(sum(value * value for value in vector))


class SimplePCA:
    """
    Giảm chiều dữ liệu bằng phân tích thành phần chính (PCA) tự cài đặt.

    Các bước thực hiện:
    1. Trừ trung bình từng cột để dữ liệu có trung bình bằng 0.
    2. Lập ma trận hiệp phương sai C kích thước d x d (d là số đặc trưng).
    3. Tìm vector riêng ứng với trị riêng lớn nhất của C bằng phương pháp lũy thừa:
       lặp phép nhân C với một vector đơn vị cho tới khi hướng của vector không đổi nữa.
    4. Loại thành phần vừa tìm khỏi C (deflation: C = C - lambda * v * v^T) rồi lặp lại
       để tìm thành phần tiếp theo.
    5. Chiếu dữ liệu đã trừ trung bình lên các vector riêng đó để thu được dữ liệu giảm chiều.

    Không dùng bất kỳ hàm phân rã ma trận có sẵn nào; chỉ dùng vòng lặp, phép cộng/nhân và căn bậc hai.
    """

    def __init__(
        self,
        n_components: int = 2,
        max_iter: int = 1000,
        tol: float = 1e-10,
        random_state: Any = 42,
    ):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.mean: List[float] = []
        self.components: List[List[float]] = []
        self.eigenvalues: List[float] = []
        self.explained_variance_ratio: List[float] = []

    # ------------------------------------------------------------------ bước con
    def _center(self, data: List[List[float]]) -> List[List[float]]:
        """Trừ trung bình từng cột, lưu lại trung bình để dùng cho transform()."""
        n_samples = len(data)
        n_features = len(data[0])

        self.mean = []
        for col in range(n_features):
            total = 0.0
            for row in range(n_samples):
                total += data[row][col]
            self.mean.append(total / n_samples)

        centered = []
        for row in range(n_samples):
            centered.append([data[row][col] - self.mean[col] for col in range(n_features)])
        return centered

    def _covariance_matrix(self, centered: List[List[float]]) -> List[List[float]]:
        """Ma trận hiệp phương sai: C[i][j] = sum(x_i * x_j) / (n - 1), ma trận đối xứng."""
        n_samples = len(centered)
        n_features = len(centered[0])
        matrix = [[0.0] * n_features for _ in range(n_features)]

        for i in range(n_features):
            for j in range(i, n_features):
                total = 0.0
                for row in range(n_samples):
                    total += centered[row][i] * centered[row][j]
                value = total / (n_samples - 1)
                matrix[i][j] = value
                matrix[j][i] = value
        return matrix

    def _power_iteration(self, matrix: List[List[float]]) -> Tuple[float, List[float]]:
        """
        Tìm trị riêng lớn nhất và vector riêng tương ứng bằng phương pháp lũy thừa.

        Lặp: v <- C v, chuẩn hóa v về độ dài 1, dừng khi v thay đổi ít hơn sai số tol.
        Trị riêng cuối cùng lấy theo thương Rayleigh: lambda = v^T C v.
        """
        n_features = len(matrix)

        if self.random_state is None:
            # Khởi tạo tất định: chọn cột có phương sai lớn nhất
            start = max(range(n_features), key=lambda idx: matrix[idx][idx])
            vector = [0.0] * n_features
            vector[start] = 1.0
        else:
            generator = random.Random(self.random_state)
            vector = [generator.uniform(-1.0, 1.0) for _ in range(n_features)]
            norm = vector_norm(vector)
            vector = [value / norm for value in vector]

        for _ in range(self.max_iter):
            product = mat_vec_mul(matrix, vector)
            norm = vector_norm(product)
            if norm == 0.0:
                break
            updated = [value / norm for value in product]
            difference = vector_norm([updated[i] - vector[i] for i in range(n_features)])
            vector = updated
            if difference < self.tol:
                break

        product = mat_vec_mul(matrix, vector)
        eigenvalue = sum(vector[i] * product[i] for i in range(n_features))
        return eigenvalue, vector

    # ------------------------------------------------------------------ API chính
    def fit(self, data) -> "SimplePCA":
        """Học các thành phần chính từ dữ liệu."""
        matrix_data = to_list_of_lists(data)
        centered = self._center(matrix_data)
        covariance = self._covariance_matrix(centered)
        total_variance = sum(covariance[i][i] for i in range(len(covariance)))

        self.components = []
        self.eigenvalues = []
        working = [row[:] for row in covariance]

        for _ in range(min(self.n_components, len(covariance))):
            eigenvalue, vector = self._power_iteration(working)
            self.eigenvalues.append(eigenvalue)
            self.components.append(vector)

            # Loại thành phần vừa tìm khỏi ma trận để vòng sau tìm được thành phần kế tiếp
            for i in range(len(working)):
                for j in range(len(working)):
                    working[i][j] -= eigenvalue * vector[i] * vector[j]

        if total_variance > 0.0:
            self.explained_variance_ratio = [value / total_variance for value in self.eigenvalues]
        else:
            self.explained_variance_ratio = [0.0] * len(self.eigenvalues)
        return self

    def transform(self, data) -> List[List[float]]:
        """Chiếu dữ liệu lên các thành phần chính đã học."""
        matrix_data = to_list_of_lists(data)
        result = []
        for row in matrix_data:
            centered_row = [row[col] - self.mean[col] for col in range(len(row))]
            projected = []
            for component in self.components:
                projected.append(
                    sum(centered_row[i] * component[i] for i in range(len(component)))
                )
            result.append(projected)
        return result

    def fit_transform(self, data) -> List[List[float]]:
        return self.fit(data).transform(data)


def apply_pca(X_scaled: np.ndarray, n_components: int = 2, random_state: Any = 42):
    """
    Giảm chiều dữ liệu bằng SimplePCA tự cài đặt, phục vụ vẽ biểu đồ phân tán 2D.

    Giữ nguyên chữ ký cũ để các notebook đang gọi hàm này không phải sửa.
    """
    pca = SimplePCA(n_components=n_components, random_state=random_state)
    X_pca = pca.fit_transform(X_scaled)
    return np.array(X_pca), pca

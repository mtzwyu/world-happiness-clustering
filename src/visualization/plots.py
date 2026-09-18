"""
Các hàm vẽ biểu đồ dùng cho báo cáo Word.

Mọi hình đều được lưu ở 300 DPI để chèn vào báo cáo, kèm tiêu đề và nhãn trục bằng tiếng Việt.
Thư viện vẽ (matplotlib, seaborn) chỉ dùng để trình bày, không tham gia tính toán kết quả.
"""

from pathlib import Path
from typing import Dict, List, Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def _save(fig, save_path: Optional[str]) -> None:
    """Lưu hình ở 300 DPI nếu có đường dẫn."""
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")


def plot_elbow_silhouette(metrics_df: pd.DataFrame, save_path: Optional[str] = None):
    """Vẽ hai biểu đồ liền kề: đường khuỷu tay (inertia) và Silhouette theo số cụm k."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(metrics_df["k"], metrics_df["inertia"], "bo-", linewidth=2, markersize=8)
    axes[0].set_title("Phương pháp khuỷu tay (Elbow)", fontsize=13)
    axes[0].set_xlabel("Số cụm k")
    axes[0].set_ylabel("Inertia (tổng bình phương khoảng cách trong cụm)")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    axes[1].plot(metrics_df["k"], metrics_df["silhouette"], "ro-", linewidth=2, markersize=8)
    axes[1].set_title("Hệ số Silhouette theo số cụm", fontsize=13)
    axes[1].set_xlabel("Số cụm k")
    axes[1].set_ylabel("Silhouette")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_elbow_silhouette_by_year(metrics_by_year: Dict[int, pd.DataFrame], save_path: Optional[str] = None):
    """Lưới biểu đồ khuỷu tay và Silhouette cho từng năm (mỗi năm một cột)."""
    years = sorted(metrics_by_year)
    fig, axes = plt.subplots(2, len(years), figsize=(4 * len(years), 8), sharex=True)

    for column, year in enumerate(years):
        metrics_df = metrics_by_year[year]
        axes[0, column].plot(metrics_df["k"], metrics_df["inertia"], "bo-", markersize=5)
        axes[0, column].set_title(f"Năm {year}", fontsize=12)
        axes[0, column].grid(True, linestyle="--", alpha=0.5)
        if column == 0:
            axes[0, column].set_ylabel("Inertia")

        axes[1, column].plot(metrics_df["k"], metrics_df["silhouette"], "ro-", markersize=5)
        axes[1, column].set_xlabel("Số cụm k")
        axes[1, column].grid(True, linestyle="--", alpha=0.5)
        if column == 0:
            axes[1, column].set_ylabel("Silhouette")

    fig.suptitle("Khảo sát số cụm theo từng năm (K-Means, chuẩn hóa Z-score)", fontsize=14)
    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_scaling_comparison(comparison_df: pd.DataFrame, metric: str = "silhouette",
                            save_path: Optional[str] = None):
    """So sánh một độ đo giữa các cấu hình gom cụm theo từng năm (biểu đồ cột nhóm)."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=comparison_df, x="year", y=metric, hue="configuration", ax=ax)
    ax.set_title(f"So sánh {metric} giữa các cấu hình gom cụm theo năm", fontsize=13)
    ax.set_xlabel("Năm")
    ax.set_ylabel(metric)
    ax.legend(title="Cấu hình", fontsize=9, ncol=2)
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    _save(fig, save_path)
    return fig


def plot_heatmap(matrix: pd.DataFrame, title: str, xlabel: str, ylabel: str,
                 save_path: Optional[str] = None, fmt: str = ".0f", cmap: str = "YlGnBu"):
    """Bản đồ nhiệt cho bảng số liệu hai chiều (ví dụ số cụm theo eps và min_samples)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(matrix, annot=True, fmt=fmt, cmap=cmap, ax=ax, cbar_kws={"label": title})
    ax.set_title(title, fontsize=13)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _save(fig, save_path)
    return fig


def plot_clusters_2d(X_2d, labels: Sequence[int], title: str = "Trực quan hóa phân cụm (2D PCA)",
                     save_path: Optional[str] = None):
    """Biểu đồ phân tán 2D cho các cụm (nhãn -1 là điểm nhiễu)."""
    fig, ax = plt.subplots(figsize=(9, 6))
    frame = pd.DataFrame(
        {
            "Thành phần 1": X_2d[:, 0],
            "Thành phần 2": X_2d[:, 1],
            "Cụm": [f"Nhiễu" if label == -1 else f"Cụm {label}" for label in labels],
        }
    )
    sns.scatterplot(data=frame, x="Thành phần 1", y="Thành phần 2", hue="Cụm", palette="tab10",
                    s=70, alpha=0.85, ax=ax)
    ax.set_title(title, fontsize=13, pad=12)
    ax.grid(True, linestyle="--", alpha=0.5)
    _save(fig, save_path)
    return fig


def plot_clusters_grid(pca_by_year: Dict[int, np.ndarray], labels_by_year: Dict[int, Sequence[int]],
                       save_path: Optional[str] = None):
    """Lưới biểu đồ phân tán PCA 2D của các cụm cho từng năm."""
    years = sorted(pca_by_year)
    fig, axes = plt.subplots(1, len(years), figsize=(4 * len(years), 4.2))
    if len(years) == 1:
        axes = [axes]

    for axis, year in zip(axes, years):
        coordinates = pca_by_year[year]
        labels = labels_by_year[year]
        colors = ["#d62728" if label == -1 else f"C{label}" for label in labels]
        axis.scatter(coordinates[:, 0], coordinates[:, 1], c=colors, s=28, alpha=0.85)
        axis.set_title(f"Năm {year}", fontsize=12)
        axis.grid(True, linestyle="--", alpha=0.4)
        axis.set_xlabel("Thành phần 1")
    axes[0].set_ylabel("Thành phần 2")

    fig.suptitle("Phân bố các cụm trên không gian giảm chiều PCA (2 thành phần đầu)", fontsize=14)
    plt.tight_layout()
    _save(fig, save_path)
    return fig


def plot_cluster_radar(cluster_means: pd.DataFrame, features: Sequence[str],
                       title: str = "Biểu đồ radar so sánh các yếu tố giữa các cụm",
                       save_path: Optional[str] = None):
    """Biểu đồ radar so sánh giá trị trung bình các đặc trưng giữa các cụm."""
    num_vars = len(features)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for index, row in cluster_means.iterrows():
        values = row[list(features)].tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=f"Cụm {index}")
        ax.fill(angles, values, alpha=0.15)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), list(features), fontsize=10)
    ax.set_title(title, y=1.08, fontsize=13)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
    _save(fig, save_path)
    return fig


def plot_cluster_profiles_bar(cluster_means: pd.DataFrame, features: Sequence[str],
                              save_path: Optional[str] = None):
    """Biểu đồ cột nhóm so sánh giá trị trung bình các đặc trưng giữa các cụm."""
    fig, ax = plt.subplots(figsize=(12, 6))
    positions = np.arange(len(features))
    width = 0.8 / max(len(cluster_means), 1)

    for offset, (index, row) in enumerate(cluster_means.iterrows()):
        values = [row[feature] for feature in features]
        ax.bar(positions + offset * width, values, width, label=f"Cụm {index}")

    ax.set_xticks(positions + width * (len(cluster_means) - 1) / 2)
    ax.set_xticklabels(list(features), rotation=12, fontsize=9)
    ax.set_title("Giá trị trung bình các yếu tố theo cụm", fontsize=13)
    ax.set_ylabel("Giá trị trung bình")
    ax.legend(fontsize=9)
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    _save(fig, save_path)
    return fig


def plot_happiness_score_by_cluster(frame: pd.DataFrame, cluster_column: str, score_column: str,
                                    title: str = "Phân bố điểm hạnh phúc theo cụm (hậu kiểm)",
                                    save_path: Optional[str] = None):
    """Biểu đồ hộp phân bố điểm hạnh phúc của từng cụm (bước hậu kiểm)."""
    fig, ax = plt.subplots(figsize=(9, 5))
    data = frame.copy()
    data[cluster_column] = data[cluster_column].astype(str)
    sns.boxplot(data=data, x=cluster_column, y=score_column, palette="Set2", ax=ax)
    sns.stripplot(data=data, x=cluster_column, y=score_column, color="black", size=3, alpha=0.5, ax=ax)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Cụm")
    ax.set_ylabel(score_column)
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    _save(fig, save_path)
    return fig


def plot_cluster_count_trend(trend_df: pd.DataFrame, save_path: Optional[str] = None):
    """Số lượng quốc gia trong mỗi cụm qua các năm (đã ghép cụm liên năm)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=trend_df, x="year", y="n_countries", hue="matched_cluster", marker="o", ax=ax)
    ax.set_title("Số lượng quốc gia trong mỗi cụm qua các năm", fontsize=13)
    ax.set_xlabel("Năm")
    ax.set_ylabel("Số quốc gia")
    ax.legend(title="Cụm (đã ghép)", fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.5)
    _save(fig, save_path)
    return fig


def plot_dendrogram(merge_history: List[Dict], n_clusters: int, title: str = "Biểu đồ cây phân cấp (Ward)",
                    save_path: Optional[str] = None):
    """
    Vẽ biểu đồ cây từ lịch sử hợp nhất của phân cấp Ward.

    Mỗi lần hợp nhất là một nút với độ cao bằng độ tăng tổng bình phương sai số. Vì thuật toán dừng
    khi còn đúng n_clusters cụm nên lịch sử hợp nhất tạo thành một RỪNG gồm n_clusters cây; phải vẽ
    từ tất cả các gốc, không chỉ gốc của lần hợp nhất cuối cùng. Vị trí ngang của lá được đánh số theo
    thứ tự duyệt cây, vị trí của nút cha là trung bình vị trí hai nút con.
    """
    if not merge_history:
        return None

    children = {step["new"]: (step["left"], step["right"]) for step in merge_history}
    heights = {step["new"]: step["height"] for step in merge_history}

    used_as_child = set()
    for left, right in children.values():
        used_as_child.add(left)
        used_as_child.add(right)
    roots = sorted(children.keys() - used_as_child, key=lambda node: (-heights[node], node))

    positions: Dict[int, float] = {}
    counter = [0.0]

    def assign(node: int) -> float:
        if node in children:
            left, right = children[node]
            x = (assign(left) + assign(right)) / 2.0
        else:
            x = counter[0]
            counter[0] += 1.0
        positions[node] = x
        return x

    for root in roots:
        assign(root)
        counter[0] += 1.0  # chừa khoảng trống giữa các cây

    fig, ax = plt.subplots(figsize=(12, 5))
    for node, (left, right) in children.items():
        height = heights[node]
        for child in (left, right):
            ax.plot([positions[child], positions[child]], [heights.get(child, 0.0), height],
                    color="#1f77b4", linewidth=0.8)
        ax.plot([positions[left], positions[right]], [height, height], color="#1f77b4", linewidth=0.8)

    top_height = max(heights.values())
    ax.axhline(top_height, color="red", linestyle="--", linewidth=1.2,
               label=f"Mức hợp nhất cuối cùng (dừng ở {n_clusters} cụm)")
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Quốc gia (sắp theo thứ tự hợp nhất)")
    ax.set_ylabel("Độ tăng tổng bình phương sai số khi hợp nhất")
    ax.set_xticks([])
    ax.legend(fontsize=9)
    _save(fig, save_path)
    return fig

"""
Kiểm chứng các thuật toán và độ đo tự cài đặt so với thư viện chuẩn.

Đây là NƠI DUY NHẤT trong dự án được phép dùng `scikit-learn` và `scipy`: mục đích là đối chứng
kết quả của hàm tự viết, không dùng để tạo ra kết quả cho báo cáo (xem docs/adr/0001, docs/adr/0003).

Cách chạy (từ gốc repo):
    .venv\\Scripts\\python.exe scripts/verify_scratch_implementations.py

Script in ra bảng PASS/FAIL cho từng hạng mục và trả mã thoát khác 0 nếu có hạng mục FAIL.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.data_loader import load_interim  # noqa: E402
from src.features.feature_engineering import (  # noqa: E402
    FEATURE_COLUMNS,
    SimplePCA,
    scale_features,
)
from src.models.clustering import (  # noqa: E402
    calculate_adjusted_rand_index,
    calculate_calinski_harabasz_score_simple,
    calculate_davies_bouldin_score_simple,
    calculate_silhouette_score_simple,
    euclidean_distance,
    evaluate_clustering,
    run_dbscan,
    run_hierarchical,
    run_kmeans,
)

RESULTS: list[dict] = []


def record(name: str, value: str, tolerance: str, passed: bool) -> None:
    """Ghi lại một hạng mục kiểm chứng để in thành bảng ở cuối."""
    RESULTS.append({"name": name, "value": value, "tolerance": tolerance, "passed": bool(passed)})


def main() -> int:
    # ----------------------------------------------------------------------------------
    # 0. Bất biến của đề tài: không đưa điểm/thứ hạng hạnh phúc vào ma trận đặc trưng
    # ----------------------------------------------------------------------------------
    forbidden = {"happiness_score", "happiness_rank"}
    record(
        "Quy tắc vàng: ma trận đặc trưng không chứa điểm/thứ hạng hạnh phúc",
        f"X gồm {FEATURE_COLUMNS}",
        "không giao với {happiness_score, happiness_rank}",
        forbidden.isdisjoint(FEATURE_COLUMNS),
    )

    # ----------------------------------------------------------------------------------
    # 1. Dữ liệu kiểm chứng: 156 quốc gia năm 2019, 6 đặc trưng đã chuẩn hóa Z-score
    # ----------------------------------------------------------------------------------
    df = load_interim()
    df_2019 = df[df["year"] == 2019].dropna(subset=FEATURE_COLUMNS).reset_index(drop=True)
    X_scaled, _ = scale_features(df_2019, method="standard")
    print(f"Dữ liệu kiểm chứng: {X_scaled.shape[0]} quốc gia x {X_scaled.shape[1]} đặc trưng\n")

    # ----------------------------------------------------------------------------------
    # 2. Khoảng cách Euclid
    # ----------------------------------------------------------------------------------
    reference_distance = float(np.sqrt(((X_scaled[0] - X_scaled[1]) ** 2).sum()))
    mine_distance = euclidean_distance(X_scaled[0].tolist(), X_scaled[1].tolist())
    difference = abs(mine_distance - reference_distance)
    record("Khoảng cách Euclid", f"{difference:.3e}", "sai lệch < 1e-12", difference < 1e-12)

    # ----------------------------------------------------------------------------------
    # 3. K-Means so với sklearn
    # ----------------------------------------------------------------------------------
    from sklearn.cluster import KMeans  # noqa: E402
    from sklearn.metrics import adjusted_rand_score  # noqa: E402

    my_labels, my_model = run_kmeans(X_scaled, n_clusters=3, n_init=10, random_state=42)
    reference_model = KMeans(n_clusters=3, n_init=10, random_state=42)
    reference_labels = reference_model.fit_predict(X_scaled)

    ari_kmeans = adjusted_rand_score(my_labels, reference_labels)
    record(
        "K-Means: nhãn cụm khớp sklearn",
        f"ARI = {ari_kmeans:.4f}",
        "ARI >= 0.99",
        ari_kmeans >= 0.99,
    )
    inertia_gap = my_model.inertia - float(reference_model.inertia_)
    record(
        "K-Means: inertia không lớn hơn sklearn",
        f"chênh lệch = {inertia_gap:.4f}",
        "chênh lệch <= 1e-6",
        inertia_gap <= 1e-6,
    )
    record(
        "K-Means: số vòng lặp tới khi hội tụ",
        f"n_iter = {my_model.n_iter_}",
        "hữu hạn và <= max_iter",
        0 < my_model.n_iter_ <= my_model.max_iter,
    )

    # ----------------------------------------------------------------------------------
    # 4. Phân cấp Ward so với scipy
    # ----------------------------------------------------------------------------------
    from scipy.cluster.hierarchy import fcluster, linkage  # noqa: E402
    from scipy.spatial.distance import pdist  # noqa: E402

    scipy_linkage = linkage(X_scaled, method="ward")
    for k in (2, 3, 4):
        ward_labels, ward_model = run_hierarchical(X_scaled, n_clusters=k, linkage="ward")
        scipy_labels = fcluster(scipy_linkage, t=k, criterion="maxclust")
        ari_ward = adjusted_rand_score(ward_labels, scipy_labels)
        record(
            f"Phân cấp Ward (k={k}): nhãn cụm khớp scipy",
            f"ARI = {ari_ward:.4f}",
            "ARI >= 0.99",
            ari_ward >= 0.99,
        )

    heights = [step["height"] for step in ward_model.merge_history]
    monotonic = all(heights[i] <= heights[i + 1] + 1e-9 for i in range(len(heights) - 1))
    record(
        "Phân cấp Ward: độ cao hợp nhất tăng dần",
        f"{len(heights)} lần hợp nhất",
        "độ cao không giảm",
        monotonic,
    )

    # So sánh centroid linkage (cách cài đặt cũ) với Ward để thấy hai tiêu chí khác nhau
    centroid_labels, _ = run_hierarchical(X_scaled, n_clusters=3, linkage="centroid")
    ari_linkage = calculate_adjusted_rand_index(ward_labels, centroid_labels)
    record(
        "Ward và centroid linkage cho kết quả khác nhau (đúng như lý thuyết)",
        f"ARI = {ari_linkage:.4f}",
        "ARI < 1.0",
        ari_linkage < 1.0,
    )

    # ----------------------------------------------------------------------------------
    # 5. DBSCAN so với sklearn (dữ liệu tổng hợp dạng chùm)
    # ----------------------------------------------------------------------------------
    from sklearn.cluster import DBSCAN  # noqa: E402

    generator = np.random.default_rng(42)
    blobs = np.vstack(
        [
            generator.normal(loc=(0, 0), scale=0.35, size=(60, 2)),
            generator.normal(loc=(3, 3), scale=0.35, size=(60, 2)),
            generator.normal(loc=(-3, 3), scale=0.35, size=(60, 2)),
            generator.uniform(low=-6, high=6, size=(25, 2)),  # điểm rải rác -> nhiễu
        ]
    )
    my_dbscan_labels, my_dbscan = run_dbscan(blobs, eps=0.9, min_samples=5)
    reference_dbscan = DBSCAN(eps=0.9, min_samples=5).fit_predict(blobs)

    ari_dbscan = adjusted_rand_score(my_dbscan_labels, reference_dbscan)
    record(
        "DBSCAN: nhãn cụm khớp sklearn",
        f"ARI = {ari_dbscan:.4f}",
        "ARI >= 0.95",
        ari_dbscan >= 0.95,
    )
    my_noise = {i for i, label in enumerate(my_dbscan_labels) if label == -1}
    reference_noise = {i for i, label in enumerate(reference_dbscan) if label == -1}
    record(
        "DBSCAN: tập điểm nhiễu khớp sklearn",
        f"|chênh lệch| = {len(my_noise ^ reference_noise)}",
        "bằng nhau",
        my_noise == reference_noise,
    )

    # ----------------------------------------------------------------------------------
    # 6. Các độ đo nội tại so với sklearn
    # ----------------------------------------------------------------------------------
    from sklearn.metrics import (  # noqa: E402
        calinski_harabasz_score,
        davies_bouldin_score,
        silhouette_score,
    )

    my_silhouette = calculate_silhouette_score_simple(X_scaled, my_labels)
    reference_silhouette = silhouette_score(X_scaled, my_labels)
    record(
        "Silhouette khớp sklearn",
        f"sai lệch = {abs(my_silhouette - reference_silhouette):.3e}",
        "< 1e-6",
        abs(my_silhouette - reference_silhouette) < 1e-6,
    )

    my_db = calculate_davies_bouldin_score_simple(X_scaled, my_labels)
    reference_db = davies_bouldin_score(X_scaled, my_labels)
    record(
        "Davies-Bouldin khớp sklearn",
        f"sai lệch = {abs(my_db - reference_db):.3e}",
        "< 1e-6",
        abs(my_db - reference_db) < 1e-6,
    )

    my_ch = calculate_calinski_harabasz_score_simple(X_scaled, my_labels)
    reference_ch = calinski_harabasz_score(X_scaled, my_labels)
    record(
        "Calinski-Harabasz khớp sklearn",
        f"sai lệch tương đối = {abs(my_ch - reference_ch) / reference_ch:.3e}",
        "< 1e-6",
        abs(my_ch - reference_ch) / reference_ch < 1e-6,
    )

    my_ari = calculate_adjusted_rand_index(my_labels, reference_labels)
    reference_ari = adjusted_rand_score(my_labels, reference_labels)
    record(
        "Adjusted Rand Index khớp sklearn",
        f"sai lệch = {abs(my_ari - reference_ari):.3e}",
        "< 1e-9",
        abs(my_ari - reference_ari) < 1e-9,
    )

    # ARI phải bằng 1 khi hai cách gán nhãn giống nhau nhưng khác thứ tự nhãn
    relabeled = [label + 100 for label in my_labels]
    record(
        "ARI = 1 khi hai cách gán nhãn tương đương",
        f"ARI = {calculate_adjusted_rand_index(my_labels, relabeled):.4f}",
        "= 1.0",
        abs(calculate_adjusted_rand_index(my_labels, relabeled) - 1.0) < 1e-12,
    )

    # ----------------------------------------------------------------------------------
    # 7. evaluate_clustering trả về dict giá trị phẳng (dùng trực tiếp trong bảng so sánh)
    # ----------------------------------------------------------------------------------
    summary = evaluate_clustering(X_scaled, my_labels)
    expected_keys = {
        "n_clusters",
        "n_noise",
        "inertia",
        "silhouette",
        "davies_bouldin",
        "calinski_harabasz",
        "sizes",
    }
    flat_types = all(not isinstance(value, (list, dict)) for value in summary.values())
    record(
        "evaluate_clustering trả về giá trị phẳng đủ khoá",
        f"{sorted(summary.keys())}",
        "đủ 7 khoá và không lồng cấu trúc",
        set(summary.keys()) == expected_keys and flat_types,
    )

    # ----------------------------------------------------------------------------------
    # 8. PCA tự cài đặt so với sklearn
    # ----------------------------------------------------------------------------------
    from sklearn.decomposition import PCA  # noqa: E402

    my_pca = SimplePCA(n_components=3, random_state=42)
    my_projection = np.array(my_pca.fit_transform(X_scaled))
    reference_pca = PCA(n_components=3, random_state=42)
    reference_projection = reference_pca.fit_transform(X_scaled)

    ratio_gap = max(
        abs(a - b)
        for a, b in zip(my_pca.explained_variance_ratio, reference_pca.explained_variance_ratio_)
    )
    record(
        "PCA: phương sai giải thích khớp sklearn",
        f"sai lệch = {ratio_gap:.3e}",
        "< 1e-6",
        ratio_gap < 1e-6,
    )
    projection_gap = float(np.abs(np.abs(my_projection) - np.abs(reference_projection)).max())
    record(
        "PCA: toạ độ sau khi chiếu khớp sklearn",
        f"sai lệch = {projection_gap:.3e}",
        "< 1e-6",
        projection_gap < 1e-6,
    )

    # ----------------------------------------------------------------------------------
    # In bảng kết quả
    # ----------------------------------------------------------------------------------
    print(f"{'Hạng mục kiểm chứng':<62}{'Giá trị':<34}{'Kết quả'}")
    print("-" * 108)
    failed = 0
    for item in RESULTS:
        if not item["passed"]:
            failed += 1
        status = "PASS" if item["passed"] else "FAIL"
        print(f"{item['name']:<62}{item['value']:<34}{status}  ({item['tolerance']})")
    print("-" * 108)
    print(f"Tổng số hạng mục: {len(RESULTS)} | PASS: {len(RESULTS) - failed} | FAIL: {failed}")

    if failed:
        print("\nKET QUA: FAIL")
        return 1
    print("\nKET QUA: PASS - các hàm tự cài đặt khớp với thư viện đối chứng")
    return 0


if __name__ == "__main__":
    sys.exit(main())

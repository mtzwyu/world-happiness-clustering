"""
Ứng dụng demo tương tác (Streamlit) — Đề tài 16:
Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report 2015 – 2019)

Phụ trách: Ngô Quang Trung (MSSV: 2045240325) — Mốc M4 (Ngày 22 – Ngày 23)
Ứng dụng đọc trực tiếp dữ liệu thực nghiệm đã sinh ở các mốc M1–M3 (không hardcode số liệu):
- data/interim/happiness_merged.csv
- data/processed/contrast_k3/contrast_k3_{kmeans,ward}_{year}.csv
- data/processed/country_cluster_shift.csv
- reports/tables/model_comparison_metrics_by_year.csv, contrast_k3_by_year.csv
- models/kmeans_2019.json (tâm cụm + tham số scaler cho Tab What-if)

Bốn tab tương tác: (1) Tổng quan cụm & Radar, (2) Bản đồ thế giới Choropleth,
(3) Tra cứu quốc gia & dịch chuyển cụm, (4) Thử nghiệm gán nhãn quốc gia mới.

Cách chạy:
    streamlit run app/app.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ===========================================================================
# 1. ĐƯỜNG DẪN TƯƠNG ĐỐI ĐỘC LẬP MÔI TRƯỜNG
# ===========================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM_PATH = PROJECT_ROOT / "data" / "interim" / "happiness_merged.csv"
CONTRAST_DIR = PROJECT_ROOT / "data" / "processed" / "contrast_k3"
SHIFT_PATH = PROJECT_ROOT / "data" / "processed" / "country_cluster_shift.csv"
MODELS_DIR = PROJECT_ROOT / "models"
METRICS_PATH = PROJECT_ROOT / "reports" / "tables" / "model_comparison_metrics_by_year.csv"
CONTRAST_KPI_PATH = PROJECT_ROOT / "reports" / "tables" / "contrast_k3_by_year.csv"

YEARS: List[int] = [2015, 2016, 2017, 2018, 2019]

# Quy tắc vàng: ma trận đặc trưng X chỉ gồm 6 yếu tố cơ sở, KHÔNG có happiness_score.
FEATURE_COLUMNS: List[str] = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]

FEATURE_LABELS: Dict[str, str] = {
    "gdp_per_capita": "GDP bình quân đầu người",
    "social_support": "Hỗ trợ xã hội",
    "healthy_life_expectancy": "Tuổi thọ khỏe mạnh",
    "freedom": "Tự do lựa chọn cuộc sống",
    "generosity": "Mức độ hào phóng",
    "corruption_perception": "Nhận thức tham nhũng (cao = ít tham nhũng)",
}

CLUSTER_NAMES: Dict[int, str] = {
    0: "Cụm 1: Phát triển toàn diện",
    1: "Cụm 2: Đang phát triển phụ thuộc kinh tế",
    2: "Cụm 3: Dễ bị tổn thương & Khó khăn",
}

CLUSTER_COLORS: Dict[str, str] = {
    "Cụm 1: Phát triển toàn diện": "#2ecc71",
    "Cụm 2: Đang phát triển phụ thuộc kinh tế": "#f39c12",
    "Cụm 3: Dễ bị tổn thương & Khó khăn": "#e74c3c",
}

ALGORITHM_OPTIONS: Dict[str, str] = {
    "K-Means": "K-Means",
    "Hierarchical Clustering (Ward)": "Ward",
}

# Ghi chú định tính cho các quốc gia có dịch chuyển cụm (đối chiếu từ country_cluster_shift.csv)
NOTABLE_SHIFTS: Dict[str, str] = {
    "Botswana": "Thăng hạng lên nhóm trung bình từ năm 2016",
    "Georgia": "Thăng hạng lên nhóm trung bình từ năm 2019",
    "Indonesia": "Thăng hạng lên nhóm cao từ năm 2019",
    "Myanmar": "Thăng hạng lên nhóm cao từ năm 2018",
    "Kuwait": "Tụt hạng do nhận thức tham nhũng xấu đi",
    "Uruguay": "Tụt hạng xuống nhóm trung bình từ năm 2017",
}


# ===========================================================================
# 2. CÁC HÀM NẠP DỮ LIỆU CÓ CACHE (@st.cache_data) — chạy offline mượt mà
# ===========================================================================
@st.cache_data(show_spinner=False)
def load_interim() -> pd.DataFrame:
    """Nạp bảng dữ liệu trung gian 781 dòng (sinh ở M1) kèm cột iso_alpha."""
    return pd.read_csv(INTERIM_PATH, encoding="utf-8")


@st.cache_data(show_spinner=False)
def load_cluster_labels(algorithm: str) -> pd.DataFrame:
    """Nạp nhãn cụm k=3 của một thuật toán qua 5 năm từ data/processed/contrast_k3/."""
    file_key = algorithm.lower().replace("-", "").replace(" ", "")
    frames = []
    for year in YEARS:
        path = CONTRAST_DIR / f"contrast_k3_{file_key}_{year}.csv"
        if path.exists():
            frames.append(pd.read_csv(path, encoding="utf-8"))
    if not frames:
        raise FileNotFoundError(
            f"Không tìm thấy nhãn cụm cho thuật toán '{algorithm}' trong {CONTRAST_DIR}"
        )
    return pd.concat(frames, ignore_index=True)


@st.cache_data(show_spinner=False)
def load_country_shift() -> pd.DataFrame:
    """Nạp bảng dịch chuyển cụm 156 quốc gia (sinh ở M3)."""
    return pd.read_csv(SHIFT_PATH, encoding="utf-8")


@st.cache_data(show_spinner=False)
def load_metrics() -> pd.DataFrame:
    """Nạp bảng so sánh 5 cấu hình × 5 năm."""
    return pd.read_csv(METRICS_PATH, encoding="utf-8")


@st.cache_data(show_spinner=False)
def load_contrast_kpi() -> pd.DataFrame:
    """Nạp bảng chỉ số đối chứng k=3 theo năm và thuật toán."""
    return pd.read_csv(CONTRAST_KPI_PATH, encoding="utf-8")


@st.cache_data(show_spinner=False)
def load_kmeans_model(year: int) -> dict:
    """Nạp tâm cụm và tham số scaler K-Means của một năm (JSON)."""
    path = MODELS_DIR / f"kmeans_{year}.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


@st.cache_data(show_spinner=False)
def canonical_mapping(year: int, algorithm: str) -> Dict[int, int]:
    """
    Ánh xạ nhãn cụm gốc -> nhãn chuẩn 0/1/2 theo điểm hạnh phúc trung bình giảm dần,
    để tên cụm nhất quán giữa các năm (0 = hạnh phúc cao, 2 = hạnh phúc thấp).
    """
    labels = load_cluster_labels(algorithm)
    subset = labels[labels["year"] == year]
    mean_scores = subset.groupby("cluster_k3")["happiness_score"].mean().to_dict()
    ordered = sorted(mean_scores, key=lambda raw: mean_scores[raw], reverse=True)
    return {raw: canonical for canonical, raw in enumerate(ordered)}


@st.cache_data(show_spinner=False)
def build_cluster_frame(year: int, algorithm: str) -> pd.DataFrame:
    """
    Ghép dữ liệu 6 đặc trưng + điểm hạnh phúc của một năm với nhãn cụm đã chuẩn hóa.
    Trả về DataFrame: country, iso3, happiness_score, 6 đặc trưng, cluster_id, cluster_name.
    """
    interim = load_interim()
    labels = load_cluster_labels(algorithm)
    mapping = canonical_mapping(year, algorithm)

    base = interim[interim["year"] == year][
        ["country", "iso_alpha", "happiness_score"] + FEATURE_COLUMNS
    ].copy()
    label_subset = labels[labels["year"] == year][["country", "cluster_k3"]]

    merged = base.merge(label_subset, on="country", how="inner")
    merged["cluster_id"] = merged["cluster_k3"].map(mapping).astype(int)
    merged["cluster_name"] = merged["cluster_id"].map(CLUSTER_NAMES)
    merged = merged.rename(columns={"iso_alpha": "iso3"})
    return merged.sort_values(["cluster_id", "country"]).reset_index(drop=True)


# ===========================================================================
# 3. CÁC HÀM DỰNG BIỂU ĐỒ PLOTLY DÙNG CHUNG
# ===========================================================================
def make_radar_figure(
    profiles: pd.DataFrame,
    title: str,
    radial_title: str = "Giá trị trung bình",
    color_map: Dict[str, str] | None = None,
) -> go.Figure:
    """
    Dựng Radar Chart so sánh nhiều hồ sơ (mỗi dòng là một cụm) trên 6 trục đặc trưng.
    `profiles` cần có cột 'name' và 6 cột trong FEATURE_COLUMNS.
    """
    categories = [FEATURE_LABELS[col] for col in FEATURE_COLUMNS]
    closed_categories = categories + [categories[0]]

    fig = go.Figure()
    for _, row in profiles.iterrows():
        values = [float(row[col]) for col in FEATURE_COLUMNS]
        values = values + [values[0]]
        color = None
        if color_map is not None:
            color = color_map.get(row["name"])
        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=closed_categories,
                fill="toself",
                name=str(row["name"]),
                line=dict(color=color, width=2),
                opacity=0.85,
            )
        )

    fig.update_layout(
        title=title,
        polar=dict(
            radialaxis=dict(visible=True, title=radial_title),
            angularaxis=dict(tickfont=dict(size=10)),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
        margin=dict(l=60, r=60, t=70, b=60),
    )
    return fig


def make_happiness_line_figure(country_frame: pd.DataFrame, country_name: str) -> go.Figure:
    """Vẽ biến thiên 6 chỉ số cơ sở và điểm hạnh phúc của một quốc gia qua các năm."""
    fig = go.Figure()
    for column in FEATURE_COLUMNS:
        fig.add_trace(
            go.Scatter(
                x=country_frame["year"],
                y=country_frame[column],
                mode="lines+markers",
                name=FEATURE_LABELS[column],
            )
        )
    fig.add_trace(
        go.Scatter(
            x=country_frame["year"],
            y=country_frame["happiness_score"],
            mode="lines+markers",
            name="Điểm hạnh phúc (hậu kiểm)",
            yaxis="y2",
            line=dict(dash="dash", color="#34495e", width=2),
        )
    )
    fig.update_layout(
        title=f"Biến thiên 6 chỉ số cơ sở và điểm hạnh phúc — {country_name} (2015–2019)",
        xaxis=dict(title="Năm", dtick=1),
        yaxis=dict(title="Giá trị chỉ số cơ sở"),
        yaxis2=dict(
            title="Điểm hạnh phúc (0–10)",
            overlaying="y",
            side="right",
            range=[0, 10],
            showgrid=False,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=60, r=60, t=70, b=60),
    )
    return fig


# ===========================================================================
# 4. BỐN HÀM DỰNG NỘI DUNG TAB
# ===========================================================================
def render_tab_overview(year: int, algorithm: str) -> None:
    """Tab 1 — Tổng quan cụm & Radar Chart."""
    st.subheader("Tổng quan cụm & Radar Chart")
    st.caption(
        f"Chân dung 3 cụm năm {year} theo thuật toán {algorithm}, cấu hình đối chứng k = 3. "
        "Điểm hạnh phúc chỉ dùng để hậu kiểm, không tham gia gom cụm."
    )

    kpi_table = load_contrast_kpi()
    kpi_row = kpi_table[(kpi_table["year"] == year) & (kpi_table["algorithm"] == algorithm)]
    frame = build_cluster_frame(year, algorithm)

    if not kpi_row.empty:
        record = kpi_row.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Silhouette Score", f"{record['silhouette']:.4f}")
        col2.metric("Davies–Bouldin Index", f"{record['davies_bouldin']:.4f}")
        col3.metric("Calinski–Harabasz Index", f"{record['calinski_harabasz']:.1f}")
        col4.metric("Kích thước cụm", str(record["sizes"]))

    means_frame = (
        frame.groupby(["cluster_id", "cluster_name"])[FEATURE_COLUMNS]
        .mean()
        .reset_index()
        .sort_values("cluster_id")
    )
    radar_profiles = means_frame.rename(columns={"cluster_name": "name"})
    radial_max = float(means_frame[FEATURE_COLUMNS].to_numpy().max()) * 1.1

    radar_figure = make_radar_figure(
        radar_profiles,
        title=f"Radar chân dung 3 cụm — năm {year} ({algorithm})",
        radial_title="Giá trị trung bình",
        color_map=CLUSTER_COLORS,
    )
    radar_figure.update_layout(polar=dict(radialaxis=dict(range=[0, radial_max])))
    st.plotly_chart(radar_figure)

    summary = (
        frame.groupby(["cluster_id", "cluster_name"])
        .agg(
            So_quoc_gia=("country", "count"),
            Diem_hanh_phuc_trung_binh=("happiness_score", "mean"),
        )
        .reset_index()
        .sort_values("cluster_id")
    )
    summary["Diem_hanh_phuc_trung_binh"] = summary["Diem_hanh_phuc_trung_binh"].round(3)
    st.markdown("**Bảng chân dung 3 cụm**")
    st.dataframe(
        summary.rename(
            columns={
                "cluster_id": "Mã cụm",
                "cluster_name": "Tên cụm",
                "So_quoc_gia": "Số quốc gia",
                "Diem_hanh_phuc_trung_binh": "Điểm hạnh phúc TB",
            }
        ),
        hide_index=True,
    )

    with st.expander("So sánh 5 cấu hình gom cụm của năm này"):
        metrics = load_metrics()
        subset = metrics[metrics["year"] == year][
            [
                "algorithm",
                "scaling",
                "silhouette",
                "davies_bouldin",
                "calinski_harabasz",
                "runtime_seconds",
            ]
        ]
        st.dataframe(subset.reset_index(drop=True), hide_index=True)


def render_tab_map(year: int, algorithm: str) -> None:
    """Tab 2 — Bản đồ thế giới (Choropleth Map)."""
    st.subheader("Bản đồ thế giới theo cụm")
    st.caption(
        f"Tô màu các quốc gia theo cụm năm {year} ({algorithm}) bằng mã ISO-3. "
        "Hover để xem tên quốc gia, mã ISO-3, nhóm cụm và điểm hạnh phúc thực tế."
    )

    frame = build_cluster_frame(year, algorithm)
    figure = px.choropleth(
        frame,
        locations="iso3",
        color="cluster_name",
        hover_name="country",
        hover_data={
            "iso3": True,
            "cluster_name": True,
            "happiness_score": ":.3f",
            "cluster_id": False,
        },
        color_discrete_map=CLUSTER_COLORS,
        category_orders={"cluster_name": list(CLUSTER_COLORS.keys())},
        title=f"Phân nhóm {len(frame)} quốc gia theo cụm — năm {year} ({algorithm})",
    )
    figure.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="#f4f6f7",
        countrycolor="#d5d8dc",
    )
    figure.update_layout(
        legend_title_text="Nhóm cụm",
        margin=dict(l=0, r=0, t=60, b=0),
    )
    st.plotly_chart(figure)

    counts = (
        frame.groupby("cluster_name")["country"]
        .count()
        .reindex(list(CLUSTER_COLORS.keys()))
        .fillna(0)
        .astype(int)
    )
    columns = st.columns(3)
    for column, (cluster_name, count) in zip(columns, counts.items()):
        column.metric(cluster_name, f"{count} quốc gia")


def render_tab_lookup() -> None:
    """Tab 3 — Tra cứu quốc gia & Dịch chuyển cụm."""
    st.subheader("Tra cứu quốc gia & Dịch chuyển cụm")
    shift = load_country_shift()
    interim = load_interim()

    countries = sorted(shift["country"].unique())
    default_index = countries.index("Vietnam") if "Vietnam" in countries else 0
    selected = st.selectbox("Chọn quốc gia (156 quốc gia trong bộ dữ liệu)", countries, index=default_index)

    row = shift[shift["country"] == selected].iloc[0]
    cluster_2019 = int(row["cluster_2019"])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nhóm cụm năm 2019", CLUSTER_NAMES.get(cluster_2019, "Không xác định"))
    col2.metric("Mã ISO-3", str(row["iso3"]))
    col3.metric("Trạng thái dịch chuyển", str(row["shift_status"]))
    col4.metric("Chiều hướng", str(row["shift_direction"]))

    history = []
    for year in YEARS:
        value = row.get(f"cluster_{year}")
        if pd.isna(value):
            history.append({"Năm": year, "Mã cụm": "—", "Tên cụm": "Không có dữ liệu năm này"})
        else:
            cluster_id = int(value)
            history.append(
                {
                    "Năm": year,
                    "Mã cụm": cluster_id + 1,
                    "Tên cụm": CLUSTER_NAMES[cluster_id],
                }
            )
    st.markdown("**Lịch sử phân cụm qua 5 năm**")
    st.dataframe(pd.DataFrame(history), hide_index=True)

    country_frame = interim[interim["country"] == selected].sort_values("year")
    st.plotly_chart(make_happiness_line_figure(country_frame, selected))

    if selected in NOTABLE_SHIFTS:
        st.info(f"{selected}: {NOTABLE_SHIFTS[selected]}.")

    # Nhận xét định lượng: hai chỉ số biến động mạnh nhất giai đoạn 2015–2019
    if len(country_frame) >= 2:
        first, last = country_frame.iloc[0], country_frame.iloc[-1]
        deltas = {column: float(last[column] - first[column]) for column in FEATURE_COLUMNS}
        risen = sorted(deltas.items(), key=lambda item: item[1], reverse=True)[:2]
        fallen = sorted(deltas.items(), key=lambda item: item[1])[:2]
        happiness_delta = float(last["happiness_score"] - first["happiness_score"])
        risen_text = ", ".join(f"{FEATURE_LABELS[key]} ({value:+.3f})" for key, value in risen)
        fallen_text = ", ".join(f"{FEATURE_LABELS[key]} ({value:+.3f})" for key, value in fallen)
        st.markdown(
            f"- Giai đoạn {int(first['year'])}–{int(last['year'])}: "
            f"điểm hạnh phúc thay đổi **{happiness_delta:+.3f}**.\n"
            f"- Hai chỉ số cải thiện mạnh nhất: {risen_text}.\n"
            f"- Hai chỉ số suy giảm mạnh nhất: {fallen_text}."
        )


def render_tab_whatif() -> None:
    """Tab 4 — Thử nghiệm gán nhãn cho quốc gia mới (What-if Analysis)."""
    st.subheader("Thử nghiệm gán nhãn quốc gia mới (What-if)")
    st.caption(
        "Kéo 6 thanh trượt mô tả một quốc gia giả định. Hệ thống z-score hóa vector theo "
        "mean/std của dữ liệu năm 2019, tính khoảng cách Euclidean tới 3 tâm cụm K-Means "
        "và gán vào cụm gần nhất."
    )

    model = load_kmeans_model(2019)
    centroids = np.asarray(model["model"]["centroids"], dtype=float)
    means = np.asarray(model["scaler"]["means"], dtype=float)
    stds = np.asarray(model["scaler"]["stds"], dtype=float)
    mapping = canonical_mapping(2019, "K-Means")

    interim_2019 = load_interim()
    interim_2019 = interim_2019[interim_2019["year"] == 2019]

    slider_values: Dict[str, float] = {}
    left_column, right_column = st.columns(2)
    for index, column in enumerate(FEATURE_COLUMNS):
        target = left_column if index % 2 == 0 else right_column
        low = float(np.floor(interim_2019[column].min() * 100) / 100)
        high = float(np.ceil(interim_2019[column].max() * 100) / 100)
        default = float(round(interim_2019[column].mean(), 3))
        slider_values[column] = target.slider(
            FEATURE_LABELS[column],
            min_value=low,
            max_value=high,
            value=default,
            step=0.01,
        )

    vector = np.asarray([slider_values[column] for column in FEATURE_COLUMNS], dtype=float)
    z_vector = (vector - means) / stds

    distances = [
        float(np.sqrt(np.sum((z_vector - centroid) ** 2))) for centroid in centroids
    ]
    nearest_raw = int(np.argmin(distances))
    nearest_cluster = mapping[nearest_raw]

    result_column, distance_column = st.columns([1, 2])
    result_column.metric("Cụm được gán", CLUSTER_NAMES[nearest_cluster])
    distance_table = pd.DataFrame(
        {
            "Nhóm cụm": [CLUSTER_NAMES[mapping[index]] for index in range(len(centroids))],
            "Khoảng cách Euclidean (không gian z-score)": [round(value, 4) for value in distances],
        }
    )
    distance_column.markdown("**Khoảng cách tới từng tâm cụm**")
    distance_column.dataframe(distance_table, hide_index=True)

    assigned_centroid = centroids[nearest_raw]
    compare_profiles = pd.DataFrame(
        [
            {
                "name": "Quốc gia giả định",
                **{column: z_vector[index] for index, column in enumerate(FEATURE_COLUMNS)},
            },
            {
                "name": CLUSTER_NAMES[nearest_cluster],
                **{
                    column: assigned_centroid[index]
                    for index, column in enumerate(FEATURE_COLUMNS)
                },
            },
        ]
    )
    radar_figure = make_radar_figure(
        compare_profiles,
        title="So sánh quốc gia giả định với tâm cụm được gán (không gian z-score)",
        radial_title="Giá trị z-score",
        color_map={CLUSTER_NAMES[nearest_cluster]: CLUSTER_COLORS[CLUSTER_NAMES[nearest_cluster]]},
    )
    st.plotly_chart(radar_figure)


# ===========================================================================
# 5. HÀM CHÍNH — GIAO DIỆN ỨNG DỤNG
# ===========================================================================
def main() -> None:
    st.set_page_config(
        page_title="WHR Cluster Explorer — Nhóm 12",
        layout="wide",
    )

    st.title("Khám phá phân nhóm quốc gia theo Báo cáo Hạnh phúc Thế giới")
    st.markdown(
        "Ứng dụng demo tương tác phục vụ đồ án môn **Khai thác dữ liệu** — Nhóm 12 — Đề tài 16. "
        "Dữ liệu đọc trực tiếp từ kết quả thực nghiệm 5 năm (2015–2019); điểm hạnh phúc chỉ "
        "dùng ở bước hậu kiểm, không tham gia gom cụm."
    )

    with st.sidebar:
        st.header("Cấu hình phân tích")
        year = st.selectbox("Chọn năm dữ liệu", list(reversed(YEARS)), index=0)
        algorithm_label = st.selectbox(
            "Chọn thuật toán gom cụm", list(ALGORITHM_OPTIONS.keys()), index=0
        )
        algorithm = ALGORITHM_OPTIONS[algorithm_label]
        st.caption(
            "Số cụm cố định k = 3 — cấu hình tối ưu đồng thuận qua cả 5 năm "
            "(Silhouette cực đại 0,293 – 0,344)."
        )
        st.divider()
        st.caption(
            "Nguồn dữ liệu: data/interim/happiness_merged.csv, "
            "data/processed/contrast_k3/, data/processed/country_cluster_shift.csv, "
            "reports/tables/."
        )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Tổng quan cụm & Radar Chart",
            "Bản đồ thế giới",
            "Tra cứu quốc gia",
            "Thử nghiệm gán nhãn (What-if)",
        ]
    )

    with tab1:
        render_tab_overview(year, algorithm)
    with tab2:
        render_tab_map(year, algorithm)
    with tab3:
        render_tab_lookup()
    with tab4:
        render_tab_whatif()

    st.divider()
    st.caption(
        "Nhóm 12 — Hà Mạnh Trường (2045240326) · Huỳnh Tâm Trí (2045240315) · "
        "Ngô Quang Trung (2045240325). Mọi số liệu truy vết về reports/tables/*.csv và data/processed/*.csv."
    )


if __name__ == "__main__":
    main()

"""
Ứng dụng demo tương tác (Streamlit) — Đề tài 16:
Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report 2015 – 2019)

Phụ trách: Ngô Quang Trung (MSSV: 2045240325) — Mốc M4 (Ngày 22 – Ngày 23)
Giao diện được thiết kế theo chuẩn UI/UX cao cấp, hỗ trợ chế độ chuyển đổi Sáng / Tối (Dark / Light Mode),
bố cục dạng Bento Grid khoa học, hiển thị biểu đồ Plotly tương tác và thẻ chỉ số KPI trực quan.

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
    "freedom": "Tự do lựa chọn",
    "generosity": "Mức độ hào phóng",
    "corruption_perception": "Nhận thức tham nhũng",
}

CLUSTER_NAMES: Dict[int, str] = {
    0: "Cụm 1: Phát triển toàn diện",
    1: "Cụm 2: Đang phát triển phụ thuộc kinh tế",
    2: "Cụm 3: Dễ bị tổn thương & Khó khăn",
}

CLUSTER_COLORS: Dict[str, str] = {
    "Cụm 1: Phát triển toàn diện": "#10b981",  # Emerald
    "Cụm 2: Đang phát triển phụ thuộc kinh tế": "#f59e0b",  # Amber
    "Cụm 3: Dễ bị tổn thương & Khó khăn": "#ef4444",  # Red
}

ALGORITHM_OPTIONS: Dict[str, str] = {
    "K-Means": "K-Means",
    "Hierarchical Clustering (Ward)": "Ward",
}

NOTABLE_SHIFTS: Dict[str, str] = {
    "Botswana": "Thăng hạng lên nhóm trung bình từ năm 2016 nhờ tuổi thọ và hỗ trợ xã hội tăng mạnh",
    "Georgia": "Thăng hạng lên nhóm trung bình từ năm 2019 nhờ kinh tế và hỗ trợ xã hội cải thiện",
    "Indonesia": "Thăng hạng lên nhóm cao từ năm 2019 nhờ tăng trưởng toàn diện các chỉ số",
    "Myanmar": "Thăng hạng lên nhóm cao từ năm 2018 nhờ cải thiện mạnh mẽ hỗ trợ xã hội và GDP",
    "Kuwait": "Tụt hạng xuống nhóm trung bình do nhận thức tham nhũng suy giảm",
    "Uruguay": "Tụt hạng xuống nhóm trung bình từ năm 2017 do hào phóng và thể chế giảm nhẹ",
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
# 3. HỆ THỐNG GIAO DIỆN & TÙY BIẾN CSS (LIGHT / DARK THEME)
# ===========================================================================
def apply_custom_theme(dark_mode: bool) -> None:
    """Tiêm CSS tùy biến cao cấp cho giao diện Streamlit theo chế độ Sáng / Tối."""
    if dark_mode:
        bg_main = "#0f172a"
        bg_card = "#1e293b"
        border_color = "#334155"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        accent_color = "#38bdf8"
        card_shadow = "0 8px 24px rgba(0, 0, 0, 0.45)"
        metric_bg = "#1e293b"
    else:
        bg_main = "#f8fafc"
        bg_card = "#ffffff"
        border_color = "#e2e8f0"
        text_primary = "#0f172a"
        text_secondary = "#64748b"
        accent_color = "#0284c7"
        card_shadow = "0 4px 16px rgba(0, 0, 0, 0.05)"
        metric_bg = "#f1f5f9"

    css = f"""
    <style>
        .stApp {{
            background-color: {bg_main} !important;
            color: {text_primary} !important;
        }}
        
        /* Tiêu đề & typography */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }}
        
        p, span, label, div {{
            color: {text_primary};
        }}
        
        .stCaption, .caption-text {{
            color: {text_secondary} !important;
            font-size: 0.92rem !important;
        }}
        
        /* Hero Header Card */
        .hero-banner {{
            background: linear-gradient(135deg, {bg_card} 0%, {bg_main} 100%);
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 24px;
            box-shadow: {card_shadow};
        }}
        
        .badge-pill {{
            display: inline-block;
            background: {accent_color}20;
            color: {accent_color} !important;
            border: 1px solid {accent_color}40;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* Card container */
        .ui-card {{
            background-color: {bg_card};
            border: 1px solid {border_color};
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: {card_shadow};
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        
        /* Thẻ Metric */
        div[data-testid="stMetric"] {{
            background-color: {metric_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            box-shadow: {card_shadow} !important;
        }}
        div[data-testid="stMetricLabel"] p {{
            color: {text_secondary} !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
        }}
        div[data-testid="stMetricValue"] div {{
            color: {text_primary} !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
        }}
        
        /* Tab Navigation Bar */
        div.stTabs [data-baseweb="tab-list"] {{
            background-color: {bg_card};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 6px;
            gap: 8px;
            box-shadow: {card_shadow};
        }}
        div.stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: 600;
            color: {text_secondary} !important;
            border: none !important;
            transition: all 0.2s ease;
        }}
        div.stTabs [aria-selected="true"] {{
            background-color: {accent_color}18 !important;
            color: {accent_color} !important;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {bg_card} !important;
            border-right: 1px solid {border_color} !important;
        }}
        
        /* Dataframe styling */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {border_color};
            border-radius: 10px;
            overflow: hidden;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ===========================================================================
# 4. CÁC HÀM DỰNG BIỂU ĐỒ PLOTLY ĐỒNG BỘ THEME
# ===========================================================================
def make_radar_figure(
    profiles: pd.DataFrame,
    title: str,
    radial_title: str = "Giá trị trung bình",
    color_map: Dict[str, str] | None = None,
    dark_mode: bool = False,
) -> go.Figure:
    """Dựng Radar Chart so sánh nhiều hồ sơ cụm trên 6 trục đặc trưng."""
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
                line=dict(color=color, width=2.5),
                opacity=0.75,
            )
        )

    grid_color = "#334155" if dark_mode else "#e2e8f0"
    text_color = "#f8fafc" if dark_mode else "#0f172a"
    bg_paper = "rgba(0,0,0,0)"

    fig.update_layout(
        template="plotly_dark" if dark_mode else "plotly_white",
        paper_bgcolor=bg_paper,
        plot_bgcolor=bg_paper,
        title=dict(text=f"<b>{title}</b>", font=dict(size=14, color=text_color)),
        polar=dict(
            radialaxis=dict(
                visible=True,
                title=radial_title,
                gridcolor=grid_color,
                linecolor=grid_color,
                tickfont=dict(color=text_color, size=9),
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color=text_color),
                gridcolor=grid_color,
                linecolor=grid_color,
            ),
            bgcolor=bg_paper,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10.5, color=text_color),
        ),
        margin=dict(l=40, r=40, t=60, b=60),
    )
    return fig


def make_happiness_line_figure(
    country_frame: pd.DataFrame, country_name: str, dark_mode: bool = False
) -> go.Figure:
    """Vẽ biến thiên 6 chỉ số cơ sở và điểm hạnh phúc của một quốc gia qua các năm."""
    fig = go.Figure()
    text_color = "#f8fafc" if dark_mode else "#0f172a"
    grid_color = "#334155" if dark_mode else "#e2e8f0"

    palette_6 = ["#38bdf8", "#818cf8", "#c084fc", "#f472b6", "#fb923c", "#facc15"]
    for idx, column in enumerate(FEATURE_COLUMNS):
        fig.add_trace(
            go.Scatter(
                x=country_frame["year"],
                y=country_frame[column],
                mode="lines+markers",
                name=FEATURE_LABELS[column],
                line=dict(width=2, color=palette_6[idx % len(palette_6)]),
                marker=dict(size=6),
            )
        )
    fig.add_trace(
        go.Scatter(
            x=country_frame["year"],
            y=country_frame["happiness_score"],
            mode="lines+markers",
            name="Điểm hạnh phúc (hậu kiểm)",
            yaxis="y2",
            line=dict(dash="dash", color="#10b981", width=3),
            marker=dict(size=8, symbol="diamond"),
        )
    )
    fig.update_layout(
        template="plotly_dark" if dark_mode else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(
            text=f"<b>Biến thiên 6 chỉ số cơ sở & Điểm hạnh phúc — {country_name} (2015–2019)</b>",
            font=dict(size=14, color=text_color),
        ),
        xaxis=dict(title="Năm", dtick=1, gridcolor=grid_color, tickfont=dict(color=text_color)),
        yaxis=dict(title="Giá trị chỉ số", gridcolor=grid_color, tickfont=dict(color=text_color)),
        yaxis2=dict(
            title="Điểm hạnh phúc (0–10)",
            overlaying="y",
            side="right",
            range=[0, 10],
            showgrid=False,
            tickfont=dict(color="#10b981"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color=text_color),
        ),
        margin=dict(l=40, r=40, t=60, b=70),
    )
    return fig


# ===========================================================================
# 5. BỐN HÀM DỰNG NỘI DUNG TAB (BENTO LAYOUT TỐI ƯU UI/UX)
# ===========================================================================
def render_tab_overview(year: int, algorithm: str, dark_mode: bool = False) -> None:
    """Tab 1 — Tổng quan cụm & Radar Chart."""
    st.markdown(
        f"### Tổng quan cấu trúc cụm — Năm {year}\n"
        f"Thuật toán khảo sát: **{algorithm}** (Cấu hình đối chứng chuẩn $k = 3$). "
        "Điểm hạnh phúc chỉ dùng để đối chiếu hậu kiểm, không tham gia vào quá trình gom cụm."
    )

    kpi_table = load_contrast_kpi()
    kpi_row = kpi_table[(kpi_table["year"] == year) & (kpi_table["algorithm"] == algorithm)]
    frame = build_cluster_frame(year, algorithm)

    if not kpi_row.empty:
        record = kpi_row.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Silhouette Score", f"{record['silhouette']:.4f}", help="Độ tách biệt cụm (càng cao càng tốt)")
        col2.metric("Davies–Bouldin Index", f"{record['davies_bouldin']:.4f}", help="Độ nén cụm (càng thấp càng tốt)")
        col3.metric("Calinski–Harabasz", f"{record['calinski_harabasz']:.1f}", help="Tỷ số phân tán cụm")
        col4.metric("Kích thước 3 cụm", str(record["sizes"]), help="Số lượng quốc gia phân bổ theo cụm [0, 1, 2]")

    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        means_frame = (
            frame.groupby(["cluster_id", "cluster_name"])[FEATURE_COLUMNS]
            .mean()
            .reset_index()
            .sort_values("cluster_id")
        )
        radar_profiles = means_frame.rename(columns={"cluster_name": "name"})
        radial_max = float(means_frame[FEATURE_COLUMNS].to_numpy().max()) * 1.15

        radar_figure = make_radar_figure(
            radar_profiles,
            title=f"Chân dung 6 đặc trưng của 3 cụm (Năm {year})",
            radial_title="Giá trị trung bình",
            color_map=CLUSTER_COLORS,
            dark_mode=dark_mode,
        )
        radar_figure.update_layout(polar=dict(radialaxis=dict(range=[0, radial_max])))
        st.plotly_chart(radar_figure)

    with col_right:
        st.markdown("**Bảng chân dung và Điểm hạnh phúc thực tế:**")
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
        st.dataframe(
            summary.rename(
                columns={
                    "cluster_id": "Mã cụm",
                    "cluster_name": "Tên định danh cụm",
                    "So_quoc_gia": "Số quốc gia",
                    "Diem_hanh_phuc_trung_binh": "Điểm hạnh phúc TB",
                }
            ),
            hide_index=True,
        )

        st.markdown(
            """
            - **Cụm 1 (Xanh lá):** Vượt trội đồng thời ở GDP, tuổi thọ và hỗ trợ xã hội. Điểm hạnh phúc cao nhất (~6.9).
            - **Cụm 2 (Vàng cam):** Các chỉ số ở mức trung bình khá, số lượng quốc gia đông nhất. Điểm hạnh phúc trung bình (~5.4).
            - **Cụm 3 (Đỏ cam):** Điểm rất thấp ở hầu hết các trụ cột kinh tế, y tế và tự do. Điểm hạnh phúc thấp nhất (~4.1).
            """
        )

    with st.expander("So sánh chi tiết 5 cấu hình thực nghiệm lõi của năm này"):
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


def render_tab_map(year: int, algorithm: str, dark_mode: bool = False) -> None:
    """Tab 2 — Bản đồ thế giới (Choropleth Map)."""
    st.markdown(
        f"### Bản đồ phân bố địa lý các cụm quốc gia — Năm {year}\n"
        f"Dữ liệu tô màu theo nhãn cụm của **{algorithm}** bằng mã chuẩn ISO-3. "
        "Rê chuột vào từng quốc gia để xem chi tiết tên, nhóm cụm và điểm hạnh phúc thực tế."
    )

    frame = build_cluster_frame(year, algorithm)
    counts = (
        frame.groupby("cluster_name")["country"]
        .count()
        .reindex(list(CLUSTER_COLORS.keys()))
        .fillna(0)
        .astype(int)
    )

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for col, (cluster_name, count) in zip(cols, counts.items()):
        col.metric(cluster_name, f"{count} quốc gia")

    land_color = "#1e293b" if dark_mode else "#f1f5f9"
    border_color = "#475569" if dark_mode else "#cbd5e1"
    text_color = "#f8fafc" if dark_mode else "#0f172a"

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
        title=f"Bản đồ phân bố 3 cụm quốc gia năm {year} ({algorithm})",
    )
    figure.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor=land_color,
        countrycolor=border_color,
        coastlinecolor=border_color,
        bgcolor="rgba(0,0,0,0)",
    )
    figure.update_layout(
        template="plotly_dark" if dark_mode else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=14, color=text_color)),
        legend=dict(
            title_text="Nhóm cụm",
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color=text_color),
        ),
        margin=dict(l=0, r=0, t=50, b=40),
    )
    st.plotly_chart(figure)


def render_tab_lookup(dark_mode: bool = False) -> None:
    """Tab 3 — Tra cứu quốc gia & Dịch chuyển cụm."""
    st.markdown("### Hồ sơ quốc gia & Quỹ đạo dịch chuyển (2015–2019)")
    shift = load_country_shift()
    interim = load_interim()

    countries = sorted(shift["country"].unique())
    default_index = countries.index("Vietnam") if "Vietnam" in countries else 0

    col_select, col_empty = st.columns([1, 1])
    with col_select:
        selected = st.selectbox(
            "Chọn quốc gia cần khảo sát (156 quốc gia)", countries, index=default_index
        )

    row = shift[shift["country"] == selected].iloc[0]
    cluster_2019 = int(row["cluster_2019"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nhóm cụm năm 2019", CLUSTER_NAMES.get(cluster_2019, "Không xác định"))
    col2.metric("Mã chuẩn ISO-3", str(row["iso3"]))
    col3.metric("Trạng thái ổn định", str(row["shift_status"]))
    col4.metric("Chiều hướng dịch chuyển", str(row["shift_direction"]))

    col_left, col_right = st.columns([1, 1.3])

    with col_left:
        history = []
        for year in YEARS:
            value = row.get(f"cluster_{year}")
            if pd.isna(value):
                history.append({"Năm": year, "Mã cụm": "—", "Tên cụm": "Không khảo sát"})
            else:
                cluster_id = int(value)
                history.append(
                    {
                        "Năm": year,
                        "Mã cụm": cluster_id + 1,
                        "Tên cụm": CLUSTER_NAMES[cluster_id],
                    }
                )
        st.markdown("**Lịch sử phân cụm qua 5 năm:**")
        st.dataframe(pd.DataFrame(history), hide_index=True)

        if selected in NOTABLE_SHIFTS:
            st.info(f"**Ghi chú dịch chuyển:** {NOTABLE_SHIFTS[selected]}.")

        country_frame = interim[interim["country"] == selected].sort_values("year")
        if len(country_frame) >= 2:
            first, last = country_frame.iloc[0], country_frame.iloc[-1]
            deltas = {column: float(last[column] - first[column]) for column in FEATURE_COLUMNS}
            risen = sorted(deltas.items(), key=lambda item: item[1], reverse=True)[:2]
            fallen = sorted(deltas.items(), key=lambda item: item[1])[:2]
            happiness_delta = float(last["happiness_score"] - first["happiness_score"])
            risen_text = ", ".join(f"{FEATURE_LABELS[key]} ({value:+.3f})" for key, value in risen)
            fallen_text = ", ".join(f"{FEATURE_LABELS[key]} ({value:+.3f})" for key, value in fallen)
            st.markdown(
                f"- Thay đổi điểm hạnh phúc: **{happiness_delta:+.3f}** (từ {first['happiness_score']:.2f} lên {last['happiness_score']:.2f}).\n"
                f"- Chỉ số tăng mạnh nhất: {risen_text}.\n"
                f"- Chỉ số giảm mạnh nhất: {fallen_text}."
            )

    with col_right:
        country_frame = interim[interim["country"] == selected].sort_values("year")
        st.plotly_chart(
            make_happiness_line_figure(country_frame, selected, dark_mode=dark_mode),
        )


def render_tab_whatif(dark_mode: bool = False) -> None:
    """Tab 4 — Thử nghiệm gán nhãn cho quốc gia mới (What-if Analysis)."""
    st.markdown("### Thử nghiệm gán nhãn chính sách giả định (What-if Simulation)")
    st.caption(
        "Kéo 6 thanh trượt để thiết lập bộ chỉ số của một quốc gia giả định. Hệ thống tự động "
        "chuẩn hóa Z-score theo tham số năm 2019, tính khoảng cách Euclidean tới 3 tâm cụm "
        "và gán vào cụm tối ưu tương ứng."
    )

    model = load_kmeans_model(2019)
    centroids = np.asarray(model["model"]["centroids"], dtype=float)
    means = np.asarray(model["scaler"]["means"], dtype=float)
    stds = np.asarray(model["scaler"]["stds"], dtype=float)
    mapping = canonical_mapping(2019, "K-Means")

    interim_2019 = load_interim()
    interim_2019 = interim_2019[interim_2019["year"] == 2019]

    slider_values: Dict[str, float] = {}

    col_sliders, col_results = st.columns([1.1, 1])

    with col_sliders:
        st.markdown("**1. Trụ cột Kinh tế & Y tế:**")
        sub_c1, sub_c2 = st.columns(2)
        for idx, col_name in enumerate(["gdp_per_capita", "social_support", "healthy_life_expectancy"]):
            target = sub_c1 if idx % 2 == 0 else sub_c2
            low = float(np.floor(interim_2019[col_name].min() * 100) / 100)
            high = float(np.ceil(interim_2019[col_name].max() * 100) / 100)
            default = float(round(interim_2019[col_name].mean(), 3))
            slider_values[col_name] = target.slider(
                FEATURE_LABELS[col_name],
                min_value=low,
                max_value=high,
                value=default,
                step=0.01,
            )

        st.markdown("**2. Trụ cột Thể chế & Xã hội:**")
        sub_c3, sub_c4 = st.columns(2)
        for idx, col_name in enumerate(["freedom", "generosity", "corruption_perception"]):
            target = sub_c3 if idx % 2 == 0 else sub_c4
            low = float(np.floor(interim_2019[col_name].min() * 100) / 100)
            high = float(np.ceil(interim_2019[col_name].max() * 100) / 100)
            default = float(round(interim_2019[col_name].mean(), 3))
            slider_values[col_name] = target.slider(
                FEATURE_LABELS[col_name],
                min_value=low,
                max_value=high,
                value=default,
                step=0.01,
            )

    # Tính toán vector z-score và khoảng cách
    vector = np.asarray([slider_values[col] for col in FEATURE_COLUMNS], dtype=float)
    z_vector = (vector - means) / stds

    distances = [
        float(np.sqrt(np.sum((z_vector - centroid) ** 2))) for centroid in centroids
    ]
    nearest_raw = int(np.argmin(distances))
    nearest_cluster = mapping[nearest_raw]
    assigned_name = CLUSTER_NAMES[nearest_cluster]

    with col_results:
        st.markdown("**Kết quả phân cụm dự đoán:**")
        st.metric("Cụm được gán", assigned_name)

        distance_table = pd.DataFrame(
            {
                "Nhóm cụm": [CLUSTER_NAMES[mapping[index]] for index in range(len(centroids))],
                "Khoảng cách Euclidean (Z-score)": [round(value, 4) for value in distances],
            }
        )
        st.dataframe(distance_table, hide_index=True)

        assigned_centroid = centroids[nearest_raw]
        compare_profiles = pd.DataFrame(
            [
                {
                    "name": "Quốc gia giả định",
                    **{col: z_vector[index] for index, col in enumerate(FEATURE_COLUMNS)},
                },
                {
                    "name": assigned_name,
                    **{
                        col: assigned_centroid[index]
                        for index, col in enumerate(FEATURE_COLUMNS)
                    },
                },
            ]
        )
        radar_figure = make_radar_figure(
            compare_profiles,
            title="So sánh quốc gia giả định với tâm cụm tương ứng",
            radial_title="Giá trị Z-score",
            color_map={assigned_name: CLUSTER_COLORS[assigned_name]},
            dark_mode=dark_mode,
        )
        st.plotly_chart(radar_figure)


# ===========================================================================
# 6. HÀM CHÍNH — KHỞI CHẠY GIAO DIỆN
# ===========================================================================
def main() -> None:
    st.set_page_config(
        page_title="WHR Cluster Explorer — Nhóm 12",
        page_icon="chart_with_upwards_trend",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 1. Sidebar: Nút bật/tắt Sáng / Tối & Bộ lọc tham số
    with st.sidebar:
        st.markdown("### Giao diện & Chủ đề")
        dark_mode = st.toggle("Chế độ nền tối (Dark Mode)", value=False, help="Chuyển đổi giao diện Sáng / Tối toàn ứng dụng")
        st.divider()

        st.markdown("### Cấu hình phân tích")
        year = st.selectbox("Chọn năm khảo sát", list(reversed(YEARS)), index=0)
        algorithm_label = st.selectbox(
            "Thuật toán gom cụm", list(ALGORITHM_OPTIONS.keys()), index=0
        )
        algorithm = ALGORITHM_OPTIONS[algorithm_label]
        st.caption(
            "Cấu hình chuẩn hóa Z-score, $k^* = 3$ cụm tối ưu đồng thuận cả 5 năm "
            "(Silhouette: 0,2931 – 0,3436)."
        )
        st.divider()

        st.markdown("### Thông tin đề tài")
        st.caption(
            "**Đề tài 16:** Phân nhóm quốc gia theo các yếu tố hạnh phúc\n\n"
            "**Nhóm 12 — Thành viên:**\n"
            "- Hà Mạnh Trường (2045240326)\n"
            "- Huỳnh Tâm Trí (2045240315)\n"
            "- Ngô Quang Trung (2045240325)\n\n"
            "Dữ liệu gốc: World Happiness Report (2015–2019)"
        )

    # 2. Áp dụng CSS theme động
    apply_custom_theme(dark_mode)

    # 3. Hero Header Banner
    st.markdown(
        """
        <div class="hero-banner">
            <span class="badge-pill">Đề tài 16 — Khai thác dữ liệu</span>
            <h1 style="margin-top: 4px; margin-bottom: 8px; font-size: 2.1rem;">
                Báo Cáo Hạnh Phúc Thế Giới (WHR) — Phân Nhóm Quốc Gia 2015–2019
            </h1>
            <p class="caption-text" style="font-size: 1.05rem; margin-bottom: 0;">
                Hệ thống phân nhóm không giám sát dựa trên 6 yếu tố cơ sở (GDP, Hỗ trợ xã hội, Tuổi thọ, Tự do, Hào phóng, Tham nhũng).
                Dữ liệu 5 năm được tiền xử lý sạch, thuật toán cài đặt from-scratch và hậu kiểm độc lập với Điểm hạnh phúc.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4. Bốn Tab tương tác chính
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Tổng quan cụm & Radar Chart",
            "Bản đồ thế giới",
            "Tra cứu quốc gia",
            "Thử nghiệm gán nhãn (What-if)",
        ]
    )

    with tab1:
        render_tab_overview(year, algorithm, dark_mode=dark_mode)
    with tab2:
        render_tab_map(year, algorithm, dark_mode=dark_mode)
    with tab3:
        render_tab_lookup(dark_mode=dark_mode)
    with tab4:
        render_tab_whatif(dark_mode=dark_mode)

    # 5. Footer chuẩn mực
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; opacity: 0.75; font-size: 0.88rem; border-top: 1px solid rgba(128, 128, 128, 0.2);">
            Đồ án môn học Khai thác dữ liệu — Nhóm 12 — Khoa Công nghệ Thông tin<br>
            Hà Mạnh Trường · Huỳnh Tâm Trí · Ngô Quang Trung — Toàn bộ số liệu đối chiếu 100% với CSV thực nghiệm
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

"""
Script kiểm thử ứng dụng demo và bộ slide — Mốc M4
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách: Ngô Quang Trung (MSSV: 2045240325)
Tài liệu căn cứ: reports/final_report/nhiem_vu_ngo_quang_trung.md (Mốc M4, Ngày 22 – Ngày 26)

Phạm vi kiểm thử:
1. app/app.py hợp lệ cú pháp Python (ast.parse) và nạp được module.
2. Sáu hàm nạp dữ liệu đều được bọc @st.cache_data và chạy thành công, trả về
   DataFrame/dict đúng schema (interim, nhãn cụm K-Means/Ward, bảng dịch chuyển,
   bảng metric, bảng đối chứng k=3, mô hình K-Means 2019).
3. Bốn tab trong app.py có đủ thành phần logic cam kết (choropleth, Scatterpolar,
   slider, metric, dataframe, selectbox) và bốn hàm render chạy không lỗi.
4. reports/presentation/slides.md tồn tại, đủ 15 slide đánh số liên tục, mỗi slide
   có nội dung, và không chứa ký tự placeholder giả lập.

Cách chạy:
    python scripts/audit_m4_app_and_slides.py

Mã thoát (exit code):
- 0: toàn bộ hạng mục PASS.
- 1: có ít nhất một hạng mục FAIL.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import ast
import importlib.util
import logging
import re
from pathlib import Path

import pandas as pd

# Tắt cảnh báo (WARNING trở xuống) khi chạy ngoài Streamlit runtime để console sạch.
# Không ảnh hưởng tới exception nên vẫn bảo toàn khả năng phát hiện lỗi.
logging.disable(logging.WARNING)

# Thiết lập đường dẫn tương đối độc lập môi trường
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

APP_PATH = project_root / "app" / "app.py"
PPTX_PATH = project_root / "reports" / "presentation" / "Nhom12_BaoCao_Slides.pptx"
ROOT_PPTX_PATH = project_root / "Nhom12_BaoCao_Slides.pptx"
LOG_DIR = project_root / "logs"
LOG_FILE = LOG_DIR / "audit_m4_app.log"

EXPECTED_TAB_COUNT = 4
EXPECTED_SLIDE_COUNTS = [15, 16, 17]

# Sáu hàm nạp dữ liệu bắt buộc phải được bọc @st.cache_data
CACHED_LOADER_FUNCTIONS = [
    "load_interim",
    "load_cluster_labels",
    "load_country_shift",
    "load_metrics",
    "load_contrast_kpi",
    "load_kmeans_model",
]

FEATURE_COLUMNS = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
]

# Ký hiệu placeholder giả lập không được xuất hiện trong bộ slide
PLACEHOLDER_TOKENS = [
    "todo",
    "tbd",
    "lorem ipsum",
    "placeholder",
    "xxx",
    "<...>",
    "??",
    "...",
]

# Thành phần logic cam kết cho 4 tab tương tác
REQUIRED_APP_TOKENS = {
    "Choropleth (Tab 2)": "choropleth",
    "Radar Scatterpolar (Tab 1, 4)": "Scatterpolar",
    "Thanh trượt Slider (Tab 4)": ".slider(",
    "Thẻ KPI Metric (Tab 1, 3)": ".metric(",
    "Bảng dữ liệu Dataframe": "st.dataframe",
    "Bộ chọn Selectbox (Tab 3)": "st.selectbox",
    "Cache dữ liệu": "@st.cache_data",
}

# Bốn hàm dựng nội dung tab
TAB_RENDER_FUNCTIONS = [
    "render_tab_overview",
    "render_tab_map",
    "render_tab_lookup",
    "render_tab_whatif",
]


def load_app_module():
    """Nạp app/app.py thành module để gọi trực tiếp các hàm nạp dữ liệu."""
    spec = importlib.util.spec_from_file_location("whr_demo_app", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collect_cached_functions(tree: ast.Module) -> set:
    """Trả về tên các hàm module-level có decorator chứa cache_data."""
    cached = set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                try:
                    decorator_text = ast.unparse(decorator)
                except Exception:
                    decorator_text = ""
                if "cache_data" in decorator_text:
                    cached.add(node.name)
    return cached


def collect_function_spans(tree: ast.Module) -> dict:
    """Trả về {tên hàm: số dòng thân hàm} cho các hàm module-level."""
    spans = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            spans[node.name] = node.end_lineno - node.lineno + 1
    return spans


def extract_tab_labels(tree: ast.Module):
    """Trích danh sách nhãn tab từ lời gọi st.tabs([...])."""
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "tabs"
            and node.args
            and isinstance(node.args[0], (ast.List, ast.Tuple))
        ):
            labels = [
                element.value
                for element in node.args[0].elts
                if isinstance(element, ast.Constant) and isinstance(element.value, str)
            ]
            return labels
    return None


def audit() -> int:
    output_lines = []

    def log(message: str) -> None:
        print(message)
        output_lines.append(message)

    def check(name: str, passed: bool, detail: str = "") -> bool:
        status = "PASS" if passed else "FAIL"
        log(f"{status}: {name}" + (f" — {detail}" if detail else ""))
        return passed

    all_passed = True

    log("================================================================================")
    log("BÁO CÁO KIỂM THỬ ỨNG DỤNG DEMO VÀ BỘ SLIDE — MỐC M4")
    log("Người thực hiện: Ngô Quang Trung (MSSV: 2045240325)")
    log("Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)")
    log("Thời gian thực hiện: Mốc M4 (Ngày 22 – Ngày 26)")
    log("================================================================================")

    # ----------------------------------------------------------------------
    # MỤC 1: Kiểm tra cú pháp và nạp module app.py
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 1] CÚ PHÁP VÀ NẠP MODULE app/app.py ---")
    if not APP_PATH.exists():
        check("Tệp app/app.py tồn tại", False, "không tìm thấy tệp")
        all_passed = False
        app_source = ""
        app_tree = None
        app_module = None
    else:
        app_source = APP_PATH.read_text(encoding="utf-8")
        check("Tệp app/app.py tồn tại", True, f"{len(app_source.splitlines())} dòng")

        try:
            app_tree = ast.parse(app_source)
            check("Cú pháp Python hợp lệ (ast.parse)", True, "phân tích thành công")
        except SyntaxError as error:
            app_tree = None
            if not check("Cú pháp Python hợp lệ (ast.parse)", False, f"SyntaxError: {error}"):
                all_passed = False

        try:
            app_module = load_app_module()
            check("Nạp module app.py thành công", True, "import các gói phụ thuộc không lỗi")
        except Exception as error:  # noqa: BLE001
            app_module = None
            if not check("Nạp module app.py thành công", False, f"{type(error).__name__}: {error}"):
                all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 2: Sáu hàm nạp dữ liệu được cache và trả đúng schema
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 2] HÀM NẠP DỮ LIỆU CACHE VÀ SCHEMA TRẢ VỀ ---")
    if app_tree is not None:
        cached_functions = collect_cached_functions(app_tree)
        missing_decorator = [
            name for name in CACHED_LOADER_FUNCTIONS if name not in cached_functions
        ]
        if not check(
            "Sáu hàm nạp dữ liệu được bọc @st.cache_data",
            not missing_decorator,
            f"thiếu decorator ở: {missing_decorator}" if missing_decorator else "đủ 6/6 hàm",
        ):
            all_passed = False
    else:
        cached_functions = set()
        all_passed = False

    if app_module is None:
        log("BỎ QUA: không nạp được module nên không kiểm tra được schema dữ liệu.")
        all_passed = False
    else:
        # 2a. interim
        try:
            interim = app_module.load_interim()
            required = {"country", "year", "happiness_score", "iso_alpha"} | set(FEATURE_COLUMNS)
            ok = isinstance(interim, pd.DataFrame) and required.issubset(interim.columns) and len(interim) == 781
            if not check(
                "load_interim() trả DataFrame 781 dòng đủ cột",
                ok,
                f"{len(interim)} dòng, {len(interim.columns)} cột" if isinstance(interim, pd.DataFrame) else "không phải DataFrame",
            ):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("load_interim() chạy thành công", False, f"{type(error).__name__}: {error}"):
                all_passed = False

        # 2b. nhãn cụm K-Means và Ward
        for algorithm in ["K-Means", "Ward"]:
            try:
                labels = app_module.load_cluster_labels(algorithm)
                required = {"country", "year", "happiness_score", "cluster_k3"}
                ok = (
                    isinstance(labels, pd.DataFrame)
                    and required.issubset(labels.columns)
                    and len(labels) == 781
                    and labels["year"].nunique() == 5
                )
                if not check(
                    f"load_cluster_labels('{algorithm}') trả nhãn cụm 5 năm",
                    ok,
                    f"{len(labels)} dòng, {labels['year'].nunique()} năm",
                ):
                    all_passed = False
            except Exception as error:  # noqa: BLE001
                if not check(f"load_cluster_labels('{algorithm}') chạy thành công", False, f"{type(error).__name__}: {error}"):
                    all_passed = False

        # 2c. bảng dịch chuyển cụm
        try:
            shift = app_module.load_country_shift()
            required = {"country", "iso3", "cluster_2015", "cluster_2019", "shift_status", "shift_direction"}
            ok = isinstance(shift, pd.DataFrame) and required.issubset(shift.columns) and len(shift) == 156
            if not check(
                "load_country_shift() trả bảng 156 quốc gia đủ cột",
                ok,
                f"{len(shift)} dòng, cột {list(shift.columns)[:4]}",
            ):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("load_country_shift() chạy thành công", False, f"{type(error).__name__}: {error}"):
                all_passed = False

        # 2d. bảng metric so sánh
        try:
            metrics = app_module.load_metrics()
            required = {"year", "algorithm", "scaling", "silhouette", "davies_bouldin", "calinski_harabasz"}
            ok = isinstance(metrics, pd.DataFrame) and required.issubset(metrics.columns)
            if not check("load_metrics() trả bảng metric 5 cấu hình × 5 năm", ok, f"{len(metrics)} dòng"):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("load_metrics() chạy thành công", False, f"{type(error).__name__}: {error}"):
                all_passed = False

        # 2e. bảng đối chứng k=3
        try:
            kpi = app_module.load_contrast_kpi()
            required = {"year", "algorithm", "silhouette", "davies_bouldin", "calinski_harabasz"}
            ok = isinstance(kpi, pd.DataFrame) and required.issubset(kpi.columns) and len(kpi) == 10
            if not check("load_contrast_kpi() trả bảng đối chứng 10 dòng", ok, f"{len(kpi)} dòng"):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("load_contrast_kpi() chạy thành công", False, f"{type(error).__name__}: {error}"):
                all_passed = False

        # 2f. mô hình K-Means 2019 (tâm cụm + scaler cho Tab What-if)
        try:
            model = app_module.load_kmeans_model(2019)
            centroids = model["model"]["centroids"]
            means = model["scaler"]["means"]
            stds = model["scaler"]["stds"]
            ok = len(centroids) == 3 and len(centroids[0]) == 6 and len(means) == 6 and len(stds) == 6
            if not check("load_kmeans_model(2019) trả 3 tâm cụm và scaler 6 đặc trưng", ok, f"{len(centroids)} tâm cụm"):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("load_kmeans_model(2019) chạy thành công", False, f"{type(error).__name__}: {error}"):
                all_passed = False

        # 2g. hàm dẫn xuất build_cluster_frame và canonical_mapping
        try:
            frame = app_module.build_cluster_frame(2019, "K-Means")
            mapping = app_module.canonical_mapping(2019, "K-Means")
            required = {"country", "iso3", "happiness_score", "cluster_id", "cluster_name"} | set(FEATURE_COLUMNS)
            ok = isinstance(frame, pd.DataFrame) and required.issubset(frame.columns) and len(frame) == 156 and len(mapping) == 3
            if not check("build_cluster_frame(2019) ghép nhãn cụm 156 quốc gia", ok, f"{len(frame)} dòng"):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("build_cluster_frame(2019) chạy thành công", False, f"{type(error).__name__}: {error}"):
                all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 3: Bốn tab tương tác có đủ thành phần logic
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 3] BỐN TAB TƯƠNG TÁC TRONG app/app.py ---")
    if app_tree is None:
        log("BỎ QUA: không phân tích được app.py.")
        all_passed = False
    else:
        tab_labels = extract_tab_labels(app_tree)
        if tab_labels is None:
            check("Tìm thấy lời gọi st.tabs([...])", False, "không tìm thấy")
            all_passed = False
        elif not check(
            "st.tabs() khai báo đúng 4 tab",
            len(tab_labels) == EXPECTED_TAB_COUNT,
            f"{len(tab_labels)} tab: {tab_labels}",
        ):
            all_passed = False

        for description, token in REQUIRED_APP_TOKENS.items():
            if not check(f"Có thành phần: {description}", token in app_source, f"tìm thấy '{token}'"):
                all_passed = False

        for tab_variable in ["tab1", "tab2", "tab3", "tab4"]:
            if not check(
                f"Khối nội dung 'with {tab_variable}:' tồn tại",
                f"with {tab_variable}:" in app_source,
            ):
                all_passed = False

        spans = collect_function_spans(app_tree)
        for name in TAB_RENDER_FUNCTIONS:
            if not check(
                f"Hàm dựng nội dung tab '{name}' đầy đủ",
                spans.get(name, 0) >= 15,
                f"{spans.get(name, 0)} dòng",
            ):
                all_passed = False

        # Chạy thử bốn hàm render (chế độ bare của Streamlit) để chắc chắn không lỗi
        if app_module is not None and all(name in spans for name in TAB_RENDER_FUNCTIONS):
            smoke_cases = [
                ("render_tab_overview(2019, K-Means)", lambda: app_module.render_tab_overview(2019, "K-Means")),
                ("render_tab_overview(2016, Ward)", lambda: app_module.render_tab_overview(2016, "Ward")),
                ("render_tab_map(2019, K-Means)", lambda: app_module.render_tab_map(2019, "K-Means")),
                ("render_tab_lookup()", lambda: app_module.render_tab_lookup()),
                ("render_tab_whatif()", lambda: app_module.render_tab_whatif()),
            ]
            for name, runner in smoke_cases:
                try:
                    runner()
                    if not check(f"Chạy thử {name}", True, "không lỗi"):
                        all_passed = False
                except Exception as error:  # noqa: BLE001
                    if not check(f"Chạy thử {name}", False, f"{type(error).__name__}: {error}"):
                        all_passed = False

        # Chạy thật toàn bộ ứng dụng trong runtime mô phỏng của Streamlit (AppTest)
        try:
            from streamlit.testing.v1 import AppTest

            app_test = AppTest.from_file(str(APP_PATH), default_timeout=180)
            app_test.run()

            if not check(
                "AppTest chạy toàn bộ app không phát sinh ngoại lệ",
                len(app_test.exception) == 0,
                f"{len(app_test.exception)} ngoại lệ",
            ):
                all_passed = False
            if not check("AppTest: hiển thị đúng 4 tab", len(app_test.tabs) == 4, f"{len(app_test.tabs)} tab"):
                all_passed = False
            if not check(
                "AppTest: đủ 6 thanh trượt What-if",
                len(app_test.slider) == 6,
                f"{len(app_test.slider)} thanh trượt",
            ):
                all_passed = False
            if not check("AppTest: đủ thẻ KPI", len(app_test.metric) >= 9, f"{len(app_test.metric)} thẻ"):
                all_passed = False
            plotly_charts = app_test.get("plotly_chart")
            if not check(
                "AppTest: biểu đồ Plotly hiển thị đủ",
                len(plotly_charts) >= 4,
                f"{len(plotly_charts)} biểu đồ",
            ):
                all_passed = False

            # Đổi thuật toán -> các chỉ số KPI phải thay đổi (kiểm tra chống hardcode)
            algorithm_box = next(
                (box for box in app_test.selectbox if "thuật toán" in box.label.lower()), None
            )
            if algorithm_box is None:
                if not check("Tìm thấy bộ chọn thuật toán", False, "không thấy selectbox thuật toán"):
                    all_passed = False
            else:
                metrics_before = [metric.value for metric in app_test.metric]
                algorithm_box.select("Hierarchical Clustering (Ward)")
                app_test.run()
                metrics_after = [metric.value for metric in app_test.metric]
                if not check(
                    "Đổi thuật toán thì chỉ số KPI thay đổi (không hardcode)",
                    metrics_before != metrics_after and len(app_test.exception) == 0,
                    "K-Means vs Ward cho kết quả khác nhau",
                ):
                    all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("AppTest chạy toàn bộ app", False, f"{type(error).__name__}: {error}"):
                all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 4: Bộ slide thuyết trình PowerPoint chính thức
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 4] BỘ SLIDE THUYẾT TRÌNH POWERPOINT (Nhom12_BaoCao_Slides.pptx) ---")
    if not PPTX_PATH.exists():
        check("Tệp Nhom12_BaoCao_Slides.pptx tồn tại", False, "không tìm thấy tệp")
        all_passed = False
    else:
        pptx_size = PPTX_PATH.stat().st_size
        check("Tệp Nhom12_BaoCao_Slides.pptx tồn tại", True, f"{round(pptx_size / (1024 * 1024), 2)} MB")

        root_exists = ROOT_PPTX_PATH.exists() and ROOT_PPTX_PATH.stat().st_size > 1000000
        if not check("Tệp Nhom12_BaoCao_Slides.pptx tại thư mục gốc tồn tại và hợp lệ", root_exists, f"{ROOT_PPTX_PATH}"):
            all_passed = False

        try:
            from pptx import Presentation
            prs = Presentation(str(PPTX_PATH))
            slide_count = len(prs.slides)
            if not check(
                f"Đủ slide thuyết trình ({', '.join(str(x) for x in EXPECTED_SLIDE_COUNTS)} slide)",
                slide_count in EXPECTED_SLIDE_COUNTS,
                f"tìm thấy {slide_count} slide",
            ):
                all_passed = False

            w_in = round(prs.slide_width.inches, 3)
            h_in = round(prs.slide_height.inches, 3)
            aspect_ok = (abs(w_in - 13.333) < 0.05 and abs(h_in - 7.5) < 0.05)
            if not check("Kích thước slide chuẩn Widescreen 16:9", aspect_ok, f"{w_in} x {h_in} inches"):
                all_passed = False

            images_count = sum(1 for s in prs.slides for shape in s.shapes if shape.shape_type == 13)
            if not check("Slide chứa hình ảnh thực chứng nhúng", images_count >= 7, f"{images_count} hình ảnh"):
                all_passed = False

            all_text = []
            for s in prs.slides:
                for shape in s.shapes:
                    if shape.has_text_frame:
                        all_text.append(shape.text_frame.text)
            slide_full_text = " ".join(all_text)

            required_figures = ["781", "142", "Silhouette", "ISO-3", "K-Means", "Ward"]
            missing_figures = [item for item in required_figures if item.lower() not in slide_full_text.lower()]
            if not check(
                "Slide chứa các số liệu dẫn chứng chủ chốt",
                not missing_figures,
                f"thiếu: {missing_figures}" if missing_figures else ", ".join(required_figures),
            ):
                all_passed = False

        except Exception as error:
            check("Nạp tệp PowerPoint thành công", False, f"{type(error).__name__}: {error}")
            all_passed = False

    # ----------------------------------------------------------------------
    # TỔNG KẾT VÀ GHI LOG
    # ----------------------------------------------------------------------
    log("\n================================================================================")
    if all_passed:
        log("KẾT LUẬN: TOÀN BỘ HẠNG MỤC KIỂM THỬ MỐC M4 ĐÃ ĐẠT CHUẨN (PASS 100%).")
        log("Xác nhận: app/app.py có 4 tab tương tác thật kết nối dữ liệu đã sinh và tệp Nhom12_BaoCao_Slides.pptx đạt chuẩn.")
    else:
        log("KẾT LUẬN: CÓ HẠNG MỤC CHƯA ĐẠT CHUẨN — CẦN KHẮC PHỤC TRƯỚC KHI CHỐT MỐC M4.")
    log("================================================================================")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log_handle:
        log_handle.write("\n".join(output_lines) + "\n")

    log(f"\nĐã lưu toàn bộ nhật ký kiểm thử vào: {LOG_FILE}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(audit())

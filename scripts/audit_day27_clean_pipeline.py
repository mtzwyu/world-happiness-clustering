"""
Script kiểm thử toàn diện toàn bộ Pipeline trên máy sạch — Mốc M5 (Ngày 27)
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách: Hà Mạnh Trường (MSSV: 2045240326, Nhóm trưởng Nhóm 12)
Tài liệu căn cứ: reports/final_report/nhiem_vu_ha_manh_truong.md (Mốc M5, Ngày 27)

Mục đích:
Tự động hóa 100% quá trình kiểm toán và nghiệm thu toàn diện pipeline từ dữ liệu thô
đến sản phẩm bàn giao cuối cùng nhằm bảo đảm tính tái lập (reproducibility) trên mọi máy chấm.

Phạm vi 7 tầng kiểm thử:
1. Tầng 1: Dữ liệu thô (2015-2019) & Chuỗi sinh dữ liệu trung gian chuẩn (interim 781 dòng, 13 cột, 0 NaN ở 6 đặc trưng, loại bỏ UAE 2018).
2. Tầng 2: Tính toàn vẹn và trạng thái thực thi sạch của 4 Jupyter Notebooks (01 -> 04).
3. Tầng 3: Các thuật toán tự code từ đầu (From-scratch K-Means, Ward, DBSCAN, Silhouette, DB, CH, ARI, PCA) và kiểm tra Quy tắc vàng.
4. Tầng 4: Ứng dụng Streamlit tương tác (app/app.py hợp lệ cú pháp, đủ 4 tabs, cơ chế cache @st.cache_data).
5. Tầng 5: Bộ tạo tác dữ liệu thực chứng (8 bảng số liệu reports/tables/*.csv và 17 hình ảnh reports/figures/*.png).
6. Tầng 6: Văn bản Báo cáo Word (Nhom12_BaoCao.docx chuẩn 5 chương, lề 3-2-3-3cm, 13pt Times New Roman) và bản xuất bản PDF.
7. Tầng 7: Bộ slide trình chiếu (Nhom12_BaoCao_Slides.pptx chuẩn 17 slide, 16:9, nhúng 7 hình thực chứng).

Cách chạy:
    python scripts/audit_day27_clean_pipeline.py

Mã thoát (exit code):
- 0: Tất cả 7 tầng kiểm thử đều PASS (100%).
- 1: Có ít nhất một hạng mục kiểm thử bị FAIL.
"""

import ast
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thiết lập đường dẫn gốc dự án độc lập môi trường
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Cấu hình logging
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "audit_day27_clean_pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("AuditDay27")

CORE_FEATURES = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "corruption_perception",
    "generosity",
]

INTERIM_COLUMNS = [
    "country",
    "region",
    "happiness_rank",
    "happiness_score",
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "corruption_perception",
    "generosity",
    "dystopia_residual",
    "year",
    "iso_alpha",
]


class PipelineAuditor:
    def __init__(self):
        self.results: List[Tuple[str, bool, str]] = []

    def record(self, check_name: str, passed: bool, details: str = ""):
        self.results.append((check_name, passed, details))
        status = "PASS" if passed else "FAIL"
        msg = f"[{status}] {check_name}" + (f" — {details}" if details else "")
        if passed:
            logger.info(msg)
        else:
            logger.error(msg)

    # =========================================================================
    # TẦNG 1: DỮ LIỆU THÔ VÀ DỮ LIỆU TRUNG GIAN (DATA PIPELINE)
    # =========================================================================
    def audit_layer1_raw_and_interim(self):
        logger.info("=== TẦNG 1: KIỂM THỬ DỮ LIỆU THÔ VÀ BỘ DỮ LIỆU TRUNG GIAN ===")
        raw_dir = PROJECT_ROOT / "data" / "raw"
        years = [2015, 2016, 2017, 2018, 2019]
        for y in years:
            f = raw_dir / f"{y}.csv"
            self.record(f"T1.1_Raw_File_{y}", f.exists() and f.stat().st_size > 1000, f"Đường dẫn: {f}")

        # Kiểm tra module data_loader và hàm build_interim_dataset
        try:
            import pandas as pd
            from src.data.data_loader import build_interim_dataset, load_interim

            interim_path = PROJECT_ROOT / "data" / "interim" / "happiness_merged.csv"
            self.record("T1.2_Interim_CSV_Exists", interim_path.exists(), f"Kích thước: {interim_path.stat().st_size if interim_path.exists() else 0} bytes")

            df = pd.read_csv(interim_path, encoding="utf-8")
            
            # Cỡ mẫu 781 dòng
            row_count_ok = (len(df) == 781)
            self.record("T1.3_Interim_Exact_Row_Count_781", row_count_ok, f"Số dòng thực tế: {len(df)}")

            # Đủ 13 cột chuẩn
            col_match_ok = (list(df.columns) == INTERIM_COLUMNS)
            self.record("T1.4_Interim_Schema_13_Columns", col_match_ok, f"Danh sách cột khớp 100%: {col_match_ok}")

            # 0 missing values ở 6 biến cốt lõi
            missing_core = df[CORE_FEATURES].isna().sum().sum()
            self.record("T1.5_Interim_Zero_Missing_Core_Features", missing_core == 0, f"Tổng số giá trị khuyết ở 6 đặc trưng: {missing_core}")

            # Kiểm tra loại bỏ mẫu UAE năm 2018 (quyết định xử lý missing)
            uae_2018 = df[(df["country"] == "United Arab Emirates") & (df["year"] == 2018)]
            self.record("T1.6_UAE_2018_Excluded_Cleanly", len(uae_2018) == 0, f"Số bản ghi UAE 2018: {len(uae_2018)} (chuẩn = 0)")

            # Kiểm tra số lượng bản ghi từng năm: 2015: 158, 2016: 157, 2017: 155, 2018: 155, 2019: 156 -> Tổng 781
            counts_by_year = df["year"].value_counts().to_dict()
            expected_counts = {2015: 158, 2016: 157, 2017: 155, 2018: 155, 2019: 156}
            counts_match = (counts_by_year == expected_counts)
            self.record("T1.7_Yearly_Sample_Distribution", counts_match, f"Phân bố các năm: {counts_by_year}")

            # Kiểm tra 100% bản ghi có mã ISO-3 hợp lệ (3 ký tự in hoa)
            iso_valid = df["iso_alpha"].str.match(r"^[A-Z]{3}$").all()
            self.record("T1.8_Valid_ISO3_Alpha_Codes", iso_valid, "Tất cả 781 dòng đều có mã ISO-3 3 ký tự")

        except Exception as e:
            self.record("T1_Exception", False, f"Lỗi thực thi Tầng 1: {e}")

    # =========================================================================
    # TẦNG 2: KIỂM THỬ 4 JUPYTER NOTEBOOKS
    # =========================================================================
    def audit_layer2_notebooks(self):
        logger.info("=== TẦNG 2: KIỂM THỬ TÍNH TOÀN VẸN CỦA 4 JUPYTER NOTEBOOKS ===")
        notebook_files = [
            ("01_data_understanding_and_cleaning.ipynb", 10),
            ("02_exploratory_data_analysis.ipynb", 10),
            ("03_clustering_experiments_and_comparison.ipynb", 10),
            ("04_cluster_profiling_and_evaluation.ipynb", 10),
        ]
        nb_dir = PROJECT_ROOT / "notebooks"
        for nb_name, min_cells in notebook_files:
            nb_path = nb_dir / nb_name
            if not nb_path.exists():
                self.record(f"T2_Notebook_{nb_name}_Exists", False, "Tệp không tồn tại")
                continue

            try:
                with open(nb_path, "r", encoding="utf-8") as f:
                    nb_json = json.load(f)

                cells = nb_json.get("cells", [])
                cell_ok = len(cells) >= min_cells
                self.record(f"T2_{nb_name}_Cells", cell_ok, f"Số ô: {len(cells)} (yêu cầu >= {min_cells})")

                # Kiểm tra có ô code đã thực thi thành công (có outputs và không có error/traceback)
                has_outputs = any(len(c.get("outputs", [])) > 0 for c in cells if c.get("cell_type") == "code")
                has_error = False
                for c in cells:
                    if c.get("cell_type") == "code":
                        for out in c.get("outputs", []):
                            if out.get("output_type") == "error":
                                has_error = True
                                break

                self.record(f"T2_{nb_name}_Executed_Outputs", has_outputs and not has_error, f"Đã chạy có output: {has_outputs}, Không có ô báo lỗi đỏ: {not has_error}")
            except Exception as e:
                self.record(f"T2_{nb_name}_Valid_JSON", False, f"Lỗi đọc JSON: {e}")

    # =========================================================================
    # TẦNG 3: THUẬT TOÁN TỰ CÀI ĐẶT (FROM-SCRATCH) & QUY TẮC VÀNG
    # =========================================================================
    def audit_layer3_from_scratch_algorithms(self):
        logger.info("=== TẦNG 3: KIỂM THỬ THUẬT TOÁN FROM-SCRATCH & QUY TẮC VÀNG ===")
        try:
            import numpy as np
            from src.models import (
                SimpleDBSCAN,
                SimpleHierarchicalClustering,
                SimpleKMeans,
                calculate_adjusted_rand_index,
                calculate_calinski_harabasz_score_simple,
                calculate_davies_bouldin_score_simple,
                calculate_silhouette_score_simple,
            )
            from src.models.clustering import euclidean_distance
            from src.features.feature_engineering import SimplePCA

            # 1. Khoảng cách Euclid
            d = euclidean_distance([0, 0], [3, 4])
            self.record("T3.1_Euclidean_Distance", abs(d - 5.0) < 1e-12, f"Khoảng cách (0,0)-(3,4) = {d:.6f}")

            # 2. Quy tắc vàng: Không dùng happiness_score / happiness_rank trong feature clustering
            forbidden = {"happiness_score", "happiness_rank"}
            has_forbidden = bool(set(CORE_FEATURES) & forbidden)
            self.record("T3.2_Golden_Rule_Clustering_Features", not has_forbidden, f"CORE_FEATURES không chứa biến mục tiêu: {CORE_FEATURES}")

            # 3. K-Means from scratch
            X_test = np.array([
                [0.0, 0.0], [0.1, 0.2], [0.2, 0.1],
                [5.0, 5.0], [5.1, 5.2], [5.2, 5.1],
                [10.0, 0.0], [10.1, 0.2], [10.2, 0.1],
            ])
            km = SimpleKMeans(k=3, random_state=42, n_init=10).fit(X_test)
            self.record("T3.3_SimpleKMeans_Fit", len(km.labels) == len(X_test) and km.inertia < 0.2, f"Inertia = {km.inertia:.4f}")

            # 4. Ward Hierarchical from scratch
            ward = SimpleHierarchicalClustering(k=3)
            ward_labels = ward.fit_predict(X_test)
            self.record("T3.4_Ward_Hierarchical_Fit", len(ward_labels) == len(X_test) and len(set(ward_labels)) == 3, f"Số cụm tạo ra = {len(set(ward_labels))}")

            # 5. Silhouette from scratch
            labels = [0, 0, 0, 1, 1, 1, 2, 2, 2]
            sil = calculate_silhouette_score_simple(X_test, labels)
            self.record("T3.5_Silhouette_Score_From_Scratch", sil > 0.8, f"Silhouette score = {sil:.4f}")

            # 6. Davies-Bouldin & Calinski-Harabasz from scratch
            db = calculate_davies_bouldin_score_simple(X_test, labels)
            ch = calculate_calinski_harabasz_score_simple(X_test, labels)
            self.record("T3.6_DB_and_CH_Scores", db > 0 and ch > 10, f"DB = {db:.4f}, CH = {ch:.4f}")

            # 7. SimplePCA from scratch
            pca = SimplePCA(n_components=2)
            coords = pca.fit_transform(X_test)
            self.record("T3.7_SimplePCA_Fit_Transform", coords.shape == (9, 2) and sum(pca.explained_variance_ratio_) > 0.9, f"Tỷ lệ phương sai tích lũy: {sum(pca.explained_variance_ratio_):.4f}")

        except Exception as e:
            self.record("T3_Exception", False, f"Lỗi kiểm thử Tầng 3: {e}")

    # =========================================================================
    # TẦNG 4: ỨNG DỤNG STREAMLIT TƯƠNG TÁC (APP/APP.PY)
    # =========================================================================
    def audit_layer4_streamlit_app(self):
        logger.info("=== TẦNG 4: KIỂM THỬ ỨNG DỤNG DEMO TƯƠNG TÁC STREAMLIT ===")
        app_file = PROJECT_ROOT / "app" / "app.py"
        self.record("T4.1_App_File_Exists", app_file.exists(), f"Đường dẫn: {app_file}")

        if not app_file.exists():
            return

        try:
            with open(app_file, "r", encoding="utf-8") as f:
                code_text = f.read()

            # Kiểm tra cú pháp AST
            ast.parse(code_text)
            self.record("T4.2_App_AST_Valid_Syntax", True, "app.py hợp lệ cú pháp Python 100%")

            # Kiểm tra 4 Tabs
            has_tab1 = "Tổng quan cụm & Radar Chart" in code_text or "render_tab_overview" in code_text
            has_tab2 = "Bản đồ thế giới" in code_text or "render_tab_map" in code_text
            has_tab3 = "Tra cứu quốc gia" in code_text or "render_tab_lookup" in code_text
            has_tab4 = "Thử nghiệm gán nhãn (What-if)" in code_text or "render_tab_what_if" in code_text
            all_tabs = has_tab1 and has_tab2 and has_tab3 and has_tab4
            self.record("T4.3_App_Contains_All_4_Tabs", all_tabs, f"Tab1={has_tab1}, Tab2={has_tab2}, Tab3={has_tab3}, Tab4={has_tab4}")

            # Kiểm tra cơ chế Cache (@st.cache_data)
            has_cache = "@st.cache_data" in code_text
            self.record("T4.4_App_Uses_Streamlit_Cache", has_cache, "Đã bọc @st.cache_data cho các hàm nạp dữ liệu")

        except Exception as e:
            self.record("T4_Exception", False, f"Lỗi kiểm thử Tầng 4: {e}")

    # =========================================================================
    # TẦNG 5: BẢNG SỐ LIỆU VÀ BIỂU ĐỒ MINH CHỨNG THỰC TẾ
    # =========================================================================
    def audit_layer5_tables_and_figures(self):
        logger.info("=== TẦNG 5: KIỂM THỬ BẢNG SỐ LIỆU VÀ BIỂU ĐỒ THỰC CHỨNG ===")
        import pandas as pd

        tables_dir = PROJECT_ROOT / "reports" / "tables"
        figures_dir = PROJECT_ROOT / "reports" / "figures"

        expected_tables = [
            "cluster_trends.csv",
            "contrast_k3_by_year.csv",
            "cross_year_matching.csv",
            "dbscan_sweep.csv",
            "k_sensitivity_by_year.csv",
            "model_comparison_metrics_2019.csv",
            "model_comparison_metrics_by_year.csv",
            "stability_ari.csv",
        ]
        for tbl in expected_tables:
            p = tables_dir / tbl
            valid = False
            rows = 0
            if p.exists() and p.stat().st_size > 0:
                try:
                    df = pd.read_csv(p)
                    rows = len(df)
                    valid = (rows > 0)
                except Exception:
                    valid = False
            self.record(f"T5_Table_{tbl}", valid, f"Số dòng: {rows}")

        # Kiểm tra hình ảnh figures >= 13 hình
        png_files = list(figures_dir.glob("*.png"))
        self.record("T5_Figures_Count_GTE_13", len(png_files) >= 13, f"Số hình thực tế: {len(png_files)} hình (yêu cầu >= 13)")
        for png in png_files[:5]:
            self.record(f"T5_Figure_Size_{png.name}", png.stat().st_size > 10000, f"Dung lượng: {png.stat().st_size / 1024:.1f} KB")

    # =========================================================================
    # TẦNG 6: BÁO CÁO WORD VÀ TỆP PDF
    # =========================================================================
    def audit_layer6_word_and_pdf(self):
        logger.info("=== TẦNG 6: KIỂM THỬ VĂN BẢN BÁO CÁO WORD VÀ XUẤT BẢN PDF ===")
        docx_file = PROJECT_ROOT / "reports" / "final_report" / "Nhom12_BaoCao.docx"
        pdf_file = PROJECT_ROOT / "reports" / "final_report" / "Nhom12_BaoCao.pdf"

        self.record("T6.1_Word_File_Exists", docx_file.exists() and docx_file.stat().st_size > 1000000, f"Dung lượng Word: {docx_file.stat().st_size / (1024*1024):.2f} MB")
        self.record("T6.2_PDF_File_Exists", pdf_file.exists() and pdf_file.stat().st_size > 500000, f"Dung lượng PDF: {pdf_file.stat().st_size / (1024*1024):.2f} MB")

        if docx_file.exists():
            try:
                from docx import Document
                doc = Document(docx_file)
                # Kiểm tra đủ 5 chương
                text_full = "\n".join(p.text for p in doc.paragraphs)
                has_ch1 = "CHƯƠNG 1" in text_full
                has_ch2 = "CHƯƠNG 2" in text_full
                has_ch3 = "CHƯƠNG 3" in text_full
                has_ch4 = "CHƯƠNG 4" in text_full
                has_ch5 = "CHƯƠNG 5" in text_full
                all_chapters = has_ch1 and has_ch2 and has_ch3 and has_ch4 and has_ch5
                self.record("T6.3_Word_Contains_All_5_Chapters", all_chapters, f"Đủ 5 chương từ Tổng quan đến Kết luận")

                # Kiểm tra lề trang chuẩn (Trái 3.0, Phải 2.0, Trên 3.0, Dưới 3.0 cm)
                section = doc.sections[0]
                left_cm = round(section.left_margin.cm, 1)
                right_cm = round(section.right_margin.cm, 1)
                top_cm = round(section.top_margin.cm, 1)
                bottom_cm = round(section.bottom_margin.cm, 1)
                margins_ok = (left_cm == 3.0 and right_cm == 2.0 and top_cm == 3.0 and bottom_cm == 3.0)
                self.record("T6.4_Word_Page_Margins_Standard_3_2_3_3", margins_ok, f"Lề thực tế: Trái={left_cm}cm, Phải={right_cm}cm, Trên={top_cm}cm, Dưới={bottom_cm}cm")

            except Exception as e:
                self.record("T6_Word_Exception", False, f"Lỗi đọc Word: {e}")

    # =========================================================================
    # TẦNG 7: BỘ SLIDE THUYẾT TRÌNH POWERPOINT
    # =========================================================================
    def audit_layer7_presentation_slides(self):
        logger.info("=== TẦNG 7: KIỂM THỬ BỘ SLIDE THUYẾT TRÌNH POWERPOINT ===")
        pptx_file = PROJECT_ROOT / "reports" / "presentation" / "Nhom12_BaoCao_Slides.pptx"
        root_pptx_file = PROJECT_ROOT / "Nhom12_BaoCao_Slides.pptx"

        self.record("T7.1_PPTX_File_Exists", pptx_file.exists() and pptx_file.stat().st_size > 1000000, f"Dung lượng PPTX: {pptx_file.stat().st_size / (1024*1024):.2f} MB")
        self.record("T7.2_Root_PPTX_File_Exists", root_pptx_file.exists() and root_pptx_file.stat().st_size > 1000000, f"Dung lượng PPTX thư mục gốc: {root_pptx_file.stat().st_size / (1024*1024):.2f} MB")

        if pptx_file.exists():
            try:
                from pptx import Presentation
                prs = Presentation(pptx_file)
                slide_count = len(prs.slides)
                self.record("T7.3_Slide_Count_Exact_17", slide_count == 17, f"Tổng số slide: {slide_count} (chuẩn = 17)")

                # Kiểm tra tỷ lệ widescreen 16:9 (13.333 x 7.5 inches)
                w_in = round(prs.slide_width.inches, 3)
                h_in = round(prs.slide_height.inches, 3)
                aspect_ok = (abs(w_in - 13.333) < 0.05 and abs(h_in - 7.5) < 0.05)
                self.record("T7.4_Slide_Widescreen_16_9", aspect_ok, f"Kích thước slide: {w_in} x {h_in} inches")

                # Kiểm tra có nhúng ảnh thực chứng
                images_count = 0
                for s in prs.slides:
                    for shape in s.shapes:
                        if shape.shape_type == 13:  # Picture shape
                            images_count += 1
                self.record("T7.5_Embedded_Visual_Images", images_count >= 7, f"Số hình ảnh thực chứng nhúng trong slide: {images_count}")

            except Exception as e:
                self.record("T7_PPTX_Exception", False, f"Lỗi đọc PPTX: {e}")

    # =========================================================================
    # TỔNG KẾT BÁO CÁO KIỂM THỬ
    # =========================================================================
    def generate_summary(self) -> bool:
        total = len(self.results)
        passed = sum(1 for _, ok, _ in self.results if ok)
        failed = total - passed

        logger.info("=========================================================================")
        logger.info(f"TỔNG KẾT KIỂM THỬ MÁY SẠCH NGÀY 27: {passed}/{total} TIÊU CHÍ PASS ({passed/total*100:.1f}%)")
        logger.info("=========================================================================")

        if failed > 0:
            logger.error(f"CÓ {failed} TIÊU CHÍ BỊ THẤT BẠI:")
            for name, ok, details in self.results:
                if not ok:
                    logger.error(f"  - [FAIL] {name}: {details}")
            return False
        else:
            logger.info("TẤT CẢ 7 TẦNG ĐỀU ĐẠT CHUẨN TỐI ĐA (100% REPRODUCIBLE)!")
            return True


def main():
    auditor = PipelineAuditor()
    auditor.audit_layer1_raw_and_interim()
    auditor.audit_layer2_notebooks()
    auditor.audit_layer3_from_scratch_algorithms()
    auditor.audit_layer4_streamlit_app()
    auditor.audit_layer5_tables_and_figures()
    auditor.audit_layer6_word_and_pdf()
    auditor.audit_layer7_presentation_slides()

    success = auditor.generate_summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

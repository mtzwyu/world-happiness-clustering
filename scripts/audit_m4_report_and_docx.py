"""
Script kiểm toán Báo cáo Word và công cụ biên dịch — Mốc M4
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách: Hà Mạnh Trường (MSSV: 2045240326)
Tài liệu căn cứ: reports/final_report/nhiem_vu_ha_manh_truong.md (Mốc M4, Ngày 22 – Ngày 26)

Phạm vi kiểm toán:
1. Chạy `reports/final_report/build_report.py` và xác nhận mã thoát bằng 0.
2. Kiểm tra hai tệp Word `bao_cao.docx` và `Nhom12_BaoCao.docx`: tồn tại, dung lượng
   trên 50 KB, nạp được bằng python-docx, đủ số đoạn văn, bảng và hình ảnh.
3. Kiểm tra định dạng in ấn: font Times New Roman 13pt, canh lề đóng gáy và viền khung trang bìa.
4. Đối chiếu tính nhất quán số liệu giữa `bao_cao.md` và các tệp `reports/tables/*.csv`
   (cỡ mẫu, số cụm tối ưu, Silhouette, ARI, phân tích phương sai, dịch chuyển cụm).
5. Kiểm tra mọi bảng/hình được nhúng trong Markdown đều trỏ tới tệp có thật.

Cách chạy:
    python scripts/audit_m4_report_and_docx.py

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

import re
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from docx import Document
from docx.oxml.ns import qn

# Thiết lập đường dẫn tương đối độc lập môi trường
project_root = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = project_root / "reports" / "final_report" / "build_report.py"
SOURCE_MD = project_root / "reports" / "final_report" / "bao_cao.md"
DOCX_PRIMARY = project_root / "reports" / "final_report" / "bao_cao.docx"
DOCX_SUBMISSION = project_root / "reports" / "final_report" / "Nhom12_BaoCao.docx"
TABLES_DIR = project_root / "reports" / "tables"
FIGURES_DIR = project_root / "reports" / "figures"
INTERIM_PATH = project_root / "data" / "interim" / "happiness_merged.csv"
SHIFT_PATH = project_root / "data" / "processed" / "country_cluster_shift.csv"
RAW_DIR = project_root / "data" / "raw"
LOG_DIR = project_root / "logs"
LOG_FILE = LOG_DIR / "audit_m4_report.log"

YEARS = [2015, 2016, 2017, 2018, 2019]
MIN_DOCX_BYTES = 50 * 1024
MIN_PARAGRAPHS = 100
MIN_TABLES = 5
MIN_IMAGES = 8

# Các cụm từ bắt buộc xuất hiện trên trang bìa
COVER_KEYWORDS = [
    "TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH",
    "KHOA CÔNG NGHỆ THÔNG TIN",
    "BỘ MÔN KHOA HỌC DỮ LIỆU",
    "KHAI THÁC DỮ LIỆU",
    "ĐỀ TÀI 16",
    "Đinh Nguyễn Trọng Nghĩa",
    "2045240326",
    "2045240315",
    "2045240325",
]

# Mẫu đường dẫn tuyệt đối gắn cứng máy cá nhân, không được xuất hiện trong mã nguồn
ABSOLUTE_PATH_PATTERNS = [r"[A-Za-z]:\\", r"/home/", r"/Users/"]


def vn_number(value, digits=4):
    """Định dạng số kiểu Việt Nam (dấu phẩy thập phân) để đối chiếu với văn bản báo cáo."""
    return f"{float(value):.{digits}f}".replace(".", ",")


def compute_anova_f(year: int) -> tuple:
    """Tính F của phân tích phương sai một nhân tố trên nhãn cụm K-Means của một năm."""
    csv_path = project_root / "data" / "processed" / "contrast_k3" / f"contrast_k3_kmeans_{year}.csv"
    frame = pd.read_csv(csv_path, encoding="utf-8")
    groups = [group["happiness_score"].to_numpy() for _, group in frame.groupby("cluster_k3")]
    k = len(groups)
    n = sum(len(group) for group in groups)
    grand_mean = np.concatenate(groups).mean()
    ss_between = sum(len(group) * (group.mean() - grand_mean) ** 2 for group in groups)
    ss_within = sum(((group - group.mean()) ** 2).sum() for group in groups)
    df_between, df_within = k - 1, n - k
    f_value = (ss_between / df_between) / (ss_within / df_within)
    return f_value, n, df_between, df_within


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
    log("BÁO CÁO KIỂM TOÁN BÁO CÁO WORD VÀ CÔNG CỤ BIÊN DỊCH — MỐC M4")
    log("Người thực hiện: Hà Mạnh Trường (MSSV: 2045240326)")
    log("Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)")
    log("Thời gian thực hiện: Mốc M4 (Ngày 22 – Ngày 26)")
    log("================================================================================")

    # ----------------------------------------------------------------------
    # MỤC 1: Chạy build_report.py
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 1] THỰC THI CÔNG CỤ BIÊN DỊCH build_report.py ---")
    if not BUILD_SCRIPT.exists():
        check("Tệp build_report.py tồn tại", False, "không tìm thấy tệp")
        all_passed = False
        run_ok = False
    else:
        check("Tệp build_report.py tồn tại", True, str(BUILD_SCRIPT.relative_to(project_root)))
        result = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(project_root),
        )
        run_ok = result.returncode == 0
        if not check(
            "build_report.py chạy thành công (exit code 0)",
            run_ok,
            f"exit code {result.returncode}",
        ):
            all_passed = False
            log("  --- stdout của build_report.py ---")
            for line in (result.stdout or "").strip().splitlines():
                log(f"  {line}")
            log("  --- stderr của build_report.py ---")
            for line in (result.stderr or "").strip().splitlines():
                log(f"  {line}")
        else:
            for line in (result.stdout or "").strip().splitlines():
                log(f"  {line}")

    # Kiểm tra mã nguồn builder dùng đường dẫn tương đối
    if BUILD_SCRIPT.exists():
        builder_source = BUILD_SCRIPT.read_text(encoding="utf-8")
        hardcoded = []
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if re.search(pattern, builder_source):
                hardcoded.append(pattern)
        if not check(
            "build_report.py không dùng đường dẫn tuyệt đối gắn cứng",
            not hardcoded,
            "không phát hiện" if not hardcoded else f"phát hiện mẫu: {hardcoded}",
        ):
            all_passed = False
        if not check(
            "build_report.py phân giải đường dẫn từ thư mục gốc dự án",
            "__file__" in builder_source and "resolve()" in builder_source,
            "dùng Path(__file__).resolve()",
        ):
            all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 2: Hai tệp Word đầu ra
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 2] HAI TỆP WORD ĐẦU RA ---")
    documents = {}
    for label, path in [("bao_cao.docx", DOCX_PRIMARY), ("Nhom12_BaoCao.docx", DOCX_SUBMISSION)]:
        if not path.exists():
            if not check(f"Tệp {label} tồn tại", False, "không tìm thấy tệp"):
                all_passed = False
            continue

        size = path.stat().st_size
        if not check(
            f"Tệp {label} dung lượng trên {MIN_DOCX_BYTES // 1024} KB",
            size > MIN_DOCX_BYTES,
            f"{size} bytes",
        ):
            all_passed = False

        try:
            document = Document(str(path))
            documents[label] = document
            if not check(f"Tệp {label} nạp được bằng python-docx", True, "OOXML hợp lệ"):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check(f"Tệp {label} nạp được bằng python-docx", False, f"{type(error).__name__}: {error}"):
                all_passed = False
            continue

        paragraph_count = len(document.paragraphs)
        table_count = len(document.tables)
        image_count = len(document.inline_shapes)
        if not check(f"Tệp {label} đủ đoạn văn (>= {MIN_PARAGRAPHS})", paragraph_count >= MIN_PARAGRAPHS, f"{paragraph_count} đoạn"):
            all_passed = False
        if not check(f"Tệp {label} đủ bảng (>= {MIN_TABLES})", table_count >= MIN_TABLES, f"{table_count} bảng"):
            all_passed = False
        if not check(f"Tệp {label} đủ hình ảnh (>= {MIN_IMAGES})", image_count >= MIN_IMAGES, f"{image_count} hình"):
            all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 3: Định dạng in ấn và trang bìa
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 3] ĐỊNH DẠNG IN ẤN VÀ TRANG BÌA ---")
    primary = documents.get("bao_cao.docx")
    if primary is None:
        log("BỎ QUA: chưa nạp được bao_cao.docx.")
        all_passed = False
    else:
        normal_style = primary.styles["Normal"]
        font_name = normal_style.font.name
        font_size = normal_style.font.size.pt if normal_style.font.size else None
        if not check(
            "Font nội dung là Times New Roman",
            font_name == "Times New Roman",
            f"font hiện tại: {font_name}",
        ):
            all_passed = False
        if not check("Cỡ chữ nội dung 13pt", font_size == 13, f"{font_size} pt"):
            all_passed = False

        body_section = primary.sections[-1]
        margins = {
            "trái": round(body_section.left_margin.cm, 2),
            "phải": round(body_section.right_margin.cm, 2),
            "trên": round(body_section.top_margin.cm, 2),
            "dưới": round(body_section.bottom_margin.cm, 2),
        }
        if not check(
            "Canh lề chuẩn (trái 3,0 cm; phải 2,0 cm; trên 2,0 cm; dưới 2,0 cm)",
            margins == {"trái": 3.0, "phải": 2.0, "trên": 2.0, "dưới": 2.0},
            str(margins),
        ):
            all_passed = False

        cover_section = primary.sections[0]
        has_page_border = cover_section._sectPr.find(qn("w:pgBorders")) is not None
        if not check("Trang bìa có viền khung (pgBorders)", has_page_border):
            all_passed = False

        footer_paragraphs = body_section.footer.paragraphs
        footer_xml = body_section.footer.paragraphs[0]._p.xml if footer_paragraphs else ""
        if not check(
            "Footer có trường đánh số trang tự động (PAGE)",
            "PAGE" in footer_xml,
            "đã chèn trường PAGE",
        ):
            all_passed = False

        document_text = "\n".join([paragraph.text for paragraph in primary.paragraphs])
        missing_keywords = [keyword for keyword in COVER_KEYWORDS if keyword not in document_text]
        if not check(
            "Trang bìa có đủ thông tin trường, học phần, đề tài, giảng viên, sinh viên",
            not missing_keywords,
            f"thiếu: {missing_keywords}" if missing_keywords else "đủ thông tin",
        ):
            all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 4: Đối chiếu số liệu giữa bao_cao.md và các CSV
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 4] ĐỐI CHIẾU SỐ LIỆU GIỮA BÁO CÁO VÀ CÁC TỆP CSV ---")
    if not SOURCE_MD.exists():
        check("Tệp bao_cao.md tồn tại", False, "không tìm thấy tệp")
        all_passed = False
        markdown_text = ""
    else:
        markdown_text = SOURCE_MD.read_text(encoding="utf-8")
        check("Tệp bao_cao.md tồn tại", True, f"{len(markdown_text.splitlines())} dòng")

        # 4a. Cấu trúc 5 chương
        chapters = re.findall(r"^# Chương (\d+):", markdown_text, flags=re.MULTILINE)
        if not check(
            "Bao_cao.md có đủ 5 chương",
            [int(value) for value in chapters] == [1, 2, 3, 4, 5],
            f"tìm thấy chương: {chapters}",
        ):
            all_passed = False

        # 4b. Cỡ mẫu interim 781 dòng
        interim = pd.read_csv(INTERIM_PATH, encoding="utf-8")
        if not check(
            "Báo cáo ghi đúng 781 bản ghi sạch",
            "781" in markdown_text and len(interim) == 781,
            f"interim {len(interim)} dòng",
        ):
            all_passed = False

        # 4c. Cỡ mẫu thô từng năm
        raw_counts = {year: len(pd.read_csv(RAW_DIR / f"{year}.csv")) for year in YEARS}
        raw_ok = raw_counts == {2015: 158, 2016: 157, 2017: 155, 2018: 156, 2019: 156}
        if not check(
            "Cỡ mẫu thô khớp 158/157/155/156/156",
            raw_ok,
            str(raw_counts),
        ):
            all_passed = False

        # 4d. Số cụm tối ưu k* = 3 cho mọi năm
        k_table = pd.read_csv(TABLES_DIR / "k_sensitivity_by_year.csv", encoding="utf-8")
        best_k = sorted(k_table.loc[k_table.groupby("year")["silhouette"].idxmax()]["k"].tolist())
        if not check(
            "Số cụm tối ưu k* = 3 cho cả năm năm",
            best_k == [3, 3, 3, 3, 3] and "k* = 3" in markdown_text,
            f"k* theo năm: {best_k}",
        ):
            all_passed = False

        # 4e. Silhouette K-Means/Z-score
        metrics = pd.read_csv(TABLES_DIR / "model_comparison_metrics_by_year.csv", encoding="utf-8")
        km = metrics[(metrics.algorithm == "K-Means") & (metrics.scaling == "standard")]
        sil_min, sil_max = km.silhouette.min(), km.silhouette.max()
        if not check(
            "Silhouette cực trị 0,2931 và 0,3436 khớp báo cáo",
            vn_number(sil_min) in markdown_text and vn_number(sil_max) in markdown_text,
            f"min {vn_number(sil_min)}, max {vn_number(sil_max)}",
        ):
            all_passed = False

        # 4f. Phân tích phương sai ANOVA
        anova_ok = True
        anova_detail = []
        for year in YEARS:
            f_value, _, _, _ = compute_anova_f(year)
            expected = vn_number(f_value, 2)
            anova_detail.append(f"{year}: F={expected}")
            if expected not in markdown_text:
                anova_ok = False
        if not check("Giá trị F của ANOVA khớp giữa báo cáo và dữ liệu", anova_ok, "; ".join(anova_detail)):
            all_passed = False

        # 4g. Phân bố dịch chuyển cụm
        shift = pd.read_csv(SHIFT_PATH, encoding="utf-8")
        shift_counts = shift.shift_status.value_counts().to_dict()
        expected_shift = {
            "Ổn định tuyệt đối": 142,
            "Biến động trung gian": 8,
            "Cải thiện nhóm (+)": 4,
            "Suy giảm nhóm (-)": 2,
        }
        if not check(
            "Phân bố dịch chuyển 142/8/4/2 khớp báo cáo",
            shift_counts == expected_shift and "142" in markdown_text and "91,0%" in markdown_text,
            str(shift_counts),
        ):
            all_passed = False

        cluster_columns = [column for column in shift.columns if column.startswith("cluster_")]
        missing_cells = int(shift[cluster_columns].isna().sum().sum())
        if not check(
            "Số ô khuyết 17 của bảng dịch chuyển khớp báo cáo",
            missing_cells == 17 and "17 ô khuyết" in markdown_text,
            f"{missing_cells} ô khuyết",
        ):
            all_passed = False

        # 4h. Khoảng cách ghép cụm liên năm
        matching = pd.read_csv(TABLES_DIR / "cross_year_matching.csv", encoding="utf-8")
        dist_min, dist_max = matching.centroid_euclidean_distance.min(), matching.centroid_euclidean_distance.max()
        if not check(
            "Khoảng cách ghép cụm 0,0571–0,4196 khớp báo cáo",
            vn_number(dist_min) in markdown_text and vn_number(dist_max) in markdown_text,
            f"{vn_number(dist_min)} – {vn_number(dist_max)}",
        ):
            all_passed = False

        # 4i. Số dòng các bảng khảo sát
        table_rows = {
            "k_sensitivity_by_year.csv": 40,
            "model_comparison_metrics_by_year.csv": 25,
            "dbscan_sweep.csv": 60,
            "stability_ari.csv": 25,
            "contrast_k3_by_year.csv": 10,
        }
        rows_ok = True
        detail_rows = []
        for file_name, expected in table_rows.items():
            actual = len(pd.read_csv(TABLES_DIR / file_name, encoding="utf-8"))
            detail_rows.append(f"{file_name}: {actual}")
            if actual != expected:
                rows_ok = False
        if not check("Số dòng các bảng khảo sát khớp thiết kế", rows_ok, "; ".join(detail_rows)):
            all_passed = False

        # 4j. Số quốc gia và mã ISO-3 trong interim
        n_countries = interim["country"].nunique()
        n_iso = interim["iso_alpha"].nunique()
        if not check(
            "Số quốc gia 164 và 162 mã ISO-3 khớp báo cáo",
            n_countries == 164 and n_iso == 162 and "164 quốc gia" in markdown_text,
            f"{n_countries} quốc gia, {n_iso} mã ISO-3",
        ):
            all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 5: Bảng và hình nhúng trong Markdown trỏ tới tệp có thật
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 5] TÍNH HỢP LỆ CỦA BẢNG VÀ HÌNH NHÚNG TRONG MARKDOWN ---")
    if markdown_text:
        table_directives = re.findall(r":::table\s*\n(.*?)\n:::", markdown_text, flags=re.DOTALL)
        figure_directives = re.findall(r":::figure\s*\n(.*?)\n:::", markdown_text, flags=re.DOTALL)

        missing_tables = []
        for directive in table_directives:
            match = re.search(r"file:\s*(\S+)", directive)
            if not match or not (TABLES_DIR / match.group(1)).exists():
                missing_tables.append(match.group(1) if match else "(thiếu file)")
        if not check(
            f"Mọi bảng nhúng ({len(table_directives)}) trỏ tới CSV có thật",
            not missing_tables,
            f"thiếu: {missing_tables}" if missing_tables else "tất cả hợp lệ",
        ):
            all_passed = False

        missing_figures = []
        for directive in figure_directives:
            match = re.search(r"file:\s*(\S+)", directive)
            if not match or not (FIGURES_DIR / match.group(1)).exists():
                missing_figures.append(match.group(1) if match else "(thiếu file)")
        if not check(
            f"Mọi hình nhúng ({len(figure_directives)}) trỏ tới PNG có thật",
            not missing_figures,
            f"thiếu: {missing_figures}" if missing_figures else "tất cả hợp lệ",
        ):
            all_passed = False

        if not check(
            "Số hình nhúng trong Markdown đạt yêu cầu tối thiểu",
            len(figure_directives) >= MIN_IMAGES,
            f"{len(figure_directives)} hình",
        ):
            all_passed = False
    else:
        all_passed = False

    # ----------------------------------------------------------------------
    # TỔNG KẾT VÀ GHI LOG
    # ----------------------------------------------------------------------
    log("\n================================================================================")
    if all_passed and run_ok:
        log("KẾT LUẬN: TOÀN BỘ HẠNG MỤC KIỂM TOÁN MỐC M4 ĐÃ ĐẠT CHUẨN (PASS 100%).")
        log("Xác nhận: build_report.py xuất đủ hai tệp Word; số liệu báo cáo khớp 100% với CSV.")
    else:
        log("KẾT LUẬN: CÓ HẠNG MỤC CHƯA ĐẠT CHUẨN — CẦN KHẮC PHỤC TRƯỚC KHI CHỐT MỐC M4.")
    log("================================================================================")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log_handle:
        log_handle.write("\n".join(output_lines) + "\n")

    log(f"\nĐã lưu toàn bộ nhật ký kiểm toán vào: {LOG_FILE}")

    return 0 if (all_passed and run_ok) else 1


if __name__ == "__main__":
    sys.exit(audit())

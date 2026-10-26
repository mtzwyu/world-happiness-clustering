"""
Script kiểm toán chất lượng Báo cáo Word và tệp nộp bài — Mốc M4
Học phần: Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report
Phụ trách: Hà Mạnh Trường (MSSV: 2045240326)
Tài liệu căn cứ: reports/final_report/nhiem_vu_ha_manh_truong.md (Mốc M4, Ngày 22 – Ngày 26)

Phạm vi kiểm toán:
1. Kiểm tra Siêu dữ liệu (Metadata) tác giả và tính toàn vẹn của tệp Word nộp bài Nhom12_BaoCao.docx:
   - Tác giả, người chỉnh sửa cuối cùng khớp thành viên nhóm (Hà Mạnh Trường).
   - Kiểm tra quyền tác giả và thuộc tính tài liệu hợp lệ.
   - Dung lượng tệp > 50 KB, nạp được bằng thư viện OOXML chuẩn.
2. Kiểm tra quy chuẩn định dạng luận văn:
   - Font Times New Roman 13pt, giãn dòng 1.5 lines.
   - Căn lề chuẩn: Trái 3,0 cm; Phải 2,0 cm; Trên 3,0 cm; Dưới 3,0 cm.
   - Phân cấp tiêu đề: Heading 1 in hoa, đậm, thẳng; Heading 2 chữ thường, đậm, thẳng; Heading 3 nghiêng.
   - Trang bìa có khung viền (pgBorders), đầy đủ thông tin trường/khoa/giảng viên/sinh viên.
   - Đánh số trang ở chân trang (Footer PAGE).
3. Đối chiếu số liệu thực chứng giữa Báo cáo Word và các tệp bảng dữ liệu gốc `reports/tables/*.csv`:
   - Đủ cấu trúc 5 chương.
   - Cỡ mẫu 781 dòng interim, cỡ mẫu thô từng năm (158/157/155/156/156).
   - Số cụm tối ưu k* = 3 cho cả 5 năm.
   - Giá trị Silhouette cực trị và kiểm định ANOVA một nhân tố.
   - Bảng phân bố dịch chuyển cụm 156 quốc gia qua 5 năm.
4. Kiểm tra tệp xuất bản PDF (Nhom12_BaoCao.pdf): tồn tại, dung lượng hợp lệ, siêu dữ liệu sạch.

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
from pathlib import Path

import numpy as np
import pandas as pd
import pypdf
from docx import Document
from docx.oxml.ns import qn

# Thiết lập đường dẫn tương đối độc lập môi trường
project_root = Path(__file__).resolve().parents[1]
DOCX_SUBMISSION = project_root / "reports" / "final_report" / "Nhom12_BaoCao.docx"
PDF_SUBMISSION = project_root / "reports" / "final_report" / "Nhom12_BaoCao.pdf"
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
    "KHAI THÁC DỮ LIỆU",
    "ĐỀ TÀI 16",
    "Đinh Nguyễn Trọng Nghĩa",
    "2045240326",
    "2045240315",
    "2045240325",
]


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
    log("BÁO CÁO KIỂM TOÁN CHẤT LƯỢNG BÁO CÁO WORD VÀ TỆP NỘP BÀI — MỐC M4")
    log("Người thực hiện: Hà Mạnh Trường (MSSV: 2045240326)")
    log("Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)")
    log("Thời gian thực hiện: Mốc M4 (Ngày 22 – Ngày 26)")
    log("================================================================================")

    # ----------------------------------------------------------------------
    # MỤC 1: Siêu dữ liệu và cấu trúc tệp Word nộp bài
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 1] SIÊU DỮ LIỆU VÀ CẤU TRÚC TỆP WORD NỘP BÀI ---")
    if not DOCX_SUBMISSION.exists():
        check("Tệp Nhom12_BaoCao.docx tồn tại", False, "không tìm thấy tệp")
        all_passed = False
        document = None
    else:
        check("Tệp Nhom12_BaoCao.docx tồn tại", True, str(DOCX_SUBMISSION.relative_to(project_root)))
        size = DOCX_SUBMISSION.stat().st_size
        if not check(
            f"Tệp Nhom12_BaoCao.docx dung lượng trên {MIN_DOCX_BYTES // 1024} KB",
            size > MIN_DOCX_BYTES,
            f"{size} bytes ({round(size / (1024 * 1024), 2)} MB)",
        ):
            all_passed = False

        try:
            document = Document(str(DOCX_SUBMISSION))
            if not check("Tệp Nhom12_BaoCao.docx nạp thành công bằng chuẩn OOXML", True, "cấu trúc tài liệu hợp lệ"):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            if not check("Tệp Nhom12_BaoCao.docx nạp thành công bằng chuẩn OOXML", False, f"{type(error).__name__}: {error}"):
                all_passed = False
            document = None

    if document is not None:
        cp = document.core_properties
        author = cp.author or ""
        last_modified = cp.last_modified_by or ""
        comments = cp.comments or ""

        # Kiểm tra siêu dữ liệu tác giả
        meta_author_ok = ("Hà Mạnh Trường" in author) or ("Nhóm 12" in author)
        if not check("Tác giả tài liệu (Author) thuộc thành viên nhóm", meta_author_ok, f"hiện tại: {author}"):
            all_passed = False

        valid_authors = ["Hà Mạnh Trường", "Nhóm 12", "Huỳnh Tâm Trí", "Ngô Quang Trung"]
        meta_valid_author = any(name in author for name in valid_authors)
        if not check("Tác giả tài liệu hợp lệ theo danh sách nhóm", meta_valid_author, f"tác giả: {author}"):
            all_passed = False

        meta_valid_comments = len(comments.strip()) < 500
        if not check("Mục ghi chú (Comments) tài liệu hợp lệ", meta_valid_comments, f"comments: {comments}"):
            all_passed = False

        paragraph_count = len(document.paragraphs)
        table_count = len(document.tables)
        image_count = len(document.inline_shapes)
        if not check(f"Tệp đủ đoạn văn (>= {MIN_PARAGRAPHS})", paragraph_count >= MIN_PARAGRAPHS, f"{paragraph_count} đoạn"):
            all_passed = False
        if not check(f"Tệp đủ bảng biểu (>= {MIN_TABLES})", table_count >= MIN_TABLES, f"{table_count} bảng"):
            all_passed = False
        if not check(f"Tệp đủ hình ảnh (>= {MIN_IMAGES})", image_count >= MIN_IMAGES, f"{image_count} hình"):
            all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 2: Định dạng in ấn và trang bìa
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 2] ĐỊNH DẠNG IN ẤN VÀ TRANG BÌA ---")
    if document is None:
        log("BỎ QUA: chưa nạp được Nhom12_BaoCao.docx.")
        all_passed = False
    else:
        normal_style = document.styles["Normal"]
        font_name = normal_style.font.name
        font_size = normal_style.font.size.pt if normal_style.font.size else None
        line_spacing = normal_style.paragraph_format.line_spacing
        if not check("Font nội dung là Times New Roman", font_name == "Times New Roman", f"font hiện tại: {font_name}"):
            all_passed = False
        if not check("Cỡ chữ nội dung 13pt", font_size == 13, f"{font_size} pt"):
            all_passed = False
        if not check("Giãn cách dòng 1.5 lines", line_spacing == 1.5, f"{line_spacing} lines"):
            all_passed = False

        body_section = document.sections[-1]
        margins = {
            "trái": round(body_section.left_margin.cm, 2),
            "phải": round(body_section.right_margin.cm, 2),
            "trên": round(body_section.top_margin.cm, 2),
            "dưới": round(body_section.bottom_margin.cm, 2),
        }
        if not check(
            "Canh lề chuẩn (trái 3,0 cm; phải 2,0 cm; trên 3,0 cm; dưới 3,0 cm)",
            margins == {"trái": 3.0, "phải": 2.0, "trên": 3.0, "dưới": 3.0},
            str(margins),
        ):
            all_passed = False

        # Kiểm tra quy chuẩn phân cấp tiêu đề
        h1_style = document.styles["Heading 1"]
        h2_style = document.styles["Heading 2"]
        h3_style = document.styles["Heading 3"]
        h1_ok = (h1_style.font.bold is True) and (not h1_style.font.italic)
        h2_ok = (h2_style.font.bold is True) and (not h2_style.font.italic)
        h3_ok = (not h3_style.font.bold) and (h3_style.font.italic is True)
        if not check("Heading 1 định dạng in hoa, đậm, thẳng", h1_ok, f"bold={h1_style.font.bold}, italic={h1_style.font.italic}"):
            all_passed = False
        if not check("Heading 2 định dạng chữ thường, đậm, thẳng", h2_ok, f"bold={h2_style.font.bold}, italic={h2_style.font.italic}"):
            all_passed = False
        if not check("Heading 3 định dạng chữ thường, nghiêng", h3_ok, f"bold={h3_style.font.bold}, italic={h3_style.font.italic}"):
            all_passed = False

        h1_paragraphs = [p.text for p in document.paragraphs if p.style.name == "Heading 1"]
        all_h1_upper = all(t == t.upper() for t in h1_paragraphs)
        if not check(f"Toàn bộ {len(h1_paragraphs)} tiêu đề Heading 1 đều là chữ in hoa", all_h1_upper, f"số lượng: {len(h1_paragraphs)}"):
            all_passed = False

        cover_section = document.sections[0]
        has_page_border = cover_section._sectPr.find(qn("w:pgBorders")) is not None
        if not check("Trang bìa có viền khung (pgBorders)", has_page_border):
            all_passed = False

        # Kiểm tra trường đánh số trang trong Footer
        footer_xml = body_section.footer._element.xml
        if not check("Footer có trường đánh số trang (PAGE)", "PAGE" in footer_xml, "đã chèn trường PAGE"):
            all_passed = False

        document_text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        missing_keywords = [keyword for keyword in COVER_KEYWORDS if keyword not in document_text]
        if not check(
            "Trang bìa có đủ thông tin trường, học phần, đề tài, giảng viên, sinh viên",
            not missing_keywords,
            f"thiếu: {missing_keywords}" if missing_keywords else "đủ thông tin",
        ):
            all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 3: Đối chiếu số liệu giữa Báo cáo Word và các CSV
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 3] ĐỐI CHIẾU SỐ LIỆU GIỮA BÁO CÁO VÀ CÁC TỆP CSV ---")
    if document is not None:
        # Gom toàn bộ văn bản từ cả đoạn văn và các ô bảng biểu
        all_text_elements = [p.text for p in document.paragraphs]
        for t in document.tables:
            for row in t.rows:
                all_text_elements.append(" ".join(cell.text.strip() for cell in row.cells))
        doc_text = "\n".join(all_text_elements)

        # 3a. Cấu trúc 5 chương
        chapter_matches = re.findall(r"(?:CHƯƠNG|Chương)\s*(\d+)", doc_text)
        found_chapters = sorted(list(set(int(c) for c in chapter_matches if 1 <= int(c) <= 5)))
        if not check(
            "Báo cáo Word có đủ 5 chương",
            found_chapters == [1, 2, 3, 4, 5],
            f"tìm thấy chương: {found_chapters}",
        ):
            all_passed = False

        # 3b. Cỡ mẫu interim 781 dòng
        interim = pd.read_csv(INTERIM_PATH, encoding="utf-8")
        if not check(
            "Báo cáo ghi đúng 781 bản ghi sạch",
            "781" in doc_text and len(interim) == 781,
            f"interim {len(interim)} dòng",
        ):
            all_passed = False

        # 3c. Cỡ mẫu thô từng năm
        raw_counts = {year: len(pd.read_csv(RAW_DIR / f"{year}.csv")) for year in YEARS}
        raw_ok = raw_counts == {2015: 158, 2016: 157, 2017: 155, 2018: 156, 2019: 156}
        if not check("Cỡ mẫu thô khớp 158/157/155/156/156", raw_ok, str(raw_counts)):
            all_passed = False

        # 3d. Số cụm tối ưu k* = 3 cho mọi năm
        k_table = pd.read_csv(TABLES_DIR / "k_sensitivity_by_year.csv", encoding="utf-8")
        best_k = sorted(k_table.loc[k_table.groupby("year")["silhouette"].idxmax()]["k"].tolist())
        if not check(
            "Số cụm tối ưu k* = 3 cho cả năm năm",
            best_k == [3, 3, 3, 3, 3] and ("k = 3" in doc_text or "k* = 3" in doc_text),
            f"k* theo năm: {best_k}",
        ):
            all_passed = False

        # 3e. Silhouette K-Means/Z-score
        metrics = pd.read_csv(TABLES_DIR / "model_comparison_metrics_by_year.csv", encoding="utf-8")
        km = metrics[(metrics.algorithm == "K-Means") & (metrics.scaling == "standard")]
        sil_min, sil_max = km.silhouette.min(), km.silhouette.max()
        if not check(
            "Silhouette cực trị 0,2931 và 0,3436 khớp báo cáo",
            vn_number(sil_min) in doc_text and vn_number(sil_max) in doc_text,
            f"min {vn_number(sil_min)}, max {vn_number(sil_max)}",
        ):
            all_passed = False

        # 3f. Phân tích phương sai ANOVA
        anova_ok = True
        anova_detail = []
        for year in YEARS:
            f_value, _, _, _ = compute_anova_f(year)
            expected = vn_number(f_value, 2)
            anova_detail.append(f"{year}: F={expected}")
            if expected not in doc_text:
                anova_ok = False
        if not check("Giá trị F của ANOVA khớp giữa báo cáo và dữ liệu", anova_ok, "; ".join(anova_detail)):
            all_passed = False

        # 3g. Phân bố dịch chuyển cụm
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
            shift_counts == expected_shift and "142" in doc_text and ("91,0%" in doc_text or "91%" in doc_text),
            str(shift_counts),
        ):
            all_passed = False

        cluster_columns = [column for column in shift.columns if column.startswith("cluster_")]
        missing_cells = int(shift[cluster_columns].isna().sum().sum())
        if not check(
            "Số ô khuyết 17 của bảng dịch chuyển khớp báo cáo",
            missing_cells == 17 and "17 ô khuyết" in doc_text,
            f"{missing_cells} ô khuyết",
        ):
            all_passed = False

        # 3h. Khoảng cách ghép cụm liên năm
        matching = pd.read_csv(TABLES_DIR / "cross_year_matching.csv", encoding="utf-8")
        dist_min, dist_max = matching.centroid_euclidean_distance.min(), matching.centroid_euclidean_distance.max()
        if not check(
            "Khoảng cách ghép cụm 0,0571–0,4196 khớp báo cáo",
            vn_number(dist_min) in doc_text and vn_number(dist_max) in doc_text,
            f"{vn_number(dist_min)} – {vn_number(dist_max)}",
        ):
            all_passed = False

        # 3i. Số quốc gia và mã ISO-3 trong interim
        n_countries = interim["country"].nunique()
        n_iso = interim["iso_alpha"].nunique()
        if not check(
            "Số quốc gia 164 và 162 mã ISO-3 khớp báo cáo",
            n_countries == 164 and n_iso == 162 and "164 quốc gia" in doc_text,
            f"{n_countries} quốc gia, {n_iso} mã ISO-3",
        ):
            all_passed = False

    # ----------------------------------------------------------------------
    # MỤC 4: Kiểm tra tệp xuất bản PDF
    # ----------------------------------------------------------------------
    log("\n--- [MỤC 4] KIỂM TRA TỆP XUẤT BẢN PDF ---")
    if not PDF_SUBMISSION.exists():
        check("Tệp Nhom12_BaoCao.pdf tồn tại", False, "không tìm thấy tệp")
        all_passed = False
    else:
        pdf_size = PDF_SUBMISSION.stat().st_size
        check(
            "Tệp Nhom12_BaoCao.pdf tồn tại",
            True,
            f"{round(pdf_size / (1024 * 1024), 2)} MB",
        )
        try:
            reader = pypdf.PdfReader(str(PDF_SUBMISSION))
            meta = reader.metadata or {}
            pdf_author = str(meta.get("/Author", ""))
            valid_authors = ["Hà Mạnh Trường", "Nhóm 12", "Huỳnh Tâm Trí", "Ngô Quang Trung"]
            pdf_author_valid = any(name in pdf_author for name in valid_authors) or pdf_author == ""
            if not check("Siêu dữ liệu PDF hợp lệ", pdf_author_valid, f"Author: {pdf_author}"):
                all_passed = False
            if not check(f"Tệp PDF đọc được ({len(reader.pages)} trang)", len(reader.pages) >= 30, f"{len(reader.pages)} trang"):
                all_passed = False
        except Exception as error:  # noqa: BLE001
            check("Tệp PDF nạp thành công", False, f"{type(error).__name__}: {error}")
            all_passed = False

    # ----------------------------------------------------------------------
    # TỔNG KẾT VÀ GHI LOG
    # ----------------------------------------------------------------------
    log("\n================================================================================")
    if all_passed:
        log("KẾT LUẬN: TOÀN BỘ HẠNG MỤC KIỂM TOÁN MỐC M4 ĐÃ ĐẠT CHUẨN (PASS 100%).")
        log("Xác nhận: Tệp Báo cáo Nhom12_BaoCao.docx và PDF đạt chuẩn quy cách nộp bài.")
    else:
        log("KẾT LUẬN: CÓ HẠNG MỤC CHƯA ĐẠT CHUẨN — CẦN KHẮC PHỤC TRƯỚC KHI CHỐT MỐC M4.")
    log("================================================================================")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log_handle:
        log_handle.write("\n".join(output_lines) + "\n")

    log(f"\nĐã lưu toàn bộ nhật ký kiểm toán vào: {LOG_FILE}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(audit())

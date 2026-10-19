"""
Script chuẩn hóa toàn diện tệp Báo cáo Word Nhom12_1_BaoCao.docx và Nhom12_BaoCao.docx
Tuân thủ tuyệt đối Quy tắc 8 trong AGENTS.md:
- Font: Times New Roman, Cỡ chữ 13pt, Giãn cách dòng 1.5 lines.
- Căn lề trang in: Trái 3.0cm, Phải 2.0cm, Trên 3.0cm, Dưới 3.0cm.
- Phân cấp tiêu đề:
  + Heading 1 (Mục / Chương): IN HOA, ĐẬM, THẲNG, 13pt
  + Heading 2 (Tiểu mục 1.1, 1.2...): chữ thường, ĐẬM, THẲNG, 13pt
  + Heading 3 (Tiểu tiết 1.1.1, 1.2.1...): chữ thường, NGHIÊNG, KHÔNG ĐẬM, 13pt
- Công thức toán học: Chuyển đổi toàn bộ sang native Microsoft Word Equation OMML (Cambria Math)
- Bảng biểu: Căn giữa trang in 16.0cm, font Times New Roman 11.5pt, line spacing 1.15 để không tràn lề.
- Tự động hóa Word COM: Làm mới Mục lục (TOC) và xuất bản PDF đối chiếu.
"""

from __future__ import annotations

import os
import re
import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import docx
from docx import Document
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import qn, nsdecls
import lxml.etree as ET
import latex2mathml.converter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = PROJECT_ROOT / "reports" / "final_report"
TARGET_DOCX = REPORT_DIR / "Nhom12_1_BaoCao.docx"
SUBMISSION_DOCX = REPORT_DIR / "Nhom12_BaoCao.docx"
TARGET_PDF = REPORT_DIR / "Nhom12_1_BaoCao.pdf"
SUBMISSION_PDF = REPORT_DIR / "Nhom12_BaoCao.pdf"

FONT_NAME = "Times New Roman"
FONT_SIZE_BODY = Pt(13)
FONT_SIZE_TABLE = Pt(11.5)
FONT_SIZE_CAPTION = Pt(12)

POSSIBLE_XSL_PATHS = [
    r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
    r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
    r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL",
    r"C:\Program Files (x86)\Microsoft Office\Office16\MML2OMML.XSL",
]

_xslt_transform = None

def get_xslt_transform():
    global _xslt_transform
    if _xslt_transform is not None:
        return _xslt_transform
    for path in POSSIBLE_XSL_PATHS:
        if os.path.exists(path):
            xslt_tree = ET.parse(path)
            _xslt_transform = ET.XSLT(xslt_tree)
            return _xslt_transform
    raise FileNotFoundError("Không tìm thấy stylesheet MML2OMML.XSL của Microsoft Office.")


def latex_to_omml_para_xml(latex_code: str) -> str:
    """Chuyển mã LaTeX thành XML khối phương trình native Word Equation <m:oMathPara>."""
    transform = get_xslt_transform()
    mathml_str = latex2mathml.converter.convert(latex_code)
    dom = ET.fromstring(mathml_str.encode("utf-8"))
    omml_elem = transform(dom).getroot()
    omml_str = ET.tostring(omml_elem, encoding="utf-8").decode("utf-8")
    wrapper = f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{omml_str}</m:oMathPara>'
    return wrapper


def create_math_p_element(latex_code: str):
    """Tạo XML element <w:p> chứa khối công thức native OMML căn giữa."""
    omml_xml = latex_to_omml_para_xml(latex_code)
    xml_str = (
        f'<w:p {nsdecls("w", "m")}>'
        f'  <w:pPr>'
        f'    <w:jc w:val="center"/>'
        f'    <w:spacing w:before="120" w:after="120" w:line="276" w:lineRule="auto"/>'
        f'    <w:ind w:firstLine="0" w:left="0"/>'
        f'  </w:pPr>'
        f'  {omml_xml}'
        f'</w:p>'
    )
    return parse_xml(xml_str)


def create_text_p_element(text: str, italic=False, bold=False):
    """Tạo XML element <w:p> chứa đoạn văn giải thích trước công thức."""
    p_elem = parse_xml(
        f'<w:p {nsdecls("w")}>'
        f'  <w:pPr>'
        f'    <w:jc w:val="both"/>'
        f'    <w:spacing w:before="60" w:after="40" w:line="360" w:lineRule="auto"/>'
        f'    <w:ind w:firstLine="720"/>'
        f'  </w:pPr>'
        f'  <w:r>'
        f'    <w:rPr>'
        f'      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>'
        f'      <w:sz w:val="26"/>'
        f'      <w:szCs w:val="26"/>'
        f'      {"<w:i/>" if italic else ""}'
        f'      {"<w:b/>" if bold else ""}'
        f'    </w:rPr>'
        f'    <w:t>{text}</w:t>'
        f'  </w:r>'
        f'</w:p>'
    )
    return p_elem


def set_run_font(run, name=FONT_NAME, size=None, bold=None, italic=None, color=None):
    """Gán font, cỡ chữ, kiểu chữ cho run bảo đảm không bị theme ghi đè."""
    run.font.name = name
    if size is not None:
        run.font.size = size
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)
    for theme_attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(theme_attr)) is not None:
            rfonts.attrib.pop(qn(theme_attr))


def force_style_font(style, name=FONT_NAME, size=None, bold=None, italic=None,
                     color=None, before=None, after=None, keep_with_next=False):
    """Thiết lập style chuẩn tránh font theme mặc định."""
    style.font.name = name
    if size is not None:
        style.font.size = size
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    if color is not None:
        style.font.color.rgb = RGBColor.from_string(color)

    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for theme_attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(theme_attr)) is not None:
            rfonts.attrib.pop(qn(theme_attr))
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)

    if before is not None:
        style.paragraph_format.space_before = before
    if after is not None:
        style.paragraph_format.space_after = after
    if keep_with_next:
        style.paragraph_format.keep_with_next = True


def apply_margins(section):
    """Căn lề chuẩn trang in: Trái 3.0cm, Phải 2.0cm, Trên 3.0cm, Dưới 3.0cm."""
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)
    section.top_margin = Cm(3.0)
    section.bottom_margin = Cm(3.0)


def standardize_report():
    print(f"Bắt đầu chuẩn hóa file Word: {TARGET_DOCX}")
    doc = Document(str(TARGET_DOCX))

    # 1. Căn lề toàn bộ các sections
    for i, section in enumerate(doc.sections):
        apply_margins(section)
        print(f"  Đã căn lề Section {i}: Trái={section.left_margin.cm:.1f}cm, Phải={section.right_margin.cm:.1f}cm, Trên={section.top_margin.cm:.1f}cm, Dưới={section.bottom_margin.cm:.1f}cm")

    # 2. Cấu hình Styles chuẩn
    force_style_font(doc.styles["Normal"], size=FONT_SIZE_BODY, bold=False, italic=False, color="000000", before=Pt(0), after=Pt(6))
    doc.styles["Normal"].paragraph_format.line_spacing = 1.5

    force_style_font(doc.styles["Heading 1"], size=FONT_SIZE_BODY, bold=True, italic=False, color="000000", before=Pt(12), after=Pt(6), keep_with_next=True)
    doc.styles["Heading 1"].paragraph_format.line_spacing = 1.5

    force_style_font(doc.styles["Heading 2"], size=FONT_SIZE_BODY, bold=True, italic=False, color="000000", before=Pt(8), after=Pt(4), keep_with_next=True)
    doc.styles["Heading 2"].paragraph_format.line_spacing = 1.5

    if "Heading 3" in doc.styles:
        force_style_font(doc.styles["Heading 3"], size=FONT_SIZE_BODY, bold=False, italic=True, color="000000", before=Pt(6), after=Pt(2), keep_with_next=True)
        doc.styles["Heading 3"].paragraph_format.line_spacing = 1.5

    for style_name in ("List Bullet", "List Number"):
        if style_name in doc.styles:
            force_style_font(doc.styles[style_name], size=FONT_SIZE_BODY, color="000000", after=Pt(2))
            doc.styles[style_name].paragraph_format.line_spacing = 1.5

    # 3. Dọn dẹp khoảng trống thừa giữa TOC và TÓM TẮT
    # Tìm đoạn "MỤC LỤC" và "TÓM TẮT"
    tom_tat_idx = None
    toc_idx = None
    for idx, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if txt == "MỤC LỤC":
            toc_idx = idx
        elif txt == "TÓM TẮT":
            tom_tat_idx = idx
            break

    if tom_tat_idx is not None and toc_idx is not None:
        # Xóa bớt các đoạn rỗng giữa TOC và TÓM TẮT
        # Để lại 1 đoạn ngắt trang sạch
        empty_paras = []
        for idx in range(toc_idx + 1, tom_tat_idx):
            p = doc.paragraphs[idx]
            if not p.text.strip() and not any(p._element.iter()):
                empty_paras.append(p)
            elif not p.text.strip():
                # Xóa style Heading nếu rỗng
                if p.style.name.startswith("Heading"):
                    p.style = doc.styles["Normal"]

        # Cho TÓM TẮT bắt đầu trang mới
        doc.paragraphs[tom_tat_idx].paragraph_format.page_break_before = True

    # 4. Duyệt và chuẩn hóa từng đoạn văn
    in_cover = True
    in_toc = False

    for idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        elem = p._element
        has_drawing = any(e.tag.endswith("drawing") for e in elem.iter())
        has_omml = any(e.tag.endswith("oMath") for e in elem.iter())

        if idx > 24:
            in_cover = False

        if text == "MỤC LỤC":
            in_toc = True
        elif text == "TÓM TẮT":
            in_toc = False

        if in_cover:
            p.paragraph_format.first_line_indent = Inches(0)
            for r in p.runs:
                set_run_font(r, name=FONT_NAME)
            continue

        if in_toc:
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.line_spacing = 1.25
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(0)
            for r in p.runs:
                set_run_font(r, name=FONT_NAME)
            continue

        p_style = p.style.name

        if p_style == "Heading 1":
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.first_line_indent = Inches(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            # Các chương chính ngắt trang đầu chương
            if any(text.startswith(c) for c in ["CHƯƠNG", "TÀI LIỆU", "PHỤ LỤC", "TÓM TẮT"]):
                p.paragraph_format.page_break_before = True
            # IN HOA
            if text and text != text.upper():
                p.text = text.upper()
            for r in p.runs:
                set_run_font(r, name=FONT_NAME, size=FONT_SIZE_BODY, bold=True, italic=False, color="000000")

        elif p_style == "Heading 2":
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.first_line_indent = Inches(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                set_run_font(r, name=FONT_NAME, size=FONT_SIZE_BODY, bold=True, italic=False, color="000000")

        elif p_style == "Heading 3":
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.first_line_indent = Inches(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                set_run_font(r, name=FONT_NAME, size=FONT_SIZE_BODY, bold=False, italic=True, color="000000")

        elif has_drawing:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.first_line_indent = Inches(0)

        elif has_omml:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.first_line_indent = Inches(0)

        elif text.startswith("Hình ") or text.startswith("Bảng "):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.line_spacing = 1.2
            for r in p.runs:
                set_run_font(r, name=FONT_NAME, size=FONT_SIZE_CAPTION, italic=True, color="000000")

        elif p_style in ("List Bullet", "List Number"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(0)
            for r in p.runs:
                set_run_font(r, name=FONT_NAME, size=FONT_SIZE_BODY, color="000000")

        else:
            if text:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.first_line_indent = Cm(1.27)
                for r in p.runs:
                    set_run_font(r, name=FONT_NAME, size=FONT_SIZE_BODY, color="000000")

    # 5. Chuẩn hóa bảng biểu
    print(f"  Chuẩn hóa {len(doc.tables)} bảng biểu...")
    for t_idx, table in enumerate(doc.tables):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for r_idx, row in enumerate(table.rows):
            is_header = (r_idx == 0)
            for cell in row.cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                tcPr = cell._tc.get_or_add_tcPr()
                tcMar = OxmlElement('w:tcMar')
                for edge in ('top', 'bottom'):
                    node = OxmlElement(f'w:{edge}')
                    node.set(qn('w:w'), '80')
                    node.set(qn('w:type'), 'dxa')
                    tcMar.append(node)
                for edge in ('left', 'right'):
                    node = OxmlElement(f'w:{edge}')
                    node.set(qn('w:w'), '120')
                    node.set(qn('w:type'), 'dxa')
                    tcMar.append(node)
                tcPr.append(tcMar)

                for p in cell.paragraphs:
                    p.paragraph_format.first_line_indent = Inches(0)
                    p.paragraph_format.line_spacing = 1.15
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        set_run_font(r, name=FONT_NAME, size=FONT_SIZE_TABLE, bold=is_header, color="000000")

    # 6. Chèn và hoàn thiện các công thức toán OMML còn thiếu
    print("  Kiểm tra và hoàn thiện các khối Equation Math native OMML...")
    insert_math_equations(doc)

    # 7. Lưu tệp đã chuẩn hóa
    doc.save(str(TARGET_DOCX))
    print(f"  Đã lưu tệp Word chuẩn hóa: {TARGET_DOCX}")

    # Đồng bộ sang tệp nộp bài Nhom12_BaoCao.docx
    shutil.copyfile(str(TARGET_DOCX), str(SUBMISSION_DOCX))
    print(f"  Đã đồng bộ sang tệp nộp bài: {SUBMISSION_DOCX}")


def insert_math_equations(doc: Document):
    """
    Chèn đầy đủ các công thức toán học native Word OMML vào các vị trí tương ứng.
    """
    # 1. Pearson Correlation
    for idx, p in enumerate(doc.paragraphs):
        if "Cặp GDP bình quân đầu người và tuổi thọ khỏe mạnh đạt r = 0,79" in p.text:
            next_p = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else None
            if next_p is None or not any(e.tag.endswith("oMath") for e in next_p._element.iter()):
                lead_p = create_text_p_element("Hệ số tương quan tuyến tính Pearson được xác định theo công thức:")
                math_p = create_math_p_element(r"r_{xy} = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2 \sum_{i=1}^n (y_i - \bar{y})^2}}")
                p._element.addnext(math_p)
                p._element.addnext(lead_p)
                print("    + Đã chèn công thức: Pearson Correlation")
            break

    # 2. Z-score and Min-Max (Section 3.2)
    for idx, p in enumerate(doc.paragraphs):
        if "Nhóm giữ lại cả ba phương án chuẩn hóa cho K-Means" in p.text and "z = (x − μ) / σ" in p.text:
            # Sửa lại đoạn văn cho mượt và chuyển công thức sang display math
            p.text = "Nhóm giữ lại cả ba phương án chuẩn hóa cho K-Means để có căn cứ thực nghiệm thay vì chọn theo cảm tính. Phương án Z-score đưa từng biến về phân phối có trung bình 0 và độ lệch chuẩn 1:"
            for r in p.runs:
                set_run_font(r, name=FONT_NAME, size=FONT_SIZE_BODY, color="000000")
            p.paragraph_format.first_line_indent = Cm(1.27)
            p.paragraph_format.line_spacing = 1.5

            math_z = create_math_p_element(r"z = \frac{x - \mu}{\sigma}")
            lead_minmax = create_text_p_element("Phương án Min-Max co giãn toàn bộ các giá trị về đoạn [0, 1]:")
            math_minmax = create_math_p_element(r"x^\prime = \frac{x - x_{\min}}{x_{\max} - x_{\min}}")
            lead_raw = create_text_p_element("Phương án Raw giữ nguyên thang đo gốc của dữ liệu. Min-Max rất nhạy với ngoại lai: một quốc gia có GDP hoặc tuổi thọ đột biến sẽ nén các quốc gia còn lại về dải hẹp.")

            # Chèn theo thứ tự sau p
            p._element.addnext(lead_raw)
            p._element.addnext(math_minmax)
            p._element.addnext(lead_minmax)
            p._element.addnext(math_z)
            print("    + Đã chèn khối công thức: Z-score & Min-Max")
            break

    # 3. K-Means Centroid Update (Section 3.3)
    for idx, p in enumerate(doc.paragraphs):
        if "Hàm mục tiêu là tổng bình phương khoảng cách trong cụm" in p.text:
            # Đoạn sau p là WCSS equation
            wcss_p = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else None
            if wcss_p is not None:
                # Kiểm tra xem đã có centroid update chưa
                after_wcss = doc.paragraphs[idx + 2] if idx + 2 < len(doc.paragraphs) else None
                if after_wcss is not None and not any("mu_k" in after_wcss.text for _ in [1]):
                    lead_c = create_text_p_element("Trong mỗi vòng lặp, tọa độ trọng tâm mới của từng cụm được cập nhật bằng trung bình cộng các điểm trong cụm:")
                    math_c = create_math_p_element(r"\mu_k = \frac{1}{|C_k|} \sum_{x_i \in C_k} x_i")
                    wcss_p._element.addnext(math_c)
                    wcss_p._element.addnext(lead_c)
                    print("    + Đã chèn công thức: K-Means Centroid Update")
            break

    # 4. DBSCAN Core Point Condition (Section 3.5)
    for idx, p in enumerate(doc.paragraphs):
        if "DBSCAN phân loại điểm theo mật độ với hai tham số eps là bán kính" in p.text:
            next_p = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else None
            if next_p is None or not any(e.tag.endswith("oMath") for e in next_p._element.iter()):
                lead_db = create_text_p_element("Tập lân cận bán kính và điều kiện điểm lõi trong thuật toán DBSCAN được xác định theo:")
                math_db = create_math_p_element(r"N_\epsilon(p) = \{q \in D \mid \text{dist}(p, q) \le \epsilon\}, \quad |N_\epsilon(p)| \ge \text{MinPts}")
                p._element.addnext(math_db)
                p._element.addnext(lead_db)
                print("    + Đã chèn công thức: DBSCAN Core Point")
            break

    # 5. Silhouette Formula (Section 3.6)
    for idx, p in enumerate(doc.paragraphs):
        if "Silhouette của điểm i so sánh khoảng cách trung bình" in p.text:
            # Đoạn kế tiếp là s(i) = (b(i) - a(i)) / max...
            s_p = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else None
            if s_p is not None and "s(i) =" in s_p.text:
                # Thay thế s_p bằng khối OMML
                s_p.text = ""
                s_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                s_p.paragraph_format.first_line_indent = Inches(0)
                s_p.paragraph_format.space_before = Pt(6)
                s_p.paragraph_format.space_after = Pt(6)
                omml_xml = latex_to_omml_para_xml(r"s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad s(i) \in [-1, 1]")
                s_p._element.append(parse_xml(omml_xml))
                print("    + Đã chuẩn hóa công thức: Silhouette s(i)")
            break

    # 6. Davies-Bouldin & Calinski-Harabasz (Section 3.6)
    for idx, p in enumerate(doc.paragraphs):
        if "Davies–Bouldin là trung bình tỉ số giữa độ phân tán nội cụm" in p.text:
            next_p = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else None
            if next_p is None or not any(e.tag.endswith("oMath") for e in next_p._element.iter()):
                p.text = "Davies–Bouldin (DB) là trung bình tỉ số độ phân tán nội cụm trên khoảng cách giữa hai tâm cụm, giá trị nhỏ hơn thể hiện cấu trúc cụm tốt hơn:"
                for r in p.runs:
                    set_run_font(r, name=FONT_NAME, size=FONT_SIZE_BODY, color="000000")
                p.paragraph_format.first_line_indent = Cm(1.27)
                p.paragraph_format.line_spacing = 1.5

                math_db = create_math_p_element(r"\text{DB} = \frac{1}{k} \sum_{i=1}^k \max_{j \ne i} \left( \frac{\sigma_i + \sigma_j}{d(c_i, c_j)} \right)")
                lead_ch = create_text_p_element("Calinski–Harabasz (CH) đo tỉ số giữa phương sai giữa cụm và phương sai trong cụm, giá trị càng lớn thể hiện cụm càng chặt chẽ:")
                math_ch = create_math_p_element(r"\text{CH} = \frac{\text{SSB} / (k - 1)}{\text{SSW} / (n - k)}")
                lead_ari = create_text_p_element("Adjusted Rand Index (ARI) đo mức trùng khớp nhãn giữa hai phân hoạch sau khi loại trừ yếu tố ngẫu nhiên; ARI bằng 1 thể hiện hai phân hoạch trùng khớp hoàn toàn.")

                p._element.addnext(lead_ari)
                p._element.addnext(math_ch)
                p._element.addnext(lead_ch)
                p._element.addnext(math_db)
                print("    + Đã chèn khối công thức: Davies-Bouldin & Calinski-Harabasz")
            break


def update_toc_and_export_pdf():
    """
    Kích hoạt Microsoft Word 16.0 COM Automation để cập nhật toàn bộ trường Mục lục (TOC)
    và xuất bản PDF độ phân giải cao cho Nhom12_1_BaoCao.docx và Nhom12_BaoCao.docx.
    """
    print("Khởi động Microsoft Word 16.0 COM Engine...")
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0  # wdAlertsNone

    try:
        for docx_path, pdf_path in [(TARGET_DOCX, TARGET_PDF), (SUBMISSION_DOCX, SUBMISSION_PDF)]:
            abs_docx = str(docx_path.resolve())
            abs_pdf = str(pdf_path.resolve())
            print(f"  Mở tài liệu trong Word: {docx_path.name}")
            doc = word.Documents.Open(abs_docx)

            print("    Đang làm mới tất cả các trường (Fields) và Mục lục (TOC)...")
            doc.Fields.Update()
            for toc in doc.TablesOfContents:
                toc.Update()

            doc.Save()
            print(f"    Đã lưu Word với Mục lục mới.")

            print(f"    Đang xuất PDF sang: {pdf_path.name}")
            doc.ExportAsFixedFormat(
                OutputFileName=abs_pdf,
                ExportFormat=17,  # wdExportFormatPDF
                OpenAfterExport=False,
                OptimizeFor=0,     # wdExportOptimizeForPrint
                CreateBookmarks=1, # wdExportCreateHeadingBookmarks
                DocStructureTags=True
            )
            doc.Close(SaveChanges=True)
            print(f"  -> Xuất PDF thành công: {pdf_path.name}")

    finally:
        word.Quit()
        print("Đã đóng Microsoft Word COM Engine an toàn.")


if __name__ == "__main__":
    standardize_report()
    update_toc_and_export_pdf()
    print("HOÀN THÀNH QUY TRÌNH CHUẨN HÓA VÀ XUẤT BẢN!")

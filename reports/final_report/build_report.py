"""Sinh báo cáo Word (.docx) cho Đề tài 16 từ file markdown.

Không cần `python-docx`, không cần mạng, không cần Microsoft Word:
file .docx được tạo trực tiếp theo chuẩn OOXML bằng `zipfile` + XML của thư viện chuẩn Python.

Cách dùng (chạy từ gốc repo):
    .venv\\Scripts\\python.exe reports/final_report/build_report.py
    .venv\\Scripts\\python.exe reports/final_report/build_report.py --md <file.md> --out <file.docx> --max-rows 40

Cú pháp markdown được hỗ trợ (tập con, đủ cho báo cáo môn học):
    # Tiêu đề mục lớn      -> Heading1 (tự động sang trang mới)
    ## Tiêu đề mục con     -> Heading2
    ### Tiêu đề mục nhỏ    -> Heading3
    - gạch đầu dòng        -> bullet
    1. mục đánh số         -> numbered
    > ghi chú              -> đoạn in nghiêng, thụt lề
    | a | b |              -> bảng markdown (hàng đầu là tiêu đề)
    **đậm**, *nghiêng*, `code`

Chỉ thị đặc biệt (đặt trên một dòng riêng):
    <!-- TOC -->                          -> chèn mục lục tự động (bấm F9 trong Word để cập nhật)
    <!-- PAGEBREAK -->                    -> ngắt trang
    <!-- HINH: reports/figures/x.png | Chú thích hình -->
    <!-- BANG: reports/tables/x.csv | Chú thích bảng -->
    <!-- BANG_MD: ... -->                 -> xem chú thích trong README của thư mục này

Nếu file hình/CSV chưa tồn tại, báo cáo vẫn build được: chỗ đó sẽ hiện dòng nhắc
"[Chưa có dữ liệu: <đường dẫn>]" để nhóm biết cần bổ sung.
"""

from __future__ import annotations

import argparse
import csv
import re
import struct
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------------------
# CẤU HÌNH TRANG BÌA — nhóm điền các thông tin còn thiếu (đang để TODO)
# --------------------------------------------------------------------------------------
REPORT_INFO = {
    "truong": "TRƯỜNG ĐẠI HỌC ...",  # TODO: điền tên trường
    "khoa": "KHOA ...",  # TODO: điền tên khoa
    "hoc_phan": "KHAI THÁC DỮ LIỆU",
    "de_tai": (
        "PHÂN NHÓM QUỐC GIA THEO CÁC YẾU TỐ TẠO NÊN MỨC ĐỘ HẠNH PHÚC\n"
        "(WORLD HAPPINESS REPORT)"
    ),
    "de_tai_so": "Đề tài số 16",
    "nhom": "Nhóm 12",
    "lop": "...",  # TODO: điền lớp
    "giang_vien": "...",  # TODO: điền tên giảng viên
    "hoc_ky": "Học kỳ ... - Năm học ...",  # TODO
    "thanh_vien": [
        ("Hà Mạnh Trường", "2045240326", "Nhóm trưởng"),
        ("Huỳnh Tâm Trí", "2045240315", "Thành viên"),
        ("Ngô Quang Trung", "2045240325", "Thành viên"),
    ],
}

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MD = Path(__file__).resolve().parent / "bao_cao.md"
DEFAULT_OUT = Path(__file__).resolve().parent / "Bao_cao_De_tai_16_Nhom_12.docx"

# Khổ A4 và lề chuẩn báo cáo (đơn vị twips: 1 cm = 567 twips)
PAGE_W, PAGE_H = 11906, 16838
MARGIN = {"top": 1701, "right": 1134, "bottom": 1418, "left": 1701}  # 3cm trên, 2cm phải, 2.5cm dưới, 3cm trái
CONTENT_WIDTH_CM = 15.5  # bề rộng vùng chứa chữ, dùng để co hình
MAX_TABLE_ROWS = 30


# --------------------------------------------------------------------------------------
# TIỆN ÍCH
# --------------------------------------------------------------------------------------
def w_p(text_runs: str, *, style: str | None = None, align: str | None = None,
        indent_twips: int | None = None, spacing_before: int = 0, spacing_after: int = 60) -> str:
    """Tạo một đoạn văn Word từ chuỗi các run đã dựng sẵn."""
    ppr = [f'<w:spacing w:before="{spacing_before}" w:after="{spacing_after}"/>']
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if indent_twips is not None:
        ppr.append(f'<w:ind w:left="{indent_twips}"/>')
    return f"<w:p><w:pPr>{''.join(ppr)}</w:pPr>{text_runs}</w:p>"


def w_run(text: str, *, bold: bool = False, italic: bool = False, size_half_pt: int | None = None,
          color: str | None = None, mono: bool = False) -> str:
    """Tạo một run (đoạn chữ liền mạch) với định dạng cơ bản."""
    rpr = []
    if mono:
        rpr.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>')
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if color:
        rpr.append(f'<w:color w:val="{color}"/>')
    if size_half_pt:
        rpr.append(f'<w:sz w:val="{size_half_pt}"/><w:szCs w:val="{size_half_pt}"/>')
    rpr_xml = f"<w:rPr>{''.join(rpr)}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr_xml}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


INLINE_RE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`)")


def runs_from_markdown(text: str, *, base_bold: bool = False, base_italic: bool = False) -> str:
    """Chuyển chuỗi markdown có **đậm**, *nghiêng*, `code` thành các run Word."""
    out = []
    for part in INLINE_RE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append(w_run(part[2:-2], bold=True, italic=base_italic))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append(w_run(part[1:-1], italic=True, bold=base_bold))
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append(w_run(part[1:-1], mono=True, bold=base_bold))
        else:
            out.append(w_run(part, bold=base_bold, italic=base_italic))
    return "".join(out) or w_run("")


def png_size(path: Path) -> tuple[int, int] | None:
    """Đọc kích thước ảnh PNG từ header (byte 16-24) để tính tỷ lệ hiển thị."""
    try:
        with path.open("rb") as f:
            head = f.read(24)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width, height = struct.unpack(">II", head[16:24])
        return width, height
    except OSError:
        return None


def image_paragraph(path: Path, rel_id: str, doc_pr_id: int) -> str:
    """Tạo đoạn văn chứa ảnh (inline drawing), tự co theo bề rộng vùng chữ."""
    size = png_size(path)
    if size is None:
        return w_p(runs_from_markdown(f"*[Không đọc được kích thước ảnh: {path.name}]*"), align="center")

    px_w, px_h = size
    width_cm = min(CONTENT_WIDTH_CM, px_w / 96 * 2.54)  # giả định 96 DPI
    height_cm = width_cm * px_h / px_w
    cx, cy = int(width_cm * 360000), int(height_cm * 360000)  # 1 cm = 360000 EMU

    drawing = (
        "<w:r><w:drawing>"
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{doc_pr_id}" name="Hinh {doc_pr_id}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic><pic:nvPicPr>'
        f'<pic:cNvPr id="{doc_pr_id}" name="Hinh {doc_pr_id}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>"
    )
    return w_p(drawing, align="center", spacing_before=120, spacing_after=0)


def cell(text: str, *, width_twips: int, header: bool = False) -> str:
    """Tạo một ô bảng; hàng tiêu đề có nền xám."""
    shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>' if header else ""
    return (
        "<w:tc><w:tcPr>"
        f'<w:tcW w:w="{width_twips}" w:type="dxa"/>{shade}'
        '<w:vAlign w:val="center"/></w:tcPr>'
        + w_p(
            runs_from_markdown(text, base_bold=header),
            align="center" if header else "left",
            spacing_before=20,
            spacing_after=20,
        )
        + "</w:tc>"
    )


def build_table(rows: list[list[str]], available_width_twips: int = 9000) -> str:
    """Sinh XML bảng có viền, lặp lại hàng tiêu đề khi sang trang."""
    if not rows:
        return ""
    n_cols = max(len(r) for r in rows)
    rows = [r + [""] * (n_cols - len(r)) for r in rows]
    col_w = max(600, available_width_twips // n_cols)

    borders = (
        "<w:tblBorders>"
        + "".join(
            f'<w:{side} w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
            for side in ("top", "left", "bottom", "right", "insideH", "insideV")
        )
        + "</w:tblBorders>"
    )
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{col_w}"/>' for _ in range(n_cols)) + "</w:tblGrid>"

    body = []
    for r_idx, row in enumerate(rows):
        header_row = r_idx == 0
        tr_pr = '<w:trPr><w:tblHeader/></w:trPr>' if header_row else ""
        cells = "".join(cell(value, width_twips=col_w, header=header_row) for value in row)
        body.append(f"<w:tr>{tr_pr}{cells}</w:tr>")

    return (
        '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>'
        f"{borders}<w:tblLayout w:type=\"fixed\"/></w:tblPr>{grid}{''.join(body)}</w:tbl>"
    )


def read_csv_rows(path: Path, max_rows: int) -> tuple[list[list[str]], int]:
    """Đọc CSV thành bảng; trả về (các hàng hiển thị, tổng số hàng dữ liệu)."""
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        all_rows = [row for row in reader if any(c.strip() for c in row)]
    if not all_rows:
        return [], 0
    header, data = all_rows[0], all_rows[1:]
    shown = data[:max_rows]
    return [header] + shown, len(data)


# --------------------------------------------------------------------------------------
# BỘ DỰNG BÁO CÁO
# --------------------------------------------------------------------------------------
class ReportBuilder:
    """Thu thập nội dung báo cáo rồi đóng gói thành file .docx."""

    def __init__(self, max_rows: int = MAX_TABLE_ROWS) -> None:
        self.body: list[str] = []
        self.images: list[tuple[str, Path]] = []  # (rel_id, đường dẫn ảnh)
        self.max_rows = max_rows
        self.fig_no = 0
        self.table_no = 0

    # -- phần thân ---------------------------------------------------------------------
    def add_cover(self, info: dict) -> None:
        """Trang bìa theo thông tin cấu hình ở đầu file."""
        cover = [
            w_p(w_run(info["truong"], bold=True, size_half_pt=28), align="center", spacing_after=0),
            w_p(w_run(info["khoa"], bold=True, size_half_pt=28), align="center", spacing_after=240),
            w_p(w_run(info["hoc_phan"], bold=True, size_half_pt=32), align="center", spacing_after=120),
            w_p(w_run(f'({info["de_tai_so"]})', italic=True, size_half_pt=26), align="center", spacing_after=480),
            w_p(w_run("BÁO CÁO ĐỒ ÁN NHÓM", bold=True, size_half_pt=36), align="center", spacing_after=240),
        ]
        for line in info["de_tai"].split("\n"):
            cover.append(w_p(w_run(line, bold=True, size_half_pt=30), align="center", spacing_after=60))
        cover.append(w_p("", spacing_after=360))
        cover.append(w_p(w_run(info["nhom"], bold=True, size_half_pt=28), align="center", spacing_after=120))
        cover.append(w_p(w_run(f'Lớp: {info["lop"]}', size_half_pt=26), align="center", spacing_after=0))
        cover.append(w_p(w_run(f'Giảng viên hướng dẫn: {info["giang_vien"]}', size_half_pt=26), align="center", spacing_after=0))
        cover.append(w_p(w_run(info["hoc_ky"], size_half_pt=26), align="center", spacing_after=360))
        cover.append(w_p(w_run("Thành viên thực hiện", bold=True, size_half_pt=26), align="center", spacing_after=120))
        for name, student_id, role in info["thanh_vien"]:
            cover.append(w_p(w_run(f"{name} — {student_id} — {role}", size_half_pt=26), align="center", spacing_after=40))
        cover.append(w_p("", spacing_after=240))
        cover.append(w_p(w_run(f'Ngày hoàn thành: {date.today().strftime("%d/%m/%Y")}', italic=True, size_half_pt=24), align="center"))
        self.body.extend(cover)
        self.body.append(self.page_break())

    def page_break(self) -> str:
        return w_p('<w:r><w:br w:type="page"/></w:r>', spacing_after=0)

    def add_toc(self) -> None:
        """Chèn mục lục tự động; Word sẽ hỏi/cho phép bấm F9 để cập nhật."""
        self.body.append(w_p(w_run("MỤC LỤC", bold=True, size_half_pt=30), align="center", spacing_after=120))
        field = (
            '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            + w_run("(Bấm chuột phải vào đây và chọn Update Field, hoặc nhấn F9, để hiện mục lục)")
            + '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        )
        self.body.append(w_p(field))
        self.body.append(self.page_break())

    def add_heading(self, level: int, text: str) -> None:
        # Mục lớn luôn bắt đầu trang mới, trừ khi vừa ngắt trang xong (tránh trang trắng)
        if level == 1 and self.body and 'w:type="page"' not in self.body[-1]:
            self.body.append(self.page_break())
        style = {1: "Heading1", 2: "Heading2", 3: "Heading3"}.get(level, "Heading3")
        self.body.append(w_p(runs_from_markdown(text), style=style, spacing_before=200, spacing_after=100))

    def add_paragraph(self, text: str) -> None:
        self.body.append(w_p(runs_from_markdown(text)))

    def add_bullet(self, text: str) -> None:
        self.body.append(w_p(w_run("• ") + runs_from_markdown(text), indent_twips=567))

    def add_numbered(self, text: str) -> None:
        self.body.append(w_p(runs_from_markdown(text), indent_twips=567))

    def add_quote(self, text: str) -> None:
        self.body.append(w_p(runs_from_markdown(text, base_italic=True), indent_twips=567))

    def add_missing_note(self, kind: str, path: Path) -> None:
        self.body.append(
            w_p(w_run(f"[Chưa có dữ liệu {kind}: {path}] — cần bổ sung trước khi nộp", italic=True, color="C00000"),
                align="center")
        )

    def add_figure(self, rel_path: str, caption: str) -> None:
        path = (REPO_ROOT / rel_path).resolve()
        self.fig_no += 1
        if path.exists():
            rel_id = f"rIdImg{len(self.images) + 1}"
            self.images.append((rel_id, path))
            self.body.append(image_paragraph(path, rel_id, 1000 + self.fig_no))
        else:
            self.add_missing_note("hình", Path(rel_path))
        self.body.append(w_p(w_run(f"Hình {self.fig_no}. {caption}", italic=True), align="center", spacing_after=160))

    def add_table_from_csv(self, rel_path: str, caption: str) -> None:
        path = (REPO_ROOT / rel_path).resolve()
        self.table_no += 1
        if path.exists():
            rows, total = read_csv_rows(path, self.max_rows)
            if rows:
                self.body.append(build_table(rows))
                if total > self.max_rows:
                    self.add_quote(f"Bảng đầy đủ có {total} dòng; báo cáo chỉ in {self.max_rows} dòng đầu, phần còn lại xem trong {rel_path}.")
            else:
                self.add_missing_note("bảng (CSV rỗng)", Path(rel_path))
        else:
            self.add_missing_note("bảng", Path(rel_path))
        self.body.append(w_p(w_run(f"Bảng {self.table_no}. {caption}", italic=True), align="center", spacing_after=160))

    def add_markdown_table(self, lines: list[str]) -> None:
        rows: list[list[str]] = []
        for line in lines:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                continue  # dòng phân cách |---|---|
            rows.append(cells)
        if rows:
            self.body.append(build_table(rows))

    # -- đóng gói ----------------------------------------------------------------------
    def save(self, out_path: Path) -> None:
        document = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            "<w:document "
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f"<w:body>{''.join(self.body)}"
            "<w:sectPr>"
            '<w:footerReference w:type="default" r:id="rIdFooter"/>'
            f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>'
            f'<w:pgMar w:top="{MARGIN["top"]}" w:right="{MARGIN["right"]}" w:bottom="{MARGIN["bottom"]}" '
            f'w:left="{MARGIN["left"]}" w:header="709" w:footer="709" w:gutter="0"/>'
            "</w:sectPr></w:body></w:document>"
        )

        overrides = [
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>',
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>',
            '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>',
        ]
        defaults = [
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
            '<Default Extension="xml" ContentType="application/xml"/>',
        ]
        if self.images:
            image_types = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "gif": "image/gif",
                "bmp": "image/bmp",
            }
            for suffix in sorted({p.suffix.lower().lstrip(".") for _, p in self.images}):
                content_type = image_types.get(suffix)
                if content_type:
                    defaults.append(f'<Default Extension="{suffix}" ContentType="{content_type}"/>')

        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            + "".join(defaults + overrides)
            + "</Types>"
        )

        root_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            "</Relationships>"
        )

        doc_rels = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>',
        ]
        for idx, (rel_id, path) in enumerate(self.images, start=1):
            doc_rels.append(
                f'<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                f'Target="media/image{idx}{path.suffix.lower()}"/>'
            )
        doc_rels.append("</Relationships>")

        footer = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
            '<w:r><w:t xml:space="preserve">Trang </w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            '<w:r><w:t>1</w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
            "</w:p></w:ftr>"
        )

        styles = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:docDefaults><w:rPrDefault><w:rPr>"
            '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
            '<w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:line="360" w:lineRule="auto"/>'
            '<w:jc w:val="both"/></w:pPr></w:pPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
            '<w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="0"/><w:jc w:val="left"/></w:pPr>'
            '<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
            '<w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="1"/><w:jc w:val="left"/></w:pPr>'
            '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>'
            '<w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="2"/><w:jc w:val="left"/></w:pPr>'
            '<w:rPr><w:b/><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>'
            "</w:styles>"
        )

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types)
            z.writestr("_rels/.rels", root_rels)
            z.writestr("word/_rels/document.xml.rels", "".join(doc_rels))
            z.writestr("word/document.xml", document)
            z.writestr("word/styles.xml", styles)
            z.writestr("word/footer1.xml", footer)
            for idx, (_, path) in enumerate(self.images, start=1):
                z.writestr(f"word/media/image{idx}{path.suffix.lower()}", path.read_bytes())


# --------------------------------------------------------------------------------------
# ĐỌC MARKDOWN
# --------------------------------------------------------------------------------------
HINH_RE = re.compile(r"<!--\s*HINH:\s*(.+?)\s*\|\s*(.+?)\s*-->")
BANG_RE = re.compile(r"<!--\s*BANG:\s*(.+?)\s*\|\s*(.+?)\s*-->")


def render_markdown(md_path: Path, builder: ReportBuilder) -> None:
    """Đọc file markdown và đưa nội dung vào builder. Ghi chú HTML bị bỏ qua, không xuất ra báo cáo."""
    lines = md_path.read_text(encoding="utf-8").splitlines()
    idx = 0
    in_comment = False
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        # Đang trong ghi chú nội bộ nhiều dòng: bỏ qua tới khi gặp dấu kết thúc
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            idx += 1
            continue

        if stripped in ("<!-- TOC -->", "<!--TOC-->"):
            builder.add_toc()
        elif stripped in ("<!-- PAGEBREAK -->", "<!--PAGEBREAK-->"):
            builder.body.append(builder.page_break())
        elif HINH_RE.match(stripped):
            match = HINH_RE.match(stripped)
            builder.add_figure(match.group(1), match.group(2))
        elif BANG_RE.match(stripped):
            match = BANG_RE.match(stripped)
            builder.add_table_from_csv(match.group(1), match.group(2))
        elif stripped.startswith("<!--") and "-->" in stripped:
            pass  # ghi chú nội bộ một dòng
        elif stripped.startswith("<!--"):
            in_comment = True  # mở ghi chú nội bộ nhiều dòng
        elif stripped.startswith("|") and stripped.endswith("|"):
            block = []
            while idx < len(lines) and lines[idx].strip().startswith("|"):
                block.append(lines[idx])
                idx += 1
            builder.add_markdown_table(block)
            continue
        elif stripped.startswith("### "):
            builder.add_heading(3, stripped[4:])
        elif stripped.startswith("## "):
            builder.add_heading(2, stripped[3:])
        elif stripped.startswith("# "):
            builder.add_heading(1, stripped[2:])
        elif stripped.startswith("> "):
            builder.add_quote(stripped[2:])
        elif re.match(r"^[-*]\s+", stripped):
            builder.add_bullet(re.sub(r"^[-*]\s+", "", stripped))
        elif re.match(r"^\d+\.\s+", stripped):
            builder.add_numbered(stripped)
        elif stripped in ("---", "***", "___"):
            pass
        elif stripped == "":
            pass
        else:
            builder.add_paragraph(stripped)
        idx += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Sinh báo cáo Word (.docx) cho Đề tài 16 từ markdown.")
    parser.add_argument("--md", type=Path, default=DEFAULT_MD, help="file markdown nguồn")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="file .docx xuất ra")
    parser.add_argument("--max-rows", type=int, default=MAX_TABLE_ROWS, help="số dòng tối đa in cho mỗi bảng CSV")
    args = parser.parse_args()

    if not args.md.exists():
        raise SystemExit(f"Không tìm thấy file markdown: {args.md}")

    builder = ReportBuilder(max_rows=args.max_rows)
    builder.add_cover(REPORT_INFO)
    render_markdown(args.md, builder)

    out_used = args.out
    try:
        builder.save(args.out)
    except PermissionError:
        # Trường hợp thường gặp: file .docx đang mở trong Word nên bị khoá ghi.
        # Ghi ra tên khác để không mất kết quả, rồi báo rõ cho người dùng.
        out_used = args.out.with_name(f"{args.out.stem}_moi{args.out.suffix}")
        builder.save(out_used)
        print(f"CẢNH BÁO: không ghi được {args.out.name} vì file đang mở trong Word.")
        print("         Hãy đóng Word rồi chạy lại nếu muốn ghi đè tên gốc.")

    print(f"Đã tạo báo cáo: {out_used}")
    print(f"  Số hình chèn: {builder.fig_no} | Số bảng: {builder.table_no} | Dung lượng: {out_used.stat().st_size} bytes")
    print("  Mở bằng Word rồi bấm F9 (hoặc Update Field) để hiện mục lục và số trang.")


if __name__ == "__main__":
    main()

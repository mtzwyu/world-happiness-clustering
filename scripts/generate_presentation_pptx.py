"""
Script sinh bộ slide báo cáo PowerPoint chuẩn 16:9 cho Đề tài 16 — Nhóm 12
Học phần: Khai thác dữ liệu (Data Mining)
Đề tài: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report 2015–2019)
Quy cách: 16 slide (đã tách riêng Slide Quy trình tiền xử lý và Slide Kết quả tiền xử lý),
font chữ to rõ ràng (>= 16.5pt body, 21-24pt header, 32-36pt title, 50-60pt stat callouts),
bố cục trực quan kết hợp ảnh chụp Notebook thực tế và Bảng dữ liệu Excel/DataFrame,
giảm thiểu chữ thừa, tăng tính thực chứng, tích hợp đầy đủ Speaker Notes tiếng Việt.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

# Thiết lập đường dẫn tương đối độc lập môi trường
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "reports" / "presentation"
OUTPUT_PPTX = OUTPUT_DIR / "Nhom12_BaoCao_Slides.pptx"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
ARTIFACTS_DIR = FIGURES_DIR / "slide_artifacts"

# -----------------------------------------------------------------------------
# BẢNG MÀU CHUẨN ĐỒ HỌA CHUYÊN NGHIỆP (TOPIC-INFORMED PALETTE)
# -----------------------------------------------------------------------------
COLOR_DARK_BG       = RGBColor(15, 23, 42)      # #0F172A - Xanh than sâu (Deep Slate)
COLOR_WHITE         = RGBColor(255, 255, 255)  # #FFFFFF - Trắng
COLOR_CARD_BG       = RGBColor(248, 250, 252)  # #F8FAFC - Xám nhạt siêu mịn
COLOR_BORDER        = RGBColor(226, 232, 240)  # #E2E8F0 - Viền thẻ phân cách
COLOR_TEXT_MAIN     = RGBColor(15, 23, 42)      # #0F172A - Chữ chính đậm tương phản cao
COLOR_TEXT_MUTED    = RGBColor(100, 116, 139)  # #64748B - Chữ chú thích phụ
COLOR_TEAL_ACCENT   = RGBColor(2, 132, 199)    # #0284C7 - Xanh dương điểm nhấn
COLOR_GREEN_C1      = RGBColor(5, 150, 105)    # #059669 - Xanh ngọc Cụm 1 (Phát triển)
COLOR_BLUE_C2       = RGBColor(37, 99, 235)    # #2563EB - Xanh dương Cụm 2 (Đang phát triển)
COLOR_CORAL_C3      = RGBColor(220, 38, 38)    # #DC2626 - Đỏ cam Cụm 3 (Khó khăn)
COLOR_AMBER         = RGBColor(217, 119, 6)    # #D97706 - Vàng hổ phách nổi bật
COLOR_GOLD_TEXT     = RGBColor(253, 224, 71)   # #FDE047 - Vàng cát điểm nhấn trên nền tối

FONT_FAMILY = "Arial"

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: tạo hiệu ứng chuyển cảnh mượt mà (Animation / Slide Transition)
    def set_slide_transition(slide, transition_type="fade", direction="l", speed="med"):
        """Thiết lập hiệu ứng animation chuyển cảnh mượt mà, chuyên nghiệp cho slide."""
        if transition_type == "fade":
            anim_tag = "<p:fade/>"
        elif transition_type == "push":
            anim_tag = f'<p:push dir="{direction}"/>'
        elif transition_type == "wipe":
            anim_tag = f'<p:wipe dir="{direction}"/>'
        elif transition_type == "cover":
            anim_tag = f'<p:cover dir="{direction}"/>'
        else:
            anim_tag = "<p:fade/>"

        xml_str = (
            f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            f'spd="{speed}" advClick="1">'
            f'{anim_tag}'
            f'</p:transition>'
        )
        slide.element.append(parse_xml(xml_str))

    # Helper: tạo slide nền kèm hiệu ứng animation
    def add_slide_with_bg(dark_mode=False, transition_type="fade", direction="l"):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_DARK_BG if dark_mode else COLOR_WHITE
        bg.line.fill.background()
        set_slide_transition(slide, transition_type=transition_type, direction=direction)
        return slide

    # Helper: tạo header slide (Cỡ chữ tinh chỉnh 23.5pt vừa vặn, thanh lịch, không lấn át bố cục)
    def add_slide_header(slide, title_text, category_text="", dark_mode=False):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        if category_text:
            p_cat = tf.paragraphs[0]
            p_cat.text = category_text.upper()
            p_cat.font.name = FONT_FAMILY
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_GOLD_TEXT if dark_mode else COLOR_TEAL_ACCENT
            p_title = tf.add_paragraph()
            p_title.space_before = Pt(3)
        else:
            p_title = tf.paragraphs[0]
            
        p_title.text = title_text
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(23.5)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE if dark_mode else COLOR_TEXT_MAIN

    # Helper: tạo thẻ card
    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    # Helper: tạo text trong thẻ (Căn giữa hoàn hảo, chống tràn khung)
    def add_card_text(slide, left, top, width, height, header_text="", bullets=None, header_color=COLOR_TEXT_MAIN, font_size=15.5, header_size=18.5, space_before=5):
        tb = slide.shapes.add_textbox(left + Inches(0.22), top, width - Inches(0.44), height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_first = True
        if header_text:
            p = tf.paragraphs[0]
            p.text = header_text
            p.font.name = FONT_FAMILY
            p.font.size = Pt(header_size)
            p.font.bold = True
            p.font.color.rgb = header_color
            p_first = False

        if bullets:
            for item in bullets:
                if p_first:
                    p = tf.paragraphs[0]
                    p_first = False
                else:
                    p = tf.add_paragraph()
                p.text = f"• {item}"
                p.font.name = FONT_FAMILY
                p.font.size = Pt(font_size)
                p.font.color.rgb = COLOR_TEXT_MAIN
                p.space_before = Pt(space_before)
                p.space_after = Pt(0)

    # Helper: tạo hộp số liệu lớn (Stat Box - Căn giữa chuẩn xác)
    def add_stat_box(slide, left, top, width, height, big_num, label_text, sub_text="", num_color=COLOR_TEAL_ACCENT):
        add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=num_color)
        tb = slide.shapes.add_textbox(left + Inches(0.2), top, width - Inches(0.4), height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_num = tf.paragraphs[0]
        p_num.text = big_num
        p_num.font.name = FONT_FAMILY
        p_num.font.size = Pt(46)
        p_num.font.bold = True
        p_num.font.color.rgb = num_color
        p_num.alignment = PP_ALIGN.CENTER

        p_lbl = tf.add_paragraph()
        p_lbl.text = label_text
        p_lbl.font.name = FONT_FAMILY
        p_lbl.font.size = Pt(17)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_TEXT_MAIN
        p_lbl.alignment = PP_ALIGN.CENTER
        p_lbl.space_before = Pt(6)

        if sub_text:
            p_sub = tf.add_paragraph()
            p_sub.text = sub_text
            p_sub.font.name = FONT_FAMILY
            p_sub.font.size = Pt(14)
            p_sub.font.color.rgb = COLOR_TEXT_MUTED
            p_sub.alignment = PP_ALIGN.CENTER
            p_sub.space_before = Pt(4)

    # Helper: đặt Speaker Notes
    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TRANG BÌA (DARK BACKGROUND)
    # =========================================================================
    s1 = add_slide_with_bg(dark_mode=True)
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(2.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "HỌC PHẦN: KHAI THÁC DỮ LIỆU (DATA MINING)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_TEXT

    p2 = tf1.add_paragraph()
    p2.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC — ĐỀ TÀI 16"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report 2015–2019)"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(19.5)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.space_before = Pt(6)

    # 3 thẻ thành viên
    members = [
        ("Hà Mạnh Trường", "2045240326 (Nhóm trưởng)", "Phần 1: Dữ liệu & Tiền xử lý", COLOR_GREEN_C1),
        ("Huỳnh Tâm Trí", "2045240315", "Phần 2: Thuật toán From Scratch", COLOR_BLUE_C2),
        ("Ngô Quang Trung", "2045240325", "Phần 3: Diễn giải tri thức & Demo", COLOR_AMBER),
    ]
    card_w = Inches(3.6)
    card_gap = Inches(0.26)
    start_x = Inches(1.0)
    card_y = Inches(3.2)
    card_h = Inches(2.3)

    for i, (name, mssv, role, accent_col) in enumerate(members):
        cx = start_x + i * (card_w + card_gap)
        add_card(s1, cx, card_y, card_w, card_h, bg_color=RGBColor(30, 41, 59), border_color=accent_col)
        tb_m = s1.shapes.add_textbox(cx + Inches(0.2), card_y, card_w - Inches(0.4), card_h)
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        tf_m.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0

        p_name = tf_m.paragraphs[0]
        p_name.text = name
        p_name.font.name = FONT_FAMILY
        p_name.font.size = Pt(20)
        p_name.font.bold = True
        p_name.font.color.rgb = COLOR_WHITE

        p_id = tf_m.add_paragraph()
        p_id.text = f"MSSV: {mssv}"
        p_id.font.name = FONT_FAMILY
        p_id.font.size = Pt(15.5)
        p_id.font.color.rgb = COLOR_GOLD_TEXT
        p_id.space_before = Pt(4)

        p_role = tf_m.add_paragraph()
        p_role.text = role
        p_role.font.name = FONT_FAMILY
        p_role.font.size = Pt(15)
        p_role.font.color.rgb = RGBColor(226, 232, 240)
        p_role.space_before = Pt(8)

    # Footer slide 1
    tb_foot = s1.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.333), Inches(0.9))
    tf_foot = tb_foot.text_frame
    p_f = tf_foot.paragraphs[0]
    p_f.text = "Video báo cáo: Thời lượng tối đa 12 phút • Dữ liệu nghiên cứu: 5 năm WHR (781 bản ghi sạch) • Cài đặt 100% From Scratch"
    p_f.font.name = FONT_FAMILY
    p_f.font.size = Pt(15)
    p_f.font.color.rgb = RGBColor(148, 163, 184)
    p_f.alignment = PP_ALIGN.CENTER

    set_notes(s1, (
        "Kính chào Thầy và Hội đồng chấm đồ án. Em là Hà Mạnh Trường, nhóm trưởng Nhóm 12. "
        "Hôm nay nhóm em xin phép báo cáo Đề tài 16: Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc "
        "dựa trên dữ liệu World Happiness Report giai đoạn 2015–2019. Video báo cáo hôm nay sẽ kéo dài dưới 12 phút "
        "và được chia làm 3 phần rành mạch: Em sẽ phụ trách Phần 1 về bối cảnh đề tài và quy trình tiền xử lý dữ liệu; "
        "bạn Huỳnh Tâm Trí sẽ trình bày Phần 2 về thuật toán tự cài đặt và thực nghiệm tham số; cuối cùng bạn Ngô Quang Trung "
        "sẽ trình bày Phần 3 về diễn giải tri thức, theo dõi dịch chuyển cụm và demo ứng dụng tương tác."
    ))

    # =========================================================================
    # SLIDE 2: NỘI DUNG BÁO CÁO GỒM (THEO YÊU CẦU ĐẶT TẠI VỊ TRÍ SỐ 2, KHÔNG TÊN NGƯỜI)
    # =========================================================================
    s2 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s2, "NỘI DUNG BÁO CÁO GỒM", "TỔNG QUAN TIẾN TRÌNH THỰC HIỆN")

    sections = [
        ("Phần 1: Tổng quan đề tài & Cơ sở lý thuyết", [
            "Bối cảnh Báo cáo Hạnh phúc Thế giới WHR (2015–2019).",
            "Hạn chế điểm số đơn lẻ & Gom cụm không giám sát 6 yếu tố cơ sở."
        ], COLOR_GREEN_C1),
        ("Phần 2: Dữ liệu & Quy trình tiền xử lý 5 năm", [
            "Đồng nhất schema 5 năm, xử lý khuyết thiếu (loại UAE 2018).",
            "Tập dữ liệu 781 bản ghi sạch 100% và chuẩn hóa địa lý ISO-3."
        ], COLOR_GREEN_C1),
        ("Phần 3: Phương pháp luận & Thuật toán From Scratch", [
            "Cơ sở lựa chọn chuẩn hóa Z-score & giảm chiều PCA.",
            "Tự cài đặt K-Means++, Hierarchical Ward Lance-Williams & DBSCAN."
        ], COLOR_BLUE_C2),
        ("Phần 4: Thực nghiệm gom cụm, Tối ưu hóa & Đối chứng", [
            "Thẩm định số cụm tối ưu k* = 3 đồng thuận qua cả 5 năm.",
            "Đối chứng K-Means vs Ward vs DBSCAN và kiểm định độ ổn định ARI."
        ], COLOR_BLUE_C2),
        ("Phần 5: Diễn giải tri thức, Demo tương tác & Kết luận", [
            "Chân dung 3 cụm, hậu kiểm ANOVA, dịch chuyển 142/156 quốc gia.",
            "Demo tương tác Streamlit 4 tab, đúc kết đóng góp & hướng mở rộng."
        ], COLOR_AMBER),
    ]

    row1_w = Inches(3.7)
    row1_gap = Inches(0.31)
    r1_x = Inches(0.8)
    r1_y = Inches(1.6)
    r1_h = Inches(2.6)

    for i in range(3):
        title_sec, bullets, col = sections[i]
        cx = r1_x + i * (row1_w + row1_gap)
        add_card(s2, cx, r1_y, row1_w, r1_h, border_color=col)
        add_card_text(s2, cx, r1_y, row1_w, r1_h, header_text=title_sec, bullets=bullets, header_color=col, font_size=15, header_size=18, space_before=4)

    row2_w = Inches(5.71)
    row2_gap = Inches(0.31)
    r2_x = Inches(0.8)
    r2_y = Inches(4.45)
    r2_h = Inches(2.6)

    for i in range(2):
        title_sec, bullets, col = sections[3 + i]
        cx = r2_x + i * (row2_w + row2_gap)
        add_card(s2, cx, r2_y, row2_w, r2_h, border_color=col)
        add_card_text(s2, cx, r2_y, row2_w, r2_h, header_text=title_sec, bullets=bullets, header_color=col, font_size=15.5, header_size=18.5, space_before=5)

    set_notes(s2, (
        "Kính thưa Thầy và Hội đồng chấm đồ án, nội dung bài báo cáo của nhóm em gồm 5 phần chính: "
        "Phần 1 là tổng quan bối cảnh đề tài và cơ sở lý thuyết; Phần 2 là quy trình thu thập và tiền xử lý dữ liệu 5 năm; "
        "Phần 3 là phương pháp luận và cài đặt các thuật toán from scratch; Phần 4 là kết quả thực nghiệm tối ưu hóa và đánh giá đối chứng mô hình; "
        "và Phần 5 là diễn giải tri thức kinh tế - xã hội, theo dõi dịch chuyển cụm, demo ứng dụng tương tác cùng kết luận đề tài."
    ))

    # =========================================================================
    # SLIDE 3: LÝ DO CHỌN ĐỀ TÀI & Ý NGHĨA WHR (CHƯƠNG 1)
    # =========================================================================
    s3 = add_slide_with_bg()
    add_slide_header(s3, "LÝ DO CHỌN ĐỀ TÀI & Ý NGHĨA WORLD HAPPINESS REPORT", "CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI")

    col_w = Inches(5.7)
    c1_x = Inches(0.8)
    c2_x = Inches(6.83)
    c_y = Inches(1.6)
    c_h = Inches(5.3)

    add_card(s3, c1_x, c_y, col_w, c_h, border_color=COLOR_CORAL_C3)
    add_card_text(s3, c1_x, c_y, col_w, c_h,
                  header_text="Thực trạng: Hạn chế của Điểm số Đơn lẻ",
                  bullets=[
                      "World Happiness Report (WHR) công bố thường niên từ 2012 dưới sự chủ trì của SDSN Liên Hợp Quốc.",
                      "Điểm Cantril Ladder (0–10) là một con số duy nhất, dễ che lấp các thế mạnh hoặc điểm nghẽn đặc thù của từng quốc gia.",
                      "Hai quốc gia cùng điểm số có thể đến từ 2 mô hình đối nghịch: kinh tế vượt trội vs. an sinh xã hội vững chắc.",
                      "Không thể áp dụng chính sách 'cào bằng' nếu chưa hiểu rõ các yếu tố cốt lõi thúc đẩy hạnh phúc thực tế."
                  ],
                  header_color=COLOR_CORAL_C3, font_size=17)

    add_card(s3, c2_x, c_y, col_w, c_h, border_color=COLOR_TEAL_ACCENT)
    add_card_text(s3, c2_x, c_y, col_w, c_h,
                  header_text="Giải pháp: Khai phá Gom cụm Không giám sát",
                  bullets=[
                      "Gom cụm không giám sát (Unsupervised Clustering) thuần túy dựa trên 6 trụ cột cơ sở khách quan.",
                      "Quy tắc vàng: Tuyệt đối không dùng Happiness Score vào phân cụm để bảo đảm tính khách quan hoàn toàn.",
                      "Nhận diện đúng điểm nghẽn về thể chế (tham nhũng), y tế hay an sinh để tư vấn chính sách trúng đích.",
                      "Ý nghĩa học thuật: Hiện thực hóa quy trình khai thác dữ liệu chuẩn mực, tự lập trình 100% From Scratch."
                  ],
                  header_color=COLOR_TEAL_ACCENT, font_size=17)

    set_notes(s3, (
        "Về lý do chọn đề tài: Báo cáo Hạnh phúc Thế giới là nguồn dữ liệu chuẩn mực toàn cầu. "
        "Tuy nhiên, nếu chỉ nhìn vào một con số điểm hạnh phúc duy nhất, chúng ta không thể biết một quốc gia đạt điểm đó "
        "nhờ kinh tế vượt trội hay nhờ an sinh xã hội vững chắc. Do đó, việc áp dụng gom cụm không giám sát dựa trên 6 yếu tố cơ sở "
        "sẽ giúp khám phá ra các nhóm quốc gia có cùng chân dung phát triển tự nhiên. Đây là cơ sở thực chứng giúp định hình chính sách hỗ trợ phát triển bền vững."
    ))

    # =========================================================================
    # SLIDE 4: QUY TRÌNH TIỀN XỬ LÝ (TÁCH THÀNH SLIDE RIÊNG THEO YÊU CẦU)
    # =========================================================================
    s4 = add_slide_with_bg()
    add_slide_header(s4, "QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU 5 NĂM (2015–2019)", "CHƯƠNG 2: 4 BƯỚC TIỀN XỬ LÝ KỸ THUẬT")

    # Cột trái: Thẻ 4 bước xử lý kỹ thuật
    add_card(s4, Inches(0.8), Inches(1.6), Inches(4.3), Inches(5.3), border_color=COLOR_TEAL_ACCENT)
    add_card_text(s4, Inches(0.8), Inches(1.6), Inches(4.3), Inches(5.3),
                  header_text="4 Bước Tiền xử lý Kỹ thuật",
                  bullets=[
                      "Bước 1: Thu thập 5 tệp CSV từ Kaggle với 782 mẫu thô ban đầu (2015–2019).",
                      "Bước 2: Đồng nhất Schema dị biệt qua COLUMN_MAPPING và loại bỏ sai số mẫu.",
                      "Bước 3: Kiểm tra khuyết thiếu, loại duy nhất UAE 2018 do thiếu 100% tham nhũng.",
                      "Bước 4: Chuẩn hóa tên quốc gia biến động (Macedonia...) và gắn mã địa lý ISO-3.",
                      "Bảo đảm tính tái lập: Tệp happiness_merged.csv sạch 100% không khuyết thiếu."
                  ],
                  header_color=COLOR_TEAL_ACCENT, font_size=16)

    # Cột phải: Sơ đồ quy trình thực nghiệm (Kích thước to, rõ nét)
    img_flow = ARTIFACTS_DIR / "pipeline_preprocessing_flow.png"
    if img_flow.exists():
        s4.shapes.add_picture(str(img_flow), Inches(5.3), Inches(1.6), width=Inches(7.233))

    set_notes(s4, (
        "Ở khâu tiền xử lý dữ liệu, thách thức lớn nhất là cấu trúc cột và cách đặt tên quốc gia qua 5 năm hoàn toàn không đồng nhất. "
        "Nhóm đã thực hiện quy trình 4 bước chặt chẽ: Đầu tiên là đồng nhất schema 6 đặc trưng bằng từ điển chuyển đổi; "
        "thứ hai là loại bỏ triệt để các cột sai số thống kê mẫu; thứ ba là loại bỏ đúng 1 dòng của UAE năm 2018 do khuyết thiếu hoàn toàn "
        "chỉ số tham nhũng; và cuối cùng là chuẩn hóa danh pháp các quốc gia biến động cùng mã địa lý ISO-3 để phục vụ liên kết dữ liệu."
    ))

    # =========================================================================
    # SLIDE 5: KẾT QUẢ TIỀN XỬ LÝ (TÁCH THÀNH SLIDE RIÊNG THEO YÊU CẦU)
    # =========================================================================
    s5 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s5, "KẾT QUẢ TIỀN XỬ LÝ VÀ TẬP DỮ LIỆU CHUẨN HÓA", "CHƯƠNG 2: MINH CHỨNG DỮ LIỆU SẠCH 100%")

    # Cột trái: 2 stat box lớn gọn gàng
    add_stat_box(s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(2.5), "781", "Bản ghi Sạch 100%", "Từ 782 mẫu thô; loại duy nhất UAE 2018; Tỷ lệ NaN = 0.0%", COLOR_GREEN_C1)
    add_stat_box(s5, Inches(0.8), Inches(4.35), Inches(3.7), Inches(2.55), "162", "Mã Chuẩn hóa ISO-3", "164 quốc gia duy nhất qua 5 năm (đầy đủ mã tọa độ)", COLOR_TEAL_ACCENT)

    # Cột phải: Ảnh chụp Notebook 01 thực tế to rõ nét
    img_nb01 = ARTIFACTS_DIR / "nb01_data_cleaning_head.png"
    if img_nb01.exists():
        s5.shapes.add_picture(str(img_nb01), Inches(4.7), Inches(1.6), width=Inches(7.833))

    set_notes(s5, (
        "Kết quả sau tiền xử lý là một tập dữ liệu hoàn hảo gồm 781 bản ghi của 164 quốc gia với 162 mã ISO-3 phân biệt, "
        "sạch 100% không còn giá trị khuyết thiếu. Toàn bộ được đóng gói vào tệp dữ liệu trung gian happiness_merged.csv. "
        "Trên màn hình là ảnh chụp thực tế từ Notebook 01 hiển thị 5 dòng đầu của tập dữ liệu năm 2019. "
        "Tiếp theo, em xin nhường phần thuyết trình cho bạn Huỳnh Tâm Trí với nội dung thuật toán và thực nghiệm."
    ))

    # =========================================================================
    # SLIDE 6: EDA & CHUẨN HÓA Z-SCORE (CHƯƠNG 2-3) — CÓ HEATMAP TƯƠNG QUAN
    # =========================================================================
    s6 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s6, "KHÁM PHÁ DỮ LIỆU (EDA) & CƠ SỞ CHUẨN HÓA Z-SCORE", "CHƯƠNG 2 & 3: PHÂN TÍCH KHÁM PHÁ")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), border_color=COLOR_BLUE_C2)
    add_card_text(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
                  header_text="Phân tích Phân bố & Quyết định Chuẩn hóa",
                  bullets=[
                      "Độ lệch dữ liệu mạnh: Chỉ số Tham nhũng (skewness = 1.52) và Hảo tâm (1.04) lệch phải rất mạnh.",
                      "Tương quan cao: GDP bình quân và Tuổi thọ khỏe mạnh có tương quan tuyến tính rất chặt chẽ (r = 0.79).",
                      "Ngoại lai rõ nét: Nhận diện nhiều điểm ngoại lai ở nhóm Bắc Âu (rất cao) và Châu Phi (rất thấp).",
                      "Tại sao chọn Z-score?: Min-Max bị nén do ngoại lai cực đại; Z-score đưa kỳ vọng về 0 và phương sai về 1, bảo đảm 6 đặc trưng đóng góp bình đẳng vào khoảng cách Euclid."
                  ],
                  header_color=COLOR_BLUE_C2, font_size=17)

    img_corr = FIGURES_DIR / "correlation_heatmap.png"
    if img_corr.exists():
        s6.shapes.add_picture(str(img_corr), Inches(6.6), Inches(1.6), width=Inches(5.9))

    set_notes(s6, (
        "Xin chào Thầy, em là Huỳnh Tâm Trí. Tiếp nối phần của bạn Trường, khi phân tích phân bố và tương quan, "
        "nhóm nhận thấy các chỉ số như tham nhũng và lòng hảo tâm bị lệch phải rất mạnh, đồng thời xuất hiện nhiều giá trị ngoại lai. "
        "Khi so sánh giữa Min-Max và Z-score, Min-Max làm các quốc gia trung bình bị nén chặt lại do tác động của các nước ngoại lai cực đại. "
        "Do đó, nhóm quyết định chọn Z-score làm phương pháp chuẩn hóa chính để giữ nguyên cấu trúc phân tán tự nhiên "
        "và tính toán khoảng cách Euclidean công bằng giữa 6 yếu tố."
    ))

    # =========================================================================
    # SLIDE 7: CÀI ĐẶT THUẬT TOÁN FROM SCRATCH (CHƯƠNG 3) — CÓ ẢNH CHỤP CODE NOTEBOOK 03
    # =========================================================================
    s7 = add_slide_with_bg()
    add_slide_header(s7, "CÀI ĐẶT THUẬT TOÁN GOM CỤM TỪ ĐẦU (FROM SCRATCH)", "CHƯƠNG 3: MINH CHỨNG MÃ NGUỒN THỰC THI")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(4.3), Inches(5.3), border_color=COLOR_GREEN_C1)
    add_card_text(s7, Inches(0.8), Inches(1.6), Inches(4.3), Inches(5.3),
                  header_text="Cài đặt Thuật toán From Scratch",
                  bullets=[
                      "SimpleKMeans: Khởi tạo thông minh K-Means++ với xác suất D(x)^2, lặp n_init = 10 lần tối ưu WCSS.",
                      "Phân cấp Ward: Cập nhật khoảng cách liên tục theo Lance-Williams, lưu vết lịch sử gộp.",
                      "Độ đo tự code: Tự lập trình 100% Silhouette s(i), Davies-Bouldin, Calinski-Harabasz và ARI.",
                      "Kiểm chứng đối chứng: Khớp hoàn toàn scikit-learn & scipy với sai số < 1e-4."
                  ],
                  header_color=COLOR_GREEN_C1, font_size=16)

    img_nb03 = ARTIFACTS_DIR / "nb03_from_scratch_code.png"
    if img_nb03.exists():
        s7.shapes.add_picture(str(img_nb03), Inches(5.3), Inches(1.6), width=Inches(7.233))

    set_notes(s7, (
        "Điểm cốt lõi về kỹ thuật trong đồ án của nhóm là toàn bộ thuật toán gom cụm và độ đo đánh giá đều được tự lập trình from scratch "
        "bằng Python và NumPy cơ bản, tuyệt đối không gọi hàm thư viện có sẵn trong pipeline. Nhóm đã tự cài K-Means++ với khởi tạo xác suất, "
        "phân cấp tích tụ liên kết Ward chuẩn công thức Lance-Williams, và DBSCAN quét mật độ. "
        "Trên màn hình bên phải là ảnh chụp cell code và kết quả thực thi trong Notebook 03, khớp chính xác từng con số với scikit-learn và scipy."
    ))

    # =========================================================================
    # SLIDE 8: THẨM ĐỊNH K*=3 (CHƯƠNG 4) — CÓ BẢNG EXCEL ĐỘ NHẠY K & ĐỒ THỊ ELBOW
    # =========================================================================
    s8 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s8, "THẨM ĐỊNH SỐ CỤM TỐI ƯU k* = 3 ĐỒNG THUẬN 5 NĂM", "CHƯƠNG 4: THỰC NGHIỆM ĐỘ NHẠY K")

    # Cột trái: Đồ thị Elbow & Thẻ luận cứ thống kê
    img_elbow = FIGURES_DIR / "elbow_silhouette_kmeans.png"
    if img_elbow.exists():
        s8.shapes.add_picture(str(img_elbow), Inches(0.8), Inches(1.6), width=Inches(5.2))

    add_card(s8, Inches(0.8), Inches(3.9), Inches(5.2), Inches(3.0), border_color=COLOR_TEAL_ACCENT)
    add_card_text(s8, Inches(0.8), Inches(3.9), Inches(5.2), Inches(3.0),
                  header_text="Luận cứ Toán học Chốt k* = 3",
                  bullets=[
                      "Cả 5 năm (2015–2019) đồng thuận tuyệt đối tại k* = 3.",
                      "Silhouette đạt đỉnh cực đại (0.293 – 0.344).",
                      "Độ uốn Elbow rõ nét tại k=3 trước khi suy giảm quán tính WCSS.",
                      "Số cụm phản ánh hoàn hảo 3 nhóm trình độ kinh tế - xã hội."
                  ],
                  header_color=COLOR_TEAL_ACCENT, font_size=15, header_size=17.5, space_before=4)

    # Cột phải: Bảng Excel độ nhạy k to rõ nét
    img_k_excel = ARTIFACTS_DIR / "excel_k_sensitivity.png"
    if img_k_excel.exists():
        s8.shapes.add_picture(str(img_k_excel), Inches(6.2), Inches(1.6), width=Inches(6.333))

    set_notes(s8, (
        "Để xác định số cụm tối ưu, nhóm đã tiến hành khảo sát k từ 2 đến 9 trên cả 5 năm độc lập. "
        "Kết quả trên biểu đồ Elbow bên trái và bảng tính Excel thực nghiệm bên phải cho thấy cả 5 năm đều đồng thuận tuyệt đối tại k* = 3 "
        "với điểm Silhouette đạt đỉnh cao nhất, dao động từ 0,293 đến 0,344. Cấu hình 3 cụm này vừa có tính ổn định toán học cao nhất, "
        "vừa mang ý nghĩa kinh tế - xã hội rõ rệt khi phân hóa thế giới thành 3 nhóm phát triển tương ứng."
    ))

    # =========================================================================
    # SLIDE 9: SO SÁNH ĐỐI CHỨNG THUẬT TOÁN (CHƯƠNG 4) — CÓ BẢNG EXCEL MODEL COMPARISON
    # =========================================================================
    s9 = add_slide_with_bg()
    add_slide_header(s9, "SO SÁNH ĐỐI CHỨNG CÁC THUẬT TOÁN GOM CỤM", "CHƯƠNG 4: BẢNG ĐỐI CHỨNG HIỆU NĂNG THỰC TẾ")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(4.3), Inches(5.3), border_color=COLOR_TEAL_ACCENT)
    add_card_text(s9, Inches(0.8), Inches(1.6), Inches(4.3), Inches(5.3),
                  header_text="Quyết định Lựa chọn Mô hình",
                  bullets=[
                      "K-Means (Z-score): Toàn diện nhất với Silhouette 0.293–0.344 và Calinski-Harabasz cao nhất (86.02).",
                      "Phân cấp Ward (Z-score): Thuật toán tất định, kiểm chứng tính khách quan của ranh giới cụm (Silhouette 0.310).",
                      "DBSCAN không khả thi: Mật độ biến thiên liên tục khiến DBSCAN coi 28 quốc gia thành nhiễu, điểm âm.",
                      "Chốt phương án: Chọn K-Means làm thuật toán phân nhóm chính, Ward làm đối chứng."
                  ],
                  header_color=COLOR_TEAL_ACCENT, font_size=16)

    img_comp_excel = ARTIFACTS_DIR / "excel_model_comparison.png"
    if img_comp_excel.exists():
        s9.shapes.add_picture(str(img_comp_excel), Inches(5.3), Inches(1.6), width=Inches(7.233))

    set_notes(s9, (
        "Khi đặt các thuật toán lên bàn cân so sánh trên bảng tính thực nghiệm bên phải, K-Means trên dữ liệu Z-score thể hiện ưu thế vượt trội "
        "về độ tách biệt cụm với điểm Silhouette và Calinski-Harabasz cao nhất. Thuật toán phân cấp Ward cho kết quả tương đồng và mang tính tất định. "
        "Ngược lại, khi quét lưới 60 cấu hình DBSCAN, thuật toán này hoạt động kém hiệu quả do dữ liệu 6 chiều có mật độ biến thiên liên tục, "
        "khiến DBSCAN coi gần một phần tư số quốc gia là nhiễu. Do đó, nhóm chốt K-Means làm thuật toán phân nhóm chính cho đề tài."
    ))

    # =========================================================================
    # SLIDE 10: KIỂM ĐỊNH ĐỘ ỔN ĐỊNH MÔ HÌNH (CHƯƠNG 4) — CÓ BẢNG EXCEL STABILITY ARI
    # =========================================================================
    s10 = add_slide_with_bg()
    add_slide_header(s10, "KIỂM ĐỊNH ĐỘ ỔN ĐỊNH MÔ HÌNH (STABILITY EVALUATION)", "CHƯƠNG 4: BẢNG ĐO LƯỜNG SEEDS NGẪU NHIÊN")

    add_stat_box(s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3), "0.98 – 1.00", "Adjusted Rand Index (ARI)",
                 "Khảo sát trên 10 Random Seeds ngẫu nhiên độc lập mỗi năm; thuật toán hội tụ tuyệt đối sau < 1.0s", COLOR_GREEN_C1)

    img_ari_excel = ARTIFACTS_DIR / "excel_stability_ari.png"
    if img_ari_excel.exists():
        s10.shapes.add_picture(str(img_ari_excel), Inches(4.7), Inches(1.6), width=Inches(7.833))

    set_notes(s10, (
        "Để kiểm tra tính bền vững của kết quả, nhóm đã kiểm tra độ ổn định của K-Means qua 10 lần khởi tạo hạt giống khác nhau. "
        "Bảng số liệu kiểm định bên phải cho thấy chỉ số Adjusted Rand Index đạt xấp xỉ tuyệt đối từ 0,979 đến 1,000, chứng minh thuật toán "
        "hội tụ rất ổn định và không phụ thuộc vào may rủi khởi tạo tâm ban đầu. Sau đây, em xin mời bạn Ngô Quang Trung tiếp tục trình bày "
        "Phần 3 về diễn giải tri thức kinh tế - xã hội và demo ứng dụng."
    ))

    # =========================================================================
    # SLIDE 11: XÂY DỰNG CHÂN DUNG 3 CỤM (CHƯƠNG 5) — CÓ BIỂU ĐỒ RADAR 6 CHIỀU
    # =========================================================================
    s11 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s11, "XÂY DỰNG CHÂN DUNG 3 CỤM KINH TẾ — XÃ HỘI", "CHƯƠNG 5: HÌNH MẠNG NHỆN RADAR 6 CHIỀU")

    c_w = Inches(5.2)
    card_h_c = Inches(1.65)
    gap_c = Inches(0.17)

    add_card(s11, Inches(0.8), Inches(1.6), c_w, card_h_c, border_color=COLOR_GREEN_C1)
    add_card_text(s11, Inches(0.8), Inches(1.6), c_w, card_h_c,
                  header_text="Cụm 1: Phát triển Toàn diện (24–29 nước)",
                  bullets=["Vượt trội về GDP, Tuổi thọ, An sinh và Minh bạch (Bắc Âu, Tây Âu, ANZ)."],
                  header_color=COLOR_GREEN_C1, font_size=15.5, header_size=17.5, space_before=4)

    add_card(s11, Inches(0.8), Inches(1.6) + card_h_c + gap_c, c_w, card_h_c, border_color=COLOR_BLUE_C2)
    add_card_text(s11, Inches(0.8), Inches(1.6) + card_h_c + gap_c, c_w, card_h_c,
                  header_text="Cụm 2: Đang phát triển (79–85 nước)",
                  bullets=["Kinh tế & Tuổi thọ khá; Thể chế và Hảo tâm còn nhiều điểm nghẽn (Việt Nam, ĐNA)."],
                  header_color=COLOR_BLUE_C2, font_size=15.5, header_size=17.5, space_before=4)

    add_card(s11, Inches(0.8), Inches(1.6) + 2 * (card_h_c + gap_c), c_w, card_h_c, border_color=COLOR_CORAL_C3)
    add_card_text(s11, Inches(0.8), Inches(1.6) + 2 * (card_h_c + gap_c), c_w, card_h_c,
                  header_text="Cụm 3: Khó khăn & Tổn thương (46–50 nước)",
                  bullets=["Điểm rất thấp ở an sinh xã hội và y tế cơ sở (Châu Phi hạ Sahara, Xung đột)."],
                  header_color=COLOR_CORAL_C3, font_size=15.5, header_size=17.5, space_before=4)

    img_radar = FIGURES_DIR / "radar_chart_2019.png"
    if img_radar.exists():
        s11.shapes.add_picture(str(img_radar), Inches(6.3), Inches(1.6), width=Inches(6.233))

    set_notes(s11, (
        "Kính chào Thầy, em là Ngô Quang Trung. Bước sang phần diễn giải tri thức, trên biểu đồ radar mạng nhện 6 chiều bên phải, "
        "nhóm đã phác họa rõ nét chân dung của 3 cụm: Cụm 1 là nhóm các nước phát triển toàn diện, đường màu xanh bao trọn cả 6 đỉnh; "
        "Cụm 2 chiếm số đông nhất gồm các nước đang phát triển như Việt Nam và các nước Đông Nam Á, có tăng trưởng kinh tế khá nhưng an sinh "
        "và thể chế cần tiếp tục hoàn thiện. Cụm 3 là nhóm các quốc gia khó khăn và xung đột, cần sự ưu tiên trợ giúp khẩn cấp về y tế và an sinh xã hội."
    ))

    # =========================================================================
    # SLIDE 12: HẬU KIỂM VỚI ĐIỂM HẠNH PHÚC (CHƯƠNG 5) — CÓ BOXPLOT PHÂN HÓA
    # =========================================================================
    s12 = add_slide_with_bg()
    add_slide_header(s12, "HẬU KIỂM ĐỘC LẬP VỚI ĐIỂM HẠNH PHÚC THỰC TẾ", "CHƯƠNG 5: HẬU KIỂM THỐNG KÊ ANOVA")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), border_color=COLOR_AMBER)
    add_card_text(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
                  header_text="Kiểm định Thống kê ANOVA Một nhân tố",
                  bullets=[
                      "Quy tắc vàng: Tuyệt đối không dùng Happiness Score để gom cụm; chỉ dùng ở bước hậu kiểm độc lập.",
                      "Phân hóa sâu sắc giữa 3 cụm:",
                      "  • Cụm 1: Trung bình đạt 6.73 – 6.85 điểm",
                      "  • Cụm 2: Trung bình đạt 5.57 – 5.61 điểm",
                      "  • Cụm 3: Trung bình đạt 4.10 – 4.26 điểm",
                      "Chênh lệch điểm số: Khoảng cách Cụm 1 và Cụm 3 lên tới 2.5 – 2.7 điểm trên thang đo 10.",
                      "Kiểm định ANOVA F = 107.09 – 159.18 qua 5 năm (p-value < 1e-15), khẳng định 6 yếu tố khách quan phản ánh hoàn hảo cảm nhận hạnh phúc thực tế."
                  ],
                  header_color=COLOR_AMBER, font_size=15, header_size=18, space_before=4)

    img_val = FIGURES_DIR / "validation_happiness_score_2019.png"
    if img_val.exists():
        s12.shapes.add_picture(str(img_val), Inches(6.6), Inches(1.6), width=Inches(5.9))

    set_notes(s12, (
        "Tuân thủ nghiêm ngặt quy tắc vàng của đề tài, nhóm không đưa điểm hạnh phúc vào lúc phân cụm mà chỉ dùng để hậu kiểm độc lập. "
        "Biểu đồ phân phối điểm bên phải và kết quả kiểm định ANOVA một nhân tố cho giá trị F từ 107 đến 159, cực kỳ có ý nghĩa thống kê. "
        "Điểm hạnh phúc giữa 3 cụm phân hóa rành mạch và giữ nguyên thứ tự qua cả 5 năm, với mức chênh lệch giữa cụm cao nhất và thấp nhất lên tới hơn 2,5 điểm. "
        "Điều này khẳng định 6 yếu tố cơ sở phản ánh rất sát mức độ hạnh phúc thực tế của con người."
    ))

    # =========================================================================
    # SLIDE 13: THEO DÕI DỊCH CHUYỂN CỤM (CHƯƠNG 5) — CÓ BẢNG EXCEL DỊCH CHUYỂN
    # =========================================================================
    s13 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s13, "THEO DÕI DỊCH CHUYỂN CỤM 156 QUỐC GIA QUA 5 NĂM", "CHƯƠNG 5: BẢNG TRÍCH XUẤT QUỐC GIA BIẾN ĐỘNG")

    add_stat_box(s13, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3), "91.0%", "Quốc gia Ổn định Tuyệt đối",
                 "142 / 156 quốc gia giữ vững nhóm cụm suốt nửa thập kỷ (2015–2019). Cấu trúc hạnh phúc có quán tính thể chế cao.", COLOR_GREEN_C1)

    img_shift_excel = ARTIFACTS_DIR / "excel_country_shift.png"
    if img_shift_excel.exists():
        s13.shapes.add_picture(str(img_shift_excel), Inches(4.7), Inches(1.6), width=Inches(7.833))

    set_notes(s13, (
        "Điểm mới trong đồ án của nhóm là thuật toán ghép cụm liên năm để theo dõi sự dịch chuyển của 156 quốc gia qua nửa thập kỷ. "
        "Kết quả chỉ ra rằng 91% số quốc gia ổn định tuyệt đối trong nhóm của mình. Trên bảng tính bên phải, có 4 quốc gia ghi nhận sự thăng hạng bền vững "
        "gồm Indonesia, Myanmar, Georgia và Botswana nhờ những bước tiến rõ rệt về an sinh xã hội và tuổi thọ khỏe mạnh. "
        "Ngược lại có 2 quốc gia bị suy giảm nhẹ do biến động về thể chế và tham nhũng."
    ))

    # =========================================================================
    # SLIDE 14: DEMO TƯƠNG TÁC STREAMLIT 4 TAB (CHƯƠNG 5) — CÓ GIAO DIỆN APP
    # =========================================================================
    s14 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s14, "TRỰC QUAN HÓA TƯƠNG TÁC — ỨNG DỤNG STREAMLIT 4 TAB", "CHƯƠNG 5: SẢN PHẨM ỨNG DỤNG")

    img_demo = FIGURES_DIR / "demo_app_overview.png"
    if img_demo.exists():
        s14.shapes.add_picture(str(img_demo), Inches(0.8), Inches(1.6), width=Inches(5.7))

    add_card(s14, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3), border_color=COLOR_TEAL_ACCENT)
    add_card_text(s14, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
                  header_text="4 Tab Chức năng Chuyên sâu",
                  bullets=[
                      "Tab 1: Tổng quan cụm & Radar Chart: Trực quan hóa hình mạng nhện so sánh 6 yếu tố, xem thẻ chỉ số KPI Silhouette, DB, CH theo từng năm.",
                      "Tab 2: Bản đồ Thế giới: Bản đồ Choropleth tương tác toàn cầu tô màu theo mã ISO-3, rê chuột xem chi tiết nhóm cụm.",
                      "Tab 3: Tra cứu Quốc gia: Xem tiến trình 5 năm chi tiết của 156 nước (như Việt Nam), đồ thị biến thiên 6 chỉ số.",
                      "Tab 4: Thử nghiệm What-if: Kéo 6 thanh trượt chỉ số giả định, hệ thống tự chuẩn hóa Z-score và gán cụm thời gian thực.",
                      "Tối ưu hiệu năng: Bọc @st.cache_data, phản hồi dưới 0.1 giây."
                  ],
                  header_color=COLOR_TEAL_ACCENT, font_size=15, header_size=18, space_before=4)

    set_notes(s14, (
        "Để biến các tri thức khai phá thành công cụ trực quan hữu ích, nhóm đã xây dựng ứng dụng web tương tác Streamlit với 4 tab chức năng. "
        "Người dùng có thể tùy biến xem biểu đồ radar đa chiều, tra cứu bản đồ địa lý thế giới theo chuẩn ISO-3, tra cứu chi tiết tiến trình "
        "phát triển của từng quốc gia như Việt Nam, và đặc biệt là tab mô phỏng gán nhãn cho một quốc gia giả định bằng cách kéo thanh trượt "
        "6 chỉ số để hệ thống tính toán khoảng cách tâm theo thời gian thực."
    ))

    # =========================================================================
    # SLIDE 15: ĐÓNG GÓP, KẾT LUẬN & HẠN CHẾ (CHƯƠNG 5)
    # =========================================================================
    s15 = add_slide_with_bg()
    add_slide_header(s15, "ĐÓNG GÓP CHÍNH, KẾT LUẬN & HẠN CHẾ ĐỀ TÀI", "CHƯƠNG 5: TỔNG KẾT ĐỀ TÀI")

    col_w = Inches(5.7)
    c1_x = Inches(0.8)
    c2_x = Inches(6.83)
    c_y = Inches(1.6)
    c_h = Inches(5.3)

    add_card(s15, c1_x, c_y, col_w, c_h, border_color=COLOR_GREEN_C1)
    add_card_text(s15, c1_x, c_y, col_w, c_h,
                  header_text="Đóng góp Cốt lõi của Đề tài",
                  bullets=[
                      "Pipeline nghiên cứu chuẩn mực: 11 bước khép kín từ tiền xử lý, EDA đến đóng gói ứng dụng, khả năng chạy lại 100%.",
                      "Lập trình From Scratch thành công: Tự cài đặt K-Means++, Hierarchical Ward và các độ đo đánh giá, đối chứng khớp scikit-learn sai số < 1e-4.",
                      "Phát hiện thực nghiệm vững chắc: Chứng minh số cụm tối ưu k* = 3 đồng thuận qua cả 5 năm liên tiếp.",
                      "Sản phẩm ứng dụng thực tiễn: Bảng theo dõi dịch chuyển cụm 156 nước và web app tương tác 4 tab hoàn chỉnh."
                  ],
                  header_color=COLOR_GREEN_C1, font_size=17)

    add_card(s15, c2_x, c_y, col_w, c_h, border_color=COLOR_CORAL_C3)
    add_card_text(s15, c2_x, c_y, col_w, c_h,
                  header_text="Hạn chế Nghiên cứu",
                  bullets=[
                      "Phạm vi biến số giới hạn: Báo cáo WHR chỉ gồm 6 yếu tố cơ bản, chưa bao quát bất bình đẳng thu nhập nội bộ (hệ số Gini) hay yếu tố văn hóa bản địa.",
                      "Giả định khoảng cách Euclid: Coi các trục đặc trưng trực giao, chưa mô hình hóa phi tuyến sâu giữa các biến có tương quan cao như GDP và Tuổi thọ.",
                      "Dữ liệu khảo sát mẫu: Gallup World Poll có độ lệch biên nhất định tại các vùng đang có xung đột địa chính trị."
                  ],
                  header_color=COLOR_CORAL_C3, font_size=17)

    set_notes(s15, (
        "Tóm lại, đề tài đã hoàn thành xuất sắc các mục tiêu đề ra với một pipeline hoàn chỉnh, thuật toán tự lập trình chuẩn xác "
        "và những phát hiện thực tế có giá trị về sự phân tầng hạnh phúc thế giới. Tuy vậy, nghiên cứu vẫn còn hạn chế do bộ dữ liệu chưa có "
        "các chỉ số về văn hóa và chênh lệch giàu nghèo nội bộ, điều mà nhóm mong muốn tiếp tục hoàn thiện trong tương lai."
    ))

    # =========================================================================
    # SLIDE 16: HƯỚNG PHÁT TRIỂN & NGHIÊN CỨU MỞ RỘNG (TÁCH THÀNH SLIDE RIÊNG)
    # =========================================================================
    s16 = add_slide_with_bg(transition_type="push", direction="l")
    add_slide_header(s16, "HƯỚNG PHÁT TRIỂN & NGHIÊN CỨU MỞ RỘNG", "CHƯƠNG 5: HƯỚNG MỞ RỘNG ĐỀ TÀI")

    col_w16 = Inches(3.7)
    gap16 = Inches(0.31)
    start_x16 = Inches(0.8)
    c_y16 = Inches(1.6)
    c_h16 = Inches(5.3)

    # Cột 1: Mở rộng chuỗi dữ liệu
    add_card(s16, start_x16, c_y16, col_w16, c_h16, border_color=COLOR_GREEN_C1)
    add_card_text(s16, start_x16, c_y16, col_w16, c_h16,
                  header_text="1. Mở rộng Chuỗi Dữ liệu (2020–2024)",
                  bullets=[
                      "Kéo dài chuỗi thời gian sang giai đoạn đại dịch COVID-19 và phục hồi.",
                      "Đo lường độ chống chịu của 3 cụm trước khủng hoảng y tế và lạm phát.",
                      "Khám phá xu hướng tái định hình trật tự hạnh phúc trong thập kỷ mới."
                  ],
                  header_color=COLOR_GREEN_C1, font_size=15.5, header_size=18, space_before=6)

    # Cột 2: Bổ sung chỉ số vi mô
    add_card(s16, start_x16 + col_w16 + gap16, c_y16, col_w16, c_h16, border_color=COLOR_BLUE_C2)
    add_card_text(s16, start_x16 + col_w16 + gap16, c_y16, col_w16, c_h16,
                  header_text="2. Bổ sung Chỉ số Vi mô (World Bank)",
                  bullets=[
                      "Tích hợp hệ số bất bình đẳng thu nhập Gini vào không gian phân tích.",
                      "Bổ sung chi tiêu ngân sách cho an sinh xã hội và giáo dục cơ sở.",
                      "Phản ánh chính xác phân hóa giàu - nghèo nội bộ thay vì chỉ xét bình quân."
                  ],
                  header_color=COLOR_BLUE_C2, font_size=15.5, header_size=18, space_before=6)

    # Cột 3: Thuật toán nâng cao
    add_card(s16, start_x16 + 2 * (col_w16 + gap16), c_y16, col_w16, c_h16, border_color=COLOR_AMBER)
    add_card_text(s16, start_x16 + 2 * (col_w16 + gap16), c_y16, col_w16, c_h16,
                  header_text="3. Thuật toán Gom cụm Nâng cao",
                  bullets=[
                      "Thử nghiệm phân cụm mờ (Fuzzy C-Means) cho quốc gia vùng biên.",
                      "Áp dụng mô hình hỗn hợp Gauss (GMM) tính xác suất mềm thuộc về cụm.",
                      "Phân cụm chuỗi thời gian (Time-series Clustering) với độ đo khoảng cách DTW."
                  ],
                  header_color=COLOR_AMBER, font_size=15.5, header_size=18, space_before=6)

    set_notes(s16, (
        "Trong giai đoạn tiếp theo, nhóm định hướng mở rộng nghiên cứu theo 3 hướng trọng tâm: "
        "Thứ nhất là cập nhật chuỗi dữ liệu sang giai đoạn 2020–2024 để đo lường biến động của đại dịch COVID-19 và suy thoái kinh tế lên cấu trúc cụm hạnh phúc; "
        "thứ hai là bổ sung thêm các chỉ số vi mô như hệ số bất bình đẳng Gini và chi tiêu an sinh xã hội từ World Bank; "
        "và thứ ba là thử nghiệm các mô hình phân cụm nâng cao như Fuzzy C-Means và Time-series Clustering để phân tích sâu hơn các quốc gia chuyển tiếp."
    ))

    # =========================================================================
    # SLIDE 17: LỜI CẢM ƠN & PHIÊN VẤN ĐÁP (Q&A) (DARK BACKGROUND)
    # =========================================================================
    s17 = add_slide_with_bg(dark_mode=True)
    add_slide_header(s17, "LỜI CẢM ƠN & PHIÊN VẤN ĐÁP (Q&A)", "KẾT THÚC BÁO CÁO ĐỒ ÁN", dark_mode=True)

    # Khối cảm ơn trung tâm (Hero Thank-you Card)
    add_card(s17, Inches(1.0), Inches(1.6), Inches(11.333), Inches(2.4), bg_color=RGBColor(30, 41, 59), border_color=COLOR_GOLD_TEXT)
    tb_thx = s17.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(10.933), Inches(2.4))
    tf_thx = tb_thx.text_frame
    tf_thx.word_wrap = True
    tf_thx.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_thx.margin_left = tf_thx.margin_top = tf_thx.margin_right = tf_thx.margin_bottom = 0

    p_t1 = tf_thx.paragraphs[0]
    p_t1.text = "XIN CHÂN THÀNH CẢM ƠN THẦY VÀ HỘI ĐỒNG!"
    p_t1.font.name = FONT_FAMILY
    p_t1.font.size = Pt(28)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_GOLD_TEXT
    p_t1.alignment = PP_ALIGN.CENTER

    p_t2 = tf_thx.add_paragraph()
    p_t2.text = "Cả 3 thành viên Nhóm 12 sẵn sàng lắng nghe và giải đáp các câu hỏi phản biện từ Quý Thầy Cô."
    p_t2.font.name = FONT_FAMILY
    p_t2.font.size = Pt(18)
    p_t2.font.color.rgb = COLOR_WHITE
    p_t2.alignment = PP_ALIGN.CENTER
    p_t2.space_before = Pt(8)

    p_t3 = tf_thx.add_paragraph()
    p_t3.text = "Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report 2015–2019)"
    p_t3.font.name = FONT_FAMILY
    p_t3.font.size = Pt(15)
    p_t3.font.color.rgb = RGBColor(148, 163, 184)
    p_t3.alignment = PP_ALIGN.CENTER
    p_t3.space_before = Pt(6)

    # 3 thẻ thành viên nhóm ở hàng dưới
    card_w17 = Inches(3.6)
    card_gap17 = Inches(0.26)
    start_x17 = Inches(1.0)
    card_y17 = Inches(4.3)
    card_h17 = Inches(2.25)

    for i, (name, mssv, role, accent_col) in enumerate(members):
        cx = start_x17 + i * (card_w17 + card_gap17)
        add_card(s17, cx, card_y17, card_w17, card_h17, bg_color=RGBColor(30, 41, 59), border_color=accent_col)
        tb_m17 = s17.shapes.add_textbox(cx + Inches(0.2), card_y17, card_w17 - Inches(0.4), card_h17)
        tf_m17 = tb_m17.text_frame
        tf_m17.word_wrap = True
        tf_m17.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_m17.margin_left = tf_m17.margin_top = tf_m17.margin_right = tf_m17.margin_bottom = 0

        p_name = tf_m17.paragraphs[0]
        p_name.text = name
        p_name.font.name = FONT_FAMILY
        p_name.font.size = Pt(19.5)
        p_name.font.bold = True
        p_name.font.color.rgb = COLOR_WHITE
        p_name.alignment = PP_ALIGN.CENTER

        p_id = tf_m17.add_paragraph()
        p_id.text = f"MSSV: {mssv}"
        p_id.font.name = FONT_FAMILY
        p_id.font.size = Pt(15)
        p_id.font.color.rgb = COLOR_GOLD_TEXT
        p_id.alignment = PP_ALIGN.CENTER
        p_id.space_before = Pt(4)

        p_role = tf_m17.add_paragraph()
        p_role.text = role
        p_role.font.name = FONT_FAMILY
        p_role.font.size = Pt(14.5)
        p_role.font.color.rgb = RGBColor(226, 232, 240)
        p_role.alignment = PP_ALIGN.CENTER
        p_role.space_before = Pt(6)

    # Dòng ghi chú chân trang
    tb_foot17 = s17.shapes.add_textbox(Inches(1.0), Inches(6.75), Inches(11.333), Inches(0.5))
    tf_foot17 = tb_foot17.text_frame
    p_foot = tf_foot17.paragraphs[0]
    p_foot.text = "Mã nguồn From Scratch, Dữ liệu chuẩn hóa 781 dòng & Ứng dụng Streamlit 4 tab đã sẵn sàng."
    p_foot.font.name = FONT_FAMILY
    p_foot.font.size = Pt(13.5)
    p_foot.font.color.rgb = RGBColor(100, 116, 139)
    p_foot.alignment = PP_ALIGN.CENTER

    set_notes(s17, (
        "Đến đây, phần báo cáo của Nhóm 12 xin phép được khép lại. "
        "Chúng em xin chân thành cảm ơn Thầy và Quý Hội đồng đã dành thời gian theo dõi bài thuyết trình của nhóm. "
        "Bây giờ cả 3 thành viên chúng em xin sẵn sàng lắng nghe các câu hỏi, góp ý quý báu và trả lời phản biện từ Thầy ạ. "
        "Em xin trân trọng cảm ơn!"
    ))

    # Lưu tệp PowerPoint
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUTPUT_PPTX))
    print(f"Đã tạo thành công bộ slide {len(prs.slides)} trang với ảnh thực chứng: {OUTPUT_PPTX}")
    print(f"Tổng số slide: {len(prs.slides)}")

if __name__ == "__main__":
    build_presentation()

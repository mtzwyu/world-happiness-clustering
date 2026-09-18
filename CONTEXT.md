# World Happiness Clustering Context

Ngữ cảnh nghiệp vụ cho Đề tài 16: Phân nhóm các quốc gia dựa trên các chỉ số hạnh phúc từ báo cáo World Happiness Report (WHR).

## Core Factors (6 Đặc trưng cơ sở)

Ma trận đặc trưng $X$ dùng để gom cụm hoàn toàn chỉ được tạo thành từ 6 yếu tố cơ sở này:

**GDP per Capita**:
Mức độ đóng góp của thu nhập bình quân đầu người vào sự hạnh phúc của quốc gia.
_Avoid_: Economic score, Income, GDP thô

**Social Support**:
Mức độ tương trợ xã hội khi người dân gặp khó khăn (tương đương Family ở báo cáo các năm cũ).
_Avoid_: Family support, Social welfare

**Healthy Life Expectancy**:
Tuổi thọ trung bình khỏe mạnh dự tính của người dân tại quốc gia.
_Avoid_: Health score, Life span, Tuổi thọ tổng quát

**Freedom**:
Mức độ tự do của người dân trong việc đưa ra các quyết định và lựa chọn cuộc sống.
_Avoid_: Liberty, Democracy, Freedom of speech

**Generosity**:
Mức độ đóng góp thiện nguyện và sự hào phóng của người dân đối với cộng đồng.
_Avoid_: Charity score, Altruism

**Perceptions of Corruption**:
Mức độ niềm tin của người dân vào sự trong sạch của chính phủ và doanh nghiệp (tham nhũng càng thấp thì chỉ số càng cao).
_Avoid_: Trust, Corruption rate, Government integrity

---

## Evaluation & Invariants (Thuật ngữ đánh giá & Ranh giới)

**Happiness Score**:
Điểm số hạnh phúc tổng thể (hoặc Ladder Score) do người dân tự đánh giá trên thang điểm từ 0 đến 10. Thuộc tính này là biến mục tiêu dùng ĐỘC LẬP để hậu kiểm và đối chiếu ở bước diễn giải tri thức.
_Avoid_: Feature gom cụm, Biến đầu vào, Thuộc tính X

**Happiness Rank**:
Thứ hạng hạnh phúc của các quốc gia trên toàn cầu.
_Avoid_: Rank feature, Cột gom cụm

**Cluster Profile**:
Bức chân dung định tính của từng nhóm quốc gia sau khi gom cụm (ví dụ: nhóm Phát triển toàn diện, nhóm Đang phát triển phụ thuộc kinh tế, nhóm Kém phát triển).
_Avoid_: Cluster label, Nhóm số nguyên thuần túy

---

## Methodology & Pipeline (Phương pháp luận)

**11-Step Pipeline**:
Chu trình khai phá dữ liệu 11 bước bắt buộc theo đề cương: (1) Xác định bài toán → (2) Hiểu dữ liệu → (3) Tiền xử lý → (4) Khám phá EDA → (5) Biến đổi đặc trưng → (6) Huấn luyện mô hình → (7) So sánh phương án → (8) Tinh chỉnh tham số → (9) Diễn giải tri thức → (10) Demo tương tác → (11) Đánh giá & Hạn chế.
_Avoid_: Ad-hoc analysis, Quy trình tự do

**From-Scratch Algorithm**:
Thuật toán do sinh viên tự code logic toán học từng bước bằng NumPy/Pandas cơ bản, không sử dụng API huấn luyện của thư viện Scikit-Learn.
_Avoid_: Black-box model, Built-in clusterer

# CẨM NANG VẤN ĐÁP BẢO VỆ ĐỒ ÁN & KỊCH BẢN THUYẾT MINH VIDEO

**Học phần:** Khai thác dữ liệu (Data Mining) — Đề tài 16: World Happiness Report  
**Sinh viên chuẩn bị:** Hà Mạnh Trường (MSSV: 2045240326, Nhóm trưởng Nhóm 12)  
**Phân công chuyên môn:** Phụ trách Chương 1 (Tổng quan), Chương 2 (Tiền xử lý dữ liệu), Quản trị Pipeline nhóm và Thuyết trình Phần 1 (Slide 1–4)  
**Tài liệu căn cứ:** [`reports/final_report/nhiem_vu_ha_manh_truong.md`](final_report/nhiem_vu_ha_manh_truong.md) & [`reports/final_report/Nhom12_BaoCao.docx`](final_report/Nhom12_BaoCao.docx)

---

## PHẦN 1: 5 CÂU HỎI THEN CHỐT VỀ TIỀN XỬ LÝ & LÀM SẠCH DỮ LIỆU

### Câu hỏi 1: Tại sao nhóm tuyệt đối không đưa `Happiness Score` hay `Happiness Rank` vào ma trận đặc trưng $X$ để gom cụm?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, đây là **quy tắc vàng** mang tính cốt lõi của Đề tài 16 trong Đề cương môn học.  
  - Thứ nhất, `Happiness Score` là điểm số khảo sát chủ quan (Cantril Ladder) do người dân tự đánh giá từ 0 đến 10, trong khi mục tiêu nghiên cứu của nhóm là **khám phá cấu trúc phân nhóm tự nhiên** của các quốc gia thuần túy dựa trên 6 yếu tố khách quan về kinh tế, y tế, xã hội và thể chế (`GDP per capita`, `Social support`, `Healthy life expectancy`, `Freedom`, `Generosity`, `Perceptions of corruption`).
  - Thứ hai, nếu đưa `Happiness Score` vào gom cụm, do điểm số này có độ biến thiên lớn và tương quan rất mạnh với thứ hạng, thuật toán sẽ bị chi phối và biến bài toán thành việc 'cắt khúc điểm hạnh phúc' (nhóm điểm cao, điểm trung bình, điểm thấp) một cách cơ học, làm lu mờ hoàn toàn các đặc trưng cấu trúc nội tại giữa 6 yếu tố.
  - Nhóm chỉ sử dụng `Happiness Score` ở **Bước 9 (Hậu kiểm)** để đối chiếu xem: sau khi gom cụm hoàn toàn độc lập từ 6 đặc trưng cơ sở, các cụm tự nhiên hình thành có phản ánh sự phân hóa điểm hạnh phúc thực tế hay không. Kết quả kiểm định ANOVA một nhân tố cho thấy $F > 450$ và $p\text{-value} < 10^{-15}$, chứng minh cấu trúc 3 cụm tự nhiên phân hóa triệt để mức độ hạnh phúc mà không hề bị 'rò rỉ nhãn' (data leakage)."

---

### Câu hỏi 2: Dữ liệu 5 năm (2015–2019) có cấu trúc cột và số lượng cột rất khác nhau, nhóm đã đồng nhất schema như thế nào để không bị mất mát dữ liệu?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, bộ dữ liệu Kaggle thô có sự biến động lớn về cấu trúc qua các năm:
  - Năm 2015 và 2016 có 12 cột, tên cột dạng tiếng Anh có dấu cách như `Economy (GDP per Capita)`, `Trust (Government Corruption)`.
  - Năm 2017 có 12 cột nhưng lại dùng dấu chấm như `Economy..GDP.per.Capita.`, `Trust..Government.Corruption.`.
  - Năm 2018 và 2019 giảm xuống còn 9 cột, tên cột đổi thành `GDP per capita`, `Perceptions of corruption`, và bỏ hẳn các cột `Region`, `Standard Error`, `Dystopia Residual`.
  
  Để giải quyết triệt để vấn đề này trong module [`src/data/data_loader.py`](file:///C:/Users/xpaga/Documents/data_mining/src/data/data_loader.py), em đã thiết kế quy trình 3 bước:
  1. Xây dựng từ điển ánh xạ chuẩn `COLUMN_MAPPING` để đổi tên toàn bộ các biến qua 5 năm về định dạng thống nhất `snake_case`.
  2. Xây dựng cơ chế khôi phục trường `Region` (Khu vực địa lý): Vì năm 2017–2019 tác giả bỏ cột `Region`, em đã trích xuất bảng từ điển quốc gia – khu vực từ dữ liệu 2015–2016 để tự động ánh xạ lại cho các năm sau, đồng thời bổ sung ngoại lệ (như `Gambia` thuộc `Sub-Saharan Africa`).
  3. Lọc bỏ các cột sai số đo lường khảo sát (`Standard Error`, `Whisker.high`, `Whisker.low`) vì chúng chỉ là chỉ số thống kê sai số mẫu, không phải đặc tính quốc gia. Kết quả là bảng dữ liệu trung gian chuẩn `data/interim/happiness_merged.csv` đạt chuẩn cấu trúc 13 cột đồng nhất cho toàn bộ 781 dòng."

---

### Câu hỏi 3: Tại sao năm 2018 quốc gia United Arab Emirates (UAE) bị khuyết chỉ số tham nhũng, nhóm lại chọn cách loại bỏ bản ghi đó thay vì dùng kỹ thuật Imputation (điền trung bình hoặc KNN)?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, trong 782 quan sát thô của 5 năm, toàn bộ tập dữ liệu chỉ xuất hiện duy nhất **1 ô bị thiếu giá trị NaN**, đó là chỉ số `Perceptions of corruption` của Các Tiểu vương quốc Ả Rập Thống nhất (UAE) năm 2018.  
  Nhóm em đã cân nhắc rất kỹ giữa hai phương án:
  - **Phương án 1 (Imputation):** Dùng giá trị trung bình toàn cầu hoặc nội suy từ năm 2017/2019 của chính UAE. Tuy nhiên, UAE là một quốc gia đặc thù ở Trung Đông với mức GDP và chất lượng sống rất cao, nếu dùng trung bình thế giới sẽ kéo tụt chỉ số thể chế của họ xuống sai lệch thực tế; nếu dùng KNN thì khoảng cách trong không gian 5 chiều còn lại có thể bị méo do các quốc gia gần về GDP chưa chắc đã tương đồng về mô hình quản trị.
  - **Phương án 2 (Loại bỏ bản ghi):** Do tập dữ liệu có tới 782 dòng, việc loại bỏ 1 dòng khuyết duy nhất chỉ làm giảm 0,128% tổng số mẫu, hoàn toàn không ảnh hưởng đến độ lớn hay tính đại diện thống kê của tập dữ liệu.
  
  Quan trọng hơn, việc loại bỏ bản ghi này bảo đảm ma trận dữ liệu đầu vào $X$ đạt độ tinh khiết 100% sạch không khuyết thiếu, giúp thuật toán gom cụm K-Means và Hierarchical from-scratch không phải chịu bất kỳ sự suy đoán nhân tạo nào từ khâu điền dữ liệu. Do đó, tập dữ liệu interim chốt chính xác ở **781 dòng sạch hoàn hảo**."

---

### Câu hỏi 4: Nhóm đã xử lý sự không nhất quán về tên quốc gia và bổ sung mã hóa ISO-3 (`iso_alpha`) như thế nào?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, qua 5 năm báo cáo, tên của một số quốc gia bị thay đổi do đổi tên chính thức hoặc cách ghi của các tổ chức khác nhau:
  - Ví dụ: `Macedonia` đổi thành `North Macedonia`, `Swaziland` đổi thành `Eswatini`, `Hong Kong S.A.R., China` đổi thành `Hong Kong`, `Taiwan Province of China` đổi thành `Taiwan`.
  - Nếu không chuẩn hóa, khi nhóm thực hiện theo dõi chuỗi thời gian (Time-series cluster shifts), hệ thống sẽ hiểu lầm đây là các quốc gia khác nhau và làm đứt đoạn chuỗi quan sát 5 năm.
  - Em đã xây dựng từ điển `COUNTRY_NAME_FIXES` để quy đổi toàn bộ về tên địa lý chuẩn quốc tế.
  - Đồng thời, em đã lập từ điển ánh xạ `ISO3_MAP` bổ sung mã chuẩn **ISO 3166-1 alpha-3** (như VNM cho Việt Nam, USA cho Mỹ, FRA cho Pháp) cho toàn bộ 156 quốc gia. Việc chuẩn hóa mã ISO-3 này là điều kiện tiên quyết giúp ứng dụng Streamlit có thể vẽ bản đồ nhiệt toàn cầu (Choropleth Map) chuẩn xác từng tọa độ lãnh thổ mà không bị lỗi nhận diện địa danh."

---

### Câu hỏi 5: Tại sao nhóm lại lựa chọn phương pháp chuẩn hóa thang đo Min-Max Scaling [0, 1] thay vì Z-score Standardization?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, trong các thuật toán dựa trên khoảng cách như K-Means hay Hierarchical (Ward), nếu không chuẩn hóa thang đo thì đặc trưng có miền giá trị lớn hơn sẽ chi phối hoàn toàn hàm khoảng cách Euclid.  
  Nhóm đã phân tích và quyết định chọn **Min-Max Scaling** đưa toàn bộ 6 đặc trưng về miền $[0, 1]$ vì 3 lý do kỹ thuật:
  1. *Bản chất của dữ liệu WHR:* Bản thân các chỉ số trong WHR vốn đã là các điểm ước lượng đóng góp (contributions) có chặn dưới là 0 (đại diện cho quốc gia giả định kém nhất - Dystopia). Min-Max Scaling bảo toàn trọn vẹn điểm mốc 0 tuyệt đối này.
  2. *Tránh giá trị âm gây khó khăn khi vẽ Radar Chart:* Z-score đưa dữ liệu về trung bình bằng 0 và độ lệch chuẩn bằng 1, dẫn đến việc xuất hiện các giá trị âm. Khi trực quan hóa hồ sơ cụm trên biểu đồ Radar đa chiều (Tab 1 & 2 của Demo), các giá trị âm sẽ gây khó khăn và trực quan sai lệch cho người xem. Min-Max giữ toàn bộ giá trị dương trong $[0, 1]$, giúp trục Radar thể hiện trực quan mức độ phát triển từ thấp đến cao rất tự nhiên.
  3. *Không làm thay đổi hình dạng phân phối:* Min-Max Scaling là một phép biến đổi tuyến tính, nó bảo toàn tỷ lệ khoảng cách tương đối giữa các quốc gia trong từng chiều đặc trưng."

---

## PHẦN 2: 3 CÂU HỎI PHẢN BIỆN CHÉO & LÀM CHỦ TOÀN BỘ PIPELINE

### Câu hỏi 6 (Hỗ trợ Huỳnh Tâm Trí về Thuật toán From-scratch): Nhóm tự cài đặt thuật toán gom cụm thì khác gì so với gọi hàm thư viện `sklearn.cluster.KMeans`?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, tinh thần lớn nhất của đồ án nhóm 12 là **Learning-First (Học để hiểu sâu bản chất)**.
  - Thay vì xem thư viện Scikit-learn như một chiếc 'hộp đen' (black-box), nhóm em đã tự tay lập trình từng công thức toán học bằng thư viện cơ bản `numpy`:
    - Tự lập trình thuật toán khởi tạo tâm **K-Means++**: tính khoảng cách ngắn nhất $D(x)$ từ mỗi điểm đến tâm gần nhất, sau đó lấy mẫu tâm tiếp theo theo phân phối xác suất tỷ lệ thuận với bình phương khoảng cách $P(x) = \frac{D(x)^2}{\sum D(x')^2}$ để các tâm ban đầu nằm cách xa nhau tối đa.
    - Tự lập trình vòng lặp gán nhãn theo khoảng cách Euclid và tái tính toán trọng tâm bằng `np.mean`.
    - Tự cài đặt thuật toán phân cấp tích tụ theo liên kết **Ward**: tính toán độ gia tăng tổng bình phương sai lệch $\Delta \text{WSS}(A, B) = \frac{n_A n_B}{n_A + n_B} \lVert \mu_A - \mu_B \rVert^2$ để quyết định gộp hai cụm nào ở mỗi bước.
  - Để kiểm chứng tính đúng đắn, nhóm đã viết script độc lập [`scripts/verify_scratch_implementations.py`](file:///C:/Users/xpaga/Documents/data_mining/scripts/verify_scratch_implementations.py) đối chiếu trực tiếp với Scikit-learn và SciPy. Kết quả đạt chỉ số tương đồng $\text{ARI} = 1.000000$ và sai số giá trị Inertia/Silhouette nhỏ hơn $10^{-10}$, chứng minh thuật toán tự viết hoạt động chuẩn xác tuyệt đối theo nguyên lý toán học."

---

### Câu hỏi 7 (Hỗ trợ Ngô Quang Trung về Demo Streamlit): Trong ứng dụng Demo Tab 4, khi người dùng nhập 6 chỉ số giả định mới, hệ thống dự báo cụm bằng cách nào? Có cần huấn luyện lại mô hình không?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, hệ thống **hoàn toàn không cần huấn luyện lại (re-train)** từ đầu, đảm bảo thời gian phản hồi tức thì dưới 0.1 giây.
  - Cơ chế dự báo cụm trực tiếp (Online Inference) diễn ra như sau:
    1. Khi người dùng điều chỉnh 6 thanh trượt trên giao diện Streamlit, giá trị đầu vào được chuẩn hóa theo đúng dải min-max của năm mô hình được chọn.
    2. Hệ thống tải vector trọng tâm đã được huấn luyện sẵn của 3 cụm ($\mu_0, \mu_1, \mu_2$).
    3. Tính toán khoảng cách Euclid từ vector mới $x_{\text{new}}$ đến từng tâm cụm: $d_j = \lVert x_{\text{new}} - \mu_j \rVert$.
    4. Gán mẫu mới vào cụm có khoảng cách ngắn nhất: $C^* = \arg\min_j d_j$.
  - Đồng thời, giao diện ngay lập tức vẽ chồng vector mới này lên biểu đồ Radar của 3 cụm để người dùng trực quan thấy quốc gia giả định đó vượt trội hay tụt hậu ở tiêu chí nào so với mặt bằng chung thế giới."

---

### Câu hỏi 8: Nhóm đã phát hiện những ngoại lệ (Outliers) nào trong dữ liệu và tại sao nhóm không loại bỏ chúng?
* **Trả lời trọng tâm:**  
  "Thưa thầy/cô, trong quá trình EDA bằng biểu đồ Boxplot và phân tích phân vị $IQR$, nhóm phát hiện một số quốc gia có giá trị cực trị rõ rệt:
  - Quốc gia **Rwanda**: có chỉ số `Perceptions of corruption` cao đột biến so với phần còn lại của châu Phi nhờ các chính sách chống tham nhũng quyết liệt của chính phủ.
  - Quốc gia **Botswana**: dù có mức GDP per capita khá cao ở châu Phi nhưng điểm số `Generosity` lại rất thấp.
  - Các quốc gia Bắc Âu (Phần Lan, Đan Mạch): chỉ số hạnh phúc và niềm tin thể chế liên tục đứng đỉnh thế giới.
  
  Nhóm em quyết định **giữ lại toàn bộ các giá trị ngoại lệ này**, bởi vì trong dữ liệu kinh tế - xã hội vĩ mô, mỗi quốc gia là một thực thể độc lập có bối cảnh lịch sử và thể chế riêng biệt. Đây là **ngoại lệ thực tế có ý nghĩa kinh tế - xã hội** (meaningful natural outliers), không phải lỗi nhập liệu hay nhiễu kỹ thuật. Nếu máy móc loại bỏ chúng, ta sẽ làm mất đi tính toàn vẹn của bức tranh địa chính trị toàn cầu."

---

## PHẦN 3: KỊCH BẢN THUYẾT MINH VIDEO BÁO CÁO (PHẦN 1: SLIDE 1–4)

* **Người thuyết trình:** Hà Mạnh Trường (Nhóm trưởng)  
* **Thời lượng phân bổ:** Đúng 3 phút 30 giây (trong tổng số 12 phút của nhóm)  
* **Phạm vi slide:** Slide 1 đến Slide 4

```
[SLIDE 1: TRANG BÌA — 00:00 - 00:30]
"Kính chào Thầy và các bạn! 
Em là Hà Mạnh Trường, nhóm trưởng Nhóm 12. 
Hôm nay, nhóm chúng em gồm em, bạn Huỳnh Tâm Trí và bạn Ngô Quang Trung xin được báo cáo đề tài Đồ án môn Khai thác dữ liệu: 
'Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc dựa trên bộ dữ liệu World Happiness Report giai đoạn 2015–2019'.
Bài báo cáo của nhóm sẽ bám sát trọn vẹn 11 bước của pipeline khai thác dữ liệu chuẩn, gồm 3 phần chính do cả 3 thành viên lần lượt trình bày: 
Em sẽ bắt đầu với phần Tổng quan và Quy trình Tiền xử lý dữ liệu."

[SLIDE 2: BỐI CẢNH & CÂU HỎI NGHIÊN CỨU — 00:30 - 01:30]
"Thưa Thầy, Báo cáo Hạnh phúc Thế giới hàng năm thường thu hút sự chú ý qua bảng xếp hạng đơn chiều. 
Tuy nhiên, câu hỏi cốt lõi mà nhóm đặt ra là: Liệu thứ hạng hạnh phúc có phản ánh đầy đủ mô hình phát triển nội tại của một quốc gia? 
Các quốc gia có cùng mức thu nhập hay cùng khu vực địa lý có thực sự chia sẻ những đặc trưng tương tự nhau về sức khỏe, tự do và niềm tin thể chế hay không?
Từ đó, mục tiêu nghiên cứu của nhóm là: Áp dụng các thuật toán gom cụm không giám sát nhằm phát hiện cấu trúc phân nhóm tự nhiên của các quốc gia dựa trên 6 yếu tố cơ sở: GDP bình quân đầu người, hỗ trợ xã hội, tuổi thọ kỳ vọng, tự do lựa chọn, độ hào phóng và niềm tin chống tham nhũng. 
Đặc biệt, nhóm tuân thủ quy tắc vàng: Tuyệt đối không dùng Happiness Score hay thứ hạng để gom cụm, mà chỉ dùng để hậu kiểm tri thức ở bước cuối cùng."

[SLIDE 3: KIẾN TRÚC PIPELINE 11 BƯỚC — 01:30 - 02:30]
"Để hiện thực hóa mục tiêu trên, nhóm đã thiết lập kiến trúc pipeline hoàn chỉnh gồm 11 bước nghiêm ngặt theo đề cương môn học:
Khởi đầu từ việc Xác định bài toán và Hiểu dữ liệu thô, tiến hành Tiền xử lý và Làm sạch 5 năm dữ liệu thành bộ dữ liệu trung gian 781 dòng.
Tiếp theo, dữ liệu được khám phá đa chiều qua EDA và chuẩn hóa bằng Min-Max Scaling.
Tại tầng khai thác mẫu, nhóm tự cài đặt thuật toán K-Means, Ward Hierarchical và DBSCAN from-scratch bằng NumPy, kết hợp khảo sát độ nhạy tham số và kiểm tra độ ổn định liên năm qua chỉ số ARI.
Cuối cùng, tri thức được diễn giải thành hồ sơ 3 cụm phát triển toàn cầu, kiểm định thống kê ANOVA và đóng gói thành ứng dụng Streamlit tương tác 4 tab."

[SLIDE 4: QUY TRÌNH TIỀN XỬ LÝ 5 NĂM DỮ LIỆU — 02:30 - 03:30]
"Về khâu tiền xử lý, dữ liệu 5 năm từ Kaggle có cấu trúc cột rất phân mảnh. 
Nhóm đã xây dựng từ điển ánh xạ chuẩn hóa tên cột về snake_case, đồng bộ hóa tên các quốc gia bị biến động như North Macedonia hay Eswatini, và gắn mã định danh ISO-3 cho 100% bản ghi phục vụ bản đồ thế giới.
Về xử lý khuyết thiếu, trong 782 mẫu thô chỉ có duy nhất bản ghi UAE năm 2018 bị khuyết chỉ số tham nhũng. 
Nhóm quyết định loại bỏ mẫu này thay vì điền ước lượng, giúp ma trận 781 dòng sạch tuyệt đối mà không gây nhiễu thuật toán.
Các cột sai số khảo sát như Standard Error hay Whisker cũng được loại bỏ hoàn toàn.
Sau khi làm sạch, dữ liệu được chuẩn hóa Min-Max về đoạn [0, 1] để bảo toàn tính bị chặn tự nhiên và phục vụ vẽ biểu đồ Radar.
Toàn bộ mã nguồn tiền xử lý đã được kiểm thử tự động đạt chuẩn 100% trên máy sạch.
Sau đây, em xin kính mời bạn Huỳnh Tâm Trí tiếp tục trình bày Phần 2 về Cơ sở thuật toán From-scratch và Thực nghiệm so sánh mô hình."
```

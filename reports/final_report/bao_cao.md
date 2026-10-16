# Tóm tắt

Báo cáo này trình bày kết quả gom cụm các quốc gia theo sáu yếu tố cơ sở của World Happiness Report giai đoạn 2015–2019: GDP bình quân đầu người, hỗ trợ xã hội, tuổi thọ khỏe mạnh, tự do lựa chọn cuộc sống, mức độ hào phóng và nhận thức tham nhũng. Dữ liệu thô gồm 782 bản ghi của 5 năm; sau khi loại bản ghi United Arab Emirates năm 2018 vì khuyết chỉ số tham nhũng, bảng phân tích còn 781 bản ghi.

Nhóm chạy năm thí nghiệm độc lập, mỗi năm gom cụm riêng trên ma trận sáu đặc trưng đã chuẩn hóa Z-score. Số cụm tối ưu theo Silhouette là k* = 3 ở cả năm năm, với Silhouette trong khoảng 0,293–0,344 và Davies–Bouldin 1,00–1,07. Ba cụm có chân dung kinh tế – xã hội tách biệt và khi hậu kiểm bằng điểm hạnh phúc thực tế thì phân hóa rõ: phân tích phương sai một nhân tố cho F từ 107,09 đến 159,18. Bảng theo dõi dịch chuyển của 156 quốc gia cho thấy 142 quốc gia giữ nguyên cụm cả năm năm, 4 quốc gia thăng hạng và 2 quốc gia tụt hạng.

Toàn bộ số liệu trong báo cáo truy vết về `reports/tables/*.csv` và `data/processed/*.csv`. Thuật toán K-Means, phân cấp Ward, DBSCAN và các độ đo Silhouette, Davies–Bouldin, Calinski–Harabasz, ARI đều được cài đặt lại từ đầu bằng NumPy ở mức phép toán cơ bản.

# Mục lục

:::toc
:::

:::pagebreak
:::

# Chương 1: Tổng quan đề tài và cơ sở lý thuyết

## 1.1. Bối cảnh và lý do chọn đề tài

World Happiness Report (WHR) là báo cáo thường niên công bố từ năm 2012, sử dụng dữ liệu khảo sát Gallup World Poll để xếp hạng mức độ hạnh phúc của các quốc gia. Bản 2017 công bố ngày 20/3/2017 xếp hạng 155 quốc gia. Điểm số của mỗi quốc gia lấy từ câu hỏi Cantril Ladder, tức người trả lời tự đánh giá cuộc sống hiện tại trên thang 0 đến 10.

Điểm hạnh phúc tổng hợp là một con số duy nhất nên khi đọc bảng xếp hạng, người xem khó thấy quốc gia yếu ở trục nào. Ví dụ một nước có GDP cao nhưng nhận thức tham nhũng kém vẫn có thể đứng gần một nước có GDP thấp hơn nhưng thể chế tốt. Gom cụm theo sáu yếu tố cơ sở cho phép tách các nhóm quốc gia theo cấu trúc đặc trưng thay vì theo một thứ hạng tổng.

Nhóm chọn bài toán gom cụm vì dữ liệu không có nhãn mục tiêu cho bài toán phân lớp, và các đặc trưng đầu vào đều là thang đo liên tục. Kết quả dùng để mô tả cấu trúc nhóm trong từng năm; nhóm không đặt mục tiêu dự đoán điểm hạnh phúc hay chứng minh quan hệ nhân quả.

## 1.2. Bài toán và câu hỏi nghiên cứu

Cho ma trận đặc trưng X kích thước n×6 của từng năm, với mỗi dòng là một quốc gia và sáu cột là sáu yếu tố cơ sở, bài toán đặt ra là tìm phân hoạch các quốc gia thành các nhóm có đặc trưng gần nhau theo khoảng cách Euclid.

Bốn câu hỏi nghiên cứu:

1. Có thể chia các quốc gia thành bao nhiêu nhóm dựa trên sáu yếu tố cơ sở, và số cụm tối ưu có ổn định qua các năm không?
2. Cách chuẩn hóa dữ liệu (Raw, Min-Max, Z-score) ảnh hưởng thế nào đến kết quả K-Means?
3. Phân cấp Ward và DBSCAN cho kết quả thế nào khi so sánh với K-Means trên cùng dữ liệu?
4. Nhãn cụm có ổn định khi đổi seed khởi tạo, và các cụm hình thành từ sáu yếu tố có phân hóa theo điểm hạnh phúc thực tế hay không?

## 1.3. Nguồn dữ liệu

Dữ liệu là bản tổng hợp World Happiness Report trên Kaggle, gồm năm tệp CSV cho các năm 2015 đến 2019, lưu tại `data/raw/`. Mỗi tệp có schema riêng và đều chứa tên quốc gia, thứ hạng, điểm hạnh phúc, sáu yếu tố cơ sở và một số cột phụ về sai số khảo sát. Chi tiết cấu trúc từng năm được trình bày ở Chương 2.

Tài liệu phương pháp luận của nhóm (thang đo Cantril Ladder, mô hình Dystopia, ý nghĩa sáu biến) được tổng hợp tại `docs/nghien_cuu/whr_nguon_du_lieu.md`.

## 1.4. Thang đo Cantril Ladder

Gallup World Poll đo đánh giá cuộc sống bằng câu hỏi Cantril Ladder: người trả lời hình dung một chiếc thang có bậc từ 0 (cuộc sống tồi tệ nhất có thể) đến 10 (cuộc sống tốt nhất có thể) và chọn bậc cho cuộc sống hiện tại của mình. Điểm của quốc gia là trung bình có trọng số Gallup của các câu trả lời, tính trên mẫu đại diện khoảng 1.000 người trưởng thành mỗi nước.

Vì là thang tự đánh giá, điểm số chịu ảnh hưởng của yếu tố văn hóa và kỳ vọng sống của từng dân tộc. Đây là lý do nhóm không dùng điểm hạnh phúc làm đặc trưng gom cụm, mà chỉ dùng để hậu kiểm sau khi đã phân nhóm.

## 1.5. Mô hình Dystopia và Dystopia Residual

Dystopia là quốc gia giả định được nhóm tác giả WHR dựng từ giá trị thấp nhất thế giới quan sát được ở từng yếu tố trong sáu yếu tố cơ sở. Dystopia làm mốc chuẩn để mọi đóng góp của sáu yếu tố đều mang giá trị dương trong biểu đồ phân rã. Mức sống trung bình của Dystopia được ước lượng khoảng 1,85 trên thang 0–10.

Trong dữ liệu, ba năm 2015–2017 có sẵn cột `Dystopia Residual`; hai năm 2018–2019 không có cột này nên nhóm tính lại bằng hiệu số giữa điểm hạnh phúc và tổng sáu yếu tố. Nhóm đã kiểm chứng đẳng thức happiness_score xấp xỉ tổng sáu yếu tố cộng dystopia_residual trên ba tệp 2015–2017: sai lệch tuyệt đối lớn nhất chỉ là 0,00051 do dữ liệu gốc đã làm tròn.

## 1.6. Sáu biến cơ sở

Sáu cột nằm sau cột điểm số trong tệp WHR là mức đóng góp ước lượng của từng yếu tố, được so với chuẩn Dystopia nên luôn dương. Bảng 1.1 đối chiếu tên cột gốc qua các năm với tên chuẩn hóa dùng trong mã nguồn.

**Bảng 1.1: Sáu yếu tố cơ sở và tên cột tương ứng qua các năm**

| Tên chuẩn trong mã nguồn | Tên cột gốc 2015–2016 | Tên cột gốc 2017 | Tên cột gốc 2018–2019 | Nội dung đo lường |
| --- | --- | --- | --- | --- |
| gdp_per_capita | Economy (GDP per Capita) | Economy..GDP.per.Capita. | GDP per capita | Log GDP bình quân đầu người theo sức mua tương đương |
| social_support | Family | Family | Social support | Có người thân hoặc bạn bè để dựa vào khi gặp khó khăn |
| healthy_life_expectancy | Health (Life Expectancy) | Health..Life.Expectancy. | Healthy life expectancy | Số năm sống khỏe mạnh kỳ vọng từ lúc sinh |
| freedom | Freedom | Freedom | Freedom to make life choices | Mức hài lòng với tự do lựa chọn cuộc sống |
| generosity | Generosity | Generosity | Generosity | Mức quyên góp từ thiện đã trừ phần dự báo bởi GDP |
| corruption_perception | Trust (Government Corruption) | Trust..Government.Corruption. | Perceptions of corruption | Niềm tin vào sự liêm chính của chính phủ và doanh nghiệp |

Riêng `corruption_perception` được mã hóa sao cho giá trị cao tương ứng với ít tham nhũng. Kiểm tra nhanh trên tệp 2019: Phần Lan đạt 0,393 và Đan Mạch đạt 0,410, trong khi Nga chỉ 0,031 và Afghanistan 0,025. Khi viết nhận xét, nhóm luôn diễn giải theo hướng "điểm càng cao thì nhận thức tham nhũng càng thấp".

## 1.7. Quy tắc vàng của đề tài

Quy tắc vàng: không đưa `happiness_score` và `happiness_rank` vào ma trận đặc trưng X. Việc gom cụm chỉ dựa trên sáu yếu tố cơ sở; điểm hạnh phúc dùng độc lập ở bước hậu kiểm.

Có hai căn cứ. Thứ nhất, về mặt đại số, điểm hạnh phúc bằng tổng sáu yếu tố cộng phần dư Dystopia, nên nếu đưa vào X thì cụm sẽ bị chi phối bởi chính biến cần giải thích. Thứ hai, về mặt phương pháp, nếu dùng điểm hạnh phúc để gom cụm thì bước đối chiếu mất tính độc lập và không còn chứng minh được điều gì.

Nhóm kiểm soát quy tắc này bằng ba chốt: danh sách `CORE_FEATURES` trong `src/data/data_loader.py` chỉ có sáu cột; script đối chứng `scripts/verify_scratch_implementations.py` khẳng định X không chứa hai cột bị cấm; và notebook 04 chỉ dùng điểm hạnh phúc sau khi đã gán nhãn cụm.

## 1.8. Đối chiếu 11 bước pipeline với cấu trúc báo cáo

Bảng 1.2 ánh xạ 11 bước của quy trình khai phá dữ liệu theo đề cương vào các chương và sản phẩm cụ thể.

**Bảng 1.2: Ánh xạ 11 bước pipeline vào báo cáo**

| Bước | Nội dung | Chương | Sản phẩm |
| --- | --- | --- | --- |
| 1 | Xác định bài toán và câu hỏi khai thác | Chương 1 | Mục 1.1, 1.2 |
| 2 | Tìm hiểu dữ liệu | Chương 1 và 2 | Mục 1.3, 1.6, 2.1 |
| 3 | Đánh giá chất lượng dữ liệu | Chương 2 | Mục 2.3, 2.5 |
| 4 | Tiền xử lý và chuẩn hóa | Chương 2 | Mục 2.2, 2.4 |
| 5 | Khám phá dữ liệu EDA | Chương 2 | Mục 2.6 đến 2.8 |
| 6 | Biến đổi dữ liệu cho thuật toán | Chương 3 | Mục 3.1, 3.2 |
| 7 | Thực hiện thuật toán và chọn tham số | Chương 3 | Mục 3.3 đến 3.7 |
| 8 | Đánh giá và so sánh cấu hình | Chương 3 và 4 | Mục 3.8, 4.1, 4.2 |
| 9 | Diễn giải tri thức | Chương 4 | Mục 4.3 đến 4.7 |
| 10 | Sản phẩm demo | Chương 5 | Mục 5.1, 5.2 |
| 11 | Kết luận và hướng phát triển | Chương 5 | Mục 5.3 đến 5.6 |

# Chương 2: Thu thập dữ liệu và khám phá EDA

## 2.1. Cấu trúc dữ liệu thô và tình trạng lệch schema

Năm tệp thô có số dòng và số cột khác nhau. Bảng 2.1 ghi lại cỡ mẫu, số cột và các cột sai số khảo sát xuất hiện trong từng tệp.

**Bảng 2.1: Cấu trúc và chất lượng dữ liệu thô theo năm**

| Năm | Số dòng | Số cột | Cột sai số khảo sát | Ghi chú |
| --- | --- | --- | --- | --- |
| 2015 | 158 | 12 | Standard Error | Đủ sáu yếu tố |
| 2016 | 157 | 13 | Lower/Upper Confidence Interval | Đủ sáu yếu tố |
| 2017 | 155 | 12 | Whisker.high, Whisker.low | Đủ sáu yếu tố |
| 2018 | 156 | 9 | Không có | UAE khuyết Perceptions of corruption |
| 2019 | 156 | 9 | Không có | Đủ sáu yếu tố |

Tổng số bản ghi thô là 782. Ba vấn đề chất lượng dữ liệu cần xử lý: lệch tên cột giữa các năm, sự xuất hiện của các cột sai số khảo sát, và một giá trị khuyết duy nhất của UAE năm 2018.

## 2.2. Đồng nhất tên cột

Từ điển `COLUMN_MAPPING` trong `src/data/data_loader.py` ánh xạ toàn bộ tên cột gốc về mười ba tên snake_case thống nhất. Ví dụ `Happiness Rank` và `Happiness.Rank` và `Overall rank` đều về `happiness_rank`; `Economy (GDP per Capita)`, `Economy..GDP.per.Capita.` và `GDP per capita` đều về `gdp_per_capita`; `Family` và `Social support` đều về `social_support`. Hàm `standardize_columns` áp từ điển này cho từng tệp trước khi ghép.

Ba cột sai số khảo sát (`Standard Error`, `Lower/Upper Confidence Interval`, `Whisker.high`, `Whisker.low`) bị loại. Lý do: đây là sai số chọn mẫu và khoảng tin cậy của cuộc khảo sát, không phản ánh mức sống của quốc gia; nếu giữ lại thì khoảng cách Euclid bị nhiễu bởi độ chính xác khảo sát thay vì bởi chất lượng sống.

## 2.3. Xử lý giá trị khuyết của UAE năm 2018

Tệp 2018 có đúng một giá trị khuyết trong toàn bộ năm năm: chỉ số `Perceptions of corruption` của United Arab Emirates. Nhóm không điền giá trị thiếu vì hai lý do. Thứ nhất, điền bằng trung bình sẽ tạo ra một giá trị giả cho một quốc gia, làm sai lệch kết quả gom cụm và không thể giải trình. Thứ hai, không thể bỏ cả cột `corruption_perception` chỉ vì một dòng, vì cột này là một trong sáu trụ cột và ảnh hưởng đến 155 quốc gia còn lại của năm 2018.

Nhóm loại đúng một dòng, đưa bảng phân tích về 781 bản ghi với cỡ mẫu theo năm là 158, 157, 155, 155 và 156. Trong bảng theo dõi dịch chuyển cụm, UAE vẫn xuất hiện nhưng `cluster_2018` để trống, đây là khuyết thiếu có chủ đích và được ghi chú rõ.

## 2.4. Chuẩn hóa tên quốc gia và bổ sung mã ISO-3

Tên quốc gia bị ghi khác nhau giữa các năm nên nếu giữ nguyên thì bảng theo dõi dịch chuyển sẽ tách một quốc gia thành nhiều dòng. Từ điển `COUNTRY_NAME_FIXES` xử lý các trường hợp: `Macedonia` về `North Macedonia`, `Swaziland` về `Eswatini`, `Taiwan Province of China` về `Taiwan`, `Hong Kong S.A.R., China` về `Hong Kong`, `Trinidad & Tobago` về `Trinidad and Tobago`.

Mã ISO-3 được sinh bằng hàm `country_to_iso3` kèm bảng ghi đè cho các trường hợp đặc biệt (Kosovo về XKX, North Cyprus về CYP, Somaliland về SOM). Kết quả kiểm tra trên bảng interim: 781 trên 781 dòng có mã ISO-3 hợp lệ theo mẫu ba chữ cái in hoa; bảng có 164 quốc gia duy nhất xuyên năm năm và 162 mã ISO-3 phân biệt. Mã ISO-3 là điều kiện cần để vẽ bản đồ Choropleth trong ứng dụng demo ở Chương 5.

## 2.5. Bảng dữ liệu trung gian

Sau tiền xử lý, nhóm xuất `data/interim/happiness_merged.csv` gồm 13 cột: `country`, `region`, `happiness_rank`, `happiness_score`, sáu yếu tố cơ sở, `dystopia_residual`, `year` và `iso_alpha`. Cột `region` chỉ có ở 2015–2016 nên được bù từ dữ liệu hai năm đầu và bảng dự phòng; cột này giữ lại để tham khảo, không dùng trong gom cụm.

## 2.6. Phân tích hình dạng phân phối

Hình 2.1 vẽ histogram kèm đường cong KDE cho sáu đặc trưng, kèm độ lệch skewness trên tiêu đề từng subplot.

:::figure
file: feature_distributions.png
caption: Hình 2.1: Phân bố sáu yếu tố cơ sở trên toàn bộ 781 bản ghi (Histogram và KDE)
width: 6.1
:::

Hai đặc trưng lệch phải rõ: `generosity` có skewness 1,043 và `corruption_perception` có skewness 1,521. Bốn đặc trưng còn lại lệch nhẹ về bên trái: GDP bình quân đầu người −0,344; hỗ trợ xã hội −0,688; tuổi thọ khỏe mạnh −0,500; tự do −0,524. Phân phối lệch phải của `corruption_perception` cho thấy đa số quốc gia có điểm thấp, chỉ một nhóm nhỏ đạt điểm cao.

## 2.7. Tương quan Pearson

Hình 2.2 là ma trận tương quan Pearson giữa sáu đặc trưng và điểm hạnh phúc.

:::figure
file: correlation_heatmap.png
caption: Hình 2.2: Ma trận hệ số tương quan Pearson giữa sáu yếu tố cơ sở và điểm hạnh phúc
width: 5.6
:::

Cặp GDP bình quân đầu người và tuổi thọ khỏe mạnh đạt r = 0,79, vượt ngưỡng 0,7 nên cần lưu ý hiện tượng đa cộng tuyến khi diễn giải. Điểm hạnh phúc tương quan mạnh với GDP bình quân đầu người (r = 0,79) và tuổi thọ khỏe mạnh (r = 0,74), trong khi `generosity` gần như không tương quan (r = −0,01). Kết quả này củng cố nhận định rằng sáu yếu tố mô tả được phần lớn chênh lệch mức sống, nhưng không phải mọi yếu tố đều đóng góp như nhau.

## 2.8. Nhận diện ngoại lai

Hình 2.3 là biểu đồ hộp cho sáu đặc trưng sau khi đưa về cùng thang Min-Max để hiển thị chung một trục.

:::figure
file: boxplots_outliers.png
caption: Hình 2.3: Biểu đồ hộp nhận diện ngoại lai theo quy tắc 1,5 lần IQR
width: 6.0
:::

Số điểm ngoại lai theo quy tắc 1,5 lần IQR tập trung ở các nước thu nhập cao và một số nước châu Phi. Nhóm không loại các điểm này vì đó là quan sát thật, phản ánh chênh lệch thực tế giữa các quốc gia; vai trò của bước nhận diện ngoại lai là để chọn cách chuẩn hóa phù hợp ở Chương 3.

## 2.9. Kết luận chương 2

Bảng phân tích cuối cùng có 781 bản ghi sạch, sáu yếu tố không còn giá trị khuyết, tên cột và tên quốc gia đã đồng nhất, mã ISO-3 hợp lệ toàn bộ. Dữ liệu lệch thang đo giữa các trụ cột và có ngoại lai, nên bước chuẩn hóa ở Chương 3 là bắt buộc trước khi gom cụm.

# Chương 3: Phương pháp luận và thử nghiệm mô hình

## 3.1. Ma trận đặc trưng

Mỗi quan sát là một quốc gia trong một năm. Ma trận đầu vào gồm sáu cột tương ứng sáu yếu tố cơ sở. Điểm hạnh phúc và thứ hạng hạnh phúc không nằm trong ma trận này, tuân theo quy tắc vàng ở Mục 1.7. Số dòng ma trận theo năm là 158, 157, 155, 155 và 156.

## 3.2. So sánh ba phương án chuẩn hóa

Nhóm giữ lại cả ba phương án chuẩn hóa cho K-Means để có căn cứ thực nghiệm thay vì chọn theo cảm tính. Z-score đưa từng biến về phân phối có trung bình 0 và độ lệch chuẩn 1 theo công thức z = (x − μ) / σ. Min-Max co giãn về đoạn [0, 1] theo công thức x' = (x − min) / (max − min). Phương án Raw giữ nguyên thang đo.

Min-Max rất nhạy với ngoại lai: một quốc gia có GDP hoặc tuổi thọ đột biến sẽ nén các quốc gia còn lại vào một khoảng hẹp và làm mất độ phân giải giữa các nước trung bình. Phương án Raw để biến có thang đo lớn chi phối khoảng cách Euclid. Z-score giữ nguyên hình dáng phân phối và mức phân tán tương đối nên mỗi trụ cột đóng góp công bằng hơn.

Bảng 3.1 tổng hợp chỉ số trung bình của năm cấu hình lõi qua năm năm.

**Bảng 3.1: So sánh năm cấu hình gom cụm lõi (trung bình 2015–2019)**

| Thuật toán | Chuẩn hóa | Silhouette | Davies–Bouldin | Calinski–Harabasz | Inertia | Thời gian (giây) |
| --- | --- | --- | --- | --- | --- | --- |
| DBSCAN | Z-score | 0,0514 | 0,7991 | 14,6058 | 511,6867 | 0,1027 |
| K-Means | Min-Max | 0,3288 | 1,0896 | 88,6959 | 19,6404 | 0,4390 |
| K-Means | Raw | 0,3234 | 1,0586 | 148,8569 | 18,5140 | 0,5518 |
| K-Means | Z-score | 0,3180 | 1,1432 | 79,6817 | 459,7275 | 0,3697 |
| Ward | Z-score | 0,2868 | 1,1558 | 66,7203 | 501,3057 | 1,1842 |

Silhouette của Min-Max (0,3288) nhỉnh hơn Raw (0,3234) và Z-score (0,3180), nhưng chênh lệch chỉ khoảng 0,01. Cột Inertia không so sánh trực tiếp được giữa các phương án chuẩn hóa vì phụ thuộc thang đo. Nhóm chọn Z-score làm cấu hình chính vì lý do diễn giải: Z-score đưa sáu trụ cột về cùng đơn vị độ lệch chuẩn, giữ được cấu trúc tương quan giữa các biến, và ổn định qua các lần khởi tạo với ARI trung bình 0,9904. Kết quả của cả ba phương án vẫn được báo cáo đầy đủ để bảo đảm tính khách quan của thực nghiệm.

## 3.3. Thuật toán K-Means cài đặt từ đầu

K-Means lặp hai bước: gán mỗi điểm vào tâm gần nhất và cập nhật tâm bằng trung bình các điểm trong cụm. Hàm mục tiêu là tổng bình phương khoảng cách trong cụm:

WCSS = Σ (i = 1..n) || x_i − μ_c(i) ||²

Nhóm cài đặt khởi tạo K-Means++ thay vì chọn ngẫu nhiên thuần túy: tâm đầu tiên chọn ngẫu nhiên, các tâm sau chọn với xác suất tỉ lệ thuận với khoảng cách bình phương đến tâm gần nhất. Cách này giảm khả năng rơi vào cực tiểu địa phương. Với mỗi cấu hình, nhóm chạy `n_init = 10` lần với các seed khác nhau và giữ lần có inertia nhỏ nhất; số vòng lặp tối đa là 100. Class `SimpleKMeans` lưu lại `inertia_history` và `n_iter_` để truy vết quá trình hội tụ.

## 3.4. Phân cấp Ward cài đặt từ đầu

Phân cấp Ward gộp cụm theo tiêu chí tối thiểu hóa gia tăng phương sai nội cụm. Với hai cụm A và B, độ tăng phương sai khi gộp tính qua khoảng cách tâm cụm:

Δ(A, B) = (n_A · n_B) / (n_A + n_B) · || μ_A − μ_B ||²

Sau khi gộp, khoảng cách giữa cụm mới và cụm còn lại được cập nhật theo công thức Lance–Williams:

d(A ∪ B, C) = ((n_A + n_C) / (n_A + n_B + n_C)) · d(A, C) + ((n_B + n_C) / (n_A + n_B + n_C)) · d(B, C) − (n_C / (n_A + n_B + n_C)) · d(A, B)

Nhóm lưu `merge_history` gồm chỉ số hai cụm con, khoảng cách gộp và số điểm của cụm mới. Ward là thuật toán tất định với dữ liệu và tham số cố định, nên không cần chạy lặp nhiều seed.

## 3.5. DBSCAN cài đặt từ đầu

DBSCAN phân loại điểm theo mật độ với hai tham số `eps` là bán kính và `min_samples` là số điểm tối thiểu. Điểm lõi có ít nhất `min_samples` điểm (kể cả nó) trong bán kính `eps`; điểm biên nằm trong bán kính của một điểm lõi; điểm còn lại gán nhãn nhiễu −1. Nhóm cài đặt `SimpleDBSCAN` bằng cách duyệt vùng lân cận và lan truyền nhãn.

Nhóm quét toàn bộ lưới `eps` thuộc {0,6; 0,8; 1,0; 1,2} và `min_samples` thuộc {3; 4; 5}, tổng 60 cấu hình cho năm năm. Bảng 3.2 ghi số tổ hợp tạo được ít nhất hai cụm, tức đủ điều kiện tính chỉ số nội bộ.

**Bảng 3.2: Số tổ hợp tham số DBSCAN đủ điều kiện tính chỉ số, theo năm**

| Năm | Tổ hợp đủ cụm | Tổ hợp không đủ cụm | Tổng |
| --- | --- | --- | --- |
| 2015 | 9 | 3 | 12 |
| 2016 | 7 | 5 | 12 |
| 2017 | 8 | 4 | 12 |
| 2018 | 10 | 2 | 12 |
| 2019 | 11 | 1 | 12 |

Với cấu hình tốt nhất `eps = 1,2` và `min_samples = 4`, DBSCAN chỉ tạo 1 đến 2 cụm và đánh dấu 24 đến 35 điểm nhiễu; Silhouette đạt 0,2976 năm 2015 nhưng bằng 0 ở 2016 và 2017, âm ở 2019. Nguyên nhân là sáu đặc trưng sau chuẩn hóa có mật độ khá đồng đều, không tồn tại vùng dày đặc trưng để tách cụm. Nhóm giữ DBSCAN như phương án đối chứng để chứng minh dữ liệu quốc gia phù hợp hơn với phương pháp dựa trên khoảng cách.

## 3.6. Các độ đo đánh giá

**Silhouette** của điểm i so sánh khoảng cách trung bình đến các điểm cùng cụm a(i) với khoảng cách trung bình nhỏ nhất đến cụm lân cận b(i):

s(i) = (b(i) − a(i)) / max(a(i), b(i)), giá trị nằm trong đoạn [−1; 1]

Hệ số Silhouette của cả tập là trung bình của s(i); giá trị gần 1 nghĩa là cụm tách biệt, gần 0 là nằm sát ranh giới, âm là có khả năng gán sai cụm.

**Davies–Bouldin** là trung bình tỉ số giữa độ phân tán nội cụm và khoảng cách giữa hai tâm cụm, giá trị nhỏ hơn thường tốt hơn. **Calinski–Harabasz** là tỉ số giữa phương sai giữa cụm và phương sai trong cụm, giá trị lớn hơn thường tốt hơn. **Adjusted Rand Index (ARI)** đo mức trùng khớp nhãn giữa hai lần chạy sau khi loại yếu tố ngẫu nhiên; ARI bằng 1 là trùng khớp hoàn toàn.

Cả bốn độ đo đều được cài đặt lại từ đầu bằng vòng lặp và công thức cơ bản, không gọi hàm dựng sẵn.

## 3.7. Khảo sát số cụm tối ưu

Nhóm khảo sát k từ 2 đến 9 cho từng năm bằng Elbow trên Inertia kết hợp với Silhouette; bảng khảo sát gồm 40 dòng. Hình 3.1 là biểu đồ khuỷu tay và Silhouette của K-Means.
:::figure
file: elbow_silhouette_kmeans.png
caption: Hình 3.1: Đường khuỷu tay Inertia và hệ số Silhouette theo số cụm k
width: 6.1
:::

Bảng 3.3 ghi số cụm tối ưu và Silhouette cực đại theo từng năm.

**Bảng 3.3: Số cụm tối ưu k* và Silhouette cực đại theo năm (K-Means, Z-score)**

| Năm | k* | Silhouette cực đại | Inertia tại k* |
| --- | --- | --- | --- |
| 2015 | 3 | 0,2931 | 481,9405 |
| 2016 | 3 | 0,3037 | 472,8497 |
| 2017 | 3 | 0,3133 | 457,0866 |
| 2018 | 3 | 0,3365 | 446,1818 |
| 2019 | 3 | 0,3436 | 440,5788 |

Kết quả là k* = 3 ở cả năm năm, Silhouette cực đại tăng từ 0,2931 năm 2015 lên 0,3436 năm 2019. Vì k* đồng thuận, nhóm giữ thêm cấu hình k = 3 làm đối chứng xuyên năm để phục vụ so sánh giữa các năm. Hình 3.2 là biểu đồ khảo sát số cụm riêng cho năm 2019.

:::figure
file: k_sensitivity_2019.png
caption: Hình 3.2: Khảo sát số cụm k từ 2 đến 9 cho năm 2019 (Inertia và Silhouette)
width: 5.4
:::

## 3.8. Kiểm tra độ ổn định

Nhóm chạy K-Means mười lần với mười seed khác nhau cho mỗi năm và tính ARI cho từng cặp trong 45 cặp. Bảng 3.4 là kết quả ARI của các cấu hình dùng Z-score.

:::table
file: stability_ari.csv
caption: Bảng 3.4: Chỉ số ARI của các cấu hình dùng Z-score (mười seed, năm năm)
where: scaling == 'standard'
columns: year, algorithm, k, n_runs, mean_pairwise_ari, min_pairwise_ari
round: 4
:::

ARI trung bình của K-Means/Z-score đạt 0,9763 đến 1,0000 với mức thấp nhất từng cặp là 0,9763; điều này cho thấy phân hoạch gần như không phụ thuộc seed. Ward và DBSCAN là thuật toán tất định nên ARI bằng 1,0000 giữa các lần chạy, nhóm ghi nhận kèm giải thích thay vì chạy lặp hình thức.

## 3.9. Quy trình thực nghiệm

Mỗi năm là một thí nghiệm độc lập. Quy trình gồm: nạp bảng interim; chọn sáu đặc trưng của năm; chuẩn hóa theo cấu hình; chạy thuật toán; tính Silhouette, Davies–Bouldin, Calinski–Harabasz; và hậu kiểm bằng điểm hạnh phúc. Tổng cộng năm cấu hình lõi nhân năm năm là 25 dòng kết quả, cộng với 60 dòng quét DBSCAN và 25 dòng độ ổn định ARI. Toàn bộ kết quả lưu tại `reports/tables/`.

# Chương 4: Kết quả thực nghiệm và diễn giải tri thức

## 4.1. Chỉ số đánh giá của K-Means qua các năm

Bảng 4.1 là chỉ số của K-Means với Z-score theo từng năm.

:::table
file: model_comparison_metrics_by_year.csv
caption: Bảng 4.1: Chỉ số đánh giá của K-Means/Z-score theo năm
where: algorithm == 'K-Means' and scaling == 'standard'
columns: year, silhouette, davies_bouldin, calinski_harabasz, inertia, runtime_seconds
round: 4
:::

Silhouette tăng đều từ 0,2931 lên 0,3436 qua năm năm, Davies–Bouldin giảm từ 1,2166 xuống 1,0703 và Calinski–Harabasz tăng từ 74,95 lên 86,02. Xu hướng này cho thấy cấu trúc ba cụm ngày càng tách biệt hơn ở các năm cuối giai đoạn.

## 4.2. Chỉ số đánh giá của Ward và so sánh với K-Means

Bảng 4.2 là chỉ số của phân cấp Ward với Z-score theo từng năm.

:::table
file: model_comparison_metrics_by_year.csv
caption: Bảng 4.2: Chỉ số đánh giá của Ward/Z-score theo năm
where: algorithm == 'Ward' and scaling == 'standard'
columns: year, silhouette, davies_bouldin, calinski_harabasz, inertia, runtime_seconds
round: 4
:::

Ward có Silhouette thấp hơn K-Means ở cả năm năm (0,2541 đến 0,3104 so với 0,2931 đến 0,3436) và thời gian chạy lớn hơn (0,77 đến 1,42 giây so với 0,08 đến 0,39 giây). Cả hai thuật toán đều đồng thuận chọn ba cụm ở mọi năm; K-Means được chọn làm cấu hình kể chuyện chính vì chỉ số tách biệt tốt hơn và chi phí tính toán thấp hơn.

## 4.3. Chân dung ba cụm

Bảng 4.3 tổng hợp số lượng quốc gia và điểm hạnh phúc trung bình của từng cụm theo năm; số liệu lấy từ `reports/tables/cluster_trends.csv`.

:::table
file: cluster_trends.csv
caption: Bảng 4.3: Số lượng quốc gia và điểm hạnh phúc trung bình theo cụm qua năm năm
columns: year, cluster_id, country_count, mean_happiness_score
round: 4
:::

Nhóm đặt tên cụm theo chân dung sáu đặc trưng, thứ tự ổn định là 0 là nhóm hạnh phúc cao, 1 là trung bình và 2 là thấp:

1. Cụm 1 — Phát triển toàn diện: vượt trội đồng thời ở GDP, tuổi thọ và hỗ trợ xã hội, nhận thức tham nhũng cao nhất. Số quốc gia theo năm là 29, 27, 29, 24 và 28; điểm hạnh phúc trung bình từ 6,728 đến 6,846.
2. Cụm 2 — Đang phát triển phụ thuộc kinh tế: các chỉ số ở mức trung bình khá và chiếm số lượng đông nhất. Số quốc gia theo năm là 79, 84, 80, 85 và 82; điểm hạnh phúc trung bình từ 5,570 đến 5,608.
3. Cụm 3 — Dễ bị tổn thương và Khó khăn: điểm rất thấp ở hầu hết trụ cột kinh tế, y tế và tự do. Số quốc gia theo năm là 50, 46, 46, 46 và 46; điểm hạnh phúc trung bình từ 4,096 đến 4,263.

Hình 4.1 là chân dung radar trung bình năm năm của ba cụm.

:::figure
file: radar_chart_clusters.png
caption: Hình 4.1: Chân dung radar sáu yếu tố của ba cụm quốc gia (trung bình 2015–2019)
width: 5.6
:::

Cần lưu ý rằng nhãn 0, 1, 2 chỉ là mã định danh. Ở lớp nhãn gốc trước khi chuẩn hóa thứ tự, cụm điểm cao nhất của K-Means lần lượt mang nhãn 2, 0, 2, 1 và 0 từ 2015 đến 2019. Nhóm chuẩn hóa lại theo điểm hạnh phúc trung bình để tên cụm nhất quán giữa các năm, và trong báo cáo luôn diễn giải bằng giá trị trung bình sáu đặc trưng thay vì bằng số nhãn.

## 4.4. Hậu kiểm độc lập bằng điểm hạnh phúc

Điểm hạnh phúc không tham gia gom cụm. Sau khi gán nhãn, nhóm kiểm tra mức phân hóa bằng phân tích phương sai một nhân tố với nhân tố là cụm (ba mức) và biến phụ thuộc là điểm hạnh phúc. Công thức F là tỉ số giữa phương sai giữa cụm và phương sai trong cụm:

F = (SS_between / (k − 1)) / (SS_within / (n − k))

Bảng 4.4 là kết quả tính cho nhãn cụm K-Means của từng năm.

**Bảng 4.4: Phân tích phương sai một nhân tố cho điểm hạnh phúc theo cụm K-Means**

| Năm | Số quan sát | Bậc tự do | F | Chênh lệch cụm cao nhất và thấp nhất |
| --- | --- | --- | --- | --- |
| 2015 | 158 | (2; 155) | 144,89 | 2,638 |
| 2016 | 157 | (2; 154) | 148,24 | 2,715 |
| 2017 | 155 | (2; 152) | 159,18 | 2,658 |
| 2018 | 155 | (2; 152) | 127,15 | 2,634 |
| 2019 | 156 | (2; 153) | 107,09 | 2,465 |

Giá trị F đều trên 100, lớn hơn nhiều mức cần thiết để bác bỏ giả thuyết không ở mức ý nghĩa 1 phần trăm. Chênh lệch giữa điểm trung bình cụm cao nhất và thấp nhất nằm trong khoảng 2,465 đến 2,943 điểm trên thang 0–10 tùy cấu hình và năm. Hình 4.2 là biểu đồ hộp phân bố điểm hạnh phúc theo cụm qua năm năm.

:::figure
file: validation_happiness_score_by_cluster.png
caption: Hình 4.2: Hậu kiểm độc lập, phân bố điểm hạnh phúc thực tế giữa ba cụm qua năm năm
width: 6.1
:::

Kết quả này là căn cứ để nhóm kết luận các cụm hình thành từ sáu yếu tố khách quan vẫn phản ánh đúng mức sống thực tế, dù không dùng điểm hạnh phúc trong quá trình gom cụm.

## 4.5. Cấu hình đối chứng k = 3

Vì k* = 3 ở cả năm năm, cấu hình đối chứng k = 3 trùng với cấu hình tối ưu. Bảng 4.5 tổng hợp chỉ số của hai thuật toán theo năm.

:::table
file: contrast_k3_by_year.csv
caption: Bảng 4.5: Chỉ số của cấu hình đối chứng k = 3 cho hai thuật toán qua năm năm
columns: year, algorithm, k_star, ari_k3_vs_k_star, silhouette, davies_bouldin, calinski_harabasz
round: 4
:::

ARI giữa cấu hình k* và k = 3 bằng 1,0000 ở cả 10 trường hợp (hai thuật toán nhân năm năm). Đây là kiểm tra tính nhất quán, không phải so sánh hai giá trị k khác nhau.

## 4.6. Ghép cụm liên năm

Nhãn cụm không so sánh trực tiếp được giữa các năm vì mỗi năm gom cụm riêng. Nhóm ghép cụm của hai năm liền kề bằng thuật toán tham lam: tính khoảng cách Euclid giữa mọi cặp tâm cụm, sắp xếp tăng dần, nếu khoảng cách chênh nhau dưới 10^-6 thì xét thêm chênh lệch điểm hạnh phúc trung bình; sau đó ghép lần lượt các cặp chưa dùng. Hàm xử lý nằm tại `match_clusters_greedy` trong `src/models/clustering.py`. Bảng 4.6 là kết quả ghép cụm liên năm.

:::table
file: cross_year_matching.csv
caption: Bảng 4.6: Kết quả ghép cụm liên năm theo khoảng cách tâm cụm
columns: base_year, target_year, base_cluster_raw, target_cluster_raw, centroid_euclidean_distance, happiness_score_diff
round: 4
:::

Khoảng cách tâm cụm của 12 cặp được ghép nằm trong khoảng 0,0571 đến 0,4196; chênh lệch điểm hạnh phúc giữa hai cụm được ghép tối đa 0,0921. Khoảng cách nhỏ cho thấy cấu trúc cụm giữa hai năm liền kề thay đổi ít.

## 4.7. Dịch chuyển cụm của 156 quốc gia

Bảng theo dõi dịch chuyển (`data/processed/country_cluster_shift.csv`) ghi nhãn cụm của 156 quốc gia qua năm năm. Bảng 4.7 là phân bố trạng thái dịch chuyển.

**Bảng 4.7: Phân bố trạng thái dịch chuyển cụm của 156 quốc gia (2015–2019)**

| Trạng thái | Số quốc gia | Tỷ lệ | Ví dụ |
| --- | --- | --- | --- |
| Ổn định tuyệt đối | 142 | 91,0% | Việt Nam giữ cụm trung bình cả năm năm |
| Biến động trung gian | 8 | 5,1% | Bahrain, Iran, Israel, Thái Lan |
| Cải thiện nhóm | 4 | 2,6% | Botswana, Georgia, Indonesia, Myanmar |
| Suy giảm nhóm | 2 | 1,3% | Kuwait, Uruguay |

Bảng dịch chuyển có 17 ô khuyết ở các cột cụm, nguyên nhân là một số quốc gia không được khảo sát ở mọi năm (Gambia vắng từ 2015 đến 2018, Eswatini vắng 2016 đến 2018) cộng với UAE năm 2018 bị loại có chủ đích. Nhóm đã đối chiếu chéo với bảng interim và xác nhận toàn bộ 17 ô khuyết đều ứng với quốc gia không có dữ liệu năm tương ứng.

Phân tích định lượng nguyên nhân cho sáu quốc gia dịch chuyển, xét chênh lệch giữa năm 2015 và 2019:

- Botswana chuyển lên nhóm trung bình từ năm 2016, hai chỉ số tăng mạnh nhất là tuổi thọ khỏe mạnh (+0,490) và GDP bình quân đầu người (+0,047); điểm hạnh phúc trong giai đoạn lại giảm 0,844, cho thấy dịch chuyển cụm theo sáu yếu tố không đồng nghĩa điểm hạnh phúc tăng.
- Georgia chuyển lên nhóm trung bình từ năm 2019 nhờ hỗ trợ xã hội (+0,280) và GDP bình quân đầu người (+0,144); nhận thức tham nhũng lại giảm 0,219.
- Indonesia chuyển lên nhóm cao từ năm 2019 nhờ hỗ trợ xã hội (+0,116) và GDP bình quân đầu người (+0,103).
- Myanmar chuyển lên nhóm cao từ năm 2018 nhờ hỗ trợ xã hội (+0,472) và GDP bình quân đầu người (+0,439).
- Kuwait tụt xuống nhóm trung bình, chỉ số giảm mạnh nhất là nhận thức tham nhũng (−0,159).
- Uruguay tụt xuống nhóm trung bình, chỉ số giảm mạnh nhất là mức độ hào phóng (−0,105) và nhận thức tham nhũng (−0,096).

Hình 4.3 là xu hướng số lượng quốc gia trong từng cụm qua năm năm.

:::figure
file: cluster_count_trend.png
caption: Hình 4.3: Xu hướng số lượng quốc gia trong từng cụm giai đoạn 2015–2019
width: 6.0
:::

## 4.8. Phân bố cụm trên không gian PCA 2D

Hình 4.4 là lưới biểu đồ phân bố ba cụm trên mặt phẳng hai thành phần chính, tính riêng cho từng năm bằng SimplePCA.

:::figure
file: pca_clusters_grid.png
caption: Hình 4.4: Lưới phân bố ba cụm trên không gian 2D PCA giai đoạn 2015–2019
width: 6.2
:::

Ở mọi năm, ba cụm chiếm các vùng tương đối tách biệt trên mặt phẳng PCA; trật tự phân tách theo trục thứ nhất giữ nguyên qua các năm, phù hợp với kết quả Silhouette tăng dần về cuối giai đoạn. Hình 4.5 là chân dung radar của ba cụm riêng cho năm 2019.

:::figure
file: radar_chart_2019.png
caption: Hình 4.5: Chân dung radar sáu yếu tố của ba cụm quốc gia năm 2019
width: 5.4
:::

## 4.9. Kết luận chương 4

Trong phạm vi sáu đặc trưng và dữ liệu 2015–2019, ba cụm là cấu hình tối ưu đồng thuận; K-Means/Z-score cho Silhouette 0,293–0,344 và ổn định cao qua seed; Ward xác nhận cùng số cụm; DBSCAN không phù hợp với dữ liệu trong vùng tham số đã quét. Bước hậu kiểm bằng điểm hạnh phúc cho F từ 107,09 đến 159,18, chứng minh ba cụm phân hóa theo mức sống thực tế.

# Chương 5: Ứng dụng demo, kết luận và hướng phát triển

## 5.1. Kiến trúc ứng dụng demo Streamlit

Ứng dụng `app/app.py` đọc trực tiếp dữ liệu đã sinh ở các mốc M1 đến M3 và gồm bốn tab tương tác. Mọi hàm nạp dữ liệu được bọc `@st.cache_data` để không phải đọc lại đĩa khi người dùng đổi lựa chọn.

1. Tab Tổng quan cụm và Radar: chọn năm từ 2015 đến 2019 và thuật toán K-Means hoặc Ward; hiển thị thẻ chỉ số Silhouette, Davies–Bouldin, Calinski–Harabasz và Radar Chart so sánh sáu đặc trưng trung bình của ba cụm.
2. Tab Bản đồ thế giới: vẽ bản đồ Choropleth bằng Plotly, tô màu theo cụm và dùng mã ISO-3 trong cột `iso3`; khi rê chuột hiển thị tên quốc gia, mã ISO-3, nhóm cụm và điểm hạnh phúc.
3. Tab Tra cứu quốc gia: chọn một trong 156 quốc gia, xem nhóm cụm năm 2019, trạng thái và chiều dịch chuyển, bảng lịch sử phân cụm và biểu đồ biến thiên sáu chỉ số cùng điểm hạnh phúc.
4. Tab Thử nghiệm gán nhãn: kéo sáu thanh trượt theo dải giá trị năm 2019, hệ thống chuẩn hóa z-score theo mean và std đã lưu trong `models/kmeans_2019.json`, tính khoảng cách Euclid tới ba tâm cụm và gán vào cụm gần nhất, kèm bảng khoảng cách và Radar so sánh.

Hình 5.1 minh họa phân bố ba cụm của năm 2019, đây là dữ liệu mà Tab Bản đồ và Tab Tra cứu hiển thị.

:::figure
file: pca_clusters_2019.png
caption: Hình 5.1: Phân bố ba cụm quốc gia năm 2019 trên không gian 2D PCA
width: 5.8
:::

## 5.2. Kiểm thử ứng dụng

Ứng dụng được kiểm thử tự động bằng `streamlit.testing.v1.AppTest` trong `scripts/audit_m4_app_and_slides.py`. Kết quả: chạy toàn bộ app không phát sinh ngoại lệ; hiển thị đúng bốn tab, sáu thanh trượt, mười hai thẻ chỉ số và bốn biểu đồ Plotly. Khi đổi thuật toán từ K-Means sang Ward, các thẻ chỉ số thay đổi từ 0,3436 / 1,0703 / 86,0 thành 0,3104 / 1,0019 / 68,2, xác nhận ứng dụng không hardcode số liệu.

Bộ slide thuyết trình gồm 15 slide, lưu tại `reports/presentation/slides.md`.

## 5.3. Đóng góp chính của đồ án

1. Xây dựng pipeline dữ liệu năm năm chạy lại được từ đầu, tự động sinh bảng trung gian 781 bản ghi với mã ISO-3 hợp lệ toàn bộ.
2. Cài đặt lại từ đầu K-Means, phân cấp Ward, DBSCAN, SimplePCA và bốn độ đo đánh giá bằng NumPy ở mức phép toán cơ bản, có script đối chứng với thư viện chuẩn.
3. Thực nghiệm năm cấu hình nhân năm năm, khảo sát số cụm, quét tham số DBSCAN và kiểm tra độ ổn định qua mười seed; toàn bộ kết quả lưu thành CSV.
4. Xây dựng thuật toán ghép cụm liên năm và bảng dịch chuyển của 156 quốc gia qua năm năm.
5. Xây dựng ứng dụng demo bốn tab và bộ slide 15 slide, kèm công cụ biên dịch báo cáo Word từ Markdown.

## 5.4. Hạn chế

Về dữ liệu: bộ dữ liệu chỉ có sáu trụ cột của Gallup World Poll, thiếu các chỉ số văn hóa và thể chế chuyên sâu nên phần dư Dystopia còn lớn ở một số quốc gia (từ 0,33 đến 3,84 tùy năm). Cỡ mẫu mỗi năm khác nhau (158, 157, 155, 155, 156) nên mọi so sánh theo thời gian đều phải ghi rõ cỡ mẫu. Bảng dịch chuyển có 17 ô khuyết do quốc gia vắng mặt ở một số năm.

Về phương pháp: gom cụm không có nhãn chuẩn để đối chiếu nên kết luận dựa trên các độ đo nội tại và hậu kiểm bằng điểm hạnh phúc. Tên cụm mang tính diễn giải của nhóm. Silhouette trong khoảng 0,293–0,344 là mức trung bình, phản ánh việc các quốc gia nằm dọc một phổ liên tục chứ không tách rời hoàn toàn. DBSCAN nhạy với tham số và không phù hợp với dữ liệu trong vùng đã quét.

Về phạm vi: kết luận chỉ đúng cho sáu đặc trưng, dữ liệu 2015–2019 và dải tham số của thí nghiệm; báo cáo không chứng minh quan hệ nhân quả giữa sáu yếu tố và mức hạnh phúc.

## 5.5. Hướng phát triển

1. Mở rộng chuỗi thời gian sang 2020–2024 để kiểm tra cấu trúc cụm có giữ nguyên sau đại dịch hay không.
2. Bổ sung đặc trưng ngoài sáu trụ cột như bất bình đẳng Gini, chi tiêu y tế và chỉ số chất lượng quản trị để giảm phần dư.
3. So sánh thêm phân cụm mờ (Fuzzy C-Means) cho các quốc gia đang chuyển tiếp giữa các nhóm.
4. Phân tích độ nhạy theo trọng số trụ cột khi ưu tiên thể chế hoặc kinh tế.
5. Đưa demo lên dashboard công khai và bổ sung chức năng xuất báo cáo PDF cho từng quốc gia.

## 5.6. Kết luận

Trên dữ liệu 2015–2019 và sáu yếu tố cơ sở, ba cụm là cấu hình tối ưu đồng thuận ở cả năm năm. K-Means với Z-score cho Silhouette 0,293–0,344, Davies–Bouldin 1,00–1,07 và Calinski–Harabasz 74,95–86,02; kết quả ổn định qua mười seed với ARI thấp nhất 0,9763. Ba cụm tương ứng với các nhóm phát triển toàn diện, đang phát triển và khó khăn, phân hóa rõ rệt khi hậu kiểm bằng điểm hạnh phúc với F từ 107,09 đến 159,18. Bảng dịch chuyển cho thấy 142 trong 156 quốc gia giữ nguyên cụm cả năm năm.

# Tài liệu tham khảo

1. Helliwell, J. F., Layard, R., Sachs, J. D. (chủ biên), World Happiness Report các bản 2015–2019, Mạng lưới Giải pháp Phát triển Bền vững Liên Hợp Quốc.
2. Bộ dữ liệu World Happiness Report trên Kaggle và mô tả kèm trong repo: `data/Aboutdataset.md`.
3. Gallup World Poll, tài liệu phương pháp khảo sát và thang đo Cantril Ladder.
4. Ward, J. H., Hierarchical Grouping to Optimize an Objective Function, Journal of the American Statistical Association, 1963.
5. Ester, M., Kriegel, H. P., Sander, J., Xu, X., A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise, KDD, 1996.
6. Rousseeuw, P. J., Silhouettes: a Graphical Aid to the Interpretation and Validation of Cluster Analysis, Journal of Computational and Applied Mathematics, 1987.
7. Hubert, L., Arabie, P., Comparing Partitions, Journal of Classification, 1985.
8. Tài liệu hướng dẫn đề tài nhóm Khai thác dữ liệu, Mục 1.2 và Đề tài 16.

# Phụ lục A: Bảng khảo sát số cụm năm 2019

:::table
file: k_sensitivity_by_year.csv
caption: Bảng A.1: Khảo sát số cụm k từ 2 đến 9 cho năm 2019
where: year == 2019
columns: k, inertia, silhouette, year
round: 4
:::

# Phụ lục B: Kết quả quét tham số DBSCAN năm 2019

:::table
file: dbscan_sweep.csv
caption: Bảng B.1: Kết quả quét tham số DBSCAN cho năm 2019
where: year == 2019
columns: eps, min_samples, silhouette, davies_bouldin, calinski_harabasz, n_clusters, n_noise
round: 4
:::

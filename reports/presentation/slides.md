# Bộ slide thuyết trình — Đề tài 16 — Nhóm 12

**Học phần:** Khai thác dữ liệu (Data Mining)  
**Đề tài 16:** Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report 2015–2019)  
**Quy cách video:** Tổng thời lượng tối đa 12 phút, chia làm 3 phần tuần tự theo nguyên tắc *"Ai làm phần nào thuyết trình phần đó"*.

> Mọi số liệu trong bộ slide này truy vết trực tiếp về `reports/tables/*.csv`, `data/processed/*.csv` và `data/interim/happiness_merged.csv`.

---

# PHẦN 1: TỔNG QUAN ĐỀ TÀI & TIỀN XỬ LÝ DỮ LIỆU
**Người trình bày:** Hà Mạnh Trường (MSSV: 2045240326 — Nhóm trưởng)  
**Thời lượng dự kiến:** ~3 phút 30 giây (Slide 1 – Slide 4)

---

## Slide 1: Trang bìa

- Học phần: Khai thác dữ liệu — Ngành Khoa học dữ liệu
- Đề tài 16: Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc (World Happiness Report 2015–2019)
- Nhóm 12:
  - Hà Mạnh Trường — MSSV 2045240326 — Nhóm trưởng (Phần 1: Tổng quan & Tiền xử lý dữ liệu)
  - Huỳnh Tâm Trí — MSSV 2045240315 (Phần 2: Thuật toán from scratch & Thực nghiệm)
  - Ngô Quang Trung — MSSV 2045240325 (Phần 3: EDA, Diễn giải tri thức, Demo & Kết luận)
- Giảng viên hướng dẫn: Giảng viên học phần Khai thác dữ liệu
- Sản phẩm nộp: Toàn bộ mã nguồn, 4 Notebook phân tích, Demo Streamlit 4 tab, Báo cáo Word 5 chương, Video báo cáo dưới 12 phút
- Dữ liệu nghiên cứu: 5 năm khảo sát Gallup World Poll (2015–2019), 781 bản ghi quốc gia – năm sau làm sạch

> 🎙️ **Lời dẫn thuyết trình gợi ý (Hà Mạnh Trường - ~45 giây):**  
> *"Kính chào Thầy và Hội đồng chấm đồ án. Em là Hà Mạnh Trường, nhóm trưởng Nhóm 12. Hôm nay nhóm em xin phép báo cáo Đề tài 16: Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc dựa trên dữ liệu World Happiness Report giai đoạn 2015–2019. Video báo cáo hôm nay sẽ kéo dài dưới 12 phút và được chia làm 3 phần rành mạch: Em sẽ phụ trách Phần 1 về bối cảnh đề tài và quy trình tiền xử lý dữ liệu; bạn Huỳnh Tâm Trí sẽ trình bày Phần 2 về thuật toán tự cài đặt và thực nghiệm tham số; cuối cùng bạn Ngô Quang Trung sẽ trình bày Phần 3 về diễn giải tri thức, theo dõi dịch chuyển cụm và demo ứng dụng tương tác."*

---

## Slide 2: Nội dung báo cáo

- Nội dung Báo cáo gồm 5 phần chính bám sát tiến trình phân tích khoa học dữ liệu:
- **Phần 1: Tổng quan đề tài & Cơ sở lý thuyết**
  - Bối cảnh Báo cáo Hạnh phúc Thế giới (WHR), hạn chế của điểm đơn lẻ, 6 trụ cột cơ sở.
- **Phần 2: Dữ liệu & Quy trình tiền xử lý**
  - Khảo sát dữ liệu 2015–2019, xử lý khuyết thiếu (loại UAE 2018), làm sạch 781 bản ghi và gắn mã địa lý ISO-3.
- **Phần 3: Phương pháp luận & Cài đặt thuật toán from scratch**
  - Cơ sở chuẩn hóa Z-score, thuật toán tự cài đặt K-Means++, Hierarchical Ward Lance–Williams và DBSCAN.
- **Phần 4: Thực nghiệm gom cụm, Tối ưu hóa & Đánh giá mô hình**
  - Thẩm định số cụm tối ưu k* = 3 đồng thuận 5 năm, so sánh đối chứng mô hình và kiểm định độ ổn định ARI.
- **Phần 5: Diễn giải tri thức, Ứng dụng tương tác & Kết luận**
  - Chân dung 3 cụm, hậu kiểm ANOVA, dịch chuyển 142/156 quốc gia, demo Streamlit 4 tab, hạn chế và mở rộng.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Hà Mạnh Trường - ~35 giây):**  
> *"Kính thưa Thầy và Hội đồng chấm đồ án, nội dung bài báo cáo của nhóm em gồm 5 phần chính: Phần 1 là tổng quan bối cảnh đề tài và cơ sở lý thuyết; Phần 2 là quy trình thu thập và tiền xử lý dữ liệu 5 năm; Phần 3 là phương pháp luận và cài đặt các thuật toán from scratch; Phần 4 là kết quả thực nghiệm tối ưu hóa và đánh giá đối chứng mô hình; và Phần 5 là diễn giải tri thức kinh tế - xã hội, theo dõi dịch chuyển cụm, demo ứng dụng tương tác cùng kết luận đề tài."*

---

## Slide 3: Lý do chọn đề tài và ý nghĩa của Báo cáo Hạnh phúc Thế giới

- World Happiness Report (WHR) công bố thường niên từ năm 2012 dưới sự chủ trì của Mạng lưới Giải pháp Phát triển Bền vững Liên Hợp Quốc (SDSN).
- Điểm hạnh phúc (Happiness Score) thu thập từ khảo sát Gallup World Poll, đo bằng thang đo Cantril Ladder từ 0 đến 10.
- Vấn đề cốt lõi: Điểm tổng hợp là một giá trị duy nhất, dễ che lấp các thế mạnh hoặc điểm nghẽn đặc thù của từng quốc gia trên 6 trụ cột phát triển.
- Sự phù hợp với Khai thác dữ liệu: Bài toán phân nhóm không giám sát (Unsupervised Clustering) hoàn hảo để khám phá cấu trúc tự nhiên mà không dựa trên nhãn định kiến.
- Ý nghĩa thực tiễn: Giúp các nhà hoạch định chính sách nhận diện đúng nhóm quốc gia cần ưu tiên cải thiện thể chế, y tế hay hỗ trợ an sinh.
- Ý nghĩa học thuật: Hiện thực hóa trọn vẹn quy trình khai thác dữ liệu chuẩn mực với tư duy lập trình from scratch độc lập thư viện.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Hà Mạnh Trường - ~50 giây):**  
> *"Về lý do chọn đề tài: Báo cáo Hạnh phúc Thế giới là nguồn dữ liệu chuẩn mực toàn cầu. Tuy nhiên, nếu chỉ nhìn vào một con số điểm hạnh phúc duy nhất, chúng ta không thể biết một quốc gia đạt điểm đó nhờ kinh tế vượt trội hay nhờ an sinh xã hội vững chắc. Do đó, việc áp dụng gom cụm không giám sát dựa trên 6 yếu tố cơ sở sẽ giúp khám phá ra các nhóm quốc gia có cùng chân dung phát triển tự nhiên. Đây là cơ sở thực chứng giúp định hình chính sách hỗ trợ phát triển bền vững."*

---

## Slide 4: Quy trình tiền xử lý dữ liệu 5 năm

- Thu thập dữ liệu: 5 tệp CSV độc lập tương ứng với các năm từ 2015 đến 2019 tải từ Kaggle với 782 mẫu thô ban đầu.
- Xử lý dị biệt cấu trúc: Đồng nhất tên 6 đặc trưng về chuẩn snake_case thống nhất qua từ điển `COLUMN_MAPPING`.
- Loại bỏ nhiễu: Loại bỏ các cột sai số thống kê mẫu (`Standard Error`, `Whisker.high/low`) không mang giá trị kinh tế.
- Xử lý giá trị khuyết thiếu: Loại bỏ đúng 1 bản ghi của UAE năm 2018 do khuyết thiếu hoàn toàn chỉ số tham nhũng.
- Đồng bộ danh pháp & ISO-3: Chuẩn hóa các trường hợp lệch tên (Macedonia, Swaziland và vùng lãnh thổ) và bổ sung mã ISO-3 chuẩn hóa cho toàn bộ các dòng.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Hà Mạnh Trường - ~40 giây):**  
> *"Ở khâu tiền xử lý dữ liệu, thách thức lớn nhất là cấu trúc cột và cách đặt tên quốc gia qua 5 năm hoàn toàn không đồng nhất. Nhóm đã thực hiện quy trình 4 bước chặt chẽ: Đầu tiên là đồng nhất schema 6 đặc trưng bằng từ điển chuyển đổi; thứ hai là loại bỏ triệt để các cột sai số thống kê mẫu; thứ ba là loại bỏ đúng 1 dòng của UAE năm 2018 do khuyết thiếu hoàn toàn chỉ số tham nhũng; và cuối cùng là chuẩn hóa danh pháp các quốc gia biến động cùng mã địa lý ISO-3 để phục vụ liên kết dữ liệu."*

---

## Slide 5: Kết quả tiền xử lý và tập dữ liệu chuẩn hóa

- Quy mô bộ dữ liệu sạch: Giữ lại chính xác **781 bản ghi** sạch 100%, tỷ lệ hoàn thiện dữ liệu đạt 100% không còn bất kỳ giá trị NaN nào.
- Độ bao phủ địa lý: Bao gồm **164 quốc gia** duy nhất trên toàn cầu với **162 mã ISO-3** phân biệt.
- Tệp trung gian xuất bản: Đóng gói toàn bộ vào tệp chuẩn hóa `data/interim/happiness_merged.csv` với 13 thuộc tính sạch.
- Minh chứng thực tế từ Notebook: Ảnh chụp trực tiếp lệnh `df.head()` từ Notebook 01 cho thấy cấu trúc dữ liệu năm 2019 sắc nét, sẵn sàng cho các bước mô hình hóa.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Hà Mạnh Trường - ~35 giây):**  
> *"Kết quả sau tiền xử lý là một tập dữ liệu hoàn hảo gồm 781 bản ghi của 164 quốc gia với 162 mã ISO-3 phân biệt, sạch 100% không còn giá trị khuyết thiếu. Toàn bộ được đóng gói vào tệp dữ liệu trung gian happiness_merged.csv. Trên màn hình là ảnh chụp thực tế từ Notebook 01 hiển thị 5 dòng đầu của tập dữ liệu năm 2019. Tiếp theo, em xin nhường phần thuyết trình cho bạn Huỳnh Tâm Trí với nội dung thuật toán và thực nghiệm."*

---

# PHẦN 2: THUẬT TOÁN FROM SCRATCH & THỰC NGHIỆM GOM CỤM
**Người trình bày:** Huỳnh Tâm Trí (MSSV: 2045240315)  
**Thời lượng dự kiến:** ~4 phút 00 giây (Slide 6 – Slide 10)

---

## Slide 6: Khám phá dữ liệu (EDA) & Cơ sở lựa chọn phương pháp

- Phân bố đặc trưng: `Generosity` lệch phải (skewness 1,04) và `Perceptions of corruption` lệch phải rất mạnh (skewness 1,52).
- Tương quan mạnh: GDP bình quân đầu người và Tuổi thọ khỏe mạnh có tương quan tuyến tính rất cao (r = 0,79).
- Phát hiện ngoại lai: Quy tắc 1,5 × IQR phát hiện nhiều điểm ngoại lai ở các nước Bắc Âu giàu có và nhóm nước châu Phi khó khăn.
- Lựa chọn phương pháp chuẩn hóa: So sánh thực nghiệm giữa Z-score (StandardScaler) và Min-Max Scaler:
  - Min-Max nén phần lớn quốc gia vào dải hẹp do bị ảnh hưởng bởi giá trị ngoại lai biên.
  - Z-score chuẩn hóa phương sai về 1, bảo đảm 6 đặc trưng đóng góp bình đẳng vào khoảng cách Euclidean.
- Giảm chiều dữ liệu: Tự cài đặt `SimplePCA` bằng phân rã phổ ma trận hiệp phương sai để trực quan hóa không gian 2D/3D.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Huỳnh Tâm Trí - ~50 giây):**  
> *"Xin chào Thầy, em là Huỳnh Tâm Trí. Tiếp nối phần của bạn Trường, khi phân tích phân bố và tương quan, nhóm nhận thấy các chỉ số như tham nhũng và lòng hảo tâm bị lệch phải rất mạnh, đồng thời xuất hiện nhiều giá trị ngoại lai. Khi so sánh giữa Min-Max và Z-score, Min-Max làm các quốc gia trung bình bị nén chặt lại do tác động của các nước ngoại lai cực đại. Do đó, nhóm quyết định chọn Z-score làm phương pháp chuẩn hóa chính để giữ nguyên cấu trúc phân tán tự nhiên và tính toán khoảng cách Euclidean công bằng giữa 6 yếu tố."*

---

## Slide 7: Cài đặt thuật toán gom cụm từ đầu (From Scratch)

- `SimpleKMeans`: Khởi tạo tâm cụm thông minh K-Means++ (tính xác suất tỉ lệ khoảng cách bình phương $D(x)^2$), tối ưu hóa hàm mục tiêu Inertia/WCSS, tham số `n_init = 10` để tránh cực tiểu địa phương.
- `SimpleHierarchicalClustering`: Thuật toán phân cấp tích tụ theo liên kết Ward thật, cập nhật khoảng cách liên tục qua công thức Lance–Williams với bộ nhớ đệm tâm cụm, lưu lịch sử gộp `merge_history`.
- `SimpleDBSCAN`: Phân cụm dựa trên mật độ, duyệt vùng lân cận bán kính `eps` và `min_samples`, phát hiện và gán nhãn −1 cho các điểm nhiễu.
- Tự cài đặt các độ đo đánh giá: Tự viết 100% công thức tính hệ số Silhouette $s(i)$, chỉ số Davies–Bouldin (DB), Calinski–Harabasz (CH) và Adjusted Rand Index (ARI).
- Nguyên tắc đối chứng: Thư viện `scikit-learn` và `scipy` chỉ được dùng trong `scripts/verify_scratch_implementations.py` để assert đối chứng thuật toán tự viết với dung sai $10^{-4}$.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Huỳnh Tâm Trí - ~55 giây):**  
> *"Điểm cốt lõi về kỹ thuật trong đồ án của nhóm là toàn bộ thuật toán gom cụm và độ đo đánh giá đều được tự lập trình from scratch bằng Python và NumPy cơ bản, tuyệt đối không gọi hàm thư viện có sẵn trong pipeline. Nhóm đã tự cài K-Means++ với khởi tạo xác suất, phân cấp tích tụ liên kết Ward chuẩn công thức Lance-Williams, và DBSCAN quét mật độ. Toàn bộ mã nguồn tự viết đã được kiểm chứng bằng script đối chứng độc lập, khớp chính xác từng con số với scikit-learn và scipy."*

---

## Slide 8: Thẩm định số cụm tối ưu k*

- Phạm vi khảo sát: Quét $k \in [2, 9]$ độc lập trên từng năm (2015–2019) bằng phương pháp Elbow kết hợp hệ số Silhouette.
- Bộ dữ liệu khảo sát: Tổng hợp 40 dòng thực nghiệm tại `reports/tables/k_sensitivity_by_year.csv`.
- Kết quả đồng thuận: Cả 5 năm khảo sát đều chỉ ra số cụm tối ưu đồng thuận là $k^* = 3$.
- Đỉnh Silhouette theo năm: Đều đạt cực đại tại $k = 3$:
  - Năm 2015: đạt 0,2931
  - Năm 2016: đạt 0,3037
  - Năm 2017: đạt 0,3133
  - Năm 2018: đạt 0,3365
  - Năm 2019: đạt 0,3436
- Cơ sở thực tiễn: Cấu hình 3 cụm phản ánh hoàn hảo cấu trúc 3 tầng phát triển kinh tế – xã hội của thế giới: Nhóm Phát triển toàn diện, Nhóm Đang phát triển và Nhóm Khó khăn.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Huỳnh Tâm Trí - ~45 giây):**  
> *"Để xác định số cụm tối ưu, nhóm đã tiến hành khảo sát k từ 2 đến 9 trên cả 5 năm độc lập. Kết quả trên bảng độ nhạy cho thấy cả 5 năm đều đồng thuận tuyệt đối tại k* = 3 với điểm Silhouette đạt đỉnh cao nhất, dao động từ 0,293 đến 0,344. Cấu hình 3 cụm này vừa có tính ổn định toán học cao nhất, vừa mang ý nghĩa kinh tế - xã hội rõ rệt khi phân hóa thế giới thành 3 nhóm phát triển tương ứng."*

---

## Slide 9: So sánh đối chứng các thuật toán gom cụm

- K-Means / Z-score: Cho kết quả toàn diện nhất: Silhouette 0,293 – 0,344; Davies–Bouldin 1,07 – 1,22; Calinski–Harabasz 74,9 – 86,0.
- Hierarchical Ward / Z-score: Đạt Silhouette 0,254 – 0,310; Davies–Bouldin 1,00 – 1,26; Calinski–Harabasz 59,9 – 71,0. Ward là thuật toán tất định nên độ ổn định ARI luôn bằng 1,0.
- Khảo sát DBSCAN: Quét lưới 60 cấu hình tham số: `eps` $\in \{0,6; 0,8; 1,0; 1,2\}$ và `min_samples` $\in \{3, 4, 5\}$.
  - Kết quả DBSCAN: Với `eps = 1,2` và `min_samples = 4`, DBSCAN chỉ gom được 1 đến 2 cụm và loại bỏ tới 24 đến 35 quốc gia thành điểm nhiễu.
  - Lý do: Không gian 6 chiều sau chuẩn hóa có mật độ chuyển tiếp liên tục, không tồn tại ranh giới mật độ rỗng để DBSCAN phân tách.
- Kết luận thuật toán: Lựa chọn **K-Means làm mô hình chính** và **Hierarchical Ward làm mô hình đối chứng**.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Huỳnh Tâm Trí - ~50 giây):**  
> *"Khi đặt các thuật toán lên bàn cân so sánh, K-Means trên dữ liệu Z-score thể hiện ưu thế vượt trội về độ tách biệt cụm với điểm Silhouette và Calinski-Harabasz cao nhất. Thuật toán phân cấp Ward cho kết quả tương đồng và mang tính tất định. Ngược lại, khi quét lưới 60 cấu hình DBSCAN, thuật toán này hoạt động kém hiệu quả do dữ liệu 6 chiều có mật độ biến thiên liên tục, khiến DBSCAN coi gần một phần tư số quốc gia là nhiễu. Do đó, nhóm chốt K-Means làm thuật toán phân nhóm chính cho đề tài."*

---

## Slide 10: Đánh giá độ ổn định mô hình (Stability Evaluation)

- Thử nghiệm độ ổn định ngẫu nhiên: Chạy K-Means trên 10 giá trị hạt giống ngẫu nhiên (random seeds khác nhau) trên từng năm.
- Đo lường bằng Adjusted Rand Index (ARI):
  - Điểm ARI trung bình qua 10 seed đạt từ 0,979 đến 1,000.
  - Điểm ARI thấp nhất ghi nhận là 0,9763 (năm 2017), cho thấy thuật toán hội tụ cực kỳ ổn định, gần như không bị ảnh hưởng bởi điểm khởi tạo.
- Khả năng tái lập (Reproducibility): Toàn bộ pipeline thực nghiệm chạy lại trên máy sạch với thời gian chạy dưới 1 giây cho K-Means và 1,2 giây cho Ward.
- Bàn giao kết quả: Bàn giao ma trận nhãn cụm 5 năm sạch cho bạn Ngô Quang Trung tiếp tục bước Diễn giải tri thức và Xây dựng demo.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Huỳnh Tâm Trí - ~40 giây):**  
> *"Để kiểm tra tính bền vững của kết quả, nhóm đã kiểm tra độ ổn định của K-Means qua 10 lần khởi tạo hạt giống khác nhau. Chỉ số Adjusted Rand Index đạt xấp xỉ tuyệt đối từ 0,979 đến 1,000, chứng minh thuật toán hội tụ rất ổn định và không phụ thuộc vào may rủi khởi tạo tâm ban đầu. Sau đây, em xin mời bạn Ngô Quang Trung tiếp tục trình bày Phần 3 về diễn giải tri thức kinh tế - xã hội và demo ứng dụng."*

---

# PHẦN 3: PHÂN TÍCH EDA, DIỄN GIẢI TRI THỨC, DỊCH CHUYỂN, DEMO TƯƠNG TÁC & KẾT LUẬN
**Người trình bày:** Ngô Quang Trung (MSSV: 2045240325)  
**Thời lượng dự kiến:** ~4 phút 30 giây (Slide 11 – Slide 16)

---

## Slide 11: Xây dựng chân dung 3 cụm kinh tế — xã hội

- **Cụm 1 — Nhóm Phát triển toàn diện (24–29 quốc gia):**
  - Đặc trưng: Vượt trội toàn diện về GDP, Tuổi thọ khỏe mạnh, Hỗ trợ xã hội và Chỉ số trong sạch thể chế (ít tham nhũng).
  - Đại diện tiêu biểu: Phần Lan, Đan Mạch, Na Uy, Thụy Sĩ, New Zealand, Canada.
- **Cụm 2 — Nhóm Đang phát triển phụ thuộc kinh tế (79–85 quốc gia):**
  - Đặc trưng: Chiếm đa số các quốc gia; chỉ số kinh tế và tuổi thọ ở mức trung bình khá nhưng điểm thể chế và tự do còn hạn chế.
  - Đại diện tiêu biểu: Việt Nam, Thái Lan, Malaysia, Brazil, Mexico, Nga, Trung Quốc.
- **Cụm 3 — Nhóm Dễ bị tổn thương và Khó khăn (46–50 quốc gia):**
  - Đặc trưng: Điểm rất thấp ở hầu hết các trụ cột cơ sở, đặc biệt là an sinh xã hội và y tế.
  - Đại diện tiêu biểu: Afghanistan, Nam Sudan, Yemen, Trung Phi.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Ngô Quang Trung - ~45 giây):**  
> *"Kính chào Thầy, em là Ngô Quang Trung. Bước sang phần diễn giải tri thức, từ kết quả gom cụm 6 đặc trưng, nhóm đã phác họa rõ nét chân dung của 3 cụm: Cụm 1 là nhóm các nước phát triển toàn diện, đứng đầu thế giới về kinh tế, y tế và sự minh bạch thể chế như các nước Bắc Âu. Cụm 2 chiếm số đông nhất gồm các nước đang phát triển như Việt Nam và các nước Đông Nam Á, có tăng trưởng kinh tế khá nhưng an sinh và thể chế cần tiếp tục hoàn thiện. Cụm 3 là nhóm các quốc gia khó khăn và xung đột, cần sự ưu tiên trợ giúp khẩn cấp về y tế và an sinh xã hội."*

---

## Slide 12: Hậu kiểm độc lập với Điểm Hạnh phúc thực tế (Validation)

- **Quy tắc vàng của đề tài:** Tuyệt đối không đưa `Happiness Score` vào ma trận gom cụm $X$; chỉ dùng điểm này ở bước hậu kiểm độc lập.
- **Kết quả hậu kiểm phân hóa sâu sắc:**
  - Cụm 1 (Phát triển): Điểm hạnh phúc trung bình thực tế đạt 6,73 – 6,85 điểm.
  - Cụm 2 (Đang phát triển): Điểm hạnh phúc trung bình thực tế đạt 5,57 – 5,61 điểm.
  - Cụm 3 (Khó khăn): Điểm hạnh phúc trung bình thực tế đạt 4,10 – 4,26 điểm.
  - Khoảng cách chênh lệch giữa Cụm 1 và Cụm 3 lên tới 2,46 – 2,72 điểm trên thang đo 10 điểm.
- **Kiểm định thống kê ANOVA một nhân tố:** Giá trị kiểm định $F$ cực lớn, dao động từ $107,09$ đến $159,18$ qua cả 5 năm ($p$-value $< 10^{-15}$).
- **Ý nghĩa:** Chứng minh các cụm gom được thuần túy từ 6 yếu tố khách quan phản ánh hoàn toàn chính xác mức độ hạnh phúc cảm nhận thực tế của người dân.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Ngô Quang Trung - ~45 giây):**  
> *"Tuân thủ nghiêm ngặt quy tắc vàng của đề tài, nhóm không đưa điểm hạnh phúc vào lúc phân cụm mà chỉ dùng để hậu kiểm độc lập. Kết quả kiểm định ANOVA một nhân tố cho giá trị F từ 107 đến 159, cực kỳ có ý nghĩa thống kê. Điểm hạnh phúc giữa 3 cụm phân hóa rành mạch và giữ nguyên thứ tự qua cả 5 năm, với mức chênh lệch giữa cụm cao nhất và thấp nhất lên tới hơn 2,5 điểm. Điều này khẳng định 6 yếu tố cơ sở phản ánh rất sát mức độ hạnh phúc thực tế của con người."*

---

## Slide 13: Theo dõi Dịch chuyển cụm của 156 quốc gia qua 5 năm

- Thuật toán ghép cụm liên năm: Xây dựng hàm `match_clusters_greedy` ghép cụm dựa trên khoảng cách tâm Euclid nhỏ nhất giữa các năm liên tiếp (khoảng cách cực kỳ nhỏ: 0,057 – 0,420).
- Bảng tổng hợp dịch chuyển: Theo dõi 156 quốc gia qua 5 năm tại `data/processed/country_cluster_shift.csv`.
- Phân bố trạng thái:
  - **142 quốc gia Ổn định tuyệt đối (chiếm 91,0%):** Giữ nguyên nhóm cụm suốt giai đoạn 2015–2019.
  - **8 quốc gia Biến động trung gian (chiếm 5,1%):** Dao động nhẹ quanh ranh giới giữa Cụm 2 và Cụm 3.
  - **4 quốc gia Thăng hạng bền vững (+):** Botswana, Georgia, Indonesia, Myanmar dịch chuyển từ nhóm khó khăn lên nhóm trung bình.
  - **2 quốc gia Tụt hạng bền vững (−):** Kuwait và Uruguay tụt nhẹ từ nhóm phát triển xuống nhóm trung bình.
- Nhận xét: Cấu trúc hạnh phúc thế giới có tính trơ và bền vững cao; các dịch chuyển tích cực đều bắt nguồn từ sự cải thiện rõ nét về an sinh xã hội và y tế.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Ngô Quang Trung - ~50 giây):**  
> *"Điểm mới trong đồ án của nhóm là thuật toán ghép cụm liên năm để theo dõi sự dịch chuyển của 156 quốc gia qua nửa thập kỷ. Kết quả chỉ ra rằng 91% số quốc gia ổn định tuyệt đối trong nhóm của mình. Đáng chú ý, có 4 quốc gia ghi nhận sự thăng hạng bền vững gồm Indonesia, Myanmar, Georgia và Botswana nhờ những bước tiến rõ rệt về an sinh xã hội và tuổi thọ khỏe mạnh. Ngược lại có 2 quốc gia bị suy giảm nhẹ do biến động về thể chế và tham nhũng."*

---

## Slide 14: Trực quan hóa tương tác — Ứng dụng Streamlit 4 Tab

- Khởi chạy nhanh: `streamlit run app/app.py`, nạp trực tiếp kết quả từ các tệp dữ liệu sạch.
- **Tab 1 — Phân bố & Radar Chart:** Trực quan hóa hình mạng nhện so sánh tương quan 6 yếu tố theo từng năm và từng thuật toán; hiển thị thẻ chỉ số đánh giá Silhouette, DB, CH.
- **Tab 2 — Bản đồ Hạnh phúc Thế giới:** Bản đồ tương tác Choropleth tô màu theo mã ISO-3, rê chuột xem chi tiết nhóm cụm và điểm số từng nước.
- **Tab 3 — Tra cứu lịch sử quốc gia:** Tra cứu chi tiết từng quốc gia trong số 156 nước, theo dõi lịch sử phân cụm 5 năm và đồ thị đường biến thiên của từng chỉ số.
- **Tab 4 — Thử nghiệm gán cụm cho quốc gia mới:** Cho phép người dùng tùy chỉnh 6 thanh trượt chỉ số, hệ thống tự động chuẩn hóa Z-score và gán nhãn cụm theo khoảng cách tâm thời gian thực.
- Tối ưu hiệu năng: Sử dụng `@st.cache_data`, tốc độ phản hồi dưới 0,1 giây.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Ngô Quang Trung - ~50 giây):**  
> *"Để biến các tri thức khai phá thành công cụ trực quan hữu ích, nhóm đã xây dựng ứng dụng web tương tác Streamlit với 4 tab chức năng. Người dùng có thể tùy biến xem biểu đồ radar đa chiều, tra cứu bản đồ địa lý thế giới theo chuẩn ISO-3, tra cứu chi tiết tiến trình phát triển của từng quốc gia như Việt Nam, và đặc biệt là tab mô phỏng gán nhãn cho một quốc gia giả định bằng cách kéo thanh trượt 6 chỉ số để hệ thống tính toán khoảng cách tâm theo thời gian thực."*

---

## Slide 15: Đóng góp chính, Kết luận và Hạn chế

- **Đóng góp chính của đề tài:**
  - Pipeline nghiên cứu hoàn chỉnh, chạy lại được 100% từ dữ liệu thô trên môi trường sạch.
  - Thuật toán gom cụm (K-Means++, Ward, DBSCAN) và các độ đo tự cài đặt from scratch chuẩn xác.
  - Khám phá và chứng minh số cụm tối ưu $k^* = 3$ đồng thuận tuyệt đối trong 5 năm liên tiếp.
  - Xây dựng ma trận dịch chuyển cụm 156 quốc gia và ứng dụng tương tác hoàn chỉnh.
- **Hạn chế của nghiên cứu:**
  - Bộ dữ liệu WHR giới hạn ở 6 trụ cột cơ bản, chưa bao quát các yếu tố văn hóa bản địa, biến đổi khí hậu hay bất bình đẳng thu nhập nội bộ.
  - Giả định khoảng cách Euclidean trong K-Means xem các trục trực giao, chưa mô hình hóa phi tuyến sâu giữa các đặc trưng có tương quan cao.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Ngô Quang Trung - ~45 giây):**  
> *"Tóm lại, đề tài đã hoàn thành xuất sắc các mục tiêu đề ra với một pipeline hoàn chỉnh, thuật toán tự lập trình chuẩn xác và những phát hiện thực tế có giá trị về sự phân tầng hạnh phúc thế giới. Tuy vậy, nghiên cứu vẫn còn hạn chế do bộ dữ liệu chưa có các chỉ số về văn hóa và chênh lệch giàu nghèo nội bộ, điều mà nhóm mong muốn tiếp tục hoàn thiện trong tương lai."*

---

## Slide 16: Hướng phát triển và Nghiên cứu mở rộng

- **Mở rộng chuỗi dữ liệu (2020–2024):** Kéo dài chuỗi thời gian sang giai đoạn hậu đại dịch COVID-19 để đánh giá sự phục hồi và mức độ bền vững của 3 cụm hạnh phúc.
- **Bổ sung chỉ số kinh tế - xã hội vi mô:** Tích hợp thêm hệ số bất bình đẳng thu nhập Gini và chi tiêu an sinh xã hội từ Ngân hàng Thế giới (World Bank).
- **Thử nghiệm mô hình phân cụm nâng cao:** Áp dụng phân cụm mờ (Fuzzy C-Means), mô hình hỗn hợp Gauss (GMM) và phân cụm chuỗi thời gian (Time-series Clustering) với khoảng cách DTW.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Ngô Quang Trung - ~35 giây):**  
> *"Trong giai đoạn tiếp theo, nhóm định hướng mở rộng nghiên cứu theo 3 hướng trọng tâm: Thứ nhất là cập nhật chuỗi dữ liệu sang giai đoạn 2020–2024 để đo lường biến động của đại dịch COVID-19 và suy thoái kinh tế lên cấu trúc cụm hạnh phúc; thứ hai là bổ sung thêm các chỉ số vi mô như hệ số bất bình đẳng Gini và chi tiêu an sinh xã hội từ World Bank; và thứ ba là thử nghiệm các mô hình phân cụm nâng cao như Fuzzy C-Means và Time-series Clustering để phân tích sâu hơn các quốc gia chuyển tiếp."*

---

## Slide 17: Lời cảm ơn và Phiên vấn đáp (Q&A)

- **Lời tri ân sâu sắc:** Nhóm 12 xin chân thành cảm ơn Thầy hướng dẫn đã tận tình chỉ dẫn và định hướng khoa học cho nhóm trong suốt học phần Khai thác dữ liệu.
- **Tương tác phản biện:** Cả 3 thành viên Nhóm 12 xin sẵn sàng lắng nghe mọi câu hỏi, nhận xét và giải đáp các nội dung phản biện từ Hội đồng chấm thi!
- **Đầy đủ minh chứng:** Toàn bộ mã nguồn From-scratch, dữ liệu chuẩn hóa 781 dòng, báo cáo 5 chương và ứng dụng demo Streamlit 4 tab đều đã được đóng gói hoàn thiện.

> 🎙️ **Lời dẫn thuyết trình gợi ý (Ngô Quang Trung - ~25 giây):**  
> *"Đến đây, phần báo cáo của Nhóm 12 xin phép được khép lại. Chúng em xin chân thành cảm ơn Thầy và Quý Hội đồng đã dành thời gian theo dõi bài thuyết trình của nhóm. Bây giờ cả 3 thành viên chúng em xin sẵn sàng lắng nghe các câu hỏi, góp ý quý báu và trả lời phản biện từ Thầy ạ. Em xin trân trọng cảm ơn!"*

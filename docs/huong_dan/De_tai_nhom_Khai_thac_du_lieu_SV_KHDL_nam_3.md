# THỰC HÀNH KHAI THÁC DỮ LIỆU
## DANH SÁCH ĐỀ TÀI BÁO CÁO NHÓM
*Dành cho sinh viên năm 3 - ngành Khoa học dữ liệu*

| Mục | Nội dung |
| :--- | :--- |
| **Hình thức** | Đồ án nhóm - 03 sinh viên/nhóm |
| **Nội dung trọng tâm** | Tiền xử lý dữ liệu; khai thác tập phổ biến và luật kết hợp; gom cụm |
| **Sản phẩm** | Báo cáo Word + mã nguồn + dữ liệu xử lý + sản phẩm demo + báo cáo tại lớp |
| **Thang điểm** | 10 điểm: Báo cáo Word 6,0 điểm; báo cáo và demo tại lớp 4,0 điểm |

---

## 1. YÊU CẦU CHUNG CHO CÁC ĐỀ TÀI

Mục tiêu của phần báo cáo đề tài là giúp sinh viên thực hiện trọn vẹn một pipeline khai thác dữ liệu trên dữ liệu thực tế, từ hiểu bài toán và dữ liệu cho đến tiền xử lý, khai thác mẫu/gom cụm, đánh giá kết quả, diễn giải tri thức và xây dựng sản phẩm có thể trình diễn. Đề tài không được chỉ dừng ở trực quan hóa dữ liệu hoặc mô tả thống kê.

### 1.1. Tổ chức nhóm và phân công công việc

- Mỗi nhóm gồm đúng **03 sinh viên**. Trừ trường hợp nhóm cuối không đủ thành viên. Nhóm phải có bảng phân công công việc cụ thể, thể hiện phần việc chính, phần việc hỗ trợ và tỷ lệ đóng góp dự kiến của từng thành viên.
- Mỗi thành viên phải hiểu toàn bộ pipeline của nhóm, không chỉ phần việc cá nhân. Khi báo cáo, giảng viên có thể hỏi bất kỳ thành viên nào về dữ liệu, thuật toán, tham số, kết quả hoặc mã nguồn.
- Nhóm thực hiện đúng đề tài và đúng bộ dữ liệu được giao. Việc đổi đề tài hoặc đổi bộ dữ liệu chỉ được thực hiện khi có sự đồng ý của giảng viên.
- Mã nguồn phải có khả năng chạy lại. Khuyến khích quản lý mã nguồn bằng Git/GitHub hoặc thư mục dùng chung có lịch sử phiên bản; không chấm cao cho sản phẩm chỉ có ảnh chụp kết quả mà không thể tái hiện.
- Các nhóm có thể tham khảo tài liệu, notebook Kaggle và công cụ AI, nhưng phải tự triển khai, hiểu mã nguồn và trích dẫn nguồn tham khảo. Sao chép nguyên notebook hoặc không giải thích được phần cài đặt sẽ bị trừ điểm.

**Mẫu bảng phân công bắt buộc trong báo cáo:**

| Thành viên | Công việc chính | Công việc hỗ trợ | Tỷ lệ đóng góp (%) |
| :--- | :--- | :--- | :--- |
| | | | |
| | | | |
| | | | |

---

### 1.2. Pipeline bắt buộc của một đồ án khai thác dữ liệu

1. **Xác định bài toán và câu hỏi khai thác dữ liệu:** Nhóm phải nêu rõ cần phát hiện mẫu nào, phân nhóm đối tượng nào và kết quả sẽ hỗ trợ quyết định gì.
2. **Tìm hiểu dữ liệu:** Mô tả nguồn Kaggle, kích thước, ý nghĩa các thuộc tính, kiểu dữ liệu, đơn vị đo và các bảng cần ghép nếu dữ liệu gồm nhiều tệp.
3. **Đánh giá chất lượng dữ liệu:** Kiểm tra thiếu dữ liệu, trùng lặp, giá trị không hợp lệ, ngoại lệ, phân phối lệch và các trường hợp cần làm sạch.
4. **Tiền xử lý:** Xử lý thiếu/trùng/ngoại lệ phù hợp; chuẩn hóa tên/kiểu dữ liệu; chọn thuộc tính; mã hóa dữ liệu phân loại; chuẩn hóa/thang đo nếu cần; ghi rõ lý do cho từng quyết định.
5. **Khám phá dữ liệu (EDA) có mục tiêu:** Dùng bảng thống kê và biểu đồ để hiểu dữ liệu, nhưng EDA chỉ là bước hỗ trợ, không phải kết quả chính của đề tài.
6. **Biến đổi dữ liệu sang biểu diễn phù hợp với thuật toán:** Ví dụ giỏ hàng dạng transaction/one-hot cho khai thác tập phổ biến; ma trận đặc trưng số đã scale cho gom cụm.
7. **Thực hiện thuật toán và lựa chọn tham số:** Giải thích ngưỡng support/confidence/lift hoặc số cụm, metric khoảng cách, tiêu chí dừng... thay vì dùng mặc định mà không phân tích.
8. **Đánh giá và so sánh:** Dùng chỉ số phù hợp, khảo sát độ nhạy tham số và so sánh ít nhất hai phương án/cấu hình để chứng minh kết quả có ý nghĩa.
9. **Diễn giải tri thức:** Chuyển frequent itemset/association rule hoặc cluster thành nhận xét dễ hiểu; chọn các kết quả thực sự có giá trị thay vì liệt kê hàng trăm luật hoặc cụm.
10. **Xây dựng sản phẩm demo:** Sản phẩm phải cho phép người xem nhập/chọn một số điều kiện và quan sát kết quả khai thác. Có thể dùng Streamlit, Gradio, notebook tương tác hoặc dashboard có chức năng lọc và sinh kết quả.
11. **Kết luận và khả năng mở rộng:** Nêu hạn chế của dữ liệu/phương pháp, những trường hợp kết quả có thể sai lệch và hướng cải tiến.

---

### 1.3. Yêu cầu kỹ thuật theo loại đề tài

#### A. Đề tài khai thác tập phổ biến / luật kết hợp
- Phải xây dựng đúng đơn vị giao dịch (transaction). Nhóm cần giải thích mỗi transaction đại diện cho điều gì và vì sao cách biểu diễn đó hợp lý.
- Thực hiện ít nhất 02 phương pháp trong nhóm Apriori, FP-Growth và IT-Tree theo nội dung đã học; khuyến khích so sánh cả 03 nếu kích thước dữ liệu cho phép.
- Phải báo cáo ít nhất support, confidence và lift; phân tích tác động của ngưỡng minsup/minconf đến số lượng frequent itemsets/rules và thời gian chạy.
- Có bước lọc luật dư thừa hoặc luật ít giá trị; trình bày khoảng 10-20 luật tiêu biểu và giải thích ý nghĩa ứng dụng của chúng.
- Phần demo nên cho phép thay đổi ngưỡng, chọn sản phẩm/đặc trưng ở vế trái và trả về các gợi ý/luật liên quan.

#### B. Đề tài gom cụm
- Không sử dụng nhãn mục tiêu để tạo cụm. Nếu dữ liệu có nhãn như Churn, Satisfaction hoặc y, chỉ dùng nhãn sau khi gom cụm để mô tả/hậu kiểm các cụm.
- Phải chuẩn hóa hoặc biến đổi thang đo khi cần; giải thích việc xử lý biến lệch mạnh, biến phân loại và các thuộc tính không nên đưa trực tiếp vào khoảng cách.
- K-Means có thể dùng làm baseline. Nhóm cần so sánh với ít nhất một phương án khác hoặc một cấu hình có cơ sở (ví dụ Hierarchical, DBSCAN, thay đổi tập đặc trưng hoặc xử lý ngoại lệ).
- Đánh giá bằng các tiêu chí phù hợp như Elbow, Silhouette Score, Davies-Bouldin, Calinski-Harabasz và đặc biệt là khả năng diễn giải profile từng cụm.
- Phần demo nên cho phép xem profile cụm, chọn đối tượng mới để gán vào cụm gần nhất hoặc lọc/so sánh các cụm.

---

### 1.4. Sản phẩm phải nộp

- **01 báo cáo Word (.docx)**, khuyến nghị khoảng 50 trang, trình bày theo cấu trúc ở cuối tài liệu này.
- **Mã nguồn Python và tệp requirements.txt** hoặc ghi rõ thư viện/phiên bản cần thiết. Notebook phải được chạy sạch từ đầu đến cuối trước khi nộp.
- **Bộ dữ liệu gốc** hoặc hướng dẫn tải; bộ dữ liệu sau tiền xử lý nếu nhóm tạo ra tệp trung gian quan trọng.
- **Sản phẩm demo** có thể chạy tại lớp. Không bắt buộc triển khai lên Internet; có thể chạy cục bộ hoặc trên Google Colab nếu chuẩn bị đầy đủ.
- **Slide báo cáo** ngắn gọn; không đưa toàn bộ báo cáo Word lên slide.
- **Một tệp README** ngắn hướng dẫn cách chạy mã nguồn và demo.

---

### 1.5. Hình thức báo cáo tại lớp

- Mỗi nhóm trình bày khoảng 8-10 phút, sau đó demo và trả lời câu hỏi khoảng 3-5 phút. Giảng viên có thể điều chỉnh thời lượng tùy số lượng nhóm thực tế.
- Cả 03 thành viên phải có mặt và tham gia. Mỗi thành viên đều phải thực hiện báo cáo.
- Phần trình bày tập trung vào: bài toán, dữ liệu, quyết định tiền xử lý quan trọng, cách chọn thuật toán/tham số, kết quả chính, insight và demo.
- Không đọc slide. Nhóm phải có khả năng giải thích một luật kết hợp, một frequent itemset hoặc profile của một cụm bằng ngôn ngữ dễ hiểu.

---

## 2. DANH SÁCH ĐỀ TÀI

### 2.1. Nhóm đề tài khai thác tập phổ biến và luật kết hợp

#### 1. Phân tích giỏ hàng siêu thị và xây dựng gợi ý mua kèm
- **Nội dung tóm tắt:** Xây dựng transaction theo từng khách hàng/ngày mua, khai thác frequent itemsets và luật kết hợp giữa các mặt hàng. So sánh Apriori với FP-Growth và/hoặc IT-Tree ở nhiều ngưỡng support; phân tích support, confidence, lift và thời gian chạy. Từ các luật tốt, xây dựng chức năng demo: người dùng chọn một hoặc nhiều mặt hàng đã có trong giỏ và hệ thống đề xuất các mặt hàng thường được mua kèm. Nhóm cần xử lý các sản phẩm hiếm và tránh đưa ra luật có confidence cao nhưng lift xấp xỉ 1.
- **Dữ liệu:** Groceries dataset. Khoảng 38 nghìn dòng dữ liệu mua hàng, phù hợp trực tiếp cho Market Basket Analysis. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset)

#### 2. Khai thác mẫu mua hàng tại tiệm bánh theo thời điểm
- **Nội dung tóm tắt:** Khai thác các món thường xuất hiện cùng nhau trong hơn 9.000 giao dịch của một tiệm bánh. Ngoài luật kết hợp tổng quát, nhóm chia dữ liệu theo buổi sáng/trưa/chiều hoặc ngày trong tuần để khảo sát xem cấu trúc giỏ hàng có thay đổi theo thời gian hay không. Phần demo cho phép chọn khung thời gian và một món để hiển thị các món đi kèm có lift cao. Điểm nhấn của đề tài là biến thông tin ngày/giờ thành ngữ cảnh khai thác thay vì chỉ chạy Apriori một lần trên toàn bộ dữ liệu.
- **Dữ liệu:** The Bread Basket. Dữ liệu tiệm bánh với hơn 20 nghìn bản ghi và hơn 9 nghìn transaction, có thông tin ngày/giờ và món. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/mittalvasu95/the-bread-basket)

#### 3. Khai thác luật kết hợp cho dữ liệu bán lẻ trực tuyến và đề xuất cross-selling
- **Nội dung tóm tắt:** Làm sạch dữ liệu giao dịch bán lẻ trực tuyến: xử lý đơn hủy, số lượng âm, dữ liệu thiếu và chuẩn hóa mã sản phẩm. Tạo transaction theo InvoiceNo, khai thác các nhóm sản phẩm thường mua cùng nhau và so sánh kết quả giữa các quốc gia có đủ số giao dịch. Nhóm cần đánh giá ảnh hưởng của minsup đối với số luật và runtime, đồng thời xây dựng một màn hình demo đề xuất sản phẩm mua kèm. Có thể mở rộng bằng cách chỉ khai thác top sản phẩm để giảm độ thưa và so sánh với khai thác toàn bộ dữ liệu.
- **Dữ liệu:** Online Retail II UCI. Dữ liệu giao dịch thực tế của một nhà bán lẻ trực tuyến tại Anh trong khoảng hai năm. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)

#### 4. So sánh khả năng mở rộng của Apriori, FP-Growth và IT-Tree trên dữ liệu bán lẻ lớn
- **Nội dung tóm tắt:** Tập trung vào khía cạnh thuật toán. Sau khi tạo transaction từ BillNo và Itemname, chạy ít nhất hai thuật toán khai thác frequent itemset và khảo sát runtime/số itemset khi thay đổi minsup. Nhóm cần thiết kế thí nghiệm có kiểm soát, ghi rõ kích thước dữ liệu và cấu hình máy, sau đó chọn các luật có ý nghĩa để minh họa ứng dụng gợi ý mua kèm. Demo có thể cho phép điều chỉnh minsup/minconf và quan sát số luật cùng thời gian chạy gần đúng trên một tập dữ liệu con.
- **Dữ liệu:** Market Basket Analysis. Bộ dữ liệu bán lẻ hơn 500 nghìn dòng với BillNo, Itemname, Quantity, Date, Price, CustomerID và Country. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/aslanahmedov/market-basket-analysis)

#### 5. Khai thác quan hệ mua kèm giữa các danh mục sản phẩm trong thương mại điện tử Olist
- **Nội dung tóm tắt:** Dữ liệu Olist gồm nhiều bảng nên nhóm phải thực hiện bước ghép dữ liệu đúng khóa. Từ order_items và products, xây dựng mỗi order_id thành một transaction gồm các danh mục sản phẩm. Khai thác các cặp/nhóm danh mục thường được mua trong cùng đơn hàng; có thể phân tích thêm theo bang của khách hàng hoặc khoảng thời gian. Sản phẩm demo hiển thị danh mục được chọn và các danh mục có khả năng cross-sell tốt nhất. Đề tài đánh giá mạnh phần tiền xử lý nhiều bảng và khả năng diễn giải luật.
- **Dữ liệu:** Brazilian E-Commerce Public Dataset by Olist. Khoảng 100 nghìn đơn hàng với nhiều bảng về đơn hàng, sản phẩm, khách hàng, thanh toán và đánh giá. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

#### 6. Khai thác mẫu đồng xuất hiện thể loại và thuộc tính nội dung trên Netflix
- **Nội dung tóm tắt:** Xem mỗi phim/chương trình là một transaction gồm các item dạng Genre=..., Country=..., Rating=... và có thể thêm Type=Movie/TV Show. Tách trường listed_in và country thành nhiều item, làm sạch giá trị thiếu rồi khai thác frequent itemsets/association rules để phát hiện các tổ hợp thể loại, quốc gia và phân loại độ tuổi thường đi cùng nhau. Nhóm phải giải thích rõ đây là khai thác đồng xuất hiện thuộc tính, không phải hành vi người dùng. Demo cho phép chọn một thể loại và tìm các thể loại/thuộc tính thường đồng xuất hiện.
- **Dữ liệu:** Netflix Movies and TV Shows. Hơn 8.000 tiêu đề với thể loại, quốc gia, diễn viên, đạo diễn, rating, năm phát hành và loại nội dung. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/shivamb/netflix-shows)

#### 7. Khai thác luật kết hợp giữa gói dịch vụ viễn thông và hiện tượng rời mạng
- **Nội dung tóm tắt:** Chuyển mỗi khách hàng thành transaction gồm các item như InternetService=Fiber, OnlineSecurity=No, Contract=Month-to-month, PaymentMethod=... và Churn=Yes/No. Khai thác các luật có vế phải liên quan đến Churn để phát hiện những tổ hợp dịch vụ/hợp đồng thường đi cùng hiện tượng rời mạng. Đây là bài toán association rule mining, không xây dựng mô hình phân lớp. Nhóm cần lọc luật theo lift và độ hỗ trợ, tránh kết luận nhân quả. Demo cho phép chọn một cấu hình dịch vụ và hiển thị các luật tương đồng.
- **Dữ liệu:** Telco Customer Churn. Dữ liệu IBM mẫu về khoảng 7.000 khách hàng, gói dịch vụ, hợp đồng, chi phí và trạng thái churn. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

#### 8. Khai thác luật đặc trưng của nấm ăn được và nấm độc bằng frequent itemset
- **Nội dung tóm tắt:** Biến mỗi mẫu nấm thành một transaction gồm các item thuộc tính-giá trị, ví dụ odor=foul, gill-size=narrow, habitat=woods và class=poisonous/edible. Khai thác frequent itemsets và các luật có consequent là class để tìm những tổ hợp đặc trưng gắn với từng nhóm. Nhóm phải phân tích support, confidence, lift, loại bỏ luật trùng lặp và nhấn mạnh rằng kết quả chỉ có ý nghĩa trên dữ liệu, không dùng làm hướng dẫn an toàn ngoài thực tế. Demo cho phép nhập một số đặc trưng và tìm luật phù hợp.
- **Dữ liệu:** Mushroom Classification. Dữ liệu UCI dạng bảng với đặc trưng phân loại của nhiều mẫu nấm và nhãn edible/poisonous. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/uciml/mushroom-classification)

#### 9. Khai thác mối liên hệ giữa thói quen ăn uống và sở thích thực phẩm của sinh viên
- **Nội dung tóm tắt:** Bộ dữ liệu thô có nhiều biến khảo sát và một số câu trả lời chưa sạch. Nhóm chọn một tập biến hợp lý, chuẩn hóa dữ liệu phân loại, rời rạc hóa một số biến số nếu cần và chuyển mỗi sinh viên thành một transaction gồm các item mô tả thói quen/sở thích. Khai thác các luật như mức độ nấu ăn, chế độ ăn, thói quen ăn sáng, comfort food hoặc xu hướng dinh dưỡng. Điểm chính là thiết kế item có ý nghĩa và xử lý dữ liệu khảo sát cẩn thận. Demo cho phép chọn một thói quen và xem các sở thích thường đi cùng.
- **Dữ liệu:** Food choices. 126 phản hồi khảo sát về lựa chọn thực phẩm, dinh dưỡng, nấu ăn và sở thích của sinh viên đại học; dữ liệu còn thô. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/borapajo/food-choices)

#### 10. Khai thác mẫu hành vi phiên truy cập liên quan đến quyết định mua hàng trực tuyến
- **Nội dung tóm tắt:** Dữ liệu gồm hơn 12 nghìn phiên truy cập với thời gian trên các loại trang, bounce rate, exit rate, visitor type, weekend và nhãn Revenue. Nhóm rời rạc hóa các biến liên tục thành mức thấp/trung bình/cao dựa trên phân phối có giải thích, sau đó tạo transaction các item dạng ProductRelatedDuration=High, BounceRates=Low, VisitorType=Returning, Revenue=True. Khai thác luật có Revenue=True/False ở vế phải và so sánh các nhóm hành vi. Không xây dựng classifier; trọng tâm là luật kết hợp và diễn giải mẫu hành vi.
- **Dữ liệu:** Online Shoppers Purchasing Intention Dataset. 12.330 phiên mua sắm trực tuyến với 10 biến số, 8 biến phân loại và cờ Revenue. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/imakash3011/online-shoppers-purchasing-intention-dataset)

---

### 2.2. Nhóm đề tài gom cụm

#### 11. Phân khúc khách hàng trung tâm thương mại theo thu nhập và hành vi chi tiêu
- **Nội dung tóm tắt:** Tiền xử lý các đặc trưng tuổi, giới tính, thu nhập và Spending Score; thực hiện chuẩn hóa phù hợp rồi gom cụm khách hàng. K-Means được dùng làm baseline, sau đó so sánh với Hierarchical Clustering hoặc một phương án khác. Dùng Elbow/Silhouette để lựa chọn số cụm và xây dựng profile cho từng phân khúc như thu nhập cao-chi tiêu cao, thu nhập cao-chi tiêu thấp... Demo cho phép nhập thông tin một khách hàng mới và hiển thị cụm gần nhất cùng mô tả phân khúc.
- **Dữ liệu:** Mall Customer Segmentation Data. Dữ liệu khách hàng trung tâm thương mại gồm CustomerID, Gender, Age, Annual Income và Spending Score. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python)

#### 12. Phân khúc người dùng thẻ tín dụng theo hành vi chi tiêu và thanh toán
- **Nội dung tóm tắt:** Bộ dữ liệu có khoảng 9.000 khách hàng và nhiều biến hành vi. Nhóm phải xử lý missing values, phân phối lệch, chuẩn hóa thang đo và cân nhắc log-transform cho các biến tiền tệ. Thực hiện K-Means và ít nhất một phương án so sánh; dùng PCA chỉ để hỗ trợ trực quan hóa nếu cần. Xây dựng profile các cụm như người dùng trả góp thường xuyên, khách hàng dùng cash advance cao, khách hàng thanh toán đầy đủ... Demo hiển thị radar/bar profile của các cụm và gán khách hàng mới vào cụm.
- **Dữ liệu:** Credit Card Dataset for Clustering. Khoảng 9.000 chủ thẻ với 18 biến về balance, purchases, cash advance, payment, credit limit và tenure. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata)

#### 13. Xây dựng chân dung khách hàng từ dữ liệu chiến dịch marketing
- **Nội dung tóm tắt:** Tạo thêm các đặc trưng có ý nghĩa như tuổi, tổng chi tiêu, số trẻ em trong gia đình, tổng số lần mua và mức độ phản hồi chiến dịch. Xử lý missing/outlier, scale dữ liệu rồi gom cụm để tạo các customer persona. So sánh K-Means với Hierarchical hoặc DBSCAN nếu phù hợp. Nhóm phải mô tả từng cụm bằng ngôn ngữ marketing và đề xuất một chiến lược tiếp cận tương ứng, nhưng tránh sử dụng nhãn Response để tạo cụm. Demo cho phép xem profile và tỷ lệ phản hồi chiến dịch của mỗi cụm sau khi phân nhóm.
- **Dữ liệu:** Customer Personality Analysis. Dữ liệu khách hàng gồm nhân khẩu học, thu nhập, chi tiêu theo nhóm sản phẩm, kênh mua và phản hồi chiến dịch. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)

#### 14. Phân nhóm khách hàng bán sỉ theo cơ cấu chi tiêu hàng năm
- **Nội dung tóm tắt:** Sử dụng các khoản chi Fresh, Milk, Grocery, Frozen, Detergents_Paper và Delicassen để phân nhóm khách hàng của nhà phân phối. Nhóm cần xem xét độ lệch mạnh, outlier và hiệu quả của log-transform trước khi chuẩn hóa. So sánh ít nhất hai phương án gom cụm và đánh giá bằng Silhouette/Davies-Bouldin. Kết quả phải tạo profile cụm có thể dùng cho chính sách bán hàng, ví dụ khách hàng thiên về hàng tươi sống hoặc nhóm mua nhiều grocery/detergent. Có thể hậu kiểm cụm theo Channel và Region.
- **Dữ liệu:** Wholesale customers Data Set. 440 khách hàng của nhà phân phối với chi tiêu hằng năm theo sáu nhóm sản phẩm cùng Channel và Region. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/binovi/wholesale-customers-data-set)

#### 15. Gom cụm các quốc gia theo điều kiện kinh tế - xã hội và sức khỏe
- **Nội dung tóm tắt:** Dùng các chỉ số về thu nhập, GDP, xuất nhập khẩu, sức khỏe, tuổi thọ, tử vong trẻ em và lạm phát để phân nhóm quốc gia theo mức phát triển. Nhóm chuẩn hóa dữ liệu, phân tích tương quan và thực hiện K-Means cùng một phương án so sánh. Có thể dùng PCA để trực quan hóa cụm trên 2D. Kết quả cần trả lời: đặc điểm nào phân biệt các cụm, những quốc gia nào ở nhóm cần ưu tiên hỗ trợ và vì sao. Demo có thể cho phép chọn quốc gia để hiển thị cụm và profile so với trung bình cụm.
- **Dữ liệu:** Unsupervised Learning on Country Data. Dữ liệu quốc gia với các yếu tố kinh tế-xã hội và sức khỏe, được thiết kế phù hợp cho bài toán clustering. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/rohan0301/unsupervised-learning-on-country-data)

#### 16. Phân nhóm quốc gia theo các yếu tố tạo nên mức độ hạnh phúc
- **Nội dung tóm tắt:** Chọn một năm có đầy đủ các biến hoặc xây dựng bảng thống nhất theo năm, sau đó gom cụm quốc gia dựa trên GDP/capita, social support, healthy life expectancy, freedom, generosity, corruption perception và các yếu tố liên quan. Không dùng Happiness Rank để trực tiếp tạo cụm nếu muốn đánh giá độc lập. Nhóm so sánh profile cụm và xem mức Happiness Score phân bố thế nào sau khi gom cụm. Demo cho phép chọn quốc gia hoặc cụm và hiển thị radar chart các yếu tố so với trung bình.
- **Dữ liệu:** World Happiness Report. Dữ liệu xếp hạng hạnh phúc nhiều quốc gia với các yếu tố kinh tế, xã hội, sức khỏe và tự do. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/synful/world-happiness-report)

#### 17. Gom cụm bài hát Spotify theo đặc trưng âm thanh để tạo playlist
- **Nội dung tóm tắt:** Chọn các audio features như danceability, energy, valence, acousticness, instrumentalness, speechiness, tempo và loudness; xử lý trùng lặp, giá trị bất thường và scale. Gom cụm các track để tạo các nhóm âm nhạc có profile khác nhau như sôi động, thư giãn, acoustic, mood thấp... Không dùng tên genre làm đầu vào chính nếu muốn hậu kiểm tính tự nhiên của cụm; có thể dùng genre sau đó để xem mỗi cụm chứa những thể loại nào. Demo cho phép chọn một bài hát và tìm các track cùng cụm hoặc hiển thị profile của playlist.
- **Dữ liệu:** Spotify Tracks Dataset. Bộ dữ liệu CSV cỡ vài MB với nhiều track và các audio features do Spotify cung cấp. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)

#### 18. Gom cụm các kiểu sử dụng xe đạp chia sẻ theo thời gian và thời tiết
- **Nội dung tóm tắt:** Từ dữ liệu theo giờ/ngày, tạo các vector mô tả tình huống sử dụng xe đạp dựa trên hour, season, workingday, weather, temperature, humidity, windspeed và số lượt thuê. Nhóm có thể gom cụm các khung giờ hoặc các ngày để nhận diện các pattern như giờ đi làm, cuối tuần giải trí, ngày thời tiết xấu, mùa cao điểm. Cần xử lý biến chu kỳ giờ/tháng hợp lý hoặc giải thích cách mã hóa. Demo cho phép chọn ngày/giờ hoặc điều kiện thời tiết và hiển thị kiểu sử dụng tương ứng.
- **Dữ liệu:** Bike Sharing Dataset. Dữ liệu lượt thuê xe đạp theo giờ và ngày trong 2011-2012, kèm thông tin thời tiết và mùa. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)

#### 19. Phân khúc hành khách hàng không theo trải nghiệm dịch vụ
- **Nội dung tóm tắt:** Gom cụm hành khách dựa trên tuổi, flight distance, loại chuyến đi, hạng ghế và các điểm đánh giá dịch vụ như wifi, seat comfort, cleanliness, baggage handling, inflight service... Nhãn Satisfaction không được dùng để tạo cụm; sau khi clustering mới so sánh tỷ lệ hài lòng của từng cụm để hỗ trợ diễn giải. Nhóm xử lý biến phân loại, scale và chọn thuật toán phù hợp. Demo hiển thị profile trải nghiệm của từng cụm và các yếu tố dịch vụ cần ưu tiên cải thiện.
- **Dữ liệu:** Airline Passenger Satisfaction. Hơn 100 nghìn phản hồi hành khách với thông tin chuyến bay và điểm đánh giá nhiều khía cạnh dịch vụ. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction)

#### 20. Phân khúc khách hàng ngân hàng phục vụ chiến dịch tiếp thị tiền gửi
- **Nội dung tóm tắt:** Dữ liệu chứa cả biến số và biến phân loại về khách hàng, tình trạng tài chính và lịch sử liên hệ marketing. Nhóm lựa chọn/mã hóa đặc trưng, xử lý trường unknown, scale biến số và gom cụm khách hàng mà không dùng biến y để tạo cụm. Sau khi clustering, dùng y chỉ để hậu kiểm tỷ lệ đăng ký tiền gửi ở từng cụm và mô tả profile có khả năng phản hồi cao/thấp. Có thể mở rộng bằng việc khai thác một vài association rules trong từng cụm, nhưng phần chính vẫn là gom cụm. Demo cho phép xem profile cụm và tỷ lệ đăng ký hậu kiểm.
- **Dữ liệu:** UCI Bank Marketing Dataset. Dữ liệu chiến dịch marketing qua điện thoại của ngân hàng Bồ Đào Nha với đặc trưng khách hàng, tài chính, liên hệ và biến y. [Kaggle - truy cập bộ dữ liệu](https://www.kaggle.com/datasets/adityamhaske/bank-marketing-dataset)

---

## 3. THANG ĐIỂM (10,0 ĐIỂM)

Điểm đồ án gồm hai phần: **Báo cáo Word 6,0 điểm** và **Báo cáo + demo tại lớp 4,0 điểm**.

### 3.1. Báo cáo Word - 6,0 điểm

| Tiêu chí | Điểm | Mô tả yêu cầu |
| :--- | :---: | :--- |
| **1. Xác định bài toán và hiểu dữ liệu** | 0,50 | Mục tiêu rõ ràng; mô tả dữ liệu, thuộc tính, nguồn Kaggle và câu hỏi khai thác đúng bản chất. |
| **2. Tiền xử lý và chuẩn bị dữ liệu** | 1,00 | Phát hiện và xử lý vấn đề dữ liệu hợp lý; giải thích quyết định; tạo đúng representation cho transaction hoặc clustering. |
| **3. Phương pháp khai thác dữ liệu** | 1,50 | Mô tả đúng thuật toán; cài đặt/chạy đúng; lựa chọn tham số có cơ sở; đáp ứng yêu cầu so sánh phương án. |
| **4. Thực nghiệm và đánh giá** | 1,50 | Có thí nghiệm có cấu trúc; dùng metric phù hợp; bảng/biểu đồ rõ; phân tích ảnh hưởng tham số hoặc so sánh thuật toán/cấu hình. |
| **5. Diễn giải kết quả và insight** | 1,00 | Chọn kết quả tiêu biểu, giải thích frequent itemset/rule/cluster, rút ra nhận xét có ý nghĩa và không suy diễn quá mức dữ liệu. |
| **6. Chất lượng báo cáo và khả năng tái lập** | 0,50 | Bố cục khoa học; hình/bảng có tên; trích dẫn nguồn; mã nguồn/README rõ; có bảng phân công công việc; văn phong và trình bày tốt. |

---

### 3.2. Báo cáo và demo tại lớp - 4,0 điểm

| Tiêu chí | Điểm | Mô tả yêu cầu |
| :--- | :---: | :--- |
| **1. Trình bày vấn đề và pipeline** | 0,50 | Trình bày mạch lạc, đúng trọng tâm; thể hiện được tiến trình từ dữ liệu đến tri thức. |
| **2. Demo sản phẩm** | 1,50 | Demo chạy được; thể hiện đúng kết quả khai thác; người xem có thể tương tác/chọn điều kiện; xử lý tình huống cơ bản. |
| **3. Giải thích kết quả và kỹ thuật** | 1,00 | Giải thích được thuật toán, tham số, metric, luật kết hợp hoặc profile cụm bằng ngôn ngữ rõ ràng. |
| **4. Trả lời câu hỏi** | 0,50 | Cả nhóm hiểu bài; trả lời đúng và có lập luận; phân biệt được kết quả thực nghiệm với suy luận chủ quan. |
| **5. Phối hợp nhóm và thời gian** | 0,50 | Phân chia trình bày hợp lý, đúng thời gian, các thành viên đều tham gia và làm chủ phần việc. |

---

### 3.3. Quy định điều chỉnh điểm cá nhân

- Điểm cơ sở là điểm chung của nhóm. Giảng viên có thể điều chỉnh điểm từng sinh viên khi phần đóng góp, mức độ hiểu bài hoặc khả năng trả lời câu hỏi chênh lệch rõ rệt.
- Sinh viên không nắm được phần việc đã ghi trong bảng phân công hoặc không giải thích được mã nguồn/kết quả của nhóm có thể bị trừ điểm cá nhân.
- Trường hợp vắng báo cáo không có lý do chính đáng: phần điểm báo cáo tại lớp của sinh viên đó sẽ được 0đ. Sinh viên vẫn sẽ có điểm phần word nếu trong bảng phân công thể hiện sinh viên hoàn thành các công việc được giao.
- Điểm tối đa của phần đồ án này vẫn là 10,0 điểm.

---

## 4. CẤU TRÚC BÁO CÁO WORD ĐỀ XUẤT

1. **Trang bìa:** Tên học phần, mã đề tài, tên đề tài, danh sách 03 thành viên, lớp, giảng viên, học kỳ.
2. **Bảng phân công công việc và tỷ lệ đóng góp.**
3. **Giới thiệu bài toán:** Bối cảnh, mục tiêu, câu hỏi khai thác dữ liệu, giá trị của kết quả.
4. **Dữ liệu:** Nguồn Kaggle, mô tả tệp/bảng, thuộc tính, kích thước, vấn đề chất lượng dữ liệu.
5. **Tiền xử lý dữ liệu:** Các bước làm sạch, biến đổi, lựa chọn đặc trưng và lý do.
6. **Phương pháp:** Mô tả thuật toán, biểu diễn dữ liệu, tham số, quy trình thực nghiệm.
7. **Kết quả và đánh giá:** Bảng/biểu đồ, metric, so sánh thuật toán/cấu hình, phân tích tham số.
8. **Diễn giải tri thức và ứng dụng:** Các luật/frequent itemset/cluster tiêu biểu, insight và khuyến nghị.
9. **Sản phẩm demo:** Mô tả chức năng, ảnh giao diện và cách chạy.
10. **Kết luận, hạn chế và hướng phát triển.**
11. **Tài liệu tham khảo:** Kaggle Data Card, tài liệu thuật toán, thư viện, bài viết hoặc nguồn đã sử dụng.
12. **Phụ lục nếu cần:** Bảng luật đầy đủ, tham số, cấu trúc thư mục mã nguồn.

---

## 5. CHECKLIST TRƯỚC KHI NỘP

- [ ] Đúng nhóm 03 thành viên và có bảng phân công.
- [ ] Đúng đề tài, đúng dữ liệu Kaggle được giao.
- [ ] Có mô tả pipeline đầy đủ và không chỉ dừng ở EDA.
- [ ] Có bước tiền xử lý được giải thích, không chỉ gọi hàm tự động.
- [ ] Có so sánh thuật toán/cấu hình và metric đánh giá phù hợp.
- [ ] Có phần diễn giải kết quả thành tri thức/insight.
- [ ] Có sản phẩm demo chạy được.
- [ ] Mã nguồn chạy lại được từ đầu; đường dẫn dữ liệu không phụ thuộc máy cá nhân.
- [ ] Báo cáo Word có hình/bảng rõ ràng, trích dẫn nguồn và không sao chép notebook.
- [ ] Cả 03 thành viên chuẩn bị trả lời câu hỏi tại lớp.

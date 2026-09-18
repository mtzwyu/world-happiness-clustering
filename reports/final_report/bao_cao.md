<!-- TOC -->

<!-- Ghi chú nội bộ (không xuất hiện trong file Word): đây là bản gốc của báo cáo.
     Sửa nội dung ở đây rồi chạy .venv\Scripts\python.exe reports/final_report/build_report.py để sinh lại .docx.
     Chỗ nào chưa có kết quả thì giữ nguyên chỉ thị chèn bảng/hình, báo cáo vẫn build được và in dòng nhắc đỏ.
     Mọi con số phải lấy từ reports/tables hoặc reports/figures. Mọi ghi chú dạng này sẽ bị bỏ qua khi sinh Word. -->

# 1. Bảng phân công công việc và tỷ lệ đóng góp

<!-- Phụ trách: Hà Mạnh Trường -->

Nhóm gồm đúng 03 sinh viên. Bảng dưới đây nêu phần việc chính, phần việc hỗ trợ và tỷ lệ đóng góp dự kiến của từng thành viên; tỷ lệ cộng lại bằng 100%.

| Thành viên | Công việc chính | Công việc hỗ trợ | Tỷ lệ đóng góp (%) |
| Hà Mạnh Trường (2045240326, nhóm trưởng) | Thu thập và tiền xử lý dữ liệu 5 năm; dựng bảng dữ liệu trung gian; kiểm soát khả năng chạy lại của mã nguồn; điều phối tiến độ và ghép báo cáo; viết mục 1-4 | Rà soát phần thuật toán gom cụm; đối chiếu số liệu giữa các năm; hỗ trợ nạp dữ liệu cho demo | 34 |
| Huỳnh Tâm Trí (2045240315) | Tự cài đặt thuật toán gom cụm (K-Means, phân cấp Ward, DBSCAN), giảm chiều PCA và các độ đo đánh giá; chạy thực nghiệm 5 cấu hình × 5 năm; khảo sát tham số; viết mục 5-7 | Rà soát bộ nạp dữ liệu; kiểm chứng các độ đo bằng thư viện; rà soát phần nối dữ liệu của demo | 33 |
| Ngô Quang Trung (2045240325) | Phân tích khám phá dữ liệu; diễn giải kết quả gom cụm; ghép cụm giữa các năm và lập bảng dịch chuyển cụm; xây dựng demo Streamlit; làm slide; viết mục 8-11 | Rà soát notebook 01; kiểm tra chất lượng dữ liệu theo năm; kiểm tra bản đồ; điều hành buổi tổng duyệt | 33 |

Cả ba thành viên cùng tham gia tất cả các bước của quy trình và đều có thể trình bày, giải thích bất kỳ phần nào của báo cáo khi được hỏi.

# 2. Giới thiệu bài toán

<!-- Phụ trách: Hà Mạnh Trường -->

## 2.1. Bối cảnh

World Happiness Report (WHR) là báo cáo thường niên đánh giá mức độ hạnh phúc của người dân các quốc gia, dựa trên khảo sát Gallup World Poll với câu hỏi Cantril Ladder (người trả lời tự chấm cuộc sống hiện tại từ 0 đến 10). Bên cạnh điểm hạnh phúc tổng hợp, báo cáo còn công bố sáu yếu tố cơ sở được dùng để giải thích vì sao quốc gia này cao hơn quốc gia khác.

## 2.2. Mục tiêu

Phân nhóm các quốc gia thành những nhóm có đặc điểm kinh tế - xã hội - sức khỏe tương đồng, chỉ dựa trên sáu yếu tố cơ sở, rồi dùng điểm hạnh phúc để kiểm tra xem cách phân nhóm tự nhiên đó có phân hóa đúng mức sống thực tế hay không.

## 2.3. Câu hỏi khai thác dữ liệu

1. Có thể phân chia các quốc gia thành những nhóm đặc trưng nào dựa trên sáu yếu tố cơ sở?
2. Các nhóm khác biệt rõ nhất ở những yếu tố nào (kinh tế, hỗ trợ xã hội, sức khỏe, tự do, hào phóng, nhận thức tham nhũng)?
3. Cấu trúc phân nhóm thay đổi thế nào qua năm năm 2015-2019, và quốc gia nào chuyển nhóm?
4. Nhóm quốc gia nào ở mức thấp nhất và cần ưu tiên hỗ trợ?

> Điểm hạnh phúc và thứ hạng hạnh phúc không được đưa vào ma trận đặc trưng dùng để gom cụm; hai thuộc tính này chỉ dùng để hậu kiểm ở mục 7.

# 3. Dữ liệu

<!-- Phụ trách: Hà Mạnh Trường (số liệu chất lượng dữ liệu do Ngô Quang Trung kiểm) -->

## 3.1. Nguồn dữ liệu

Bộ dữ liệu World Happiness Report trên Kaggle, gồm năm tệp CSV theo năm. Nguồn tham chiếu chính thức là báo cáo của Liên Hợp Quốc và trang dữ liệu của Kaggle (xem mục 10).

| Năm | Tệp | Số dòng dữ liệu |
| 2015 | data/raw/2015.csv | 158 |
| 2016 | data/raw/2016.csv | 157 |
| 2017 | data/raw/2017.csv | 155 |
| 2018 | data/raw/2018.csv | 156 |
| 2019 | data/raw/2019.csv | 156 |

## 3.2. Ý nghĩa các thuộc tính

| Thuộc tính dùng để gom cụm | Ý nghĩa |
| GDP per capita | Mức đóng góp của thu nhập bình quân đầu người vào mức độ hạnh phúc |
| Social support | Mức độ tương trợ xã hội khi người dân gặp khó khăn |
| Healthy life expectancy | Tuổi thọ khỏe mạnh dự tính của người dân |
| Freedom | Mức độ tự do trong việc đưa ra quyết định và lựa chọn cuộc sống |
| Generosity | Mức độ hào phóng, đóng góp thiện nguyện so với mức trung bình |
| Perceptions of corruption | Mức độ tin tưởng vào sự trong sạch của chính phủ và doanh nghiệp |

Các thuộc tính **không** dùng để gom cụm: `Happiness Score`, `Happiness Rank`, `Dystopia Residual`, `Standard Error`, khoảng tin cậy và whisker (các cột sau chỉ mô tả độ bất định của điểm số, không phải yếu tố cơ sở).

## 3.3. Vấn đề chất lượng dữ liệu

- Tên cột không thống nhất giữa các năm (ví dụ `Family` ở 2015-2016 và `Social support` ở 2018-2019; `Economy (GDP per Capita)` ở 2015 và `GDP per capita` ở 2019).
- Năm 2018 thiếu giá trị `Perceptions of corruption` ở một quốc gia (United Arab Emirates).
- Cột vùng địa lý (`Region`) chỉ có ở 2015-2016, không có ở 2017-2019.
- Một số quốc gia đổi tên giữa các năm (Macedonia/North Macedonia, Swaziland/Eswatini), cần chuẩn hóa trước khi so sánh theo thời gian.
- Số quốc gia mỗi năm khác nhau (158, 157, 155, 156, 156), nên mọi so sánh theo thời gian phải ghi rõ cỡ mẫu.

<!-- BANG: reports/tables/data_quality_by_year.csv | Tổng hợp chất lượng dữ liệu theo từng năm (giá trị thiếu, trùng lặp, lệch tên cột) -->

# 4. Tiền xử lý dữ liệu

<!-- Phụ trách: Hà Mạnh Trường -->

Các bước tiền xử lý và lý do:

1. **Chuẩn hóa tên cột** về dạng snake_case thống nhất cho cả năm năm, vì mỗi năm dùng một cách đặt tên khác nhau.
2. **Chuẩn hóa tên quốc gia** giữa các năm để một quốc gia không bị tách thành hai dòng khi phân tích theo thời gian.
3. **Chọn sáu thuộc tính cơ sở** làm ma trận đặc trưng; loại bỏ điểm hạnh phúc, thứ hạng và các cột độ bất định.
4. **Xử lý giá trị thiếu**: với năm 2018, quốc gia thiếu `Perceptions of corruption` bị loại khỏi thực nghiệm của năm đó và được ghi rõ trong phần hạn chế.
5. **Chuẩn hóa thang đo**: dùng Z-score làm cấu hình chính, thêm Min-Max và phương án không chuẩn hóa để so sánh, vì các thuộc tính có đơn vị và độ lệch khác nhau nên khoảng cách Euclid sẽ bị chi phối nếu không chuẩn hóa.
6. **Ghép năm năm thành một bảng trung gian** với bộ cột cố định, lưu ở `data/interim/happiness_merged.csv`.

<!-- BANG: reports/tables/interim_preview.csv | Trích 10 dòng đầu của bảng dữ liệu trung gian sau tiền xử lý -->

<!-- HINH: reports/figures/feature_distributions.png | Phân phối của sáu yếu tố cơ sở sau tiền xử lý -->

<!-- HINH: reports/figures/boxplots_outliers.png | Biểu đồ hộp phát hiện ngoại lệ trên sáu yếu tố -->

<!-- HINH: reports/figures/correlation_heatmap.png | Ma trận tương quan giữa sáu yếu tố và điểm hạnh phúc (điểm hạnh phúc chỉ để tham chiếu, không đưa vào gom cụm) -->

# 5. Phương pháp

<!-- Phụ trách: Huỳnh Tâm Trí -->
## 5.1. Biểu diễn dữ liệu và khoảng cách

Mỗi quốc gia trong một năm là một điểm trong không gian sáu chiều. Khoảng cách giữa hai điểm được tính bằng khoảng cách Euclid; toàn bộ hàm tính khoảng cách, chuẩn hóa và thuật toán đều do nhóm tự cài đặt, không gọi thư viện học máy.

## 5.2. K-Means tự cài đặt

Thuật toán lặp bốn bước: khởi tạo tâm cụm, gán mỗi điểm vào tâm gần nhất, cập nhật tâm bằng trung bình cộng các điểm trong cụm, lặp đến khi nhãn không đổi hoặc hết số vòng lặp. Nhóm dùng khởi tạo k-means++ để giảm phụ thuộc vào điểm khởi tạo và chạy nhiều lần khởi tạo, giữ nghiệm có tổng bình phương khoảng cách trong cụm nhỏ nhất.

## 5.3. Phân cấp Ward tự cài đặt

Bắt đầu với mỗi quốc gia là một cụm, lặp lại việc hợp nhất hai cụm làm tăng tổng bình phương sai số ít nhất (tiêu chí Ward), dùng công thức cập nhật Lance-Williams để không phải tính lại toàn bộ khoảng cách sau mỗi lần hợp nhất. Kết quả lưu lại lịch sử hợp nhất để vẽ biểu đồ cây.

## 5.4. DBSCAN tự cài đặt

Gom cụm theo mật độ với hai tham số `eps` (bán kính lân cận) và `min_samples` (số điểm tối thiểu). Thuật toán phát hiện được cụm có hình dạng bất kỳ và gán nhãn nhiễu cho các điểm nằm ngoài vùng mật độ.

## 5.5. Chọn số cụm

Khảo sát `k` từ 2 đến 9 cho từng năm bằng hai tiêu chí: phương pháp khuỷu tay trên tổng bình phương khoảng cách trong cụm, và hệ số Silhouette. Số cụm tối ưu của từng năm là kết quả chính; cấu hình ba cụm được giữ làm đối chứng để so sánh xuyên năm.

## 5.6. Các độ đo đánh giá

- **Silhouette**: so độ kết dính trong cụm với độ tách biệt so với cụm gần nhất, giá trị càng gần 1 càng tốt.
- **Davies-Bouldin**: tỷ lệ giữa độ tán xạ trong cụm và khoảng cách giữa các cụm, càng nhỏ càng tốt.
- **Calinski-Harabasz**: tỷ lệ phương sai giữa các cụm và trong cụm, càng lớn càng tốt.
- **Adjusted Rand Index**: đo độ ổn định của nhãn cụm khi chạy lại với các seed khác nhau.

## 5.7. Quy trình thực nghiệm

Năm thí nghiệm độc lập theo năm 2015-2019; mỗi năm chạy năm cấu hình lõi: K-Means với chuẩn hóa Z-score, K-Means với Min-Max, K-Means không chuẩn hóa, phân cấp Ward có chuẩn hóa và DBSCAN có chuẩn hóa. Với DBSCAN, quét bốn giá trị `eps` và ba giá trị `min_samples`. Với ba cấu hình K-Means, đo độ ổn định trên 10 seed bằng Adjusted Rand Index. Kết quả của mọi cấu hình được lưu thành CSV để làm nguồn số liệu duy nhất cho báo cáo và demo.

# 6. Kết quả và đánh giá

<!-- Phụ trách: Huỳnh Tâm Trí. Mọi con số dưới đây lấy từ thư mục reports/tables -->

## 6.1. Chọn số cụm theo từng năm

<!-- BANG: reports/tables/k_sensitivity_by_year.csv | Giá trị Inertia và Silhouette theo số cụm cho từng năm -->

<!-- HINH: reports/figures/elbow_silhouette_by_year.png | Biểu đồ khuỷu tay và Silhouette theo số cụm cho năm năm -->

Số cụm tối ưu mỗi năm được chọn theo hai tiêu chí trên và được ghi rõ trong bảng. Mục đối chứng với ba cụm giúp so sánh cấu trúc phân nhóm giữa các năm trên cùng một số cụm.

## 6.2. So sánh năm cấu hình gom cụm

<!-- BANG: reports/tables/model_comparison_metrics_by_year.csv | So sánh năm cấu hình gom cụm trên năm năm theo Silhouette, Davies-Bouldin và Calinski-Harabasz -->

<!-- HINH: reports/figures/scaling_comparison.png | Ảnh hưởng của việc chuẩn hóa dữ liệu tới kết quả gom cụm -->

## 6.3. Độ nhạy tham số của DBSCAN

<!-- BANG: reports/tables/dbscan_sweep.csv | Số cụm và số điểm nhiễu theo eps và min_samples cho từng năm -->

<!-- HINH: reports/figures/dbscan_sweep_heatmap.png | Bản đồ nhiệt số cụm theo eps và min_samples -->

## 6.4. Độ ổn định của cụm

<!-- BANG: reports/tables/stability_ari.csv | Chỉ số Adjusted Rand Index trên 10 seed cho các cấu hình có khởi tạo ngẫu nhiên -->

<!-- HINH: reports/figures/stability_ari_heatmap.png | Mức độ ổn định của nhãn cụm theo cấu hình và theo năm -->

Phân cấp Ward và DBSCAN là thuật toán tất định nên chỉ số ổn định bằng 1; phần này tập trung vào ba cấu hình K-Means.

## 6.5. Nhận xét về kết quả

<!-- TODO (Trí): viết 1-2 đoạn nhận xét dựa trên các bảng trên: cấu hình nào cho cụm tách biệt nhất, việc không chuẩn hóa gây hậu quả gì, eps ảnh hưởng thế nào tới tỷ lệ điểm nhiễu -->

# 7. Diễn giải tri thức và ứng dụng

<!-- Phụ trách: Ngô Quang Trung -->

## 7.1. Chân dung từng cụm

Mỗi cụm được mô tả bằng giá trị trung bình sáu yếu tố và được đặt tên theo ngôn ngữ nghiệp vụ (ví dụ nhóm phát triển toàn diện, nhóm phụ thuộc kinh tế, nhóm cần hỗ trợ).

<!-- BANG: reports/tables/cluster_profiles_by_year.csv | Giá trị trung bình sáu yếu tố của từng cụm theo năm và tên gọi của cụm -->

<!-- HINH: reports/figures/radar_chart_clusters_2019.png | Biểu đồ radar so sánh sáu yếu tố giữa các cụm năm 2019 -->

<!-- HINH: reports/figures/pca_clusters_grid.png | Trực quan hóa các cụm trên không gian giảm chiều PCA cho năm năm -->

## 7.2. Ghép cụm giữa các năm và dịch chuyển cụm

Vì mỗi năm gom cụm độc lập nên nhãn cụm không so sánh trực tiếp được. Nhóm ghép cụm giữa hai năm liền kề theo khoảng cách tâm cụm nhỏ nhất, hoà thì xét điểm hạnh phúc trung bình; nếu số cụm lệch nhau thì chỉ ghép được phần nhỏ hơn và phần dư được ghi là không có cặp tương ứng.

<!-- BANG: reports/tables/cross_year_matching.csv | Bảng ghép cụm giữa các năm liền kề kèm khoảng cách tâm cụm -->

<!-- BANG: data/processed/country_cluster_shift.csv | Bảng dịch chuyển cụm của từng quốc gia qua năm năm -->

<!-- HINH: reports/figures/cluster_count_trend.png | Số lượng quốc gia trong mỗi nhóm qua năm năm -->

## 7.3. Hậu kiểm bằng điểm hạnh phúc

Không dùng điểm hạnh phúc để gom cụm; sau khi gom cụm mới kiểm tra xem các cụm có phân hóa rõ về điểm hạnh phúc hay không.

<!-- HINH: reports/figures/validation_happiness_score_by_cluster.png | Phân bố điểm hạnh phúc theo cụm (hậu kiểm) -->

<!-- BANG: reports/tables/happiness_posthoc_by_year.csv | Thống kê điểm hạnh phúc theo cụm và theo năm -->

## 7.4. Khuyến nghị

<!-- TODO (Trung): nêu 3-4 khuyến nghị gắn với từng nhóm quốc gia (ví dụ nhóm yếu ở sức khỏe cần ưu tiên y tế; nhóm yếu ở nhận thức tham nhũng cần cải cách thể chế), kèm lưu ý không suy diễn nhân quả từ dữ liệu quan sát -->

# 8. Sản phẩm demo

<!-- Phụ trách: Ngô Quang Trung -->

Ứng dụng Streamlit cho phép người xem tương tác trực tiếp với kết quả khai thác:

1. **Tab tổng quan và radar**: chọn năm, thuật toán, cách chuẩn hóa và số cụm; hiển thị chân dung cụm và các chỉ số Silhouette, Davies-Bouldin, Calinski-Harabasz của cấu hình đang chọn.
2. **Tab bản đồ thế giới**: tô màu quốc gia theo cụm; cảnh báo số quốc gia không ánh xạ được mã quốc gia.
3. **Tab tra cứu quốc gia**: chọn một quốc gia để xem cụm, so sánh sáu chỉ số với trung bình cụm và vị trí percentile.
4. **Tab gán quốc gia mới**: nhập sáu chỉ số và nhận cụm gần nhất kèm khoảng cách tới từng tâm cụm.

Cách chạy: `streamlit run app/app.py`. Ứng dụng dùng dữ liệu đã xử lý trong `data/processed/` và các tệp tham số trong `models/`; nếu thiếu thì tự dựng lại từ dữ liệu gốc.

<!-- HINH: reports/figures/demo_screenshot_overview.png | Giao diện tab tổng quan và biểu đồ radar của ứng dụng demo -->

<!-- HINH: reports/figures/demo_screenshot_map.png | Giao diện tab bản đồ thế giới của ứng dụng demo -->

# 9. Kết luận, hạn chế và hướng phát triển

<!-- Phụ trách: Ngô Quang Trung -->

## 9.1. Kết luận

<!-- TODO (Trung): chốt 3-4 kết luận từ số liệu thật: số nhóm phù hợp mỗi năm, yếu tố phân biệt mạnh nhất, mức phân hóa điểm hạnh phúc giữa các nhóm, và nhóm nào cần ưu tiên hỗ trợ -->

## 9.2. Hạn chế

- Dữ liệu khảo sát dựa trên cảm nhận chủ quan của người dân (thang Cantril), có thể lệch theo văn hóa trả lời.
- Số quốc gia mỗi năm khác nhau (158, 157, 155, 156, 156) nên so sánh theo thời gian chỉ mang tính tương đối.
- Năm 2018 thiếu một giá trị ở United Arab Emirates, quốc gia này bị loại khỏi thực nghiệm năm đó.
- Cột vùng địa lý chỉ có ở 2015-2016 nên không dùng được cho phân tích chính.
- K-Means giả định cụm dạng cầu lồi và phương sai tương đương; DBSCAN nhạy với `eps` và `min_samples`.
- Kết quả gom cụm phụ thuộc vào việc chuẩn hóa dữ liệu; phương án không chuẩn hóa bị chi phối bởi thuộc tính có độ lệch lớn.

## 9.3. Hướng phát triển

- Bổ sung chỉ số vĩ mô ngoài bộ dữ liệu (bất bình đẳng thu nhập, phát thải, chi tiêu công) để chân dung cụm đầy đủ hơn.
- Mở rộng chuỗi thời gian ra ngoài 2019 và phân tích quỹ đạo chuyển nhóm của từng quốc gia.
- So sánh thêm các phương pháp gom cụm khác (mô hình hỗn hợp Gaussian, gom cụm mờ) và kiểm định thống kê mức khác biệt giữa các cụm.

# 10. Tài liệu tham khảo

<!-- Phụ trách: cả nhóm; danh mục công thức có trích dẫn nằm ở docs/nghien_cuu/phuong_phap.md -->

1. World Happiness Report — trang chính thức: https://worldhappiness.report/
2. Bộ dữ liệu World Happiness Report trên Kaggle: https://www.kaggle.com/datasets/synful/world-happiness-report
3. Helliwell, J. F., Layard, R., Sachs, J., & De Neve, J.-E. (các năm). *World Happiness Report*. Sustainable Development Solutions Network.
4. Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. *Journal of the American Statistical Association*.
5. Lance, G. N., & Williams, W. T. (1967). A general theory of classificatory sorting strategies: Hierarchical systems. *The Computer Journal*.
6. Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. *KDD*.
7. Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*.
8. Davies, D. L., & Bouldin, D. W. (1979). A cluster separation measure. *IEEE Transactions on Pattern Analysis and Machine Intelligence*.
9. Caliński, T., & Harabasz, J. (1974). A dendrite method for cluster analysis. *Communications in Statistics*.
10. Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. *SODA*.
11. Tài liệu thư viện dùng để đối chứng kết quả: scikit-learn (chỉ dùng trong script kiểm chứng, không dùng trong notebook và demo).

# 11. Phụ lục

<!-- Phụ trách: Hà Mạnh Trường -->

## 11.1. Cấu trúc mã nguồn

| Thư mục hoặc tệp | Nội dung |
| data/raw/ | Dữ liệu gốc năm tệp CSV |
| data/interim/ | Bảng dữ liệu trung gian sau tiền xử lý |
| data/processed/ | Kết quả gom cụm, chân dung cụm và bảng dịch chuyển cụm |
| notebooks/ | Bốn notebook chạy theo thứ tự 01 đến 04 |
| src/ | Module nạp dữ liệu, biến đổi đặc trưng, thuật toán gom cụm và trực quan hóa |
| scripts/ | Script kiểm chứng thuật toán tự viết so với thư viện |
| app/ | Ứng dụng demo Streamlit |
| reports/tables/ | Bảng số liệu dùng làm nguồn cho báo cáo |
| reports/figures/ | Hình ảnh phân giải cao chèn vào báo cáo |
| models/ | Tâm cụm, tham số chuẩn hóa và metric lưu dạng JSON |

## 11.2. Cách chạy lại toàn bộ

1. Tạo môi trường ảo và cài đặt thư viện theo `requirements.txt`.
2. Chạy lần lượt bốn notebook trong `notebooks/` từ 01 đến 04.
3. Chạy `python scripts/verify_scratch_implementations.py` để kiểm chứng thuật toán tự viết.
4. Chạy `streamlit run app/app.py` để mở demo.
5. Chạy `python reports/final_report/build_report.py` để sinh lại báo cáo Word này.

## 11.3. Bảng số liệu đầy đủ

Danh sách đầy đủ các bảng số liệu và tham số cấu hình nằm trong thư mục `reports/tables/`.

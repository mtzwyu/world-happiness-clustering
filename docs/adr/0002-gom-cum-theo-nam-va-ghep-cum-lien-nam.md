# 0002. Gom cụm độc lập theo từng năm và ghép cụm liên năm bằng ghép tham lam

Dự án chạy năm thí nghiệm gom cụm **độc lập** cho từng năm 2015-2019 thay vì gộp cả năm năm thành một bảng rồi gom một lần, vì mục tiêu của đề tài là mô tả cấu trúc phân nhóm quốc gia trong từng năm và theo dõi xu hướng dịch chuyển nhóm. Do mỗi năm gom cụm riêng nên nhãn cụm không so sánh trực tiếp được giữa các năm; dự án ghép cụm của hai năm liền kề bằng **ghép tham lam theo khoảng cách tâm cụm nhỏ nhất**, hoà thì xét điểm hạnh phúc trung bình, và giữ **cấu hình ba cụm làm đối chứng xuyên năm**.

## Status

Accepted

## Considered Options

- **Gộp cả năm năm thành một bảng rồi gom một lần**: chỉ có một mô hình duy nhất nên dễ diễn giải, nhưng mỗi quốc gia xuất hiện năm lần nên cụm bị chi phối bởi năm có nhiều dữ liệu, và mất khả năng theo dõi dịch chuyển nhóm.
- **Gom trên năm 2019 rồi gán nhãn cho các năm còn lại**: nhẹ nhất về tính toán, nhưng không phải năm thí nghiệm song song và giả định sai rằng cấu trúc cụm không đổi theo thời gian.
- **Ghép cụm tối ưu kiểu Hungarian**: chính xác hơn về mặt gán cặp nhưng phức tạp không cần thiết cho chỉ 2-5 cụm mỗi năm.

## Consequences

- Mọi so sánh theo thời gian phải ghi rõ cỡ mẫu từng năm (158, 157, 155, 156, 156), và chỉ so sánh được phần nhỏ hơn khi số cụm tối ưu lệch nhau giữa hai năm.
- Cần thêm hàm ghép cụm trong `src/models/clustering.py` và bảng kết quả ghép ở `reports/tables/cross_year_matching.csv`.
- Cấu hình ba cụm trở thành cấu hình duy nhất so sánh được xuyên năm, nên nó phải luôn được chạy song song với số cụm tối ưu.

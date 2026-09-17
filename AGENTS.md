# Hướng Dẫn Dành Cho AI Agent (AGENTS.md)

Tài liệu này chứa các quy tắc bắt buộc, phong cách lập trình và cấu hình kỹ năng cho các AI agent hoạt động trong repository **data_mining** (Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc - World Happiness Report).

---

## 🎯 Các Quy Tắc Cốt Lõi Của Dự Án (Project Rules)

1. **Mục tiêu học tập (Learning-First / From Scratch):**
   - Dự án phục vụ mục tiêu học tập và bảo vệ đồ án của sinh viên.
   - **Bắt buộc tự code thuật toán:** Thuật toán gom cụm (K-Means, Hierarchical Clustering) và các độ đo đánh giá (khoảng cách Euclidean, WCSS/Inertia, Silhouette Score) phải được tự cài đặt logic từ đầu (*from scratch*).
   - **Tuyệt đối KHÔNG** gọi các hàm black-box có sẵn như `sklearn.cluster.KMeans` làm kết quả chính của bài toán.

2. **Quy định về thư viện và hàm cơ bản:**
   - **Được phép dùng `pandas` và `numpy`:** Dùng cho việc đọc dữ liệu, thao tác DataFrame, mảng và các phép toán số học cơ bản (`np.mean`, `np.sum`, `np.sqrt`, `np.min`, `np.max`, `np.abs`, v.v.).
   - Tránh các hàm ma trận phức tạp hoặc cú pháp nâng cao khó diễn giải. Ưu tiên code rõ ràng, có chú thích giải thích công thức toán học để sinh viên dễ hiểu và tự tin trả lời vấn đáp trước giảng viên.

3. **Tuân thủ trọn vẹn 11 bước Pipeline bắt buộc (Mục 1.2):**
   - Bất kỳ phân tích hay triển khai nào đều phải bám sát theo 11 bước quy định trong đề cương môn học (từ Xác định bài toán -> Hiểu dữ liệu -> Tiền xử lý -> EDA -> Biến đổi -> Huấn luyện thuật toán -> So sánh phương án -> Diễn giải tri thức -> Demo tương tác -> Kết luận & Hạn chế).

4. **Quy tắc vàng của Đề tài 16 (World Happiness Report):**
   - Tuyệt đối **KHÔNG** đưa thuộc tính `Happiness Score` hay `Happiness Rank` vào ma trận đặc trưng $X$ để gom cụm.
   - Gom cụm hoàn toàn dựa trên 6 yếu tố cơ sở: `GDP per capita`, `Social support`, `Healthy life expectancy`, `Freedom`, `Generosity`, `Perceptions of corruption`.
   - Chỉ sử dụng `Happiness Score` ở bước 9 (Notebook 04) để hậu kiểm và đối chiếu xem các cụm tự nhiên có sự phân hóa điểm số thực tế ra sao.

---

## 🛠️ Agent skills

### Issue tracker

Issues and specs are tracked as local markdown files in `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical triage label roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repository layout (`CONTEXT.md` and `docs/adr/` at the root). See `docs/agents/domain.md`.

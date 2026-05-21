# 🎬 BÀI TẬP LỚN: ỨNG DỤNG PHÂN TÍCH DỮ LIỆU PHIM & DOANH THU

Ứng dụng Dashboard trực quan hóa số liệu được xây dựng bằng ngôn ngữ **Python** và thư viện **Streamlit**. Hệ thống hỗ trợ xử lý, phân tích tự động dữ liệu từ tệp nguồn để phục vụ cho việc thống kê, quản lý các chỉ số kinh doanh và phân bổ người dùng.

---

## 👥 Thông Tin Nhóm Thực Hiện
* **Thành viên 1:** [Hoàng Nguyễn Khánh Linh] - [B25DCKT055]
* **Môn học:** KTDL và AI cho kế toán

---

## 📌 Các Tính Năng Chính Của Ứng Dụng

Hệ thống Dashboard cung cấp giao diện quản trị trực quan với các cấu phần chính:

### 1. Thống kê tổng quan dữ liệu (Metrics)
* **Người dùng:** Tổng hợp số lượng tài khoản người dùng có trên hệ thống.
* **Phim:** Thống kê tổng số lượng đầu phim đang quản lý.
* **Đánh giá trung bình:** Tính toán điểm số rating trung bình của phim (định dạng làm tròn 2 chữ số thập phân).
* **Doanh thu gói:** Tổng doanh thu tích lũy từ các gói đăng ký dịch vụ (hiển thị định dạng tiền tệ VND).

### 2. Biểu đồ trực quan hóa (Charts)
* **Biểu đồ phân bố điểm đánh giá:** Trực quan hóa số lượng đánh giá theo từng thang điểm.
* **Biểu đồ số lượng phim theo thể loại:** Thống kê và so sánh tỷ trọng phim giữa các thể loại khác nhau.
* **Biểu đồ tỷ lệ gói đăng ký:** Phân tích cấu trúc các gói dịch vụ được người dùng lựa chọn nhiều nhất.
* **Biểu đồ doanh thu theo gói:** So sánh đóng góp tài chính thực tế của từng gói dịch vụ vào tổng doanh thu.

### 3. Tra cứu chi tiết
* Tích hợp công cụ mở rộng dữ liệu (`st.expander`) cho phép xem thông tin chi tiết và cụ thể về danh sách người dùng một cách khoa học mà không làm ảnh hưởng đến bố cục tổng thể của Dashboard.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
Baitaplon/
├── app.py          # File chứa mã nguồn xử lý logic và giao diện Streamlit
├── movies.csv      # File cơ sở dữ liệu (chứa thông tin phim, tài khoản, doanh thu)
└── README.md       # Tài liệu hướng dẫn sử dụng và cài đặt dự án
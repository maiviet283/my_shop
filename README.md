# 🛍 CLOTHING SHOP API

![Django](https://img.shields.io/badge/Django-4.x-green?style=flat&logo=django)
![DRF](https://img.shields.io/badge/DRF-API-red?style=flat&logo=django)
![JWT](https://img.shields.io/badge/JWT-Authentication-yellow?style=flat&logo=jsonwebtokens)
![Jazzmin](https://img.shields.io/badge/Admin-Jazzmin-blue?style=flat&logo=django)
![Redis](https://img.shields.io/badge/Redis-Cache-red?style=flat&logo=redis)
![Google OAuth](https://img.shields.io/badge/Google%20OAuth-Authentication-blue?style=flat&logo=google)

---

## 📌 Giới Thiệu

**Clothing Shop API** là hệ thống backend mạnh mẽ cho một cửa hàng quần áo trực tuyến, được xây dựng bằng **Django Rest Framework (DRF)**. Hệ thống hỗ trợ quản lý sản phẩm, đơn hàng, giỏ hàng, đánh giá sản phẩm và tích hợp thanh toán. API sử dụng **JWT Authentication** để đảm bảo bảo mật cho người dùng. Giao diện **Admin Django** được cải tiến bằng **Jazzmin**, mang lại trải nghiệm quản lý mượt mà và chuyên nghiệp.

Ngoài ra, hệ thống có thêm **Middleware chống spam & DDoS nhẹ**, cùng với **Django Axes** giúp bảo vệ đăng nhập trước tấn công brute-force. Đặc biệt, **Redis** được tích hợp để **tăng tốc độ xử lý dữ liệu và caching**, giúp cải thiện hiệu suất API.

---

## 🚀 Công Nghệ Sử Dụng

- 🐍 **Django 5.x** - Framework chính.
- 🔥 **Django Rest Framework (DRF)** - Xây dựng API RESTful.
- 🌐 **Google OAuth 2.0** - Đăng nhập bằng tài khoản Google.
- 🔑 **JWT Authentication** - Bảo mật và xác thực người dùng.
- 🎨 **Jazzmin Admin** - Tối ưu giao diện quản trị.
- 🛒 **SQLite / PostgreSQL / MySQL** - Cơ sở dữ liệu.
- 🚀 **Redis** - Caching và tăng tốc API.
- 🛡 **Middleware chống spam/DDoS** - Hạn chế request spam.
- 🚫 **Django Axes** - Ngăn chặn brute-force đăng nhập.

---

## 📦 Chức Năng Chính

| Chức Năng               | Mô Tả |
|--------------------------|--------------------------------------------------------------------------------------------------|
| **🔑 Xác Thực Người Dùng** | Đăng ký, đăng nhập, quên mật khẩu với **JWT**. Hỗ trợ phân quyền **Khách hàng / Nhân viên / Quản trị viên**. |
| **🛡 Bảo Mật** | **Middleware chống spam/DDoS**, **Django Axes** bảo vệ đăng nhập. Giới hạn số lần đăng nhập sai. |
| **🛍 Quản Lý Sản Phẩm** | CRUD sản phẩm, hỗ trợ **tải lên nhiều hình ảnh** và bộ lọc theo danh mục, giá, màu sắc, kích thước. |
| **🛒 Giỏ Hàng & Thanh Toán** | Thêm/Xóa sản phẩm vào giỏ hàng, tạo đơn hàng, thanh toán **COD / Thẻ tín dụng / PayPal**. |
| **⭐ Đánh Giá & Bình Luận** | Hệ thống đánh giá sản phẩm **(1-5 sao)**, bình luận và phản hồi. |
| **📦 Quản Lý Đơn Hàng** | Xem lịch sử mua hàng, nhân viên cập nhật trạng thái đơn hàng, tìm kiếm & lọc đơn hàng theo tiêu chí. |
| **🎛 Trang Admin Django** | Giao diện **Jazzmin** giúp quản trị dễ dàng, hỗ trợ tìm kiếm, lọc dữ liệu nhanh chóng. |
| **🚀 Hiệu Suất & Redis** | **Redis** giúp caching và tăng tốc API, giảm tải cơ sở dữ liệu. |
| **🌐 Đăng Nhập Google OAuth 2.0** | Đăng nhập nhanh chóng và dễ dàng thông qua tài khoản Google. |
| **📧 Thông Báo Qua Email** | Khi xem thông tin cá nhân thông báo sẽ được gửi về email. |
---

## 🛠 Cài Đặt & Chạy Dự Án

### Yêu Cầu Hệ Thống

- Python 3.10+
- PostgreSQL/MySQL (hoặc SQLite cho phát triển cục bộ)
- Redis

### Cài Đặt Redis

- **Tải Redis:** [Redis for Windows](https://github.com/tporadowski/redis/releases/latest)
- **Giải nén Redis** vào thư mục mong muốn.
- **Chạy Redis Server Trên CMD Thư Mục Đó:**
  ```bash
  redis-server
  ```

### Cài Đặt Dự Án

```bash
# Clone repository
git clone https://github.com/maiviet283/my_shop.git
cd my_shop

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate    # Trên Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Thiết lập database
python manage.py migrate

# Chạy server
python manage.py runserver
```

**🚀 Giờ đây, bạn có thể truy cập tại: http://127.0.0.1:8000 🎯** 🎉

---

## 📜 Hướng Dẫn Triển Khai (Deploy)

Hệ thống đã có hướng dẫn triển khai chi tiết lên **Nginx & Gunicorn**, kèm theo hình ảnh minh họa. Vui lòng tham khảo file:

- **[Deploy_Nginx.docx](./Deploy_Nginx.docx)** – Hướng dẫn triển khai với hình ảnh minh họa.  
- **[Deploy_Nginx.md](./Deploy_Nginx.md)** – Phiên bản markdown dành cho lập trình viên.  
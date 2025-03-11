# 🛍 CLOTHING SHOP API

![Django](https://img.shields.io/badge/Django-4.x-green?style=flat&logo=django)
![DRF](https://img.shields.io/badge/DRF-API-red?style=flat&logo=django)
![JWT](https://img.shields.io/badge/JWT-Authentication-yellow?style=flat&logo=jsonwebtokens)
![Jazzmin](https://img.shields.io/badge/Admin-Jazzmin-blue?style=flat&logo=django)

---

## 📌 Giới Thiệu

![E-commerce](https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif)

**Clothing Shop API** là hệ thống backend mạnh mẽ cho một cửa hàng quần áo trực tuyến, được xây dựng bằng **Django Rest Framework (DRF)**. Hệ thống hỗ trợ quản lý sản phẩm, đơn hàng, giỏ hàng, đánh giá sản phẩm và tích hợp thanh toán. API sử dụng **JWT Authentication** để đảm bảo bảo mật cho người dùng. Giao diện **Admin Django** được cải tiến bằng **Jazzmin**, mang lại trải nghiệm quản lý mượt mà và chuyên nghiệp.

---

## 🚀 Công Nghệ Sử Dụng

- 🐍 **Django 4.x** - Framework chính.
- 🔥 **Django Rest Framework (DRF)** - Xây dựng API RESTful.
- 🔑 **JWT Authentication** - Bảo mật và xác thực người dùng.
- 🎨 **Jazzmin Admin** - Tối ưu giao diện quản trị.
- 🛒 **SQLite / PostgreSQL / MySQL** - Cơ sở dữ liệu.

---

## 📦 Chức Năng Chính

### 🎯 **Người Dùng & Xác Thực**

✔ Đăng ký, đăng nhập, quên mật khẩu bằng **JWT**.  
✔ Phân quyền: **Khách hàng / Nhân viên / Quản trị viên**.  
✔ Xác thực token JWT giúp API an toàn hơn.  

![Login GIF](https://media.giphy.com/media/Ll22OhMLAlVDb8UQWe/giphy.gif)

### 🛍 **Quản Lý Sản Phẩm**

✔ CRUD danh mục, sản phẩm.  
✔ Hỗ trợ tải lên **nhiều hình ảnh**.  
✔ Bộ lọc theo danh mục, giá, màu sắc, kích thước.  

![Product GIF](https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif)

### 🛒 **Giỏ Hàng & Thanh Toán**

✔ Thêm/Xóa sản phẩm vào giỏ hàng.  
✔ Tạo đơn hàng & cập nhật trạng thái.  
✔ Hỗ trợ thanh toán **COD / Thẻ tín dụng / PayPal**.  

![Checkout GIF](https://media.giphy.com/media/26xBwdIuRJiAIqHwA/giphy.gif)

### ⭐ **Đánh Giá & Bình Luận**

✔ Khách hàng có thể đánh giá sản phẩm **(1-5 sao)**.  
✔ Hệ thống bình luận & phản hồi.  

![Rating GIF](https://media.giphy.com/media/3oEjHGrVGrqgFFknfO/giphy.gif)

### 📦 **Quản Lý Đơn Hàng**

✔ Xem lịch sử mua hàng.  
✔ Nhân viên cập nhật trạng thái đơn hàng.  
✔ Tìm kiếm & lọc đơn hàng theo nhiều tiêu chí.  

![Order GIF](https://media.giphy.com/media/3ov9jNziFTMfzSumAw/giphy.gif)

### 🎛 **Trang Admin Django**

✔ Giao diện **Jazzmin** giúp quản trị dễ dàng.  
✔ Hỗ trợ tìm kiếm, lọc dữ liệu nhanh chóng.  
✔ Quản lý sản phẩm, đơn hàng, người dùng chuyên nghiệp.  

![Admin Panel GIF](https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif)

---

## 🛠 Cài Đặt & Chạy Dự Án

### Yêu Cầu Hệ Thống

- Python 3.8+
- PostgreSQL/MySQL (hoặc SQLite cho phát triển cục bộ)

### Cài Đặt

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

🚀 **🚀 Giờ đây, bạn có thể truy cập tại: http://127.0.0.1:8000 🎯** 🎉


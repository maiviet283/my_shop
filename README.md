# 🛍 CLOTHING SHOP API - Django Backend

![Django](https://img.shields.io/badge/Django-4.x-green?style=flat&logo=django)
![DRF](https://img.shields.io/badge/DRF-API-red?style=flat&logo=django)
![JWT](https://img.shields.io/badge/JWT-Authentication-yellow?style=flat&logo=jsonwebtokens)
![Jazzmin](https://img.shields.io/badge/Admin-Jazzmin-blue?style=flat&logo=django)

## 📌 Giới thiệu
Dự án **Clothing Shop API** là hệ thống backend cho một shop quần áo, cung cấp API mạnh mẽ sử dụng **Django Rest Framework (DRF)** và **JWT Authentication** để xác thực khách hàng.  
Trang **Admin Django** được tối ưu và làm đẹp bằng **Jazzmin**, giúp quản lý sản phẩm, đơn hàng, người dùng một cách trực quan và chuyên nghiệp.  

---

## 🚀 Công nghệ sử dụng
- 🐍 **Django 4.x** - Framework chính.
- 🔥 **Django Rest Framework (DRF)** - Xây dựng API RESTful.
- 🔑 **JWT Authentication** - Xác thực người dùng khách hàng.
- 🎨 **Jazzmin Admin** - Giao diện Admin thân thiện và đẹp mắt.
- 🛒 **PostgreSQL/MySQL** - Lưu trữ dữ liệu.
- ☁ **Cloudinary** (hoặc S3) - Lưu trữ hình ảnh sản phẩm (nếu cần).

---

## 📦 Chức năng chính
### 🎯 **Người dùng & Xác thực**
✔ Đăng ký, đăng nhập, quên mật khẩu (JWT).  
✔ Phân quyền: **Khách hàng / Nhân viên / Admin**.  
✔ Xác thực JWT cho API bảo mật.  

### 🛍 **Quản lý Sản phẩm**
✔ CRUD danh mục, sản phẩm.  
✔ Hỗ trợ tải lên nhiều hình ảnh.  
✔ Bộ lọc theo danh mục, giá, màu sắc, kích thước.  

### 🛒 **Giỏ hàng & Thanh toán**
✔ Thêm/Xóa sản phẩm vào giỏ hàng.  
✔ Tạo đơn hàng & cập nhật trạng thái đơn hàng.  
✔ Thanh toán qua **COD / Credit Card / PayPal**.  

### ⭐ **Đánh giá sản phẩm**
✔ Khách hàng có thể đánh giá (1-5 sao).  
✔ Hệ thống bình luận sản phẩm.  

### 📦 **Quản lý Đơn hàng**
✔ Lịch sử mua hàng cho khách.  
✔ Nhân viên quản lý trạng thái đơn hàng.  

### 🎛 **Trang Admin Django**
✔ Jazzmin UI giúp Admin dễ dàng quản lý dữ liệu.  
✔ Tìm kiếm, lọc đơn hàng, sản phẩm nhanh chóng.  
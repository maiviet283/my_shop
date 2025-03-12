# Hướng Dẫn Triển Khai Django với Nginx và Gunicorn trên Ubuntu

## **1. Tạo User mới trên Ubuntu**
Trước tiên, tạo một user mới để quản lý ứng dụng Django.
```bash
sudo adduser maiviet
```

### **Cấp quyền sudo cho user mới:**
```bash
sudo usermod -aG sudo maiviet
```

### **Chuyển sang user mới:**
```bash
su - maiviet
```

---
## **2. Cài đặt các gói cần thiết**
Cập nhật hệ thống và cài đặt các gói yêu cầu:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
pip install gunicorn
```

---
## **3. Clone và Cấu hình Dự án Django**
### **Clone code từ GitHub:**
```bash
git clone https://github.com/maiviet283/my_shop.git
cd my_shop/
```

### **Tạo Virtual Environment và cài đặt dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---
## **4. Cấu hình Static Files và cấp quyền**
### **Chạy collectstatic để thu thập file tĩnh:**
```bash
python3 manage.py collectstatic
```

### **Cấp quyền truy cập cho thư mục staticfiles:**
```bash
sudo chmod -R 755 /home/maiviet/my_shop/staticfiles
sudo chown -R www-data:www-data /home/maiviet/my_shop/staticfiles
```

---
## **5. Cấu hình Gunicorn để chạy Django**
### **Tạo file `gunicorn.socket`**
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
Thêm nội dung:
```ini
[Unit]
Description=Gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### **Tạo file `gunicorn.service`**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Thêm nội dung:
```ini
[Unit]
Description=Gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=maiviet
Group=www-data
WorkingDirectory=/home/maiviet/my_shop
ExecStart=/home/maiviet/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          my_shop.wsgi:application

[Install]
WantedBy=multi-user.target
```

### **Tải lại Systemd và khởi động Gunicorn**
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service
```

### **Kiểm tra trạng thái Gunicorn**
```bash
sudo systemctl status gunicorn.service
```

---
## **6. Cấu hình Nginx để phục vụ Django**
### **Tạo file cấu hình Nginx**
```bash
sudo nano /etc/nginx/sites-available/my_shop
```
Thêm nội dung:
```nginx
server {
    listen 80;
    server_name 192.168.233.161;  # Thay bằng IP của máy

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/maiviet/my_shop/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Cache-Control "no-store";
    }
}
```

### **Kích hoạt file cấu hình cho Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/my_shop /etc/nginx/sites-enabled/
```

### **Kiểm tra cấu hình Nginx**
```bash
sudo nginx -t
```
Nếu không có lỗi, khởi động lại Nginx:
```bash
sudo systemctl restart nginx
```

---
## **7. Cấp quyền và Kiểm tra Socket Gunicorn**
### **Kiểm tra socket của Gunicorn**
```bash
ls -l /run/gunicorn.sock
```
Nếu không tồn tại, chạy lại Gunicorn:
```bash
sudo systemctl restart gunicorn
```

### **Cấp quyền cho Gunicorn socket**
```bash
sudo chown www-data:www-data /run/gunicorn.sock
sudo chmod 666 /run/gunicorn.sock
```

---
## **8. Cấu hình quyền truy cập**
```bash
sudo chmod 755 /home/maiviet
sudo find /home/maiviet/my_shop/staticfiles/ -type f -exec chmod 644 {} \;
sudo find /home/maiviet/my_shop/staticfiles/ -type d -exec chmod 755 {} \;
```

---
## **9. Khởi động lại Nginx và Gunicorn**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### **Truy cập vào website để kiểm tra**
Mở trình duyệt và truy cập:
```
http://192.168.233.161/
```
Nếu trang Django hiển thị, nghĩa là deploy thành công! 🚀


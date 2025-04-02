Dưới đây là hướng dẫn chi tiết triển khai Django với Nginx theo tài liệu của bạn:

---

# **Triển khai Django với Nginx và Gunicorn trên Ubuntu**
## **1. Tạo user mới và cấp quyền sudo**
```sh
sudo adduser maiviet
sudo usermod -aG sudo maiviet
su - maiviet
```

## **2. Cập nhật và cài đặt các gói cần thiết**
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
```

## **3. Clone mã nguồn từ Git**
```sh
git clone https://github.com/maiviet283/my_shop.git
```

## **4. Thiết lập môi trường ảo và cài đặt dependencies**
```sh
python3 -m venv venv
source venv/bin/activate
cd my_shop/
pip install -r requirements.txt
```

## **5. Tạo và cấp quyền thư mục tĩnh**
```sh
python3 manage.py collectstatic
sudo chmod -R 755 /home/maiviet/my_shop/staticfiles
sudo chown -R www-data:www-data /home/maiviet/my_shop/staticfiles
```

---

# **Cấu hình Gunicorn**
## **6. Tạo file Gunicorn socket**
```sh
sudo nano /etc/systemd/system/gunicorn.socket
```
**Nội dung:**
```
[Unit]
Description=Gunicorn socket for Django

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

## **7. Tạo file Gunicorn service**
```sh
sudo nano /etc/systemd/system/gunicorn.service
```
**Nội dung:**
```
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

## **8. Tải lại và chạy Gunicorn**
```sh
sudo systemctl daemon-reload
sudo systemctl start gunicorn.service
sudo systemctl status gunicorn.service
```

---

# **Cấu hình Nginx**
## **9. Tạo file cấu hình cho Nginx**
```sh
sudo nano /etc/nginx/sites-available/my_shop
```
**Nội dung:**
```
server {
    listen 80;
    server_name 192.168.233.161;  # Thay bằng IP của bạn

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/maiviet/my_shop/staticfiles/;
    }

    location /media/ {
        alias /home/maiviet/my_shop/media/;
        autoindex on;
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

## **10. Áp dụng cấu hình Nginx**
```sh
sudo ln -s /etc/nginx/sites-available/my_shop /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## **11. Kiểm tra file socket của Gunicorn**
```sh
ls -l /run/gunicorn.sock
```
Nếu file tồn tại, nghĩa là Gunicorn đang chạy đúng.

---

# **Cấp quyền và kiểm tra hoạt động**
## **12. Cấp quyền truy cập**
```sh
sudo chmod 755 /home/maiviet
sudo find /home/maiviet/my_shop/staticfiles/ -type f -exec chmod 644 {} \;
sudo find /home/maiviet/my_shop/staticfiles/ -type d -exec chmod 755 {} \;
```

## **13. Khởi động lại Nginx**
```sh
sudo systemctl restart nginx
```

## **14. Kiểm tra hoạt động**
Mở trình duyệt và truy cập:
```
http://192.168.233.161/
```
Nếu thấy trang web chạy, bạn đã triển khai thành công! 🚀
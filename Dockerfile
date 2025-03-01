# Sử dụng Python image
FROM python:3.10

# Đặt thư mục làm việc
WORKDIR /app

# Copy các file vào container
COPY . .

# Cài đặt dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Chạy migrations và collectstatic
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Chạy ứng dụng với Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "my_shop.wsgi:application"]

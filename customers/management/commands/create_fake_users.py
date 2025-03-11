from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from customers.models import CustomerUser
from orders.models import Cart

class Command(BaseCommand):
    help = "Tạo nhiều tài khoản khách hàng ngẫu nhiên"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Số lượng tài khoản cần tạo')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        created_count = 0  # Đếm số user đã tạo

        while created_count < total:
            username = fake.user_name()
            email = fake.email()
            phone_number = f"+849{random.randint(10000000, 99999999)}"
            full_name = fake.name()
            password = make_password("password123")
            gender = random.choice(["male", "female", "other"])

            # Kiểm tra trùng lặp trước khi tạo
            if CustomerUser.objects.filter(username=username).exists():
                continue  # Bỏ qua nếu username đã tồn tại

            if CustomerUser.objects.filter(email=email).exists():
                continue  # Bỏ qua nếu email đã tồn tại

            if CustomerUser.objects.filter(phone_number=phone_number).exists():
                continue  # Bỏ qua nếu số điện thoại đã tồn tại

            # Nếu không trùng thì tạo user
            user = CustomerUser.objects.create(
                username=username,
                email=email,
                phone_number=phone_number,
                full_name=full_name,
                password=password,
                gender=gender,
                date_joined=timezone.now(),
            )

            # Tạo giỏ hàng tương ứng
            Cart.objects.create(user=user)

            self.stdout.write(self.style.SUCCESS(f"Đã tạo user: {user.username} và giỏ hàng tương ứng"))
            created_count += 1  # Cập nhật số lượng đã tạo

import threading
from django.core.mail import send_mail
from django.utils.timezone import localtime, now
from django.conf import settings


def send_profile_view_email(user):
    if not user.email:
        print("[Email Warning] Người dùng không có địa chỉ email.")
        return

    current_time = localtime(now()).strftime("%H:%M:%S, ngày %d/%m/%Y")

    subject = "Bạn vừa xem thông tin tài khoản"
    message = f"""Chào {user.full_name or user.username},

Bạn vừa xem thông tin tài khoản của mình lúc {current_time}.

🔐 Thông tin tài khoản của bạn:
- Họ tên: {user.full_name or 'Chưa có'}
- Email: {user.email}
- Số điện thoại: {user.phone_number or 'Chưa có'}
- Ngày sinh: {user.date_of_birth or 'Chưa cập nhật'}
- Địa chỉ: {user.address or 'Chưa cập nhật'}
- Giới tính: {user.get_gender_display() if user.gender else 'Chưa cập nhật'}
- Tên đăng nhập: {user.username}
- Ngày tạo tài khoản: {user.date_joined.strftime('%d/%m/%Y')}

Trân trọng,
{settings.DEFAULT_FROM_EMAIL}
"""

    try:
        result = send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Sẽ dùng DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False
        )
        if result == 1:
            print(f"[Email Success] Đã gửi email đến {user.email}")
        else:
            print(f"[Email Failure] Không thể gửi email đến {user.email}")
    except Exception as e:
        print(f"[Email Error] Gửi email thất bại: {e}")


def send_profile_view_email_async(user):
    threading.Thread(target=send_profile_view_email, args=(user,)).start()

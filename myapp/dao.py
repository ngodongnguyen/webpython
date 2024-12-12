import json
from myapp.models import NguoiDung
def get_user_by_username_or_email(username_or_email):
    # Giả sử có một hàm để tìm kiếm người dùng theo tên tài khoản hoặc email
    user = NguoiDung.query.filter((NguoiDung.username == username_or_email) | (NguoiDung.email == username_or_email)).first()
    return user


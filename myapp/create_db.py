# create_db.py
from myapp import create_app, db
from myapp.models import NguoiDung

# app = create_app()

# # Tạo tất cả các bảng theo mô hình đã định nghĩa
# with app.app_context():
#     db.create_all()

#     # Thêm một user mẫu vào cơ sở dữ liệu
#     new_user = NguoiDung(username='john_doe', email='john@example.com')

#     # Lưu đối tượng vào cơ sở dữ liệu
#     db.session.add(new_user)
#     db.session.commit()

#     # Kiểm tra dữ liệu đã được thêm hay chưa
#     users = NguoiDung.query.all()  # Truy vấn tất cả user
#     print("All Users in the Database:")
#     for user in users:
#         print(f"Username: {user.username}, Email: {user.email}")

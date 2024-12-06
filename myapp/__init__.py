from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cấu hình kết nối cơ sở dữ liệu MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ngodongnguyen2004?@localhost/PhongY'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Khởi tạo SQLAlchemy với app
    db.init_app(app)

    # Import models để tạo bảng
    from myapp.models import NguoiDung, BacSi, BenhNhan, YTa

    # Tạo các bảng trong cơ sở dữ liệu (Chỉ dùng khi phát triển)
    with app.app_context():
        db.create_all()  # Tạo bảng từ tất cả các mô hình đã định nghĩa

    # Chuyển import vào trong hàm để tránh import vòng
    from myapp import routes
    app.register_blueprint(routes.bp)

    return app

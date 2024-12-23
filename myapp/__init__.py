from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
import os
import cloudinary
from flask_migrate import Migrate
# from myapp import HomeView, StatisticView
secret_key = os.urandom(24)  # Tạo một chuỗi ngẫu nhiên dài 24 byte
# Khởi tạo SQLAlchemy
db = SQLAlchemy()
migrate = Migrate(db)
CLOUD_NAME = 'ouweb'
API_KEY = '899316619339996'
API_SECRET = 'gXGG4apFKY4xJ7xRk0UM2WAdGyA'
cloudinary.config(cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET,secure=True)
def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    # Cấu hình kết nối cơ sở dữ liệu MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ngodongnguyen2004?@localhost/PhongY'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # Khởi tạo SQLAlchemy với app
    db.init_app(app)
    from myapp import models  # Import models after app and db are initialized
    # Tạo các bảng trong cơ sở dữ liệu (Chỉ dùng khi phát triển)
    with app.app_context():
        db.create_all()  # Tạo bảng từ tất cả các mô hình đã định nghĩa

    # Chuyển import vào trong hàm để tránh import vòng
    from myapp import routes
    app.register_blueprint(routes.bp)

    return app

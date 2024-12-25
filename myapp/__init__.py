from flask import Flask
import os
import cloudinary
from myapp.extensions import db, migrate
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Cloudinary config
CLOUD_NAME = 'ouweb'
API_KEY = '899316619339996'
API_SECRET = 'gXGG4apFKY4xJ7xRk0UM2WAdGyA'
cloudinary.config(cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET, secure=True)

# Secret key
secret_key = os.urandom(24)

def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ngodongnguyen2004?@localhost/PhongY'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models (sau khi khởi tạo db)
    with app.app_context():
        from myapp.models import NhanVien  # Import model ở đây

        # Flask-Admin
        from myapp.view.admin.human.y_ta import NurseView
        admin = Admin(app, name="Phòng mạch", template_mode="bootstrap4")
        admin.add_view(NurseView(NhanVien, db.session, name="Quản lý Y tá"))

    # Đăng ký route (nếu có)
    from myapp import routes
    app.register_blueprint(routes.bp)

    return app

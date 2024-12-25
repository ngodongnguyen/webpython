from flask import Flask
import os
import cloudinary
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from myapp.extensions import db, migrate

# Cloudinary config
CLOUD_NAME = 'ouweb'
API_KEY = '899316619339996'
API_SECRET = 'gXGG4apFKY4xJ7xRk0UM2WAdGyA'
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
    secure=True
)

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:079204022585B%40o@localhost/PhongY'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models and initialize within app context
    with app.app_context():
        from myapp.models import NhanVien  # Import models

        # Flask-Admin setup
        from myapp.view.admin.human.y_ta import NurseView
        admin = Admin(app, name="Phòng mạch", template_mode="bootstrap4")
        admin.add_view(NurseView(NhanVien, db.session, name="Quản lý Y tá"))

        # Auto-create tables (optional, for development)
        db.create_all()

    # Register routes
    from myapp import routes
    app.register_blueprint(routes.bp)

    return app

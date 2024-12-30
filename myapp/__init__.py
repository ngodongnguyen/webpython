from flask import Flask
import os
import cloudinary
from flask_admin import Admin, AdminIndexView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from myapp.extensions import db, migrate
from myapp.view.home_view import HomeView
from flask_login import LoginManager
from myapp.models import NhanVien,YTa,BacSi,BenhNhan,Khoa,DangKyKham,Thuoc,PhieuKhamBenh,ThongKe,HoaDon,QuyDinh
from myapp.view.admin.human.y_ta import NurseView
from flask_admin.contrib.sqla import ModelView
from myapp.view.admin.human.nhan_vien import EmployeeView
from myapp.view.admin.human.bac_si import DoctorView
from myapp.view.admin.human.benh_nhan import BenhNhanView
from myapp.view.admin.khoa import KhoaView
from myapp.view.admin.main_usecase.dat_lich_kham import DangKyKhamView
from myapp.view.admin.category.thuoc import ThuocView
from myapp.view.admin.main_usecase.phieu_kham_benh import PhieuKhamBenhView
from myapp.view.admin.main_usecase.thong_ke import ThongKeView
from myapp.view.admin.main_usecase.hoa_don import HoaDonView
from myapp.view.admin.main_usecase.quy_dinh import QuyDinhView
class SimpleView(ModelView):
    pass

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return NhanVien.query.get(int(user_id))  # Trả về đối tượng người dùng dựa trên ID
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
app = Flask(__name__)
    
    # Configurations
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ngodongnguyen2004?@localhost/PhongY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)  # Liên kết LoginManager với app
admin = Admin(app, name="Phòng mạch", template_mode="bootstrap4", index_view=HomeView())

def create_app():
    

    # Import models and initialize within app context
    with app.app_context():
        from myapp.models import NhanVien  # Import models

        db.create_all()

    # Register routes
    from myapp import routes
    app.register_blueprint(routes.bp)

    return app
def initAdmin():
    try:
        admin.add_view(NurseView(YTa, db.session, name="Y tá",endpoint="yta"))
        print("Y tá view added successfully")
    except Exception as e:
        print(f"Error adding Y tá view: {e}")

    try:
        admin.add_view(DoctorView(BacSi, db.session, name="Bác Sĩ"))
        print("Doctor view added successfully")
    except Exception as e:
        print(f"Error adding Doctor view: {e}")
    admin.add_view(BenhNhanView(BenhNhan, db.session,name='Bệnh Nhân'))
    admin.add_view(KhoaView(Khoa, db.session, name='Quản lý khoa'))
    admin.add_view(DangKyKhamView(DangKyKham, db.session, name='Quản lý lịch khám'))
    admin.add_view(ThuocView(Thuoc, db.session,name='Thuốc'))
    admin.add_view(PhieuKhamBenhView(PhieuKhamBenh, db.session, name="Phiếu Khám Bệnh",endpoint='phieukhambenh'))
    admin.add_view(HoaDonView(HoaDon, db.session, name="Hóa Đơn"))
    admin.add_view(ThongKeView(name="Thống Kê", endpoint='thong_ke'))
    admin.add_view(QuyDinhView(QuyDinh, db.session, name="Quy Định", endpoint='quy_dinh'))

    print(f"Views in Admin: {[view.name for view in admin._views]}")





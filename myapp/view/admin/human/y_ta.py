from flask_admin.contrib.sqla import ModelView
from wtforms import validators, StringField, DateField, TelField, FileField
import cloudinary.uploader
from myapp.models import NhanVien, Sdt, DiaChi, Email
from myapp.extensions import db
from flask_admin import Admin
from myapp.view.home_view import HomeView


class NurseView(ModelView):
    # **1. Cấu hình hiển thị cột**
    column_list = [
        'id', 'ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'so_dien_thoai', 'dia_chi', 
        'email', 'type', 'avatar'
    ]
    column_labels = {
        'id': 'Mã y tá',
        'ho': 'Họ',
        'ten': 'Tên',
        'gioi_tinh': 'Giới tính',
        'ngay_sinh': 'Ngày sinh',
        'so_dien_thoai': 'Số điện thoại',
        'dia_chi': 'Địa chỉ',
        'email': 'Email',
        'type': 'Loại nhân viên',
        'avatar': 'Ảnh đại diện',
    }

    # **2. Cấu hình tìm kiếm**
    column_searchable_list = ['id', 'ho', 'ten']

    # **3. Cấu hình sắp xếp**
    column_sortable_list = ['id', 'ho', 'ten', 'ngay_sinh']

    # **4. Cấu hình bộ lọc**
    column_filters = [
        'gioi_tinh', 'ngay_sinh']

    # **5. Định nghĩa form cho dữ liệu**
    form_extra_fields = {
        'ngay_sinh': DateField('Ngày sinh', validators=[validators.DataRequired()]),
        'so_dien_thoai': TelField('Số điện thoại', validators=[validators.Length(min=10, max=11)]),
        'email': StringField('Email', validators=[validators.Email()]),
        'avatar': FileField('Ảnh đại diện'),
    }

    form_args = dict(
        ho=dict(validators=[validators.DataRequired(), validators.Length(max=100)]),
        ten=dict(validators=[validators.DataRequired(), validators.Length(max=100)]),
        dia_chi=dict(validators=[validators.DataRequired(), validators.Length(max=255)]),
    )

    # **6. Xử lý trước khi lưu dữ liệu**
    def on_model_change(self, form, model, is_created):
        # Upload avatar nếu có
        if form.avatar.data:
            upload_result = cloudinary.uploader.upload(form.avatar.data, folder='nurse_avatars')
            model.avatar = upload_result['secure_url']
        else:
            model.avatar = ''

    # **7. Cấu hình hiển thị các trường liên kết**
    column_list = ['ho', 'ten', 'gioi_tinh', 'ngay_sinh']

    # **8. Thêm cột tùy chỉnh cho giới tính**
    def _format_gender(view, context, model, name):
        return "Nam" if model.gioi_tinh else "Nữ"

    column_formatters = {
        'gioi_tinh': _format_gender,
    }
    
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from myapp.models import NhanVien
from myapp.extensions import db

class EmployeeView(ModelView):
    # 1. Hiển thị các cột trong bảng nhân viên
    column_list = ['id', 'ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'so_dien_thoai', 'dia_chi', 'email', 'type', 'avatar']

    # 2. Đặt nhãn cho các cột
    column_labels = {
        'id': 'Mã nhân viên',
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

    # 3. Tìm kiếm theo các cột
    column_searchable_list = ['id', 'ho', 'ten']

    # 4. Sắp xếp
    column_sortable_list = ['id', 'ho', 'ten', 'ngay_sinh']

    # 5. Bộ lọc
    column_filters = ['gioi_tinh', 'ngay_sinh', 'type']

    # 6. Tùy chỉnh giới tính hiển thị
    def _format_gender(view, context, model, name):
        return "Nam" if model.gioi_tinh else "Nữ"

    column_formatters = {
        'gioi_tinh': _format_gender,
    }

    # 7. Chỉ cho phép người dùng có quyền truy cập
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    # 8. Định nghĩa form để thêm/sửa nhân viên
    form_columns = ['ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'type', 'avatar']

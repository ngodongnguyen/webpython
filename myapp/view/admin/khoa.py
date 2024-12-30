from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from myapp.extensions import db
from myapp.models import Khoa, BacSi

class KhoaView(ModelView):
    # Các cột hiển thị trên giao diện quản trị
    column_list = ['id', 'ten_khoa', 'mo_ta', 'danh_sach_bac_si', 'so_luong_bac_si']

    # Nhãn hiển thị cho các cột
    column_labels = {
        'id': 'Mã khoa',
        'ten_khoa': 'Tên khoa',
        'mo_ta': 'Mô tả',
        'danh_sach_bac_si': 'Danh sách bác sĩ',
        'so_luong_bac_si': 'Số lượng bác sĩ'
    }

    # Các trường có thể tìm kiếm
    column_searchable_list = ['ten_khoa', 'mo_ta']

    # Các cột có thể sắp xếp
    column_sortable_list = ['id', 'ten_khoa']

    # Cấu hình form nhập liệu
    form_columns = ['ten_khoa', 'mo_ta']

    # Định nghĩa cột tùy chỉnh: Danh sách bác sĩ
    def _list_bac_si(view, context, model, name):
        """
        Hiển thị danh sách tên bác sĩ thuộc khoa.
        """
        if model.bac_sis:
            return ", ".join([f"{bac_si.ho} {bac_si.ten}" for bac_si in model.bac_sis])
        return "Không có bác sĩ"

    # Định nghĩa cột tùy chỉnh: Số lượng bác sĩ
    def _count_bac_si(view, context, model, name):
        """
        Hiển thị số lượng bác sĩ thuộc khoa.
        """
        return len(model.bac_sis)

    # Thêm formatter cho các cột
    column_formatters = {
        'danh_sach_bac_si': _list_bac_si,
        'so_luong_bac_si': _count_bac_si
    }

    # Xử lý quyền truy cập
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type in ['quan_tri']

    # Xử lý khi không có quyền truy cập
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))


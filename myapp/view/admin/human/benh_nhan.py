from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from myapp.extensions import db
from myapp.models import BacSi, Sdt, DiaChi, Email,NguoiDung,BenhNhan
from sqlalchemy import or_
from flask import request
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
import unicodedata
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from wtforms import StringField, PasswordField
from datetime import datetime,date

def validate_cccd(form, field):
    value = field.data
    if not value.startswith("079"):
        raise ValidationError("CCCD phải bắt đầu bằng '079'.")
    if len(value) != 12:
        raise ValidationError("CCCD phải có đúng 12 ký tự.")
def remove_accents(input_str):
    """
    Loại bỏ dấu tiếng Việt từ chuỗi.
    """
    if not input_str:  # Kiểm tra nếu chuỗi là None hoặc rỗng
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

class BenhNhanView(ModelView):
    form_columns = ['ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'cccd']

    # Đảm bảo sử dụng mối quan hệ trong `inline_models`
    inline_models = [
        (Sdt, dict(form_columns=['id', 'so_dien_thoai'])),
        (DiaChi, dict(form_columns=['id', 'dia_chi'])),
        (Email, dict(form_columns=['id', 'email']))
    ]
    
    # Sử dụng SelectField cho gioi_tinh, không gọi SelectField mà chỉ định lớp
    form_overrides = {
        'gioi_tinh': SelectField  # Dùng SelectField cho `gioi_tinh`
    }
    # Cập nhật form_choices để sử dụng SelectField
    form_choices = {
    'gioi_tinh': [(True, 'Nam'), (False, 'Nữ')]
}


    column_list = [
        'id', 'ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'cccd', 'so_dien_thoai', 'dia_chi', 'email'
    ]

    column_labels = {
        'id': 'Mã bác sĩ',
        'ho': 'Họ',
        'ten': 'Tên',
        'gioi_tinh': 'Giới tính',
        'ngay_sinh': 'Ngày sinh',
        'cccd': 'CCCD',
        'so_dien_thoai': 'Số điện thoại',
        'dia_chi': 'Địa chỉ',
        'email': 'Email',
    }

    column_searchable_list = [
        'ho', 'ten', 'cccd',  # Các cột từ bảng BenhNhan
        'so_dien_thoai_s.so_dien_thoai',  # Số điện thoại từ bảng liên kết
        'email_addresses.email',         # Email từ bảng liên kết
        'dia_chi_s.dia_chi'              # Địa chỉ từ bảng liên kết
    ]
    
    def get_query(self):
        """
        Override default query to add custom search behavior.
        """
        query = super(BenhNhanView, self).get_query()
        search_term = request.args.get('search')  # Lấy từ khóa tìm kiếm từ query string

        if search_term:  # Chỉ xử lý nếu có từ khóa tìm kiếm
            normalized_term = remove_accents(search_term)  # Loại bỏ dấu
            query = query.join(Sdt, BenhNhan.id == Sdt.nguoi_dung_id, isouter=True) \
                         .join(DiaChi, BenhNhan.id == DiaChi.nguoi_dung_id, isouter=True) \
                         .join(Email, BenhNhan.id == Email.nguoi_dung_id, isouter=True) \
                         .filter(
                             or_(
                                 BenhNhan.ho.ilike(f"%{search_term}%"),
                                 BenhNhan.ten.ilike(f"%{search_term}%"),
                                 BenhNhan.ho.ilike(f"%{normalized_term}%"),
                                 BenhNhan.ten.ilike(f"%{normalized_term}%"),
                                BenhNhan.cccd.ilike(f"%{search_term}%"),  # Tìm kiếm theo cccd
                                 Sdt.so_dien_thoai.ilike(f"%{search_term}%"),
                                 DiaChi.dia_chi.ilike(f"%{search_term}%"),
                                 Email.email.ilike(f"%{search_term}%")
                             )
                         )
            print(query.all())  # Debug dữ liệu

        return query




    def _format_phone(view, context, model, name):
        return ", ".join([sdt.so_dien_thoai for sdt in model.so_dien_thoai_s]) if model.so_dien_thoai_s else "N/A"

    def _format_address(view, context, model, name):
        return ", ".join([dia_chi.dia_chi for dia_chi in model.dia_chi_s]) if model.dia_chi_s else "N/A"

    def _format_email(view, context, model, name):
        return ", ".join([email.email for email in model.email_addresses]) if model.email_addresses else "N/A"
    form_args = {
    'gioi_tinh': {
        'label': 'Giới tính',
        'coerce': lambda x: x == '1',  # Chuyển đổi giá trị từ 1/0 sang Boolean
        'choices': [(True, 'Nam'), (False, 'Nữ')]
    }
}

    column_formatters = {
    'gioi_tinh': lambda v, c, m, n: "Nam" if m.gioi_tinh else "Nữ",
    'so_dien_thoai': _format_phone,
    'dia_chi': _format_address,
    'email': _format_email,
}


    def is_accessible(self):
        return current_user.is_authenticated and current_user.type in ['quan_tri', 'y_ta','bac_si']

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from myapp.extensions import db
from myapp.models import BacSi, Sdt, DiaChi, Email
from sqlalchemy import or_
from flask import request
from flask_admin.form import rules
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length
import unicodedata
def remove_accents(input_str):
    """
    Loại bỏ dấu tiếng Việt từ chuỗi.
    """
    if not input_str:  # Kiểm tra nếu chuỗi là None hoặc rỗng
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

class DoctorView(ModelView):
    form_columns = ['ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'cccd']  # Các cột chính

    # Đảm bảo sử dụng mối quan hệ trong `inline_models`
    inline_models = [
        ('so_dien_thoai_s', dict(form_columns=['so_dien_thoai'])),  # Quan hệ với bảng Sdt
        ('dia_chi_s', dict(form_columns=['dia_chi'])),  # Quan hệ với bảng DiaChi
        ('email_addresses', dict(form_columns=['email']))  # Quan hệ với bảng Email
    ]
    
    # Sử dụng `SelectField` cho `gioi_tinh`
    form_overrides = {
        'gioi_tinh': SelectField  # Nếu bạn muốn sử dụng SelectField cho `gioi_tinh`
    }

    # Đảm bảo bạn định nghĩa đúng các lựa chọn trong `form_choices`
    form_choices = {
        'gioi_tinh': [('True', 'Nam'), ('False', 'Nữ')]  # Các lựa chọn cho giới tính
    }
    # Các cấu hình hiện tại
    column_list = [
        'id', 'ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'cccd', 
        'khoa.ten_khoa', 'so_dien_thoai', 'dia_chi', 'email'
    ]

    column_labels = {
        'id': 'Mã bác sĩ',
        'ho': 'Họ',
        'ten': 'Tên',
        'gioi_tinh': 'Giới tính',
        'ngay_sinh': 'Ngày sinh',
        'cccd': 'CCCD',
        'khoa.ten_khoa': 'Khoa',
        'so_dien_thoai': 'Số điện thoại',
        'dia_chi': 'Địa chỉ',
        'email': 'Email',
    }

    # Thêm các cột vào danh sách tìm kiếm
    column_searchable_list = [
        'ho', 'ten', 'cccd',  # Các cột từ bảng BacSi
        'so_dien_thoai_s.so_dien_thoai',  # Số điện thoại từ bảng liên kết
        'email_addresses.email',         # Email từ bảng liên kết
        'dia_chi_s.dia_chi'              # Địa chỉ từ bảng liên kết
    ]
    def get_query(self):
        """
        Override default query to add custom search behavior.
        """
        query = super(DoctorView, self).get_query()
        search_term = request.args.get('search')  # Lấy từ khóa tìm kiếm từ query string

        if search_term:  # Chỉ xử lý nếu có từ khóa tìm kiếm
            normalized_term = remove_accents(search_term)  # Loại bỏ dấu
            print(f"Searching for: {search_term}, Normalized: {normalized_term}")  # Log từ khóa tìm kiếm
            query = query.join(Sdt, BacSi.id == Sdt.nguoi_dung_id, isouter=True) \
                     .join(DiaChi, BacSi.id == DiaChi.nguoi_dung_id, isouter=True) \
                     .join(Email, BacSi.id == Email.nguoi_dung_id, isouter=True) \
                     .filter(
                         or_(
                             BacSi.ho.ilike(f"%{search_term}%"),
                             BacSi.ten.ilike(f"%{search_term}%"),
                             BacSi.ho.ilike(f"%{normalized_term}%"),
                             BacSi.ten.ilike(f"%{normalized_term}%"),
                             Sdt.so_dien_thoai.ilike(f"%{search_term}%"),
                             DiaChi.dia_chi.ilike(f"%{search_term}%"),
                             Email.email.ilike(f"%{search_term}%")
                         )
                     )
            print(f"Query Result IDs: {[bacsi.id for bacsi in query.all()]}")

        return query

    # Định nghĩa cách hiển thị các cột liên kết
    def _format_phone(view, context, model, name):
        return ", ".join([sdt.so_dien_thoai for sdt in model.so_dien_thoai_s]) if model.so_dien_thoai_s else "N/A"

    def _format_address(view, context, model, name):
        return ", ".join([dia_chi.dia_chi for dia_chi in model.dia_chi_s]) if model.dia_chi_s else "N/A"

    def _format_email(view, context, model, name):
        return ", ".join([email.email for email in model.email_addresses]) if model.email_addresses else "N/A"
    
    column_formatters = {
        'gioi_tinh': lambda v, c, m, n: "Nam" if m.gioi_tinh else "Nữ",
        'so_dien_thoai': _format_phone,
        'dia_chi': _format_address,
        'email': _format_email,
    }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from myapp.extensions import db
from myapp.models import BacSi, Sdt, DiaChi, Email
from sqlalchemy import or_
from flask import request
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
import unicodedata
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
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

class DoctorView(ModelView):
    form_columns = ['ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'cccd']  # Các cột chính

    # Đảm bảo sử dụng mối quan hệ trong `inline_models`
    inline_models = [
        (Sdt, dict(form_columns=['so_dien_thoai'])),  # Bao gồm trường 'so_dien_thoai'
        (DiaChi, dict(form_columns=['dia_chi'])),    # Bao gồm trường 'dia_chi'
        (Email, dict(form_columns=['email']))         # Bao gồm trường 'email'
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
            print(query.all())  # Debug dữ liệu

        return query
    # Định nghĩa hàm tùy chỉnh lưu dữ liệu
    def on_model_change(self, form, model, is_created):
        """
        Tùy chỉnh lưu thông tin bác sĩ và các mối quan hệ liên kết.
        """
        if 'so_dien_thoai' in form.data:
            # Xóa các số điện thoại cũ
            model.sdt = []

            # Lấy danh sách số điện thoại mới
            phone_numbers = form.data['so_dien_thoai'].split("\n")
            for phone in phone_numbers:
                phone = phone.strip()
                if phone:  # Bỏ qua các dòng trống
                    sdt = Sdt(so_dien_thoai=phone, nguoi_dung=model)
                    db.session.add(sdt)
        print(f"Model: {model}")
        print(f"Form data: {form.data}")
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
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

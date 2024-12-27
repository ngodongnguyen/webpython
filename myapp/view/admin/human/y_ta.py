from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
from flask_login import current_user
from myapp.models import YTa, Sdt, DiaChi, Email
from myapp.extensions import db
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email as WTFormsEmail
from datetime import datetime,date

class NurseView(ModelView):
    # Các cột hiển thị trong danh sách
    column_list = ['id', 'ho', 'ten', 'username', 'emails', 'dia_chi_s']

    # Nhãn hiển thị
    column_labels = {
        'id': 'Mã Y Tá',
        'ho': 'Họ',
        'ten': 'Tên',
        'username': 'Tên đăng nhập',
        'emails': 'Email',
        'dia_chi_s': 'Địa chỉ',
    }

    # Các trường nhập liệu trên form
    form_columns = ['ho', 'ten', 'username', 'password', 'email', 'dia_chi']

    form_extra_fields = {
        'ho': StringField('Họ', validators=[DataRequired()]),
        'ten': StringField('Tên', validators=[DataRequired()]),
        'username': StringField('Tên đăng nhập', validators=[DataRequired()]),
        'password': PasswordField('Mật khẩu', validators=[DataRequired()]),
        'email': StringField('Email', validators=[DataRequired(), WTFormsEmail()]),
        'dia_chi': StringField('Địa chỉ', validators=[DataRequired()])
    }

    # Định dạng hiển thị email và địa chỉ trong danh sách
    column_formatters = {
        'emails': lambda v, c, m, p: ", ".join([email.email for email in m.emails]) if m.emails else "N/A",
        'dia_chi_s': lambda v, c, m, p: ", ".join([dia_chi.dia_chi for dia_chi in m.dia_chi_s]) if m.dia_chi_s else "N/A",
    }

    def on_model_change(self, form, model, is_created):
        # Cập nhật email và địa chỉ từ form
        if form.email.data:
            if model.emails:
                model.emails[0].email = form.email.data  # Cập nhật email đầu tiên
            else:
                email = Email(email=form.email.data, nguoi_dung_id=model.id)
                model.emails.append(email)

        if form.dia_chi.data:
            if model.dia_chi_s:
                model.dia_chi_s[0].dia_chi = form.dia_chi.data  # Cập nhật địa chỉ đầu tiên
            else:
                dia_chi = DiaChi(dia_chi=form.dia_chi.data, nguoi_dung_id=model.id)
                model.dia_chi_s.append(dia_chi)

    # Hiển thị đúng giá trị email và địa chỉ trong form edit
    def on_form_prefill(self, form, id):
        model = self.get_one(id)
        if model.emails and len(model.emails) > 0:
            form.email.data = model.emails[0].email
        if model.dia_chi_s and len(model.dia_chi_s) > 0:
            form.dia_chi.data = model.dia_chi_s[0].dia_chi

    def create_model(self, form):
        # Logic tạo y tá mới
        try:
            y_ta = YTa(
                ho=form.ho.data,
                ten=form.ten.data,
                username=form.username.data,
                password=form.password.data,
                gioi_tinh=True,
                ngay_sinh=datetime.now(),
                cccd="123456789012",
            )
            y_ta.set_password(form.password.data)
            db.session.add(y_ta)
            db.session.flush()

            email = Email(email=form.email.data, nguoi_dung_id=y_ta.id)
            dia_chi = DiaChi(dia_chi=form.dia_chi.data, nguoi_dung_id=y_ta.id)

            db.session.add_all([email, dia_chi])
            db.session.commit()
            flash("Thêm y tá thành công!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi thêm y tá: {str(e)}", "error")
            raise

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập vào chức năng này.", "error")
        return redirect(url_for('main.index'))

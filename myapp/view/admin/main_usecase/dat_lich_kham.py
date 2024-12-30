from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
from flask_login import current_user
from myapp.models import DangKyKham, BenhNhan, Sdt, DiaChi, Email,YTa,DanhSachDangKyKham
from myapp.extensions import db
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from wtforms_sqlalchemy.fields import QuerySelectField


from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
from flask_login import current_user
from myapp.models import DangKyKham, BenhNhan, Sdt, DiaChi, Email, YTa, DanhSachDangKyKham,QuyDinh
from myapp.extensions import db
from wtforms import StringField, DateField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField  # Sử dụng QuerySelectField từ wtforms_sqlalchemy.fields
from wtforms.validators import DataRequired
from datetime import datetime


class DangKyKhamView(ModelView):
    # Các cột hiển thị trong danh sách
    column_list = ['id', 'ngay_dang_ky', 'danh_sach_id', 'id_benh_nhan', 'benh_nhan_full_name', 'id_y_ta', 'y_ta_full_name']

    # Nhãn hiển thị
    column_labels = {
        'id': 'Mã đăng ký',
        'ngay_dang_ky': 'Ngày đăng ký',
        'danh_sach_id': 'Danh sách đăng ký',
        'id_benh_nhan': 'ID Bệnh Nhân',
        'benh_nhan_full_name': 'Họ tên bệnh nhân',
        'id_y_ta': 'ID Y Tá',
        'y_ta_full_name': 'Họ tên y tá',
    }

    # Định dạng cột
    column_formatters = {
        'benh_nhan_full_name': lambda v, c, m, p: f"{m.benh_nhan.ho} {m.benh_nhan.ten}" if m.benh_nhan else "N/A",
        'y_ta_full_name': lambda v, c, m, p: f"{m.y_ta.ho} {m.y_ta.ten}" if m.y_ta else "N/A",
        'gioi_tinh': lambda v, c, m, n: "Nam" if m.gioi_tinh else "Nữ",

    }
    form_overrides = {
    'gioi_tinh': SelectField  # Dùng SelectField cho trường 'gioi_tinh'
}

# Cấu hình `form_choices` để chỉ định các lựa chọn cho các trường 'SelectField'
    form_choices = {
        'gioi_tinh': [(True, 'Nam'), (False, 'Nữ')]
    }

    # Cấu hình `form_args` chứa các tham số bổ sung cho các trường trong form
    form_args = {
        'gioi_tinh': {
            'label': 'Giới tính',
            'coerce': lambda x: x == '1',  # Chuyển đổi giá trị từ 1/0 sang Boolean
            'choices': [(True, 'Nam'), (False, 'Nữ')]
        }
    }
    # Các trường nhập liệu trên form
    form_create_rules = ('ngay_dang_ky', 'benh_nhan_ho', 'benh_nhan_ten', 'gioi_tinh', 'cccd', 'benh_nhan_sdt', 'benh_nhan_email', 'benh_nhan_dia_chi')

    form_extra_fields = {
        'benh_nhan_ho': StringField('Họ bệnh nhân', validators=[DataRequired()]),
        'benh_nhan_ten': StringField('Tên bệnh nhân', validators=[DataRequired()]),
        'benh_nhan_sdt': StringField('Số điện thoại', validators=[DataRequired()]),
        'benh_nhan_email': StringField('Email', validators=[DataRequired()]),
        'benh_nhan_dia_chi': StringField('Địa chỉ', validators=[DataRequired()]),
        'cccd': StringField('CCCD', validators=[DataRequired()]),
        'gioi_tinh': SelectField(
        'Giới tính',
        choices=[(True, 'Nam'), (False, 'Nữ')],
        coerce=bool,
        validators=[DataRequired()]
    ),
        'ngay_dang_ky': DateField(
            'Ngày đăng ký',
            default=datetime.today,
            validators=[DataRequired()],
            render_kw={
                'min': datetime.today().strftime('%Y-%m-%d')
            }
        ),
    }

    def create_model(self, form):
        try:
            print("[DEBUG] Bắt đầu xử lý create_model")
            print("[DEBUG] Form data:", form.data)

            # Lấy thông tin từ form
            cccd = form.cccd.data
            ngay_dang_ky = form.ngay_dang_ky.data

            # Kiểm tra nếu CCCD đã đăng ký trong ngày
            benh_nhan = BenhNhan.query.filter_by(cccd=cccd).first()
            print(f"[DEBUG] Kết quả tìm kiếm bệnh nhân: {benh_nhan}")

            if benh_nhan:
                # Kiểm tra nếu đã đăng ký trong ngày
                da_dang_ky = DangKyKham.query.filter_by(id_benh_nhan=benh_nhan.id, ngay_dang_ky=ngay_dang_ky).first()
                print(f"[DEBUG] Kết quả tìm kiếm đăng ký trong ngày: {da_dang_ky}")
                if da_dang_ky:
                    flash(f"CCCD {cccd} đã đăng ký vào ngày {ngay_dang_ky.strftime('%d-%m-%Y')}.", "error")
                    return

            # Nếu bệnh nhân chưa tồn tại, tạo mới
            if not benh_nhan:
                gioi_tinh_value = form.gioi_tinh.data  # Boolean value from SelectField
                print(f"[DEBUG] Giá trị gioi_tinh từ form: {gioi_tinh_value}")

                benh_nhan = BenhNhan(
                    ho=form.benh_nhan_ho.data,
                    ten=form.benh_nhan_ten.data,
                    gioi_tinh=gioi_tinh_value,
                    ngay_sinh=datetime.now(),  # Ngày sinh tạm thời
                    cccd=cccd,
                )
                db.session.add(benh_nhan)
                db.session.flush()  # Đảm bảo lấy ID bệnh nhân
                print(f"[DEBUG] Tạo mới bệnh nhân thành công, ID: {benh_nhan.id}")

                # Thêm số điện thoại, email, và địa chỉ
                sdt = Sdt(so_dien_thoai=form.benh_nhan_sdt.data, nguoi_dung_id=benh_nhan.id)
                email = Email(email=form.benh_nhan_email.data, nguoi_dung_id=benh_nhan.id)
                dia_chi = DiaChi(dia_chi=form.benh_nhan_dia_chi.data, nguoi_dung_id=benh_nhan.id)
                db.session.add_all([sdt, email, dia_chi])
                db.session.flush()

            # Kiểm tra số lượng đăng ký trong ngày
            danh_sach = DangKyKham.query.filter_by(ngay_dang_ky=ngay_dang_ky).count()
            print(f"[DEBUG] Số lượng đăng ký trong ngày: {danh_sach}")
            max_so_benh_nhan = QuyDinh.query.first().so_benh_nhan
# Kiểm tra nếu danh sách đã đạt hoặc vượt giới hạn
            if danh_sach >= max_so_benh_nhan:
                flash(f"Ngày {ngay_dang_ky.strftime('%d-%m-%Y')} đã đạt giới hạn {max_so_benh_nhan} lượt đăng ký.", "error")
                return

            # Tạo đăng ký khám
            dang_ky_kham = DangKyKham(
                ngay_dang_ky=ngay_dang_ky,
                id_benh_nhan=benh_nhan.id,
                id_y_ta=current_user.id  # Lấy y tá hiện tại
            )
            db.session.add(dang_ky_kham)
            db.session.commit()
            print("[DEBUG] Tạo đăng ký khám thành công!")
            flash("Tạo đăng ký thành công!", "success")

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Lỗi khi tạo đăng ký: {e}")
            flash(f"Lỗi khi tạo đăng ký: {str(e)}", "error")
            raise



    def is_accessible(self):
        print(f"[DEBUG] Kiểm tra quyền truy cập của user: {current_user}")
        return current_user.is_authenticated and current_user.type in ['quan_tri', 'y_ta']

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập vào chức năng này.", "error")
        return redirect(url_for('admin.index'))

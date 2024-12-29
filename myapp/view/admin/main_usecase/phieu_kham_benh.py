from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for
from flask_login import current_user
from wtforms import Form, StringField, DateField, TextAreaField, FieldList, FormField, IntegerField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from myapp.models import PhieuKhamBenh, BenhNhan, Thuoc, ChiTietDonThuoc
from myapp.extensions import db


# Form để chọn thuốc và số lượng
class ThuocForm(Form):
    thuoc_id = SelectField(
        'Thuốc',
        coerce=int,
        validators=[DataRequired()],
        choices=lambda: [(thuoc.id, thuoc.ten_thuoc) for thuoc in Thuoc.query.all()]
    )
    so_luong = IntegerField('Số lượng', validators=[DataRequired()])


# View quản lý phiếu khám bệnh
class PhieuKhamBenhView(ModelView):
    # Các cột hiển thị trong danh sách
    column_list = [
        'id', 
        'ngay_kham', 
        'trieu_chung', 
        'chuan_doan', 
        'benh_nhan_full_name', 
        'bac_si_full_name', 
        'thuoc_info'
    ]

    # Nhãn hiển thị
    column_labels = {
        'id': 'Mã phiếu khám',
        'ngay_kham': 'Ngày khám',
        'trieu_chung': 'Triệu chứng',
        'chuan_doan': 'Chẩn đoán',
        'benh_nhan_full_name': 'Họ tên bệnh nhân',
        'bac_si_full_name': 'Họ tên bác sĩ',
        'thuoc_info': 'Thuốc kê đơn',
    }

    # Định dạng cột
    column_formatters = {
        'benh_nhan_full_name': lambda v, c, m, p: f"{m.benh_nhan.ho} {m.benh_nhan.ten}" if m.benh_nhan else "N/A",
        'bac_si_full_name': lambda v, c, m, p: f"{m.bac_si.ho} {m.bac_si.ten}" if m.bac_si else "N/A",
        'thuoc_info': lambda v, c, m, p: "\n".join([
            f"{ct.thuoc.ten_thuoc} - {ct.so_luong} {ct.thuoc.loai} ({ct.thuoc.huong_dan_su_dung or 'Không có hướng dẫn'})"
            for ct in m.thuoc
        ]) if m.thuoc else "Không có thuốc"
    }

    # Các trường nhập liệu trên form
    form_create_rules = ('ngay_kham', 'trieu_chung', 'chuan_doan', 'benh_nhan_search', 'thuoc_list')

    form_extra_fields = {
        'ngay_kham': DateField(
            'Ngày khám',
            default=datetime.today,
            validators=[DataRequired()],
            render_kw={'min': datetime.today().strftime('%Y-%m-%d')}
        ),
        'trieu_chung': TextAreaField('Triệu chứng', validators=[DataRequired()]),
        'chuan_doan': TextAreaField('Chẩn đoán', validators=[DataRequired()]),
        'benh_nhan_search': StringField(
            'Tìm kiếm bệnh nhân',
            validators=[DataRequired()],
            render_kw={'placeholder': 'Nhập tên bệnh nhân để tìm kiếm'}
        ),
        'thuoc_list': FieldList(
            FormField(ThuocForm),  # Sử dụng form `ThuocForm`
            min_entries=1
        ),
    }

    def create_model(self, form):
        try:
            print("[DEBUG] Bắt đầu tạo phiếu khám bệnh")
            
            # Lấy thông tin bệnh nhân từ kết quả tìm kiếm
            benh_nhan_name = form.benh_nhan_search.data
            benh_nhan = BenhNhan.query.filter(
                (BenhNhan.ho + " " + BenhNhan.ten) == benh_nhan_name
            ).first()
            if not benh_nhan:
                flash("Không tìm thấy bệnh nhân.", "error")
                return
            
            # Lấy thông tin bác sĩ hiện tại
            bac_si_id = current_user.id

            # Tạo phiếu khám bệnh
            phieu_kham = PhieuKhamBenh(
                ngay_kham=form.ngay_kham.data,
                trieu_chung=form.trieu_chung.data,
                chuan_doan=form.chuan_doan.data,
                benh_nhan_id=benh_nhan.id,
                bac_si_id=bac_si_id,
            )
            db.session.add(phieu_kham)
            db.session.flush()  # Lưu tạm để lấy ID

            # Thêm thuốc vào phiếu khám
            for thuoc_entry in form.thuoc_list.entries:
                thuoc_id = thuoc_entry.form.thuoc_id.data
                so_luong = thuoc_entry.form.so_luong.data
                thuoc = Thuoc.query.get(thuoc_id)
                if not thuoc:
                    flash(f"Không tìm thấy thuốc với ID {thuoc_id}.", "error")
                    return
                chi_tiet_thuoc = ChiTietDonThuoc(
                    phieu_kham_id=phieu_kham.id,
                    thuoc_id=thuoc_id,
                    so_luong=so_luong
                )
                db.session.add(chi_tiet_thuoc)

            db.session.commit()
            flash("Tạo phiếu khám thành công!", "success")
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Lỗi khi tạo phiếu khám: {e}")
            flash(f"Lỗi khi tạo phiếu khám: {str(e)}", "error")
            raise

    def is_accessible(self):
        return current_user.is_authenticated and current_user.type in ['admin', 'bac_si']

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập vào chức năng này.", "error")
        return redirect(url_for('admin.index'))

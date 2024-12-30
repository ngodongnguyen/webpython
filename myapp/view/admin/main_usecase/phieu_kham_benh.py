from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for
from flask_login import current_user
from wtforms import Form, StringField, TextAreaField, FieldList, FormField, IntegerField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from myapp.models import PhieuKhamBenh, BenhNhan, Thuoc, ChiTietDonThuoc, DanhSachPhieuKhamBenh, HoaDon
from myapp.extensions import db


# Form để chọn thuốc và số lượng
class ThuocForm(Form):
    thuoc_id = SelectField(
        'Thuốc',
        coerce=int,
        validators=[DataRequired()]
    )
    so_luong = IntegerField('Số lượng', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cập nhật danh sách thuốc từ database
        self.thuoc_id.choices = [(thuoc.id, thuoc.ten_thuoc) for thuoc in Thuoc.query.all()]
        if not self.thuoc_id.choices:
            flash("Không có thuốc nào trong cơ sở dữ liệu.", "warning")


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
            f"{ct.thuoc.ten_thuoc} - {ct.so_luong_thuoc} {ct.thuoc.loai} ({ct.thuoc.huong_dan_su_dung or 'Không có hướng dẫn'})"
            for ct in m.thuoc
        ]) if m.thuoc else "Không có thuốc"
    }

    # Các trường nhập liệu trên form
    form_create_rules = ('trieu_chung', 'chuan_doan', 'benh_nhan_search', 'thuoc_list')

    form_extra_fields = {
        'trieu_chung': TextAreaField(
            'Triệu chứng',
            validators=[DataRequired()],
            render_kw={'class': 'form-control', 'rows': 4, 'style': 'margin-bottom: 15px;'}
        ),
        'chuan_doan': TextAreaField(
            'Chẩn đoán',
            validators=[DataRequired()],
            render_kw={'class': 'form-control', 'rows': 4, 'style': 'margin-bottom: 15px;'}
        ),
        'benh_nhan_search': StringField(
            'Tìm kiếm bệnh nhân',
            validators=[DataRequired()],
            render_kw={'class': 'form-control', 'placeholder': 'Nhập tên bệnh nhân để tìm kiếm'}
        ),
        'thuoc_list': FieldList(
            FormField(ThuocForm),
            min_entries=10,  # Cho phép ít nhất 1 thuốc
            render_kw={'style': 'margin-bottom: 200px;'}
        ),
    }

    def create_model(self, form):
        try:
            # Kiểm tra thông tin nhập vào từ form
            benh_nhan_name = form.benh_nhan_search.data
            benh_nhan = BenhNhan.query.filter(
                (BenhNhan.ho + " " + BenhNhan.ten) == benh_nhan_name
            ).first()

            if not benh_nhan:
                flash("Không tìm thấy bệnh nhân.", "error")
                return

            bac_si_id = current_user.id
            ngay_kham = datetime.today().date()

            # Kiểm tra danh sách cho ngày hiện tại
            danhsach = DanhSachPhieuKhamBenh.query.filter_by(ngay_tao=ngay_kham).first()

            if not danhsach:
                danhsach = DanhSachPhieuKhamBenh(tong_so=0, ngay_tao=ngay_kham)
                db.session.add(danhsach)
                db.session.commit()

            # Tạo phiếu khám bệnh
            phieu_kham = PhieuKhamBenh(
                ngay_kham=ngay_kham,
                trieu_chung=form.trieu_chung.data,
                chuan_doan=form.chuan_doan.data,
                benh_nhan_id=benh_nhan.id,
                bac_si_id=bac_si_id,
                danhsach_id=danhsach.id,
            )
            db.session.add(phieu_kham)
            db.session.flush()

            # Thêm nhiều thuốc vào phiếu khám
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
                    so_luong_thuoc=so_luong
                )
                db.session.add(chi_tiet_thuoc)

            # Tự động tạo hóa đơn sau khi thêm phiếu khám
            default_tien_kham_benh = 100000  # Số tiền khám bệnh mặc định
            tien_thuoc = sum(
                chi_tiet.thuoc.gia_tien * chi_tiet.so_luong_thuoc for chi_tiet in phieu_kham.thuoc
            ) if phieu_kham.thuoc else 0

            hoa_don = HoaDon(
                ngay_tinh_tien=ngay_kham,
                tien_kham_benh=default_tien_kham_benh,
                tien_thuoc=tien_thuoc,
                tong_tien=default_tien_kham_benh + tien_thuoc,
                phieu_kham_id=phieu_kham.id,
                benh_nhan_id=benh_nhan.id,
                thu_ngan_id=benh_nhan.id  # Cập nhật nếu cần
            )
            db.session.add(hoa_don)

            # Cập nhật số lượng phiếu khám trong danh sách
            danhsach.tong_so += 1
            db.session.commit()

            flash("Tạo phiếu khám và hóa đơn thành công!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi tạo phiếu khám: {str(e)}", "error")
            raise

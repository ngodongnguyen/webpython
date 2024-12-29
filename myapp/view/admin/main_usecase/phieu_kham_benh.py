from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for
from flask_login import current_user
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired
from datetime import datetime
from myapp.models import PhieuKhamBenh, BenhNhan, BacSi, ChiTietDonThuoc, Thuoc
from myapp.extensions import db

class PhieuKhamBenhView(ModelView):
    # Các cột hiển thị trong danh sách
    column_list = [
        'id',
        'trieu_chung',
        'chuan_doan',
        'benh_nhan.ho',
        'benh_nhan.ten',
        'bac_si.ho',
        'bac_si.ten',
    ]

    # Nhãn hiển thị
    column_labels = {
        'id': 'Mã phiếu khám',
        'trieu_chung': 'Triệu chứng',
        'chuan_doan': 'Chẩn đoán',
        'benh_nhan.ho': 'Họ bệnh nhân',
        'benh_nhan.ten': 'Tên bệnh nhân',
        'bac_si.ho': 'Họ bác sĩ',
        'bac_si.ten': 'Tên bác sĩ',
    }

    form_columns = ['trieu_chung', 'chuan_doan', 'benh_nhan_id', 'bac_si_id']

    # Cấu hình form
    form_args = {
        'trieu_chung': {
            'label': 'Triệu chứng',
            'validators': [DataRequired()],
        },
        'chuan_doan': {
            'label': 'Chẩn đoán',
            'validators': [DataRequired()],
        },
        'benh_nhan_id': {
            'label': 'Bệnh nhân',
            'coerce': int,
            'choices': lambda: [(bn.id, f"{bn.ho} {bn.ten}") for bn in BenhNhan.query.all()],
        },
        'bac_si_id': {
            'label': 'Bác sĩ',
            'coerce': int,
            'choices': lambda: [(bs.id, f"{bs.ho} {bs.ten}") for bs in BacSi.query.all()],
        },
    }

    # Inline models để hiển thị thuốc
    inline_models = [
        (ChiTietDonThuoc, dict(
            form_columns=['thuoc_id', 'so_luong_thuoc'],
            form_overrides={
                'thuoc_id': StringField,
                'so_luong': StringField,
            },
            form_args={
                'thuoc_id': {
                    'label': 'Thuốc',
                    'validators': [DataRequired()],
                },
                'so_luong': {
                    'label': 'Số lượng',
                    'validators': [DataRequired()],
                }
            }
        ))
    ]

    def create_model(self, form):
        try:
            # Tạo phiếu khám
            phieu_kham = PhieuKhamBenh(
                trieu_chung=form.trieu_chung.data,
                chuan_doan=form.chuan_doan.data,
                benh_nhan_id=form.benh_nhan_id.data,
                bac_si_id=current_user.id,
            )
            db.session.add(phieu_kham)
            db.session.commit()
            flash("Tạo phiếu khám thành công!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi tạo phiếu khám: {e}", "error")
            raise

    def is_accessible(self):
        return current_user.is_authenticated and current_user.type in ['admin', 'bac_si']

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập vào chức năng này.", "error")
        return redirect(url_for('admin.index'))

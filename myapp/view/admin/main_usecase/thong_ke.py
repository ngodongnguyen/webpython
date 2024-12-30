from flask import flash, redirect, url_for
from flask_admin import BaseView, expose
from flask_login import current_user
from myapp.models import HoaDon, PhieuKhamBenh, ChiTietDonThuoc, Thuoc
from myapp.extensions import db
from sqlalchemy import extract, func, and_

class ThongKeView(BaseView):
    @expose('/')
    def index(self):
        try:
            # Thống kê doanh thu và tần suất khám từng tháng
            doanh_thu_tan_suat = db.session.query(
                extract('month', HoaDon.ngay_tinh_tien).label('thang'),
                func.count(HoaDon.id).label('tan_suat'),
                func.sum(HoaDon.tong_tien).label('doanh_thu')
            ).filter(and_(
                extract('month', HoaDon.ngay_tinh_tien) >= 1,
                extract('month', HoaDon.ngay_tinh_tien) <= 12  # Chỉ lấy dữ liệu tháng hợp lệ
            )).group_by(extract('month', HoaDon.ngay_tinh_tien)).all()

            # Thống kê tần suất sử dụng các thuốc theo tháng
            thuoc_tan_suat = db.session.query(
                extract('month', PhieuKhamBenh.ngay_kham).label('thang'),
                Thuoc.ten_thuoc,
                func.sum(ChiTietDonThuoc.so_luong_thuoc).label('tong_so_luong')
            ).select_from(PhieuKhamBenh).join(ChiTietDonThuoc, PhieuKhamBenh.id == ChiTietDonThuoc.phieu_kham_id) \
            .join(Thuoc, ChiTietDonThuoc.thuoc_id == Thuoc.id) \
            .group_by(extract('month', PhieuKhamBenh.ngay_kham), Thuoc.ten_thuoc).all()

            # Xử lý dữ liệu để đảm bảo đủ 12 tháng cho doanh thu
            doanh_thu_data = {
                "tan_suat": [0] * 12,  # Mảng 12 tháng, mặc định giá trị 0
                "doanh_thu": [0] * 12
            }
            for row in doanh_thu_tan_suat:
                month_index = int(row.thang) - 1  # Chỉ số tháng bắt đầu từ 0
                if 0 <= month_index < 12:  # Kiểm tra chỉ số hợp lệ
                    doanh_thu_data["tan_suat"][month_index] = row.tan_suat
                    doanh_thu_data["doanh_thu"][month_index] = row.doanh_thu
                else:
                    print("Dữ liệu sai tháng:", row)  # Debug dữ liệu sai

            # Xử lý dữ liệu thuốc
            thuoc_data = {}
            for row in thuoc_tan_suat:
                if row.ten_thuoc not in thuoc_data:
                    thuoc_data[row.ten_thuoc] = [0] * 12  # Mảng 12 tháng, mặc định giá trị 0
                thuoc_data[row.ten_thuoc][int(row.thang) - 1] = row.tong_so_luong

            # Tạo nhãn cho 12 tháng
            doanh_thu_labels = [f"Tháng {i+1}" for i in range(12)]

            return self.render(
                'admin/thongke.html',
                doanh_thu_labels=doanh_thu_labels,
                doanh_thu_data=doanh_thu_data,
                thuoc_data=thuoc_data
            )
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)
            flash(f"Lỗi khi lấy dữ liệu: {e}", "error")
            return redirect(url_for('admin.index'))

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập vào chức năng này.", "error")
        return redirect(url_for('admin.index'))

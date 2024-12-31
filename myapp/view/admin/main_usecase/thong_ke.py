from flask import flash, redirect, url_for, render_template
from flask_admin import BaseView, expose
from flask_login import current_user
from myapp.models import HoaDon, PhieuKhamBenh, ChiTietDonThuoc, Thuoc
from myapp.extensions import db
from sqlalchemy import func

class ThongKeView(BaseView):
    @expose('/')
    def index(self):
        try:
            # Thống kê doanh thu và tần suất khám
            doanh_thu_tan_suat = db.session.query(
                func.extract('year', HoaDon.ngay_tinh_tien).label('nam'),
                func.extract('month', HoaDon.ngay_tinh_tien).label('thang'),
                func.count(HoaDon.id).label('tan_suat'),
                func.sum(HoaDon.tong_tien).label('doanh_thu')
            ).group_by(
                func.extract('year', HoaDon.ngay_tinh_tien), 
                func.extract('month', HoaDon.ngay_tinh_tien)
            ).all()
            
            print("Doanh thu và tần suất khám:", doanh_thu_tan_suat)

            # Thống kê tần suất sử dụng thuốc
            thuoc_tan_suat = db.session.query(
                func.extract('year', PhieuKhamBenh.ngay_kham).label('nam'),
                func.extract('month', PhieuKhamBenh.ngay_kham).label('thang'),
                Thuoc.ten_thuoc,
                func.sum(ChiTietDonThuoc.so_luong_thuoc).label('tong_so_luong')
            ).join(
                ChiTietDonThuoc, PhieuKhamBenh.id == ChiTietDonThuoc.phieu_kham_id
            ).join(
                Thuoc, ChiTietDonThuoc.thuoc_id == Thuoc.id
            ).group_by(
                func.extract('year', PhieuKhamBenh.ngay_kham),
                func.extract('month', PhieuKhamBenh.ngay_kham), 
                Thuoc.ten_thuoc
            ).all()
            
            print("Thuốc tần suất:", thuoc_tan_suat)

            # Xử lý dữ liệu doanh thu và tần suất khám
            tan_suat_theo_nam = {}
            doanh_thu_theo_nam = {}
            for row in doanh_thu_tan_suat:
                year = int(row.nam)
                month_index = int(row.thang) - 1

                if year not in tan_suat_theo_nam:
                    tan_suat_theo_nam[year] = [0] * 12
                if year not in doanh_thu_theo_nam:
                    doanh_thu_theo_nam[year] = [0] * 12

                tan_suat_theo_nam[year][month_index] = row.tan_suat or 0
                doanh_thu_theo_nam[year][month_index] = row.doanh_thu or 0

            print("Tần suất theo năm:", tan_suat_theo_nam)
            print("Doanh thu theo năm:", doanh_thu_theo_nam)

            # Xử lý dữ liệu thuốc
            thuoc_theo_nam = {}
            for row in thuoc_tan_suat:
                year = int(row.nam)
                month_index = int(row.thang) - 1
                ten_thuoc = row.ten_thuoc
                so_luong = row.tong_so_luong or 0

                if year not in thuoc_theo_nam:
                    thuoc_theo_nam[year] = {}
                if ten_thuoc not in thuoc_theo_nam[year]:
                    thuoc_theo_nam[year][ten_thuoc] = [0] * 12

                thuoc_theo_nam[year][ten_thuoc][month_index] = so_luong

            print("Thuốc theo năm:", thuoc_theo_nam)

            return self.render(
                'admin/thongke.html',
                tan_suat_theo_nam=tan_suat_theo_nam,
                doanh_thu_theo_nam=doanh_thu_theo_nam,
                thuoc_theo_nam=thuoc_theo_nam,
                labels=[f"Tháng {i+1}" for i in range(12)]
            )
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)
            flash(f"Lỗi khi lấy dữ liệu: {e}", "error")
            return redirect(url_for('admin.index'))

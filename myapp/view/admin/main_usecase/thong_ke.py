from flask_admin import BaseView, expose
from flask import render_template
from sqlalchemy import func
from myapp.extensions import db
from myapp.models import HoaDon

class ThongKeView(BaseView):
    @expose('/')
    def index(self):
        """
        Trang thống kê chính, hiển thị dữ liệu và biểu đồ.
        """
        # Truy vấn dữ liệu thống kê
        doanh_thu = db.session.query(
            func.strftime('%Y-%m', HoaDon.ngay_tinh_tien).label('month'),
            func.sum(HoaDon.tien_kham_benh).label('tien_kham_benh'),
            func.sum(HoaDon.tien_thuoc).label('tien_thuoc')
        ).group_by('month').all()

        # Chuẩn bị dữ liệu
        data = [{'month': row[0], 'tien_kham_benh': row[1], 'tien_thuoc': row[2]} for row in doanh_thu]

        # Render dữ liệu ra view
        return self.render('admin/thong_ke.html', data=data)

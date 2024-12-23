from flask import render_template
from flask.views import MethodView
from myapp import app

class HomeView(MethodView):
    def get(self):
        # Trang chủ - trả về template trang chủ
        return render_template('admin/trangchu.html')

class StatisticView(MethodView):
    def get(self):
        # Trang thống kê - trả về template thống kê
        return render_template('admin/thongke.html')

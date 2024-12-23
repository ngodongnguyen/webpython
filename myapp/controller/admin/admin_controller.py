from flask import render_template, jsonify, session, request
from myapp import db
from myapp.models import DangKyKham, BacSi, YTa, NhanVien

class AdminController:
    @staticmethod
    def dashboard():
        # Trang chính admin dashboard
        if not session.get('username'):  # Kiểm tra đăng nhập
            return render_template('admin/login.html')  # Hoặc chuyển hướng tới login
        return render_template('admin/trangchu.html')

    @staticmethod
    def statistics():
        # Lấy dữ liệu thống kê
        try:
            medical_amount = DangKyKham.query.count()
            doctor_amount = BacSi.query.count()
            nurse_amount = YTa.query.count()
            staff_amount = NhanVien.query.count()

            # Hiển thị trang thống kê
            return render_template(
                'admin/thongke.html',
                medical_amount=medical_amount,
                doctor_amount=doctor_amount,
                nurse_amount=nurse_amount,
                staff_amount=staff_amount
            )
        except Exception as e:
            return render_template('admin/thongke.html', error=str(e))

    @staticmethod
    def fetch_statistics():
        # API trả về dữ liệu thống kê
        try:
            medical_amount = DangKyKham.query.count()
            doctor_amount = BacSi.query.count()
            nurse_amount = YTa.query.count()
            staff_amount = NhanVien.query.count()

            return jsonify({
                'status': 'success',
                'counter': {
                    'medical_amount': medical_amount,
                    'doctor_amount': doctor_amount,
                    'nurse_amount': nurse_amount,
                    'staff_amount': staff_amount
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

from flask import Blueprint, render_template,request,redirect,url_for,flash,session,jsonify
from flask_bcrypt import Bcrypt
from myapp import db
from myapp.models import NguoiDung,Sdt,DiaChi,NhanVien,BacSi,Khoa
import json
from myapp.controller.client.client_controller import get_doctor_info as gdri
bcrypt = Bcrypt()

bp = Blueprint('main', __name__)
@bp.route('/')
def index():
    # Tạo nhân viên
#     password="123"
#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#     user = NguoiDung(ho_ten="Nhan Vien", username="nhanvien", password=hashed_password, gioi_tinh=True, cccd="987654", type="nguoi_dung")
# # Tạo admin
#     admin = NhanVien(ho_ten="Admin", username="admin", password=hashed_password, gioi_tinh=True, cccd="123456", type="nhan_vien")
# # Thêm vào cơ sở dữ liệu
#     db.session.add(user)
#     db.session.add(admin)
#     db.session.commit()

    return render_template('index.html')
# Route cho trang đăng nhập
@bp.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    return render_template('admin.html')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kiểm tra xem người dùng có tồn tại trong cơ sở dữ liệu không
        user = NguoiDung.query.filter_by(username=username).first()

        if user:
            # Kiểm tra mật khẩu đã mã hóa trong cơ sở dữ liệu
            if bcrypt.check_password_hash(user.password, password):
                session['username'] = user.username
                session['user_id'] = user.id
                if user.type == 'nhan_vien':  # Kiểm tra nếu user là nhân viên
                    return redirect(url_for('main.admin_dashboard'))  # Chuyển hướng đến trang quản trị nhân viên
                else:
                # Nếu mật khẩu chính xác, đăng nhập thành công và chuyển hướng đến trang chủ
                    return redirect(url_for('main.index'))
            else:
                # Thông báo lỗi nếu mật khẩu sai
                flash('Mật khẩu không đúng!', 'danger')
        else:
            # Thông báo lỗi nếu tài khoản không tồn tại
            flash('Tên tài khoản không đúng!', 'danger')

    return render_template('login.html')


# Route đăng ký
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        gioi_tinh = request.form['gender']
        ho_ten = request.form['fullname']
        cccd = request.form['cccd']
        phone = request.form['phone']
        address = request.form['address']
        
        # Kiểm tra xem mật khẩu có khớp không
        if password != confirm_password:
            flash('Mật khẩu không khớp!', 'danger')
            return redirect(url_for('main.register'))
        
        # Kiểm tra xem tên người dùng đã tồn tại chưa
        user = NguoiDung.query.filter_by(username=username).first()
        if user:
            flash('Tên tài khoản đã tồn tại!', 'danger')
            return redirect(url_for('main.register'))
        
        # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Lưu thông tin người dùng vào cơ sở dữ liệu
        new_user = NguoiDung(
            ho_ten=ho_ten,
            username=username,
            password=hashed_password,
            gioi_tinh=gioi_tinh == 'male',  # Nếu gioi_tinh = 'male', sẽ lưu True cho giới tính nam
            cccd=cccd
        )
        db.session.add(new_user)
        db.session.commit()

        # Sau khi tạo người dùng, thêm số điện thoại và địa chỉ
        new_sdt = Sdt(so_dien_thoai=phone, nguoi_dung_id=new_user.id)
        new_dia_chi = DiaChi(dia_chi=address, nguoi_dung_id=new_user.id)
        db.session.add(new_dia_chi,new_sdt)
        db.session.commit()
        # Thêm số điện thoại và địa chỉ vào cơ sở dữ liệu
        flash('Đăng ký thành công! Hãy đăng nhập ngay.', 'success')
        return redirect(url_for('main.login'))  # Chuyển hướng đến trang đăng nhập

    return render_template('register.html')



@bp.route('/logout')
def logout():
    # Xoá session của người dùng
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('main.index'))  # Quay lại trang chủ

# Route cho trang quên mật khẩu
@bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')
@bp.route('/api/doctors', methods=['GET'])
def get_doctors():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    khoa_id = request.args.get('khoa_id', None, type=int)

    query = BacSi.query

    # Lọc theo khoa nếu có khoa_id
    if khoa_id:
        query = query.filter(BacSi.khoa_id == khoa_id)

    doctors_paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    doctor_list = [
        {
            "id": doctor.id,
            "ho_ten": doctor.ho_ten,
            "khoa": doctor.khoa.ten_khoa if doctor.khoa else "Chưa có khoa",
            "avatar": doctor.avatar
        }
        for doctor in doctors_paginated.items
    ]

    return jsonify({
        "doctors": doctor_list,
        "total": doctors_paginated.total,
        "pages": doctors_paginated.pages,
        "current_page": doctors_paginated.page
    })




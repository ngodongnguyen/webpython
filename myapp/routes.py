from flask import Blueprint, render_template,request,redirect,url_for,flash,session,jsonify
from flask_bcrypt import Bcrypt
from myapp import db
from myapp.models import NguoiDung,Sdt,DiaChi,NhanVien,BacSi,Khoa,DanhSachDangKyKham,DangKyKham,YTa,BenhNhan,Email
import json
from myapp.controller.client.client_controller import get_doctor_info as gdri
from sqlalchemy import func
from datetime import datetime,date
from sqlalchemy.exc import IntegrityError
import re


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

    try:
        # Fetch the total number of registrations
        total_slots = 30  # Example: Total number of slots available per day
        registered_count = DangKyKham.query.count()
        remaining_slots = max(0, total_slots - registered_count)  # Ensure non-negative slots

        # Pass remainingSlots to the template
        return render_template('index.html', remainingSlots=remaining_slots)
    except Exception as e:
        # Handle potential errors
        return render_template('index.html', remainingSlots=0, error=str(e))# Route cho trang đăng nhập
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
            "ho": doctor.ho,
            "ten": doctor.ten,
            "khoa": doctor.khoa.ten_khoa if doctor.khoa else "Chưa có khoa",
            "avatar": doctor.avatar,
            "sdt": [s.so_dien_thoai for s in doctor.sdt],  # Lấy danh sách số điện thoại
            "emails": [e.email for e in doctor.emails],  # Lấy danh sách email
            "dia_chi": [d.dia_chi for d in doctor.dia_chi]  # Lấy danh sách địa chỉ
        }
        for doctor in doctors_paginated.items
    ]

    return jsonify({
        "doctors": doctor_list,
        "total": doctors_paginated.total,
        "pages": doctors_paginated.pages,
        "current_page": doctors_paginated.page
    })
@bp.route('/api/counter', methods=['GET'])
def get_counters():
    try:
        # Đếm số lượng trong từng bảng
        medical_amount = DangKyKham.query.count()  # Số lượng đăng ký khám
        doctor_amount = BacSi.query.count()       # Số lượng bác sĩ
        nurse_amount = YTa.query.count()         # Số lượng y tá
        staff_amount = NhanVien.query.count()    # Số lượng nhân viên

        # Trả về kết quả dạng JSON
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
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
@bp.route('/api/get_slots', methods=['GET'])
def get_slots():
    from datetime import datetime, timedelta

    today = datetime.now()
    max_days = 30
    slots = {}

    # Dữ liệu slot mẫu
    for i in range(max_days):
        date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
        slots[date] = 10 if i % 5 != 0 else 0  # Ví dụ: hết slot mỗi 5 ngày

    return jsonify({"status": "success", "slots": slots})
@bp.route('/api/check_slots', methods=['GET'])
def check_slots():
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'Invalid date'}), 400

    # Count the number of registrations for the selected date
    count = db.session.query(func.count(DangKyKham.id)).filter(DangKyKham.ngay_dang_ky == date).scalar()
    remaining_slots = max(0, 30 - count)

    return jsonify({'remainingSlots': remaining_slots})


from sqlalchemy.exc import IntegrityError

@bp.route('/api/client/online_registration', methods=['POST'])
def online_registration():
    try:
        # Lấy dữ liệu từ form
        ho = request.form.get('last_name')
        ten = request.form.get('first_name')
        gioi_tinh = request.form.get('sex') == 'male'
        ngay_sinh = request.form.get('date_of_birth')
        cccd = request.form.get('id_card')
        so_dien_thoai = request.form.get('phone_number')
        email = request.form.get('email')
        dia_chi = request.form.get('address')
        ngay_dang_ky = request.form.get('registration_date')

        # Kiểm tra ngày sinh phải nhỏ hơn hôm nay
        if date.fromisoformat(ngay_sinh) >= date.today():
            flash('Ngày sinh phải nhỏ hơn ngày hiện tại!', 'error')
            return redirect(url_for('main.index'))  # Thay 'main.index' bằng route form của bạn

        # Kiểm tra CCCD đã đăng ký trong ngày chưa
        existing_registration = (
            db.session.query(DangKyKham)
            .join(BenhNhan, DangKyKham.id_benh_nhan == BenhNhan.id)
            .filter(BenhNhan.cccd == cccd, DangKyKham.ngay_dang_ky == ngay_dang_ky)
            .first()
        )
        if existing_registration:
            flash('CCCD đã được đăng ký trong ngày hôm nay!', 'error')
            return redirect(url_for('main.index'))

        # Tạo bệnh nhân
        benh_nhan = BenhNhan(ho=ho, ten=ten, gioi_tinh=gioi_tinh, ngay_sinh=ngay_sinh, cccd=cccd)
        db.session.add(benh_nhan)
        db.session.flush()  # Lưu tạm để lấy ID

        # Lưu số điện thoại
        if so_dien_thoai:
            db.session.add(Sdt(so_dien_thoai=so_dien_thoai, nguoi_dung_id=benh_nhan.id))

        # Lưu email
        if email:
            db.session.add(Email(email=email, nguoi_dung_id=benh_nhan.id))

        # Lưu địa chỉ
        if dia_chi:
            db.session.add(DiaChi(dia_chi=dia_chi, nguoi_dung_id=benh_nhan.id))

        # Lưu đăng ký khám
        db.session.add(DangKyKham(ngay_dang_ky=ngay_dang_ky, id_benh_nhan=benh_nhan.id))
        db.session.commit()

        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('main.index'))

    except IntegrityError as e:
        db.session.rollback()
        # Lấy thông tin chi tiết từ IntegrityError
        error_message = str(e.orig)  # Thông báo lỗi chi tiết từ cơ sở dữ liệu
        flash(f'Lỗi khi lưu thông tin: {error_message}', 'error')
        return redirect(url_for('main.index'))

    except Exception as e:
        db.session.rollback()
        # Xóa bệnh nhân nếu tạo thất bại
        if 'benh_nhan' in locals():
            db.session.delete(benh_nhan)
            db.session.commit()
        flash(f'Đã xảy ra lỗi không xác định: {e}', 'error')
        return redirect(url_for('main.index'))

@bp.context_processor
def inject_today_date():
    return {'today_date': date.today().isoformat()}
def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

# Hàm kiểm tra định dạng số điện thoại
def is_valid_phone(phone):
    regex = r'^\d{9,10}$'  # Số điện thoại Việt Nam thường có 10 chữ số
    return re.match(regex, phone) is not None
@bp.route('/api/check_cccd', methods=['POST'])
def check_cccd():
    data = request.json
    cccd = data.get('cccd')
    ngay_dang_ky = data.get('ngay_dang_ky')

    # Kiểm tra đầu vào
    if not cccd or not ngay_dang_ky:
        return jsonify({'error': 'CCCD và ngày đăng ký là bắt buộc!'}), 400

    # Kiểm tra CCCD đã đăng ký trong ngày này chưa
    existing_registration = (
        db.session.query(DangKyKham)
        .join(BenhNhan, DangKyKham.id_benh_nhan == BenhNhan.id)
        .filter(BenhNhan.cccd == cccd, DangKyKham.ngay_dang_ky == ngay_dang_ky)
        .first()
    )

    if existing_registration:
        return jsonify({'exists': True, 'message': 'CCCD đã được đăng ký trong ngày này!'}), 200

    return jsonify({'exists': False, 'message': 'CCCD hợp lệ.'}), 200



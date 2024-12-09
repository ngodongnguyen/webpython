from flask import Blueprint, render_template,request,redirect,url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
# Route cho trang đăng nhập
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Kiểm tra thông tin đăng nhập (thực hiện xác thực)
        # Ví dụ: Kiểm tra cơ sở dữ liệu nếu tên tài khoản và mật khẩu đúng
        if username == 'admin' and password == '123456':  # Thay thế logic kiểm tra
            return redirect(url_for('main.index'))  # Sau khi đăng nhập thành công, chuyển đến trang chủ
        else:
            # Thông báo lỗi nếu thông tin không hợp lệ
            return render_template('login.html', error="Tên tài khoản hoặc mật khẩu không đúng.")
    return render_template('login.html')

# Route cho trang đăng ký tài khoản mới
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Thực hiện logic đăng ký tài khoản mới
        # Lưu thông tin người dùng vào cơ sở dữ liệu
        return redirect(url_for('main.login'))  # Chuyển hướng đến trang đăng nhập sau khi đăng ký
    return render_template('register.html')

# Route cho trang quên mật khẩu
@bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

import datetime
import hashlib
from myapp.models import NhanVien,Sdt,DiaChi,Email
from myapp import db

def get_account(username=None, password=None):
    if username and password:
        return NhanVien.query.filter(NhanVien.username.__eq__(username),
                                         NhanVien.password.__eq__(
                                             hashlib.md5(password.encode('utf8')).hexdigest())).first()


def get_account_by_id(account_id=None):
    if account_id:
        return NhanVien.query.get(account_id)

def get_info_current_user(username=None):
    # Lấy thông tin người dùng dựa trên username
    data = db.session.query(
        NhanVien.ho,
        NhanVien.ten,
        NhanVien.ngay_sinh,
        NhanVien.gioi_tinh,
        Sdt.so_dien_thoai,
        DiaChi.dia_chi,
        Email.email,
        NhanVien.type,
        NhanVien.avatar
    ).select_from(NhanVien) \
        .join(Sdt, Sdt.nguoi_dung_id == NhanVien.id, isouter=True) \
        .join(DiaChi, DiaChi.nguoi_dung_id == NhanVien.id, isouter=True) \
        .join(Email, Email.nguoi_dung_id == NhanVien.id, isouter=True) \
        .filter(NhanVien.username == username).first()

    # Kiểm tra nếu không có dữ liệu
    if data is None:
        return None

    # Chuyển đổi giới tính thành chuỗi 'Nam' hoặc 'Nữ'
    gioi_tinh = 'Nam' if data[3] else 'Nữ'

    # Trả về kết quả dưới dạng từ điển
    return {
        'ho': data[0],
        'ten': data[1],
        'ngay_sinh': data[2].strftime('%d/%m/%Y') if data[2] else None,
        'gioi_tinh': gioi_tinh,
        'so_dien_thoai': data[4] if data[4] else 'Không có',
        'dia_chi': data[5] if data[5] else 'Không có',
        'email': data[6] if data[6] else 'Không có',
        'loai_nhan_vien': data[7] if data[7] else 'Không xác định',
        'avatar': data[8] if data[8] else 'Không có'
    }

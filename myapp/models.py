from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey,Enum
from sqlalchemy.orm import relationship
from myapp.extensions import db
from sqlalchemy.orm import validates
from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property


class NguoiDung(db.Model):
    __tablename__ = 'nguoi_dung'
    id = db.Column(db.Integer, primary_key=True)
    ho = db.Column(db.String(100), nullable=False)
    ten = db.Column(db.String(100), nullable=False)
    gioi_tinh = db.Column(db.Boolean, nullable=False)
    cccd = db.Column(db.String(12), unique=False)
    ngay_sinh = db.Column(db.Date,nullable=False)
    sdt = db.relationship('Sdt', backref='nguoi_dung_s', lazy=True,cascade="all, delete-orphan")
    emails = db.relationship('Email', backref='nguoi_dung_s', lazy=True,cascade="all, delete-orphan")

    # Liên kết đến địa chỉ
    dia_chi = db.relationship('DiaChi', backref='nguoi_dung_s', lazy=True,cascade="all, delete-orphan")
    __mapper_args__ = {
        'polymorphic_identity': 'nguoi_dung',  # Định danh lớp cơ sở
        'polymorphic_on': None                 # Không cần `type` ở đây
    }


class NhanVien(UserMixin,NguoiDung):
    __tablename__ = 'nhan_vien'
    id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)  # Thêm cột avatar
    type = db.Column(db.String(20), nullable=False)  # Phân loại 'bac_si', 'y_ta', 'thu_ngan'
    __mapper_args__ = {
        'polymorphic_identity': 'nhan_vien',
        'polymorphic_on': type
    }
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class BacSi(NhanVien):
    __tablename__ = 'bac_si'
    id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), primary_key=True)
    khoa_id = db.Column(db.Integer, db.ForeignKey('khoa.id'))  # Liên kết với bảng Khoa
    khoa = db.relationship('Khoa', backref='bac_si_list', lazy=True)  # Mối quan hệ với Khoa

    __mapper_args__ = {
        'polymorphic_identity': 'bac_si',
    }
    phieu_kham_benh = db.relationship('PhieuKhamBenh', backref='bac_si_phieu_kham', lazy=True)
    # Quan hệ với Sdt, DiaChi, Email thông qua `NguoiDung`
    @hybrid_property
    def full_name(self):
        return f"{self.ho} {self.ten}"
class Khoa(db.Model):
    __tablename__ = 'khoa'
    id = db.Column(db.Integer, primary_key=True)
    ten_khoa = db.Column(db.String(100), nullable=False)  # Tên khoa
    mo_ta = db.Column(db.String(255), nullable=True)  # Mô tả về khoa
    bac_sis = db.relationship('BacSi', backref='danh_sach_bac_si', lazy=True)  # Liên kết đến bác sĩ


class ThuNgan(NhanVien):
    __tablename__ = 'thu_ngan'
    id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'thu_ngan',
    }


class YTa(NhanVien):
    __tablename__ = 'y_ta'
    id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'y_ta',
    }


class BenhNhan(NguoiDung):
    __tablename__ = 'benh_nhan'
    id = db.Column(
        db.Integer,
        db.ForeignKey('nguoi_dung.id', ondelete='CASCADE'),  # Kích hoạt xóa tự động
        primary_key=True
    )
    __mapper_args__ = {
        'polymorphic_identity': 'benh_nhan',
    }

class Sdt(db.Model):
    __tablename__ = 'sdt'
    id = db.Column(db.Integer, primary_key=True)
    so_dien_thoai = db.Column(db.String(15), nullable=False)
    nguoi_dung_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    
    nguoi_dung = db.relationship('NguoiDung', backref='so_dien_thoai_s', lazy=True  # Tắt kiểm tra kiểu
)
class DiaChi(db.Model):
    __tablename__ = 'dia_chi'
    id = db.Column(db.Integer, primary_key=True)
    dia_chi = db.Column(db.String(255), nullable=False)
    nguoi_dung_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    
    nguoi_dung = db.relationship('NguoiDung', backref='dia_chi_s', lazy=True)

class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False, nullable=False)
    nguoi_dung_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    
    nguoi_dung = db.relationship('NguoiDung', backref='email_addresses', lazy=True)

    def __repr__(self):
        return f"<Email {self.email}>"




class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieu_kham_benh'
    id = db.Column(db.Integer, primary_key=True)
    trieu_chung = db.Column(db.String(255))
    chuan_doan = db.Column(db.String(255))
    ngay_kham = db.Column(db.Date, nullable=False)
    # Khóa ngoại liên kết với Bệnh Nhân (1 bệnh nhân có thể có nhiều phiếu khám)
    benh_nhan_id = db.Column(db.Integer, db.ForeignKey('benh_nhan.id'), nullable=False)
    
    # Mối quan hệ với Bệnh Nhân (1 bệnh nhân có thể có nhiều phiếu khám)
    benh_nhan = db.relationship('BenhNhan', backref='phieu_kham_benh', lazy=True)
    
    # Mối quan hệ với ChiTietDonThuoc (1 phiếu khám có thể có nhiều chi tiết đơn thuốc)
    thuoc = db.relationship('ChiTietDonThuoc', backref='chi_tiet_don_thuoc', lazy=True)
    
    # Khóa ngoại liên kết đến DanhSachPhieuKhamBenh
    danhsach_id = db.Column(db.Integer, db.ForeignKey('danh_sach_phieu_kham_benh.id'),nullable=False)
    
    # Khóa ngoại và mối quan hệ với Bác Sĩ (1 bác sĩ có thể khám cho nhiều bệnh nhân)
    bac_si_id = db.Column(db.Integer, db.ForeignKey('bac_si.id'), nullable=False)
    bac_si = db.relationship('BacSi', backref='bac_si_phieu_kham', lazy=True)
    
    # Mối quan hệ với HoaDon (1 phiếu khám có thể có một hóa đơn)
    hoa_don = db.relationship('HoaDon', backref='hoa_don_phieu_kham', lazy=True)
    
    # Mối quan hệ với DanhSachPhieuKhamBenh (mỗi phiếu khám bệnh thuộc một danh sách)
    danhsach = db.relationship('DanhSachPhieuKhamBenh', backref='phieu_kham_benh', lazy=True)


class DanhSachPhieuKhamBenh(db.Model):
    __tablename__ = 'danh_sach_phieu_kham_benh'
    id = db.Column(db.Integer, primary_key=True)
    ngay_tao = db.Column(db.Date, nullable=False, unique=True)  # Thêm trường 'ngay_tao'
    tong_so = db.Column(db.Integer, default=0)



class ChiTietDonThuoc(db.Model):
    __tablename__ = 'chi_tiet_don_thuoc'
    
    thuoc_id = db.Column(db.Integer, db.ForeignKey('thuoc.id'), primary_key=True)
    phieu_kham_id = db.Column(db.Integer, db.ForeignKey('phieu_kham_benh.id'), primary_key=True)
    so_luong_thuoc = db.Column(db.Integer)

    # Mối quan hệ với Thuốc và Phiếu Khám Bệnh
    thuoc = db.relationship('Thuoc', backref='chi_tiet_don_thuoc')
    phieu_kham_benh = db.relationship('PhieuKhamBenh', backref='chi_tiet_don_thuoc')



class Thuoc(db.Model):
    __tablename__ = 'thuoc'
    id = db.Column(db.Integer, primary_key=True)
    ten_thuoc = db.Column(db.String(100), nullable=False)
    loai = db.Column(Enum('Chai', 'Viên', 'Vỉ', name='loai_thuoc_enum'), nullable=False)  # Loại thuốc: Chai, Viên, Vỉ
    so_luong = db.Column(db.Integer, nullable=False)
    gia_tien = db.Column(db.Float, nullable=False)
    huong_dan_su_dung = db.Column(db.String(255), nullable=True)  # Hướng dẫn sử dụng (có thể để trống)

    def __repr__(self):
        return (f"<Thuoc(id={self.id}, ten_thuoc={self.ten_thuoc}, loai={self.loai}, "
                f"so_luong={self.so_luong}, gia_tien={self.gia_tien}, huong_dan_su_dung={self.huong_dan_su_dung})>")

class HoaDon(db.Model):
    __tablename__ = 'hoa_don'
    id = db.Column(db.Integer, primary_key=True)
    ngay_tinh_tien = db.Column(db.Date, nullable=False)
    tien_kham_benh = db.Column(db.Float, nullable=False)
    tien_thuoc = db.Column(db.Float, nullable=True)
    tong_tien = db.Column(db.Float, nullable=False)

    # Liên kết với Phiếu Khám Bệnh
    phieu_kham_id = db.Column(db.Integer, db.ForeignKey('phieu_kham_benh.id'), nullable=False)
    phieu_kham_benh = db.relationship('PhieuKhamBenh', backref=db.backref('hoa_don_phieu_kham', uselist=False))

    # Liên kết với Bệnh Nhân
    benh_nhan_id = db.Column(db.Integer, db.ForeignKey('benh_nhan.id'), nullable=False)
    benh_nhan = db.relationship('BenhNhan', backref=db.backref('hoa_don', lazy=True))

    # Liên kết với Thu Ngân
    thu_ngan_id = db.Column(db.Integer, db.ForeignKey('thu_ngan.id'), nullable=False)
    thu_ngan = db.relationship('ThuNgan', backref=db.backref('hoa_don', lazy=True))





class DangKyKham(db.Model):
    __tablename__ = 'dang_ky_kham'
    id = db.Column(db.Integer, primary_key=True)
    ngay_dang_ky = db.Column(db.Date, nullable=False)
    
    # Liên kết với Bệnh Nhân
    id_benh_nhan = db.Column(db.Integer, db.ForeignKey('benh_nhan.id'), nullable=False)
    
    # Liên kết với Y Tá
    id_y_ta = db.Column(db.Integer, db.ForeignKey('y_ta.id'), nullable=True)
    
    # Khóa ngoại tham chiếu tới DanhSachDangKyKham
    danh_sach_id = db.Column(db.Integer, db.ForeignKey('danh_sach_dang_ky_kham.id'), nullable=False)
    
    # Mối quan hệ với Bệnh Nhân
    benh_nhan = db.relationship('BenhNhan', backref='dang_ky_kham', lazy=True)
    
    # Mối quan hệ với Y Tá
    y_ta = db.relationship('YTa', backref='dang_ky_kham', lazy=True)
    
    # Mối quan hệ với DanhSachDangKyKham
    danh_sach = db.relationship('DanhSachDangKyKham', backref='dang_ky_kham', lazy=True)

    @validates('ngay_dang_ky')
    def validate_ngay_dang_ky(self, key, value):
        """
        Tự động thêm vào danh sách đăng ký dựa trên ngày đăng ký.
        """
        danh_sach = DanhSachDangKyKham.query.filter_by(ngay_dang_ky=value).first()
        if not danh_sach:
            danh_sach = DanhSachDangKyKham(ngay_dang_ky=value)
            db.session.add(danh_sach)
            db.session.flush()  # Đảm bảo danh sách mới được thêm vào database
        self.danh_sach_id = danh_sach.id
        return value


class DanhSachDangKyKham(db.Model):
    __tablename__ = 'danh_sach_dang_ky_kham'
    id = db.Column(db.Integer, primary_key=True)
    ngay_dang_ky = db.Column(db.Date, nullable=False, unique=True)
    danh_sach = db.relationship('DangKyKham', backref='danh_sach_dang_ky_kham', lazy=True)



class QuanTri(NhanVien):
    __tablename__ = 'quan_tri'
    id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), primary_key=True)
    quyen_han = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'quan_tri',
    }
class ThongKe(db.Model):
    __tablename__ = 'thong_ke'
    id = db.Column(db.Integer, primary_key=True)
    ten_bao_cao = db.Column(db.String(100))
    noi_dung = db.Column(db.Text)
    ngay_thong_ke = db.Column(db.Date)

    # Khóa ngoại liên kết đến QuanTri (Mỗi Thống Kê có thể thuộc một Quản Trị viên)
    quan_tri_id = db.Column(db.Integer, db.ForeignKey('quan_tri.id'), nullable=False)

    # Mối quan hệ ngược lại với QuanTri
    quan_tri = db.relationship('QuanTri', backref='thong_ke', lazy=True)




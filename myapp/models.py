from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from myapp import db,create_app


class NguoiDung(db.Model):
    __tablename__ = 'nguoi_dung'
    id = db.Column(db.Integer, primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gioi_tinh = db.Column(db.Boolean, nullable=False)
    cccd = db.Column(db.String(12), unique=True)
    sdt = db.Column(db.String(15))
    dia_chi = db.Column(db.String(255))
    type = db.Column(db.String(50))  # For polymorphism

    __mapper_args__ = {
        'polymorphic_identity': 'nguoi_dung',
        'polymorphic_on': type
    }

class NhanVien(NguoiDung):
    __tablename__ = 'nhan_vien'
    id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), primary_key=True)
    chuc_vu = db.Column(db.String(100))
    __mapper_args__ = {
        'polymorphic_identity': 'nhan_vien',
    }


class BacSi(NhanVien):
    __tablename__ = 'bac_si'
    id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), primary_key=True)
    chuyen_khoa = db.Column(db.String(100))
    __mapper_args__ = {
        'polymorphic_identity': 'bac_si',
    }
    phieu_kham_benh = db.relationship('PhieuKhamBenh', backref='bac_si', lazy=True)



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
    id = db.Column(db.Integer,db.ForeignKey('nguoi_dung.id'), primary_key=True,)
    __mapper_args__ = {
        'polymorphic_identity': 'benh_nhan',
    }





class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieu_kham_benh'
    id = db.Column(db.Integer, primary_key=True)
    trieu_chung = db.Column(db.String(255))
    chuan_doan = db.Column(db.String(255))
    
    # Mối quan hệ với ChiTietDonThuoc
    thuoc = db.relationship('ChiTietDonThuoc', backref='phieu_kham_benh', lazy=True)
    
    # Khóa ngoại liên kết đến DanhSachPhieuKhamBenh
    danhsach_id = db.Column(db.Integer, db.ForeignKey('danh_sach_phieu_kham_benh.id'))
    
    # Khóa ngoại và mối quan hệ với BacSi và HoaDon
    bac_si_id = db.Column(db.Integer, db.ForeignKey('bac_si.id'))
    hoa_don_id = db.Column(db.Integer, db.ForeignKey('hoa_don.id'))
    
    bac_si = db.relationship('BacSi', backref='phieu_kham_benh', lazy=True)
    hoa_don = db.relationship('HoaDon', backref='phieu_kham_benh', lazy=True)
    
    # Mối quan hệ với DanhSachPhieuKhamBenh (mỗi phiếu khám bệnh thuộc một danh sách)
    danhsach = db.relationship('DanhSachPhieuKhamBenh', backref='phieu_kham_benh', lazy=True)

class DanhSachPhieuKhamBenh(db.Model):
    __tablename__ = 'danh_sach_phieu_kham_benh'
    id = db.Column(db.Integer, primary_key=True)
    phieu_kham_benh = db.relationship('PhieuKhamBenh', backref='danh_sach_phieu_kham_benh', lazy=True)




class ChiTietDonThuoc(db.Model):
    __tablename__ = 'chi_tiet_don_thuoc'
    
    thuoc_id = db.Column(db.Integer, db.ForeignKey('danh_muc_thuoc.id'), primary_key=True)
    phieu_kham_id = db.Column(db.Integer, db.ForeignKey('phieu_kham_benh.id'), primary_key=True)
    so_luong_thuoc = db.Column(db.Integer)

    # Mối quan hệ với Thuốc và Phiếu Khám Bệnh
    thuoc = db.relationship('thuoc', backref='chi_tiet_don_thuoc')
    phieu_kham_benh = db.relationship('PhieuKhamBenh', backref='chi_tiet_don_thuoc')



class Thuoc(db.Model):
    __tablename__ = 'thuoc'
    id = db.Column(db.Integer, primary_key=True)
    ten_thuoc = db.Column(db.String(100))
    so_luong = db.Column(db.Integer)
    loai_id = db.Column(db.Integer, db.ForeignKey('loai_thuoc.id'))
    gia_tien = db.Column(db.Float)
class DanhMucThuoc(db.Model):
    __tablename__ = 'danh_muc_thuoc'
    id = db.Column(db.Integer, primary_key=True)
    ten_thuoc = db.Column(db.String(255), nullable=False)
    mo_ta = db.Column(db.String(500))
    gia_ban = db.Column(db.Float)

    # Mối quan hệ với ChiTietDonThuoc (chi tiết đơn thuốc)
    chi_tiet_thuoc = db.relationship('ChiTietDonThuoc', backref='danh_muc_thuoc', lazy=True)

class LoaiThuoc(db.Model):
    __tablename__ = 'loai_thuoc'
    id = db.Column(db.Integer, primary_key=True)
    ten_loai = db.Column(db.String(100))


class HoaDon(db.Model):
    __tablename__ = 'hoa_don'
    id = db.Column(db.Integer, primary_key=True)
    ngay_tinh_tien = db.Column(db.Date, nullable=False)
    tien_kham_benh = db.Column(db.Float, nullable=False)
    tien_thuoc = db.Column(db.Float, nullable=False)
    tong_tien = db.Column(db.Float, nullable=False)

    # Liên kết với Phiếu Khám Bệnh
    phieu_kham_id = db.Column(db.Integer, db.ForeignKey('phieu_kham_benh.id'), nullable=False)
    phieu_kham_benh = db.relationship('PhieuKhamBenh', backref=db.backref('hoa_don', uselist=False))



class DangKyKham(db.Model):
    __tablename__ = 'dang_ky_kham'
    id = db.Column(db.Integer, primary_key=True)
    ngay_dang_ky = db.Column(db.Date)
    id_benh_nhan = db.Column(db.Integer, db.ForeignKey('benh_nhan.id'))
    id_y_ta = db.Column(db.Integer, db.ForeignKey('y_ta.id'))
    # Khóa ngoại tham chiếu tới DanhSachDangKyKham
    danh_sach_id = db.Column(db.Integer, db.ForeignKey('danh_sach_dang_ky_kham.id'), nullable=False)
    
    # Mối quan hệ với DanhSachDangKyKham
    danh_sach = db.relationship('DanhSachDangKyKham', backref='dang_ky_kham')
class DanhSachDangKyKham(db.Model):
    __tablename__ = 'danh_sach_dang_ky_kham'
    id = db.Column(db.Integer, primary_key=True)
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


if __name__=="__main__":
    with create_app.app_context():
        # db.create_all()
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Laptop")
        # c3 = Category(name="Tablet")
        # db.session.add_all([c1,c2,c3])
        # db.session.commit()
        # import json
        # with open('data/products.json', encoding='utf-8') as f:
        #     products = json.load(f)
        #     for p in products:
        #         prod = Product(**p)
        #         db.session.add(prod)

        import hashlib

        password = str(hashlib.md5("123".encode('utf-8')).hexdigest())

        u = NguoiDung(name="Hau", username="user", password=password)
        db.session.add(u)
        db.session.commit()

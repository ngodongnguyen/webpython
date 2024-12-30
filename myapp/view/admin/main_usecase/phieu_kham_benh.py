from flask import request, render_template, redirect, flash, url_for,jsonify
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from myapp.models import PhieuKhamBenh, BenhNhan, Thuoc, ChiTietDonThuoc, DanhSachPhieuKhamBenh,HoaDon
from myapp.extensions import db
from datetime import datetime
from sqlalchemy import func
import unicodedata
class PhieuKhamBenhView(ModelView):
    # Hiển thị danh sách các cột trong view
    column_list = [
        'id',
        'ngay_kham',
        'trieu_chung',
        'chuan_doan',
        'benh_nhan_full_name',
        'bac_si_full_name',
        'thuoc_info'
    ]

    # Nhãn hiển thị cho các cột
    column_labels = {
        'id': 'Mã phiếu khám',
        'ngay_kham': 'Ngày khám',
        'trieu_chung': 'Triệu chứng',
        'chuan_doan': 'Chẩn đoán',
        'benh_nhan_full_name': 'Họ tên bệnh nhân',
        'bac_si_full_name': 'Họ tên bác sĩ',
        'thuoc_info': 'Thuốc kê đơn',
    }

    # Định dạng hiển thị dữ liệu
    column_formatters = {
        'benh_nhan_full_name': lambda v, c, m, p: f"{m.benh_nhan.ho} {m.benh_nhan.ten}" if m.benh_nhan else "N/A",
        'bac_si_full_name': lambda v, c, m, p: f"{m.bac_si.ho} {m.bac_si.ten}" if m.bac_si else "N/A",
        'thuoc_info': lambda v, c, m, p: "\n".join([
            f"{ct.thuoc.ten_thuoc} - {ct.so_luong_thuoc} {ct.thuoc.loai} ({ct.thuoc.huong_dan_su_dung or 'Không có hướng dẫn'})"
            for ct in m.thuoc
        ]) if m.thuoc else "Không có thuốc"
    }

    # Ghi đè phương thức create_view để sử dụng giao diện tùy chỉnh
    @expose('/new', methods=['GET', 'POST'])
    def create_view(self):
        if not self.is_accessible():
            return self.inaccessible_callback(name='create')

        if request.method == 'POST':
            try:
                # Lấy dữ liệu từ form
                benh_nhan_name = request.form.get('benh_nhan_search')
                print(f"DEBUG: Tên bệnh nhân nhập vào: {benh_nhan_name}")

                # Chuẩn hóa tên bệnh nhân nhập vào từ form
                term_normalized = unicodedata.normalize('NFC', benh_nhan_name.strip())
                print(f"DEBUG: Tên bệnh nhân sau khi chuẩn hóa: {term_normalized}")

                trieu_chung = request.form.get('trieu_chung')
                chuan_doan = request.form.get('chuan_doan')
                thuoc_ids = request.form.getlist('thuoc_id')
                so_luong_thuocs = request.form.getlist('so_luong')

                # Kiểm tra và tìm bệnh nhân bằng tên đã chuẩn hóa
                benh_nhans = BenhNhan.query.filter(
                    func.concat(func.trim(BenhNhan.ho), ' ', func.trim(BenhNhan.ten)).ilike(f"%{term_normalized}%")
                ).all()

                if not benh_nhans:
                    print("DEBUG: Không tìm thấy bệnh nhân trong cơ sở dữ liệu.")
                    flash("Không tìm thấy bệnh nhân.", "error")
                    return self.render('admin/create_phieu_kham.html', thuoc_choices=Thuoc.query.all())
                else:
                    print(f"DEBUG: Tìm thấy bệnh nhân: {benh_nhans[0].ho} {benh_nhans[0].ten}")

                # Tạo phiếu khám bệnh
                ngay_kham = datetime.today().date()
                bac_si_id = current_user.id

                # Kiểm tra danh sách phiếu khám
                danhsach = DanhSachPhieuKhamBenh.query.filter_by(ngay_tao=ngay_kham).first()
                if not danhsach:
                    print("DEBUG: Tạo mới danh sách phiếu khám bệnh.")
                    danhsach = DanhSachPhieuKhamBenh(tong_so=0, ngay_tao=ngay_kham)
                    db.session.add(danhsach)
                    db.session.commit()

                phieu_kham = PhieuKhamBenh(
                    ngay_kham=ngay_kham,
                    trieu_chung=trieu_chung,
                    chuan_doan=chuan_doan,
                    benh_nhan_id=benh_nhans[0].id,
                    bac_si_id=bac_si_id,
                    danhsach_id=danhsach.id
                )
                db.session.add(phieu_kham)
                db.session.flush()

                # Thêm thuốc vào phiếu khám và tính tiền thuốc
                tien_thuoc = 0
                for thuoc_id, so_luong in zip(thuoc_ids, so_luong_thuocs):
                    if int(so_luong) > 0:
                        thuoc = Thuoc.query.get(int(thuoc_id))
                        if not thuoc:
                            flash(f"Không tìm thấy thuốc với ID {thuoc_id}.", "error")
                            return self.render('admin/create_phieu_kham.html', thuoc_choices=Thuoc.query.all())

                        # Thêm chi tiết đơn thuốc
                        chi_tiet_thuoc = ChiTietDonThuoc(
                            phieu_kham_id=phieu_kham.id,
                            thuoc_id=int(thuoc_id),
                            so_luong_thuoc=int(so_luong)
                        )
                        db.session.add(chi_tiet_thuoc)

                        # Tính tổng tiền thuốc
                        tien_thuoc += thuoc.gia_tien * int(so_luong)
                        if thuoc.so_luong >= int(so_luong):
                            thuoc.so_luong -= int(so_luong)  # Giảm số lượng thuốc
                            db.session.commit()  # Cập nhật bảng Thuoc sau khi giảm số lượng
                        else:
                            flash(f"Số lượng thuốc {thuoc.ten_thuoc} không đủ để xuất.", "error")
                            db.session.rollback()  # Nếu không đủ số lượng thuốc, rollback giao dịch
                            return self.render('admin/create_phieu_kham.html', thuoc_choices=Thuoc.query.all())
                # Tự động tạo hóa đơn
                tien_kham = 100000  # Giá trị mặc định của tiền khám bệnh
                tong_tien = tien_kham + tien_thuoc

                hoa_don = HoaDon(
                    ngay_tinh_tien=ngay_kham,
                    tien_kham_benh=tien_kham,
                    tien_thuoc=tien_thuoc,
                    tong_tien=tong_tien,
                    phieu_kham_id=phieu_kham.id,
                    benh_nhan_id=benh_nhans[0].id,
                    thu_ngan_id=benh_nhans[0].id  # Cập nhật nếu có logic xử lý thêm
                )
                db.session.add(hoa_don)

                # Cập nhật danh sách phiếu khám
                danhsach.tong_so += 1
                db.session.commit()
                flash("Tạo phiếu khám và hóa đơn thành công!", "success")
                return redirect(self.get_url('.index_view'))

            except Exception as e:
                db.session.rollback()
                flash(f"Lỗi khi tạo phiếu khám: {e}", "error")

        # Hiển thị giao diện tùy chỉnh
        thuoc_choices = Thuoc.query.all()
        return self.render('admin/create_phieu_kham.html', thuoc_choices=thuoc_choices)

    @expose('/autocomplete_benh_nhan', methods=['GET'])
    def autocomplete_benh_nhan(self):
        term = request.args.get('term', '').strip()
        term_normalized = unicodedata.normalize('NFC', term)
        print(f"DEBUG: Giá trị term nhận được: {term}")
        print(f"DEBUG: Giá trị term sau khi chuẩn hóa: {term_normalized}")

        if not term_normalized:
            print("DEBUG: Term rỗng, trả về danh sách trống.")
            return jsonify([])

        try:
            print("DEBUG: Đang thực hiện truy vấn tìm kiếm bệnh nhân...")
            benh_nhans = BenhNhan.query.filter(
                func.concat(func.trim(BenhNhan.ho), ' ', func.trim(BenhNhan.ten)).ilike(f"%{term_normalized}%")
            ).all()

            print(f"DEBUG: Kết quả truy vấn: {benh_nhans}")

            if not benh_nhans:
                print("DEBUG: Không tìm thấy bệnh nhân nào khớp với term.")
                return jsonify([])

            results = []
            for benh_nhan in benh_nhans:
                # Kiểm tra nếu bệnh nhân đã từng khám bệnh
                phieu_kham = PhieuKhamBenh.query.filter_by(benh_nhan_id=benh_nhan.id).all()
                da_kham = len(phieu_kham) > 0
                thong_tin_kham = [
                    {
                        "id": pk.id,
                        "ngay_kham": pk.ngay_kham.strftime('%Y-%m-%d'),
                        "trieu_chung": pk.trieu_chung,
                        "chuan_doan": pk.chuan_doan
                    }
                    for pk in phieu_kham
                ] if da_kham else None

                # Lấy số điện thoại và email nếu có
                sdt = benh_nhan.so_dien_thoai_s[0].so_dien_thoai if benh_nhan.so_dien_thoai_s else "Không có số điện thoại"
                email = benh_nhan.email_addresses[0].email if benh_nhan.email_addresses else "Không có email"

                # Thêm thông tin bệnh nhân vào kết quả
                results.append({
                    "id": benh_nhan.id,
                    "label": f"{benh_nhan.ho} {benh_nhan.ten}",
                    "value": f"{benh_nhan.ho} {benh_nhan.ten}",
                    "info": {
                        "gioi_tinh": "Nam" if benh_nhan.gioi_tinh else "Nữ",
                        "ngay_sinh": benh_nhan.ngay_sinh.strftime('%Y-%m-%d'),
                        "dia_chi": benh_nhan.dia_chi_s[0].dia_chi if benh_nhan.dia_chi_s else "Không có địa chỉ",
                        "sdt": sdt,
                        "email": email,
                        "da_kham": da_kham,
                        "thong_tin_kham": thong_tin_kham
                    }
                })

            print(f"DEBUG: JSON trả về: {results}")
            return jsonify(results)

        except Exception as e:
            print(f"ERROR: Lỗi xảy ra trong quá trình tìm kiếm bệnh nhân: {e}")
            return jsonify([]), 500



    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập vào chức năng này.", "error")
        return redirect(url_for('admin.index'))

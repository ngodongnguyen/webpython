from flask import request, render_template, flash, redirect, url_for
from flask_admin import expose, BaseView
from myapp.models import QuyDinh
from myapp.extensions import db

class QuyDinhView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def edit_view(self):
        print("DEBUG: edit_view called")  # Kiểm tra xem hàm có được gọi không
        
        if request.method == 'POST':
            try:
                # Lấy giá trị từ form
                so_benh_nhan = request.form.get('so_benh_nhan')
                so_tien_kham = request.form.get('so_tien_kham')

                print(f"DEBUG: so_benh_nhan={so_benh_nhan}, so_tien_kham={so_tien_kham}")  # Kiểm tra giá trị form

                # Cập nhật dữ liệu
                quy_dinh = QuyDinh.query.first()  # Lấy QuyDinh hiện tại
                if quy_dinh:
                    quy_dinh.so_benh_nhan = int(so_benh_nhan)
                    quy_dinh.so_tien_kham = float(so_tien_kham)

                    # Commit thay đổi
                    db.session.commit()

                    flash("Cập nhật thành công!", "success")
                    return redirect(url_for('admin.index'))
                else:
                    flash("Quy định không tồn tại.", "error")

            except Exception as e:
                db.session.rollback()
                flash(f"Lỗi khi cập nhật quy định: {e}", "error")

        # Kiểm tra sự tồn tại của QuyDinh và render giao diện
        quy_dinh = QuyDinh.query.first()
        if not quy_dinh:
            flash("Chưa có quy định nào trong cơ sở dữ liệu", "error")
            return redirect(url_for('admin.index'))

        print(f"DEBUG: QuyDinh found: {quy_dinh.so_benh_nhan}, {quy_dinh.so_tien_kham}")  # Kiểm tra dữ liệu quy_dinh

        return self.render('admin/edit_quy_dinh.html', quy_dinh=quy_dinh)

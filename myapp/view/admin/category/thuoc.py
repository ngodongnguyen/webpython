from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, ValidationError
from flask import flash
from myapp.models import Thuoc
from myapp.extensions import db
from sqlalchemy.exc import SQLAlchemyError

class ThuocView(ModelView):
    # Cấu hình hiển thị cột trong giao diện Flask-Admin
    column_list = ['id', 'ten_thuoc', 'loai', 'so_luong', 'gia_tien', 'huong_dan_su_dung']
    column_labels = {
        'id': 'Mã thuốc',
        'ten_thuoc': 'Tên thuốc',
        'loai': 'Loại thuốc',
        'so_luong': 'Số lượng',
        'gia_tien': 'Giá tiền',
        'huong_dan_su_dung': 'Hướng dẫn sử dụng'
    }

    # Định nghĩa form để thêm/sửa bản ghi
    form_columns = ['ten_thuoc', 'loai', 'so_luong', 'gia_tien', 'huong_dan_su_dung']

    # Tùy chỉnh trường `loai` để hiển thị dưới dạng SelectField
    form_overrides = {
        'loai': SelectField
    }

    # Tùy chỉnh các lựa chọn cho trường `loai`
    form_args = {
        'loai': {
            'choices': [('Chai', 'Chai'), ('Viên', 'Viên'), ('Vỉ', 'Vỉ')],
            'label': 'Loại thuốc'
        }
    }

    def on_model_change(self, form, model, is_created):
        try:
            # Kiểm tra số lượng thuốc vượt quá 30
            total_thuoc = Thuoc.query.count()
            if is_created and total_thuoc > 30:
                raise ValidationError("Số lượng thuốc trong cơ sở dữ liệu đã đạt giới hạn tối đa (30 thuốc).")
            
            # Tiếp tục thêm/sửa bản ghi nếu hợp lệ
            super(ThuocView, self).on_model_change(form, model, is_created)
        except ValidationError as e:
            # Hoàn tác mọi thay đổi trong phiên nếu có lỗi
            db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            # Hoàn tác phiên giao dịch nếu có lỗi SQLAlchemy
            db.session.rollback()
            flash("Đã xảy ra lỗi trong cơ sở dữ liệu. Vui lòng thử lại.", 'error')
            raise e

    def handle_view_exception(self, exc):
        if isinstance(exc, ValidationError):
            flash(str(exc), 'error')
        else:
            flash("Đã xảy ra lỗi trong quá trình xử lý. Vui lòng thử lại.", 'error')
        return False  # Trả về False để Flask-Admin xử lý lỗi

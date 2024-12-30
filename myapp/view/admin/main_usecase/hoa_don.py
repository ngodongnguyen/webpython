import logging
from flask_admin.contrib.sqla import ModelView

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HoaDonView(ModelView):
    # Cấu hình các cột hiển thị trong bảng
    column_list = ('id', 'benh_nhan_ho_ten', 'ngay_tinh_tien', 'tien_kham_benh', 'tien_thuoc', 'tong_tien')

    column_labels = {
        'id': 'Mã Hóa Đơn',
        'benh_nhan_ho_ten': 'Họ Tên Bệnh Nhân',
        'ngay_tinh_tien': 'Ngày Tính Tiền',
        'tien_kham_benh': 'Tiền Khám',
        'tien_thuoc': 'Tiền Thuốc',
        'tong_tien': 'Tổng Tiền',
    }

    column_formatters = {
        'benh_nhan_ho_ten': lambda v, c, m, n: f"{m.benh_nhan.ho} {m.benh_nhan.ten}" if m.benh_nhan else "N/A",
        'tong_tien': lambda v, c, m, n: f"{m.tong_tien:,.0f} VND",
        'tien_kham_benh': lambda v, c, m, n: f"{m.tien_kham_benh:,.0f} VND",
        'tien_thuoc': lambda v, c, m, n: f"{m.tien_thuoc or 0:,.0f} VND",
    }

    # Ẩn các hành động Tạo, Sửa, Xóa
    can_create = False
    can_edit = False
    can_delete = False

    # Ghi log khi cố gắng thao tác ngoài ý muốn
    def on_model_change(self, form, model, is_created):
        logger.warning("Attempted to edit a HoaDon instance. This action is not allowed.")
        raise Exception("Hóa đơn không được phép chỉnh sửa trực tiếp!")

    def create_model(self, form):
        logger.warning("Attempted to create a HoaDon instance. This action is not allowed.")
        raise Exception("Hóa đơn được tạo tự động khi lập phiếu khám. Không thể tạo thủ công!")

    def delete_model(self, model):
        logger.warning("Attempted to delete a HoaDon instance. This action is not allowed.")
        raise Exception("Hóa đơn không thể bị xóa!")

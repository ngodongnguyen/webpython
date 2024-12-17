from sqlalchemy import func
from myapp import db

from myapp.models import Khoa
def get_department_amount():
    return {
        'amount': db.session.query(func.count(Khoa.khoa_id)).first()[0]
    }
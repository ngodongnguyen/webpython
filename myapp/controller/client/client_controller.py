from sqlalchemy import func
from myapp import db

from myapp.models import Khoa,BacSi
def get_department_amount():
    return {
        'amount': db.session.query(func.count(Khoa.khoa_id)).first()[0]
    }
def get_doctor_info(major_id=None, begin_index=None, end_index=None):
    data = db.session.query(BacSi.last_name,
                            BacSi.first_name,
                            BacSi.avatar,
                            BacSi.phone_number,
                            Khoa.name,
                            BacSi.facebook_link,
                            BacSi.twitter_link) \
        .join(MajorModel) \
        .filter(MajorModel.major_id.__eq__(DoctorModel.major_id)) \
        .join(DepartmentModel) \
        .filter(DepartmentModel.department_id.__eq__(DoctorModel.contained_department_id))

    if major_id is not None:
        data = data.filter(MajorModel.major_id.__eq__(major_id))

    data = data.order_by(DoctorModel.first_name)

    if begin_index is not None and end_index is not None:
        data = data.slice(begin_index, end_index)

    data = data.all()
    doctor_list = []
    for doctor in data:
        doctor_list.append({
            'full_name': '{} {}'.format(doctor[0], doctor[1]),
            'avatar': doctor[2],
            'phone_number': doctor[3],
            'major': doctor[4],
            'department': doctor[5],
            'facebook_link': doctor[6],
            'twitter_link': doctor[7]
        })
    return doctor_list
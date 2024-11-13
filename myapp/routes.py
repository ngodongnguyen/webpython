# myapp/routes.py
from flask import Blueprint, render_template

# Tạo blueprint
bp = Blueprint('main', __name__)

# Định nghĩa route cho blueprint
@bp.route('/')
def home():
    return render_template('index.html')

from flask_login import current_user
from flask_admin import AdminIndexView
from flask import Flask, redirect, url_for, render_template, flash, Blueprint
from flask_admin.contrib.sqla import ModelView
class HomeView(AdminIndexView):
    def is_accessible(self):
        print("Is user authenticated:", current_user.is_authenticated)
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))  # Chuyển hướng về trang đăng nhập



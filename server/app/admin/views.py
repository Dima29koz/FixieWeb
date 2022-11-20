from flask import redirect, url_for, request
from flask_admin import AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from flask_login import current_user


class AdminModelView(sqla.ModelView):
    can_delete = False
    column_exclude_list = ['pwd', ]
    column_hide_backrefs = False
    column_list = ['user_name', 'user_email', 'is_email_verified', 'roles', 'date']

    def is_accessible(self):
        try:
            return 'Admin' in [role.name for role in current_user.roles]
        except AttributeError:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login', next=request.args.get("next")))


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        try:
            return current_user.has_at_least_one_of_roles('Admin')
        except AttributeError:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login', next=request.args.get("next")))


class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("main.index")

from datetime import datetime

from flask import redirect, url_for, request
from flask_admin.contrib import sqla
from flask_login import current_user


class ServiceModelView(sqla.ModelView):
    can_delete = False
    column_hide_backrefs = False
    column_exclude_list = ['timestamp']
    form_excluded_columns = ['main_services']

    def is_accessible(self):
        try:
            return 'Member' in [role.name for role in current_user.roles]
        except AttributeError:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login', next=request.args.get("next")))

    def on_model_change(self, form, model, is_created):
        if not is_created:
            model.modified = datetime.utcnow()

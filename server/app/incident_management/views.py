from datetime import datetime

from flask import redirect, url_for, request
from flask_admin.contrib import sqla
from flask_login import current_user
from wtforms import IntegerRangeField
from sqlalchemy import func


class IncidentModelView(sqla.ModelView):
    can_delete = False
    can_set_page_size = True
    can_view_details = True

    edit_modal = True
    details_modal = True
    create_modal = True

    edit_modal_template = 'model_view/modal/edit.html'
    create_modal_template = 'model_view/modal/create.html'
    details_modal_template = 'model_view/modal/details.html'

    action_disallowed_list = ['delete']

    form_overrides = dict(
        priority=IntegerRangeField,
        criticality=IntegerRangeField,
    )
    form_widget_args = dict(
        created={'readonly': True},
        modified={'readonly': True},
        priority={'min': 1, 'max': 5, 'class': 'form-range'},
        criticality={'min': 1, 'max': 5, 'class': 'form-range'},
    )

    column_display_pk = True
    column_labels = dict(
        id='ID',
        subject='Тема',
        description='Описание',
        priority='Приоритет',
        criticality='Критичность',
        status='Статус',
        type='Тип',
        creator='Контрагент',
        responsible_employee='Ответственный',
        created='Дата регистрации',
        modified='Дата изменения',
    )

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login', next=request.args.get("next")))

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.creator = current_user
        else:
            model.modified = datetime.utcnow()


class MyIncidentModelView(IncidentModelView):
    can_create = True
    can_edit = False
    column_list = ['created', 'id', 'status', 'type', 'responsible_employee', 'subject', 'description']
    form_excluded_columns = ['status', 'responsible_employee', 'creator', 'priority', 'criticality']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.creator_id == current_user.id)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.creator_id == current_user.id)

    def is_accessible(self):
        try:
            return 'Member' in [role.name for role in current_user.roles]
        except AttributeError:
            return False


class ResponsibleIncidentModelView(IncidentModelView):
    can_create = False
    can_edit = True
    column_list = ['created', 'id', 'status', 'type', 'subject', 'priority', 'criticality', 'creator']
    form_excluded_columns = ['responsible_employee', 'creator']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.responsible_employee_id == current_user.id)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.responsible_employee_id == current_user.id)

    def is_accessible(self):
        try:
            return 'Admin' in [role.name for role in current_user.roles]
        except AttributeError:
            return False

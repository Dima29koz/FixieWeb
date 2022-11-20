from datetime import datetime
from random import choice

from flask import redirect, url_for, request
from flask_admin.contrib import sqla
from flask_login import current_user
from wtforms import IntegerRangeField
from sqlalchemy import func

from server.app.incident_management.models import RequestStatus
from server.app.main.models import get_users_by_role


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
            model.status = RequestStatus.query.filter_by(name='Открыта').first()
            model.responsible_employee = choice(get_users_by_role('Support'))
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
            return current_user.has_at_least_one_of_roles('Member')
        except AttributeError:
            return False


class ResponsibleIncidentModelView(IncidentModelView):
    can_create = False
    can_edit = True
    column_list = ['created', 'id', 'status', 'type', 'subject', 'priority', 'criticality', 'creator']
    form_excluded_columns = ['responsible_employee', 'creator']
    form_widget_args = IncidentModelView.form_widget_args | dict(
        subject={'readonly': True},
        description={'readonly': True},
    )

    def get_query(self):
        return self.session.query(self.model).filter(self.model.responsible_employee_id == current_user.id)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.responsible_employee_id == current_user.id)

    def is_accessible(self):
        try:
            return current_user.has_at_least_one_of_roles('Admin', 'Support')
        except AttributeError:
            return False


class AllIncidentModelView(IncidentModelView):
    can_create = False
    can_edit = True
    can_delete = True
    column_list = [
        'created', 'id', 'status', 'type', 'responsible_employee', 'subject', 'priority', 'criticality', 'creator']

    def is_accessible(self):
        try:
            return current_user.has_at_least_one_of_roles('Admin')
        except AttributeError:
            return False
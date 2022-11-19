from datetime import datetime

from flask import redirect, url_for, request
from flask_admin.contrib import sqla
from flask_login import current_user


class ServiceModelView(sqla.ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_set_page_size = True
    can_view_details = True

    edit_modal = True
    details_modal = True
    create_modal = True

    edit_modal_template = 'model_view/modal/edit.html'
    create_modal_template = 'model_view/modal/create.html'
    details_modal_template = 'model_view/modal/details.html'

    action_disallowed_list = ['delete']
    column_list = ['name', 'price', 'related_services']
    column_details_list = ['name', 'description', 'price', 'created', 'modified', 'related_services', 'main_services']
    form_widget_args = dict(
        created={'readonly': True},
        modified={'readonly': True},
    )
    column_labels = dict(
        name='Название',
        description='Описание',
        price='Стоимость',
        created='Дата добавления',
        modified='Дата изменения',
        related_services='Включенные услуги',
        main_services='Входит в состав услуг',
    )

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

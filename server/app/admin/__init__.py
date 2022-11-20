from flask_admin import Admin

from server.app.admin.views import MyAdminIndexView


def create_admin(app=None):
    return Admin(app, template_mode='bootstrap4', index_view=MyAdminIndexView())


def create_model_viewer(app=None, config=None):
    return Admin(
        app, name='viewer',
        url='/', endpoint='/',
        base_template=config.BASE_TEMPLATE, template_mode='bootstrap4')


def create_incidents_viewer(app=None, config=None):
    return Admin(
        app, name='Инциденты',
        url='/incidents', endpoint='incidents_viewer',
        base_template=config.BASE_INCIDENTS_TEMPLATE, template_mode='bootstrap4')

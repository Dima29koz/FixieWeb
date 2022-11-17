from .views import AdminModelView, MainIndexLink, UserModelView
from server.app import db
from server.app.main.models import User


def configure_admin(app, admin):
    admin.add_view(AdminModelView(User, db.session))
    admin.add_link(MainIndexLink(name="back"))


def configure_model_viewer(app, model_viewer):
    model_viewer.add_view(UserModelView(User, db.session, name='Test', url='/test', endpoint='/test'))

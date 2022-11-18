from .views import AdminModelView, MainIndexLink
from ..services.model_views import ServiceModelView
from server.app import db
from server.app.main.models import User
from ..services.models import Service


def configure_admin(app, admin):
    admin.add_view(AdminModelView(User, db.session))
    admin.add_link(MainIndexLink(name="back"))


def configure_model_viewer(app, model_viewer):
    model_viewer.add_view(ServiceModelView(Service, db.session, name='Услуги', url='/services', endpoint='/services'))

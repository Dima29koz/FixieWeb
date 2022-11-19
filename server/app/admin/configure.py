from .views import AdminModelView, MainIndexLink
from ..incident_management.models import Incident
from ..incident_management.views import MyIncidentModelView, ResponsibleIncidentModelView
from ..services.views import ServiceModelView
from server.app import db
from server.app.main.models import User
from ..services.models import Service


def configure_admin(app, admin):
    admin.add_view(AdminModelView(User, db.session))
    admin.add_link(MainIndexLink(name="back"))


def configure_model_viewer(app, model_viewer):
    model_viewer.add_view(ServiceModelView(
        Service, db.session, name='Услуги', url='/services', endpoint='/services'))


def configure_incidents_viewer(app, incidents_viewer):
    incidents_viewer.add_view(MyIncidentModelView(
        Incident, db.session, name='Исходящие', url='my', endpoint='my'))
    incidents_viewer.add_view(ResponsibleIncidentModelView(
        Incident, db.session, name='В ответственности', url='in_responsibility', endpoint='in_responsibility'))

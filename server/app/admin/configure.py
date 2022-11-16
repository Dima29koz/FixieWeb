from flask_admin.menu import MenuLink

from .views import MicroBlogModelView, MainIndexLink
from server.app import db
from server.app.main.models import User


def configure_admin(app, admin):
    admin.add_view(MicroBlogModelView(User, db.session))
    admin.add_link(MainIndexLink(name="back"))
    # admin.add_link(MenuLink(name='Main Page'))

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
login_manager = LoginManager()
sio = SocketIO()
migrate = Migrate()
mail = Mail()


def create_app(config) -> Flask:
    """
    Creates app and register Blueprints

    :returns: app
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.test_request_context():
        db.create_all()

    from .main import main as main_blueprint
    from .messenger import messenger as messenger_blueprint
    from .api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(messenger_blueprint)
    app.register_blueprint(api_blueprint)

    from .admin import create_admin, create_model_viewer
    from .admin.configure import configure_admin, configure_model_viewer
    with app.app_context():
        admin = create_admin(app=app)
        configure_admin(app, admin)
        model_viewer = create_model_viewer(app=app, config=config)
        configure_model_viewer(app, model_viewer)

    sio.init_app(app, logger=config.LOGGER, manage_session=config.MANAGE_SESSION)

    return app

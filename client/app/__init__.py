from flask import Flask


def create_app(config) -> Flask:
    """
    Creates app and register Blueprints

    :returns: app
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(config)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app

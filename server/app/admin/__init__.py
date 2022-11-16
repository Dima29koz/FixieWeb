from flask_admin import Admin


def create_admin(app=None):
    return Admin(app, template_mode='bootstrap4')

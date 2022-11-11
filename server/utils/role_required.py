from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def allowed_roles(roles: set[str] = None):
    """
    see: https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.roles is None or not roles:
                return redirect(url_for('main.index'))
            if not {r.name for r in current_user.roles}.intersection(roles):
                return redirect(url_for('main.index'))
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper

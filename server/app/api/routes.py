import os

from flask import send_file
from flask_login import login_required

from . import api


@api.route('/api/img/<user_name>')
@login_required
def get_user_avatar(user_name):
    """API for getting user ave image"""
    filename = 'default_avatar.jpg'
    file_path = os.path.join(os.path.split(api.root_path)[0], 'static', 'images', filename)
    return send_file(file_path, mimetype='image/jpg')

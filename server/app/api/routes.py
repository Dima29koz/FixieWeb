import os

from flask import send_file, jsonify
from flask_login import login_required, current_user

from . import api
from ..main.models import get_users_by_role, get_users, get_user_by_name
from ..messenger.models import get_chat_by_recipient, Chat
from ...utils.role_required import allowed_roles


@api.route('/api/img/<user_name>')
@login_required
def get_user_avatar(user_name):
    """API for getting user ave image"""
    filename = 'default_avatar.jpg'
    file_path = os.path.join(os.path.split(api.root_path)[0], 'static', 'images', filename)
    return send_file(file_path, mimetype='image/jpg')


@api.route('/api/users_to_chat')
@login_required
@allowed_roles(roles={'Admin', 'Member'})
def get_allowed_to_chat_users():
    role = 'Admin' if 'Admin' not in [role.name for role in current_user.roles] else 'Member'
    users = get_users_by_role(role)
    return jsonify(
        users=[{'id': user.id, 'name': user.user_name} for user in users],
    )


@api.route('/api/create_chat/<recipient_name>')
@login_required
@allowed_roles(roles={'Admin', 'Member'})
def get_created_chat(recipient_name: str):
    chat = get_chat_by_recipient(recipient_name)
    if not chat:
        chat = Chat(users=[current_user, get_user_by_name(recipient_name)])
    return jsonify(
        id=chat.id,
        name=chat.get_name(),
        members=[{'id': user.id, 'name': user.user_name} for user in chat.users],
    )
import time

from flask_login import current_user
from flask_socketio import Namespace, send, join_room, leave_room, emit

from server.app.main.models import get_user_by_name
from server.app.messenger.models import Message, Chat, get_chat_by_id


class ChatNamespace(Namespace):
    @staticmethod
    def on_message(data: dict):
        """Broadcast messages"""
        msg_text = data.get("msg")
        room_id = data.get("room_id")
        chat = get_chat_by_id(room_id)
        msg = Message(current_user.id, chat.id, msg_text)
        send(msg.to_dict(), room=room_id)

    @staticmethod
    def on_join(data):
        """User joins a room"""
        username = data.get("username")
        room_id = data.get('room_id')
        join_room(room_id)
        emit('load_messages', {'messages': [msg.to_dict() for msg in get_chat_by_id(room_id).messages]})

    @staticmethod
    def on_leave(data):
        """User leaves a room"""
        username = data.get("username")
        room_id = data.get('room_id')
        leave_room(room_id)

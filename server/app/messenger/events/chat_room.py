import time

from flask_login import current_user
from flask_socketio import Namespace, send, join_room, leave_room

from server.app.messenger.models import Message, Chat


class ChatNamespace(Namespace):
    @staticmethod
    def on_message(data: dict):
        """Broadcast messages"""

        msg_text = data.get("msg")
        room_id = data.get("room")
        msg = Message(current_user.id, room_id, msg_text)
        # send(msg.to_dict(), room=room_id)
        send({"username": current_user.user_name, "msg": msg_text, "time_stamp": '123'}, room=room_id)

    @staticmethod
    def on_join(data):
        """User joins a room"""

        username = data["username"]
        room = data["room"]
        join_room(room)
        # Broadcast that new user has joined
        send({"msg": username + " has joined the " + room + " room."}, room=room)

    @staticmethod
    def on_leave(data):
        """User leaves a room"""

        username = data['username']
        room = data['room']
        leave_room(room)
        send({"msg": username + " has left the room"}, room=room)

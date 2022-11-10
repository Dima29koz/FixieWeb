import time

from flask_socketio import Namespace, send, join_room, leave_room


class ChatNamespace(Namespace):
    @staticmethod
    def on_message(data):
        """Broadcast messages"""

        msg = data["msg"]
        username = data["username"]
        room = data["room"]
        time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
        send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

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

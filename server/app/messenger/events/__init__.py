"""initialization of socketIO eventHandlerNamespace"""

from ... import sio
from .chat_room import ChatRoomNamespace

sio.on_namespace(ChatRoomNamespace('/messenger'))

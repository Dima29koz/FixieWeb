"""initialization of socketIO eventHandlerNamespace"""

from ... import sio
from .chat_room import ChatNamespace

sio.on_namespace(ChatNamespace('/chat'))

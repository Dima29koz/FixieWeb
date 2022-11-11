from datetime import datetime

from server.app import db


user_chats = db.Table(
    'user_chats',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'))
)


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    data = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

from datetime import datetime

from server.app import db


user_chats = db.Table(
    'user_chats',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    users = db.relationship('User', secondary='user_chats', backref=db.backref('users', lazy=True))


class Message(db.Model):
    def __init__(self,
                 sender_id,
                 chat_id,
                 msg_text: str):
        self.sender = sender_id
        self.chat = chat_id
        self.data = msg_text
        self.add()

    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    data = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def add(self):
        """added message to DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def to_dict(self) -> dict:
        return {
            'username': self.sender.user_name,
            'msg': self.data,
            'time_stamp': self.timestamp.strftime('%H:%M')
        }

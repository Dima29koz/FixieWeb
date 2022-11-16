from datetime import datetime

from flask_login import current_user

from server.app import db
from server.app.main.models import User, get_user_by_name

user_chats = db.Table(
    'user_chats',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)


class Chat(db.Model):
    def __init__(self, users: list[User]):
        self.name = ', '.join([user.user_name for user in users])
        self.users = users
        self.add()

    __tablename__ = 'chat'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))

    messages = db.relationship('Message', lazy=True)

    def add(self):
        """added message to DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def get_name(self):
        users = self.users.copy()
        users.remove(current_user)
        return ', '.join([user.user_name for user in users])


class Message(db.Model):
    def __init__(self,
                 sender_id,
                 chat_id,
                 msg_text: str):
        self.sender_id = sender_id
        self.chat_id = chat_id
        self.data = msg_text
        self.add()

    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    data = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

    sender = db.relationship("User", foreign_keys=[sender_id])

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
            'timestamp': f'{self.timestamp.isoformat()}Z'
        }


def get_chat_by_recipient(recipient: str):
    return Chat.query.filter(Chat.users.any(User.user_name == current_user.user_name)).filter(
        Chat.users.any(User.user_name == recipient)).first()


def get_chat_by_id(chat_id: int) -> Chat | None:
    """returns user by id if user exists"""
    return Chat.query.filter_by(id=chat_id).first()

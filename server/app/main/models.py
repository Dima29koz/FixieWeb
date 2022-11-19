from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from server.app import login_manager, db


login_manager.login_view = 'main.login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(db.Model, UserMixin):
    """
    This is a User Model

    :param user_name: users nickname
    :type user_name: str
    :param pwd: users password
    :type pwd: str
    :cvar date: date of account creation
    :type date: DateTime
    """

    def __init__(self, user_name: str, user_email: str, pwd: str):
        self.user_name = user_name
        self.user_email = user_email
        self.pwd = generate_password_hash(pwd)
        self.add()

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    pwd = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy=True))
    chats = db.relationship('Chat', secondary='user_chats', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return self.user_name

    def check_password(self, password: str):
        """
        Verified users password.

        :param password: user password
        :type password: str
        :return: result of verification
        :rtype: bool
        """
        return check_password_hash(self.pwd, password)

    def add(self):
        """added user to DB"""
        member = Role.query.filter_by(name='Member').first()
        try:
            self.roles.append(member)
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def set_email(self, new_email: str):
        self.user_email = new_email
        self.is_email_verified = False
        db.session.commit()

    def set_name(self, new_name: str):
        self.user_name = new_name
        db.session.commit()

    def set_pwd(self, new_pwd: str):
        self.pwd = generate_password_hash(new_pwd)
        db.session.commit()

    def verify_email(self):
        self.is_email_verified = True
        db.session.commit()

    def get_token(self, token_type: str, expires_in=600):
        return jwt.encode(
            {token_type: self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token: str, token_type: str):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])[token_type]
        except Exception as _:
            return
        return get_user_by_id(user_id)


def get_user_by_id(user_id: int) -> User | None:
    """returns user by id if user exists"""
    return User.query.filter_by(id=user_id).first()


def get_user_by_name(user_name: str) -> User | None:
    """returns user by user_name if user exists"""
    return User.query.filter_by(user_name=user_name).first()


def get_users_by_role(role_name: str = 'Member') -> list[User]:
    return User.query.join(User.roles).filter(Role.name == role_name).all()


def get_users():
    admin = Role.query.filter_by(name='Admin').first()
    return admin.users


class Role(db.Model):
    def __init__(self, name):
        self.name = name
        self.add()

    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def __repr__(self):
        return self.name

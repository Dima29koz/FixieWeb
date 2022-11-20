from server.app.main.models import User, Role, get_user_by_name
from server.app.incident_management.models import RequestStatus, RequestType


def create_roles():
    roles = ['Admin', 'Employee', 'Support', 'Member']
    for role in roles:
        if not Role.query.filter_by(name=role).first():
            Role(name=role)


def create_request_statuses(db):
    statuses = [
        'Открыта', 'Открыта повторно', 'Принята в исполнение',
        'Прострочено исполнение', 'Отменена', 'Требует согласования',
        'Согласовано', 'Выполнена', 'Завершена',
    ]
    try:
        for status in statuses:
            if not RequestStatus.query.filter_by(name=status).first():
                r_status = RequestStatus(name=status)
                db.session.add(r_status)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def create_request_types(db):
    types = [
        'Инцидент',
    ]
    try:
        for type_ in types:
            if not RequestType.query.filter_by(name=type_).first():
                r_type = RequestType(name=type_)
                db.session.add(r_type)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def create_admin():
    if not get_user_by_name('Admin'):
        user = User(
            user_name='Admin',
            user_email='dima29koz@yandex.ru',
            pwd='admin',
        )
        user.is_email_verified = True
        user.roles.append(Role.query.filter_by(name='Admin').first())
        user.add()


def create_users():
    for i in range(20):
        if not get_user_by_name(f'user{i}'):
            user = User(
                user_name=f'user{i}',
                user_email='dima29koz@yandex.ru',
                pwd='user',
            )
            user.is_email_verified = True
            user.add()

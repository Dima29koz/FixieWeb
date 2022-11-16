from server.app.main.models import User, Role, get_user_by_name


def create_roles():
    roles = ['Admin', 'Member']
    for role in roles:
        if not Role.query.filter_by(name=role).first():
            Role(name=role)


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

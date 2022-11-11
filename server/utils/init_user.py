from server.app.main.models import User, Role, get_user_by_name


def create_admin(db):
    if not get_user_by_name('Admin'):
        user = User(
            user_name='Admin',
            user_email='dima29koz@yandex.ru',
            pwd='admin',
        )
        user.is_email_verified = True
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Member'))
        db.session.add(user)
        db.session.commit()

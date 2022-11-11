import os
from dotenv import load_dotenv
load_dotenv()
from server.app import create_app, sio, db
from server import config
from server.utils.init_user import create_admin

conf = {'dev': config.DevelopmentConfig, 'prod': config.ProductionConfig, 'test': config.TestConfig}
app = create_app(conf.get(os.environ.get('FLASK_ENV')))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin(db)

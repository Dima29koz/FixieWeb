import os
from dotenv import load_dotenv
load_dotenv()
from server.app import create_app, sio
from server import config


conf = {'dev': config.DevelopmentConfig, 'prod': config.ProductionConfig, 'test': config.TestConfig}
app = create_app(conf.get(os.environ.get('FLASK_ENV')))


if __name__ == '__main__':
    sio.run(app)

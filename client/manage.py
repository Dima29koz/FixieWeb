import os
from dotenv import load_dotenv
load_dotenv()
from client.app import create_app
from client import config

conf = {'dev': config.DevelopmentConfig, 'prod': config.ProductionConfig, 'test': config.TestConfig}
app = create_app(conf.get(os.environ.get('FLASK_ENV')))


if __name__ == '__main__':
    app.run(port=5001)

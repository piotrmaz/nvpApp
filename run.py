import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == '__main__':

    app.run()

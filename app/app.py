import os

import dotenv

from app.blueprints.post_blueprint.views import post_blueprint
from app.paths import STATIC_PATH, DEV_CONFIG_FILE_PATH, PROD_CONFIG_FILE_PATH

from flask import Flask


def create_app():
    app = Flask(__name__, static_url_path='', static_folder=STATIC_PATH)

    app.register_blueprint(post_blueprint)

    dotenv.load_dotenv(override=True)

    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_pyfile(DEV_CONFIG_FILE_PATH)
        app.config['SECRET_KEY'] = 'super-secret-key'
    else:
        app.config.from_pyfile(PROD_CONFIG_FILE_PATH)
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    return app

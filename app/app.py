from app.blueprints.post_blueprint.views import post_blueprint
from app.paths import DEV_CONFIG_FILE_PATH, PROD_CONFIG_FILE_PATH, STATIC_PATH

from os import environ

from flask import Flask
import dotenv


app = Flask(__name__, static_url_path='', static_folder=STATIC_PATH)

app.register_blueprint(post_blueprint)

dotenv.load_dotenv(override=True)
if environ.get('APP_SETTINGS') == 'development':
    app.config.from_pyfile(DEV_CONFIG_FILE_PATH)
    app.config['SECRET_KEY'] = 'super-secret-key'
else:
    app.config.from_pyfile(PROD_CONFIG_FILE_PATH)
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

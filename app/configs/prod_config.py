from os import environ

import dotenv

from app.paths import PROD_CONFIG_FILE_PATH
from app.app import app


DEBUG = False
ENV = 'production'
TESTING = False
JSON_AS_ASCII = False

dotenv.load_dotenv(override=True)

app.config.from_pyfile(PROD_CONFIG_FILE_PATH)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

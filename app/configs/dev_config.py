import dotenv

from app.paths import DEV_CONFIG_FILE_PATH
from app.app import app


DEBUG = True
ENV = 'development'
TESTING = True
JSON_AS_ASCII = False


dotenv.load_dotenv(override=True)

app.config.from_pyfile(DEV_CONFIG_FILE_PATH)
app.config['SECRET_KEY'] = 'super-secret-key'
print(1)

import os


APP_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIGS_PATH = os.path.join(APP_PATH, 'configs')
DEV_CONFIG_FILE_PATH = os.path.join(CONFIGS_PATH, 'dev_config.py')
PROD_CONFIG_FILE_PATH = os.path.join(CONFIGS_PATH, 'prod_config.py')

DATA_PATH = os.path.join(APP_PATH, 'data')
BOOKMARKS_JSON_PATH = os.path.join(DATA_PATH, 'bookmarks.json')
COMMENTS_JSON_PATH = os.path.join(DATA_PATH, 'comments.json')
DATA_JSON_PATH = os.path.join(DATA_PATH, 'data.json')
USERS_JSON_PATH = os.path.join(DATA_PATH, 'users.json')

STATIC_PATH = os.path.join(APP_PATH, 'blueprints', 'static')

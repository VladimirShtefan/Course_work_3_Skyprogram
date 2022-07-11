from app.blueprints.post_blueprint.views import post_blueprint
from app.paths import STATIC_PATH

from flask import Flask


app = Flask(__name__, static_url_path='', static_folder=STATIC_PATH)

app.register_blueprint(post_blueprint)

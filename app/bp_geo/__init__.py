from flask import Flask
from models import db, bcrypt
from routes import api, admin, login

from config import init_config
from url_converter import ObjectIDConverter
from errorhandler import init_errorhandler


def register_blueprints(app):
    # app.register_blueprint(login)
    app.register_blueprint(api, url_prefix='/features')
    # app.register_blueprint(admin)


def create_app(**config):
    app = Flask(__name__)

    app.url_map.converters['objectid'] = ObjectIDConverter
    init_errorhandler(app)

    init_config(app)
    app.config.from_mapping(config)

    db.init_app(app)
    bcrypt.init_app(app)

    register_blueprints(app)



    return app

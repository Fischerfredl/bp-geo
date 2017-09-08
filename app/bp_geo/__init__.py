import os

from flask import Flask
from models import db, bcrypt
from routes import api, admin


def init_config(app):
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'initial_key')

    app.config['MONGODB_DB'] = os.getenv('MONGODB_DB', 'development')
    app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST', 'mongomock://localhost')
    app.config['MONGODB_PORT'] = os.getenv('MONGODB_PORT', 27017)
    app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME')
    app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD')
    return

def register_blueprints(app):
    app.register_blueprint(api)
    app.register_blueprint(admin)


def create_app(**config):
    app = Flask(__name__)

    init_config(app)
    app.config.from_mapping(config)

    db.init_app(app)
    bcrypt.init_app(app)

    register_blueprints(app)

    return app

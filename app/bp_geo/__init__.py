from flask import Flask
from models import db, bcrypt
from routes import api


def create_app(**config):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'test'

    app.config['MONGODB_DB'] = 'development'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_PORT'] = 27017

    app.config.from_mapping(config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

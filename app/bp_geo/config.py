import os


def init_config(app):
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'initial_key')

    app.config['MONGODB_DB'] = os.getenv('MONGODB_DB', 'development')
    app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST', 'mongomock://localhost')
    app.config['MONGODB_PORT'] = os.getenv('MONGODB_PORT', 27017)
    app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME')
    app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD')
    return

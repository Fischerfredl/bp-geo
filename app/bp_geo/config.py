import os

def get_secret(secret_name):
    try:
        with open('run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read()
    except IOError:
        return None


def init_config(app):
    app.config['SECRET_KEY'] = get_secret('SECRET_KEY') or 'initial_key'

    app.config['MONGODB_DB'] = os.getenv('MONGODB_DB', 'development')
    app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST', 'mongomock://localhost')
    app.config['MONGODB_PORT'] = os.getenv('MONGODB_PORT', 27017)

    app.config['MONGODB_USERNAME'] = get_secret('mongodb_username')
    app.config['MONGODB_PASSWORD'] = get_secret('mongodb_password')
    return

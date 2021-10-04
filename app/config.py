from datetime import timedelta
from environs import Env
env = Env()
env.read_env()


class Config(object):
    APP_ENV = 'development'
    TESTING = False
    FLASK_RUN_HOST = env.str('FLASK_RUN_HOST')
    FLASK_RUN_PORT = env.str('FLASK_RUN_PORT')

    MONGODB_NAME = env.str('MONGODB_NAME')
    MONGODB_HOST = env.str('MONGODB_HOST')
    MONGODB_PORT = env.str('MONGODB_PORT')
    MONGODB_USERNAME = env.str('MONGODB_USERNAME')
    MONGODB_PASSWORD = env.str('MONGODB_PASSWORD')

    secret_key = env.str('SECRET_KEY')

    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    JWT_ALGORITHM = env.str('JWT_ALGORITHM')

    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)

class ProductionConfig(Config):
    APP_ENV = 'production'

class TestingConfig(Config):
    TESTING = True
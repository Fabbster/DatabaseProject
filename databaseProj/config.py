import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'my-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    DEBUG = False
    APP_SETTINGS = 'ProductionConfig'

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    APP_SETTINGS = 'StagingConfig'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    APP_SETTINGS = 'DevelopmentConfig'

class TestingConfig(Config):
    TESTING = True
    APP_SETTINGS = 'TestingConfig'

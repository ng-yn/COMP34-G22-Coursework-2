"""Flask config class."""
from pathlib import Path

class Config(object):
    DEBUG = False
    SECRET_KEY = 'nZ2d3HLMrP97UqvibLyFIw'  # Used for session cookies
    SQLALCHEMY_TRACK_MODIFICATION = False
    DATA_PATH = Path('data')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('FinancialDatabase.db'))


class ProductionConfig(Config):
    ENV = 'production'
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True

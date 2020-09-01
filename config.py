import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'moj_jako_jako_tajni_kljuc')
    ADMIN_KEY = os.getenv('ADMIN_KEY', 'ja_sam_admin')
    RESTPLUS_MASK_HEADER = False
    RESTPLUS_MASK_SWAGGER = False
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gym_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gym_test.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProductionConfig
)

secret_key = Config.SECRET_KEY
admin_key = Config.ADMIN_KEY
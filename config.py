# For environment variables
from os import getenv


class Config:
    # Where can I put these secrets? dotenv seems a better place
    SECRET_KEY = getenv("SECRETKEY")

    # Set the URI and other stuff here
    dbuser = getenv("DBUSER")
    dbpassword = getenv("DBPASSWORD")
    dburi = getenv("DBURI")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{dbuser}:{dbpassword}@{dburi}/music-dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


# Dev config
class DevConfig(Config):
    DEBUG = True


# Test config
class TestConfig(Config):
    TESTING = True


# Production config
class ProdConfig(Config):
    pass


config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": DevConfig,
}

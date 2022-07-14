# For environment variables
from dotenv import load_dotenv
from os import getenv


class Config:
    # Load the dotenv file
    load_dotenv()

    # Get the Flask secret key
    SECRET_KEY = getenv("SECRETKEY")

    # Set the URI and other stuff here
    dbuser = getenv("DBUSER")
    dbpassword = getenv("DBPASSWORD")
    dburi = getenv("DBURI")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{dbuser}:{dbpassword}@{dburi}/music-dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email stuff
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")

    APP_ADMIN = getenv("APP_ADMIN")
    APP_MAIL_SUBJECT_PREFIX = "Flask Webdev - "
    APP_MAIL_SENDER = f"WebDev Admin <{APP_ADMIN}>"



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
    # Use the real DB

    # Set the URI and other stuff here
    dbuser = getenv("DBUSER")
    dbpassword = getenv("DBPASSWORD")
    dburi = getenv("DBURI")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{dbuser}:{dbpassword}@{dburi}/music"


config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": DevConfig,
}

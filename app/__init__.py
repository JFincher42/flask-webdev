from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

# from flask.globals import session
# from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from config import config

# We need these in global scope
bootstrap = Bootstrap()
db = SQLAlchemy()


# Application Factory
def create_app(config_name="default"):
    # Create the app instance
    app = Flask(__name__)

    # Load our configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize bootstrap and the db connection
    bootstrap.init_app(app)
    db.init_app(app)

    # Import and register the blueprint
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # App's done!
    return app

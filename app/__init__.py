# Flask and styling
from flask import Flask
from flask_bootstrap import Bootstrap

# DB Stuff
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Configuration
from config import config

# Authentication
from flask_login import LoginManager

# Email
from flask_mail import Mail

# We need these in global scope
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


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
    migrate.init_app(app, db)

    # Login manager
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Email
    mail.init_app(app)

    # Import and register the blueprint
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Get the auth blueprint as well
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # App's done!
    return app

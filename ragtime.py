# For the DB
from flask_migrate import Migrate
from app import create_app, db
from app.models import Role, User
from os import getenv

# Create the app
app = create_app(getenv("FLASK_CONFIG") or "default")

# Setup the db migration
migrate = Migrate(app, db)


# For using `flask shell`
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

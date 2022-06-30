import pytest

# from flask_migrate import Migrate
from app import create_app, db


# Configure test environment
@pytest.fixture(scope="module")
def new_app():
    test_app = create_app("testing")

    # Forgot this
    assert "mysql" in test_app.config["SQLALCHEMY_DATABASE_URI"]
    test_client = test_app.test_client()

    # He split this into two things
    # app.app_context().push()
    ctx = test_app.app_context()
    ctx.push()

    # This was not right at all
    # migrate = Migrate(app, db)
    db.create_all()

    # Should yield the client, not the app
    # yield app
    yield test_client

    # Cleanup was easier...
    db.session.remove()
    db.drop_all()
    ctx.pop()

# from app import db
# from app.models import User
from app import db
from app.models import User
import pytest


def test_database_insert(new_app):
    u = User(username="john")
    db.session.add(u)
    db.session.commit()


# Testing password stuff
def test_password_creation(new_app):
    u = User(username="john")
    u.password = "test-password"


def test_password_positive_verification(new_app):
    u = User(username="john", password="test-password")
    assert u.verify_password("test-password")


def test_password_negtive_verification(new_app):
    u = User(username="john", password="test-password")
    assert not u.verify_password("not-a-good-password")


def test_password_read_failure(new_app):
    u = User(username="john", password="test-password")
    with pytest.raises(AttributeError):
        print(u.password)


def test_password_hashes_different(new_app):
    u1 = User(username="john", password="test-password")
    u2 = User(username="mary", password="test-password")
    assert u1.password_hash != u2.password_hash

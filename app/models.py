import jwt
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from datetime import datetime, timedelta


# DB Models
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return f"<Role {self.name}>"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError("'password' is not a readable field.")

    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def __repr__(self):
        return f"<User {self.username}>"

    # Generate a confirmation token with a default 1 hour expiration
    def generate_confirmation_token(self, expiration_sec=3600):
        expiration_time = datetime.utcnow() + timedelta(expiration_sec)
        data = {"exp": expiration_time, "confirm_id": self.id}
        return jwt.encode(data, current_app.secret_key, algorithm="HS512")

    # Confirm a token returned to us
    def confirm(self, token):
        # Is the token valid?
        try:
            data = jwt.decode(token, current_app.secret_key, algorithms=["HS512"])
        except jwt.ExpiredSignatureError as e:
            # Expired token
            return False
        except jwt.InvalidSignatureError as e:
            # Invalid signature
            return False

        # Valid token, but does it match?
        if data.get("confirm_id") != self.id:
            # Wrong user
            return False

        # OK, all checks passed, we're good
        self.confirmed = True
        db.session.add(self)

        # Don't commit yet -- we need to make sure the user logs in correctly

        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

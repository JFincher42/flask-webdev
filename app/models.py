from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

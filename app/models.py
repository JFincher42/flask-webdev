from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import jwt


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

    def generate_confirmation_token(self, expiration=3600):
        # s = Serializer(current_app.secret_key, expires_in=expiration)
        # return s.dumps({"confirm_id": self.id}).decode("utf-8")
        confirm_token = jwt.encode(
            {
                "confirm_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            current_app.secret_key,
            algorithm="HS256"
        )
        return confirm_token

    def confirm(self, token):
        # s = Serializer(current_app.secret_key)
        # try:
        #     data = s.loads(token.encode("utf-8"))
        # except:
        #     # loading the token threw an exception -- not confirmed
        #     return False

        # if data.get("confirm_id") != self.id:
        #     return False

        try:
            data = jwt.decode(
                token,
                current_app.secret_key,
                # leeway accounts for clock drift, differences
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return False

        if data.get("confirm_id") != self.id:
            return False

        self.confirmed=True
        db.session.add(self)
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

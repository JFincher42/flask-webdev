from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from ..models import User


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Length(max=64), Email()])
    password = PasswordField("Password:")
    remember_me = BooleanField("Remember me on this site")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email:", validators=[DataRequired(), Length(min=1, max=64), Email()]
    )
    username = StringField(
        "Username:",
        validators=[
            DataRequired(),
            Length(min=1, max=64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must start with a letter, and only contain letters, numbers, dots, and underscores",
            ),
        ],
    )

    password = PasswordField(
        "Password:",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", message="Passwords do not match!"),
        ],
    )
    password_confirm = PasswordField("Password (confirm):", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        # Is there a user with this email? If so, raise an exception
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("An account with this email is already registered.")

    def validate_username(self, field):
        # Does this username already exist? If so, raise an exception
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                "An account with this username is already registered."
            )

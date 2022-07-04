from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Length(max=64), Email()])
    password = PasswordField("Password:")
    remember_me = BooleanField("Remember me on this site")
    submit = SubmitField("Login")

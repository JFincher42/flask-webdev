# Get the stuff we need from flask
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import logout_user, login_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db, email
from datetime import datetime

# Get the blueprint
from . import auth

# Login in a known user
@auth.route("/login", methods=["GET", "POST"])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        # Get the data from the form
        email_entered = login_form.email.data
        password_entered = login_form.password.data

        # Get the user
        user = User.query.filter_by(email=email_entered).first()
        if user and user.verify_password(password_entered):
            login_user(user, login_form.remember_me.data)
            next = request.args.get("next")
            if not next or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)

        flash("Invalid user email/password")

    return render_template("auth/login.html", form=login_form)


# Register a new user
@auth.route("/register", methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        email_entered = registration_form.email.data
        username_entered = registration_form.username.data
        password_entered = registration_form.password.data

        user = User()
        user.email = email_entered
        user.username = username_entered
        user.password = password_entered
        db.session.add(user)
        db.session.commit()

        # Welcome the user
        email.send_mail(email_entered, "Registered!", "mail/welcome", user=user)

        # Notify the admin
        email.send_mail(current_app.config["APP_ADMIN"], "New User", "mail/new_user", user=user, time=datetime.now())

        flash(f"User {username_entered} registered, please login!")
        return redirect(url_for(".login"))

    return render_template("auth/register.html", form=registration_form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You've been logged out successfully!")
    return redirect(url_for("main.index"))

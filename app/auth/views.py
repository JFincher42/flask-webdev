# Get the stuff we need from flask
from flask import render_template, redirect, url_for, flash, request
from flask_login import logout_user, login_user
from .forms import LoginForm
from ..models import User

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
@auth.route("/register")
def register():
    return render_template("auth/register.html")


@auth.route("/logout")
def logout():
    logout_user()
    flash("You've been logged out successfully!")
    return redirect(url_for("main.index"))

# Get the stuff we need from flask
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import logout_user, login_user, login_required
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

        # Generate confirmation token and send link
        token = user.generate_confirmation_token()
        email.send_mail(
            email_entered, "Confirm your email", "auth/email/confirm", token=token
        )

        # Welcome the user
        # email.send_mail(email_entered, "Registered!", "mail/welcome", user=user)

        # Send a confirmation email
        email.send_mail(email_entered, "Please Confirm Email", "mail/confirm", \
            url=url_for("confirm/<token>"), \
            token=user.generate_confirmation_token())

        # Notify the admin
        email.send_mail(
            current_app.config["APP_ADMIN"],
            "New User",
            "mail/new_user",
            user=user,
            time=datetime.now(),
        )

        flash(f"User {username_entered} registered, please login!")
        return redirect(url_for(".login"))

    return render_template("auth/register.html", form=registration_form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You've been logged out successfully!")
    return redirect(url_for("main.index"))


@auth.route("/confirm/<token>")
@login_required
def confirm(token):

    # If they're already confirmed, this is not needed
    if current_user.confirmed:
        flash("You're already confirmed, silly!")
        return redirect(url_for("main.index"))

    # Otherwise, we check the confirmation token, and confirm as necessary
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account! Thank you.")
    else:
        flash("Whoops! That confirmation link either expired, or it isn't valid.")

    # In either case, head back to the main page
    return redirect(url_for("main.index"))


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.confirmed
        and request != "static"
        and request.blueprint != "auth"
        and request.endpoint != "static"
    ):
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html", user=current_user)

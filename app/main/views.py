# Get the stuff we need from flask
from flask import session, render_template, redirect, url_for, flash

# Get the blueprint
from . import main

# Get the stuff we need for our route
from .forms import NameForm
from .. import db
from ..models import User
from flask_login import login_required


# What should our main form look like?
@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()

    if form.validate_on_submit():
        name_entered = form.name.data
        user = User.query.filter_by(username=name_entered).first()
        if user is None:
            user = User(username=name_entered)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
        else:
            session["known"] = True
        session["name"] = name_entered
        flash("Great! Hope you enjoy your stay!")
        return redirect(url_for(".index"))

    return render_template(
        "index.html", form=form, name=session.get("name"), known=session.get("known")
    )


@main.route("/top-secret")
@login_required
def top_secret():
    return "Welcome, VIP Member!"

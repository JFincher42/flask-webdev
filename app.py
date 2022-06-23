from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

# For the form
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

# For the DB
from flask_sqlalchemy import SQLAlchemy


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DateForm(FlaskForm):
    date = DateField("What is your birthdate?", validators=[DataRequired()])
    submit = SubmitField("Submit")


app = Flask(__name__)
bootstrap = Bootstrap(app)

# Where xan I put these secrets? dotenv seems a better place
app.config["SECRET_KEY"] = "good for debug, sucks for prod"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:password@0.0.0.0:3306/music-dev"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return "Hello Web World!"


@app.route("/form", methods=["GET", "POST"])
def show_form():
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
        return redirect(url_for("show_form"))
    return render_template(
        "index.html", form=form, name=session.get("name"), known=session.get("known")
    )


@app.route("/date", methods=["GET", "POST"])
def show_date():
    form = DateForm()
    if form.validate_on_submit():
        date = form.date.data
        form.date.data = ""
        return redirect(url_for("show_date"))
    return render_template("date.html", form=form, date=session.get("date"))


@app.route("/about")
def about_us():
    return "Something about us."


@app.route("/user/<username>")
def user(username):
    return render_template("user.html", username=username)


@app.route("/songs")
def songs():
    songs = ["Everybody Dies", "Tom Sawyer", "War Eternal"]
    return render_template("songs.html", favorite_songs=songs)


@app.route("/derived")
def derived():
    return render_template("derived.html")


# DB Models


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return f"<Role {self.name}>"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return f"<User {self.username}>"


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

<<<<<<< HEAD
from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

# For the form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "good for debug, sucks for prod"

@app.route("/")
def index():
    return "Hello Web World!"

@app.route("/form", methods=["GET", "POST"])
def show_form():
    # name = None
    # form = NameForm()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     form.name.data = ''
    #     return redirect(url_for("show_form"))
    # return render_template('index.html', form=form, name=name)

    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        flash("Great! Hope you enjoy your stay!")
        return redirect(url_for('show_form'))
    return render_template('index.html', form=form, name=session.get('name'))


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
=======
from flask import Flask

app = Flask(__name__)


@app.route('/')
def welcome():
    return "Welcome to Emily's Dog Costumes!"


@app.route('/services')
def services():
    return "I offer custom made costumes for your precious canine companion, "\
        "and a free in-home consultation, to get the measurements."


@app.route('/costumes/<costume>')
def costumes(costume):
    return f"Check out this {costume} costume!"
>>>>>>> e770a7e (Adding Bootstrap, some templates)

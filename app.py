from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def index():
    return "Hello Web World!"


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

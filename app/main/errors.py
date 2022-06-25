# Get what we need from flask
from flask import render_template

# Get the main blueprint
from . import main


# Error handlers
@main.errorhandler(404)
def page_not_found(e):
    error_title = "Not found"
    error_msg = "That page doesn't exist."
    return (
        render_template("error.html", error_title=error_title, error_msg=error_msg),
        404,
    )


@main.errorhandler(403)
def forbidden(e):
    error_title = "Verboten!"
    error_msg = "You can't be here -- this is the war room!"
    return (
        render_template("error.html", error_title=error_title, error_msg=error_msg),
        403,
    )


@main.errorhandler(500)
def forbidden(e):
    error_title = "Internal Server Error!"
    error_msg = "We are experiencing technical difficulties.... Please stand by..."
    return (
        render_template("error.html", error_title=error_title, error_msg=error_msg),
        500,
    )

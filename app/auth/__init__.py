from flask import Blueprint

# Authentication blueprint
auth = Blueprint("auth", __name__, url_prefix="/auth")

from . import views

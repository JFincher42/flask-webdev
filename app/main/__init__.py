# Setup the blueprint
from flask import Blueprint

# Create a global blueprint we can use
main = Blueprint("main", __name__)

# We can't import these until after the blueprint is ready
from . import views, errors

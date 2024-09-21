from flask import Blueprint

bp = Blueprint('story', __name__)

from . import routes
from flask import Blueprint
from flask_restful import Api

bp = Blueprint('api', __name__)
api = Api(bp)  #

def register_routes():
    from . import routes  
    # Register resources here if needed

# app initialization
register_routes()
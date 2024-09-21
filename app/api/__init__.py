from flask import Blueprint
from flask_restful import Api

bp = Blueprint('api', __name__)
api = Api(bp)  # Create the Api object here

def register_routes():
    from . import routes  # Import routes here to avoid circular import
    # Register resources here if needed

# Call this function in your app initialization
register_routes()
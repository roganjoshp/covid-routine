from flask import Blueprint

bp = Blueprint('solver', __name__)


from app.solver import routes

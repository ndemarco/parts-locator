from flask import Blueprint

bp = Blueprint('parts', __name__, template_folder='../templates')

from . import routes

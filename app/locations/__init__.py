from flask import Blueprint

bp = Blueprint('locations', __name__, template_folder='../templates')

from . import routes
from flask import Blueprint

messenger = Blueprint('messenger', __name__)

from . import routes, events

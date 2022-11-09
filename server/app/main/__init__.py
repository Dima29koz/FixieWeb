"""
Initialization of BluePrints
"""

from flask import Blueprint

chat = Blueprint('main', __name__)

from . import routes
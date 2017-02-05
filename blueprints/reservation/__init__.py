from flask import Blueprint

blueprint = Blueprint('reservation', __name__, url_prefix='/reservation')

from views import index, create, admin

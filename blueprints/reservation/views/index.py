from flask import render_template
from flask_login import current_user, login_required

from .. import blueprint
from models.reservation import Reservation


@blueprint.route('/')
@login_required
def index():
    reservations = current_user.reservations.order_by(Reservation.created_at.desc()).all()
    return render_template('reservation/index.html', reservations=reservations, title='Your Reservations')

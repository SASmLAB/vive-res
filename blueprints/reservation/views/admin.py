from flask import render_template, abort, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import InputRequired

from .. import blueprint
from models import db
from models.reservation import Reservation


class SearchForm(FlaskForm):
    period = SelectField('Period',
                         choices=[
                             ('', 'All periods'), ('A', 'A Period'), ('B', 'B Period'), ('C', 'C Period'),
                             ('D', 'D Period'), ('E', 'E Period'), ('F', 'F Period'), ('G', 'G Period'),
                             ('X', 'After School')
                         ],
                         default=''
                         )
    people = SelectField('People', choices=[(0, 'All people'), (1, 'Solo'), (2, 'Duo'), (-1, 'Class')], coerce=int)
    status = SelectField('Status',
                         choices=[
                             ('', 'All statuses'), ('pending', 'Pending'), ('accepted', 'Accepted'),
                             ('denied', 'Denied')
                         ],
                         default=''
                         )
    submit = SubmitField('Search')


@blueprint.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)

    search_form = SearchForm(formdata=request.args, meta={'csrf_enabled': False})
    reservations = Reservation.query

    if search_form.period.data and search_form.period.data != '':
        reservations = reservations.filter_by(period=search_form.period.data)

    if search_form.people.data and search_form.people.data != 0:
        reservations = reservations.filter_by(people=search_form.people.data)

    if search_form.status.data and search_form.status.data != '':
        status = {'pending': None, 'accepted': True, 'denied': False}.get(search_form.status.data)
        reservations = reservations.filter_by(accepted=status)

    reservations = reservations.order_by(Reservation.created_at.desc()).all()

    return render_template('reservation/admin.html',
                           search_form=search_form,
                           reservations=reservations,
                           title='Reservations Admin'
                           )


class AcceptForm(FlaskForm):
    id = IntegerField(validators=[InputRequired()])


@blueprint.route('/admin/accept', methods=['POST'])
@login_required
def admin_accept():
    if not current_user.is_admin:
        abort(403)

    form = AcceptForm()
    if form.validate_on_submit():
        reservation = Reservation.query.filter_by(id=form.id.data).first()
        if reservation:
            reservation.accepted = True
            db.session.add(reservation)
            db.session.commit()

            return jsonify(True)

    return jsonify(False)


class DenyForm(FlaskForm):
    id = IntegerField(validators=[InputRequired()])
    reason = StringField(validators=[InputRequired()])


@blueprint.route('/admin/deny', methods=['POST'])
@login_required
def admin_deny():
    if not current_user.is_admin:
        abort(403)

    form = DenyForm()
    if form.validate_on_submit():
        reservation = Reservation.query.filter_by(id=form.id.data).first()
        if reservation:
            reservation.accepted = False
            reservation.denial_reason = form.reason.data
            db.session.add(reservation)
            db.session.commit()

            return jsonify(True)

    return jsonify(False)

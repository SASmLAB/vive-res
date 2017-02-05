from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError
import datetime
import dateutil.parser

from .. import blueprint, get_schedule

from models import db
from models.reservation import Reservation


def check_date(form, field):
    if field.data:
        date = dateutil.parser.parse(field.data).date()
        today = datetime.date.today()
        if date <= today:
            raise ValidationError('You must specify a date in the future.')


def check_period(form, field):
    if form.date.data:
        date = dateutil.parser.parse(form.date.data).date()
        schedule = get_schedule().get(date)

        if not schedule or field.data not in schedule:
            raise ValidationError('You must specify a period on that date.')

        if Reservation.query.filter_by(date=form.date.data, period=form.period.data, accepted=True).first():
            raise ValidationError('Someone already has a reservation for that time.')


class CreateReservationForm(FlaskForm):
    date = StringField('What date?', validators=[
        InputRequired('You must specify a date.'),
        Regexp('^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$',
               message='You must specify a date in the format of YYYY-MM-DD.'),
        check_date
    ])

    period = SelectField('What period?',
                         choices=[
                             ('A', 'A Period'), ('B', 'B Period'), ('C', 'C Period'), ('D', 'D Period'),
                             ('E', 'E Period'), ('F', 'F Period'), ('G', 'G Period'), ('X', 'After School (3:30-4:30)')
                         ],
                         validators=[InputRequired('You must specify a class period.'), check_period]
                         )

    people = SelectField('How many people?',
                         choices=[(1, 'Solo'), (2, 'Duo'), (-1, 'Class (will contact for verification)')],
                         coerce=int,
                         validators=[InputRequired('You must specify the amount of people.')]
                         )

    agreement = BooleanField("""By checking this box,
    I agree that I may not hold St. Andrew's and any mLAB assistants liable for any injuries encountered
    whilst using the virtual reality equipment.""",
                             validators=[InputRequired('You must agree to the conditions.')]
                             )

    submit = SubmitField('Send it in!')


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateReservationForm()

    if form.validate_on_submit():
        reservation = Reservation(form.date.data, form.period.data, form.people.data, current_user)

        db.session.add(reservation)
        db.session.commit()

        flash(
            "Your reservation has been submitted! You'll be notified soon about whether your reservation was accepted.",
            category='success'
        )
        return redirect(url_for('.index'))

    form.date.data = request.args.get('date', form.date.data)
    form.period.data = request.args.get('period', form.period.data)

    return render_template('reservation/create.html', form=form, title='Reserve VR Time')

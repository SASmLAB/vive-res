from flask import jsonify, request, url_for, render_template
from flask_login import login_required
import datetime
import dateutil.parser

from .. import blueprint, get_schedule
from models.reservation import Reservation


@blueprint.route('/calendar')
@login_required
def calendar():
    return render_template('reservation/calendar.html', title='Reserve VR Time')


@blueprint.route('/calendar/events')
@login_required
def calendar_events():
    periods = [
        {'start': '08:30:00', 'end': '09:20:00'},
        {'start': '09:25:00', 'end': '10:15:00'},
        {'start': '10:40:00', 'end': '11:30:00'},
        {'start': '11:35:00', 'end': '12:25:00'},
        {'start': '13:40:00', 'end': '14:30:00'},
        {'start': '14:35:00', 'end': '15:25:00'},
        {'start': '15:30:00', 'end': '16:30:00'}
    ]

    today = datetime.datetime.now()
    start_date = dateutil.parser.parse(request.args.get('start'))
    end_date = dateutil.parser.parse(request.args.get('end'))

    if start_date <= today:
        start_date = today + datetime.timedelta(days=1)

    events = []
    date_delta = end_date - start_date
    for i in range(date_delta.days + 1):
        date = start_date + datetime.timedelta(days=i)
        if date.weekday() in [5, 6]:
            continue

        schedule = get_schedule().get(date.date())
        if not schedule:
            continue

        date_string = date.strftime('%Y-%m-%d')

        for index, period in enumerate(schedule):
            if period == 'X':
                title = 'After School'
            else:
                title = '%s Period' % period

            available = not bool(Reservation.query.filter_by(date=date_string, period=period, accepted=True).first())

            events.append({
                'title': title,
                'start': '%sT%sZ' % (date_string, periods[index]['start']),
                'end': '%sT%sZ' % (date_string, periods[index]['end']),
                'url': url_for('.create', date=date_string, period=period) if available else '#',
                'className': 'available' if available else 'unavailable',
                'period': period,
                'available': available
            })

    return jsonify(events)

from . import db
import datetime
import dateutil.parser


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
                           backref=db.backref('reservations', lazy='dynamic'))

    date = db.Column(db.Date, nullable=False)
    period = db.Column(db.String(1), nullable=False)
    people = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean)
    denial_reason = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, date, period, people, user):
        self.date = dateutil.parser.parse(date)
        self.period = period
        self.people = people
        self.user = user

    def __repr__(self):
        return '<Reservation %r>' % self.id

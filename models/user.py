from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(21), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, google_id, email, first_name, last_name):
        self.google_id = google_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User %r - %r>' % (self.id, self.email)

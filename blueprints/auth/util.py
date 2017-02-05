from models import db
from models.user import User
import requests


class LoginException(Exception):
    pass


def authenticate_user(google_access_token, message='Unable to authenticate.'):
    r = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', {'access_token': google_access_token})

    if r.status_code != requests.codes.ok:
        raise LoginException(message)

    try:
        google_user_data = r.json()
    except:
        raise LoginException(message)

    if google_user_data.get('hd') != 'sasaustin.org':
        raise LoginException(message)

    user = User.query.filter_by(google_id=google_user_data['sub']).first()
    if user is None:
        user = User(
            google_user_data['sub'],
            google_user_data['email'],
            google_user_data['given_name'],
            google_user_data['family_name']
        )
    else:
        user.email = google_user_data['email']
        user.first_name = google_user_data['given_name']
        user.last_name = google_user_data['family_name']

    db.session.add(user)
    db.session.commit()

    return user

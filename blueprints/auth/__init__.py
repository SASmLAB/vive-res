from flask_login import LoginManager
from flask_oauth import OAuth
from flask import Blueprint

from models.user import User


# Flask-Login Setup
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message = u'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def user_loader(id):
    user = User.query.filter_by(id=id).first()
    return user


# Google OAuth Setup
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url=None,
                          request_token_url=None,
                          access_token_url='https://www.googleapis.com/oauth2/v4/token',
                          authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
                          consumer_key='510534009886-e6a5hlisveag9nmnnqjr2qgf5pjbrca6.apps.googleusercontent.com',
                          consumer_secret='r10t777XTWrWWAuyZQyCVexa',
                          request_token_params={
                              'response_type': 'code',
                              'scope': 'email profile',
                              'access_type': 'online',
                              'prompt': 'select_account',
                              'hd': 'sasaustin.org'
                          },
                          access_token_params={'grant_type': 'authorization_code'},
                          access_token_method='POST')

blueprint = Blueprint('auth', __name__)


# Views
from views import login, logout

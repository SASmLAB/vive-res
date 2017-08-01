from flask import request, render_template, redirect, flash, url_for
from flask_login import login_user, current_user

from .. import google, blueprint
from blueprints.auth.util import authenticate_user, LoginException


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))

    return render_template('auth/login.html', title='Login')


@blueprint.route('/login/google')
def google_login():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))

    callback = url_for('.login_callback', _external=True)
    return google.authorize(callback)


@blueprint.route('/login/callback')
@google.authorized_handler
def login_callback(resp):
    access_token = resp['access_token']

    try:
        user = authenticate_user(access_token)
    except LoginException as e:
        flash(e.message, category='danger')
        return redirect(url_for('.login'))

    if login_user(user, remember=True):
        flash('Logged in!', category='success')
        return redirect(request.args.get('next', '/'))

    return redirect(url_for('standalone.index'))

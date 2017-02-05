from flask_login import logout_user, login_required
from flask import flash, redirect, url_for

from .. import blueprint


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', category='success')
    return redirect(url_for('standalone.index'))

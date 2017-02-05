from flask import Blueprint, render_template

blueprint = Blueprint('standalone', __name__)


@blueprint.route('/')
def index():
    return render_template('standalone/index.html', title='Home')


@blueprint.route('/info')
def info():
    return render_template('standalone/info.html', title='Info')

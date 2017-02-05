import click
from flask import Flask
from flask_wtf import CsrfProtect


def create_app(config_override=None):
    application = Flask(__name__)

    import config
    application.config.from_object(config)
    application.config.from_object(config_override)

    CsrfProtect(application)

    from models import db
    db.init_app(application)

    from blueprints.auth import login_manager
    login_manager.init_app(application)

    import blueprints
    for blueprint in blueprints.blueprints:
        application.register_blueprint(blueprint)

    import util
    util.init_utils(application)

    @application.cli.command()
    def routes():
        for rule in application.url_map.iter_rules():
            click.echo('%s %s' % (rule, rule.endpoint))

    @application.cli.command()
    def init_db():
        db.create_all()

    return application

import logging
import sys

from flask import Flask
from flask_bootstrap import Bootstrap5

from to_do_app.database import db
from to_do_app.extensions import csrf, login_manager
from to_do_app import public, user


def create_app(config_object="to_do_app.settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    bootstrap = Bootstrap5(app)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    return app, bootstrap


def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def configure_logger(app):
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

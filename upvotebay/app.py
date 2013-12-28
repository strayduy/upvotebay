# -*- coding: utf-8 -*-

# Third party libs
from flask import Flask
from flask import render_template

# Our libs
from .extensions import db
from .extensions import login_manager
from .models import User
from .modules import root
from .modules import oauth
from .modules import api

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    app.register_blueprint(root.blueprint)
    app.register_blueprint(oauth.blueprint)
    app.register_blueprint(api.blueprint)

def register_error_handlers(app):
    def render_error(error):
        return render_template('errors/{0}.html'.format(error.code)), error.code
    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

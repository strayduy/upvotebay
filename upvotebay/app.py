# -*- coding: utf-8 -*-

# Third party libs
from flask import Flask

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

    return app

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    app.register_blueprint(root.blueprint)
    app.register_blueprint(oauth.blueprint)
    app.register_blueprint(api.blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

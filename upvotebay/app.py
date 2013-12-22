# -*- coding: utf-8 -*-

# Third party libs
from flask import Flask

# Our libs
from .modules import root
from .modules import oauth
from .modules import api

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(root.blueprint)
    app.register_blueprint(oauth.blueprint)
    app.register_blueprint(api.blueprint, url_prefix='/api')

# -*- coding: utf-8 -*-

# Standard libs
import os

# Third party libs
from flask import Flask
from flask.ext.mako import MakoTemplates

def create_app(config_object, env):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['ENV'] = env

    # Use Mako instead of Jinja
    mako = MakoTemplates(app)

    # Register blueprints
    from .modules import public
    app.register_blueprint(public.blueprint)

    return app

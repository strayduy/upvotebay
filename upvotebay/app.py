# -*- coding: utf-8 -*-

# Third party libs
from flask import Flask

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    from flask.ext.mako import MakoTemplates

    # Use Mako instead of Jinja
    MakoTemplates(app)

def register_blueprints(app):
    from .modules import root
    from .modules import oauth
    from .modules import api
    app.register_blueprint(root.blueprint)
    app.register_blueprint(oauth.blueprint)
    app.register_blueprint(api.blueprint, url_prefix='/api')

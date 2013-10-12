# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import Blueprint
from flask import session
from flask.ext.mako import render_template

blueprint = Blueprint('me',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
def index():
    username = session['username']
    return username

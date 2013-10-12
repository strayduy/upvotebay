# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import Blueprint
from flask import session
from flask.ext.mako import render_template

# Our libs
from upvotebay.utils import login_required

blueprint = Blueprint('me',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@login_required
def index():
    username = session['username']
    return username

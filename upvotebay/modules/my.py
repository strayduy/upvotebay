# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import Blueprint
from flask import session
from flask.ext.mako import render_template

# Our libs
from upvotebay.utils import login_required

blueprint = Blueprint('my',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@blueprint.route('/profile/')
@login_required
def profile():
    username = session['username']
    return render_template('my/profile.html',
                           username=username)

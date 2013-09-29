# -*- coding: utf-8 -*-

# Third party libs
from flask import Blueprint
from flask.ext.mako import render_template

blueprint = Blueprint('public',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
def index():
    return render_template('index.html')

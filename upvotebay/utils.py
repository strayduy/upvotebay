# -*- coding: utf-8 -*-

# Standard libs
from functools import wraps

# Third party libs
from flask import flash
from flask import redirect
from flask import session
from flask import url_for

def login_required(view):
    '''Decorator that makes a view require authentication.'''
    @wraps(view)
    def wrap(*args, **kwargs):
        if session.get('username'):
            return view(*args, **kwargs)

        flash('Please sign in first.')
        return redirect(url_for('public.index'))
    return wrap

def redirect_logged_in_users_to_profile(view):
    '''Decorator that redirects logged-in users to their profile page.'''
    @wraps(view)
    def wrap(*args, **kwargs):
        if not session.get('username'):
            return view(*args, **kwargs)

        return redirect(url_for('my.profile'))
    return wrap

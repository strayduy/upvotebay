# -*- coding: utf-8 -*-

# Standard libs
from urlparse import urlparse

# Third party libs
from flask import url_for
from flask.ext.testing import TestCase
from flask.ext.webtest import TestApp
from nose.tools import * # PEP8 asserts

# Our libs
from upvotebay.app import create_app
from upvotebay.modules import root
from upvotebay.settings import TestConfig

# Constants
SIGN_IN_LINK_TEXT = 'Sign in through reddit'
LOGOUT_FORM_ID = 'logout-form'
MOCK_USERNAME = 'mock_user'

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        self.test_app = TestApp(self.app)

class TestLandingPage(BaseTestCase):
    def test_landing_page(self):
        res = self.test_app.get(url_for('root.index'))
        assert_equal(res.status_code, 200)
        assert_in(SIGN_IN_LINK_TEXT, res)

class TestLoggingIn(BaseTestCase):
    def test_log_in_from_landing_page(self):
        # Go to landing page
        res = self.test_app.get(url_for('root.index'))
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'landing.html')
        assert_in(SIGN_IN_LINK_TEXT, res)

        # Confirm that we're logged out
        assert_not_in('username', res.session)
        assert_not_in('access_info', res.session)

        # Click the sign-in link
        res = res.click(SIGN_IN_LINK_TEXT)
        assert_equal(res.status_code, 302)
        assert_url_equal(res.location, url_for('root.index'))

        # Follow the oauth callback redirect
        # Confirm that we're logged in
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'home.html')
        assert_equal(res.session['username'], MOCK_USERNAME)
        assert_equal(res.session['access_info']['scope'],
                     self.app.config['REDDIT_OAUTH_SCOPES'])

class TestLoggingOut(BaseTestCase):
    def test_log_out(self):
        username = 'test_user'

        # Log in as 'test_user'
        with self.test_app.session_transaction() as _session:
            _session['username'] = username

        # Go to home page
        res = self.test_app.get(url_for('root.index'))
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'home.html')
        assert_in(LOGOUT_FORM_ID, res.forms)

        # Confirm that we're logged in
        assert_equal(res.session['username'], username)

        # Submit the logout form
        logout_form = res.forms[LOGOUT_FORM_ID]
        res = logout_form.submit()
        assert_equal(res.status_code, 302)
        assert_url_equal(res.location, url_for('root.index'))

        # Confirm that we're logged out
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'landing.html')
        assert_not_in('username', res.session)

class TestOAuthCallback(BaseTestCase):
    def test_valid_oauth_state(self):
        auth_key = 'supersecret'

        # Save OAuth key in session
        with self.test_app.session_transaction() as _session:
            _session['auth_key'] = auth_key

        # Hit the callback route with our key
        res = self.test_app.get(url_for('oauth.oauth_callback', state=auth_key))
        assert_equal(res.status_code, 302)
        assert_url_equal(res.location, url_for('root.index'))

        # Follow the oauth callback redirect
        # Confirm that we're logged in
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'home.html')
        assert_equal(res.session['username'], MOCK_USERNAME)
        assert_equal(res.session['access_info']['scope'],
                     self.app.config['REDDIT_OAUTH_SCOPES'])

    def test_omitted_oauth_state(self):
        res = self.test_app.get(url_for('oauth.oauth_callback'),
                                status=401)
        assert_equal(res.status_code, 401)

    def test_empty_oauth_state(self):
        res = self.test_app.get(url_for('oauth.oauth_callback', state=''),
                                status=401)
        assert_equal(res.status_code, 401)

    def test_invalid_oauth_state(self):
        res = self.test_app.get(url_for('oauth.oauth_callback', state='california'),
                                status=401)
        assert_equal(res.status_code, 401)

def assert_url_equal(url_a, url_b):
    parsed_url_a = urlparse(url_a)
    parsed_url_b = urlparse(url_b)

    # Assert that the path and params match
    assert_equal(parsed_url_a.path, parsed_url_b.path)
    assert_equal(parsed_url_a.params, parsed_url_b.params)

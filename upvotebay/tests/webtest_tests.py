# -*- coding: utf-8 -*-

# Standard libs
from urlparse import urlparse

# Third party libs
from flask import session
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
        assert_in(SIGN_IN_LINK_TEXT, res)
        assert_not_in('username', res.session)
        assert_not_in('access_info', res.session)

        # Click the sign-in link
        res = res.click(SIGN_IN_LINK_TEXT)
        assert_equal(res.status_code, 302)
        assert_url_equal(res.location, url_for('root.index'))

        # Follow the oauth callback redirect
        # Confirm that the user is logged in
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.session['username'], 'mock_user')
        assert_equal(res.session['access_info']['scope'],
                     self.app.config['REDDIT_OAUTH_SCOPES'])

def assert_url_equal(url_a, url_b):
    parsed_url_a = urlparse(url_a)
    parsed_url_b = urlparse(url_b)

    # Assert that the path and params match
    assert_equal(parsed_url_a.path, parsed_url_b.path)
    assert_equal(parsed_url_a.params, parsed_url_b.params)

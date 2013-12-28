# -*- coding: utf-8 -*-

# Standard libs
from urlparse import urlparse
import uuid

# Third party libs
from flask import url_for
from flask.ext.testing import TestCase
from flask.ext.webtest import TestApp
from nose.tools import * # PEP8 asserts

# Our libs
from upvotebay.app import create_app
from upvotebay.extensions import db
from upvotebay.models import User
from upvotebay.modules import root
from upvotebay.settings import TestConfig

# Constants
SIGN_IN_LINK_TEXT_LANDING_PAGE = 'Sign in through reddit'
SIGN_IN_LINK_TEXT_NAVBAR = 'Sign in'
LOGOUT_FORM_ID = 'logout-form'
MOCK_USERNAME = 'mock_user'

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        self.test_app = TestApp(self.app, db=db, use_session_scopes=True)
        db.create_all()

        # Add test user account
        test_user = User(username=MOCK_USERNAME)
        db.session.add(test_user)
        db.session.commit()

        # Store test user ID to verify against later
        self.test_user_id = unicode(test_user.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestLandingPage(BaseTestCase):
    def test_landing_page(self):
        res = self.test_app.get(url_for('root.index'))
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'landing.html')
        assert_in(SIGN_IN_LINK_TEXT_LANDING_PAGE, res)

class TestLoggingIn(BaseTestCase):
    def test_log_in_from_landing_page(self):
        # Go to landing page
        res = self.test_app.get(url_for('root.index'))
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'landing.html')
        assert_in(SIGN_IN_LINK_TEXT_LANDING_PAGE, res)

        # Confirm that we're logged out
        assert_not_in('user_id', res.session)

        # Click the sign-in link
        res = res.click(SIGN_IN_LINK_TEXT_LANDING_PAGE)
        assert_equal(res.status_code, 302)
        assert_url_equal(res.location, url_for('root.index'))

        # Follow the oauth callback redirect
        # Confirm that we're logged in
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'home.html')
        assert_equal(res.session['user_id'], self.test_user_id)

class TestLoggingOut(BaseTestCase):
    def test_log_out(self):
        # Log in as test user
        with self.test_app.session_transaction() as _session:
            _session['user_id'] = self.test_user_id

        # Go to home page
        res = self.test_app.get(url_for('root.index'))
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'home.html')
        assert_in(LOGOUT_FORM_ID, res.forms)

        # Confirm that we're logged in
        assert_equal(res.session['user_id'], self.test_user_id)

        # Submit the logout form
        logout_form = res.forms[LOGOUT_FORM_ID]
        res = logout_form.submit()
        assert_equal(res.status_code, 302)
        assert_url_equal(res.location, url_for('root.index'))

        # Confirm that we're logged out
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'landing.html')
        assert_not_in('user_id', res.session)

class TestOAuthCallback(BaseTestCase):
    def test_valid_oauth_state(self):
        # Generate key
        auth_key = str(uuid.uuid4())

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
        assert_equal(res.session['user_id'], self.test_user_id)

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

class TestUserPage(BaseTestCase):
    def test_user_page_logged_out(self):
        res = self.test_app.get(url_for('root.user'))
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'home.html')

        # Verify that the sign in link is present
        assert_in(SIGN_IN_LINK_TEXT_NAVBAR, res)

    def test_user_page_logged_in(self):
        # Log in as test user
        with self.test_app.session_transaction() as _session:
            _session['user_id'] = self.test_user_id

        res = self.test_app.get(url_for('root.user'))
        assert_equal(res.status_code, 200)
        assert_equal(res.template, 'home.html')

        # Verify that the logout form is present
        assert_in(LOGOUT_FORM_ID, res.forms)

class Test404Page(BaseTestCase):
    def test_404_page(self):
        res = self.test_app.get('/there/is/no/reason/for/this/route/to/exist',
                                status=404)
        assert_equal(res.status_code, 404)
        assert_equal(res.template, 'errors/404.html')

class TestAPI(BaseTestCase):
    def test_user_likes(self):
        res = self.test_app.get(url_for('api.user_likes', username=MOCK_USERNAME))
        assert_equal(res.status_code, 200)
        assert_in('likes', res.json)

    def test_my_likes_logged_out(self):
        res = self.test_app.get(url_for('api.my_likes'), status=401)
        assert_equal(res.status_code, 401)

    def test_my_likes_logged_in(self):
        # Log in as test user
        with self.test_app.session_transaction() as _session:
            _session['user_id'] = self.test_user_id

        res = self.test_app.get(url_for('api.my_likes'))
        assert_equal(res.status_code, 200)
        assert_in('likes', res.json)

def assert_url_equal(url_a, url_b):
    parsed_url_a = urlparse(url_a)
    parsed_url_b = urlparse(url_b)

    # Assert that the path and params match
    assert_equal(parsed_url_a.path, parsed_url_b.path)
    assert_equal(parsed_url_a.params, parsed_url_b.params)

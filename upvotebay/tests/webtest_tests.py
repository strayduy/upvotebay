# -*- coding: utf-8 -*-

# Third party libs
from flask.ext.testing import TestCase
from nose.tools import * # PEP8 asserts
from webtest import TestApp

# Our libs
from upvotebay.app import create_app
from upvotebay.settings import TestConfig

class TestLandingPage(TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        self.test_app = TestApp(self.app)

    def test_landing_page(self):
        res = self.test_app.get('/')
        assert_equal(res.status_code, 200)

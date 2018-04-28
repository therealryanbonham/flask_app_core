"""Unit Test for FastCache """
import unittest
import os
import secrets
from flask import Flask
from flask_app_core import FlaskWrapper


class BaseTest(unittest.TestCase):
    """Base Testing Class for setting up Flask App"""
    app = None
    cache = None

    def setUp(self):
        os.environ['SECRET_KEY'] = secrets.token_hex(16)
        self.app = Flask(__name__)
        FlaskWrapper('Test', self.app)
        # self.client = self.app.test_client()
        # with self.app.app_context():
        #     pass

    def tearDown(self):
        self.app = None
        self.cache = None


if __name__ == '__main__':
    unittest.main()

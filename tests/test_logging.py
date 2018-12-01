import flask
# from flask import request
from tests import BaseTest
import os


class EditableRequestsTests(BaseTest):

    def setUp(self):
        os.environ['REQUEST_EDITABLE'] = 'True'
        super().setUp()

    def test_request_edit(self):
        @self.app.route('/test')
        def test_request():
            flask.request.args['Test'] = 'A'
            return flask.request.args.get('Test', 'Blank')

        with self.app.test_client() as client:
            r = client.get('/test')
            self.assertEqual(r.data, b'A')


class NonEditableRequestsTests(BaseTest):

    def setUp(self):
        if 'REQUEST_EDITABLE' in os.environ:
            del os.environ['REQUEST_EDITABLE']
        super().setUp()

    def test_request_edit(self):
        @self.app.route('/test')
        def test_request():
            with self.assertRaises(TypeError):
                flask.request.args['Test'] = 'A'
            return flask.request.args.get('Test', 'Blank')

        with self.app.test_client() as client:
            r = client.get('/test')
            self.assertEqual(r.data, b'Blank')

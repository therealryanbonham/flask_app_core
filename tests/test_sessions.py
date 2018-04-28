import flask
from tests import BaseTest
import os


class SessionTests(object):

    def test_session(self):
        @self.app.route('/set', methods=['POST'])
        def set_session():
            flask.session['value'] = flask.request.form['value']
            return 'value set'

        @self.app.route('/get')
        def get_session():
            v = flask.session.get('value', 'None')
            return v
        self.app.config.update(
            SERVER_NAME='example.com:8080'
        )
        with self.app.test_client() as client:
            r = client.post('/set', data={'value': '42'})
            assert r.data == b'value set'
            assert 'domain=.example.com' in r.headers['set-cookie'].lower()
            assert 'httponly' in r.headers['set-cookie'].lower()
            assert client.get('/get').data == b'42'


class FileSessionTests(BaseTest, SessionTests):

    def setUp(self):
        os.environ['SESSION_TYPE'] = 'filesystem'
        super().setUp()


class RedisSessionTests(BaseTest, SessionTests):

    def setUp(self):
        os.environ['SESSION_TYPE'] = 'redis'
        super().setUp()


class NoneSessionTests(BaseTest, SessionTests):

    def setUp(self):
        if 'SESSION_TYPE' in os.environ:
            del os.environ['SESSION_TYPE']
        super().setUp()

    def test_session(self):
        @self.app.route('/set', methods=['POST'])
        def set_session():
            flask.session['value'] = flask.request.form['value']
            return 'value set'

        @self.app.route('/get')
        def get_session():
            v = flask.session.get('value', 'None')
            return v
        self.app.config.update(
            SERVER_NAME='example.com:8080'
        )
        with self.app.test_client() as client:
            r = client.post('/set', data={'value': '42'})
            assert r.data == b'value set'
            assert 'set-cookie' not in r.headers
            assert client.get('/get').data == b'None'

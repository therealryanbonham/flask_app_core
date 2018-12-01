import os
import flask
from .log import setup_logging
from .aws_xray import enable_xray
from .sessions import setup_sessions
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.datastructures import MultiDict


# Deriving from flask.Request
class TheRequest(flask.Request):
    parameter_storage_class = (
        MultiDict
    )  # This is the only parameter that is going to be different


def set_flask_debug(app):
    debug = os.environ.get("FLASK_DEBUG", False)
    if debug is not False:
        app.debug = True


def set_flask_secrets(app):
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")


def set_flask_debug_toolbar(app):
    enable_toolbar = os.environ.get("ENABLE_DEBUG_TB", False)
    if enable_toolbar is not False:
        from flask_debugtoolbar import DebugToolbarExtension

        DebugToolbarExtension(app)
        app.config["DEBUG_TB_TEMPLATE_EDITOR_ENABLED"] = True
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


def fix_proxy(app):
    enable_proxy_fix = os.environ.get("ENABLE_PROXY_FIX", False)
    if enable_proxy_fix is not False:
        app.wsgi_app = ProxyFix(app.wsgi_app)


def enable_db(app):
    enable_database_url = os.environ.get("DATABASE_URL", False)
    enable_xray = os.environ.get("ENABLE_XRAY", False)
    if enable_database_url is not False:
        from flask_sqlalchemy import SQLAlchemy

        app.config["SQLALCHEMY_DATABASE_URI"] = enable_database_url
        app.logger.debug("Connect to DB: {}".format(enable_database_url))
        if enable_xray is not False:
            from aws_xray_sdk.ext.flask_sqlalchemy.query import XRayFlaskSqlAlchemy

            return XRayFlaskSqlAlchemy(app)
        else:
            from flask_sqlalchemy import SQLAlchemy

            return SQLAlchemy(app)


def enable_track_modifications(app):
    enable_track_mod = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    if enable_track_mod is not False:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    else:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def make_requests_editable(app):
    enable = os.environ.get("REQUEST_EDITABLE", False)
    if enable is not False:
        app.request_class = (
            TheRequest
        )  # This is what actually effects the change of the form object's type


def enable_profiler(app):
    enable = os.environ.get("PROFILE", False)
    if enable is not False:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        f = open("profiler.log", "w+")
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, stream=f, restrictions=[30])


class FlaskWrapper(object):
    def __init__(self, name, app):
        setup_logging(app)
        set_flask_debug(app)
        enable_xray(name, app)
        setup_sessions(app)
        set_flask_secrets(app)
        set_flask_debug_toolbar(app)
        fix_proxy(app)
        enable_track_modifications(app)
        make_requests_editable(app)

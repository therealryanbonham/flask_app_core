import os
from tempfile import gettempdir
from flask.sessions import SecureCookieSessionInterface

VALID_SESSION_TYPE = ["redis", "dynamodb", "None", "filesystem"]


class InvalidSessionType(Exception):
    """Raise for my specific kind of exception"""


class RedisPythonModuleMissing(Exception):
    """Raise for my specific kind of exception"""


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, app, session, response):
        return


def setup_sessions(app):
    session_type = os.environ.get("SESSION_TYPE", "None")
    app.logger.debug("Session Type {}".format(session_type))
    if session_type not in VALID_SESSION_TYPE:
        message = "Invalid session type {}. Valid Options {}".format(
            session_type, VALID_SESSION_TYPE
        )
        app.logger.error(message)
        raise (InvalidSessionType(message))
    if session_type == "None":
        app.session_interface = CustomSessionInterface()
        return

    from flask_sessionstore import Session

    app.config["SESSION_TYPE"] = session_type
    app.config["SESSION_KEY_PREFIX"] = os.environ.get("SESSION_KEY_PREFIX", "SESSION")
    app.logger.debug("SESSION_KEY_PREFIX: {}".format(app.config["SESSION_KEY_PREFIX"]))
    if session_type == "filesystem":
        app.config["SESSION_FILE_DIR"] = gettempdir()
    elif session_type == "redis":
        import redis

        redis_host = os.environ.get("REDIS_HOST", None)
        app.logger.debug("Using Redis Host {} for Sessions".format(redis_host))
        app.config["SESSION_REDIS"] = redis.StrictRedis(redis_host)
    else:
        app.logger.debug("Using DynamoDB Session Table")
        app.config["SESSION_DYNAMODB_TABLE"] = os.environ.get(
            "SESSION_DYNAMODB_TABLE", "SessionTable"
        )
        app.config["SESSION_DYNAMODB_REGION"] = os.environ.get(
            "SESSION_DYNAMODB_REGION", "us-east-1"
        )
        app.config["SESSION_DYNAMODB_ENDPOINT_URL"] = os.environ.get(
            "SESSION_DYNAMODB_ENDPOINT_URL", None
        )
        app.logger.debug(
            "SESSION_DYNAMODB_TABLE: {}".format(app.config["SESSION_DYNAMODB_TABLE"])
        )
        app.logger.debug(
            "SESSION_DYNAMODB_REGION: {}".format(app.config["SESSION_DYNAMODB_REGION"])
        )
        app.logger.debug(
            "SESSION_DYNAMODB_ENDPOINT_URL: {}".format(
                app.config["SESSION_DYNAMODB_ENDPOINT_URL"]
            )
        )
    # Should Session Cookies Be Insecure?
    # This is bad, and should only be used in dev
    insecure_cookie = os.environ.get("SESSION_COOKIE_INSECURE", False)
    if not insecure_cookie:
        app.config["SESSION_COOKIE_SECURE"] = True
    else:
        app.logger.warning("You Are Using InSecure Session Cookies")
    app.config["SESSION_COOKIE_DOMAIN"] = os.environ.get("SESSION_COOKIE_DOMAIN", None)
    app.logger.debug(
        "Using Security Session Cookie: {}".format(app.config["SESSION_COOKIE_SECURE"])
    )
    app.logger.debug(
        "Using Session Cookie Domain: {}".format(app.config["SESSION_COOKIE_DOMAIN"])
    )  # override the fl
    app.logger.debug(
        "Using Server Name: {}".format(app.config["SERVER_NAME"])
    )  # override the fl
    Session(app)

"""Log handling Setup"""
import logging
import os
from logging import StreamHandler


def setup_logging(app):
    """Sets log levels for the flask app.
    Defualts to INFO and can be overridden by environment variable
    called LOG_LEVEL. Options are 'INFO', 'ERROR', 'WARN', 'DEBUG'

    Arguments:
        app {[object]} -- Pass in you flask app object
    """
    log_options = ["INFO", "ERROR", "WARN", "DEBUG"]
    log_handler = StreamHandler()
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    if log_level not in log_options:
        app.logger.error(
            "LOG_LEVEL {} is invalid. Valid options are {}".format(
                log_level, log_options
            )
        )
    if log_level == "ERROR":
        app.logger.setLevel(logging.ERROR)
    if log_level == "WARN":
        app.logger.setLevel(logging.WARN)
    if log_level == "DEBUG":
        app.logger.setLevel(logging.DEBUG)
    app.logger.info("Log Level Set {}".format(log_level))

import os
import logging
from aws_xray_sdk.core.context import Context
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.core import xray_recorder, patch_all


def enable_xray(name, app):
    enable_xray = os.environ.get("ENABLE_XRAY", False)
    if enable_xray is not False:
        # Initialize xray
        patch_all()
        xray_recorder.configure(
            service=name, sampling=False, context=Context(), context_missing="LOG_ERROR"
        )
        XRayMiddleware(app, xray_recorder)
        logging.getLogger("aws_xray_sdk").setLevel(logging.ERROR)

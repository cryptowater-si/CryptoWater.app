import logging

from os import getenv

import sentry_sdk
from sentry_sdk import capture_message, capture_exception
from sentry_sdk.integrations.flask import FlaskIntegration

env_environment = getenv("ENVIRONMENT", "DEV")
env_debug_mode = getenv("DEBUG_MODE", "False")
env_server_name = getenv("SERVER_NAME", "Unknown")
env_sw_version = getenv("APP_VERSION", "0")
_release_name = env_server_name + ":" + env_sw_version
#  Set Logger Format:
logger_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
)
# Setup logger
log = logging.getLogger(_release_name)
# Set level
log.setLevel(logging.DEBUG)

# Console LOG:
__consoleLogger = logging.StreamHandler()
__consoleLogger.setLevel(logging.INFO)
__consoleLogger.setFormatter(logger_format)
log.addHandler(__consoleLogger)

# File LOG
log_path = getenv("LOG_PATH", "debug.log")
_file_logger = logging.FileHandler(log_path)
_file_logger.setLevel(logging.DEBUG)
_file_logger.setFormatter(logger_format)
log.addHandler(_file_logger)

# SET UP SENTRY
try:
    sentry_sdk.init(
        getenv("SENTRY_TOKEN"),
        integrations=[FlaskIntegration()],
        environment=env_environment,
        server_name=env_server_name,
        release=_release_name,
        send_default_pii=True,
    )

except Exception as err:
    log.error("Unable to set up Sentry logging. Reason: {0}".format(err))

captureException = capture_exception
captureMessage = capture_message

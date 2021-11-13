from os import getenv
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler
from flask_toastr import Toastr


# Cross script protection
csrf_protect = CSRFProtect()

# Bootstrap for wtf render
bootstraper = Bootstrap()

# Cron
scheduler = APScheduler()

# Notifications
toastr = Toastr()


class Config(object):
    """Base config."""

    SECRET_KEY = getenv("SECRET_KEY", None)
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Max File size
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True

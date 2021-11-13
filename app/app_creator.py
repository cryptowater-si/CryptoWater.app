from os import getenv

from flask import Flask
from lib.logger import log
from lib.core_inits import ProdConfig, DevConfig, csrf_protect, bootstraper, toastr
from lib.custom_filters import CustomTemplateFilters


def create_app():

    env = getenv("ENVIRONMENT", "DEV")
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Add logger
    app.logger.addHandler(log)

    # Config
    if env != "PROD":
        app.config.from_object(DevConfig)
    else:
        app.config.from_object(ProdConfig)

    # Csrf
    csrf_protect.init_app(app)

    # Bootstrap
    bootstraper.init_app(app)

    # Toaster (for notifications)
    toastr.init_app(app)

    # Add custom template filters
    CustomTemplateFilters(app)

    from endpoints.coin_search_blueprint import coin_search_blueprint

    app.register_blueprint(coin_search_blueprint)

    return app

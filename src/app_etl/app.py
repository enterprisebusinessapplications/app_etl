import logging
import sys
import os
from logging import log
from flask import Flask
from app_etl.api.etl_resource import etl_api

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def create_app(test_config=None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(etl_api, url_prefix="/api")

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


app = create_app()
app.run()

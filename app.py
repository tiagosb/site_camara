from flask import Flask
from ext import config, database, command
from blueprints import init_app as bp_init_app


def create_minimal_app(**configs):
    app = Flask(__name__)
    return app


def create_app(**configs):
    app = create_minimal_app(**configs)
    config.init_app(app, **configs)
    database.init_app(app)
    bp_init_app(app)
    command.init_app(app)
    return app

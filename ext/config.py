from dynaconf import FlaskDynaconf


def init_app(app, **config):
    app.url_map.strict_slashes = False
    FlaskDynaconf(app, **config)

import pytest
from app import create_app
from ext import database


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    with app.app_context():
        database.con.create_all(app=app)
        yield app
        database.con.drop_all(app=app)

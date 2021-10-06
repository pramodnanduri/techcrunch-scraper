import os

import pytest

from server import server as flask_app


@pytest.fixture
def app():
    yield flask_app




@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    TEST_DB = 'scraper.db'
    mycwd = os.getcwd()
    os.chdir("..")
    base_dir = os.getcwd()
    os.chdir(mycwd)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, TEST_DB)
    return app.test_client()

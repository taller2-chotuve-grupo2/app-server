import pytest
from app import create_app, db as _db
from config import TestConfig
from repositories import user_repository


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.yield_fixture(scope="session")
def db(app):
    _db.app = app
    _db.create_all()

    u1 = user_repository.save_user("Rich", "123")
    u2 = user_repository.save_user("Roc", "321")
    u3 = user_repository.save_user("Ricson", "456")
    u1.add_friend(u2)
    u1.add_friend(u3)
    u3.accept_friend(u1)

    u1 = user_repository.save_user("admin", "123")
    u2 = user_repository.save_user("admin1005", "123")
    u3 = user_repository.save_user("tbotalla@fi.uba.ar", "123")
    u4 = user_repository.save_user("admin9", "123")

    u1.add_friend(u2)
    u1.add_friend(u3)
    u1.add_friend(u4)

    u2.add_friend(u3)

    u2.accept_friend(u1)
    u4.accept_friend(u1)
    u3.accept_friend(u1)
    u3.accept_friend(u2)
    yield _db

    _db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()

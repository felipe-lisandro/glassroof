"""
conftest.py — shared fixtures for the entire test suite.

The app is created once per test session using an in-memory SQLite database,
and each test gets its own transaction that is rolled back at the end, keeping
tests fully isolated without having to recreate the schema every time.
"""

import pytest

from app import create_app, db as _db
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Disable CSRF / extra overhead that is not relevant for unit tests
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope="session")
def app():
    """Create the Flask application once for the whole test session."""
    application = create_app(TestConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    """Flask test client, reused across the session."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """
    Roll back every DB write after each test so tests never share state.
    Uses a nested (SAVEPOINT) transaction so the outer connection stays open.
    """
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()

        # Bind the session to this connection so all writes go through it
        _db.session.bind = connection  # type: ignore[assignment]

        yield

        _db.session.remove()
        transaction.rollback()
        connection.close()

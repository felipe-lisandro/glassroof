"""
conftest.py — shared fixtures for the entire test suite.

The app is created once per session using an in-memory SQLite database.
After each test, all table rows are deleted so tests never share state.
This is more reliable than the session.bind / SAVEPOINT trick, which
only works on SQLAlchemy 1.x.
"""

import pytest

from app import create_app, db as _db
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
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
    Delete all rows from every table after each test.
    Works with SQLAlchemy 2.x and keeps the schema intact across the session.
    """
    yield
    with app.app_context():
        _db.session.remove()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()

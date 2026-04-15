"""
test_health_routes.py — integration tests for the /api/health endpoint.
"""

from unittest.mock import patch


class TestHealthCheck:
    def test_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_status_is_ok(self, client):
        res = client.get("/health")
        assert res.get_json()["status"] == "ok"

    def test_database_connected(self, client):
        # With the in-memory SQLite fixture the DB is always up
        res = client.get("/health")
        assert res.get_json()["database"] == "connected"

    def test_database_disconnected_on_db_error(self, client, app):
        """Simulate a DB failure and ensure the endpoint still returns 200."""
        with patch("app.db") as mock_db:
            mock_db.session.execute.side_effect = Exception("DB is down")
            res = client.get("/health")
            body = res.get_json()
            assert res.status_code == 200
            assert body["status"] == "ok"
            assert body["database"] == "disconnected"

    def test_response_has_required_keys(self, client):
        body = client.get("/health").get_json()
        assert "status" in body
        assert "database" in body

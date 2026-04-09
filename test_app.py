import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


# ── Page Load Tests ────────────────────────────────────────────────────────

def test_home_page_loads(client):
    """The dashboard should render with a 200 status."""
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Live Production Telemetry' in resp.data


# ── Metrics API Tests ──────────────────────────────────────────────────────

def test_metrics_returns_json(client):
    """GET /metrics should return valid JSON with expected keys."""
    resp = client.get('/metrics')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    for key in ('cpu', 'ram', 'disk', 'threads', 'net_sent', 'net_recv', 'uptime', 'requests', 'timestamp'):
        assert key in data, f"Missing key: {key}"


def test_metrics_value_ranges(client):
    """CPU and RAM percentages should be within 0-100."""
    resp = client.get('/metrics')
    data = json.loads(resp.data)
    assert 0 <= data['cpu'] <= 100
    assert 0 <= data['ram'] <= 100
    assert 0 <= data['disk'] <= 100


def test_metrics_types(client):
    """Verify the data types of metric values."""
    resp = client.get('/metrics')
    data = json.loads(resp.data)
    assert isinstance(data['cpu'], (int, float))
    assert isinstance(data['ram'], (int, float))
    assert isinstance(data['threads'], int)
    assert isinstance(data['uptime'], int)
    assert isinstance(data['requests'], int)


# ── History Endpoint Tests ─────────────────────────────────────────────────

def test_metrics_history_returns_list(client):
    """GET /metrics/history should return a list."""
    # Seed at least one data-point
    client.get('/metrics')
    resp = client.get('/metrics/history')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) >= 1


# ── Health Check Tests ─────────────────────────────────────────────────────

def test_health_endpoint(client):
    """GET /health should return status, checks, uptime, and version."""
    resp = client.get('/health')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['status'] == 'healthy'
    assert 'checks' in data
    assert 'version' in data


# ── Performance Test ───────────────────────────────────────────────────────

def test_metrics_response_time(client):
    """The /metrics endpoint should respond in < 2 seconds."""
    import time
    start = time.time()
    client.get('/metrics')
    elapsed = time.time() - start
    assert elapsed < 2.0, f"Response took {elapsed:.2f}s — too slow"

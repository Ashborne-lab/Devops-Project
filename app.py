from flask import Flask, render_template, jsonify, request
import psutil
import threading
import time
from collections import deque
from datetime import datetime

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory stores for live telemetry
# ---------------------------------------------------------------------------
HISTORY_MAX = 60  # keep 60 data-points (≈ 1 minute at 1 req/s)
metrics_history = deque(maxlen=HISTORY_MAX)
request_count = 0
start_time = time.time()


# ---------------------------------------------------------------------------
# Middleware — count every request
# ---------------------------------------------------------------------------
@app.before_request
def _count_request():
    global request_count
    request_count += 1


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/metrics')
def metrics():
    """Return a snapshot of live system metrics."""
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    payload = {
        'cpu': cpu,
        'ram': mem.percent,
        'disk': disk.percent,
        'threads': threading.active_count(),
        'net_sent': net.bytes_sent,
        'net_recv': net.bytes_recv,
        'uptime': round(time.time() - start_time),
        'requests': request_count,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }

    # Append to history ring-buffer
    metrics_history.append(payload)
    return jsonify(payload)


@app.route('/metrics/history')
def metrics_hist():
    """Return the last 60 metric snapshots for sparkline rendering."""
    return jsonify(list(metrics_history))


@app.route('/health')
def health():
    """Structured health-check endpoint used by Docker HEALTHCHECK & monitoring."""
    checks = {
        'flask': 'ok',
        'cpu_readable': psutil.cpu_percent(interval=0) is not None,
        'memory_readable': psutil.virtual_memory() is not None,
    }
    status = 'healthy' if all(checks.values()) else 'degraded'
    return jsonify({
        'status': status,
        'checks': checks,
        'uptime': round(time.time() - start_time),
        'version': '2.0.0',
    }), 200 if status == 'healthy' else 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
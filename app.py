from flask import Flask, render_template, jsonify
import psutil
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    # Read the live hardware metrics from the Docker container
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    active_threads = threading.active_count()
    
    return jsonify({
        'cpu': cpu_usage,
        'ram': ram_usage,
        'threads': active_threads
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
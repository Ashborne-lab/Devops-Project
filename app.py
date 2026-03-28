from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>DevOps Pipeline Active</h1><p id='status'>Application is running successfully.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
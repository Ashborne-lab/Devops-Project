from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # This tells Flask to look in the 'templates' folder and serve the dashboard
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
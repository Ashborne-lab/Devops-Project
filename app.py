from flask import Flask, render_template, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Receive the text from the frontend
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
        
    # Run the NLP Sentiment Analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # Determine the category based on the math score (-1.0 to 1.0)
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
        
    # Send the result back to the dashboard
    return jsonify({
        'sentiment': sentiment,
        'polarity': round(polarity, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
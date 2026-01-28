from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Bid Monitor</title></head>
    <body style="font-family: Arial; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h1>✅ Bid Monitor is Running!</h1>
        <p>API Endpoints:</p>
        <ul>
            <li><a href="/api/health" style="color: white;">/api/health</a> - Health check</li>
            <li><a href="/api/bids" style="color: white;">/api/bids</a> - Get all bids</li>
        </ul>
        <p><strong>Status:</strong> Deployment successful!</p>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Bid Monitor API is running'
    })

@app.route('/api/bids')
def get_bids():
    # Sample bid data (we'll connect real bot later)
    sample_bids = [
        {
            'id': 1,
            'title': 'Storm Sewer Cleaning Services',
            'location': 'Cleveland, OH',
            'type': 'Municipal',
            'deadline': '2026-02-15',
            'url': 'https://www.clevelandohio.gov'
        }
    ]
    
    return jsonify({
        'success': True,
        'count': len(sample_bids),
        'bids': sample_bids
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

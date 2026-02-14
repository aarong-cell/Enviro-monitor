from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
from datetime import datetime
import threading
import time

# Import the bot
from bid_monitor_bot import BidMonitorBot

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# In-memory storage for demo (we'll add database later)
bids_cache = []
last_update = None

def run_monitor():
    """Run the bid monitor and update cache"""
    global bids_cache, last_update
    
    try:
        print(f"\n🔄 Running monitor at {datetime.now()}")
        bot = BidMonitorBot()
        
        # Run scrapers
        bot.scrape_cleveland_city()
        time.sleep(1)
        bot.scrape_cuyahoga_county()
        time.sleep(1)
        bot.scrape_ohio_state()
        time.sleep(1)
        bot.add_sample_opportunities()
        
        # Update cache
        bids_cache = bot.opportunities
        last_update = datetime.now().isoformat()
        
        print(f"✅ Found {len(bids_cache)} opportunities")
        return True
        
    except Exception as e:
        print(f"❌ Monitor error: {e}")
        return False

def monitor_loop():
    """Background monitoring every 6 hours"""
    while True:
        run_monitor()
        print("⏰ Next update in 6 hours...")
        time.sleep(6 * 3600)  # 6 hours

# Routes
@app.route('/')
def home():
    return f'''
    <html>
    <head><title>Bid Monitor</title></head>
    <body style="font-family: Arial; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h1>✅ Cleveland Bid Monitor</h1>
        <p><strong>Status:</strong> Running</p>
        <p><strong>Tracking:</strong> Stormwater, Vac Trucks, Cleaning Services</p>
        <p><strong>Last Update:</strong> {last_update or "Never"}</p>
        <hr>
        <h3>API Endpoints:</h3>
        <ul>
            <li><a href="/api/health" style="color: white;">/api/health</a> - Health check</li>
            <li><a href="/api/bids" style="color: white;">/api/bids</a> - Get all bids ({len(bids_cache)} total)</li>
            <li><a href="/api/statistics" style="color: white;">/api/statistics</a> - Statistics</li>
            <li><a href="/api/refresh" style="color: white;">/api/refresh</a> - Manual refresh (POST)</li>
        </ul>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Bid Monitor API is running',
        'bids_count': len(bids_cache),
        'last_update': last_update
    })

@app.route('/api/bids')
def get_bids():
    return jsonify({
        'success': True,
        'count': len(bids_cache),
        'bids': bids_cache,
        'last_update': last_update
    })

@app.route('/api/statistics')
def get_stats():
    stats = {
        'total': len(bids_cache),
        'municipal': len([b for b in bids_cache if b.get('type') == 'Municipal']),
        'county': len([b for b in bids_cache if b.get('type') == 'County']),
        'state': len([b for b in bids_cache if b.get('type') == 'State']),
    }
    
    return jsonify({
        'success': True,
        'statistics': stats,
        'last_update': last_update
    })

@app.route('/api/refresh', methods=['POST'])
def refresh():
    success = run_monitor()
    
    return jsonify({
        'success': success,
        'message': 'Refresh completed' if success else 'Refresh failed',
        'bids_count': len(bids_cache)
    })

# Startup
def startup():
    print("\n" + "="*60)
    print("🚀 BID MONITOR - CLEVELAND, OHIO")
    print("="*60)
    
    # Initial monitor run
    print("Running initial check...")
    run_monitor()
    
    # Start background thread
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    
    print("\n✅ App ready!")
    print("="*60 + "\n")

if __name__ == '__main__':
    startup()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
else:
    # For Gunicorn
    startup()


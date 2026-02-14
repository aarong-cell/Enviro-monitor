from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
import threading
import time

# Import the bot
from bid_monitor_bot import BidMonitorBot

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Global storage
bids_cache = []
last_update = None
monitor_running = False

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
    global monitor_running
    monitor_running = True
    
    while True:
        run_monitor()
        print("⏰ Next update in 6 hours...")
        time.sleep(6 * 3600)

def start_monitoring():
    """Start background monitoring thread"""
    global monitor_running
    
    if not monitor_running:
        print("🚀 Starting bid monitor...")
        
        # Run immediately
        run_monitor()
        
        # Start background thread
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        
        print("✅ Monitor started!")

# Routes
@app.route('/')
def index():
    """Serve the dashboard"""
    if not monitor_running:
        start_monitoring()
    return send_from_directory('static', 'index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/api/health')
def health():
    if not monitor_running:
        start_monitoring()
    
    return jsonify({
        'status': 'ok',
        'message': 'Bid Monitor API is running',
        'bids_count': len(bids_cache),
        'last_update': last_update,
        'monitor_active': monitor_running
    })

@app.route('/api/bids')
def get_bids():
    if not monitor_running:
        start_monitoring()
    
    return jsonify({
        'success': True,
        'count': len(bids_cache),
        'bids': bids_cache,
        'last_update': last_update
    })

@app.route('/api/statistics')
def get_stats():
    if not monitor_running:
        start_monitoring()
    
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

@app.route('/api/refresh', methods=['POST', 'GET'])
def refresh():
    success = run_monitor()
    
    return jsonify({
        'success': success,
        'message': 'Refresh completed' if success else 'Refresh failed',
        'bids_count': len(bids_cache),
        'last_update': last_update
    })

# For local testing
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

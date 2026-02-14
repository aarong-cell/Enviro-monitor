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
        print(f"\n🔄 Running OHIO STATEWIDE monitor at {datetime.now()}")
        bot = BidMonitorBot()
        
        # Run ALL Ohio scrapers
        opportunities = bot.run_all_scrapers()
        
        # Update cache
        bids_cache = opportunities
        last_update = datetime.now().isoformat()
        
        print(f"✅ Found {len(bids_cache)} REAL opportunities across Ohio")
        return True
        
    except Exception as e:
        print(f"❌ Monitor error: {e}")
        import traceback
        traceback.print_exc()
        return False

def monitor_loop():
    """Background monitoring every 6 hours"""
    global monitor_running
    monitor_running = True
    
    while True:
        run_monitor()
        print("⏰ Next statewide scan in 6 hours...")
        time.sleep(6 * 3600)

def start_monitoring():
    """Start background monitoring thread"""
    global monitor_running
    
    if not monitor_running:
        print("🚀 Starting OHIO STATEWIDE bid monitor...")
        
        # Run immediately
        run_monitor()
        
        # Start background thread
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        
        print("✅ Statewide monitor started!")

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
        'message': 'Ohio Statewide Bid Monitor is running',
        'bids_count': len(bids_cache),
        'last_update': last_update,
        'monitor_active': monitor_running,
        'coverage': 'All of Ohio - State, Counties, Major Cities'
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
    
    # Count by source
    sources = {}
    for bid in bids_cache:
        source = bid.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    return jsonify({
        'success': True,
        'statistics': stats,
        'sources': sources,
        'last_update': last_update
    })

@app.route('/api/refresh', methods=['POST', 'GET'])
def refresh():
    success = run_monitor()
    
    return jsonify({
        'success': success,
        'message': 'Statewide refresh completed' if success else 'Refresh failed',
        'bids_count': len(bids_cache),
        'last_update': last_update
    })

# For local testing
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

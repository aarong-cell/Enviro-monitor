from flask import Flask, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import threading
import time

# Import the bot
from bid_monitor_bot import BidMonitorBot

app = Flask(__name__)
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
def home():
    # Start monitoring on first request
    if not monitor_running:
        start_monitoring()
    
    return f'''
    <html>
    <head>
        <title>Cleveland Bid Monitor</title>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                max-width: 800px;
                padding: 40px;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            h1 {{
                margin: 0 0 20px 0;
                font-size: 42px;
            }}
            .status {{
                background: rgba(255,255,255,0.2);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .status-item {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }}
            .status-item:last-child {{
                border-bottom: none;
            }}
            .api-links {{
                margin-top: 30px;
            }}
            .api-link {{
                display: block;
                padding: 15px 20px;
                margin: 10px 0;
                background: rgba(255,255,255,0.2);
                border-radius: 10px;
                text-decoration: none;
                color: white;
                transition: all 0.3s;
            }}
            .api-link:hover {{
                background: rgba(255,255,255,0.3);
                transform: translateX(10px);
            }}
            .badge {{
                background: rgba(76, 175, 80, 0.3);
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Cleveland Bid Monitor</h1>
            
            <div class="status">
                <div class="status-item">
                    <span><strong>Status:</strong></span>
                    <span class="badge">🟢 RUNNING</span>
                </div>
                <div class="status-item">
                    <span><strong>Tracking:</strong></span>
                    <span>Stormwater, Vac Trucks, Cleaning</span>
                </div>
                <div class="status-item">
                    <span><strong>Opportunities Found:</strong></span>
                    <span><strong>{len(bids_cache)}</strong> active bids</span>
                </div>
                <div class="status-item">
                    <span><strong>Last Update:</strong></span>
                    <span>{last_update or "Updating..."}</span>
                </div>
                <div class="status-item">
                    <span><strong>Coverage:</strong></span>
                    <span>Cleveland, Cuyahoga County, Ohio</span>
                </div>
            </div>
            
            <div class="api-links">
                <h3>📡 API Endpoints:</h3>
                <a href="/api/health" class="api-link">
                    🏥 Health Check
                </a>
                <a href="/api/bids" class="api-link">
                    📋 View All Bids ({len(bids_cache)} total)
                </a>
                <a href="/api/statistics" class="api-link">
                    📊 Statistics & Breakdown
                </a>
            </div>
            
            <p style="margin-top: 30px; opacity: 0.8; text-align: center;">
                🤖 Auto-refreshes every 6 hours
            </p>
        </div>
    </body>
    </html>
    '''

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

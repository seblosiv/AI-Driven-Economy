# Life After AI - Deployment Guide

Choose your preferred deployment platform:

---

## 🚀 Option 1: Render.com (Recommended - Easiest)

**Pros**: Free tier, web UI, automatic deploys from GitHub
**Cons**: Services sleep after inactivity (cold starts)

### Steps:

1. **Sign up for Render**: https://render.com
2. **Connect GitHub**: Link your repository
3. **Deploy with Blueprint**:
   - Go to https://dashboard.render.com/blueprints
   - Click "New Blueprint Instance"
   - Connect your GitHub repo: `seblosiv/AI-Driven-Economy`
   - Select branch: `claude/life-after-ai-mvp-011CUw2hyMCcfaVjvMFppLWG`
   - Render will auto-detect `render.yaml`
   - Click "Apply"

4. **Wait for deployment** (5-10 minutes)
5. **Access your app**: `https://lifeafterai.onrender.com`

### Adding Optional API Keys (Later):

In Render dashboard, go to each service → Environment → Add:
- `OPENAI_API_KEY`: For AI-generated plans
- `STRIPE_SECRET_KEY`: For payments
- `POSTHOG_API_KEY`: For analytics

---

## 🚀 Option 2: Fly.io (Best for Always-On)

**Pros**: Better free tier, faster, no cold starts
**Cons**: Requires CLI installation

### Steps:

1. **Install Fly CLI**:
   ```bash
   # Mac
   curl -L https://fly.io/install.sh | sh

   # Linux
   curl -L https://fly.io/install.sh | sh

   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Sign up and login**:
   ```bash
   flyctl auth signup  # or: flyctl auth login
   ```

3. **Create Postgres database**:
   ```bash
   flyctl postgres create --name lifeafterai-db --region iad
   ```

4. **Deploy the app**:
   ```bash
   cd /path/to/AI-Driven-Economy

   # Launch app
   flyctl launch --no-deploy

   # Attach database
   flyctl postgres attach lifeafterai-db

   # Set secrets
   flyctl secrets set SECRET_KEY=$(openssl rand -hex 32)
   flyctl secrets set ENVIRONMENT=production

   # Deploy
   flyctl deploy
   ```

5. **Access your app**:
   ```bash
   flyctl open
   ```

### Adding Optional API Keys:

```bash
flyctl secrets set OPENAI_API_KEY="sk-..."
flyctl secrets set STRIPE_SECRET_KEY="sk_live_..."
flyctl secrets set POSTHOG_API_KEY="phc_..."
```

---

## 🚀 Option 3: Railway (Alternative)

**Pros**: Simple, nice UI, good free tier
**Cons**: Free tier limited to $5/month credit

### Steps:

1. **Sign up**: https://railway.app
2. **Install CLI**:
   ```bash
   npm i -g @railway/cli
   railway login
   ```

3. **Deploy**:
   ```bash
   cd /path/to/AI-Driven-Economy
   railway init
   railway up
   ```

4. **Add database**:
   - In Railway dashboard, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway auto-injects `DATABASE_URL`

5. **Configure environment variables** in dashboard:
   - `SECRET_KEY`: Generate random string
   - `FRONTEND_URL`: Your Railway frontend URL
   - `ENVIRONMENT`: production

---

## 🚀 Option 4: Manual VPS Deployment

If you have a VPS (DigitalOcean, AWS, etc.):

```bash
# SSH into your server
ssh user@your-server.com

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com | sh
sudo apt-get install docker-compose

# Clone repo
git clone https://github.com/seblosiv/AI-Driven-Economy.git
cd AI-Driven-Economy
git checkout claude/life-after-ai-mvp-011CUw2hyMCcfaVjvMFppLWG

# Create .env file
cp .env.sample .env
# Edit .env with your production values

# Deploy
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## ⚙️ Environment Variables Reference

### Required:
- `DATABASE_URL`: Auto-set by most platforms
- `SECRET_KEY`: Random 32+ char string
- `FRONTEND_URL`: Your frontend domain
- `ENVIRONMENT`: production

### Optional (for full features):
- `OPENAI_API_KEY`: AI-generated career plans (falls back to rules)
- `STRIPE_SECRET_KEY`: Payment processing
- `STRIPE_PUBLISHABLE_KEY`: Payment frontend
- `STRIPE_PRICE_ID_MONTHLY`: Stripe price ID
- `STRIPE_PRICE_ID_YEARLY`: Stripe price ID
- `POSTHOG_API_KEY`: Analytics
- `RESEND_API_KEY`: Transactional emails

---

## 🎯 Quick Test After Deployment

1. Visit your deployed URL
2. Click "Start the 3-Minute Test"
3. Fill out the quiz
4. Verify results page loads with charts
5. Check API health: `https://your-app.com/api/health`
6. Check API docs: `https://your-app.com/api/docs`

---

## 🐛 Troubleshooting

### "Application Error" or 502/503
- Check logs in platform dashboard
- Verify DATABASE_URL is set correctly
- Ensure ports are correct (8000 for backend)

### Database Connection Failed
- Verify PostgreSQL is provisioned
- Check DATABASE_URL format: `postgresql://user:pass@host:5432/db`
- Ensure database migrations ran (check logs for "Created 150 occupations")

### Frontend Shows Blank Page
- Check browser console for errors
- Verify VITE_API_URL points to backend
- Check CORS settings in backend

### Cold Starts (Render free tier)
- First request after inactivity takes 30-60s
- Upgrade to paid tier ($7/mo) for instant wakeup

---

## 💰 Estimated Costs

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Render | ✅ Yes (sleeps) | $7/mo per service |
| Fly.io | ✅ Yes (2 VMs) | ~$5-10/mo |
| Railway | ✅ $5/mo credit | $20/mo |
| DigitalOcean | No | $6/mo (droplet) |

**Recommendation**: Start with Render free tier to demo, upgrade to Fly.io or Railway when ready for production.

---

## 📧 Need Help?

If you encounter issues:
1. Check platform-specific logs in dashboard
2. Verify all environment variables are set
3. Test locally with `docker-compose up` first
4. Check GitHub Actions for any CI failures

---

**Choose Option 1 (Render) for the fastest deployment right now!**

Just visit https://dashboard.render.com/blueprints and connect your repo.

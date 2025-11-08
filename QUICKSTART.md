# Life After AI - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### 1. Launch the Application

```bash
# Ensure Docker is running, then:
docker-compose up --build
```

Wait 30-60 seconds for services to start. You'll see:
```
✅ Database initialized
✅ Created 150 occupations
🚀 Starting Life After AI API...
```

### 2. Access the Application

Open your browser to:
- **App**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/health

### 3. Try the User Flow

1. Click **"Start the 3-Minute Test"** on the homepage
2. Fill out the quiz (job title, salary, skills, preferences)
3. View your personalized results:
   - Automation risk & timeline
   - AIDE dividend projections
   - Career transition insights
4. Explore **Premium** and **Learn** pages

### 4. Stop the Application

```bash
docker-compose down
```

---

## 🔧 Development Mode

### Backend Only (with hot reload)

```bash
cd app/backend
pip install -r requirements.txt
python -m app.backend.db.seed  # Seed database
uvicorn app.backend.main:app --reload
```

Backend runs at: http://localhost:8000

### Frontend Only (with hot reload)

```bash
cd app/frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

### Run Tests

```bash
# Backend tests
cd app/backend
pytest tests/ -v

# Frontend build test
cd app/frontend
npm run build
```

---

## 📊 Sample API Requests

### Search for Occupations

```bash
curl "http://localhost:8000/api/occupations/search?q=software"
```

### Get Automation Prediction

```bash
curl -X POST "http://localhost:8000/api/predict/automation" \
  -H "Content-Type: application/json" \
  -d '{"occupation_id": 15}'
```

### Simulate AIDE Dividend

```bash
curl -X POST "http://localhost:8000/api/simulate/dividend" \
  -H "Content-Type: application/json" \
  -d '{
    "sector": "Technology",
    "automation_score": 0.65,
    "base_salary": 100000,
    "country": "US"
  }'
```

---

## 🐛 Troubleshooting

### Database connection errors

```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

### Port already in use

Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Backend
  - "5174:80"    # Frontend
```

### Frontend can't reach backend

Check CORS settings in `app/backend/core/config.py` and ensure frontend URL is listed.

---

## 🎯 Next Steps

1. Configure `.env` with your API keys (optional):
   - OpenAI for AI-generated plans
   - Stripe for payments
   - PostHog for analytics
   - Resend for emails

2. Customize brand colors in `app/frontend/tailwind.config.js`

3. Add more occupations to `data/occupations.csv`

4. Deploy to production (see README.md)

---

**Need help?** Check the full README.md or create an issue.

# Life After AI 🚀

**Predict your job's automation risk, simulate your AI Dividend, and plan your future in the AI economy.**

A production-ready MVP that combines FastAPI backend with React frontend to deliver personalized insights into the future of work and AI-driven economic transformation.

---

## ✨ Features

### Core Functionality

- **🤖 Automation Risk Prediction**: Deterministic scoring algorithm analyzing 150+ occupations across multiple sectors with timeline estimates (1-20 years)
- **💰 AIDE Dividend Simulator**: Interactive projection tool showing potential universal income from automation surplus over 5/10/20 years
- **📋 Personal Career Plan**: AI-generated (with rules-based fallback) transition plans offering 3 tracks: Fast (3-6mo), Balanced (6-12mo), Deep (12-18mo)
- **🎨 Social Sharing**: Dynamic OG image generation for Twitter/LinkedIn with personalized stats
- **💎 Premium Features**: Stripe-powered subscriptions unlocking advanced scenarios, PDF reports, and priority features

### Tech Highlights

- **Backend**: FastAPI + SQLModel + Pydantic v2 + PostgreSQL
- **Frontend**: React 18 + Vite + TypeScript + TailwindCSS + shadcn/ui
- **Design**: Premium glassmorphism UI with Framer Motion animations
- **Analytics**: PostHog integration for event tracking
- **AI**: Abstracted LLM provider (OpenAI/DeepInfra/Groq) with intelligent rules fallback
- **DevOps**: Docker Compose + GitHub Actions CI/CD

---

## 🎯 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local dev)
- Python 3.11+ (for local dev)

### One-Command Launch

```bash
# Clone the repo
git clone <your-repo-url>
cd AI-Driven-Economy

# Start the entire stack
docker-compose up --build
```

**Access the app:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Seed Database

The database auto-seeds with 150 occupations on first run. To manually re-seed:

```bash
docker-compose exec backend python -m app.backend.db.seed
```

---

## 📂 Project Structure

```
AI-Driven-Economy/
├── app/
│   ├── backend/              # FastAPI application
│   │   ├── api/routers/      # API endpoints
│   │   ├── core/             # Configuration
│   │   ├── db/               # Database setup & seed
│   │   ├── models/           # SQLModel schemas
│   │   ├── services/         # Business logic
│   │   ├── tests/            # Unit tests
│   │   └── main.py           # FastAPI app entry
│   └── frontend/             # React application
│       ├── src/
│       │   ├── components/   # Reusable UI components
│       │   ├── lib/          # Utils, API client, analytics
│       │   ├── routes/       # Page components
│       │   └── main.tsx      # React entry
│       └── package.json
├── data/
│   └── occupations.csv       # 150 occupation seed data
├── infra/
│   └── nginx.conf            # Nginx config for frontend
├── docker-compose.yml
├── .env.sample               # Environment variables template
└── README.md
```

---

## 🧪 Running Tests

### Backend Tests

```bash
cd app/backend
python -m pytest tests/ -v --cov=app
```

**Test coverage includes:**
- ✅ Automation scoring algorithm (deterministic logic)
- ✅ AIDE dividend simulator (projections & parameters)
- ✅ API endpoints (integration tests)

### Frontend Build

```bash
cd app/frontend
npm run build
npm run lint
```

---

## 🔧 Environment Configuration

Copy `.env.sample` to `.env` and configure:

### Required (Development)

```bash
DATABASE_URL=postgresql://lifeafterai:lifeafterai@db:5432/lifeafterai
SECRET_KEY=your-secret-key-change-in-production
```

### Optional (Production)

```bash
# AI Provider (falls back to rules if not set)
OPENAI_API_KEY=sk-...
AI_PROVIDER=openai

# Stripe Payments
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_PRICE_ID_MONTHLY=price_...
STRIPE_PRICE_ID_YEARLY=price_...

# PostHog Analytics
POSTHOG_API_KEY=phc_...

# Email (Resend)
RESEND_API_KEY=re_...
FROM_EMAIL=hello@lifeafterai.com
```

---

## 📊 API Endpoints

All endpoints documented at **http://localhost:8000/api/docs** (Swagger UI)

### Key Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/magic-link` | Request passwordless login |
| POST | `/api/quiz/submit` | Submit quiz responses |
| GET | `/api/occupations/search?q=` | Search occupations (autocomplete) |
| POST | `/api/predict/automation` | Get automation risk prediction |
| POST | `/api/simulate/dividend` | Run AIDE dividend simulation |
| POST | `/api/plan/generate` | Generate career transition plan |
| POST | `/api/share/og` | Create OG share image |
| POST | `/api/checkout/session` | Create Stripe checkout |

---

## 🎨 Design System

### Brand Colors

```css
Charcoal:      #0F1115  /* Background */
Off-White:     #F7F7F5  /* Text */
Electric Blue: #5AA9FF  /* Primary accent */
Neon Mint:     #64FBD2  /* Secondary accent */
```

### Typography

- **UI**: Inter (400, 500, 600, 700)
- **Headlines**: Space Grotesk (500, 600, 700)

### Components

- **GlassCard**: Glassmorphism with `backdrop-blur-md bg-white/5 border-white/10`
- **Button**: Rounded-2xl with shadow glow effects
- **Metric**: Animated number display with delta indicators
- **RibbonCTA**: Prominent gradient CTA banners

---

## 🚀 Deployment

### Docker Production Build

```bash
# Set production environment variables in .env
export ENVIRONMENT=production

# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push:

1. ✅ Backend: Ruff lint + pytest
2. ✅ Frontend: ESLint + build
3. ✅ Docker: Build & integration test

---

## 📈 Performance & Accessibility

Target metrics (tested with Lighthouse):

- **Performance**: ≥ 90
- **Accessibility**: ≥ 95 (WCAG AA compliant)
- **Best Practices**: ≥ 95
- **SEO**: ≥ 90

Accessibility features:
- ARIA labels on interactive elements
- Keyboard navigation support
- `prefers-reduced-motion` respect
- Color contrast ratio > 4.5:1

---

## 🧩 Key Algorithms

### Automation Risk Scoring

```python
score = (
    0.30 * baseline_risk +      # Research-backed base probability
    0.35 * ai_velocity +         # AI advancement rate in domain
    0.25 * remote_feasibility -  # Digital work feasibility
    0.10 * protection_avg        # Creativity + Social + Physical skills
)

ETA = f(score, ai_velocity)     # Piecewise timeline mapping
```

### AIDE Dividend Simulation

```python
D_y = (S * τ * δ / P) * (1 + g)^y * γ_adj

Where:
S  = Sector automation surplus
τ  = Tax rate on automation (user adjustable)
δ  = Distribution share (user adjustable)
P  = Regional population
g  = Annual growth rate
γ  = Contribution bonus (1.0 to 1.5x for contributing to commons)
```

---

## 📝 License & Disclaimers

**License**: MIT (open source)

**Important Disclaimers**:
- Automation predictions are **illustrative** based on current research, not guarantees
- AIDE dividend projections are **hypothetical scenarios**, not financial advice
- No liability for career or financial decisions based on this tool
- Data sources: Frey & Osborne (2013), O*NET, World Bank, IMF

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new functionality
4. Ensure `ruff` (backend) and `eslint` (frontend) pass
5. Submit PR with clear description

---

## 📧 Contact & Support

- **Email**: hello@lifeafterai.com
- **Issues**: [GitHub Issues](https://github.com/your-org/AI-Driven-Economy/issues)
- **Docs**: [Full Documentation](https://docs.lifeafterai.com)

---

## 🎯 Roadmap

**v1.1** (Next Release)
- [ ] PDF report export
- [ ] Multi-language support (ES, FR, DE)
- [ ] Weekly automation watchlist emails
- [ ] Mobile app (React Native)

**v2.0** (Future)
- [ ] Community discussion forums
- [ ] Expert career coaching marketplace
- [ ] Company/sector automation dashboards
- [ ] Policy advocacy tools

---

**Built with ❤️ for a future-positive AI economy**

*"The future belongs to those who plan for it."*

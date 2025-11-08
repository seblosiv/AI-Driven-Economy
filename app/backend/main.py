"""
Life After AI - Main FastAPI Application

Production-ready MVP for AI automation prediction and AIDE dividend simulation.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.backend.core.config import settings
from app.backend.db.session import init_db

# Import routers
from app.backend.api.routers import (
    auth,
    quiz,
    occupations,
    predictions,
    simulator,
    plan,
    share,
    checkout
)

# Create FastAPI app
app = FastAPI(
    title="Life After AI API",
    description="Predict automation impact and plan your future in the AI economy",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for OG images
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(occupations.router)
app.include_router(predictions.router)
app.include_router(simulator.router)
app.include_router(plan.router)
app.include_router(share.router)
app.include_router(checkout.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("🚀 Starting Life After AI API...")
    print(f"📍 Environment: {settings.environment}")
    print(f"🔗 Frontend URL: {settings.frontend_url}")

    # Initialize database
    init_db()
    print("✅ Database initialized")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Life After AI API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )

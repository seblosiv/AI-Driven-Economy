#!/bin/bash
set -e

# Start nginx in background
nginx

# Run database seed
python -m app.backend.db.seed

# Start FastAPI
exec uvicorn app.backend.main:app --host 0.0.0.0 --port 8000

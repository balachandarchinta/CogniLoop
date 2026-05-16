# AI Cognitive Learning Architect - Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the AI Cognitive Learning Architect MVP. The implementation is organized into phases, with each phase building upon the previous one.

## Prerequisites

### Required Software
- Python 3.9 or higher
- Node.js 16+ and npm/yarn
- PostgreSQL 14+
- Redis 7+
- Git
- Docker and Docker Compose (optional but recommended)

### Required Python Packages
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
redis==5.0.1
celery==5.3.4
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
xgboost==2.0.2
tensorflow==2.15.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### Required Node Packages
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@reduxjs/toolkit": "^1.9.7",
    "react-redux": "^8.1.3",
    "@mui/material": "^5.14.18",
    "@mui/icons-material": "^5.14.18",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "axios": "^1.6.2",
    "recharts": "^2.10.3",
    "socket.io-client": "^4.5.4",
    "date-fns": "^2.30.0"
  },
  "devDependencies": {
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "jest": "^29.7.0",
    "cypress": "^13.6.1"
  }
}
```

## Project Structure

```
cognitive-learning-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── config.py                  # Configuration management
│   │   ├── database.py                # Database connection and session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── learner.py            # Learner model
│   │   │   ├── cognitive_profile.py  # Cognitive profile model
│   │   │   ├── learning_session.py   # Learning session model
│   │   │   ├── content.py            # Content library model
│   │   │   ├── interaction.py        # Learner-content interaction model
│   │   │   ├── assessment.py         # Assessment model
│   │   │   └── recommendation.py     # Recommendation model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── learner.py            # Pydantic schemas for learner
│   │   │   ├── cognitive_profile.py  # Pydantic schemas for profile
│   │   │   ├── learning_session.py   # Pydantic schemas for session
│   │   │   ├── content.py            # Pydantic schemas for content
│   │   │   └── recommendation.py     # Pydantic schemas for recommendations
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # API dependencies
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py           # Authentication endpoints
│   │   │       ├── learners.py       # Learner endpoints
│   │   │       ├── sessions.py       # Learning session endpoints
│   │   │       ├── content.py        # Content endpoints
│   │   │       ├── adaptive.py       # Adaptive learning endpoints
│   │   │       ├── engagement.py     # Engagement tracking endpoints
│   │   │       ├── recommendations.py # Recommendation endpoints
│   │   │       └── analytics.py      # Analytics endpoints
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py           # Security utilities (JWT, hashing)
│   │   │   ├── cognitive_profiling/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── profiler.py       # Main profiling engine
│   │   │   │   ├── learning_style_classifier.py
│   │   │   │   ├── attention_analyzer.py
│   │   │   │   └── retention_analyzer.py
│   │   │   ├── adaptive_learning/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── adaptation_engine.py
│   │   │   │   ├── difficulty_adjuster.py
│   │   │   │   ├── pace_optimizer.py
│   │   │   │   └── content_transformer.py
│   │   │   ├── engagement/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engagement_tracker.py
│   │   │   │   ├── distraction_detector.py
│   │   │   │   ├── attention_predictor.py
│   │   │   │   └── emotional_analyzer.py
│   │   │   └── recommendations/
│   │   │       ├── __init__.py
│   │   │       ├── recommender.py
│   │   │       ├── collaborative_filter.py
│   │   │       ├── content_filter.py
│   │   │       └── path_generator.py
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   │   ├── learning_style_model.pkl
│   │   │   │   ├── attention_model.h5
│   │   │   │   ├── engagement_model.pkl
│   │   │   │   └── recommendation_model.pkl
│   │   │   ├── training/
│   │   │   │   ├── train_learning_style.py
│   │   │   │   ├── train_attention.py
│   │   │   │   ├── train_engagement.py
│   │   │   │   └── train_recommender.py
│   │   │   └── inference/
│   │   │       ├── learning_style_inference.py
│   │   │       ├── attention_inference.py
│   │   │       ├── engagement_inference.py
│   │   │       └── recommendation_inference.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── learner_service.py
│   │   │   ├── session_service.py
│   │   │   ├── content_service.py
│   │   │   ├── profiling_service.py
│   │   │   ├── adaptation_service.py
│   │   │   └── recommendation_service.py
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   ├── profile_update.py
│   │   │   ├── engagement_analysis.py
│   │   │   └── recommendation_generation.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py
│   │       ├── validators.py
│   │       └── helpers.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   ├── test_core/
│   │   ├── test_ml/
│   │   └── test_services/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── alembic.ini
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── Register.jsx
│   │   │   │   └── InitialAssessment.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── LearnerDashboard.jsx
│   │   │   │   ├── CognitiveProfile.jsx
│   │   │   │   ├── ProgressOverview.jsx
│   │   │   │   └── EngagementMetrics.jsx
│   │   │   ├── learning/
│   │   │   │   ├── ContentViewer.jsx
│   │   │   │   ├── AdaptiveContent.jsx
│   │   │   │   ├── QuizComponent.jsx
│   │   │   │   └── InteractiveExercise.jsx
│   │   │   ├── analytics/
│   │   │   │   ├── AnalyticsDashboard.jsx
│   │   │   │   ├── CognitiveInsights.jsx
│   │   │   │   ├── EngagementTrends.jsx
│   │   │   │   └── ProgressCharts.jsx
│   │   │   ├── recommendations/
│   │   │   │   ├── RecommendationCard.jsx
│   │   │   │   ├── LearningPath.jsx
│   │   │   │   └── ScheduleSuggestions.jsx
│   │   │   └── common/
│   │   │       ├── Layout.jsx
│   │   │       ├── Navigation.jsx
│   │   │       ├── Loading.jsx
│   │   │       └── ErrorBoundary.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useEngagementTracking.js
│   │   │   ├── useCognitiveProfile.js
│   │   │   ├── useAdaptiveContent.js
│   │   │   └── useRecommendations.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   ├── tracking.js
│   │   │   └── websocket.js
│   │   ├── store/
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.js
│   │   │   │   ├── profileSlice.js
│   │   │   │   ├── learningSlice.js
│   │   │   │   └── analyticsSlice.js
│   │   │   └── store.js
│   │   ├── utils/
│   │   │   ├── engagementTracker.js
│   │   │   ├── behaviorLogger.js
│   │   │   ├── adaptationHelpers.js
│   │   │   └── constants.js
│   │   ├── styles/
│   │   │   ├── theme.js
│   │   │   └── global.css
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   └── routes.jsx
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
├── ARCHITECTURE.md
└── IMPLEMENTATION_GUIDE.md
```

## Phase 1: Project Setup and Infrastructure

### Step 1.1: Initialize Project Structure

```bash
# Create main project directory
mkdir cognitive-learning-platform
cd cognitive-learning-platform

# Create backend structure
mkdir -p backend/app/{models,schemas,api/v1,core/{cognitive_profiling,adaptive_learning,engagement,recommendations},ml/{models,training,inference},services,tasks,utils}
mkdir -p backend/alembic/versions
mkdir -p backend/tests/{test_api,test_core,test_ml,test_services}

# Create frontend structure
mkdir -p frontend/src/{components/{auth,dashboard,learning,analytics,recommendations,common},hooks,services,store/slices,utils,styles}
mkdir -p frontend/public

# Create __init__.py files for Python packages
find backend/app -type d -exec touch {}/__init__.py \;
```

### Step 1.2: Set Up Backend Environment

Create [`backend/.env.example`](backend/.env.example:1):
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cognitive_learning
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=0

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Application
APP_NAME=Cognitive Learning Platform
APP_VERSION=1.0.0
DEBUG=True

# ML Models
MODEL_PATH=app/ml/models
MODEL_UPDATE_INTERVAL=86400

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

Create [`backend/requirements.txt`](backend/requirements.txt:1):
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
redis==5.0.1
celery==5.3.4
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
xgboost==2.0.2
tensorflow==2.15.0
python-dotenv==1.0.0
```

Create [`backend/requirements-dev.txt`](backend/requirements-dev.txt:1):
```txt
-r requirements.txt
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

### Step 1.3: Set Up Frontend Environment

Create [`frontend/.env.example`](frontend/.env.example:1):
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_ENV=development
```

Create [`frontend/package.json`](frontend/package.json:1):
```json
{
  "name": "cognitive-learning-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@reduxjs/toolkit": "^1.9.7",
    "react-redux": "^8.1.3",
    "@mui/material": "^5.14.18",
    "@mui/icons-material": "^5.14.18",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "axios": "^1.6.2",
    "recharts": "^2.10.3",
    "socket.io-client": "^4.5.4",
    "date-fns": "^2.30.0"
  },
  "devDependencies": {
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "jest": "^29.7.0",
    "cypress": "^13.6.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

### Step 1.4: Docker Setup

Create [`docker-compose.yml`](docker-compose.yml:1):
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: cognitive_learning
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/cognitive_learning
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery_worker:
    build: ./backend
    command: celery -A app.tasks.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/cognitive_learning
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    command: npm start
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

## Phase 2: Database Models and Migrations

### Step 2.1: Configure Database Connection

Create [`backend/app/config.py`](backend/app/config.py:1):
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Application
    APP_NAME: str = "Cognitive Learning Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # ML Models
    MODEL_PATH: str = "app/ml/models"
    MODEL_UPDATE_INTERVAL: int = 86400
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

Create [`backend/app/database.py`](backend/app/database.py:1):
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 2.2: Create Database Models

The models should be created in the [`backend/app/models/`](backend/app/models/:1) directory following the schema defined in [`ARCHITECTURE.md`](ARCHITECTURE.md:1). Key models include:

- [`learner.py`](backend/app/models/learner.py:1) - User/learner model
- [`cognitive_profile.py`](backend/app/models/cognitive_profile.py:1) - Cognitive profile model
- [`learning_session.py`](backend/app/models/learning_session.py:1) - Learning session tracking
- [`content.py`](backend/app/models/content.py:1) - Content library
- [`interaction.py`](backend/app/models/interaction.py:1) - Learner-content interactions
- [`assessment.py`](backend/app/models/assessment.py:1) - Assessments and quizzes
- [`recommendation.py`](backend/app/models/recommendation.py:1) - Recommendations

### Step 2.3: Set Up Alembic for Migrations

```bash
cd backend
alembic init alembic
```

Update [`alembic.ini`](backend/alembic.ini:1) to use environment variable for database URL.

Update [`alembic/env.py`](backend/alembic/env.py:1) to import models and use async database connection.

## Phase 3: Core ML Components

### Step 3.1: Cognitive Profiling Engine

Implement the learning style classifier in [`backend/app/core/cognitive_profiling/learning_style_classifier.py`](backend/app/core/cognitive_profiling/learning_style_classifier.py:1):

Key features:
- Feature extraction from user interactions
- Random Forest classification
- Confidence scoring
- Profile updating logic

### Step 3.2: Adaptive Learning Engine

Implement adaptation logic in [`backend/app/core/adaptive_learning/adaptation_engine.py`](backend/app/core/adaptive_learning/adaptation_engine.py:1):

Key features:
- Real-time difficulty adjustment
- Content format transformation
- Pace optimization
- Trigger-based adaptation

### Step 3.3: Engagement Tracking System

Implement engagement tracking in [`backend/app/core/engagement/engagement_tracker.py`](backend/app/core/engagement/engagement_tracker.py:1):

Key features:
- Real-time engagement scoring
- Distraction detection
- Attention span monitoring
- Emotional engagement analysis

### Step 3.4: Recommendation Engine

Implement recommendation logic in [`backend/app/core/recommendations/recommender.py`](backend/app/core/recommendations/recommender.py:1):

Key features:
- Hybrid recommendation (collaborative + content-based)
- Learning path generation
- Schedule optimization
- Personalized content suggestions

## Phase 4: API Development

### Step 4.1: Authentication System

Implement JWT authentication in [`backend/app/core/security.py`](backend/app/core/security.py:1) and [`backend/app/api/v1/auth.py`](backend/app/api/v1/auth.py:1):

Endpoints:
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

### Step 4.2: Core API Endpoints

Implement endpoints in [`backend/app/api/v1/`](backend/app/api/v1/:1):

- [`learners.py`](backend/app/api/v1/learners.py:1) - Learner profile management
- [`sessions.py`](backend/app/api/v1/sessions.py:1) - Learning session tracking
- [`content.py`](backend/app/api/v1/content.py:1) - Content delivery
- [`adaptive.py`](backend/app/api/v1/adaptive.py:1) - Adaptive learning
- [`engagement.py`](backend/app/api/v1/engagement.py:1) - Engagement tracking
- [`recommendations.py`](backend/app/api/v1/recommendations.py:1) - Recommendations
- [`analytics.py`](backend/app/api/v1/analytics.py:1) - Analytics and insights

### Step 4.3: FastAPI Application Setup

Create [`backend/app/main.py`](backend/app/main.py:1):

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import auth, learners, sessions, content, adaptive, engagement, recommendations, analytics

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(learners.router, prefix="/api/v1/learners", tags=["learners"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(adaptive.router, prefix="/api/v1/adaptive", tags=["adaptive"])
app.include_router(engagement.router, prefix="/api/v1/engagement", tags=["engagement"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {"message": "Cognitive Learning Platform API", "version": settings.APP_VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

## Phase 5: Frontend Development

### Step 5.1: Set Up Redux Store

Create [`frontend/src/store/store.js`](frontend/src/store/store.js:1):

```javascript
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import profileReducer from './slices/profileSlice';
import learningReducer from './slices/learningSlice';
import analyticsReducer from './slices/analyticsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    profile: profileReducer,
    learning: learningReducer,
    analytics: analyticsReducer,
  },
});
```

### Step 5.2: Implement API Service

Create [`frontend/src/services/api.js`](frontend/src/services/api.js:1):

```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
          refresh_token: refreshToken,
        });
        
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

### Step 5.3: Implement Engagement Tracking Hook

Create [`frontend/src/hooks/useEngagementTracking.js`](frontend/src/hooks/useEngagementTracking.js:1):

```javascript
import { useEffect, useRef, useCallback } from 'react';
import { trackBehavioralEvent } from '../services/tracking';

export const useEngagementTracking = (sessionId, contentId) => {
  const startTime = useRef(Date.now());
  const scrollDepth = useRef(0);
  const interactionCount = useRef(0);
  const mouseMovements = useRef(0);
  const lastActivityTime = useRef(Date.now());

  const trackEvent = useCallback((eventType, eventData) => {
    if (sessionId && contentId) {
      trackBehavioralEvent({
        sessionId,
        contentId,
        eventType,
        eventData: {
          ...eventData,
          timestamp: Date.now(),
        },
      });
    }
  }, [sessionId, contentId]);

  useEffect(() => {
    if (!sessionId || !contentId) return;

    // Track scroll depth
    const handleScroll = () => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const depth = ((scrollTop + windowHeight) / documentHeight) * 100;
      
      scrollDepth.current = Math.max(scrollDepth.current, depth);
      lastActivityTime.current = Date.now();
      
      trackEvent('scroll', { depth: Math.round(depth) });
    };

    // Track mouse movements
    const handleMouseMove = () => {
      mouseMovements.current += 1;
      lastActivityTime.current = Date.now();
      
      if (mouseMovements.current % 50 === 0) {
        trackEvent('mouse_activity', { movements: mouseMovements.current });
      }
    };

    // Track clicks
    const handleClick = (e) => {
      interactionCount.current += 1;
      lastActivityTime.current = Date.now();
      
      trackEvent('click', {
        x: e.clientX,
        y: e.clientY,
        target: e.target.tagName,
      });
    };

    // Track tab visibility
    const handleVisibilityChange = () => {
      const isHidden = document.hidden;
      trackEvent(isHidden ? 'tab_hidden' : 'tab_visible', {
        timeSpent: Date.now() - startTime.current,
      });
    };

    // Track inactivity
    const inactivityChecker = setInterval(() => {
      const inactiveTime = Date.now() - lastActivityTime.current;
      if (inactiveTime > 30000) { // 30 seconds of inactivity
        trackEvent('inactivity_detected', {
          inactiveDuration: inactiveTime,
        });
      }
    }, 10000);

    // Periodic engagement summary
    const engagementTracker = setInterval(() => {
      const timeSpent = (Date.now() - startTime.current) / 1000 / 60;
      trackEvent('engagement_summary', {
        timeSpentMinutes: timeSpent,
        scrollDepth: Math.round(scrollDepth.current),
        interactionCount: interactionCount.current,
        mouseMovements: mouseMovements.current,
      });
    }, 30000); // Every 30 seconds

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    window.addEventListener('click', handleClick);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('click', handleClick);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      clearInterval(inactivityChecker);
      clearInterval(engagementTracker);
      
      // Send final engagement summary
      const finalTimeSpent = (Date.now() - startTime.current) / 1000 / 60;
      trackEvent('session_end', {
        totalTimeSpent: finalTimeSpent,
        finalScrollDepth: Math.round(scrollDepth.current),
        totalInteractions: interactionCount.current,
        totalMouseMovements: mouseMovements.current,
      });
    };
  }, [sessionId, contentId, trackEvent]);

  return {
    timeSpent: (Date.now() - startTime.current) / 1000 / 60,
    scrollDepth: scrollDepth.current,
    interactionCount: interactionCount.current,
  };
};
```

### Step 5.4: Create Core Components

Implement key components:

1. **Authentication Components**:
   - [`Login.jsx`](frontend/src/components/auth/Login.jsx:1)
   - [`Register.jsx`](frontend/src/components/auth/Register.jsx:1)
   - [`InitialAssessment.jsx`](frontend/src/components/auth/InitialAssessment.jsx:1)

2. **Dashboard Components**:
   - [`LearnerDashboard.jsx`](frontend/src/components/dashboard/LearnerDashboard.jsx:1)
   - [`CognitiveProfile.jsx`](frontend/src/components/dashboard/CognitiveProfile.jsx:1)
   - [`ProgressOverview.jsx`](frontend/src/components/dashboard/ProgressOverview.jsx:1)

3. **Learning Components**:
   - [`ContentViewer.jsx`](frontend/src/components/learning/ContentViewer.jsx:1)
   - [`AdaptiveContent.jsx`](frontend/src/components/learning/AdaptiveContent.jsx:1)
   - [`QuizComponent.jsx`](frontend/src/components/learning/QuizComponent.jsx:1)

4. **Analytics Components**:
   - [`AnalyticsDashboard.jsx`](frontend/src/components/analytics/AnalyticsDashboard.jsx:1)
   - [`CognitiveInsights.jsx`](frontend/src/components/analytics/CognitiveInsights.jsx:1)
   - [`EngagementTrends.jsx`](frontend/src/components/analytics/EngagementTrends.jsx:1)

## Phase 6: ML Model Training

### Step 6.1: Prepare Training Data

Create synthetic or use real data for training initial models:

- Learning style classification data
- Attention span patterns
- Engagement prediction data
- Recommendation training data

### Step 6.2: Train Models

Implement training scripts in [`backend/app/ml/training/`](backend/app/ml/training/:1):

```bash
python backend/app/ml/training/train_learning_style.py
python backend/app/ml/training/train_attention.py
python backend/app/ml/training/train_engagement.py
python backend/app/ml/training/train_recommender.py
```

### Step 6.3: Model Evaluation

Evaluate model performance:
- Accuracy, precision, recall for classifiers
- RMSE, MAE for regressors
- A/B testing framework setup

## Phase 7: Testing

### Step 7.1: Backend Testing

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

Test coverage should include:
- Unit tests for core logic
- Integration tests for API endpoints
- ML model validation tests
- Database operation tests

### Step 7.2: Frontend Testing

```bash
cd frontend
npm test
npm run test:e2e
```

Test coverage should include:
- Component unit tests
- Integration tests
- E2E user flows
- Accessibility tests

## Phase 8: Deployment

### Step 8.1: Production Configuration

Update environment variables for production:
- Secure SECRET_KEY
- Production database credentials
- CORS origins
- SSL/TLS certificates

### Step 8.2: Docker Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Step 8.3: Database Migrations

```bash
cd backend
alembic upgrade head
```

### Step 8.4: Monitoring Setup

- Set up application monitoring (e.g., Sentry)
- Configure logging aggregation
- Set up performance monitoring
- Configure alerts

## Development Workflow

### Running Locally

1. **Start infrastructure**:
```bash
docker-compose up db redis -d
```

2. **Run backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

3. **Run frontend**:
```bash
cd frontend
npm install
npm start
```

4. **Run Celery worker**:
```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

### Code Quality

```bash
# Backend
cd backend
black app/
flake8 app/
mypy app/

# Frontend
cd frontend
npm run lint
npm run format
```

## Next Steps

After completing the MVP implementation:

1. **User Testing**: Conduct user testing with real learners
2. **Model Refinement**: Improve ML models based on real data
3. **Feature Enhancement**: Add advanced features from the roadmap
4. **Performance Optimization**: Optimize database queries and API responses
5. **Scale Testing**: Test system under load
6. **Documentation**: Complete API documentation and user guides

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Check PostgreSQL is running
   - Verify DATABASE_URL in .env
   - Check firewall settings

2. **Redis Connection Issues**:
   - Verify Redis is running
   - Check REDIS_URL configuration
   - Test connection with redis-cli

3. **CORS Issues**:
   - Verify BACKEND_CORS_ORIGINS includes frontend URL
   - Check browser console for specific errors

4. **ML Model Loading Issues**:
   - Ensure models are trained and saved
   - Check MODEL_PATH configuration
   - Verify file permissions

## Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- scikit-learn Documentation: https://scikit-learn.org/
- Material-UI Documentation: https://mui.com/

## Support

For questions or issues during implementation, refer to:
- [`ARCHITECTURE.md`](ARCHITECTURE.md:1) for system design details
- API documentation at http://localhost:8000/docs
- Project README for quick start guide
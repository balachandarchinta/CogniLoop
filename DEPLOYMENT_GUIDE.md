# AI Cognitive Learning Architect - Complete Deployment Guide

## Overview

This guide provides complete step-by-step instructions to implement and deploy the AI Cognitive Learning Architect platform from scratch.

## Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed
- **Node.js 16+** and npm installed
- **PostgreSQL 14+** installed and running
- **Redis 7+** installed and running
- **Git** installed
- **Docker & Docker Compose** (optional but recommended)

## Phase 1: Environment Setup

### Step 1: Install Python Dependencies

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your actual values
# Important: Change SECRET_KEY to a secure random string
```

Generate a secure SECRET_KEY:
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Set Up Database

```bash
# Create PostgreSQL database
createdb cognitive_learning

# Or using psql
psql -U postgres
CREATE DATABASE cognitive_learning;
\q
```

Update DATABASE_URL in .env:
```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/cognitive_learning
```

### Step 4: Initialize Database with Alembic

```bash
cd backend

# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Step 5: Start Redis

```bash
# On Windows (if installed via MSI)
redis-server

# On Linux
sudo systemctl start redis

# On Mac
brew services start redis

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

## Phase 2: Backend Implementation

### Step 1: Complete All Model Files

Create all remaining model files as specified in the architecture:

1. `backend/app/models/learning_session.py`
2. `backend/app/models/content.py`
3. `backend/app/models/assessment.py`
4. `backend/app/models/recommendation.py`
5. `backend/app/models/learning_path.py`
6. `backend/app/models/daily_routine.py`

### Step 2: Implement Core Engines

Create the core cognitive engines:

1. **Cognitive Profiling Engine**
   - `backend/app/core/cognitive_profiling/profiler.py`
   - `backend/app/core/cognitive_profiling/learning_style_classifier.py`
   - `backend/app/core/cognitive_profiling/attention_analyzer.py`

2. **Adaptive Learning Engine**
   - `backend/app/core/adaptive_learning/adaptation_engine.py`
   - `backend/app/core/adaptive_learning/difficulty_adjuster.py`
   - `backend/app/core/adaptive_learning/pace_optimizer.py`

3. **Engagement Tracking**
   - `backend/app/core/engagement/engagement_tracker.py`
   - `backend/app/core/engagement/distraction_detector.py`

4. **Recommendation Engine**
   - `backend/app/core/recommendations/recommender.py`

### Step 3: Implement API Endpoints

Create FastAPI routers in `backend/app/api/v1/`:

1. `auth.py` - Authentication endpoints
2. `learners.py` - Learner management
3. `sessions.py` - Learning sessions
4. `content.py` - Content delivery
5. `adaptive.py` - Adaptive learning
6. `engagement.py` - Engagement tracking
7. `recommendations.py` - Recommendations
8. `analytics.py` - Analytics

### Step 4: Create Main Application

Create `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.v1 import auth, learners, sessions, content, adaptive, engagement, recommendations, analytics

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/")
async def root():
    return {
        "message": "Cognitive Learning Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Step 5: Run Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access API documentation at: http://localhost:8000/docs

## Phase 3: Frontend Implementation

### Step 1: Initialize React Application

```bash
cd frontend
npx create-react-app . --template typescript
```

Or if directory already exists:
```bash
cd frontend
npm init -y
npm install react react-dom react-router-dom @reduxjs/toolkit react-redux @mui/material @mui/icons-material @emotion/react @emotion/styled axios recharts socket.io-client date-fns
npm install --save-dev @testing-library/react @testing-library/jest-dom jest cypress
```

### Step 2: Set Up Environment Variables

Create `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_ENV=development
```

### Step 3: Implement Core Components

Create all frontend components as specified in the architecture:

1. **Authentication Components**
   - `src/components/auth/Login.jsx`
   - `src/components/auth/Register.jsx`
   - `src/components/auth/InitialAssessment.jsx`

2. **Dashboard Components**
   - `src/components/dashboard/LearnerDashboard.jsx`
   - `src/components/dashboard/CognitiveProfile.jsx`
   - `src/components/dashboard/ProgressOverview.jsx`

3. **Learning Components**
   - `src/components/learning/ContentViewer.jsx`
   - `src/components/learning/AdaptiveContent.jsx`
   - `src/components/learning/QuizComponent.jsx`

4. **Analytics Components**
   - `src/components/analytics/AnalyticsDashboard.jsx`
   - `src/components/analytics/CognitiveInsights.jsx`

### Step 4: Set Up Redux Store

Create `src/store/store.js` and implement slices for:
- Authentication state
- Profile state
- Learning state
- Analytics state

### Step 5: Implement Services

Create API service layer in `src/services/`:
- `api.js` - Axios configuration
- `auth.js` - Authentication services
- `tracking.js` - Engagement tracking
- `websocket.js` - Real-time updates

### Step 6: Run Frontend Development Server

```bash
cd frontend
npm start
```

Access application at: http://localhost:3000

## Phase 4: Machine Learning Models

### Step 1: Prepare Training Data

Create synthetic training data or use real data:

```python
# backend/app/ml/training/prepare_data.py
import pandas as pd
import numpy as np

def generate_synthetic_training_data():
    """Generate synthetic data for initial model training"""
    # Generate learning style data
    # Generate attention span data
    # Generate engagement data
    # Save to CSV files
    pass
```

### Step 2: Train Models

```bash
cd backend

# Train learning style classifier
python app/ml/training/train_learning_style.py

# Train attention predictor
python app/ml/training/train_attention.py

# Train engagement predictor
python app/ml/training/train_engagement.py

# Train recommender
python app/ml/training/train_recommender.py
```

### Step 3: Verify Models

Models should be saved in `backend/app/ml/models/`:
- `learning_style_model.pkl`
- `attention_model.h5`
- `engagement_model.pkl`
- `recommendation_model.pkl`

## Phase 5: Testing

### Backend Testing

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

### Frontend Testing

```bash
cd frontend
npm test
npm run test:e2e
```

## Phase 6: Docker Deployment

### Step 1: Create Docker Files

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Step 2: Create Docker Compose File

Already created in root directory as `docker-compose.yml`

### Step 3: Build and Run with Docker

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 4: Initialize Database in Docker

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create initial admin user (if needed)
docker-compose exec backend python scripts/create_admin.py
```

## Phase 7: Production Deployment

### Option 1: Cloud Deployment (AWS/GCP/Azure)

#### AWS Deployment

1. **Set up RDS for PostgreSQL**
   - Create RDS PostgreSQL instance
   - Configure security groups
   - Note connection string

2. **Set up ElastiCache for Redis**
   - Create Redis cluster
   - Configure security groups
   - Note connection string

3. **Deploy Backend to ECS/EKS**
   - Build Docker image
   - Push to ECR
   - Create ECS task definition
   - Deploy service

4. **Deploy Frontend to S3 + CloudFront**
   - Build production frontend
   - Upload to S3 bucket
   - Configure CloudFront distribution
   - Set up custom domain

5. **Configure Environment Variables**
   - Use AWS Secrets Manager
   - Update ECS task definition

#### GCP Deployment

1. **Set up Cloud SQL for PostgreSQL**
2. **Set up Memorystore for Redis**
3. **Deploy to Cloud Run or GKE**
4. **Deploy frontend to Cloud Storage + CDN**

#### Azure Deployment

1. **Set up Azure Database for PostgreSQL**
2. **Set up Azure Cache for Redis**
3. **Deploy to Azure Container Instances or AKS**
4. **Deploy frontend to Azure Static Web Apps**

### Option 2: VPS Deployment (DigitalOcean, Linode, etc.)

1. **Set up VPS**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/cognitive-learning-platform.git
   cd cognitive-learning-platform
   ```

3. **Configure Environment**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   # Edit .env files with production values
   ```

4. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

5. **Set up Nginx Reverse Proxy**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. **Set up SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

## Phase 8: Monitoring & Maintenance

### Set Up Monitoring

1. **Application Monitoring**
   ```bash
   # Install Sentry
   pip install sentry-sdk
   ```

2. **Server Monitoring**
   - Set up Prometheus + Grafana
   - Configure alerts

3. **Log Aggregation**
   - Set up ELK stack or use cloud logging

### Backup Strategy

1. **Database Backups**
   ```bash
   # Automated daily backups
   0 2 * * * pg_dump cognitive_learning > /backups/db_$(date +\%Y\%m\%d).sql
   ```

2. **Application Backups**
   - Regular code repository backups
   - ML model versioning

### Maintenance Tasks

1. **Regular Updates**
   ```bash
   # Update dependencies
   pip install --upgrade -r requirements.txt
   npm update
   ```

2. **Database Maintenance**
   ```bash
   # Vacuum and analyze
   psql cognitive_learning -c "VACUUM ANALYZE;"
   ```

3. **Model Retraining**
   - Schedule weekly/monthly model retraining
   - A/B test new models before deployment

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify DATABASE_URL in .env
   - Check firewall settings

2. **Redis Connection Failed**
   - Verify Redis is running: `redis-cli ping`
   - Check REDIS_URL configuration

3. **CORS Errors**
   - Verify BACKEND_CORS_ORIGINS includes frontend URL
   - Check browser console for specific errors

4. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path configuration
   - Verify virtual environment is activated

5. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process
   kill -9 <PID>
   ```

## Performance Optimization

### Backend Optimization

1. **Database Query Optimization**
   - Add indexes on frequently queried columns
   - Use query profiling
   - Implement connection pooling

2. **Caching Strategy**
   - Cache frequently accessed data in Redis
   - Implement cache invalidation logic

3. **Async Processing**
   - Use Celery for long-running tasks
   - Implement task queues

### Frontend Optimization

1. **Code Splitting**
   - Implement lazy loading
   - Split routes into chunks

2. **Asset Optimization**
   - Compress images
   - Minify CSS/JS
   - Use CDN for static assets

3. **Performance Monitoring**
   - Use Lighthouse for audits
   - Monitor Core Web Vitals

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Set up CORS properly
- [ ] Sanitize all user inputs
- [ ] Use parameterized queries
- [ ] Implement JWT token rotation
- [ ] Set up security headers
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Implement logging and monitoring
- [ ] Set up backup and recovery
- [ ] Use environment variables for secrets
- [ ] Implement GDPR compliance
- [ ] Set up intrusion detection

## Success Metrics

Monitor these KPIs after deployment:

- **System Health**: Uptime >99.5%
- **Performance**: API response time <200ms
- **User Engagement**: Session duration >20 minutes
- **Learning Effectiveness**: Retention rate >70%
- **User Satisfaction**: Rating >4/5 stars

## Support & Resources

- **Documentation**: See ARCHITECTURE.md and IMPLEMENTATION_GUIDE.md
- **API Docs**: http://your-domain.com/docs
- **Issue Tracking**: GitHub Issues
- **Community**: Discord/Slack channel

## Conclusion

This deployment guide provides a complete path from development to production. Follow each phase carefully, test thoroughly, and monitor continuously for a successful deployment.

For questions or issues, refer to the troubleshooting section or contact the development team.

**Good luck with your deployment! 🚀**
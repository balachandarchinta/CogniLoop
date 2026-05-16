from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Cognitive Learning Architect - Personalized Adaptive Learning Platform",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    Creates database tables if they don't exist.
    """
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"CORS origins: {settings.cors_origins}")
    
    # Initialize database
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on application shutdown.
    """
    print(f"Shutting down {settings.APP_NAME}")


@app.get("/")
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": "AI Cognitive Learning Architect API",
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }


@app.get("/api/v1")
async def api_info():
    """
    API v1 information endpoint.
    """
    return {
        "version": "1.0",
        "endpoints": {
            "auth": "/api/v1/auth",
            "learners": "/api/v1/learners",
            "sessions": "/api/v1/sessions",
            "content": "/api/v1/content",
            "adaptive": "/api/v1/adaptive",
            "engagement": "/api/v1/engagement",
            "recommendations": "/api/v1/recommendations",
            "analytics": "/api/v1/analytics"
        }
    }


# TODO: Include API routers when implemented
# from app.api.v1 import auth, learners, sessions, content, adaptive, engagement, recommendations, analytics
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(learners.router, prefix="/api/v1/learners", tags=["learners"])
# app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
# app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
# app.include_router(adaptive.router, prefix="/api/v1/adaptive", tags=["adaptive"])
# app.include_router(engagement.router, prefix="/api/v1/engagement", tags=["engagement"])
# app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
# app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

# Made with Bob

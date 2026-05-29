from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import init_db
from routers import auth, users, cameras, alerts, entry_logs, visitors, dashboard

# Initialize database
init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup and shutdown"""
    # Startup
    print("🚀 Starting GeoVision Campus Security API...")
    print(f"📊 Database: {settings.DATABASE_URL}")
    yield
    # Shutdown
    print("🛑 Shutting down GeoVision Campus Security API...")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Backend API for Campus Security Management System",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GeoVision Campus Security API",
        "version": settings.API_VERSION
    }


# Include routers with API prefix
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(cameras.router, prefix=settings.API_PREFIX)
app.include_router(alerts.router, prefix=settings.API_PREFIX)
app.include_router(entry_logs.router, prefix=settings.API_PREFIX)
app.include_router(visitors.router, prefix=settings.API_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_PREFIX)


# Root endpoint
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "🎥 GeoVision Campus Security API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG
    )

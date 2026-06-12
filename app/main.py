"""
FastAPI application factory.

This module creates and configures the FastAPI application instance.
Using an app factory pattern makes testing and deployment easier.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base
from app import routers

# Load settings
settings = get_settings()


def create_tables():
    """
    Create database tables.
    
    ⚠️ WARNING: Only use this in development!
    In production, use Alembic migrations instead.
    """
    import asyncio
    from sqlalchemy.ext.asyncio import AsyncEngine
    
    async def _create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    asyncio.run(_create_tables())


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    # Create app instance
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production-ready FastAPI backend with async database support",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    # Allow frontend applications to access this API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create tables (development only)
    if settings.DEBUG:
        create_tables()
    
    # Include routers
    app.include_router(routers.categories.router)
    app.include_router(routers.products.router)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    def root():
        """
        Root endpoint - API information.
        
        Returns basic information about the API and links to documentation.
        """
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    def health_check():
        """
        Health check endpoint for monitoring.
        
        Used by load balancers and monitoring systems to check
        if the application is running and healthy.
        """
        return {
            "status": "healthy",
            "version": settings.APP_VERSION
        }
    
    return app


# Create app instance for uvicorn
app = create_app()

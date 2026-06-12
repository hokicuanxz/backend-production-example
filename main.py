from fastapi import FastAPI
from database import engine, Base
from routers import categories, products
import models

# Create database tables
# ⚠️ NOTE: Ini hanya untuk development!
# Di production, kita akan pakai Alembic migrations
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Hanif Backend API",
    description="Backend API untuk manage products dan categories",
    version="1.0.0"
)

# Include routers
app.include_router(categories.router)
app.include_router(products.router)

# Root endpoint - health check
@app.get("/")
def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": "Welcome to Hanif Backend API",
        "docs": "/docs",
        "endpoints": {
            "categories": "/category",
            "products": "/product"
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint untuk monitoring.
    """
    return {"status": "healthy"}

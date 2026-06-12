"""
Pytest configuration and fixtures for API tests.

This module provides shared fixtures that can be used across all test files.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import engine, Base, async_session_maker
from app.models import ModelCategory, ModelProduct


@pytest.fixture(scope="function")
async def test_db():
    """
    Create a fresh test database for each test function.
    
    This ensures tests are isolated and don't affect each other.
    """
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Drop all tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(test_db):
    """
    Async test client for making HTTP requests.
    
    Usage:
        async def test_example(client):
            response = await client.get("/")
            assert response.status_code == 200
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def sample_category(test_db):
    """
    Create a sample category for testing.
    
    Usage:
        async def test_with_category(client, sample_category):
            # sample_category is available here
            pass
    """
    async with async_session_maker() as session:
        category = ModelCategory(name_category="Test Category")
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category


@pytest.fixture
async def sample_product(test_db, sample_category):
    """
    Create a sample product for testing.
    
    Usage:
        async def test_with_product(client, sample_product):
            # sample_product is available here
            pass
    """
    async with async_session_maker() as session:
        product = ModelProduct(
            name="Test Product",
            price=10000,
            is_ready=True,
            category_id=sample_category.id
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

"""
API endpoint tests.

Tests for all API endpoints to ensure they work correctly.
"""
import pytest
from httpx import AsyncClient


class TestRootEndpoints:
    """Tests for root and health endpoints."""
    
    async def test_root(self, client):
        """Test root endpoint returns API info."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data
    
    async def test_health(self, client):
        """Test health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestCategoryEndpoints:
    """Tests for category endpoints."""
    
    async def test_create_category(self, client):
        """Test creating a new category."""
        category_data = {
            "name_category": "Electronics"
        }
        response = await client.post("/category", json=category_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name_category"] == "Electronics"
        assert "id" in data
    
    async def test_create_duplicate_category(self, client, sample_category):
        """Test creating a duplicate category fails."""
        category_data = {
            "name_category": sample_category.name_category
        }
        response = await client.post("/category", json=category_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    async def test_get_category(self, client, sample_category):
        """Test getting category details."""
        response = await client.post(f"/category/{sample_category.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_category.id
        assert data["name_category"] == sample_category.name_category
    
    async def test_get_nonexistent_category(self, client):
        """Test getting a category that doesn't exist."""
        response = await client.post("/category/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    async def test_list_categories(self, client, sample_category):
        """Test listing all categories."""
        response = await client.get("/category")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestProductEndpoints:
    """Tests for product endpoints."""
    
    async def test_create_product(self, client, sample_category):
        """Test creating a new product."""
        product_data = {
            "name": "Laptop",
            "price": 15000000,
            "is_ready": True,
            "category_id": sample_category.id
        }
        response = await client.post("/add-product", json=product_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Laptop"
        assert data["price"] == 15000000
        assert "id" in data
    
    async def test_create_product_invalid_category(self, client):
        """Test creating a product with invalid category ID."""
        product_data = {
            "name": "Laptop",
            "price": 15000000,
            "is_ready": True,
            "category_id": 9999
        }
        response = await client.post("/add-product", json=product_data)
        assert response.status_code == 404
        assert "category" in response.json()["detail"].lower()
    
    async def test_get_products(self, client, sample_product):
        """Test getting all products."""
        response = await client.get("/product")
        assert response.status_code == 200
        data = response.json()
        assert "total_find" in data
        assert "data" in data
        assert isinstance(data["data"], list)
    
    async def test_search_products(self, client, sample_product):
        """Test searching products by keyword."""
        response = await client.get("/product?keyword=Laptop")
        assert response.status_code == 200
        data = response.json()
        assert data["total_find"] >= 1
        assert len(data["data"]) >= 1
    
    async def test_update_product(self, client, sample_product, sample_category):
        """Test updating a product."""
        update_data = {
            "name": "Updated Laptop",
            "price": 20000000,
            "is_ready": False,
            "category_id": sample_category.id
        }
        response = await client.put(
            f"/change-product/{sample_product.id}",
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Laptop"
        assert data["price"] == 20000000
        assert data["is_ready"] == False
    
    async def test_delete_product(self, client, sample_product):
        """Test deleting a product."""
        response = await client.delete(f"/product/{sample_product.id}")
        assert response.status_code == 204
        
        # Verify product is deleted
        get_response = await client.get("/product")
        data = get_response.json()
        assert data["total_find"] == 0

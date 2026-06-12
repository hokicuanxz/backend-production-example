"""
Pydantic schemas for request/response validation.

Schemas define the structure of data that the API accepts and returns.
They provide automatic validation, serialization, and OpenAPI documentation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


# =============================================================================
# Category Schemas
# =============================================================================

class CategoryCreate(BaseModel):
    """
    Schema for creating a new category.
    
    Used in POST /category requests.
    """
    name_category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the category (must be unique)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name_category": "Electronics"}
        }
    )


class CategoryResponse(BaseModel):
    """
    Schema for category response.
    
    Returned in GET /category/{id} and POST /category responses.
    """
    id: int
    name_category: str
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"id": 1, "name_category": "Electronics"}
        }
    )


class CategoryWithProducts(CategoryResponse):
    """
    Schema for category with its products.
    
    Extended version that includes related products.
    """
    # Products will be added dynamically in the endpoint
    list_product: Optional[List[dict]] = None


# =============================================================================
# Product Schemas
# =============================================================================

class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    
    Used in POST /add-product requests.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Product name"
    )
    price: int = Field(
        ...,
        gt=0,
        description="Product price (must be greater than 0)"
    )
    is_ready: bool = Field(
        default=True,
        description="Product availability status"
    )
    category_id: int = Field(
        ...,
        gt=0,
        description="ID of the category this product belongs to"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop",
                "price": 15000000,
                "is_ready": True,
                "category_id": 1
            }
        }
    )


class ProductUpdate(ProductCreate):
    """
    Schema for updating an existing product.
    
    Same as ProductCreate, used in PUT /change-product/{id}.
    """
    pass


class ProductResponse(BaseModel):
    """
    Schema for product response.
    
    Returned in product-related endpoints.
    """
    id: int
    name: str
    price: int
    is_ready: bool
    category_id: int
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Laptop",
                "price": 15000000,
                "is_ready": True,
                "category_id": 1
            }
        }
    )


class ProductListResponse(BaseModel):
    """
    Schema for paginated product list.
    
    Returned in GET /product endpoint.
    """
    total_find: int = Field(description="Total number of products found")
    limit: int = Field(description="Maximum number of results per page")
    skip: int = Field(description="Number of results skipped")
    data: List[ProductResponse] = Field(description="List of products")

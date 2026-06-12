"""
Product router with async endpoints.

Handles all product-related CRUD operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.database import get_db
from app.models import ModelCategory, ModelProduct
from app.schemas import (
    ProductCreate,
    ProductResponse,
    ProductListResponse
)

router = APIRouter(
    prefix="",
    tags=["products"]
)


@router.post(
    "/add-product",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description="Create a new product and assign it to a category."
)
async def add_product(
    new_product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new product.
    
    - **name**: Product name
    - **price**: Product price (must be > 0)
    - **is_ready**: Product availability status (default: True)
    - **category_id**: ID of the category this product belongs to
    """
    # Validation: Check if category exists
    result = await db.execute(
        select(ModelCategory).where(ModelCategory.id == new_product.category_id)
    )
    check_category = result.scalar_one_or_none()
    
    if not check_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot add product, category ID doesn't exist in database"
        )
    
    # Create new product
    product_db = ModelProduct(
        name=new_product.name,
        price=new_product.price,
        is_ready=new_product.is_ready,
        category_id=new_product.category_id
    )
    db.add(product_db)
    await db.commit()
    await db.refresh(product_db)
    
    return product_db


@router.get(
    "/product",
    response_model=ProductListResponse,
    summary="Get all products",
    description="Get paginated list of products with optional search."
)
async def get_all_product(
    keyword: Optional[str] = Query(
        None,
        description="Search term (searches in product name)"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Maximum number of results (1-100)"
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Number of results to skip"
    ),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all products with optional search and pagination.
    
    - **keyword**: Search term (optional, searches in product name)
    - **limit**: Maximum number of results (default: 10, max: 100)
    - **skip**: Number of results to skip for pagination (default: 0)
    """
    # Start with base query
    query = select(ModelProduct)
    
    # Apply search filter if keyword provided
    if keyword:
        query = query.where(
            ModelProduct.name.ilike(f"%{keyword}%")
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_product = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    result_product = result.scalars().all()
    
    return {
        "total_find": total_product,
        "limit": limit,
        "skip": skip,
        "data": result_product
    }


@router.put(
    "/change-product/{product_id}",
    response_model=ProductResponse,
    summary="Update a product",
    description="Update an existing product's information."
)
async def change_product(
    product_id: int,
    new_data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing product.
    
    - **product_id**: ID of the product to update
    - **name**: New product name
    - **price**: New product price
    - **is_ready**: New availability status
    - **category_id**: New category ID (must exist)
    """
    # Find existing product
    result = await db.execute(
        select(ModelProduct).where(ModelProduct.id == product_id)
    )
    old_product = result.scalar_one_or_none()
    
    if not old_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found, can't edit"
        )
    
    # Validation: Check if new category exists
    result = await db.execute(
        select(ModelCategory).where(ModelCategory.id == new_data.category_id)
    )
    check_category = result.scalar_one_or_none()
    
    if not check_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't edit, category ID is not registered"
        )
    
    # Update product fields
    old_product.name = new_data.name
    old_product.price = new_data.price
    old_product.is_ready = new_data.is_ready
    old_product.category_id = new_data.category_id
    
    # Save to database
    await db.commit()
    await db.refresh(old_product)
    
    return old_product


@router.delete(
    "/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
    description="Delete a product by ID."
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a product.
    
    - **product_id**: ID of the product to delete
    """
    # Find product
    result = await db.execute(
        select(ModelProduct).where(ModelProduct.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Delete product
    await db.delete(product)
    await db.commit()
    
    return None

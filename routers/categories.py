"""
Category router with async endpoints.

Handles all category-related CRUD operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models import ModelCategory, ModelProduct
from app.schemas import CategoryCreate, CategoryResponse, CategoryWithProducts

router = APIRouter(
    prefix="/category",
    tags=["categories"]
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    description="Create a new category with a unique name."
)
async def add_category(
    new_category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new category.
    
    - **name_category**: Name of the category (must be unique)
    
    Returns the created category with its ID.
    """
    # Check if category already exists
    result = await db.execute(
        select(ModelCategory).where(
            ModelCategory.name_category == new_category.name_category
        )
    )
    old_category = result.scalar_one_or_none()
    
    if old_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This category already exists!"
        )
    
    # Create new category
    category_db = ModelCategory(name_category=new_category.name_category)
    db.add(category_db)
    await db.commit()
    await db.refresh(category_db)
    
    return category_db


@router.post(
    "/{category_id}",
    response_model=CategoryWithProducts,
    summary="Get category details",
    description="Get detailed information about a category including its products."
)
async def get_detail_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get category details by ID.
    
    - **category_id**: The ID of the category to retrieve
    
    Returns category info with list of products.
    """
    # Search category in database
    result = await db.execute(
        select(ModelCategory).where(ModelCategory.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Get related products
    products_result = await db.execute(
        select(ModelProduct).where(ModelProduct.category_id == category_id)
    )
    products = products_result.scalars().all()
    
    return {
        "id": category.id,
        "name_category": category.name_category,
        "list_product": products
    }


@router.get(
    "",
    response_model=List[CategoryResponse],
    summary="List all categories",
    description="Get a list of all categories."
)
async def list_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all categories.
    
    Returns a list of all categories in the database.
    """
    result = await db.execute(select(ModelCategory))
    categories = result.scalars().all()
    return categories

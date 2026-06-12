from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import sys
import os

# Add parent directory to path biar bisa import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import SchemaProductCreate, SchemaProductShow
import models
from database import get_db

# Buat router object dengan prefix dan tags
router = APIRouter(
    prefix="",  # Kita pakai prefix kosong, endpoint akan di-root level
    tags=["products"]
)

# Endpoint: POST /add-product
@router.post("/add-product", response_model=SchemaProductShow)
def add_product(new_product: SchemaProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    
    - **name**: Product name
    - **price**: Product price
    - **is_ready**: Product availability status (default: True)
    - **category_id**: ID of the category this product belongs to
    """
    # Validation: Check if category exists
    check_category = db.query(models.ModelCategory).filter(
        models.ModelCategory.id == new_product.category_id
    ).first()
    
    if not check_category:
        raise HTTPException(
            status_code=404, 
            detail="Cannot add product, ID category doesn't exist in database"
        )
    
    # Create new product
    product_db = models.ModelProduct(
        name=new_product.name,
        price=new_product.price,
        is_ready=new_product.is_ready,
        category_id=new_product.category_id
    )
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    
    return product_db

# Endpoint: GET /product
@router.get("/product", response_model=dict)
def get_all_product(
    keyword: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get all products with optional search and pagination.
    
    - **keyword**: Search term (optional, searches in product name)
    - **limit**: Maximum number of results (default: 10)
    - **skip**: Number of results to skip for pagination (default: 0)
    """
    # Start with base query
    query = db.query(models.ModelProduct)
    
    # Apply search filter if keyword provided
    if keyword:
        query = query.filter(models.ModelProduct.name.ilike(f"%{keyword}%"))
    
    # Get total count before pagination
    total_product = query.count()
    
    # Apply pagination
    result_product = query.limit(limit).offset(skip).all()
    
    return {
        "total_find": total_product,
        "limit": limit,
        "skip": skip,
        "data": result_product
    }

# Endpoint: PUT /change-product/{product_id}
@router.put("/change-product/{product_id}", response_model=SchemaProductShow)
def change_product(
    product_id: int, 
    new_data: SchemaProductCreate, 
    db: Session = Depends(get_db)
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
    old_product = db.query(models.ModelProduct).filter(
        models.ModelProduct.id == product_id
    ).first()
    
    if not old_product:
        raise HTTPException(status_code=404, detail="Product not found, can't edit")
    
    # Validation: Check if new category exists
    check_category = db.query(models.ModelCategory).filter(
        models.ModelCategory.id == new_data.category_id
    ).first()
    
    if not check_category:
        raise HTTPException(
            status_code=404, 
            detail="Can't edit, ID category destiny is not registered"
        )
    
    # Update product fields
    old_product.name = new_data.name
    old_product.price = new_data.price
    old_product.is_ready = new_data.is_ready
    old_product.category_id = new_data.category_id
    
    # Save to database
    db.commit()
    db.refresh(old_product)
    
    return old_product

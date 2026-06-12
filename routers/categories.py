from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os

# Add parent directory to path biar bisa import models, schemas, database
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import SchemaCategoryShow, SchemaCategoryFor
import models
from database import get_db

# Buat router object dengan prefix dan tags
router = APIRouter(
    prefix="/category",    # Semua endpoint di sini otomatis dapat prefix /category
    tags=["categories"]    # Grouping di Swagger UI (/docs)
)

# Endpoint: POST /category
@router.post("", response_model=SchemaCategoryShow)
def add_category(new_category: SchemaCategoryFor, db: Session = Depends(get_db)):
    """
    Create a new category.
    
    - **name_category**: Name of the category (must be unique)
    """
    # Check if category already exists
    old_category = db.query(models.ModelCategory).filter(
        models.ModelCategory.name_category == new_category.name_category
    ).first()
    
    if old_category:
        raise HTTPException(status_code=400, detail="This category already exists!")
    
    # Create new category
    category_db = models.ModelCategory(name_category=new_category.name_category)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    
    return category_db

# Endpoint: POST /category/{category_id}
@router.post("/{category_id}", response_model=SchemaCategoryShow)
def get_detail_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get category details by ID.
    
    - **category_id**: The ID of the category to retrieve
    - Returns: Category info with list of products
    """
    # Search category in database
    category = db.query(models.ModelCategory).filter(
        models.ModelCategory.id == category_id
    ).first()
    
    # If not found, return 404
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Return category with its products
    return {
        "id": category.id,
        "name_category": category.name_category,
        "list_product": category.all_products
    }

"""
SQLAlchemy models for the application.

Models define the structure of database tables and relationships.
All models inherit from Base class defined in database.py.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ModelCategory(Base):
    """
    Category model.
    
    Represents a product category. Each category can have
    multiple products (one-to-many relationship).
    """
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, index=True)
    name_category = Column(String, unique=True, index=True, nullable=False)
    
    # Relationship: One category has many products
    all_products = relationship(
        "ModelProduct",
        back_populates="the_category",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name_category}')>"


class ModelProduct(Base):
    """
    Product model.
    
    Represents a product with name, price, and availability status.
    Each product belongs to one category (many-to-one relationship).
    """
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    is_ready = Column(Boolean, default=True, nullable=False)
    
    # Foreign key: Each product belongs to one category
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    
    # Relationship: Many products belong to one category
    the_category = relationship("ModelCategory", back_populates="all_products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    category_id = db.Column(db.String(20), db.ForeignKey('product_categories.category_id'), nullable=False)
    subcategory_id = db.Column(db.String(20), db.ForeignKey('product_categories.category_id'))
    size = db.Column(db.String(50))
    unit_type = db.Column(db.String(20))  # volume, weight, count, etc.
    barcode = db.Column(db.String(20))
    ingredients = db.Column(db.JSON)  # Array of ingredients
    allergens = db.Column(db.JSON)  # Array of allergens
    nutrition_info = db.Column(db.JSON)  # Nutrition facts
    image_urls = db.Column(db.JSON)  # Array of image URLs
    attributes = db.Column(db.JSON)  # Additional product attributes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prices = db.relationship('Price', backref='product', lazy=True)
    subcategory = db.relationship('ProductCategory', foreign_keys=[subcategory_id], post_update=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self, include_prices=False):
        result = {
            'product_id': self.product_id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category.category_name if self.category else None,
            'category_id': self.category_id,
            'subcategory': self.subcategory.category_name if self.subcategory else None,
            'subcategory_id': self.subcategory_id,
            'size': self.size,
            'unit_type': self.unit_type,
            'barcode': self.barcode,
            'ingredients': self.ingredients or [],
            'allergens': self.allergens or [],
            'nutrition_info': self.nutrition_info,
            'image_urls': self.image_urls or [],
            'attributes': self.attributes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_prices and self.prices:
            # Get current prices only
            current_prices = [p for p in self.prices if p.valid_to is None]
            result['prices'] = [price.to_dict() for price in current_prices]
            
        return result
    
    def get_current_prices(self, postal_code=None, radius_km=10):
        """Get current prices for this product, optionally filtered by location"""
        from src.models.price import Price
        
        query = Price.query.filter(
            Price.product_id == self.product_id,
            Price.valid_to.is_(None)  # Current prices only
        )
        
        if postal_code:
            # TODO: Implement location-based filtering
            # This would require geocoding the postal code and filtering stores by distance
            pass
            
        return query.all()
    
    def get_best_price(self, postal_code=None, radius_km=10):
        """Get the best (lowest) current price for this product"""
        prices = self.get_current_prices(postal_code, radius_km)
        if not prices:
            return None
        return min(prices, key=lambda p: p.current_price)


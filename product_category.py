from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    
    category_id = db.Column(db.String(20), primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    parent_category_id = db.Column(db.String(20), db.ForeignKey('product_categories.category_id'))
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Self-referential relationship for parent/child categories
    subcategories = db.relationship('ProductCategory', backref=db.backref('parent', remote_side='ProductCategory.category_id'), lazy=True)
    
    # Relationship to products (only for main category, not subcategory)
    products = db.relationship('Product', foreign_keys='Product.category_id', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<ProductCategory {self.category_name}>'
    
    def to_dict(self, include_subcategories=False):
        result = {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'parent_category_id': self.parent_category_id,
            'description': self.description,
            'sort_order': self.sort_order,
            'is_active': self.is_active,
            'product_count': len(self.products) if self.products else 0
        }
        
        if include_subcategories and self.subcategories:
            result['subcategories'] = [sub.to_dict() for sub in self.subcategories if sub.is_active]
            
        return result


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class GroceryChain(db.Model):
    __tablename__ = 'grocery_chains'
    
    chain_id = db.Column(db.String(20), primary_key=True)
    chain_name = db.Column(db.String(50), nullable=False)
    logo_url = db.Column(db.String(200))
    website_url = db.Column(db.String(200))
    corporate_info = db.Column(db.JSON)
    scraping_config = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    stores = db.relationship('Store', backref='chain', lazy=True)
    
    def __repr__(self):
        return f'<GroceryChain {self.chain_name}>'
    
    def to_dict(self):
        return {
            'chain_id': self.chain_id,
            'chain_name': self.chain_name,
            'logo_url': self.logo_url,
            'website_url': self.website_url,
            'corporate_info': self.corporate_info,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


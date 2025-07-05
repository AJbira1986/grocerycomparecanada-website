from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Store(db.Model):
    __tablename__ = 'stores'
    
    store_id = db.Column(db.String(50), primary_key=True)
    chain_id = db.Column(db.String(20), db.ForeignKey('grocery_chains.chain_id'), nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    address_street = db.Column(db.String(200), nullable=False)
    address_city = db.Column(db.String(50), nullable=False)
    address_province = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(7), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    phone = db.Column(db.String(20))
    website_url = db.Column(db.String(200))
    hours = db.Column(db.JSON)
    services = db.Column(db.JSON)  # Array of services
    features = db.Column(db.JSON)  # Array of features
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prices = db.relationship('Price', backref='store', lazy=True)
    
    def __repr__(self):
        return f'<Store {self.store_name}>'
    
    def to_dict(self):
        return {
            'store_id': self.store_id,
            'chain_id': self.chain_id,
            'chain_name': self.chain.chain_name if self.chain else None,
            'store_name': self.store_name,
            'address': {
                'street': self.address_street,
                'city': self.address_city,
                'province': self.address_province,
                'postal_code': self.postal_code
            },
            'coordinates': {
                'latitude': float(self.latitude) if self.latitude else None,
                'longitude': float(self.longitude) if self.longitude else None
            },
            'contact': {
                'phone': self.phone,
                'website': self.website_url
            },
            'hours': self.hours,
            'services': self.services or [],
            'features': self.features or [],
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def calculate_distance(self, lat, lng):
        """Calculate distance from store to given coordinates using Haversine formula"""
        import math
        
        # Convert to radians
        lat1, lng1 = math.radians(float(self.latitude)), math.radians(float(self.longitude))
        lat2, lng2 = math.radians(lat), math.radians(lng)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return c * r


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from src.models.user import db

class Price(db.Model):
    __tablename__ = 'prices'
    
    price_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(50), db.ForeignKey('products.product_id'), nullable=False)
    store_id = db.Column(db.String(50), db.ForeignKey('stores.store_id'), nullable=False)
    current_price = db.Column(db.Numeric(8, 2), nullable=False)
    regular_price = db.Column(db.Numeric(8, 2))
    on_sale = db.Column(db.Boolean, default=False)
    sale_start_date = db.Column(db.Date)
    sale_end_date = db.Column(db.Date)
    price_per_unit = db.Column(db.Numeric(8, 2))
    stock_status = db.Column(db.String(20), default='unknown')  # in_stock, out_of_stock, limited, unknown
    data_source = db.Column(db.String(50), nullable=False)  # flyer, website, manual, etc.
    scraped_at = db.Column(db.DateTime, nullable=False)
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)
    valid_to = db.Column(db.DateTime)  # NULL for current prices
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Price {self.product_id} @ {self.store_id}: ${self.current_price}>'
    
    def to_dict(self, include_store_details=False):
        result = {
            'price_id': self.price_id,
            'product_id': self.product_id,
            'store_id': self.store_id,
            'current_price': float(self.current_price),
            'regular_price': float(self.regular_price) if self.regular_price else None,
            'on_sale': self.on_sale,
            'sale_start_date': self.sale_start_date.isoformat() if self.sale_start_date else None,
            'sale_end_date': self.sale_end_date.isoformat() if self.sale_end_date else None,
            'price_per_unit': float(self.price_per_unit) if self.price_per_unit else None,
            'stock_status': self.stock_status,
            'data_source': self.data_source,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_to': self.valid_to.isoformat() if self.valid_to else None,
            'last_updated': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_store_details and self.store:
            result['store_name'] = self.store.store_name
            result['chain_name'] = self.store.chain.chain_name if self.store.chain else None
            result['address'] = f"{self.store.address_street}, {self.store.address_city}, {self.store.address_province}"
            
        return result
    
    @property
    def savings(self):
        """Calculate savings if on sale"""
        if self.on_sale and self.regular_price:
            return float(self.regular_price - self.current_price)
        return 0.0
    
    @property
    def is_current(self):
        """Check if this price is currently valid"""
        return self.valid_to is None
    
    @property
    def is_sale_active(self):
        """Check if sale is currently active"""
        if not self.on_sale:
            return False
        
        today = date.today()
        
        if self.sale_start_date and today < self.sale_start_date:
            return False
            
        if self.sale_end_date and today > self.sale_end_date:
            return False
            
        return True
    
    @classmethod
    def get_current_prices_for_product(cls, product_id, store_ids=None):
        """Get all current prices for a product, optionally filtered by stores"""
        query = cls.query.filter(
            cls.product_id == product_id,
            cls.valid_to.is_(None)
        )
        
        if store_ids:
            query = query.filter(cls.store_id.in_(store_ids))
            
        return query.all()
    
    @classmethod
    def get_price_comparison(cls, product_id, store_ids=None):
        """Get price comparison data for a product across stores"""
        prices = cls.get_current_prices_for_product(product_id, store_ids)
        
        if not prices:
            return None
            
        price_list = [float(p.current_price) for p in prices]
        
        return {
            'prices': [p.to_dict(include_store_details=True) for p in prices],
            'best_price': {
                'price': min(price_list),
                'store_id': min(prices, key=lambda p: p.current_price).store_id
            },
            'average_price': sum(price_list) / len(price_list),
            'price_range': {
                'min': min(price_list),
                'max': max(price_list)
            },
            'total_stores': len(prices)
        }


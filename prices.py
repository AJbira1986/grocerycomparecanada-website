from flask import Blueprint, jsonify, request
from src.models.price import Price
from src.models.product import Product
from src.models.store import Store
from src.models.user import db
from datetime import datetime, timedelta
from sqlalchemy import and_, desc

prices_bp = Blueprint('prices', __name__)

@prices_bp.route('/prices/compare', methods=['GET'])
def compare_prices():
    """Compare prices for a specific product across multiple stores"""
    product_id = request.args.get('product_id')
    postal_code = request.args.get('postal_code')
    radius_km = request.args.get('radius_km', default=10, type=float)
    
    if not product_id:
        return jsonify({'error': 'product_id parameter is required'}), 400
    
    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Get stores within radius if postal code provided
    store_ids = None
    if postal_code:
        # TODO: Implement geocoding for postal code
        # For now, get all active stores
        stores = Store.query.filter(Store.is_active == True).all()
        store_ids = [store.store_id for store in stores]
    
    # Get price comparison
    comparison = Price.get_price_comparison(product_id, store_ids)
    
    if not comparison:
        return jsonify({
            'product': product.to_dict(),
            'price_comparison': [],
            'message': 'No prices found for this product'
        })
    
    # Calculate savings vs highest price
    if comparison['prices']:
        highest_price = comparison['price_range']['max']
        best_price_data = comparison['best_price']
        best_price_data['savings_vs_highest'] = round(highest_price - best_price_data['price'], 2)
    
    return jsonify({
        'product': product.to_dict(),
        'price_comparison': comparison['prices'],
        'best_price': comparison['best_price'],
        'average_price': round(comparison['average_price'], 2),
        'price_range': comparison['price_range']
    })

@prices_bp.route('/prices/history/<product_id>', methods=['GET'])
def get_price_history(product_id):
    """Get price history for a product"""
    days = request.args.get('days', default=30, type=int)
    store_ids = request.args.getlist('store_ids')
    
    if days > 365:
        days = 365
    
    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Build query
    query = Price.query.filter(
        Price.product_id == product_id,
        Price.created_at >= start_date
    ).order_by(desc(Price.created_at))
    
    if store_ids:
        query = query.filter(Price.store_id.in_(store_ids))
    
    prices = query.all()
    
    # Group by store and date for easier visualization
    history_by_store = {}
    for price in prices:
        store_id = price.store_id
        if store_id not in history_by_store:
            history_by_store[store_id] = {
                'store_id': store_id,
                'store_name': price.store.store_name,
                'chain_name': price.store.chain.chain_name if price.store.chain else None,
                'price_points': []
            }
        
        history_by_store[store_id]['price_points'].append({
            'date': price.created_at.isoformat(),
            'price': float(price.current_price),
            'on_sale': price.on_sale,
            'regular_price': float(price.regular_price) if price.regular_price else None
        })
    
    return jsonify({
        'product': product.to_dict(),
        'history_days': days,
        'stores': list(history_by_store.values()),
        'total_price_points': len(prices)
    })

@prices_bp.route('/prices', methods=['POST'])
def create_price():
    """Create a new price entry (admin/scraper only)"""
    data = request.json
    
    # Validate required fields
    required_fields = ['product_id', 'store_id', 'current_price', 'data_source']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if product and store exist
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    store = Store.query.get(data['store_id'])
    if not store:
        return jsonify({'error': 'Store not found'}), 404
    
    # Invalidate previous current price for this product-store combination
    current_price = Price.query.filter(
        Price.product_id == data['product_id'],
        Price.store_id == data['store_id'],
        Price.valid_to.is_(None)
    ).first()
    
    if current_price:
        current_price.valid_to = datetime.utcnow()
    
    # Create new price entry
    price = Price(
        product_id=data['product_id'],
        store_id=data['store_id'],
        current_price=data['current_price'],
        regular_price=data.get('regular_price'),
        on_sale=data.get('on_sale', False),
        sale_start_date=datetime.fromisoformat(data['sale_start_date']).date() if data.get('sale_start_date') else None,
        sale_end_date=datetime.fromisoformat(data['sale_end_date']).date() if data.get('sale_end_date') else None,
        price_per_unit=data.get('price_per_unit'),
        stock_status=data.get('stock_status', 'unknown'),
        data_source=data['data_source'],
        scraped_at=datetime.fromisoformat(data['scraped_at']) if data.get('scraped_at') else datetime.utcnow()
    )
    
    db.session.add(price)
    db.session.commit()
    
    return jsonify(price.to_dict()), 201

@prices_bp.route('/prices/bulk', methods=['POST'])
def bulk_create_prices():
    """Bulk create price entries (admin/scraper only)"""
    data = request.json
    
    if not isinstance(data, list):
        return jsonify({'error': 'Expected array of prices'}), 400
    
    created_prices = []
    errors = []
    
    for i, price_data in enumerate(data):
        try:
            # Validate required fields
            required_fields = ['product_id', 'store_id', 'current_price', 'data_source']
            for field in required_fields:
                if field not in price_data:
                    errors.append(f'Price {i}: Missing required field: {field}')
                    continue
            
            # Check if product and store exist
            if not Product.query.get(price_data['product_id']):
                errors.append(f'Price {i}: Product not found')
                continue
            
            if not Store.query.get(price_data['store_id']):
                errors.append(f'Price {i}: Store not found')
                continue
            
            # Invalidate previous current price
            current_price = Price.query.filter(
                Price.product_id == price_data['product_id'],
                Price.store_id == price_data['store_id'],
                Price.valid_to.is_(None)
            ).first()
            
            if current_price:
                current_price.valid_to = datetime.utcnow()
            
            # Create new price entry
            price = Price(
                product_id=price_data['product_id'],
                store_id=price_data['store_id'],
                current_price=price_data['current_price'],
                regular_price=price_data.get('regular_price'),
                on_sale=price_data.get('on_sale', False),
                sale_start_date=datetime.fromisoformat(price_data['sale_start_date']).date() if price_data.get('sale_start_date') else None,
                sale_end_date=datetime.fromisoformat(price_data['sale_end_date']).date() if price_data.get('sale_end_date') else None,
                price_per_unit=price_data.get('price_per_unit'),
                stock_status=price_data.get('stock_status', 'unknown'),
                data_source=price_data['data_source'],
                scraped_at=datetime.fromisoformat(price_data['scraped_at']) if price_data.get('scraped_at') else datetime.utcnow()
            )
            
            db.session.add(price)
            created_prices.append(price.to_dict())
            
        except Exception as e:
            errors.append(f'Price {i}: {str(e)}')
    
    if created_prices:
        db.session.commit()
    
    return jsonify({
        'created': len(created_prices),
        'errors': errors
    }), 201 if created_prices else 400

@prices_bp.route('/prices/current/<product_id>', methods=['GET'])
def get_current_prices(product_id):
    """Get all current prices for a product"""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    prices = Price.get_current_prices_for_product(product_id)
    
    return jsonify({
        'product': product.to_dict(),
        'current_prices': [price.to_dict(include_store_details=True) for price in prices],
        'total_stores': len(prices)
    })

@prices_bp.route('/prices/deals', methods=['GET'])
def get_deals():
    """Get current deals and sales"""
    limit = request.args.get('limit', default=50, type=int)
    category = request.args.get('category')
    
    if limit > 100:
        limit = 100
    
    # Get current prices that are on sale
    query = Price.query.filter(
        Price.valid_to.is_(None),
        Price.on_sale == True
    ).order_by(desc(Price.created_at))
    
    if category:
        query = query.join(Product).filter(Product.category_id == category)
    
    deals = query.limit(limit).all()
    
    deals_data = []
    for price in deals:
        deal_data = price.to_dict(include_store_details=True)
        deal_data['product'] = price.product.to_dict()
        deal_data['savings'] = price.savings
        deals_data.append(deal_data)
    
    return jsonify({
        'deals': deals_data,
        'total_deals': len(deals_data)
    })

@prices_bp.route('/prices/<int:price_id>', methods=['DELETE'])
def delete_price(price_id):
    """Delete a price entry (admin only)"""
    price = Price.query.get_or_404(price_id)
    db.session.delete(price)
    db.session.commit()
    return '', 204


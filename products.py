from flask import Blueprint, request, jsonify
from ..services.product_matcher_service import ProductMatcherService

products_bp = Blueprint('products', __name__)
matcher_service = ProductMatcherService()


@products_bp.route('/search', methods=['GET'])
def search_products():
    """Search for products and return price comparisons"""
    
    query = request.args.get('q', '').strip()
    postal_code = request.args.get('postal_code', '').strip()
    limit = min(int(request.args.get('limit', 20)), 50)  # Max 50 results
    
    if not query or len(query) < 2:
        return jsonify({
            'error': 'Query must be at least 2 characters long'
        }), 400
    
    try:
        results = matcher_service.search_products(query, postal_code, limit)
        
        return jsonify({
            'query': query,
            'postal_code': postal_code,
            'results_count': len(results),
            'products': results
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@products_bp.route('/<int:product_id>/compare', methods=['GET'])
def compare_product_prices(product_id):
    """Get detailed price comparison for a specific product"""
    
    try:
        comparison = matcher_service.get_price_comparison(product_id)
        
        if not comparison:
            return jsonify({
                'error': 'Product not found or no price data available'
            }), 404
        
        return jsonify(comparison)
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    
    try:
        # Return mock categories for demo
        categories = [
            'dairy', 'meat', 'produce', 'bakery', 'beverages', 
            'frozen', 'pantry', 'snacks', 'household'
        ]
        
        return jsonify({
            'categories': sorted(categories)
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@products_bp.route('/brands', methods=['GET'])
def get_brands():
    """Get all product brands"""
    
    try:
        # Return mock brands for demo
        brands = [
            'Organic Valley', 'Lactantia', 'President\'s Choice', 
            'No Name', 'Wonder', 'Coca-Cola', 'Pepsi'
        ]
        
        return jsonify({
            'brands': sorted(brands)
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


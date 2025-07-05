from flask import Blueprint, jsonify, request
from src.models.store import Store
from src.models.grocery_chain import GroceryChain
from src.models.user import db
import math

stores_bp = Blueprint('stores', __name__)

@stores_bp.route('/stores', methods=['GET'])
def get_stores():
    """Get all stores or filter by location"""
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    radius_km = request.args.get('radius_km', default=10, type=float)
    chains = request.args.getlist('chains')
    
    query = Store.query.filter(Store.is_active == True)
    
    if chains:
        query = query.filter(Store.chain_id.in_(chains))
    
    stores = query.all()
    
    # Filter by distance if coordinates provided
    if latitude and longitude:
        stores_with_distance = []
        for store in stores:
            distance = store.calculate_distance(latitude, longitude)
            if distance <= radius_km:
                store_dict = store.to_dict()
                store_dict['distance_km'] = round(distance, 2)
                stores_with_distance.append(store_dict)
        
        # Sort by distance
        stores_with_distance.sort(key=lambda x: x['distance_km'])
        return jsonify(stores_with_distance)
    
    return jsonify([store.to_dict() for store in stores])

@stores_bp.route('/stores/<store_id>', methods=['GET'])
def get_store(store_id):
    """Get detailed information for a specific store"""
    store = Store.query.get_or_404(store_id)
    return jsonify(store.to_dict())

@stores_bp.route('/stores/chains', methods=['GET'])
def get_chains():
    """Get all grocery chains"""
    chains = GroceryChain.query.all()
    return jsonify([chain.to_dict() for chain in chains])

@stores_bp.route('/stores/chains/<chain_id>', methods=['GET'])
def get_chain(chain_id):
    """Get specific grocery chain with its stores"""
    chain = GroceryChain.query.get_or_404(chain_id)
    chain_dict = chain.to_dict()
    chain_dict['stores'] = [store.to_dict() for store in chain.stores if store.is_active]
    return jsonify(chain_dict)

@stores_bp.route('/stores', methods=['POST'])
def create_store():
    """Create a new store (admin only)"""
    data = request.json
    
    # Validate required fields
    required_fields = ['store_id', 'chain_id', 'store_name', 'address_street', 
                      'address_city', 'address_province', 'postal_code', 
                      'latitude', 'longitude']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if store already exists
    if Store.query.get(data['store_id']):
        return jsonify({'error': 'Store already exists'}), 409
    
    # Check if chain exists
    if not GroceryChain.query.get(data['chain_id']):
        return jsonify({'error': 'Grocery chain not found'}), 404
    
    store = Store(
        store_id=data['store_id'],
        chain_id=data['chain_id'],
        store_name=data['store_name'],
        address_street=data['address_street'],
        address_city=data['address_city'],
        address_province=data['address_province'],
        postal_code=data['postal_code'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        phone=data.get('phone'),
        website_url=data.get('website_url'),
        hours=data.get('hours'),
        services=data.get('services', []),
        features=data.get('features', [])
    )
    
    db.session.add(store)
    db.session.commit()
    
    return jsonify(store.to_dict()), 201

@stores_bp.route('/stores/<store_id>', methods=['PUT'])
def update_store(store_id):
    """Update store information (admin only)"""
    store = Store.query.get_or_404(store_id)
    data = request.json
    
    # Update allowed fields
    updateable_fields = ['store_name', 'address_street', 'address_city', 
                        'address_province', 'postal_code', 'latitude', 
                        'longitude', 'phone', 'website_url', 'hours', 
                        'services', 'features', 'is_active']
    
    for field in updateable_fields:
        if field in data:
            setattr(store, field, data[field])
    
    db.session.commit()
    return jsonify(store.to_dict())

@stores_bp.route('/stores/<store_id>', methods=['DELETE'])
def delete_store(store_id):
    """Soft delete a store (admin only)"""
    store = Store.query.get_or_404(store_id)
    store.is_active = False
    db.session.commit()
    return '', 204


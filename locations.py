from flask import Blueprint, jsonify, request
from src.models.store import Store
from src.models.user import db
import re

locations_bp = Blueprint('locations', __name__)

def validate_postal_code(postal_code):
    """Validate Canadian postal code format"""
    if not postal_code:
        return False
    
    # Remove spaces and convert to uppercase
    postal_code = postal_code.replace(' ', '').upper()
    
    # Canadian postal code pattern: A1A1A1
    pattern = r'^[A-Z]\d[A-Z]\d[A-Z]\d$'
    return bool(re.match(pattern, postal_code))

def format_postal_code(postal_code):
    """Format postal code to standard A1A 1A1 format"""
    if not postal_code:
        return None
    
    postal_code = postal_code.replace(' ', '').upper()
    if len(postal_code) == 6:
        return f"{postal_code[:3]} {postal_code[3:]}"
    return postal_code

def geocode_postal_code(postal_code):
    """
    Geocode postal code to coordinates.
    This is a simplified implementation - in production, you would use
    a geocoding service like Google Maps API or Geocodio.
    """
    # Sample coordinates for major Ontario cities
    # In production, this would call an external geocoding API
    sample_coordinates = {
        'M5V': {'latitude': 43.6426, 'longitude': -79.3871, 'city': 'Toronto'},
        'K1A': {'latitude': 45.4215, 'longitude': -75.6972, 'city': 'Ottawa'},
        'L5B': {'latitude': 43.5890, 'longitude': -79.6441, 'city': 'Mississauga'},
        'N2L': {'latitude': 43.4643, 'longitude': -80.5204, 'city': 'Waterloo'},
        'L8S': {'latitude': 43.2557, 'longitude': -79.8711, 'city': 'Hamilton'},
        'N6A': {'latitude': 42.9849, 'longitude': -81.2453, 'city': 'London'},
        'P3A': {'latitude': 46.4917, 'longitude': -80.9930, 'city': 'Sudbury'},
        'K7L': {'latitude': 44.2312, 'longitude': -76.4860, 'city': 'Kingston'}
    }
    
    # Extract first 3 characters for lookup
    prefix = postal_code.replace(' ', '')[:3]
    
    if prefix in sample_coordinates:
        return sample_coordinates[prefix]
    
    # Default to Toronto if not found
    return {'latitude': 43.6532, 'longitude': -79.3832, 'city': 'Toronto'}

@locations_bp.route('/locations/postal-code/<postal_code>', methods=['GET'])
def validate_and_geocode_postal_code(postal_code):
    """Validate postal code and return geographic information with nearby stores"""
    
    # Validate postal code format
    if not validate_postal_code(postal_code):
        return jsonify({
            'error': 'Invalid postal code format',
            'message': 'Please provide a valid Canadian postal code (e.g., M5V 3A8)'
        }), 400
    
    # Format postal code
    formatted_postal_code = format_postal_code(postal_code)
    
    # Geocode postal code
    location_data = geocode_postal_code(formatted_postal_code)
    
    # Find nearby stores (within 50km for initial search)
    latitude = location_data['latitude']
    longitude = location_data['longitude']
    radius_km = request.args.get('radius_km', default=10, type=float)
    
    if radius_km > 50:
        radius_km = 50
    
    # Get all active stores and calculate distances
    stores = Store.query.filter(Store.is_active == True).all()
    nearby_stores = []
    
    for store in stores:
        distance = store.calculate_distance(latitude, longitude)
        if distance <= radius_km:
            store_dict = store.to_dict()
            store_dict['distance_km'] = round(distance, 2)
            nearby_stores.append(store_dict)
    
    # Sort by distance
    nearby_stores.sort(key=lambda x: x['distance_km'])
    
    return jsonify({
        'postal_code': formatted_postal_code,
        'city': location_data['city'],
        'province': 'ON',
        'latitude': location_data['latitude'],
        'longitude': location_data['longitude'],
        'nearby_stores': nearby_stores[:20]  # Limit to 20 closest stores
    })

@locations_bp.route('/locations/stores', methods=['GET'])
def get_stores_by_location():
    """Get stores within a specified radius of coordinates"""
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    radius_km = request.args.get('radius_km', default=10, type=float)
    chains = request.args.getlist('chains')
    
    if not latitude or not longitude:
        return jsonify({
            'error': 'Missing coordinates',
            'message': 'Both latitude and longitude parameters are required'
        }), 400
    
    if radius_km > 50:
        radius_km = 50
    
    # Get stores filtered by chains if specified
    query = Store.query.filter(Store.is_active == True)
    if chains:
        query = query.filter(Store.chain_id.in_(chains))
    
    stores = query.all()
    
    # Calculate distances and filter
    nearby_stores = []
    for store in stores:
        distance = store.calculate_distance(latitude, longitude)
        if distance <= radius_km:
            store_dict = store.to_dict()
            store_dict['distance_km'] = round(distance, 2)
            nearby_stores.append(store_dict)
    
    # Sort by distance
    nearby_stores.sort(key=lambda x: x['distance_km'])
    
    return jsonify({
        'coordinates': {
            'latitude': latitude,
            'longitude': longitude
        },
        'radius_km': radius_km,
        'stores': nearby_stores,
        'total_stores': len(nearby_stores)
    })

@locations_bp.route('/locations/validate-postal-code', methods=['POST'])
def validate_postal_code_endpoint():
    """Validate postal code format only"""
    data = request.json
    postal_code = data.get('postal_code')
    
    if not postal_code:
        return jsonify({'error': 'postal_code is required'}), 400
    
    is_valid = validate_postal_code(postal_code)
    formatted = format_postal_code(postal_code) if is_valid else None
    
    return jsonify({
        'postal_code': postal_code,
        'is_valid': is_valid,
        'formatted': formatted,
        'message': 'Valid Canadian postal code' if is_valid else 'Invalid postal code format'
    })

@locations_bp.route('/locations/geocode', methods=['POST'])
def geocode_endpoint():
    """Geocode a postal code to coordinates"""
    data = request.json
    postal_code = data.get('postal_code')
    
    if not postal_code:
        return jsonify({'error': 'postal_code is required'}), 400
    
    if not validate_postal_code(postal_code):
        return jsonify({'error': 'Invalid postal code format'}), 400
    
    formatted_postal_code = format_postal_code(postal_code)
    location_data = geocode_postal_code(formatted_postal_code)
    
    return jsonify({
        'postal_code': formatted_postal_code,
        'coordinates': {
            'latitude': location_data['latitude'],
            'longitude': location_data['longitude']
        },
        'city': location_data['city'],
        'province': 'ON'
    })


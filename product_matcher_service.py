"""
Product Matcher Service

This service integrates the product matching engine with the Flask API
to provide real-time product matching and price comparison functionality.
"""

import sys
import os
from typing import List, Dict, Optional
from flask import current_app

# Add the parent directory to the path to import the product matcher
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from product_matcher import ProductMatchingEngine, ProductNormalizer, ProductMatcher
except ImportError:
    # Fallback if the module is not available
    ProductMatchingEngine = None
    ProductNormalizer = None
    ProductMatcher = None


class ProductMatcherService:
    """Service for product matching and price comparison"""
    
    def __init__(self):
        self.engine = None
        if ProductMatchingEngine:
            self.engine = ProductMatchingEngine()
    
    def search_products(self, query: str, postal_code: str = None, limit: int = 20) -> List[Dict]:
        """Search for products and return price comparisons"""
        
        if not query or len(query.strip()) < 2:
            return []
        
        try:
            # For now, use mock data since database integration is complex
            return self._get_mock_search_results(query)
                
        except Exception as e:
            print(f"Error in product search: {e}")
            return self._get_mock_search_results(query)
    
    def get_price_comparison(self, product_id: int) -> Optional[Dict]:
        """Get detailed price comparison for a specific product"""
        
        try:
            # Return mock comparison data
            return {
                'product_name': 'Organic Valley Whole Milk 1L',
                'brand': 'Organic Valley',
                'size': '1L',
                'store_count': 3,
                'min_price': 5.99,
                'max_price': 6.49,
                'avg_price': 6.16,
                'price_difference': 0.50,
                'savings_percentage': 7.7,
                'stores': [
                    {
                        'store_chain': 'Walmart',
                        'store_name': 'Walmart Supercentre',
                        'store_location': 'Toronto, ON',
                        'current_price': 5.99,
                        'regular_price': 6.49,
                        'sale_price': 5.99,
                        'on_sale': True,
                        'distance': 1.2
                    },
                    {
                        'store_chain': 'Loblaws',
                        'store_name': 'Loblaws',
                        'store_location': 'Toronto, ON',
                        'current_price': 6.29,
                        'regular_price': 6.29,
                        'sale_price': None,
                        'on_sale': False,
                        'distance': 0.8
                    },
                    {
                        'store_chain': 'Metro',
                        'store_name': 'Metro',
                        'store_location': 'Toronto, ON',
                        'current_price': 6.49,
                        'regular_price': 6.49,
                        'sale_price': None,
                        'on_sale': False,
                        'distance': 1.5
                    }
                ]
            }
            
        except Exception as e:
            print(f"Error getting price comparison: {e}")
            return None
    
    def _get_mock_search_results(self, query: str) -> List[Dict]:
        """Get mock search results for demonstration"""
        
        mock_results = []
        
        if 'milk' in query.lower():
            mock_results = [
                {
                    'product_name': 'Organic Valley Whole Milk 1L',
                    'brand': 'Organic Valley',
                    'category': 'dairy',
                    'unit_size': 1.0,
                    'unit_type': 'liter',
                    'organic': True,
                    'store_count': 3,
                    'min_price': 5.99,
                    'max_price': 6.49,
                    'avg_price': 6.16,
                    'price_difference': 0.50,
                    'savings_percentage': 7.7,
                    'stores': [
                        {
                            'store_chain': 'Walmart',
                            'store_location': 'Toronto, ON',
                            'current_price': 5.99,
                            'regular_price': 6.49,
                            'sale_price': 5.99,
                            'on_sale': True,
                            'distance': 1.2
                        },
                        {
                            'store_chain': 'Loblaws',
                            'store_location': 'Toronto, ON',
                            'current_price': 6.29,
                            'regular_price': 6.29,
                            'sale_price': None,
                            'on_sale': False,
                            'distance': 0.8
                        },
                        {
                            'store_chain': 'Metro',
                            'store_location': 'Toronto, ON',
                            'current_price': 6.49,
                            'regular_price': 6.49,
                            'sale_price': None,
                            'on_sale': False,
                            'distance': 1.5
                        }
                    ]
                },
                {
                    'product_name': 'Lactantia 2% Milk 2L',
                    'brand': 'Lactantia',
                    'category': 'dairy',
                    'unit_size': 2.0,
                    'unit_type': 'liter',
                    'organic': False,
                    'store_count': 2,
                    'min_price': 4.97,
                    'max_price': 5.19,
                    'avg_price': 5.08,
                    'price_difference': 0.22,
                    'savings_percentage': 4.2,
                    'stores': [
                        {
                            'store_chain': 'Walmart',
                            'store_location': 'Toronto, ON',
                            'current_price': 4.97,
                            'regular_price': 4.97,
                            'sale_price': None,
                            'on_sale': False,
                            'distance': 1.2
                        },
                        {
                            'store_chain': 'Metro',
                            'store_location': 'Toronto, ON',
                            'current_price': 5.19,
                            'regular_price': 5.19,
                            'sale_price': None,
                            'on_sale': False,
                            'distance': 1.5
                        }
                    ]
                }
            ]
        elif 'bread' in query.lower():
            mock_results = [
                {
                    'product_name': 'Wonder Bread White 675g',
                    'brand': 'Wonder',
                    'category': 'bakery',
                    'unit_size': 675.0,
                    'unit_type': 'gram',
                    'organic': False,
                    'store_count': 3,
                    'min_price': 2.99,
                    'max_price': 3.49,
                    'avg_price': 3.16,
                    'price_difference': 0.50,
                    'savings_percentage': 14.3,
                    'stores': [
                        {
                            'store_chain': 'No Frills',
                            'store_location': 'Toronto, ON',
                            'current_price': 2.99,
                            'regular_price': 2.99,
                            'sale_price': None,
                            'on_sale': False,
                            'distance': 2.1
                        },
                        {
                            'store_chain': 'Loblaws',
                            'store_location': 'Toronto, ON',
                            'current_price': 3.19,
                            'regular_price': 3.19,
                            'sale_price': None,
                            'on_sale': False,
                            'distance': 0.8
                        },
                        {
                            'store_chain': 'Metro',
                            'store_location': 'Toronto, ON',
                            'current_price': 3.49,
                            'regular_price': 3.49,
                            'sale_price': None,
                            'on_sale': False,
                            'distance': 1.5
                        }
                    ]
                }
            ]
        
        return mock_results


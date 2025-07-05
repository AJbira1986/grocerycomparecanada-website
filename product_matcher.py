#!/usr/bin/env python3
"""
Product Matching and Normalization Engine

This module provides functionality to match and normalize grocery products
across different stores, handling variations in naming, units, and descriptions.
"""

import re
import json
import sqlite3
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from difflib import SequenceMatcher
from collections import defaultdict
import unicodedata


@dataclass
class NormalizedProduct:
    """Normalized product representation"""
    normalized_name: str
    category: str
    subcategory: str
    brand: str
    base_unit: str
    unit_size: float
    unit_type: str
    organic: bool
    keywords: List[str]
    original_products: List[Dict]


class ProductNormalizer:
    """Handles product name normalization and standardization"""
    
    def __init__(self):
        # Common brand variations and their standardized forms
        self.brand_mappings = {
            'pc': 'President\'s Choice',
            'presidents choice': 'President\'s Choice',
            'no name': 'No Name',
            'selection': 'Selection',
            'irresistible': 'Irrésistibles',
            'great value': 'Great Value',
            'kirkland': 'Kirkland Signature',
            'compliments': 'Compliments',
            'our finest': 'Our Finest'
        }
        
        # Unit standardization mappings
        self.unit_mappings = {
            'g': 'gram',
            'grams': 'gram',
            'kg': 'kilogram',
            'kilograms': 'kilogram',
            'ml': 'milliliter',
            'milliliters': 'milliliter',
            'l': 'liter',
            'liters': 'liter',
            'litres': 'liter',
            'lb': 'pound',
            'lbs': 'pound',
            'pounds': 'pound',
            'oz': 'ounce',
            'ounces': 'ounce',
            'ea': 'each',
            'each': 'each',
            'pack': 'pack',
            'packs': 'pack'
        }
        
        # Category keywords for classification
        self.category_keywords = {
            'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'dairy'],
            'meat': ['beef', 'chicken', 'pork', 'turkey', 'lamb', 'meat', 'sausage', 'bacon'],
            'produce': ['apple', 'banana', 'orange', 'lettuce', 'tomato', 'potato', 'onion', 'carrot'],
            'bakery': ['bread', 'bagel', 'muffin', 'cake', 'cookie', 'pastry'],
            'beverages': ['juice', 'soda', 'water', 'coffee', 'tea', 'beer', 'wine'],
            'frozen': ['frozen', 'ice cream', 'pizza'],
            'pantry': ['pasta', 'rice', 'cereal', 'sauce', 'oil', 'vinegar', 'spice'],
            'snacks': ['chips', 'crackers', 'nuts', 'candy', 'chocolate'],
            'household': ['detergent', 'soap', 'shampoo', 'toothpaste', 'tissue']
        }
        
        # Common words to remove for better matching
        self.stop_words = {
            'the', 'and', 'or', 'with', 'without', 'fresh', 'new', 'premium',
            'select', 'choice', 'quality', 'best', 'great', 'super', 'extra',
            'special', 'deluxe', 'classic', 'original', 'natural', 'pure'
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalize text by removing accents, converting to lowercase, etc."""
        if not text:
            return ""
        
        # Remove accents and normalize unicode
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in text if not unicodedata.combining(c))
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters except spaces and hyphens
        text = re.sub(r'[^\w\s\-]', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_brand(self, product_name: str, brand_field: str = None) -> str:
        """Extract and normalize brand from product name or brand field"""
        
        # Use brand field if available
        if brand_field:
            normalized_brand = self.normalize_text(brand_field)
            return self.brand_mappings.get(normalized_brand, brand_field.title())
        
        # Try to extract brand from product name
        normalized_name = self.normalize_text(product_name)
        
        for brand_key, brand_value in self.brand_mappings.items():
            if brand_key in normalized_name:
                return brand_value
        
        # Look for brand patterns at the beginning of the name
        words = normalized_name.split()
        if len(words) > 1:
            first_word = words[0]
            if len(first_word) > 2 and first_word.isalpha():
                return first_word.title()
        
        return "Generic"
    
    def extract_size_and_unit(self, text: str) -> Tuple[Optional[float], Optional[str]]:
        """Extract size and unit from text"""
        
        if not text:
            return None, None
        
        # Common size patterns
        size_patterns = [
            r'(\d+(?:\.\d+)?)\s*(g|grams?|kg|kilograms?)\b',
            r'(\d+(?:\.\d+)?)\s*(ml|milliliters?|l|liters?|litres?)\b',
            r'(\d+(?:\.\d+)?)\s*(lb|lbs|pounds?|oz|ounces?)\b',
            r'(\d+(?:\.\d+)?)\s*(ea|each|pack|packs?)\b',
            r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*(g|ml|oz)\b',  # Multi-pack format
            r'(\d+)\s*count\b',
            r'(\d+)\s*pk\b'
        ]
        
        text_lower = text.lower()
        
        for pattern in size_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) == 2:
                    size, unit = match.groups()
                    try:
                        size_float = float(size)
                        normalized_unit = self.unit_mappings.get(unit.lower(), unit)
                        return size_float, normalized_unit
                    except ValueError:
                        continue
                elif len(match.groups()) == 3:  # Multi-pack format
                    count, size, unit = match.groups()
                    try:
                        total_size = float(count) * float(size)
                        normalized_unit = self.unit_mappings.get(unit.lower(), unit)
                        return total_size, normalized_unit
                    except ValueError:
                        continue
        
        return None, None
    
    def categorize_product(self, product_name: str) -> Tuple[str, str]:
        """Categorize product based on keywords"""
        
        normalized_name = self.normalize_text(product_name)
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in normalized_name:
                    return category, keyword
        
        return "other", "uncategorized"
    
    def extract_keywords(self, product_name: str, description: str = None) -> List[str]:
        """Extract relevant keywords from product name and description"""
        
        text = product_name
        if description:
            text += " " + description
        
        normalized_text = self.normalize_text(text)
        words = normalized_text.split()
        
        # Filter out stop words and short words
        keywords = []
        for word in words:
            if (len(word) > 2 and 
                word not in self.stop_words and 
                not word.isdigit() and
                not re.match(r'^\d+\.?\d*$', word)):
                keywords.append(word)
        
        return list(set(keywords))  # Remove duplicates
    
    def normalize_product(self, product_data: Dict) -> NormalizedProduct:
        """Normalize a single product"""
        
        name = product_data.get('name', '')
        brand_field = product_data.get('brand')
        size_field = product_data.get('size', '')
        description = product_data.get('description', '')
        
        # Extract components
        brand = self.extract_brand(name, brand_field)
        size, unit = self.extract_size_and_unit(f"{name} {size_field}")
        category, subcategory = self.categorize_product(name)
        keywords = self.extract_keywords(name, description)
        
        # Create normalized name (remove brand and size info)
        normalized_name = self.normalize_text(name)
        for brand_key in self.brand_mappings.keys():
            normalized_name = normalized_name.replace(brand_key, '').strip()
        
        # Remove size information from name
        if size and unit:
            size_pattern = rf'\b{re.escape(str(size))}\s*{re.escape(unit)}\b'
            normalized_name = re.sub(size_pattern, '', normalized_name, flags=re.IGNORECASE).strip()
        
        # Clean up the normalized name
        normalized_name = re.sub(r'\s+', ' ', normalized_name).strip()
        
        # Detect organic
        organic = 'organic' in self.normalize_text(name + ' ' + (description or ''))
        
        return NormalizedProduct(
            normalized_name=normalized_name,
            category=category,
            subcategory=subcategory,
            brand=brand,
            base_unit=unit or 'each',
            unit_size=size or 1.0,
            unit_type=unit or 'each',
            organic=organic,
            keywords=keywords,
            original_products=[product_data]
        )


class ProductMatcher:
    """Handles matching products across different stores"""
    
    def __init__(self, normalizer: ProductNormalizer):
        self.normalizer = normalizer
        self.similarity_threshold = 0.8
        self.keyword_threshold = 0.6
    
    def calculate_similarity(self, product1: NormalizedProduct, product2: NormalizedProduct) -> float:
        """Calculate similarity score between two normalized products"""
        
        scores = []
        
        # Name similarity
        name_similarity = SequenceMatcher(None, product1.normalized_name, product2.normalized_name).ratio()
        scores.append(name_similarity * 0.4)
        
        # Brand similarity
        brand_similarity = 1.0 if product1.brand == product2.brand else 0.0
        scores.append(brand_similarity * 0.2)
        
        # Category similarity
        category_similarity = 1.0 if product1.category == product2.category else 0.0
        scores.append(category_similarity * 0.2)
        
        # Unit type similarity
        unit_similarity = 1.0 if product1.unit_type == product2.unit_type else 0.5
        scores.append(unit_similarity * 0.1)
        
        # Keywords similarity
        keywords1 = set(product1.keywords)
        keywords2 = set(product2.keywords)
        if keywords1 and keywords2:
            keyword_intersection = len(keywords1.intersection(keywords2))
            keyword_union = len(keywords1.union(keywords2))
            keyword_similarity = keyword_intersection / keyword_union if keyword_union > 0 else 0
        else:
            keyword_similarity = 0
        scores.append(keyword_similarity * 0.1)
        
        return sum(scores)
    
    def find_matches(self, products: List[NormalizedProduct]) -> List[List[NormalizedProduct]]:
        """Find matching products and group them together"""
        
        matched_groups = []
        unmatched_products = products.copy()
        
        while unmatched_products:
            current_product = unmatched_products.pop(0)
            current_group = [current_product]
            
            # Find all products that match the current product
            remaining_products = []
            for product in unmatched_products:
                similarity = self.calculate_similarity(current_product, product)
                if similarity >= self.similarity_threshold:
                    current_group.append(product)
                else:
                    remaining_products.append(product)
            
            unmatched_products = remaining_products
            matched_groups.append(current_group)
        
        return matched_groups
    
    def merge_matched_products(self, matched_group: List[NormalizedProduct]) -> NormalizedProduct:
        """Merge a group of matched products into a single normalized product"""
        
        if len(matched_group) == 1:
            return matched_group[0]
        
        # Use the most common values for merging
        brands = [p.brand for p in matched_group]
        categories = [p.category for p in matched_group]
        subcategories = [p.subcategory for p in matched_group]
        
        # Get most common brand
        brand_counts = defaultdict(int)
        for brand in brands:
            brand_counts[brand] += 1
        most_common_brand = max(brand_counts.items(), key=lambda x: x[1])[0]
        
        # Get most common category
        category_counts = defaultdict(int)
        for category in categories:
            category_counts[category] += 1
        most_common_category = max(category_counts.items(), key=lambda x: x[1])[0]
        
        # Merge keywords
        all_keywords = []
        for product in matched_group:
            all_keywords.extend(product.keywords)
        unique_keywords = list(set(all_keywords))
        
        # Merge original products
        all_original_products = []
        for product in matched_group:
            all_original_products.extend(product.original_products)
        
        # Use the first product as base and update with merged data
        base_product = matched_group[0]
        
        return NormalizedProduct(
            normalized_name=base_product.normalized_name,
            category=most_common_category,
            subcategory=base_product.subcategory,
            brand=most_common_brand,
            base_unit=base_product.base_unit,
            unit_size=base_product.unit_size,
            unit_type=base_product.unit_type,
            organic=base_product.organic,
            keywords=unique_keywords,
            original_products=all_original_products
        )


class ProductMatchingEngine:
    """Main engine for product matching and normalization"""
    
    def __init__(self, db_path: str = None):
        self.normalizer = ProductNormalizer()
        self.matcher = ProductMatcher(self.normalizer)
        self.db_path = db_path
    
    def load_products_from_db(self) -> List[Dict]:
        """Load products from SQLite database"""
        
        if not self.db_path:
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM products 
                WHERE name IS NOT NULL AND name != ''
                ORDER BY store_chain, name
            ''')
            
            products = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return products
            
        except Exception as e:
            print(f"Error loading products from database: {e}")
            return []
    
    def process_products(self, products: List[Dict]) -> List[NormalizedProduct]:
        """Process and normalize a list of products"""
        
        normalized_products = []
        
        for product in products:
            try:
                normalized = self.normalizer.normalize_product(product)
                normalized_products.append(normalized)
            except Exception as e:
                print(f"Error normalizing product {product.get('name', 'Unknown')}: {e}")
                continue
        
        return normalized_products
    
    def find_price_comparisons(self, normalized_products: List[NormalizedProduct]) -> List[Dict]:
        """Find products available at multiple stores for price comparison"""
        
        matched_groups = self.matcher.find_matches(normalized_products)
        
        price_comparisons = []
        
        for group in matched_groups:
            if len(group) > 1:  # Only include products available at multiple stores
                merged_product = self.matcher.merge_matched_products(group)
                
                # Extract price information from original products
                store_prices = []
                for original_product in merged_product.original_products:
                    store_info = {
                        'store_chain': original_product.get('store_chain'),
                        'store_location': original_product.get('store_location'),
                        'current_price': original_product.get('current_price'),
                        'regular_price': original_product.get('regular_price'),
                        'sale_price': original_product.get('sale_price'),
                        'on_sale': original_product.get('on_sale', False),
                        'unit_price': original_product.get('unit_price'),
                        'size': original_product.get('size')
                    }
                    store_prices.append(store_info)
                
                # Calculate price statistics
                prices = [p['current_price'] for p in store_prices if p['current_price']]
                if prices:
                    min_price = min(prices)
                    max_price = max(prices)
                    avg_price = sum(prices) / len(prices)
                    
                    comparison = {
                        'product_name': merged_product.normalized_name,
                        'brand': merged_product.brand,
                        'category': merged_product.category,
                        'unit_size': merged_product.unit_size,
                        'unit_type': merged_product.unit_type,
                        'organic': merged_product.organic,
                        'store_count': len(store_prices),
                        'min_price': min_price,
                        'max_price': max_price,
                        'avg_price': avg_price,
                        'price_difference': max_price - min_price,
                        'savings_percentage': ((max_price - min_price) / max_price * 100) if max_price > 0 else 0,
                        'stores': store_prices
                    }
                    
                    price_comparisons.append(comparison)
        
        # Sort by potential savings
        price_comparisons.sort(key=lambda x: x['price_difference'], reverse=True)
        
        return price_comparisons
    
    def generate_matching_report(self, products: List[Dict]) -> Dict:
        """Generate a comprehensive matching report"""
        
        print("🔄 Processing products...")
        normalized_products = self.process_products(products)
        
        print("🔍 Finding matches...")
        matched_groups = self.matcher.find_matches(normalized_products)
        
        print("💰 Calculating price comparisons...")
        price_comparisons = self.find_price_comparisons(normalized_products)
        
        # Generate statistics
        total_products = len(products)
        total_normalized = len(normalized_products)
        total_groups = len(matched_groups)
        multi_store_groups = len([g for g in matched_groups if len(g) > 1])
        
        # Category breakdown
        category_counts = defaultdict(int)
        for product in normalized_products:
            category_counts[product.category] += 1
        
        # Brand breakdown
        brand_counts = defaultdict(int)
        for product in normalized_products:
            brand_counts[product.brand] += 1
        
        report = {
            'summary': {
                'total_products': total_products,
                'normalized_products': total_normalized,
                'product_groups': total_groups,
                'multi_store_products': multi_store_groups,
                'price_comparisons': len(price_comparisons)
            },
            'categories': dict(category_counts),
            'brands': dict(brand_counts),
            'top_savings_opportunities': price_comparisons[:10],
            'all_comparisons': price_comparisons
        }
        
        return report


def main():
    """Demo function to test the product matching engine"""
    
    print("🛒 Product Matching and Normalization Engine Demo")
    print("=" * 60)
    
    # Sample product data for testing
    sample_products = [
        {
            'name': 'Organic Valley Whole Milk 1L',
            'brand': 'Organic Valley',
            'size': '1L',
            'current_price': 5.99,
            'store_chain': 'Metro',
            'store_location': 'Toronto'
        },
        {
            'name': 'Organic Valley Milk Whole 1 Liter',
            'brand': 'Organic Valley',
            'size': '1 Liter',
            'current_price': 6.29,
            'store_chain': 'Loblaws',
            'store_location': 'Toronto'
        },
        {
            'name': 'PC Organic Whole Milk 1L',
            'brand': 'President\'s Choice',
            'size': '1L',
            'current_price': 4.99,
            'store_chain': 'No Frills',
            'store_location': 'Toronto'
        },
        {
            'name': 'Lactantia 2% Milk 2L',
            'brand': 'Lactantia',
            'size': '2L',
            'current_price': 4.97,
            'store_chain': 'Metro',
            'store_location': 'Toronto'
        },
        {
            'name': 'Lactantia Milk 2% 2 Liters',
            'brand': 'Lactantia',
            'size': '2 Liters',
            'current_price': 5.19,
            'store_chain': 'Walmart',
            'store_location': 'Toronto'
        }
    ]
    
    # Initialize the matching engine
    engine = ProductMatchingEngine()
    
    # Generate matching report
    report = engine.generate_matching_report(sample_products)
    
    # Display results
    print("\n📊 Matching Report Summary:")
    print("-" * 40)
    for key, value in report['summary'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n🏷️  Categories Found:")
    print("-" * 40)
    for category, count in report['categories'].items():
        print(f"{category.title()}: {count} products")
    
    print("\n🏪 Brands Found:")
    print("-" * 40)
    for brand, count in report['brands'].items():
        print(f"{brand}: {count} products")
    
    print("\n💰 Top Savings Opportunities:")
    print("-" * 60)
    for i, comparison in enumerate(report['top_savings_opportunities'], 1):
        print(f"\n{i}. {comparison['product_name']} ({comparison['brand']})")
        print(f"   Price range: ${comparison['min_price']:.2f} - ${comparison['max_price']:.2f}")
        print(f"   Potential savings: ${comparison['price_difference']:.2f} ({comparison['savings_percentage']:.1f}%)")
        print(f"   Available at {comparison['store_count']} stores")
    
    print(f"\n{'='*60}")
    print("Demo completed! The engine successfully matched and normalized products.")
    print("In a real implementation, this would process thousands of products from the database.")


if __name__ == '__main__':
    main()


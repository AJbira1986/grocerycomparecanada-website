#!/usr/bin/env python3
"""
Database seeding script for grocery price comparison API
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, date
from src.main import app
from src.models.user import db
from src.models.grocery_chain import GroceryChain
from src.models.store import Store
from src.models.product_category import ProductCategory
from src.models.product import Product
from src.models.price import Price

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create grocery chains
        print("Creating grocery chains...")
        chains = [
            GroceryChain(
                chain_id='walmart',
                chain_name='Walmart',
                logo_url='https://logos.com/walmart.png',
                website_url='https://www.walmart.ca'
            ),
            GroceryChain(
                chain_id='loblaws',
                chain_name='Loblaws',
                logo_url='https://logos.com/loblaws.png',
                website_url='https://www.loblaws.ca'
            ),
            GroceryChain(
                chain_id='metro',
                chain_name='Metro',
                logo_url='https://logos.com/metro.png',
                website_url='https://www.metro.ca'
            ),
            GroceryChain(
                chain_id='nofrills',
                chain_name='No Frills',
                logo_url='https://logos.com/nofrills.png',
                website_url='https://www.nofrills.ca'
            ),
            GroceryChain(
                chain_id='costco',
                chain_name='Costco',
                logo_url='https://logos.com/costco.png',
                website_url='https://www.costco.ca'
            )
        ]
        
        for chain in chains:
            db.session.add(chain)
        
        # Create stores
        print("Creating stores...")
        stores = [
            # Toronto stores
            Store(
                store_id='walmart_toronto_queen',
                chain_id='walmart',
                store_name='Walmart Supercentre Queen St',
                address_street='123 Queen St W',
                address_city='Toronto',
                address_province='ON',
                postal_code='M5V 3A8',
                latitude=43.6426,
                longitude=-79.3871,
                phone='(416) 555-0123',
                hours={
                    'monday': '7:00-23:00',
                    'tuesday': '7:00-23:00',
                    'wednesday': '7:00-23:00',
                    'thursday': '7:00-23:00',
                    'friday': '7:00-23:00',
                    'saturday': '7:00-23:00',
                    'sunday': '8:00-22:00'
                },
                services=['pharmacy', 'bakery', 'deli'],
                features=['wheelchair_accessible', 'parking_available']
            ),
            Store(
                store_id='loblaws_toronto_college',
                chain_id='loblaws',
                store_name='Loblaws College Park',
                address_street='444 Yonge St',
                address_city='Toronto',
                address_province='ON',
                postal_code='M5B 2H4',
                latitude=43.6591,
                longitude=-79.3847,
                phone='(416) 555-0456',
                hours={
                    'monday': '7:00-23:00',
                    'tuesday': '7:00-23:00',
                    'wednesday': '7:00-23:00',
                    'thursday': '7:00-23:00',
                    'friday': '7:00-23:00',
                    'saturday': '7:00-23:00',
                    'sunday': '8:00-22:00'
                },
                services=['pharmacy', 'bakery', 'deli', 'floral'],
                features=['wheelchair_accessible', 'click_and_collect']
            ),
            Store(
                store_id='metro_toronto_king',
                chain_id='metro',
                store_name='Metro King Street',
                address_street='456 King St W',
                address_city='Toronto',
                address_province='ON',
                postal_code='M5V 1M3',
                latitude=43.6465,
                longitude=-79.3890,
                phone='(416) 555-0789',
                hours={
                    'monday': '8:00-22:00',
                    'tuesday': '8:00-22:00',
                    'wednesday': '8:00-22:00',
                    'thursday': '8:00-22:00',
                    'friday': '8:00-22:00',
                    'saturday': '8:00-22:00',
                    'sunday': '9:00-21:00'
                },
                services=['bakery', 'deli'],
                features=['wheelchair_accessible']
            ),
            # Ottawa stores
            Store(
                store_id='walmart_ottawa_baseline',
                chain_id='walmart',
                store_name='Walmart Baseline Road',
                address_street='3651 Baseline Rd',
                address_city='Ottawa',
                address_province='ON',
                postal_code='K2H 1B7',
                latitude=45.3506,
                longitude=-75.7582,
                phone='(613) 555-0123',
                hours={
                    'monday': '7:00-23:00',
                    'tuesday': '7:00-23:00',
                    'wednesday': '7:00-23:00',
                    'thursday': '7:00-23:00',
                    'friday': '7:00-23:00',
                    'saturday': '7:00-23:00',
                    'sunday': '8:00-22:00'
                },
                services=['pharmacy', 'bakery'],
                features=['wheelchair_accessible', 'parking_available']
            ),
            Store(
                store_id='loblaws_ottawa_rideau',
                chain_id='loblaws',
                store_name='Loblaws Rideau Centre',
                address_street='50 Rideau St',
                address_city='Ottawa',
                address_province='ON',
                postal_code='K1N 9J7',
                latitude=45.4267,
                longitude=-75.6927,
                phone='(613) 555-0456',
                hours={
                    'monday': '7:00-23:00',
                    'tuesday': '7:00-23:00',
                    'wednesday': '7:00-23:00',
                    'thursday': '7:00-23:00',
                    'friday': '7:00-23:00',
                    'saturday': '7:00-23:00',
                    'sunday': '8:00-22:00'
                },
                services=['pharmacy', 'bakery', 'deli'],
                features=['wheelchair_accessible']
            )
        ]
        
        for store in stores:
            db.session.add(store)
        
        # Create product categories
        print("Creating product categories...")
        categories = [
            ProductCategory(
                category_id='dairy',
                category_name='Dairy & Eggs',
                description='Milk, cheese, yogurt, eggs and dairy products'
            ),
            ProductCategory(
                category_id='produce',
                category_name='Produce',
                description='Fresh fruits and vegetables'
            ),
            ProductCategory(
                category_id='meat',
                category_name='Meat & Seafood',
                description='Fresh and frozen meat, poultry and seafood'
            ),
            ProductCategory(
                category_id='bakery',
                category_name='Bakery',
                description='Fresh bread, pastries and baked goods'
            ),
            ProductCategory(
                category_id='pantry',
                category_name='Pantry',
                description='Canned goods, pasta, rice and pantry staples'
            ),
            # Subcategories
            ProductCategory(
                category_id='milk',
                category_name='Milk',
                parent_category_id='dairy',
                description='All types of milk'
            ),
            ProductCategory(
                category_id='cheese',
                category_name='Cheese',
                parent_category_id='dairy',
                description='All types of cheese'
            ),
            ProductCategory(
                category_id='apples',
                category_name='Apples',
                parent_category_id='produce',
                description='Fresh apples'
            ),
            ProductCategory(
                category_id='bananas',
                category_name='Bananas',
                parent_category_id='produce',
                description='Fresh bananas'
            )
        ]
        
        for category in categories:
            db.session.add(category)
        
        # Create products
        print("Creating products...")
        products = [
            Product(
                product_id='milk_organic_valley_1l',
                name='Organic Valley Whole Milk 1L',
                brand='Organic Valley',
                category_id='dairy',
                subcategory_id='milk',
                size='1L',
                unit_type='volume',
                barcode='123456789012',
                ingredients=['Organic milk', 'Vitamin D3'],
                allergens=['Milk'],
                nutrition_info={
                    'serving_size': '250ml',
                    'calories': 150,
                    'fat_g': 8,
                    'protein_g': 8
                },
                image_urls=['https://example.com/organic_valley_milk.jpg']
            ),
            Product(
                product_id='milk_lactantia_2l',
                name='Lactantia 2% Milk 2L',
                brand='Lactantia',
                category_id='dairy',
                subcategory_id='milk',
                size='2L',
                unit_type='volume',
                barcode='123456789013',
                ingredients=['Milk', 'Vitamin A', 'Vitamin D3'],
                allergens=['Milk'],
                nutrition_info={
                    'serving_size': '250ml',
                    'calories': 130,
                    'fat_g': 5,
                    'protein_g': 8
                },
                image_urls=['https://example.com/lactantia_milk.jpg']
            ),
            Product(
                product_id='bread_wonder_white',
                name='Wonder White Bread 675g',
                brand='Wonder',
                category_id='bakery',
                size='675g',
                unit_type='weight',
                barcode='123456789014',
                ingredients=['Enriched wheat flour', 'Water', 'Sugar', 'Yeast'],
                allergens=['Wheat', 'Gluten'],
                nutrition_info={
                    'serving_size': '2 slices',
                    'calories': 140,
                    'carbohydrates_g': 26,
                    'protein_g': 4
                },
                image_urls=['https://example.com/wonder_bread.jpg']
            ),
            Product(
                product_id='bananas_fresh',
                name='Fresh Bananas',
                brand=None,
                category_id='produce',
                subcategory_id='bananas',
                size='per lb',
                unit_type='weight',
                nutrition_info={
                    'serving_size': '1 medium banana',
                    'calories': 105,
                    'carbohydrates_g': 27,
                    'potassium_mg': 422
                },
                image_urls=['https://example.com/bananas.jpg']
            ),
            Product(
                product_id='apples_gala',
                name='Gala Apples',
                brand=None,
                category_id='produce',
                subcategory_id='apples',
                size='per lb',
                unit_type='weight',
                nutrition_info={
                    'serving_size': '1 medium apple',
                    'calories': 95,
                    'carbohydrates_g': 25,
                    'fiber_g': 4
                },
                image_urls=['https://example.com/gala_apples.jpg']
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        # Commit all the above before creating prices
        db.session.commit()
        
        # Create prices
        print("Creating prices...")
        prices = [
            # Organic Valley Milk prices
            Price(
                product_id='milk_organic_valley_1l',
                store_id='walmart_toronto_queen',
                current_price=5.99,
                regular_price=6.49,
                on_sale=True,
                sale_end_date=date(2025, 1, 15),
                data_source='flyer',
                scraped_at=datetime.utcnow()
            ),
            Price(
                product_id='milk_organic_valley_1l',
                store_id='loblaws_toronto_college',
                current_price=6.29,
                regular_price=6.29,
                on_sale=False,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            Price(
                product_id='milk_organic_valley_1l',
                store_id='metro_toronto_king',
                current_price=6.49,
                regular_price=6.49,
                on_sale=False,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            # Lactantia Milk prices
            Price(
                product_id='milk_lactantia_2l',
                store_id='walmart_toronto_queen',
                current_price=4.97,
                regular_price=4.97,
                on_sale=False,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            Price(
                product_id='milk_lactantia_2l',
                store_id='loblaws_toronto_college',
                current_price=5.29,
                regular_price=5.79,
                on_sale=True,
                sale_end_date=date(2025, 1, 20),
                data_source='flyer',
                scraped_at=datetime.utcnow()
            ),
            # Wonder Bread prices
            Price(
                product_id='bread_wonder_white',
                store_id='walmart_toronto_queen',
                current_price=2.97,
                regular_price=2.97,
                on_sale=False,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            Price(
                product_id='bread_wonder_white',
                store_id='loblaws_toronto_college',
                current_price=3.49,
                regular_price=3.49,
                on_sale=False,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            # Banana prices
            Price(
                product_id='bananas_fresh',
                store_id='walmart_toronto_queen',
                current_price=1.48,
                regular_price=1.48,
                on_sale=False,
                price_per_unit=1.48,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            Price(
                product_id='bananas_fresh',
                store_id='loblaws_toronto_college',
                current_price=1.69,
                regular_price=1.69,
                on_sale=False,
                price_per_unit=1.69,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            # Apple prices
            Price(
                product_id='apples_gala',
                store_id='walmart_toronto_queen',
                current_price=2.97,
                regular_price=2.97,
                on_sale=False,
                price_per_unit=2.97,
                data_source='website',
                scraped_at=datetime.utcnow()
            ),
            Price(
                product_id='apples_gala',
                store_id='loblaws_toronto_college',
                current_price=3.49,
                regular_price=3.99,
                on_sale=True,
                sale_end_date=date(2025, 1, 12),
                price_per_unit=3.49,
                data_source='flyer',
                scraped_at=datetime.utcnow()
            )
        ]
        
        for price in prices:
            db.session.add(price)
        
        # Commit all changes
        db.session.commit()
        print("Database seeded successfully!")
        
        # Print summary
        print(f"Created {len(chains)} grocery chains")
        print(f"Created {len(stores)} stores")
        print(f"Created {len(categories)} product categories")
        print(f"Created {len(products)} products")
        print(f"Created {len(prices)} price entries")

if __name__ == '__main__':
    seed_database()


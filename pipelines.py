# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sqlite3
import os
from datetime import datetime
from itemadapter import ItemAdapter
from .items import GroceryProductItem, StoreLocationItem, FlyerItem


class ValidationPipeline:
    """Pipeline to validate scraped items"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if isinstance(item, GroceryProductItem):
            # Validate required fields
            if not adapter.get('name'):
                raise DropItem(f"Missing product name: {item}")
            
            # Clean and validate prices
            for price_field in ['regular_price', 'sale_price', 'current_price', 'unit_price']:
                price = adapter.get(price_field)
                if price is not None:
                    try:
                        adapter[price_field] = float(price)
                    except (ValueError, TypeError):
                        adapter[price_field] = None
            
            # Ensure current_price is set
            if not adapter.get('current_price'):
                if adapter.get('sale_price'):
                    adapter['current_price'] = adapter['sale_price']
                elif adapter.get('regular_price'):
                    adapter['current_price'] = adapter['regular_price']
        
        return item


class DuplicatesPipeline:
    """Pipeline to filter out duplicate items"""
    
    def __init__(self):
        self.ids_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if isinstance(item, GroceryProductItem):
            # Create unique identifier
            product_id = adapter.get('product_id')
            store_id = adapter.get('store_id', 'unknown')
            unique_id = f"{product_id}_{store_id}"
            
            if unique_id in self.ids_seen:
                raise DropItem(f"Duplicate item found: {unique_id}")
            else:
                self.ids_seen.add(unique_id)
        
        return item


class JsonWriterPipeline:
    """Pipeline to write items to JSON file"""
    
    def open_spider(self, spider):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'grocery_data_{spider.name}_{timestamp}.json'
        self.file = open(filename, 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True
    
    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()
    
    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        else:
            self.first_item = False
        
        line = json.dumps(ItemAdapter(item).asdict(), indent=2, ensure_ascii=False)
        self.file.write(line)
        return item


class SQLitePipeline:
    """Pipeline to store items in SQLite database"""
    
    def __init__(self, sqlite_db):
        self.sqlite_db = sqlite_db
    
    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DATABASE")
        if not db_settings:
            db_settings = {'sqlite_db': 'grocery_data.db'}
        return cls(
            sqlite_db=db_settings['sqlite_db'],
        )
    
    def open_spider(self, spider):
        self.connection = sqlite3.connect(self.sqlite_db)
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def close_spider(self, spider):
        self.connection.close()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        
        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                name TEXT NOT NULL,
                brand TEXT,
                description TEXT,
                category TEXT,
                subcategory TEXT,
                size TEXT,
                weight TEXT,
                unit TEXT,
                regular_price REAL,
                sale_price REAL,
                current_price REAL,
                unit_price REAL,
                unit_price_measure TEXT,
                on_sale BOOLEAN,
                sale_start_date TEXT,
                sale_end_date TEXT,
                discount_percentage REAL,
                store_chain TEXT,
                store_id TEXT,
                store_name TEXT,
                store_location TEXT,
                organic BOOLEAN,
                local_product BOOLEAN,
                canadian_product BOOLEAN,
                scraped_at TEXT,
                source_url TEXT,
                flyer_week TEXT,
                UNIQUE(product_id, store_id, scraped_at)
            )
        ''')
        
        # Store locations table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS store_locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_id TEXT UNIQUE,
                store_name TEXT,
                chain_name TEXT,
                street_address TEXT,
                city TEXT,
                province TEXT,
                postal_code TEXT,
                country TEXT,
                latitude REAL,
                longitude REAL,
                phone_number TEXT,
                store_hours TEXT,
                services TEXT,
                scraped_at TEXT,
                source_url TEXT
            )
        ''')
        
        # Flyers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flyers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flyer_id TEXT UNIQUE,
                store_chain TEXT,
                title TEXT,
                start_date TEXT,
                end_date TEXT,
                week_of TEXT,
                page_count INTEGER,
                product_count INTEGER,
                categories TEXT,
                scraped_at TEXT,
                source_url TEXT
            )
        ''')
        
        self.connection.commit()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if isinstance(item, GroceryProductItem):
            self.insert_product(adapter)
        elif isinstance(item, StoreLocationItem):
            self.insert_store_location(adapter)
        elif isinstance(item, FlyerItem):
            self.insert_flyer(adapter)
        
        return item
    
    def insert_product(self, adapter):
        """Insert product into database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO products (
                    product_id, name, brand, description, category, subcategory,
                    size, weight, unit, regular_price, sale_price, current_price,
                    unit_price, unit_price_measure, on_sale, sale_start_date,
                    sale_end_date, discount_percentage, store_chain, store_id,
                    store_name, store_location, organic, local_product,
                    canadian_product, scraped_at, source_url, flyer_week
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                adapter.get('product_id'),
                adapter.get('name'),
                adapter.get('brand'),
                adapter.get('description'),
                adapter.get('category'),
                adapter.get('subcategory'),
                adapter.get('size'),
                adapter.get('weight'),
                adapter.get('unit'),
                adapter.get('regular_price'),
                adapter.get('sale_price'),
                adapter.get('current_price'),
                adapter.get('unit_price'),
                adapter.get('unit_price_measure'),
                adapter.get('on_sale'),
                adapter.get('sale_start_date'),
                adapter.get('sale_end_date'),
                adapter.get('discount_percentage'),
                adapter.get('store_chain'),
                adapter.get('store_id'),
                adapter.get('store_name'),
                adapter.get('store_location'),
                adapter.get('organic'),
                adapter.get('local_product'),
                adapter.get('canadian_product'),
                adapter.get('scraped_at'),
                adapter.get('source_url'),
                adapter.get('flyer_week')
            ))
            self.connection.commit()
        except sqlite3.Error as e:
            spider.logger.error(f"Error inserting product: {e}")
    
    def insert_store_location(self, adapter):
        """Insert store location into database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO store_locations (
                    store_id, store_name, chain_name, street_address, city,
                    province, postal_code, country, latitude, longitude,
                    phone_number, store_hours, services, scraped_at, source_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                adapter.get('store_id'),
                adapter.get('store_name'),
                adapter.get('chain_name'),
                adapter.get('street_address'),
                adapter.get('city'),
                adapter.get('province'),
                adapter.get('postal_code'),
                adapter.get('country'),
                adapter.get('latitude'),
                adapter.get('longitude'),
                adapter.get('phone_number'),
                adapter.get('store_hours'),
                adapter.get('services'),
                adapter.get('scraped_at'),
                adapter.get('source_url')
            ))
            self.connection.commit()
        except sqlite3.Error as e:
            spider.logger.error(f"Error inserting store location: {e}")
    
    def insert_flyer(self, adapter):
        """Insert flyer into database"""
        try:
            categories_json = json.dumps(adapter.get('categories')) if adapter.get('categories') else None
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO flyers (
                    flyer_id, store_chain, title, start_date, end_date,
                    week_of, page_count, product_count, categories,
                    scraped_at, source_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                adapter.get('flyer_id'),
                adapter.get('store_chain'),
                adapter.get('title'),
                adapter.get('start_date'),
                adapter.get('end_date'),
                adapter.get('week_of'),
                adapter.get('page_count'),
                adapter.get('product_count'),
                categories_json,
                adapter.get('scraped_at'),
                adapter.get('source_url')
            ))
            self.connection.commit()
        except sqlite3.Error as e:
            spider.logger.error(f"Error inserting flyer: {e}")


class PriceComparisonPipeline:
    """Pipeline to calculate price comparisons and savings"""
    
    def __init__(self):
        self.products_by_name = {}
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if isinstance(item, GroceryProductItem):
            product_name = adapter.get('name', '').lower().strip()
            current_price = adapter.get('current_price')
            
            if product_name and current_price:
                if product_name not in self.products_by_name:
                    self.products_by_name[product_name] = []
                
                self.products_by_name[product_name].append({
                    'store': adapter.get('store_chain'),
                    'price': current_price,
                    'item': item
                })
        
        return item
    
    def close_spider(self, spider):
        """Calculate price comparisons when spider closes"""
        
        comparison_data = []
        
        for product_name, stores_data in self.products_by_name.items():
            if len(stores_data) > 1:
                prices = [data['price'] for data in stores_data]
                min_price = min(prices)
                max_price = max(prices)
                avg_price = sum(prices) / len(prices)
                
                comparison = {
                    'product_name': product_name,
                    'stores_count': len(stores_data),
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_price': avg_price,
                    'price_difference': max_price - min_price,
                    'savings_percentage': ((max_price - min_price) / max_price * 100) if max_price > 0 else 0,
                    'stores': stores_data
                }
                
                comparison_data.append(comparison)
        
        # Save comparison data
        if comparison_data:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'price_comparisons_{timestamp}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(comparison_data, f, indent=2, ensure_ascii=False, default=str)
            
            spider.logger.info(f"Price comparison data saved to {filename}")
            spider.logger.info(f"Found {len(comparison_data)} products with price differences")


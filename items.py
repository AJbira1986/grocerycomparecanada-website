# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime


class GroceryProductItem(scrapy.Item):
    """Item for grocery product data"""
    
    # Product identification
    product_id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    
    # Product details
    size = scrapy.Field()
    weight = scrapy.Field()
    unit = scrapy.Field()
    
    # Pricing information
    regular_price = scrapy.Field()
    sale_price = scrapy.Field()
    current_price = scrapy.Field()
    unit_price = scrapy.Field()
    unit_price_measure = scrapy.Field()
    
    # Sale information
    on_sale = scrapy.Field()
    sale_start_date = scrapy.Field()
    sale_end_date = scrapy.Field()
    discount_percentage = scrapy.Field()
    
    # Store information
    store_chain = scrapy.Field()
    store_id = scrapy.Field()
    store_name = scrapy.Field()
    store_location = scrapy.Field()
    
    # Product attributes
    organic = scrapy.Field()
    local_product = scrapy.Field()
    canadian_product = scrapy.Field()
    
    # Scraping metadata
    scraped_at = scrapy.Field()
    source_url = scrapy.Field()
    flyer_week = scrapy.Field()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['scraped_at'] = datetime.now().isoformat()


class StoreLocationItem(scrapy.Item):
    """Item for store location data"""
    
    store_id = scrapy.Field()
    store_name = scrapy.Field()
    chain_name = scrapy.Field()
    
    # Address information
    street_address = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    postal_code = scrapy.Field()
    country = scrapy.Field()
    
    # Geographic coordinates
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    
    # Store details
    phone_number = scrapy.Field()
    store_hours = scrapy.Field()
    services = scrapy.Field()
    
    # Scraping metadata
    scraped_at = scrapy.Field()
    source_url = scrapy.Field()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['scraped_at'] = datetime.now().isoformat()


class FlyerItem(scrapy.Item):
    """Item for flyer metadata"""
    
    flyer_id = scrapy.Field()
    store_chain = scrapy.Field()
    title = scrapy.Field()
    
    # Date information
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    week_of = scrapy.Field()
    
    # Flyer details
    page_count = scrapy.Field()
    product_count = scrapy.Field()
    categories = scrapy.Field()
    
    # Scraping metadata
    scraped_at = scrapy.Field()
    source_url = scrapy.Field()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['scraped_at'] = datetime.now().isoformat()


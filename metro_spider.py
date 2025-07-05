import scrapy
import re
import json
from urllib.parse import urljoin, urlparse, parse_qs
from datetime import datetime, timedelta
from ..items import GroceryProductItem, FlyerItem


class MetroSpider(scrapy.Spider):
    name = 'metro'
    allowed_domains = ['metro.ca']
    
    # Custom settings for this spider
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Be respectful with requests
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    def __init__(self, store_id=None, postal_code=None, *args, **kwargs):
        super(MetroSpider, self).__init__(*args, **kwargs)
        self.store_id = store_id
        self.postal_code = postal_code
        
        # Base URLs
        self.base_url = 'https://www.metro.ca'
        self.flyer_url = 'https://www.metro.ca/en/flyer'
        self.catalog_url = 'https://www.metro.ca/en/online-grocery/flyer'
        
        # Store chain information
        self.store_chain = 'Metro'
        
    def start_requests(self):
        """Generate initial requests"""
        
        # Start with the main flyer page to get store information
        yield scrapy.Request(
            url=self.flyer_url,
            callback=self.parse_flyer_page,
            meta={'dont_cache': True}
        )
    
    def parse_flyer_page(self, response):
        """Parse the main flyer page to get store info and redirect to catalog"""
        
        # Extract store information if available
        store_info = self.extract_store_info(response)
        
        # Build catalog URL with filters for flyer deals
        catalog_params = {
            'sortOrder': 'relevance',
            'filter': ':relevance:deal:Flyer & Deals'
        }
        
        catalog_url = f"{self.catalog_url}?" + "&".join([f"{k}={v}" for k, v in catalog_params.items()])
        
        yield scrapy.Request(
            url=catalog_url,
            callback=self.parse_catalog,
            meta={
                'store_info': store_info,
                'dont_cache': True
            }
        )
    
    def parse_catalog(self, response):
        """Parse the catalog view with product listings"""
        
        store_info = response.meta.get('store_info', {})
        
        # Extract flyer metadata
        flyer_item = self.extract_flyer_metadata(response, store_info)
        if flyer_item:
            yield flyer_item
        
        # Extract product information
        products = self.extract_products(response, store_info)
        for product in products:
            yield product
        
        # Handle pagination if present
        next_page = self.get_next_page(response)
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_catalog,
                meta=response.meta
            )
    
    def extract_store_info(self, response):
        """Extract store information from the page"""
        store_info = {
            'chain_name': self.store_chain,
            'store_id': None,
            'store_name': None,
            'location': None
        }
        
        # Try to extract store name and location
        store_text = response.css('.store-selector-text::text').get()
        if store_text:
            # Parse store information from text like "Metro Niagara Falls"
            store_info['store_name'] = store_text.strip()
            if 'Metro' in store_text:
                location = store_text.replace('Metro', '').strip()
                store_info['location'] = location
        
        return store_info
    
    def extract_flyer_metadata(self, response, store_info):
        """Extract flyer metadata"""
        
        # Try to find total item count
        item_count_text = response.css('.results-count::text').get()
        item_count = None
        if item_count_text:
            count_match = re.search(r'(\d+)\s+items?', item_count_text)
            if count_match:
                item_count = int(count_match.group(1))
        
        flyer_item = FlyerItem()
        flyer_item['flyer_id'] = f"metro_{datetime.now().strftime('%Y%m%d')}"
        flyer_item['store_chain'] = self.store_chain
        flyer_item['title'] = f"Metro Weekly Flyer - {datetime.now().strftime('%B %d, %Y')}"
        flyer_item['start_date'] = datetime.now().date().isoformat()
        flyer_item['end_date'] = (datetime.now() + timedelta(days=7)).date().isoformat()
        flyer_item['week_of'] = datetime.now().strftime('%Y-W%U')
        flyer_item['product_count'] = item_count
        flyer_item['source_url'] = response.url
        
        return flyer_item
    
    def extract_products(self, response, store_info):
        """Extract product information from catalog page"""
        
        products = []
        
        # Find product containers - these may be in different CSS selectors
        product_selectors = [
            '.product-tile',
            '.product-card',
            '.product-item',
            '[data-testid*="product"]',
            '.tile-product'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = response.css(selector)
            if elements:
                product_elements = elements
                break
        
        if not product_elements:
            # Fallback: look for any element containing price information
            product_elements = response.css('*:contains("$")').xpath('./ancestor-or-self::*[contains(@class, "product") or contains(@class, "tile") or contains(@class, "card")]')
        
        for product_element in product_elements:
            product = self.parse_product_element(product_element, store_info, response.url)
            if product:
                products.append(product)
        
        return products
    
    def parse_product_element(self, element, store_info, source_url):
        """Parse individual product element"""
        
        try:
            product = GroceryProductItem()
            
            # Extract product name
            name_selectors = [
                '.product-name::text',
                '.product-title::text',
                '.tile-product-name::text',
                'h3::text',
                'h4::text',
                '[data-testid*="name"]::text'
            ]
            
            name = None
            for selector in name_selectors:
                name = element.css(selector).get()
                if name:
                    break
            
            if not name:
                # Try to get name from any text content
                all_text = element.css('::text').getall()
                for text in all_text:
                    text = text.strip()
                    if text and len(text) > 5 and not re.match(r'^\$?\d+\.?\d*', text):
                        name = text
                        break
            
            if not name:
                return None
            
            product['name'] = name.strip()
            
            # Extract brand information
            brand_selectors = [
                '.product-brand::text',
                '.brand::text',
                '.tile-product-brand::text'
            ]
            
            brand = None
            for selector in brand_selectors:
                brand = element.css(selector).get()
                if brand:
                    break
            
            product['brand'] = brand.strip() if brand else None
            
            # Extract size/weight information
            size_selectors = [
                '.product-size::text',
                '.size::text',
                '.tile-product-size::text',
                '.product-format::text'
            ]
            
            size = None
            for selector in size_selectors:
                size = element.css(selector).get()
                if size:
                    break
            
            product['size'] = size.strip() if size else None
            
            # Extract pricing information
            prices = self.extract_prices(element)
            product.update(prices)
            
            # Extract sale information
            sale_info = self.extract_sale_info(element)
            product.update(sale_info)
            
            # Store information
            product['store_chain'] = store_info.get('chain_name', self.store_chain)
            product['store_id'] = store_info.get('store_id')
            product['store_name'] = store_info.get('store_name')
            product['store_location'] = store_info.get('location')
            
            # Generate product ID
            product_name_clean = re.sub(r'[^a-zA-Z0-9]', '_', name.lower())
            product['product_id'] = f"metro_{product_name_clean}_{product.get('size', '').replace(' ', '_').lower()}"
            
            # Additional attributes
            product['organic'] = 'organic' in name.lower()
            product['canadian_product'] = self.detect_canadian_product(element)
            
            # Metadata
            product['source_url'] = source_url
            product['flyer_week'] = datetime.now().strftime('%Y-W%U')
            
            return product
            
        except Exception as e:
            self.logger.error(f"Error parsing product element: {e}")
            return None
    
    def extract_prices(self, element):
        """Extract pricing information from product element"""
        
        prices = {
            'regular_price': None,
            'sale_price': None,
            'current_price': None,
            'unit_price': None,
            'unit_price_measure': None
        }
        
        # Look for price elements
        price_selectors = [
            '.price',
            '.product-price',
            '.tile-price',
            '[data-testid*="price"]'
        ]
        
        price_elements = []
        for selector in price_selectors:
            elements = element.css(selector)
            if elements:
                price_elements.extend(elements)
        
        if not price_elements:
            # Fallback: look for any text containing dollar signs
            price_elements = element.css('*:contains("$")')
        
        # Extract price values
        all_prices = []
        for price_elem in price_elements:
            price_text = price_elem.css('::text').get()
            if price_text:
                price_matches = re.findall(r'\$(\d+\.?\d*)', price_text)
                for match in price_matches:
                    try:
                        all_prices.append(float(match))
                    except ValueError:
                        continue
        
        # Determine regular vs sale price
        if len(all_prices) >= 2:
            # Assume higher price is regular, lower is sale
            all_prices.sort(reverse=True)
            prices['regular_price'] = all_prices[0]
            prices['sale_price'] = all_prices[1]
            prices['current_price'] = all_prices[1]
        elif len(all_prices) == 1:
            prices['current_price'] = all_prices[0]
        
        # Extract unit pricing
        unit_price_pattern = r'\$(\d+\.?\d*)\s*/\s*(\d+\s*(?:g|kg|ml|l|lb|oz|un|ea))'
        unit_price_text = element.css('::text').getall()
        for text in unit_price_text:
            unit_match = re.search(unit_price_pattern, text, re.IGNORECASE)
            if unit_match:
                prices['unit_price'] = float(unit_match.group(1))
                prices['unit_price_measure'] = unit_match.group(2)
                break
        
        return prices
    
    def extract_sale_info(self, element):
        """Extract sale information"""
        
        sale_info = {
            'on_sale': False,
            'sale_start_date': None,
            'sale_end_date': None,
            'discount_percentage': None
        }
        
        # Check for sale indicators
        sale_indicators = [
            '.sale',
            '.on-sale',
            '.discount',
            '.promo',
            '[data-testid*="sale"]'
        ]
        
        for indicator in sale_indicators:
            if element.css(indicator):
                sale_info['on_sale'] = True
                break
        
        # Check for "Save" text or similar
        all_text = ' '.join(element.css('::text').getall()).lower()
        if 'save' in all_text or 'sale' in all_text or 'promo' in all_text:
            sale_info['on_sale'] = True
        
        return sale_info
    
    def detect_canadian_product(self, element):
        """Detect if product is Canadian"""
        
        # Look for Canadian indicators
        canadian_indicators = [
            'canada',
            'canadian',
            'product of canada',
            'maple leaf'
        ]
        
        all_text = ' '.join(element.css('::text').getall()).lower()
        
        for indicator in canadian_indicators:
            if indicator in all_text:
                return True
        
        # Check for Canadian flag or maple leaf images
        img_alts = element.css('img::attr(alt)').getall()
        for alt in img_alts:
            if alt and ('canada' in alt.lower() or 'maple' in alt.lower()):
                return True
        
        return False
    
    def get_next_page(self, response):
        """Get next page URL if pagination exists"""
        
        # Look for pagination links
        next_selectors = [
            '.pagination .next::attr(href)',
            '.pager .next::attr(href)',
            '[data-testid*="next"]::attr(href)',
            'a:contains("Next")::attr(href)',
            'a:contains("More")::attr(href)'
        ]
        
        for selector in next_selectors:
            next_url = response.css(selector).get()
            if next_url:
                return urljoin(response.url, next_url)
        
        # Check for infinite scroll or load more functionality
        # This would require JavaScript execution in a real implementation
        
        return None


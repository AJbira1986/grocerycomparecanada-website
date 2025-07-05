# GroceryCompare Technical Documentation

**Version:** 1.0.0  
**Last Updated:** July 4, 2025  
**Author:** Manus AI  

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Design](#architecture-design)
3. [Frontend Implementation](#frontend-implementation)
4. [Backend Implementation](#backend-implementation)
5. [Database Schema](#database-schema)
6. [Web Scraping System](#web-scraping-system)
7. [Product Matching Engine](#product-matching-engine)
8. [API Documentation](#api-documentation)
9. [Deployment Guide](#deployment-guide)
10. [Testing Strategy](#testing-strategy)
11. [Performance Optimization](#performance-optimization)
12. [Security Considerations](#security-considerations)
13. [Monitoring and Logging](#monitoring-and-logging)
14. [Troubleshooting Guide](#troubleshooting-guide)

## 🏗️ System Overview

### Architecture Philosophy
GroceryCompare follows a modern, microservices-inspired architecture with clear separation of concerns. The system is designed for scalability, maintainability, and performance, utilizing industry best practices and proven technologies.

### Core Components
1. **React Frontend**: Single-page application with responsive design
2. **Flask Backend**: RESTful API server with modular structure
3. **SQLite/PostgreSQL Database**: Relational data storage with normalized schema
4. **Scrapy Web Scraper**: Automated data collection from grocery store websites
5. **Product Matching Engine**: NLP-powered product normalization and comparison
6. **Location Services**: Postal code validation and proximity calculation

### Technology Stack Rationale

#### Frontend: React + Tailwind CSS
- **React 18.2.0**: Chosen for its mature ecosystem, excellent performance, and strong community support
- **Tailwind CSS 3.3.0**: Utility-first approach enables rapid development and consistent design
- **Vite 4.4.5**: Fast build tool with hot module replacement for optimal developer experience
- **shadcn/ui**: High-quality, accessible components reducing development time

#### Backend: Python Flask
- **Flask 2.3.3**: Lightweight framework allowing fine-grained control over application structure
- **SQLAlchemy 2.0**: Powerful ORM with excellent PostgreSQL support and migration capabilities
- **Flask-CORS**: Essential for cross-origin requests in modern web applications
- **Python 3.11**: Latest stable version with performance improvements and enhanced type hints

#### Data Processing: Scrapy + Custom Matching
- **Scrapy 2.11**: Industry-standard web scraping framework with robust anti-detection features
- **BeautifulSoup4**: HTML parsing for complex page structures
- **Custom NLP Engine**: Tailored product matching using fuzzy string matching and semantic analysis

## 🏛️ Architecture Design

### System Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │    │   Flask API     │    │   PostgreSQL    │
│                 │    │                 │    │   Database      │
│ • Components    │◄──►│ • REST Endpoints│◄──►│                 │
│ • State Mgmt    │    │ • Business Logic│    │ • Products      │
│ • API Client    │    │ • Data Models   │    │ • Stores        │
└─────────────────┘    └─────────────────┘    │ • Prices        │
                                              │ • Locations     │
                                              └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Scrapy Engine  │
                       │                 │
                       │ • Store Spiders │
                       │ • Data Pipeline │
                       │ • Scheduling    │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Product Matcher │
                       │                 │
                       │ • Fuzzy Match   │
                       │ • Normalization │
                       │ • Categorization│
                       └─────────────────┘
```

### Data Flow Architecture

```
User Input (Postal Code) → Location Validation → Store Lookup → Display Stores
                                                      ↓
User Input (Product Search) → Product Matching → Price Comparison → Display Results
                                     ↓
                            Database Query → Price Analysis → Savings Calculation
```

### Component Interaction Patterns

#### Frontend-Backend Communication
- **RESTful API**: All communication follows REST principles with JSON payloads
- **Error Handling**: Standardized error responses with appropriate HTTP status codes
- **CORS Configuration**: Properly configured for cross-origin requests
- **Request/Response Validation**: Input sanitization and output formatting

#### Database Access Patterns
- **ORM Usage**: SQLAlchemy models for all database operations
- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Indexed queries and eager loading for performance
- **Transaction Management**: Proper transaction boundaries for data consistency

## 🎨 Frontend Implementation

### Project Structure
```
grocery-price-frontend/
├── src/
│   ├── components/
│   │   └── ui/                 # Reusable UI components
│   │       ├── button.jsx      # Button component
│   │       ├── input.jsx       # Input field component
│   │       ├── card.jsx        # Card container component
│   │       ├── badge.jsx       # Badge/label component
│   │       └── separator.jsx   # Visual separator component
│   ├── App.jsx                 # Main application component
│   ├── App.css                 # Application-specific styles
│   └── main.jsx               # Application entry point
├── index.html                  # HTML template
├── package.json               # Dependencies and scripts
├── tailwind.config.js         # Tailwind CSS configuration
├── vite.config.js             # Vite build configuration
└── README.md                  # Frontend documentation
```

### Component Architecture

#### App.jsx - Main Application Component
```javascript
// State management for application-wide data
const [postalCode, setPostalCode] = useState('')
const [stores, setStores] = useState([])
const [searchQuery, setSearchQuery] = useState('')
const [searchResults, setSearchResults] = useState([])
const [selectedProduct, setSelectedProduct] = useState(null)
const [priceComparison, setPriceComparison] = useState(null)
const [loading, setLoading] = useState(false)
const [error, setError] = useState(null)

// API integration functions
const findStores = async (postalCode) => { /* Implementation */ }
const searchProducts = async (query, postalCode) => { /* Implementation */ }
const getProductComparison = async (productId) => { /* Implementation */ }
```

#### UI Component Library Integration
The application uses shadcn/ui components for consistent design:

```javascript
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Separator } from '@/components/ui/separator.jsx'
```

### State Management Strategy

#### Local State with React Hooks
- **useState**: Component-level state for form inputs and UI state
- **useEffect**: Side effects for API calls and data fetching
- **Custom Hooks**: Reusable logic for API interactions and data processing

#### State Structure
```javascript
// Application state schema
{
  postalCode: string,           // User's postal code input
  stores: Array<Store>,         // Nearby stores from API
  searchQuery: string,          // Product search input
  searchResults: Array<Product>, // Search results from API
  selectedProduct: Product|null, // Currently selected product
  priceComparison: Comparison|null, // Price comparison data
  loading: boolean,             // Loading state for UI feedback
  error: string|null           // Error message for user feedback
}
```

### Responsive Design Implementation

#### Tailwind CSS Utility Classes
```css
/* Mobile-first responsive design */
.container {
  @apply w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8;
}

.grid-responsive {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4;
}

.button-responsive {
  @apply w-full sm:w-auto px-4 py-2 text-sm sm:text-base;
}
```

#### Breakpoint Strategy
- **Mobile**: 320px - 640px (base styles)
- **Tablet**: 641px - 1024px (md: prefix)
- **Desktop**: 1025px+ (lg: and xl: prefixes)

### Performance Optimizations

#### Code Splitting and Lazy Loading
```javascript
// Dynamic imports for large components
const ProductComparison = lazy(() => import('./components/ProductComparison'))

// Suspense wrapper for loading states
<Suspense fallback={<LoadingSpinner />}>
  <ProductComparison data={priceComparison} />
</Suspense>
```

#### API Request Optimization
```javascript
// Debounced search to reduce API calls
const debouncedSearch = useCallback(
  debounce((query) => {
    if (query.length >= 2) {
      searchProducts(query, postalCode)
    }
  }, 300),
  [postalCode]
)
```

## ⚙️ Backend Implementation

### Project Structure
```
grocery-price-api/
├── src/
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── grocery_chain.py    # Grocery chain model
│   │   ├── store.py           # Store location model
│   │   ├── product_category.py # Product category model
│   │   ├── product.py         # Product model
│   │   ├── price.py           # Price tracking model
│   │   └── user.py            # User model (template)
│   ├── routes/                # API endpoints
│   │   ├── __init__.py
│   │   ├── stores.py          # Store-related endpoints
│   │   ├── products.py        # Product search and comparison
│   │   ├── prices.py          # Price tracking endpoints
│   │   ├── locations.py       # Location services
│   │   └── user.py            # User endpoints (template)
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── product_matcher_service.py # Product matching logic
│   └── main.py                # Application entry point
├── venv/                      # Python virtual environment
├── requirements.txt           # Python dependencies
├── seed_data.py              # Database seeding script
└── README.md                 # Backend documentation
```

### Database Models

#### Core Model Relationships
```python
# Grocery Chain Model
class GroceryChain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website_url = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    
    # Relationships
    stores = db.relationship('Store', backref='chain', lazy=True)

# Store Model
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('grocery_chain.id'))
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    province = db.Column(db.String(50))
    postal_code = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Relationships
    prices = db.relationship('Price', backref='store', lazy=True)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    brand = db.Column(db.String(100))
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    size = db.Column(db.String(50))
    weight = db.Column(db.Float)
    unit = db.Column(db.String(20))
    
    # Relationships
    prices = db.relationship('Price', backref='product', lazy=True)

# Price Model
class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    regular_price = db.Column(db.Float)
    sale_price = db.Column(db.Float)
    on_sale = db.Column(db.Boolean, default=False)
    sale_start_date = db.Column(db.Date)
    sale_end_date = db.Column(db.Date)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
```

### API Endpoint Implementation

#### Store Lookup Endpoints
```python
@stores_bp.route('/nearby', methods=['GET'])
def get_nearby_stores():
    """Find stores near a postal code"""
    postal_code = request.args.get('postal_code', '').strip()
    radius = float(request.args.get('radius', 10))  # Default 10km
    
    # Validate postal code format
    if not validate_canadian_postal_code(postal_code):
        return jsonify({'error': 'Invalid postal code format'}), 400
    
    # Get coordinates from postal code
    coordinates = get_coordinates_from_postal_code(postal_code)
    if not coordinates:
        return jsonify({'error': 'Postal code not found'}), 404
    
    # Find nearby stores using spatial query
    nearby_stores = find_stores_within_radius(
        coordinates['lat'], 
        coordinates['lng'], 
        radius
    )
    
    return jsonify({
        'postal_code': postal_code,
        'coordinates': coordinates,
        'stores': nearby_stores,
        'count': len(nearby_stores)
    })
```

#### Product Search Endpoints
```python
@products_bp.route('/search', methods=['GET'])
def search_products():
    """Search for products and return price comparisons"""
    query = request.args.get('q', '').strip()
    postal_code = request.args.get('postal_code', '').strip()
    limit = min(int(request.args.get('limit', 20)), 50)
    
    if not query or len(query) < 2:
        return jsonify({'error': 'Query must be at least 2 characters'}), 400
    
    # Use product matcher service for intelligent search
    results = matcher_service.search_products(query, postal_code, limit)
    
    return jsonify({
        'query': query,
        'postal_code': postal_code,
        'results_count': len(results),
        'products': results
    })
```

### Business Logic Services

#### Product Matcher Service
```python
class ProductMatcherService:
    """Service for intelligent product matching and price comparison"""
    
    def __init__(self):
        self.engine = ProductMatchingEngine() if ProductMatchingEngine else None
    
    def search_products(self, query: str, postal_code: str = None, limit: int = 20):
        """Search for products with intelligent matching"""
        # Normalize search query
        normalized_query = self.normalize_search_query(query)
        
        # Search database with fuzzy matching
        products = self.fuzzy_search_products(normalized_query, limit * 2)
        
        # Apply product matching engine if available
        if self.engine and products:
            matched_products = self.engine.match_products(products)
            return self.format_search_results(matched_products[:limit])
        
        # Fallback to simple search results
        return self.format_simple_results(products[:limit])
    
    def get_price_comparison(self, product_id: int):
        """Get detailed price comparison for a specific product"""
        # Find similar products across stores
        similar_products = self.find_similar_products(product_id)
        
        # Calculate price statistics
        price_stats = self.calculate_price_statistics(similar_products)
        
        # Format comparison data
        return self.format_price_comparison(similar_products, price_stats)
```

### Error Handling Strategy

#### Standardized Error Responses
```python
def handle_api_error(error):
    """Standardized error response format"""
    if isinstance(error, ValidationError):
        return jsonify({
            'error': 'Validation Error',
            'message': str(error),
            'status_code': 400
        }), 400
    elif isinstance(error, NotFoundError):
        return jsonify({
            'error': 'Resource Not Found',
            'message': str(error),
            'status_code': 404
        }), 404
    else:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500
```

#### Input Validation
```python
def validate_canadian_postal_code(postal_code):
    """Validate Canadian postal code format (A1A 1A1)"""
    pattern = r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$'
    return bool(re.match(pattern, postal_code))

def validate_search_query(query):
    """Validate product search query"""
    if not query or len(query.strip()) < 2:
        raise ValidationError("Search query must be at least 2 characters")
    if len(query) > 100:
        raise ValidationError("Search query too long")
    return query.strip()
```

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  GroceryChain   │    │     Store       │    │     Price       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │◄──┤│ id (PK)         │◄──┤│ id (PK)         │
│ name            │   ││ chain_id (FK)   │   ││ product_id (FK) │
│ website_url     │   ││ name            │   ││ store_id (FK)   │
│ logo_url        │   ││ address         │   ││ current_price   │
│ created_at      │   ││ city            │   ││ regular_price   │
└─────────────────┘   ││ province        │   ││ sale_price      │
                      ││ postal_code     │   ││ on_sale         │
                      ││ latitude        │   ││ sale_start_date │
                      ││ longitude       │   ││ sale_end_date   │
                      ││ created_at      │   ││ last_updated    │
                      └─────────────────┘   └─────────────────┘
                                                      │
                      ┌─────────────────┐            │
                      │    Product      │◄───────────┘
                      ├─────────────────┤
                      │ id (PK)         │
                      │ name            │
                      │ brand           │
                      │ description     │
                      │ category        │
                      │ subcategory_id  │
                      │ size            │
                      │ weight          │
                      │ unit            │
                      │ organic         │
                      │ local_product   │
                      │ created_at      │
                      └─────────────────┘
                               │
                      ┌─────────────────┐
                      │ ProductCategory │
                      ├─────────────────┤
                      │ id (PK)         │
                      │ name            │
                      │ parent_id (FK)  │
                      │ description     │
                      │ created_at      │
                      └─────────────────┘
```

### Database Indexes for Performance

```sql
-- Indexes for optimal query performance
CREATE INDEX idx_store_postal_code ON store(postal_code);
CREATE INDEX idx_store_coordinates ON store(latitude, longitude);
CREATE INDEX idx_product_name ON product(name);
CREATE INDEX idx_product_brand ON product(brand);
CREATE INDEX idx_product_category ON product(category);
CREATE INDEX idx_price_product_store ON price(product_id, store_id);
CREATE INDEX idx_price_current_price ON price(current_price);
CREATE INDEX idx_price_last_updated ON price(last_updated);

-- Composite indexes for complex queries
CREATE INDEX idx_product_search ON product(name, brand, category);
CREATE INDEX idx_price_comparison ON price(product_id, current_price, on_sale);
```

### Data Migration Strategy

```python
# Database migration script example
def upgrade():
    """Add new columns for enhanced product tracking"""
    op.add_column('product', sa.Column('organic', sa.Boolean(), default=False))
    op.add_column('product', sa.Column('local_product', sa.Boolean(), default=False))
    op.add_column('product', sa.Column('nutrition_score', sa.Float()))
    
    # Create new index for performance
    op.create_index('idx_product_organic', 'product', ['organic'])

def downgrade():
    """Rollback migration"""
    op.drop_index('idx_product_organic', 'product')
    op.drop_column('product', 'nutrition_score')
    op.drop_column('product', 'local_product')
    op.drop_column('product', 'organic')
```

## 🕷️ Web Scraping System

### Scrapy Project Structure

```
grocery-scraper/
├── grocery_scraper/
│   ├── spiders/               # Spider implementations
│   │   ├── __init__.py
│   │   ├── metro_spider.py    # Metro grocery chain spider
│   │   ├── walmart_spider.py  # Walmart spider
│   │   └── loblaws_spider.py  # Loblaws spider
│   ├── items.py              # Data models for scraped items
│   ├── pipelines.py          # Data processing pipelines
│   ├── settings.py           # Scrapy configuration
│   └── middlewares.py        # Custom middleware
├── run_scraper.py            # Scraper execution script
└── requirements.txt          # Scraping dependencies
```

### Spider Implementation

#### Metro Spider Example
```python
class MetroSpider(scrapy.Spider):
    name = 'metro'
    allowed_domains = ['metro.ca']
    start_urls = ['https://www.metro.ca/en/flyer']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'USER_AGENT': 'Mozilla/5.0 (compatible; GroceryBot/1.0)',
        'ROBOTSTXT_OBEY': True
    }
    
    def parse(self, response):
        """Parse the main flyer page"""
        # Extract flyer URLs
        flyer_urls = response.css('.flyer-link::attr(href)').getall()
        
        for url in flyer_urls:
            yield response.follow(url, self.parse_flyer)
    
    def parse_flyer(self, response):
        """Parse individual flyer pages"""
        products = response.css('.product-item')
        
        for product in products:
            item = GroceryItem()
            item['name'] = product.css('.product-name::text').get()
            item['price'] = self.extract_price(product.css('.price::text').get())
            item['brand'] = product.css('.brand::text').get()
            item['size'] = product.css('.size::text').get()
            item['store_chain'] = 'Metro'
            item['scraped_at'] = datetime.now()
            
            yield item
    
    def extract_price(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract number
        price_match = re.search(r'(\d+\.?\d*)', price_text.replace(',', ''))
        return float(price_match.group(1)) if price_match else None
```

### Data Processing Pipelines

#### Price Validation Pipeline
```python
class PriceValidationPipeline:
    """Validate and clean price data"""
    
    def process_item(self, item, spider):
        # Validate price range
        if item.get('price'):
            price = float(item['price'])
            if price < 0.01 or price > 1000:
                raise DropItem(f"Invalid price: {price}")
        
        # Validate required fields
        required_fields = ['name', 'store_chain']
        for field in required_fields:
            if not item.get(field):
                raise DropItem(f"Missing required field: {field}")
        
        return item

class ProductNormalizationPipeline:
    """Normalize product data for consistency"""
    
    def __init__(self):
        self.normalizer = ProductNormalizer()
    
    def process_item(self, item, spider):
        # Normalize product name
        item['normalized_name'] = self.normalizer.normalize_name(item['name'])
        
        # Extract and normalize brand
        item['normalized_brand'] = self.normalizer.extract_brand(item['name'])
        
        # Categorize product
        item['category'] = self.normalizer.categorize_product(item['name'])
        
        # Standardize units
        item['standardized_size'] = self.normalizer.standardize_size(item.get('size', ''))
        
        return item

class DatabaseStoragePipeline:
    """Store processed items in database"""
    
    def open_spider(self, spider):
        self.connection = sqlite3.connect('grocery_data.db')
        self.cursor = self.connection.cursor()
    
    def close_spider(self, spider):
        self.connection.close()
    
    def process_item(self, item, spider):
        # Insert or update product
        product_id = self.upsert_product(item)
        
        # Insert price record
        self.insert_price(product_id, item)
        
        self.connection.commit()
        return item
```

### Anti-Detection Strategies

#### Rotating User Agents
```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

class RotateUserAgentMiddleware:
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENTS)
```

#### Proxy Rotation
```python
class ProxyMiddleware:
    def __init__(self):
        self.proxies = [
            'http://proxy1:8080',
            'http://proxy2:8080',
            'http://proxy3:8080'
        ]
    
    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy
```

## 🧠 Product Matching Engine

### Fuzzy Matching Algorithm

```python
class ProductMatchingEngine:
    """Advanced product matching using NLP techniques"""
    
    def __init__(self):
        self.normalizer = ProductNormalizer()
        self.matcher = ProductMatcher()
        self.similarity_threshold = 0.85
    
    def match_products(self, products):
        """Group similar products across stores"""
        normalized_products = [self.normalizer.normalize(p) for p in products]
        
        # Create similarity matrix
        similarity_matrix = self.calculate_similarity_matrix(normalized_products)
        
        # Group products by similarity
        product_groups = self.cluster_similar_products(
            normalized_products, 
            similarity_matrix
        )
        
        # Generate price comparisons
        comparisons = []
        for group in product_groups:
            if len(group) > 1:  # Only include products available at multiple stores
                comparison = self.create_price_comparison(group)
                comparisons.append(comparison)
        
        return sorted(comparisons, key=lambda x: x['price_difference'], reverse=True)
    
    def calculate_similarity_matrix(self, products):
        """Calculate pairwise similarity between products"""
        n = len(products)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                similarity = self.calculate_product_similarity(products[i], products[j])
                matrix[i][j] = matrix[j][i] = similarity
        
        return matrix
    
    def calculate_product_similarity(self, product1, product2):
        """Calculate similarity score between two products"""
        # Name similarity (weighted 50%)
        name_sim = fuzz.ratio(product1['normalized_name'], product2['normalized_name']) / 100
        
        # Brand similarity (weighted 30%)
        brand_sim = 1.0 if product1['brand'] == product2['brand'] else 0.0
        
        # Size similarity (weighted 20%)
        size_sim = self.calculate_size_similarity(product1['size'], product2['size'])
        
        # Weighted average
        total_similarity = (name_sim * 0.5) + (brand_sim * 0.3) + (size_sim * 0.2)
        
        return total_similarity
```

### Product Normalization

```python
class ProductNormalizer:
    """Normalize product data for consistent matching"""
    
    def __init__(self):
        self.brand_patterns = self.load_brand_patterns()
        self.size_patterns = self.load_size_patterns()
        self.category_keywords = self.load_category_keywords()
    
    def normalize_name(self, name):
        """Normalize product name for matching"""
        if not name:
            return ""
        
        # Convert to lowercase
        normalized = name.lower()
        
        # Remove special characters
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        # Remove common stop words
        stop_words = {'the', 'and', 'or', 'with', 'for', 'in', 'on', 'at'}
        words = [w for w in normalized.split() if w not in stop_words]
        
        return ' '.join(words)
    
    def extract_brand(self, name):
        """Extract brand name from product name"""
        for pattern, brand in self.brand_patterns.items():
            if re.search(pattern, name, re.IGNORECASE):
                return brand
        
        # Fallback: first word might be brand
        words = name.split()
        return words[0] if words else ""
    
    def standardize_size(self, size_text):
        """Standardize size/weight information"""
        if not size_text:
            return None
        
        # Extract numeric value and unit
        size_match = re.search(r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)', size_text)
        if not size_match:
            return None
        
        value, unit = size_match.groups()
        value = float(value)
        unit = unit.lower()
        
        # Convert to standard units
        if unit in ['g', 'gram', 'grams']:
            return {'value': value, 'unit': 'g'}
        elif unit in ['kg', 'kilogram', 'kilograms']:
            return {'value': value * 1000, 'unit': 'g'}
        elif unit in ['ml', 'milliliter', 'milliliters']:
            return {'value': value, 'unit': 'ml'}
        elif unit in ['l', 'liter', 'liters', 'litre', 'litres']:
            return {'value': value * 1000, 'unit': 'ml'}
        else:
            return {'value': value, 'unit': unit}
    
    def categorize_product(self, name):
        """Automatically categorize product based on name"""
        name_lower = name.lower()
        
        for category, keywords in self.category_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                return category
        
        return 'other'
```

## 📡 API Documentation

### Authentication
Currently, the API does not require authentication for public endpoints. Future versions may implement API key authentication for rate limiting and usage tracking.

### Base URL
```
Development: http://localhost:5002/api
Production: https://api.grocerycompare.ca/api
```

### Response Format
All API responses follow a consistent JSON structure:

```json
{
  "status": "success|error",
  "data": { ... },
  "message": "Optional descriptive message",
  "timestamp": "2025-07-04T21:30:00Z",
  "request_id": "uuid-string"
}
```

### Error Handling
HTTP status codes are used appropriately:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input parameters
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Endpoint Reference

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "service": "GroceryCompare API",
    "version": "1.0.0",
    "uptime": "2 days, 14 hours",
    "database_status": "connected"
  }
}
```

#### Store Endpoints

##### Get Nearby Stores
```http
GET /api/stores/nearby?postal_code={postal_code}&radius={radius}
```

**Parameters:**
- `postal_code` (required): Canadian postal code (A1A 1A1 format)
- `radius` (optional): Search radius in kilometers (default: 10, max: 50)

**Response:**
```json
{
  "status": "success",
  "data": {
    "postal_code": "M5V 3A8",
    "coordinates": {
      "latitude": 43.6426,
      "longitude": -79.3871
    },
    "stores": [
      {
        "id": 1,
        "name": "Walmart Supercentre Queen St",
        "chain": "Walmart",
        "address": "123 Queen St W, Toronto, ON",
        "distance_km": 1.2,
        "coordinates": {
          "latitude": 43.6500,
          "longitude": -79.3900
        }
      }
    ],
    "count": 1
  }
}
```

#### Product Endpoints

##### Search Products
```http
GET /api/products/search?q={query}&postal_code={postal_code}&limit={limit}
```

**Parameters:**
- `q` (required): Search query (minimum 2 characters)
- `postal_code` (optional): Postal code for location-based results
- `limit` (optional): Maximum results (default: 20, max: 50)

**Response:**
```json
{
  "status": "success",
  "data": {
    "query": "milk",
    "results_count": 2,
    "products": [
      {
        "product_name": "Organic Valley Whole Milk 1L",
        "brand": "Organic Valley",
        "category": "dairy",
        "store_count": 3,
        "min_price": 5.99,
        "max_price": 6.49,
        "avg_price": 6.16,
        "price_difference": 0.50,
        "savings_percentage": 7.7,
        "best_store": {
          "name": "Walmart Supercentre",
          "price": 5.99,
          "distance_km": 1.2
        }
      }
    ]
  }
}
```

##### Get Product Price Comparison
```http
GET /api/products/{product_id}/compare
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "product_name": "Organic Valley Whole Milk 1L",
    "brand": "Organic Valley",
    "size": "1L",
    "store_count": 3,
    "price_statistics": {
      "min_price": 5.99,
      "max_price": 6.49,
      "avg_price": 6.16,
      "price_difference": 0.50,
      "savings_percentage": 7.7
    },
    "stores": [
      {
        "store_chain": "Walmart",
        "store_name": "Walmart Supercentre Queen St",
        "store_location": "Toronto, ON",
        "current_price": 5.99,
        "regular_price": 6.49,
        "sale_price": 5.99,
        "on_sale": true,
        "sale_end_date": "2025-01-15",
        "distance_km": 1.2
      }
    ]
  }
}
```

### Rate Limiting
- **Public endpoints**: 100 requests per minute per IP
- **Search endpoints**: 50 requests per minute per IP
- **Bulk operations**: 10 requests per minute per IP

### API Versioning
The API uses URL versioning:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, etc.

## 🚀 Deployment Guide

### Development Environment Setup

#### Prerequisites
```bash
# System requirements
- Node.js 18+ with npm/pnpm
- Python 3.11+ with pip
- Git for version control
- SQLite (included with Python)
- Optional: PostgreSQL for production-like testing
```

#### Frontend Development Setup
```bash
# Clone repository
git clone <repository-url>
cd grocery-price-frontend

# Install dependencies
pnpm install

# Start development server
pnpm run dev

# Build for production
pnpm run build

# Preview production build
pnpm run preview
```

#### Backend Development Setup
```bash
# Navigate to backend directory
cd grocery-price-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python seed_data.py

# Start development server
python src/main.py
```

### Production Deployment

#### Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd grocery-price-frontend
vercel --prod

# Configure environment variables in Vercel dashboard
VITE_API_BASE_URL=https://api.grocerycompare.ca/api
```

#### Backend Deployment (Railway/Render)

##### Railway Deployment
```yaml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python src/main.py"
healthcheckPath = "/api/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"

[env]
FLASK_ENV = "production"
DATABASE_URL = "${{ RAILWAY_DATABASE_URL }}"
```

##### Render Deployment
```yaml
# render.yaml
services:
  - type: web
    name: grocerycompare-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python src/main.py"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: grocerycompare-db
          property: connectionString

databases:
  - name: grocerycompare-db
    databaseName: grocerycompare
    user: grocerycompare
```

#### Database Migration for Production
```python
# production_setup.py
import os
from src.main import app, db

def setup_production_database():
    """Initialize production database"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Seed initial data
        seed_grocery_chains()
        seed_store_locations()
        
        print("Production database setup complete")

def seed_grocery_chains():
    """Seed grocery chain data"""
    chains = [
        {'name': 'Walmart', 'website_url': 'https://walmart.ca'},
        {'name': 'Loblaws', 'website_url': 'https://loblaws.ca'},
        {'name': 'Metro', 'website_url': 'https://metro.ca'},
        {'name': 'No Frills', 'website_url': 'https://nofrills.ca'},
        {'name': 'Costco', 'website_url': 'https://costco.ca'},
        {'name': 'Food Basics', 'website_url': 'https://foodbasics.ca'}
    ]
    
    for chain_data in chains:
        chain = GroceryChain(**chain_data)
        db.session.add(chain)
    
    db.session.commit()

if __name__ == '__main__':
    setup_production_database()
```

### Environment Configuration

#### Frontend Environment Variables
```bash
# .env.production
VITE_API_BASE_URL=https://api.grocerycompare.ca/api
VITE_ENVIRONMENT=production
VITE_ANALYTICS_ID=GA_TRACKING_ID
```

#### Backend Environment Variables
```bash
# Production environment variables
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://grocerycompare.ca,https://www.grocerycompare.ca
REDIS_URL=redis://redis-host:6379/0
```

### SSL/TLS Configuration
```nginx
# nginx.conf for SSL termination
server {
    listen 443 ssl http2;
    server_name api.grocerycompare.ca;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Monitoring and Health Checks

#### Application Health Endpoint
```python
@app.route('/api/health')
def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check database connectivity
        db.session.execute('SELECT 1')
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check external dependencies
    external_services = check_external_services()
    
    health_data = {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": db_status,
        "external_services": external_services,
        "uptime": get_uptime()
    }
    
    status_code = 200 if health_data["status"] == "healthy" else 503
    return jsonify(health_data), status_code
```

## 🧪 Testing Strategy

### Frontend Testing

#### Unit Testing with Vitest
```javascript
// src/components/__tests__/ProductSearch.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import ProductSearch from '../ProductSearch'

describe('ProductSearch Component', () => {
  test('renders search input and button', () => {
    render(<ProductSearch onSearch={vi.fn()} />)
    
    expect(screen.getByPlaceholderText(/search for products/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument()
  })
  
  test('calls onSearch when form is submitted', async () => {
    const mockOnSearch = vi.fn()
    render(<ProductSearch onSearch={mockOnSearch} />)
    
    const input = screen.getByPlaceholderText(/search for products/i)
    const button = screen.getByRole('button', { name: /search/i })
    
    fireEvent.change(input, { target: { value: 'milk' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith('milk')
    })
  })
  
  test('validates minimum search length', () => {
    render(<ProductSearch onSearch={vi.fn()} />)
    
    const input = screen.getByPlaceholderText(/search for products/i)
    fireEvent.change(input, { target: { value: 'a' } })
    
    expect(screen.getByText(/search must be at least 2 characters/i)).toBeInTheDocument()
  })
})
```

#### Integration Testing
```javascript
// src/__tests__/App.integration.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import App from '../App'

// Mock API calls
vi.mock('../services/api', () => ({
  searchProducts: vi.fn(),
  findStores: vi.fn(),
  getProductComparison: vi.fn()
}))

describe('App Integration Tests', () => {
  test('complete user workflow: postal code -> search -> comparison', async () => {
    const mockSearchProducts = vi.mocked(searchProducts)
    const mockFindStores = vi.mocked(findStores)
    
    mockFindStores.mockResolvedValue([
      { id: 1, name: 'Walmart', distance: 1.2 }
    ])
    
    mockSearchProducts.mockResolvedValue([
      { id: 1, name: 'Milk', price: 5.99, store: 'Walmart' }
    ])
    
    render(<App />)
    
    // Enter postal code
    const postalInput = screen.getByPlaceholderText(/postal code/i)
    fireEvent.change(postalInput, { target: { value: 'M5V 3A8' } })
    fireEvent.click(screen.getByText(/find stores/i))
    
    // Wait for stores to load
    await waitFor(() => {
      expect(screen.getByText('Walmart')).toBeInTheDocument()
    })
    
    // Search for products
    const searchInput = screen.getByPlaceholderText(/search for products/i)
    fireEvent.change(searchInput, { target: { value: 'milk' } })
    fireEvent.click(screen.getByText(/search/i))
    
    // Verify results
    await waitFor(() => {
      expect(screen.getByText('Milk')).toBeInTheDocument()
      expect(screen.getByText('$5.99')).toBeInTheDocument()
    })
  })
})
```

### Backend Testing

#### Unit Testing with pytest
```python
# tests/test_product_matcher.py
import pytest
from src.services.product_matcher_service import ProductMatcherService

class TestProductMatcherService:
    def setup_method(self):
        self.service = ProductMatcherService()
    
    def test_search_products_valid_query(self):
        """Test product search with valid query"""
        results = self.service.search_products("milk", "M5V 3A8", 10)
        
        assert isinstance(results, list)
        assert len(results) <= 10
        
        if results:
            result = results[0]
            assert 'product_name' in result
            assert 'min_price' in result
            assert 'store_count' in result
    
    def test_search_products_invalid_query(self):
        """Test product search with invalid query"""
        results = self.service.search_products("a", "M5V 3A8", 10)
        assert results == []
    
    def test_get_price_comparison(self):
        """Test price comparison functionality"""
        comparison = self.service.get_price_comparison(1)
        
        if comparison:
            assert 'product_name' in comparison
            assert 'stores' in comparison
            assert 'price_statistics' in comparison
            assert isinstance(comparison['stores'], list)

# tests/test_api_endpoints.py
import pytest
from src.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestAPIEndpoints:
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_product_search_endpoint(self, client):
        """Test product search endpoint"""
        response = client.get('/api/products/search?q=milk')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'products' in data
        assert 'query' in data
        assert data['query'] == 'milk'
    
    def test_product_search_invalid_query(self, client):
        """Test product search with invalid query"""
        response = client.get('/api/products/search?q=a')
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
    
    def test_stores_nearby_endpoint(self, client):
        """Test nearby stores endpoint"""
        response = client.get('/api/stores/nearby?postal_code=M5V 3A8')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'stores' in data
        assert 'postal_code' in data
```

#### API Testing with pytest
```python
# tests/test_integration.py
import pytest
import requests
from unittest.mock import patch

class TestAPIIntegration:
    @pytest.fixture
    def api_base_url(self):
        return "http://localhost:5002/api"
    
    def test_full_user_workflow(self, api_base_url):
        """Test complete user workflow through API"""
        
        # Step 1: Find nearby stores
        stores_response = requests.get(
            f"{api_base_url}/stores/nearby",
            params={"postal_code": "M5V 3A8"}
        )
        assert stores_response.status_code == 200
        stores_data = stores_response.json()
        assert len(stores_data['stores']) > 0
        
        # Step 2: Search for products
        search_response = requests.get(
            f"{api_base_url}/products/search",
            params={"q": "milk", "postal_code": "M5V 3A8"}
        )
        assert search_response.status_code == 200
        search_data = search_response.json()
        assert len(search_data['products']) > 0
        
        # Step 3: Get price comparison (if products found)
        if search_data['products']:
            product_id = 1  # Mock product ID
            comparison_response = requests.get(
                f"{api_base_url}/products/{product_id}/compare"
            )
            # Should return comparison data or 404 if not found
            assert comparison_response.status_code in [200, 404]
```

### Performance Testing

#### Load Testing with Locust
```python
# locustfile.py
from locust import HttpUser, task, between

class GroceryCompareUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup user session"""
        self.postal_code = "M5V 3A8"
    
    @task(3)
    def search_products(self):
        """Simulate product search"""
        search_terms = ["milk", "bread", "chicken", "apples", "pasta"]
        term = self.environment.parsed_options.random.choice(search_terms)
        
        self.client.get(
            "/api/products/search",
            params={"q": term, "postal_code": self.postal_code}
        )
    
    @task(2)
    def find_stores(self):
        """Simulate store lookup"""
        self.client.get(
            "/api/stores/nearby",
            params={"postal_code": self.postal_code}
        )
    
    @task(1)
    def health_check(self):
        """Simulate health check"""
        self.client.get("/api/health")

# Run with: locust -f locustfile.py --host=http://localhost:5002
```

### Test Coverage Configuration

#### Frontend Coverage (Vitest)
```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    }
  }
})
```

#### Backend Coverage (pytest-cov)
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

## ⚡ Performance Optimization

### Frontend Optimization

#### Code Splitting and Lazy Loading
```javascript
// Lazy load heavy components
const ProductComparison = lazy(() => import('./components/ProductComparison'))
const StoreMap = lazy(() => import('./components/StoreMap'))

// Route-based code splitting
const routes = [
  {
    path: '/',
    component: lazy(() => import('./pages/Home'))
  },
  {
    path: '/search',
    component: lazy(() => import('./pages/Search'))
  }
]
```

#### Image Optimization
```javascript
// Responsive image component
const OptimizedImage = ({ src, alt, sizes }) => (
  <picture>
    <source 
      media="(max-width: 640px)" 
      srcSet={`${src}?w=640&q=75`} 
    />
    <source 
      media="(max-width: 1024px)" 
      srcSet={`${src}?w=1024&q=80`} 
    />
    <img 
      src={`${src}?w=1200&q=85`} 
      alt={alt}
      loading="lazy"
      decoding="async"
    />
  </picture>
)
```

#### API Request Optimization
```javascript
// Request debouncing for search
const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value)
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)
    
    return () => clearTimeout(handler)
  }, [value, delay])
  
  return debouncedValue
}

// Memoized API calls
const searchProducts = useMemo(() => 
  debounce(async (query, postalCode) => {
    if (query.length < 2) return []
    
    const response = await fetch(
      `/api/products/search?q=${encodeURIComponent(query)}&postal_code=${postalCode}`
    )
    return response.json()
  }, 300),
  []
)
```

### Backend Optimization

#### Database Query Optimization
```python
# Optimized product search with eager loading
def search_products_optimized(query, postal_code=None, limit=20):
    """Optimized product search with minimal database queries"""
    
    # Use database indexes for fast text search
    search_query = db.session.query(Product).join(Price).join(Store)
    
    # Add text search conditions
    search_terms = query.lower().split()
    for term in search_terms:
        search_query = search_query.filter(
            db.or_(
                Product.name.ilike(f'%{term}%'),
                Product.brand.ilike(f'%{term}%')
            )
        )
    
    # Eager load related data to avoid N+1 queries
    search_query = search_query.options(
        joinedload(Product.prices).joinedload(Price.store),
        joinedload(Product.category)
    )
    
    # Apply location filter if postal code provided
    if postal_code:
        coordinates = get_coordinates_from_postal_code(postal_code)
        if coordinates:
            search_query = search_query.filter(
                calculate_distance(
                    Store.latitude, Store.longitude,
                    coordinates['lat'], coordinates['lng']
                ) <= 25  # 25km radius
            )
    
    # Limit results and execute query
    products = search_query.limit(limit * 2).all()  # Get extra for deduplication
    
    return products

# Database connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

#### Caching Strategy
```python
# Redis caching for expensive operations
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=3600):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(
                cache_key, 
                expiration, 
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator

# Cache expensive product searches
@cache_result(expiration=1800)  # 30 minutes
def search_products_cached(query, postal_code, limit):
    return search_products_optimized(query, postal_code, limit)

# Cache store lookups
@cache_result(expiration=3600)  # 1 hour
def get_nearby_stores_cached(postal_code, radius):
    return get_nearby_stores(postal_code, radius)
```

#### API Response Compression
```python
from flask_compress import Compress

# Enable gzip compression
compress = Compress()
compress.init_app(app)

# Custom compression for large responses
@app.after_request
def compress_response(response):
    if (response.content_length and 
        response.content_length > 1000 and
        'gzip' in request.headers.get('Accept-Encoding', '')):
        
        response.headers['Content-Encoding'] = 'gzip'
        response.data = gzip.compress(response.data)
    
    return response
```

### Database Optimization

#### Index Strategy
```sql
-- Composite indexes for common query patterns
CREATE INDEX idx_product_search_composite ON product(name, brand, category);
CREATE INDEX idx_price_store_product ON price(store_id, product_id, current_price);
CREATE INDEX idx_store_location ON store(latitude, longitude, postal_code);

-- Partial indexes for filtered queries
CREATE INDEX idx_price_on_sale ON price(product_id, current_price) WHERE on_sale = true;
CREATE INDEX idx_product_organic ON product(name, brand) WHERE organic = true;

-- Text search indexes (PostgreSQL)
CREATE INDEX idx_product_name_gin ON product USING gin(to_tsvector('english', name));
CREATE INDEX idx_product_brand_gin ON product USING gin(to_tsvector('english', brand));
```

#### Query Optimization Examples
```sql
-- Optimized product search query
EXPLAIN ANALYZE
SELECT DISTINCT p.id, p.name, p.brand, 
       MIN(pr.current_price) as min_price,
       COUNT(DISTINCT pr.store_id) as store_count
FROM product p
JOIN price pr ON p.id = pr.product_id
JOIN store s ON pr.store_id = s.id
WHERE p.name ILIKE '%milk%'
  AND s.latitude BETWEEN 43.6 AND 43.7
  AND s.longitude BETWEEN -79.4 AND -79.3
GROUP BY p.id, p.name, p.brand
HAVING COUNT(DISTINCT pr.store_id) >= 2
ORDER BY min_price ASC
LIMIT 20;

-- Optimized store proximity query
EXPLAIN ANALYZE
SELECT s.id, s.name, s.address,
       (6371 * acos(cos(radians(43.6426)) * cos(radians(s.latitude)) * 
        cos(radians(s.longitude) - radians(-79.3871)) + 
        sin(radians(43.6426)) * sin(radians(s.latitude)))) AS distance
FROM store s
WHERE (6371 * acos(cos(radians(43.6426)) * cos(radians(s.latitude)) * 
       cos(radians(s.longitude) - radians(-79.3871)) + 
       sin(radians(43.6426)) * sin(radians(s.latitude)))) <= 10
ORDER BY distance
LIMIT 10;
```

## 🔒 Security Considerations

### Input Validation and Sanitization

#### Frontend Input Validation
```javascript
// Postal code validation
const validatePostalCode = (postalCode) => {
  const canadianPostalRegex = /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/
  return canadianPostalRegex.test(postalCode.trim())
}

// Search query sanitization
const sanitizeSearchQuery = (query) => {
  // Remove potentially dangerous characters
  const sanitized = query
    .replace(/[<>\"']/g, '')  // Remove HTML/script injection chars
    .replace(/[;]/g, '')      // Remove SQL injection chars
    .trim()
  
  // Limit length
  return sanitized.substring(0, 100)
}

// XSS prevention in display
const SafeText = ({ children }) => {
  const sanitizedText = DOMPurify.sanitize(children)
  return <span dangerouslySetInnerHTML={{ __html: sanitizedText }} />
}
```

#### Backend Input Validation
```python
from marshmallow import Schema, fields, validate, ValidationError
import re

class PostalCodeSchema(Schema):
    postal_code = fields.Str(
        required=True,
        validate=[
            validate.Length(min=7, max=7),
            validate.Regexp(
                r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$',
                error='Invalid Canadian postal code format'
            )
        ]
    )

class ProductSearchSchema(Schema):
    q = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100),
            validate.Regexp(
                r'^[a-zA-Z0-9\s\-\'\"\.]+$',
                error='Search query contains invalid characters'
            )
        ]
    )
    postal_code = fields.Str(validate=validate_postal_code)
    limit = fields.Int(validate=validate.Range(min=1, max=50))

def validate_input(schema_class):
    """Decorator for input validation"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            try:
                validated_data = schema.load(request.args)
                return func(validated_data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({
                    'error': 'Validation Error',
                    'details': err.messages
                }), 400
        return wrapper
    return decorator

@products_bp.route('/search', methods=['GET'])
@validate_input(ProductSearchSchema)
def search_products(validated_data):
    """Search products with validated input"""
    # Input is already validated and sanitized
    query = validated_data['q']
    postal_code = validated_data.get('postal_code')
    limit = validated_data.get('limit', 20)
    
    # Proceed with business logic
    results = matcher_service.search_products(query, postal_code, limit)
    return jsonify(results)
```

### SQL Injection Prevention

#### Parameterized Queries
```python
# SECURE: Using SQLAlchemy ORM (automatically parameterized)
def search_products_secure(query_terms):
    products = db.session.query(Product).filter(
        Product.name.ilike(f'%{query_terms}%')  # SQLAlchemy handles escaping
    ).all()
    return products

# SECURE: Raw SQL with parameters
def search_products_raw_secure(query_terms):
    sql = """
        SELECT p.id, p.name, p.brand 
        FROM product p 
        WHERE p.name ILIKE %s
    """
    result = db.session.execute(sql, (f'%{query_terms}%',))
    return result.fetchall()

# INSECURE: String concatenation (DON'T DO THIS)
def search_products_insecure(query_terms):
    sql = f"SELECT * FROM product WHERE name LIKE '%{query_terms}%'"
    # This is vulnerable to SQL injection!
    return db.session.execute(sql)
```

### API Security Headers

#### Security Headers Configuration
```python
from flask_talisman import Talisman

# Configure security headers
talisman = Talisman(
    app,
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'connect-src': "'self' https://api.grocerycompare.ca"
    }
)

@app.after_request
def add_security_headers(response):
    """Add additional security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

### Rate Limiting

#### API Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Apply rate limits to specific endpoints
@products_bp.route('/search', methods=['GET'])
@limiter.limit("50 per minute")
def search_products():
    """Rate-limited product search"""
    # Implementation here
    pass

@stores_bp.route('/nearby', methods=['GET'])
@limiter.limit("30 per minute")
def get_nearby_stores():
    """Rate-limited store lookup"""
    # Implementation here
    pass

# Custom rate limit handler
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.',
        'retry_after': e.retry_after
    }), 429
```

### Data Privacy Protection

#### Personal Data Handling
```python
class PrivacyCompliantLogger:
    """Logger that automatically redacts sensitive information"""
    
    SENSITIVE_PATTERNS = [
        r'[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d',  # Postal codes
        r'\b\d{3}-\d{3}-\d{4}\b',            # Phone numbers
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Emails
    ]
    
    def log_request(self, request_data):
        """Log request with sensitive data redacted"""
        sanitized_data = self.redact_sensitive_data(request_data)
        logger.info(f"API Request: {sanitized_data}")
    
    def redact_sensitive_data(self, data):
        """Redact sensitive information from log data"""
        redacted = str(data)
        for pattern in self.SENSITIVE_PATTERNS:
            redacted = re.sub(pattern, '[REDACTED]', redacted)
        return redacted

# GDPR-compliant data retention
class DataRetentionManager:
    """Manage data retention according to privacy regulations"""
    
    def cleanup_old_data(self):
        """Remove data older than retention period"""
        retention_days = 30
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Remove old search logs
        db.session.query(SearchLog).filter(
            SearchLog.created_at < cutoff_date
        ).delete()
        
        # Remove old price data (keep only latest)
        old_prices = db.session.query(Price).filter(
            Price.last_updated < cutoff_date
        ).filter(
            ~Price.id.in_(
                db.session.query(func.max(Price.id))
                .group_by(Price.product_id, Price.store_id)
                .subquery()
            )
        ).delete()
        
        db.session.commit()
```

### Environment Security

#### Secrets Management
```python
import os
from cryptography.fernet import Fernet

class SecureConfig:
    """Secure configuration management"""
    
    def __init__(self):
        self.encryption_key = os.environ.get('ENCRYPTION_KEY')
        if not self.encryption_key:
            raise ValueError("ENCRYPTION_KEY environment variable required")
        
        self.cipher = Fernet(self.encryption_key.encode())
    
    def get_secret(self, key):
        """Get decrypted secret from environment"""
        encrypted_value = os.environ.get(key)
        if not encrypted_value:
            return None
        
        try:
            return self.cipher.decrypt(encrypted_value.encode()).decode()
        except Exception:
            raise ValueError(f"Failed to decrypt secret: {key}")
    
    @property
    def database_url(self):
        return self.get_secret('DATABASE_URL_ENCRYPTED')
    
    @property
    def secret_key(self):
        return self.get_secret('SECRET_KEY_ENCRYPTED')

# Production configuration
class ProductionConfig:
    SECRET_KEY = SecureConfig().secret_key
    DATABASE_URL = SecureConfig().database_url
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
```

## 📊 Monitoring and Logging

### Application Monitoring

#### Health Check Implementation
```python
import psutil
from datetime import datetime, timedelta

class HealthMonitor:
    """Comprehensive application health monitoring"""
    
    def __init__(self):
        self.start_time = datetime.now()
    
    def get_health_status(self):
        """Get comprehensive health status"""
        return {
            'status': self.get_overall_status(),
            'timestamp': datetime.utcnow().isoformat(),
            'uptime': self.get_uptime(),
            'version': '1.0.0',
            'components': {
                'database': self.check_database_health(),
                'external_apis': self.check_external_apis(),
                'system_resources': self.check_system_resources(),
                'cache': self.check_cache_health()
            }
        }
    
    def get_overall_status(self):
        """Determine overall application status"""
        components = [
            self.check_database_health(),
            self.check_system_resources(),
            self.check_cache_health()
        ]
        
        if all(c['status'] == 'healthy' for c in components):
            return 'healthy'
        elif any(c['status'] == 'critical' for c in components):
            return 'critical'
        else:
            return 'degraded'
    
    def check_database_health(self):
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            db.session.execute('SELECT 1')
            response_time = (time.time() - start_time) * 1000
            
            if response_time > 1000:  # > 1 second
                return {'status': 'degraded', 'response_time_ms': response_time}
            else:
                return {'status': 'healthy', 'response_time_ms': response_time}
                
        except Exception as e:
            return {'status': 'critical', 'error': str(e)}
    
    def check_system_resources(self):
        """Check system resource usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = 'healthy'
        if cpu_percent > 80 or memory.percent > 85 or disk.percent > 90:
            status = 'degraded'
        if cpu_percent > 95 or memory.percent > 95 or disk.percent > 95:
            status = 'critical'
        
        return {
            'status': status,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent
        }
    
    def get_uptime(self):
        """Get application uptime"""
        uptime = datetime.now() - self.start_time
        return str(uptime)

# Health check endpoint
@app.route('/api/health')
def health_check():
    health_monitor = HealthMonitor()
    health_data = health_monitor.get_health_status()
    
    status_code = 200
    if health_data['status'] == 'critical':
        status_code = 503
    elif health_data['status'] == 'degraded':
        status_code = 200  # Still serving requests
    
    return jsonify(health_data), status_code
```

### Structured Logging

#### Logging Configuration
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured JSON logging for better observability"""
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # JSON formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for production
        if os.environ.get('FLASK_ENV') == 'production':
            file_handler = logging.FileHandler('app.log')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def log_api_request(self, request, response_time=None, status_code=None):
        """Log API request with structured data"""
        log_data = {
            'event_type': 'api_request',
            'timestamp': datetime.utcnow().isoformat(),
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.args),
            'user_agent': request.headers.get('User-Agent'),
            'ip_address': request.remote_addr,
            'response_time_ms': response_time,
            'status_code': status_code
        }
        
        self.logger.info(json.dumps(log_data))
    
    def log_error(self, error, context=None):
        """Log error with context"""
        log_data = {
            'event_type': 'error',
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {}
        }
        
        self.logger.error(json.dumps(log_data))
    
    def log_business_event(self, event_type, data):
        """Log business events for analytics"""
        log_data = {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        
        self.logger.info(json.dumps(log_data))

# Request logging middleware
@app.before_request
def log_request_start():
    g.start_time = time.time()

@app.after_request
def log_request_end(response):
    response_time = (time.time() - g.start_time) * 1000
    
    logger = StructuredLogger('api')
    logger.log_api_request(
        request, 
        response_time=response_time,
        status_code=response.status_code
    )
    
    return response
```

### Performance Monitoring

#### Application Performance Monitoring
```python
import time
from functools import wraps

class PerformanceMonitor:
    """Monitor application performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'request_count': 0,
            'total_response_time': 0,
            'error_count': 0,
            'endpoint_metrics': {}
        }
    
    def record_request(self, endpoint, response_time, status_code):
        """Record request metrics"""
        self.metrics['request_count'] += 1
        self.metrics['total_response_time'] += response_time
        
        if status_code >= 400:
            self.metrics['error_count'] += 1
        
        # Endpoint-specific metrics
        if endpoint not in self.metrics['endpoint_metrics']:
            self.metrics['endpoint_metrics'][endpoint] = {
                'count': 0,
                'total_time': 0,
                'errors': 0
            }
        
        endpoint_metrics = self.metrics['endpoint_metrics'][endpoint]
        endpoint_metrics['count'] += 1
        endpoint_metrics['total_time'] += response_time
        
        if status_code >= 400:
            endpoint_metrics['errors'] += 1
    
    def get_metrics_summary(self):
        """Get performance metrics summary"""
        if self.metrics['request_count'] == 0:
            return {'message': 'No requests recorded'}
        
        avg_response_time = (
            self.metrics['total_response_time'] / 
            self.metrics['request_count']
        )
        
        error_rate = (
            self.metrics['error_count'] / 
            self.metrics['request_count'] * 100
        )
        
        return {
            'total_requests': self.metrics['request_count'],
            'average_response_time_ms': round(avg_response_time, 2),
            'error_rate_percent': round(error_rate, 2),
            'endpoints': self.get_endpoint_metrics()
        }
    
    def get_endpoint_metrics(self):
        """Get per-endpoint performance metrics"""
        endpoint_summary = {}
        
        for endpoint, metrics in self.metrics['endpoint_metrics'].items():
            if metrics['count'] > 0:
                avg_time = metrics['total_time'] / metrics['count']
                error_rate = (metrics['errors'] / metrics['count']) * 100
                
                endpoint_summary[endpoint] = {
                    'requests': metrics['count'],
                    'avg_response_time_ms': round(avg_time, 2),
                    'error_rate_percent': round(error_rate, 2)
                }
        
        return endpoint_summary

# Performance monitoring decorator
def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            status_code = getattr(result, 'status_code', 200)
        except Exception as e:
            status_code = 500
            raise
        finally:
            response_time = (time.time() - start_time) * 1000
            
            # Record metrics
            performance_monitor.record_request(
                func.__name__,
                response_time,
                status_code
            )
        
        return result
    return wrapper

# Metrics endpoint
@app.route('/api/metrics')
@monitor_performance
def get_metrics():
    """Get application performance metrics"""
    return jsonify(performance_monitor.get_metrics_summary())
```

### Error Tracking

#### Error Handling and Reporting
```python
import traceback
from datetime import datetime

class ErrorTracker:
    """Track and report application errors"""
    
    def __init__(self):
        self.errors = []
        self.error_counts = {}
    
    def record_error(self, error, context=None):
        """Record error occurrence"""
        error_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        self.errors.append(error_data)
        
        # Keep only last 100 errors
        if len(self.errors) > 100:
            self.errors.pop(0)
        
        # Count error types
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Log error
        logger = StructuredLogger('error_tracker')
        logger.log_error(error, context)
    
    def get_error_summary(self):
        """Get error summary statistics"""
        return {
            'total_errors': len(self.errors),
            'error_types': self.error_counts,
            'recent_errors': self.errors[-10:] if self.errors else []
        }

# Global error handler
@app.errorhandler(Exception)
def handle_exception(error):
    """Global exception handler"""
    error_tracker.record_error(error, {
        'endpoint': request.endpoint,
        'method': request.method,
        'path': request.path,
        'args': dict(request.args)
    })
    
    # Return appropriate error response
    if isinstance(error, ValidationError):
        return jsonify({
            'error': 'Validation Error',
            'message': str(error)
        }), 400
    else:
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

# Error reporting endpoint
@app.route('/api/errors')
def get_error_summary():
    """Get error summary for monitoring"""
    return jsonify(error_tracker.get_error_summary())
```

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### Frontend Issues

##### Issue: "Network Error" when calling API
**Symptoms:**
- API calls fail with network errors
- CORS errors in browser console
- 404 errors for API endpoints

**Solutions:**
```javascript
// 1. Check API base URL configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://api.grocerycompare.ca/api'
  : 'http://localhost:5002/api'

// 2. Verify CORS configuration in backend
// 3. Check if backend server is running
// 4. Validate API endpoint URLs

// Debug API calls
const debugApiCall = async (url, options = {}) => {
  console.log('API Call:', url, options)
  
  try {
    const response = await fetch(url, options)
    console.log('Response Status:', response.status)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('API Error:', errorText)
      throw new Error(`API Error: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('Response Data:', data)
    return data
    
  } catch (error) {
    console.error('Network Error:', error)
    throw error
  }
}
```

##### Issue: Slow page loading or poor performance
**Symptoms:**
- Long initial page load times
- Sluggish interactions
- High memory usage

**Solutions:**
```javascript
// 1. Implement code splitting
const LazyComponent = lazy(() => import('./HeavyComponent'))

// 2. Optimize images
const OptimizedImage = ({ src, alt }) => (
  <img 
    src={src} 
    alt={alt} 
    loading="lazy"
    decoding="async"
  />
)

// 3. Debounce expensive operations
const debouncedSearch = useCallback(
  debounce((query) => {
    performSearch(query)
  }, 300),
  []
)

// 4. Use React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  // Component implementation
})
```

#### Backend Issues

##### Issue: Database connection errors
**Symptoms:**
- "Connection refused" errors
- Timeout errors on database operations
- SQLAlchemy connection pool errors

**Solutions:**
```python
# 1. Check database connection string
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# 2. Test database connectivity
def test_database_connection():
    try:
        db.session.execute('SELECT 1')
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")

# 3. Configure connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

# 4. Add connection retry logic
def execute_with_retry(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return db.session.execute(query)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

##### Issue: High memory usage or memory leaks
**Symptoms:**
- Gradually increasing memory usage
- Out of memory errors
- Slow response times

**Solutions:**
```python
# 1. Properly close database sessions
@app.teardown_appcontext
def close_db_session(error):
    db.session.remove()

# 2. Limit query result sizes
def search_products_limited(query, limit=50):
    # Always limit query results
    return Product.query.filter(
        Product.name.ilike(f'%{query}%')
    ).limit(min(limit, 100)).all()

# 3. Use pagination for large datasets
def get_products_paginated(page=1, per_page=20):
    return Product.query.paginate(
        page=page,
        per_page=min(per_page, 100),
        error_out=False
    )

# 4. Clear large objects from memory
def process_large_dataset(data):
    try:
        # Process data
        result = expensive_operation(data)
        return result
    finally:
        # Clear references to large objects
        del data
        gc.collect()
```

#### Web Scraping Issues

##### Issue: Scrapers getting blocked or returning empty results
**Symptoms:**
- HTTP 403/429 errors
- Empty or incomplete data
- IP address blocking

**Solutions:**
```python
# 1. Implement proper delays and randomization
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY_RANGE = (1, 3)

# 2. Rotate user agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

# 3. Respect robots.txt
ROBOTSTXT_OBEY = True

# 4. Implement retry logic
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 5. Use proxy rotation if necessary
class ProxyMiddleware:
    def process_request(self, request, spider):
        if hasattr(spider, 'use_proxy') and spider.use_proxy:
            proxy = self.get_random_proxy()
            request.meta['proxy'] = proxy
```

### Debugging Tools and Techniques

#### Frontend Debugging
```javascript
// 1. React Developer Tools
// Install React DevTools browser extension

// 2. Performance profiling
const ProfiledComponent = React.memo(({ data }) => {
  console.time('ComponentRender')
  
  const result = expensiveCalculation(data)
  
  console.timeEnd('ComponentRender')
  return <div>{result}</div>
})

// 3. API call debugging
const apiClient = {
  async get(url, options = {}) {
    const startTime = performance.now()
    
    try {
      const response = await fetch(url, options)
      const endTime = performance.now()
      
      console.log(`API Call: ${url} took ${endTime - startTime}ms`)
      return response
    } catch (error) {
      console.error(`API Call failed: ${url}`, error)
      throw error
    }
  }
}

// 4. State debugging
const useDebugState = (stateName, state) => {
  useEffect(() => {
    console.log(`${stateName} changed:`, state)
  }, [stateName, state])
}
```

#### Backend Debugging
```python
# 1. SQL query debugging
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# 2. Performance profiling
import cProfile
import pstats

def profile_function(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return result
    return wrapper

# 3. Memory debugging
import tracemalloc

def debug_memory_usage():
    tracemalloc.start()
    
    # Your code here
    
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
    tracemalloc.stop()

# 4. Request debugging middleware
@app.before_request
def debug_request():
    if app.debug:
        print(f"Request: {request.method} {request.path}")
        print(f"Args: {dict(request.args)}")
        print(f"Headers: {dict(request.headers)}")
```

### Performance Troubleshooting

#### Database Performance Issues
```sql
-- 1. Identify slow queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- 2. Check index usage
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE tablename = 'product'
ORDER BY n_distinct DESC;

-- 3. Analyze query execution plans
EXPLAIN ANALYZE
SELECT p.name, MIN(pr.current_price)
FROM product p
JOIN price pr ON p.id = pr.product_id
WHERE p.name ILIKE '%milk%'
GROUP BY p.id, p.name;

-- 4. Check for missing indexes
SELECT schemaname, tablename, attname
FROM pg_stats
WHERE n_distinct > 100
  AND correlation < 0.1
  AND tablename IN ('product', 'price', 'store');
```

#### API Performance Issues
```python
# 1. Add request timing middleware
@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_timing(response):
    duration = time.time() - g.start_time
    if duration > 1.0:  # Log slow requests
        logger.warning(f"Slow request: {request.path} took {duration:.2f}s")
    return response

# 2. Profile specific endpoints
from werkzeug.middleware.profiler import ProfilerMiddleware

if app.debug:
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app,
        restrictions=[30],  # Show top 30 functions
        profile_dir='./profiles'
    )

# 3. Monitor database query counts
class QueryCountDebugger:
    def __init__(self):
        self.query_count = 0
    
    def __call__(self, execute, sql, parameters, context, executemany):
        self.query_count += 1
        return execute(sql, parameters, context)

# Add to SQLAlchemy events
from sqlalchemy import event
query_debugger = QueryCountDebugger()
event.listen(db.engine, "before_cursor_execute", query_debugger)
```

---

**This technical documentation provides comprehensive guidance for developers working with the GroceryCompare system. For additional support or clarification on any technical aspects, please refer to the inline code comments and accompanying user documentation.**


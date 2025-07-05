# API Specification & Database Schema
## Grocery Price Comparison Platform

**Author:** Manus AI  
**Date:** January 2025  
**Version:** 1.0

---

## API Endpoints Specification

### Base URL
- **Development:** `http://localhost:8000/api/v1`
- **Production:** `https://api.grocerycompare.ca/v1`

### Authentication
All API endpoints use JWT token authentication for user-specific features. Public endpoints for basic price comparison do not require authentication.

#### Authentication Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Core API Endpoints

#### 1. Location Services

##### GET /locations/postal-code/{postal_code}
Validates postal code and returns geographic information with nearby stores.

**Parameters:**
- `postal_code` (string): Canadian postal code (format: A1A 1A1)

**Response:**
```json
{
  "postal_code": "M5V 3A8",
  "city": "Toronto",
  "province": "ON",
  "latitude": 43.6426,
  "longitude": -79.3871,
  "nearby_stores": [
    {
      "store_id": "walmart_123",
      "chain_name": "Walmart",
      "store_name": "Walmart Supercentre",
      "address": "123 Queen St W, Toronto, ON M5V 3A8",
      "distance_km": 1.2,
      "phone": "(416) 555-0123",
      "hours": {
        "monday": "7:00-23:00",
        "tuesday": "7:00-23:00",
        "wednesday": "7:00-23:00",
        "thursday": "7:00-23:00",
        "friday": "7:00-23:00",
        "saturday": "7:00-23:00",
        "sunday": "8:00-22:00"
      }
    }
  ]
}
```

##### GET /locations/stores
Returns all stores within a specified radius of coordinates.

**Query Parameters:**
- `latitude` (float): Latitude coordinate
- `longitude` (float): Longitude coordinate  
- `radius_km` (float): Search radius in kilometers (default: 10, max: 50)
- `chains` (string[]): Filter by grocery chain names (optional)

#### 2. Product Services

##### GET /products/search
Searches for products across all stores with fuzzy matching.

**Query Parameters:**
- `query` (string): Product search term
- `postal_code` (string): User's postal code for local results
- `category` (string): Product category filter (optional)
- `limit` (int): Maximum results to return (default: 20, max: 100)

**Response:**
```json
{
  "query": "organic milk",
  "results": [
    {
      "product_id": "prod_456",
      "name": "Organic Valley Whole Milk 1L",
      "brand": "Organic Valley",
      "category": "Dairy",
      "size": "1L",
      "unit_type": "volume",
      "image_url": "https://cdn.grocerycompare.ca/products/organic_valley_milk.jpg",
      "nutrition_info": {
        "calories_per_100ml": 61,
        "fat_g": 3.25,
        "protein_g": 3.15
      },
      "prices": [
        {
          "store_id": "loblaws_456",
          "store_name": "Loblaws",
          "current_price": 5.99,
          "regular_price": 6.49,
          "on_sale": true,
          "sale_end_date": "2025-01-15",
          "price_per_unit": 5.99,
          "last_updated": "2025-01-07T10:30:00Z"
        }
      ]
    }
  ],
  "total_results": 15,
  "search_time_ms": 45
}
```

##### GET /products/{product_id}
Returns detailed information for a specific product.

**Response:**
```json
{
  "product_id": "prod_456",
  "name": "Organic Valley Whole Milk 1L",
  "brand": "Organic Valley",
  "category": "Dairy",
  "subcategory": "Milk",
  "size": "1L",
  "unit_type": "volume",
  "barcode": "123456789012",
  "ingredients": ["Organic milk", "Vitamin D3"],
  "allergens": ["Milk"],
  "nutrition_info": {
    "serving_size": "250ml",
    "calories": 150,
    "fat_g": 8,
    "saturated_fat_g": 5,
    "cholesterol_mg": 30,
    "sodium_mg": 125,
    "carbohydrates_g": 12,
    "sugars_g": 12,
    "protein_g": 8,
    "calcium_mg": 300,
    "vitamin_d_iu": 120
  },
  "image_urls": [
    "https://cdn.grocerycompare.ca/products/organic_valley_milk_front.jpg",
    "https://cdn.grocerycompare.ca/products/organic_valley_milk_nutrition.jpg"
  ],
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-07T10:30:00Z"
}
```

##### GET /products/categories
Returns hierarchical product categories.

**Response:**
```json
{
  "categories": [
    {
      "id": "dairy",
      "name": "Dairy & Eggs",
      "subcategories": [
        {
          "id": "milk",
          "name": "Milk",
          "product_count": 156
        },
        {
          "id": "cheese",
          "name": "Cheese",
          "product_count": 342
        }
      ]
    }
  ]
}
```

#### 3. Price Comparison Services

##### GET /prices/compare
Compares prices for a specific product across multiple stores.

**Query Parameters:**
- `product_id` (string): Product identifier
- `postal_code` (string): User's postal code
- `radius_km` (float): Search radius (default: 10)

**Response:**
```json
{
  "product": {
    "product_id": "prod_456",
    "name": "Organic Valley Whole Milk 1L",
    "brand": "Organic Valley"
  },
  "price_comparison": [
    {
      "store_id": "loblaws_456",
      "chain_name": "Loblaws",
      "store_name": "Loblaws City Market",
      "address": "123 Queen St W, Toronto, ON",
      "distance_km": 1.2,
      "current_price": 5.99,
      "regular_price": 6.49,
      "on_sale": true,
      "sale_end_date": "2025-01-15",
      "savings": 0.50,
      "price_per_unit": 5.99,
      "stock_status": "in_stock",
      "last_updated": "2025-01-07T10:30:00Z"
    },
    {
      "store_id": "metro_789",
      "chain_name": "Metro",
      "store_name": "Metro Downtown",
      "address": "456 King St W, Toronto, ON",
      "distance_km": 0.8,
      "current_price": 6.29,
      "regular_price": 6.29,
      "on_sale": false,
      "savings": 0.00,
      "price_per_unit": 6.29,
      "stock_status": "in_stock",
      "last_updated": "2025-01-07T09:15:00Z"
    }
  ],
  "best_price": {
    "store_id": "loblaws_456",
    "price": 5.99,
    "savings_vs_highest": 0.30
  },
  "average_price": 6.14,
  "price_range": {
    "min": 5.99,
    "max": 6.29
  }
}
```

##### GET /prices/history/{product_id}
Returns price history for a product across stores.

**Query Parameters:**
- `days` (int): Number of days of history (default: 30, max: 365)
- `store_ids` (string[]): Filter by specific stores (optional)

#### 4. Store Services

##### GET /stores/{store_id}
Returns detailed information for a specific store.

**Response:**
```json
{
  "store_id": "loblaws_456",
  "chain_name": "Loblaws",
  "store_name": "Loblaws City Market",
  "address": {
    "street": "123 Queen St W",
    "city": "Toronto",
    "province": "ON",
    "postal_code": "M5V 3A8"
  },
  "coordinates": {
    "latitude": 43.6426,
    "longitude": -79.3871
  },
  "contact": {
    "phone": "(416) 555-0123",
    "website": "https://www.loblaws.ca/stores/123"
  },
  "hours": {
    "monday": "7:00-23:00",
    "tuesday": "7:00-23:00",
    "wednesday": "7:00-23:00",
    "thursday": "7:00-23:00",
    "friday": "7:00-23:00",
    "saturday": "7:00-23:00",
    "sunday": "8:00-22:00"
  },
  "services": [
    "pharmacy",
    "bakery",
    "deli",
    "floral",
    "photo_center"
  ],
  "features": [
    "wheelchair_accessible",
    "parking_available",
    "click_and_collect"
  ]
}
```

##### GET /stores/chains
Returns information about all supported grocery chains.

#### 5. User Services (Authenticated)

##### POST /users/preferences
Saves user preferences for location and product categories.

**Request Body:**
```json
{
  "default_postal_code": "M5V 3A8",
  "preferred_stores": ["loblaws_456", "metro_789"],
  "dietary_restrictions": ["vegetarian", "gluten_free"],
  "favorite_categories": ["dairy", "produce", "bakery"],
  "price_alert_threshold": 0.20
}
```

##### GET /users/search-history
Returns user's recent product searches.

##### POST /users/price-alerts
Creates price alert for a specific product.

**Request Body:**
```json
{
  "product_id": "prod_456",
  "target_price": 5.50,
  "stores": ["loblaws_456", "metro_789"],
  "notification_method": "email"
}
```

## Database Schema

### Core Tables

#### stores
```sql
CREATE TABLE stores (
    store_id VARCHAR(50) PRIMARY KEY,
    chain_id VARCHAR(20) NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    address_street VARCHAR(200) NOT NULL,
    address_city VARCHAR(50) NOT NULL,
    address_province CHAR(2) NOT NULL,
    postal_code VARCHAR(7) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    phone VARCHAR(20),
    website_url VARCHAR(200),
    hours JSONB,
    services TEXT[],
    features TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_stores_postal_code ON stores (postal_code);
CREATE INDEX idx_stores_location ON stores USING GIST (
    ll_to_earth(latitude, longitude)
);
CREATE INDEX idx_stores_chain ON stores (chain_id);
```

#### grocery_chains
```sql
CREATE TABLE grocery_chains (
    chain_id VARCHAR(20) PRIMARY KEY,
    chain_name VARCHAR(50) NOT NULL,
    logo_url VARCHAR(200),
    website_url VARCHAR(200),
    corporate_info JSONB,
    scraping_config JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### products
```sql
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    brand VARCHAR(100),
    category_id VARCHAR(20) NOT NULL,
    subcategory_id VARCHAR(20),
    size VARCHAR(50),
    unit_type VARCHAR(20),
    barcode VARCHAR(20),
    ingredients TEXT[],
    allergens TEXT[],
    nutrition_info JSONB,
    image_urls TEXT[],
    attributes JSONB,
    search_vector tsvector,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products (category_id);
CREATE INDEX idx_products_brand ON products (brand);
CREATE INDEX idx_products_search ON products USING GIN (search_vector);
CREATE INDEX idx_products_barcode ON products (barcode) WHERE barcode IS NOT NULL;
```

#### product_categories
```sql
CREATE TABLE product_categories (
    category_id VARCHAR(20) PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    parent_category_id VARCHAR(20),
    description TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true
);
```

#### prices
```sql
CREATE TABLE prices (
    price_id BIGSERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    store_id VARCHAR(50) NOT NULL,
    current_price DECIMAL(8, 2) NOT NULL,
    regular_price DECIMAL(8, 2),
    on_sale BOOLEAN DEFAULT false,
    sale_start_date DATE,
    sale_end_date DATE,
    price_per_unit DECIMAL(8, 2),
    stock_status VARCHAR(20) DEFAULT 'unknown',
    data_source VARCHAR(50) NOT NULL,
    scraped_at TIMESTAMP WITH TIME ZONE NOT NULL,
    valid_from TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    valid_to TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

CREATE INDEX idx_prices_product_store ON prices (product_id, store_id);
CREATE INDEX idx_prices_valid_period ON prices (valid_from, valid_to);
CREATE INDEX idx_prices_scraped_at ON prices (scraped_at);
CREATE INDEX idx_prices_current ON prices (product_id, store_id, valid_to) 
    WHERE valid_to IS NULL;
```

#### price_history
```sql
CREATE TABLE price_history (
    history_id BIGSERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    store_id VARCHAR(50) NOT NULL,
    price DECIMAL(8, 2) NOT NULL,
    date DATE NOT NULL,
    data_source VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

CREATE INDEX idx_price_history_product_date ON price_history (product_id, date);
CREATE INDEX idx_price_history_store_date ON price_history (store_id, date);
```

### User Management Tables

#### users
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    default_postal_code VARCHAR(7),
    preferences JSONB,
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_postal_code ON users (default_postal_code);
```

#### user_searches
```sql
CREATE TABLE user_searches (
    search_id BIGSERIAL PRIMARY KEY,
    user_id UUID,
    search_query VARCHAR(200) NOT NULL,
    postal_code VARCHAR(7),
    results_count INTEGER,
    search_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_user_searches_user_timestamp ON user_searches (user_id, search_timestamp);
```

#### price_alerts
```sql
CREATE TABLE price_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    target_price DECIMAL(8, 2) NOT NULL,
    store_ids TEXT[],
    notification_method VARCHAR(20) DEFAULT 'email',
    is_active BOOLEAN DEFAULT true,
    last_triggered TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

### Data Collection Tables

#### scraping_jobs
```sql
CREATE TABLE scraping_jobs (
    job_id BIGSERIAL PRIMARY KEY,
    chain_id VARCHAR(20) NOT NULL,
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    products_scraped INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    error_details JSONB,
    
    FOREIGN KEY (chain_id) REFERENCES grocery_chains(chain_id)
);

CREATE INDEX idx_scraping_jobs_status ON scraping_jobs (status);
CREATE INDEX idx_scraping_jobs_chain_date ON scraping_jobs (chain_id, started_at);
```

#### scraping_errors
```sql
CREATE TABLE scraping_errors (
    error_id BIGSERIAL PRIMARY KEY,
    job_id BIGINT,
    chain_id VARCHAR(20) NOT NULL,
    error_type VARCHAR(50) NOT NULL,
    error_message TEXT,
    url VARCHAR(500),
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    FOREIGN KEY (job_id) REFERENCES scraping_jobs(job_id),
    FOREIGN KEY (chain_id) REFERENCES grocery_chains(chain_id)
);
```

## Data Validation Rules

### Price Validation
- Prices must be positive values
- Sale prices cannot exceed regular prices
- Price changes exceeding 50% trigger manual review
- Prices are validated against historical ranges for each product

### Product Validation
- Product names must be unique within each store
- Barcodes must follow valid UPC/EAN formats when provided
- Nutrition information follows Health Canada guidelines
- Image URLs must be accessible and return valid image formats

### Store Validation
- Postal codes must follow Canadian format (A1A 1A1)
- Coordinates must be within Canadian geographic boundaries
- Store hours must follow valid time format (HH:MM)
- Phone numbers must follow North American format

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_POSTAL_CODE",
    "message": "The provided postal code is not valid",
    "details": {
      "field": "postal_code",
      "value": "INVALID",
      "expected_format": "A1A 1A1"
    },
    "timestamp": "2025-01-07T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

## Rate Limiting

### Public Endpoints
- 100 requests per minute per IP address
- 1000 requests per hour per IP address

### Authenticated Endpoints
- 500 requests per minute per user
- 10,000 requests per hour per user

### Search Endpoints
- 50 searches per minute per IP address
- Sliding window implementation with burst allowance

---

## References

[1] OpenAPI 3.0 Specification. https://swagger.io/specification/  
[2] PostgreSQL Documentation - Data Types. https://www.postgresql.org/docs/current/datatype.html  
[3] FastAPI Documentation - Request Validation. https://fastapi.tiangolo.com/tutorial/body/  
[4] JWT Authentication Best Practices. https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/  
[5] RESTful API Design Guidelines. https://restfulapi.net/


# Grocery Chain Research for Web Scraping

## Major Grocery Chains in Ontario

Based on research, the top grocery chains in Ontario by market share and presence are:

### Primary Target Chains
1. **Loblaws** (Loblaw Companies Limited)
   - Largest Canadian food retailer
   - Brands include: Loblaws, No Frills, Real Canadian Superstore, Fortinos, Zehrs
   - Market share: ~25-30%

2. **Metro**
   - Major Quebec and Ontario presence
   - Market share: ~11%
   - Strong urban presence

3. **Walmart**
   - Market share: ~8%
   - Supercentres with grocery sections
   - Competitive pricing

4. **Sobeys** (Empire Company)
   - Market share: ~20%
   - Brands include: Sobeys, IGA, Foodland, FreshCo

5. **Costco**
   - Market share: ~9%
   - Warehouse club model
   - Bulk purchasing

### Secondary Targets
- **Food Basics** (Metro subsidiary)
- **No Frills** (Loblaws subsidiary)
- **Farm Boy** (Sobeys subsidiary)

## Flyer and Deal Platforms

### Digital Flyer Aggregators
1. **Flipp.com** - Major flyer aggregation platform
2. **RedFlagDeals.com** - Canadian deal community with flyer section
3. **Save.ca** - Flyer aggregation and coupons

### Individual Chain Flyers
- Metro: https://www.metro.ca/en/flyer
- Sobeys: https://www.sobeys.com/flyer
- Food Basics: https://www.foodbasics.ca/flyer
- No Frills: https://www.nofrills.ca/print-flyer
- Farm Boy: https://www.farmboy.ca/weekly-flyer-specials/

## Scraping Strategy

### Phase 1: Flyer-based Scraping
- Target weekly flyers from major chains
- Extract product names, prices, sale dates
- Focus on structured flyer data

### Phase 2: Website Product Pages
- Scrape individual product pages for detailed info
- Extract regular prices, sale prices, product details
- Handle dynamic content and pagination

### Phase 3: API Integration
- Look for public APIs or mobile app endpoints
- Reverse engineer mobile app requests
- Use official data sources where available

## Technical Considerations

### Anti-Scraping Measures
- Rate limiting and IP blocking
- JavaScript-heavy sites requiring browser automation
- CAPTCHA and bot detection
- Geographic restrictions

### Data Extraction Challenges
- Inconsistent product naming across chains
- Different unit measurements (per lb, per kg, per item)
- Sale vs regular price identification
- Product categorization variations
- Store location-specific pricing

### Legal and Ethical Considerations
- Respect robots.txt files
- Implement reasonable delays between requests
- Consider terms of service compliance
- Focus on publicly available pricing information



## Metro Website Analysis

### URL Structure
- **Flyer Page**: https://www.metro.ca/en/flyer
- **Catalog View**: https://www.metro.ca/en/online-grocery/flyer?sortOrder=relevance&filter=%3Arelevance%3Adeal%3AFlyer+%26+Deals

### Data Structure
The catalog view provides excellent structured data:

#### Product Information Available
- Product name and description
- Brand information (Selection, Irrésistible, etc.)
- Regular price (crossed out when on sale)
- Sale price (in red)
- Unit pricing (per 100g, per kg, per unit)
- Product size/weight
- Canadian product indicators
- Product categories
- Sale indicators ("Save" badges)

#### Technical Details
- **Total Items**: 1933 products in flyer
- **Pagination**: Appears to load more items on scroll
- **Filtering**: Available by category, brand, health choices
- **Sorting**: Price, relevance, alphabetical
- **Store-specific**: Prices shown for selected store location

#### Scraping Approach for Metro
1. **Target URL**: Catalog view with all deals filter
2. **Data Extraction**: 
   - Product cards contain structured pricing data
   - Regular expressions can extract prices from text
   - Product links lead to detailed product pages
3. **Pagination**: Handle infinite scroll or pagination
4. **Store Selection**: Need to handle store location for accurate pricing

### Sample Product Data Structure
```json
{
  "name": "Raspberries",
  "size": "170 g",
  "brand": null,
  "regular_price": 4.99,
  "sale_price": 2.44,
  "unit_price": "$1.44 /100g",
  "on_sale": true,
  "canadian_product": false,
  "category": "Fruits & Vegetables"
}
```

### Anti-Scraping Considerations
- Cookie consent required
- Store location selection needed
- Rate limiting likely in place
- JavaScript-heavy interface
- Possible CAPTCHA on excessive requests


import { useState, useEffect } from 'react'
import { Search, MapPin, ShoppingCart, TrendingDown, Star, Clock } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import './App.css'

// API base URL - will be updated for production
const API_BASE_URL = 'http://localhost:5002/api'

// Mock data for demonstration
const mockStores = [
  {
    store_id: 'walmart_toronto_queen',
    chain_name: 'Walmart',
    store_name: 'Walmart Supercentre Queen St',
    address: { street: '123 Queen St W', city: 'Toronto', province: 'ON' },
    distance_km: 1.2
  },
  {
    store_id: 'loblaws_toronto_college',
    chain_name: 'Loblaws',
    store_name: 'Loblaws College Park',
    address: { street: '444 Yonge St', city: 'Toronto', province: 'ON' },
    distance_km: 0.8
  },
  {
    store_id: 'metro_toronto_king',
    chain_name: 'Metro',
    store_name: 'Metro King Street',
    address: { street: '456 King St W', city: 'Toronto', province: 'ON' },
    distance_km: 1.5
  }
]

const mockProducts = [
  {
    product_id: 'milk_organic_valley_1l',
    name: 'Organic Valley Whole Milk 1L',
    brand: 'Organic Valley',
    size: '1L',
    best_price: 5.99,
    best_price_store: 'Walmart'
  },
  {
    product_id: 'milk_lactantia_2l',
    name: 'Lactantia 2% Milk 2L',
    brand: 'Lactantia',
    size: '2L',
    best_price: 4.97,
    best_price_store: 'Walmart'
  },
  {
    product_id: 'bread_wonder_white',
    name: 'Wonder White Bread 675g',
    brand: 'Wonder',
    size: '675g',
    best_price: 2.97,
    best_price_store: 'Walmart'
  }
]

const mockPriceComparison = {
  product: {
    product_id: 'milk_organic_valley_1l',
    name: 'Organic Valley Whole Milk 1L',
    brand: 'Organic Valley'
  },
  price_comparison: [
    {
      chain_name: 'Walmart',
      store_name: 'Walmart Supercentre Queen St',
      address: '123 Queen St W, Toronto, ON',
      current_price: 5.99,
      regular_price: 6.49,
      on_sale: true,
      sale_end_date: '2025-01-15',
      distance_km: 1.2
    },
    {
      chain_name: 'Loblaws',
      store_name: 'Loblaws College Park',
      address: '444 Yonge St, Toronto, ON',
      current_price: 6.29,
      regular_price: 6.29,
      on_sale: false,
      distance_km: 0.8
    },
    {
      chain_name: 'Metro',
      store_name: 'Metro King Street',
      address: '456 King St W, Toronto, ON',
      current_price: 6.49,
      regular_price: 6.49,
      on_sale: false,
      distance_km: 1.5
    }
  ],
  best_price: {
    price: 5.99,
    savings_vs_highest: 0.50
  },
  average_price: 6.26,
  price_range: {
    min: 5.99,
    max: 6.49
  }
}

function App() {
  const [postalCode, setPostalCode] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [priceComparison, setPriceComparison] = useState(null)
  const [nearbyStores, setNearbyStores] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [useMockData, setUseMockData] = useState(true) // Enable mock data for demo

  // Validate and search for stores by postal code
  const handlePostalCodeSubmit = async (e) => {
    e.preventDefault()
    if (!postalCode.trim()) return

    setLoading(true)
    setError('')

    if (useMockData) {
      // Use mock data for demonstration
      setTimeout(() => {
        setNearbyStores(mockStores)
        setLoading(false)
      }, 1000)
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/locations/postal-code/${postalCode.replace(' ', '')}`)
      if (response.ok) {
        const data = await response.json()
        setNearbyStores(data.nearby_stores || [])
      } else {
        setError('Invalid postal code or no stores found in your area')
      }
    } catch (err) {
      setError('Unable to connect to the service. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // Search for products
  const handleProductSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setLoading(true)
    setError('')

    if (useMockData) {
      // Use mock data for demonstration
      setTimeout(() => {
        const filteredProducts = mockProducts.filter(product =>
          product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          (product.brand && product.brand.toLowerCase().includes(searchQuery.toLowerCase()))
        )
        setSearchResults(filteredProducts.length > 0 ? filteredProducts : mockProducts)
        setLoading(false)
      }, 800)
      return
    }

    try {
      const params = new URLSearchParams({
        query: searchQuery,
        limit: 20
      })
      
      if (postalCode) {
        params.append('postal_code', postalCode)
      }

      const response = await fetch(`${API_BASE_URL}/products/search?${params}`)
      if (response.ok) {
        const data = await response.json()
        setSearchResults(data.results || [])
      } else {
        setError('No products found matching your search')
      }
    } catch (err) {
      setError('Unable to search products. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // Get price comparison for a product
  const handleProductSelect = async (product) => {
    setSelectedProduct(product)
    setLoading(true)
    setError('')

    if (useMockData) {
      // Use mock data for demonstration
      setTimeout(() => {
        setPriceComparison(mockPriceComparison)
        setLoading(false)
      }, 600)
      return
    }

    try {
      const params = new URLSearchParams({
        product_id: product.product_id
      })
      
      if (postalCode) {
        params.append('postal_code', postalCode)
      }

      const response = await fetch(`${API_BASE_URL}/prices/compare?${params}`)
      if (response.ok) {
        const data = await response.json()
        setPriceComparison(data)
      } else {
        setError('Unable to load price comparison')
      }
    } catch (err) {
      setError('Unable to load price comparison. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // Format price display
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-CA', {
      style: 'currency',
      currency: 'CAD'
    }).format(price)
  }

  // Format distance
  const formatDistance = (distance) => {
    return `${distance.toFixed(1)} km`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <ShoppingCart className="h-8 w-8 text-green-600" />
              <h1 className="text-2xl font-bold text-gray-900">GroceryCompare</h1>
            </div>
            <div className="flex items-center space-x-4">
              <p className="text-sm text-gray-600 hidden sm:block">
                Find the best grocery prices in Ontario
              </p>
              {useMockData && (
                <Badge variant="outline" className="text-xs">
                  Demo Mode
                </Badge>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Compare Grocery Prices Across Ontario
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Enter your postal code and search for products to find the best deals 
            at Walmart, Loblaws, Metro, and other major grocery chains near you.
          </p>
          {useMockData && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto">
              <p className="text-blue-800 text-sm">
                <strong>Demo Mode:</strong> This is a demonstration using sample data. 
                Try searching for "milk" or entering postal code "M5V 3A8" to see the features in action.
              </p>
            </div>
          )}
        </div>

        {/* Postal Code Input */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <MapPin className="h-5 w-5 text-green-600" />
              <span>Your Location</span>
            </CardTitle>
            <CardDescription>
              Enter your postal code to find nearby stores and get accurate pricing
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handlePostalCodeSubmit} className="flex space-x-4">
              <Input
                type="text"
                placeholder="e.g., M5V 3A8"
                value={postalCode}
                onChange={(e) => setPostalCode(e.target.value.toUpperCase())}
                className="flex-1 text-lg"
                maxLength={7}
              />
              <Button type="submit" disabled={loading} className="px-8">
                {loading ? 'Searching...' : 'Find Stores'}
              </Button>
            </form>
            
            {nearbyStores.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold mb-3">
                  Found {nearbyStores.length} stores near you
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {nearbyStores.slice(0, 6).map((store) => (
                    <div key={store.store_id} className="p-4 border rounded-lg bg-white">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-gray-900">{store.chain_name}</h4>
                        <Badge variant="secondary">{formatDistance(store.distance_km)}</Badge>
                      </div>
                      <p className="text-sm text-gray-600">{store.store_name}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {store.address.street}, {store.address.city}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Product Search */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Search className="h-5 w-5 text-blue-600" />
              <span>Search Products</span>
            </CardTitle>
            <CardDescription>
              Search for any grocery product to compare prices across stores
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleProductSearch} className="flex space-x-4">
              <Input
                type="text"
                placeholder="e.g., organic milk, bread, bananas..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 text-lg"
              />
              <Button type="submit" disabled={loading || !searchQuery.trim()} className="px-8">
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </form>

            {/* Search Results */}
            {searchResults.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold mb-4">Search Results</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {searchResults.map((product) => (
                    <Card 
                      key={product.product_id} 
                      className="cursor-pointer hover:shadow-md transition-shadow"
                      onClick={() => handleProductSelect(product)}
                    >
                      <CardContent className="p-4">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-medium text-gray-900 line-clamp-2">
                            {product.name}
                          </h4>
                          {product.best_price && (
                            <Badge variant="outline" className="ml-2">
                              {formatPrice(product.best_price)}
                            </Badge>
                          )}
                        </div>
                        {product.brand && (
                          <p className="text-sm text-gray-600 mb-2">{product.brand}</p>
                        )}
                        {product.size && (
                          <p className="text-xs text-gray-500">{product.size}</p>
                        )}
                        {product.best_price_store && (
                          <p className="text-xs text-green-600 mt-2">
                            Best price at {product.best_price_store}
                          </p>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Price Comparison */}
        {selectedProduct && priceComparison && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingDown className="h-5 w-5 text-green-600" />
                <span>Price Comparison</span>
              </CardTitle>
              <CardDescription>
                Comparing prices for {selectedProduct.name}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {priceComparison.price_comparison && priceComparison.price_comparison.length > 0 ? (
                <div className="space-y-4">
                  {/* Best Price Highlight */}
                  {priceComparison.best_price && (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <Star className="h-5 w-5 text-green-600" />
                        <span className="font-semibold text-green-800">Best Price</span>
                      </div>
                      <p className="text-2xl font-bold text-green-800">
                        {formatPrice(priceComparison.best_price.price)}
                      </p>
                      {priceComparison.best_price.savings_vs_highest > 0 && (
                        <p className="text-sm text-green-600">
                          Save {formatPrice(priceComparison.best_price.savings_vs_highest)} vs highest price
                        </p>
                      )}
                    </div>
                  )}

                  {/* Price List */}
                  <div className="space-y-3">
                    {priceComparison.price_comparison.map((price, index) => (
                      <div key={index} className="flex items-center justify-between p-4 border rounded-lg bg-white">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3">
                            <h4 className="font-medium text-gray-900">{price.chain_name}</h4>
                            {price.on_sale && (
                              <Badge variant="destructive" className="text-xs">Sale</Badge>
                            )}
                            {price.current_price === priceComparison.best_price?.price && (
                              <Badge variant="default" className="text-xs bg-green-600">Best Price</Badge>
                            )}
                          </div>
                          <p className="text-sm text-gray-600">{price.store_name}</p>
                          {price.address && (
                            <p className="text-xs text-gray-500">{price.address}</p>
                          )}
                          {price.sale_end_date && (
                            <div className="flex items-center space-x-1 mt-1">
                              <Clock className="h-3 w-3 text-orange-500" />
                              <p className="text-xs text-orange-600">
                                Sale ends {new Date(price.sale_end_date).toLocaleDateString()}
                              </p>
                            </div>
                          )}
                        </div>
                        <div className="text-right">
                          <p className="text-xl font-bold text-gray-900">
                            {formatPrice(price.current_price)}
                          </p>
                          {price.regular_price && price.regular_price !== price.current_price && (
                            <p className="text-sm text-gray-500 line-through">
                              {formatPrice(price.regular_price)}
                            </p>
                          )}
                          {price.distance_km && (
                            <p className="text-xs text-gray-500">
                              {formatDistance(price.distance_km)}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Price Summary */}
                  {priceComparison.average_price && (
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                        <div>
                          <p className="text-sm text-gray-600">Average Price</p>
                          <p className="text-lg font-semibold">
                            {formatPrice(priceComparison.average_price)}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Lowest Price</p>
                          <p className="text-lg font-semibold text-green-600">
                            {formatPrice(priceComparison.price_range.min)}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Highest Price</p>
                          <p className="text-lg font-semibold text-red-600">
                            {formatPrice(priceComparison.price_range.max)}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Price Difference</p>
                          <p className="text-lg font-semibold">
                            {formatPrice(priceComparison.price_range.max - priceComparison.price_range.min)}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-600 text-center py-8">
                  No price data available for this product.
                </p>
              )}
            </CardContent>
          </Card>
        )}

        {/* Error Display */}
        {error && (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="p-4">
              <p className="text-red-800">{error}</p>
            </CardContent>
          </Card>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-600">
              © 2025 GroceryCompare. Helping Ontario families save on groceries.
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Prices are updated regularly but may vary. Please verify prices at the store.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App


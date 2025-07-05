#!/usr/bin/env python3
"""
Simple API test script to verify the grocery price comparison API
"""
import requests
import json

BASE_URL = "http://localhost:5001/api"

def test_endpoint(endpoint, description):
    """Test an API endpoint"""
    try:
        print(f"\n=== Testing {description} ===")
        print(f"URL: {BASE_URL}{endpoint}")
        
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Run API tests"""
    print("Testing Grocery Price Comparison API")
    print("=" * 50)
    
    # Test endpoints
    tests = [
        ("/health", "Health Check"),
        ("/stores/chains", "Grocery Chains"),
        ("/stores", "All Stores"),
        ("/products/categories", "Product Categories"),
        ("/products/search?query=milk", "Product Search - Milk"),
        ("/locations/postal-code/M5V3A8", "Postal Code Validation"),
        ("/prices/compare?product_id=milk_organic_valley_1l", "Price Comparison")
    ]
    
    passed = 0
    total = len(tests)
    
    for endpoint, description in tests:
        if test_endpoint(endpoint, description):
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

if __name__ == "__main__":
    main()


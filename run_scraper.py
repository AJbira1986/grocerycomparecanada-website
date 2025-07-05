#!/usr/bin/env python3
"""
Grocery Scraper Test Script

This script runs the grocery scraping spiders and demonstrates their functionality.
"""

import os
import sys
import subprocess
import json
import sqlite3
from datetime import datetime


def run_spider(spider_name, **kwargs):
    """Run a specific spider with optional arguments"""
    
    print(f"\n{'='*50}")
    print(f"Running {spider_name} spider...")
    print(f"{'='*50}")
    
    # Build command
    cmd = ['scrapy', 'crawl', spider_name]
    
    # Add spider arguments
    for key, value in kwargs.items():
        cmd.extend(['-a', f'{key}={value}'])
    
    # Add output settings
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    cmd.extend(['-s', f'FEEDS={{"products_{spider_name}_{timestamp}.json":{{"format":"json"}}}}'])
    
    try:
        # Change to scrapy project directory
        os.chdir('grocery_scraper')
        
        # Run the spider
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {spider_name} spider completed successfully!")
            print(f"Output: {result.stdout[-500:]}")  # Last 500 chars
        else:
            print(f"❌ {spider_name} spider failed!")
            print(f"Error: {result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {spider_name} spider timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"💥 Error running {spider_name} spider: {e}")
        return False
    finally:
        os.chdir('..')


def analyze_scraped_data():
    """Analyze the scraped data and show statistics"""
    
    print(f"\n{'='*50}")
    print("Analyzing scraped data...")
    print(f"{'='*50}")
    
    db_path = 'grocery_scraper/grocery_data.db'
    
    if not os.path.exists(db_path):
        print("❌ No database found. Run scrapers first.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get product count by store
        cursor.execute('''
            SELECT store_chain, COUNT(*) as product_count, 
                   AVG(current_price) as avg_price,
                   COUNT(CASE WHEN on_sale = 1 THEN 1 END) as sale_count
            FROM products 
            GROUP BY store_chain
        ''')
        
        store_stats = cursor.fetchall()
        
        print("\n📊 Store Statistics:")
        print("-" * 60)
        print(f"{'Store':<15} {'Products':<10} {'Avg Price':<12} {'On Sale':<10}")
        print("-" * 60)
        
        for store, count, avg_price, sale_count in store_stats:
            avg_price_str = f"${avg_price:.2f}" if avg_price else "N/A"
            print(f"{store:<15} {count:<10} {avg_price_str:<12} {sale_count:<10}")
        
        # Get price comparison examples
        cursor.execute('''
            SELECT name, store_chain, current_price, on_sale
            FROM products 
            WHERE name IN (
                SELECT name FROM products 
                GROUP BY name 
                HAVING COUNT(DISTINCT store_chain) > 1
            )
            ORDER BY name, current_price
            LIMIT 20
        ''')
        
        price_comparisons = cursor.fetchall()
        
        if price_comparisons:
            print("\n💰 Price Comparison Examples:")
            print("-" * 80)
            current_product = None
            
            for name, store, price, on_sale in price_comparisons:
                if name != current_product:
                    if current_product:
                        print()
                    print(f"\n🛒 {name}:")
                    current_product = name
                
                sale_indicator = " (ON SALE)" if on_sale else ""
                print(f"  {store}: ${price:.2f}{sale_indicator}")
        
        # Get recent scraping activity
        cursor.execute('''
            SELECT DATE(scraped_at) as scrape_date, COUNT(*) as items_scraped
            FROM products 
            GROUP BY DATE(scraped_at)
            ORDER BY scrape_date DESC
            LIMIT 7
        ''')
        
        recent_activity = cursor.fetchall()
        
        if recent_activity:
            print("\n📅 Recent Scraping Activity:")
            print("-" * 40)
            for date, count in recent_activity:
                print(f"{date}: {count} items")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")


def show_json_sample():
    """Show sample of JSON output"""
    
    print(f"\n{'='*50}")
    print("Sample JSON Output:")
    print(f"{'='*50}")
    
    # Find the most recent JSON file
    json_files = [f for f in os.listdir('.') if f.startswith('products_') and f.endswith('.json')]
    
    if not json_files:
        json_files = [f for f in os.listdir('grocery_scraper') if f.startswith('products_') and f.endswith('.json')]
        if json_files:
            json_files = [f'grocery_scraper/{f}' for f in json_files]
    
    if json_files:
        latest_file = max(json_files, key=os.path.getmtime)
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data:
                print(f"\n📄 Sample from {latest_file}:")
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
                print(f"\n📊 Total items in file: {len(data)}")
            else:
                print("📄 JSON file is empty")
                
        except Exception as e:
            print(f"❌ Error reading JSON file: {e}")
    else:
        print("📄 No JSON output files found")


def main():
    """Main function to run the scraper demo"""
    
    print("🛒 Grocery Price Scraper Demo")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('grocery_scraper'):
        print("❌ grocery_scraper directory not found!")
        print("Please run this script from the grocery-scraper directory")
        return
    
    # List available spiders
    try:
        os.chdir('grocery_scraper')
        result = subprocess.run(['scrapy', 'list'], capture_output=True, text=True)
        spiders = result.stdout.strip().split('\n') if result.stdout else []
        os.chdir('..')
        
        print(f"\n🕷️  Available spiders: {', '.join(spiders)}")
        
    except Exception as e:
        print(f"❌ Error listing spiders: {e}")
        return
    
    # Run Metro spider as demo
    if 'metro' in spiders:
        success = run_spider('metro')
        
        if success:
            # Analyze the results
            analyze_scraped_data()
            show_json_sample()
        else:
            print("\n❌ Metro spider failed. Check the logs for details.")
    else:
        print("❌ Metro spider not found!")
    
    print(f"\n{'='*50}")
    print("Demo completed!")
    print("Check the following files for results:")
    print("- grocery_data.db (SQLite database)")
    print("- products_*.json (JSON output)")
    print("- scrapy.log (Detailed logs)")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()


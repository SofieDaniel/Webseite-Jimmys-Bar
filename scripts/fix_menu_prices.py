#!/usr/bin/env python3
"""
Fix menu items price data type mismatch
Convert all price fields from string to float in the database
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def fix_menu_price_types():
    """Fix menu item price data types in MongoDB"""
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🔧 Fixing menu item price data types...")
    
    try:
        # Find all menu items
        menu_items = await db.menu_items.find().to_list(None)
        print(f"📊 Found {len(menu_items)} menu items to check")
        
        fixed_count = 0
        for item in menu_items:
            price = item.get('price')
            
            # If price is a string, convert to float
            if isinstance(price, str):
                try:
                    # Remove currency symbols and convert to float
                    clean_price = price.replace('€', '').replace(',', '.').strip()
                    float_price = float(clean_price)
                    
                    # Update the item
                    await db.menu_items.update_one(
                        {'id': item['id']},
                        {'$set': {'price': float_price}}
                    )
                    
                    fixed_count += 1
                    print(f"  ✅ Fixed {item['name']}: '{price}' → {float_price}")
                    
                except ValueError:
                    print(f"  ❌ Could not convert price for {item['name']}: '{price}'")
            
            elif isinstance(price, (int, float)):
                print(f"  ✅ {item['name']}: {price} (already correct)")
        
        print(f"\n🎉 Fixed {fixed_count} menu items")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise e
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(fix_menu_price_types())
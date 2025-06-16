#!/usr/bin/env python3
"""
Entferne alle Bilder aus den Menu-Items
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def remove_all_menu_images():
    """Remove all images from menu items"""
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🔧 Removing all images from menu items...")
    
    try:
        # Update all menu items to remove images
        result = await db.menu_items.update_many(
            {},
            {"$set": {"image": ""}}
        )
        
        print(f"✅ Updated {result.modified_count} menu items")
        print("🖼️  All images have been removed from the menu")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise e
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(remove_all_menu_images())
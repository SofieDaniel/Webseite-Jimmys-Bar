#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('/app/backend/.env')

async def fix_ueber_uns():
    # MongoDB connection
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Delete existing ueber_uns_enhanced data
    await db.ueber_uns_enhanced.delete_many({})
    
    # Insert new data without team section
    new_content = {
        "id": "fixed-ueber-uns-2024",
        "page_title": "Über uns",
        "page_subtitle": "Lernen Sie Jimmy's Tapas Bar kennen",
        "header_background": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
        "jimmy": {
            "name": "Jimmy Rodríguez",
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d",
            "story_paragraph1": "Seit der Gründung im Jahr 2015 steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.",
            "story_paragraph2": "Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.",
            "quote": "Gutes Essen bringt Menschen zusammen und schafft unvergessliche Momente."
        },
        "values_section": {
            "title": "Unsere Werte",
            "values": [
                {
                    "title": "Qualität",
                    "description": "Wir verwenden nur die besten Zutaten für unsere Gerichte.",
                    "icon": "⭐"
                },
                {
                    "title": "Gastfreundschaft", 
                    "description": "Bei uns sollen Sie sich wie zu Hause fühlen.",
                    "icon": "❤️"
                },
                {
                    "title": "Authentizität",
                    "description": "Wir bleiben den traditionellen spanischen Rezepten treu.",
                    "icon": "🇪🇸"
                }
            ]
        },
        "updated_at": datetime.utcnow(),
        "updated_by": "system"
    }
    
    await db.ueber_uns_enhanced.insert_one(new_content)
    print("✅ Über uns ohne Team-Sektion aktualisiert")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_ueber_uns())
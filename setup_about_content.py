#!/usr/bin/env python3
"""
Setup About Content for Jimmy's Tapas Bar
"""

import asyncio
import aiomysql
import os
import uuid
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# MySQL connection settings
mysql_config = {
    'host': os.environ['MYSQL_HOST'],
    'port': int(os.environ['MYSQL_PORT']),
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE'],
    'charset': 'utf8mb4',
    'autocommit': True
}

async def setup_about_content():
    """Setup about content data"""
    print("🏖️  Setting up About content for Jimmy's Tapas Bar")
    print("=" * 60)
    
    # Connect to MySQL
    connection = await aiomysql.connect(**mysql_config)
    cursor = await connection.cursor()
    
    try:
        # Clear existing data
        await cursor.execute("DELETE FROM about_content")
        print("🗑️  Cleared existing about content")
        
        # Team members data
        team_members = [
            {
                "name": "Jimmy Rodriguez",
                "role": "Küchenchef & Inhaber",
                "description": "Geboren in Valencia, bringt Jimmy über 15 Jahre Erfahrung in der spanischen Küche mit.",
                "image": "https://images.unsplash.com/photo-1560250097-0b93528c311a"
            },
            {
                "name": "Maria Gonzalez",
                "role": "Sous Chef",
                "description": "Spezialistin für traditionelle Tapas und Paella aus der Region Andalusien.",
                "image": "https://images.unsplash.com/photo-1594736797933-d0ee6a8b2023"
            }
        ]
        
        # Values data
        values = [
            {
                "title": "Authentizität",
                "description": "Wir verwenden nur die besten Zutaten direkt aus Spanien importiert.",
                "icon": "🇪🇸"
            },
            {
                "title": "Qualität",
                "description": "Jedes Gericht wird frisch zubereitet mit Liebe zum Detail.",
                "icon": "⭐"
            },
            {
                "title": "Gastfreundschaft",
                "description": "Spanische Herzlichkeit trifft norddeutsche Gemütlichkeit.",
                "icon": "❤️"
            }
        ]
        
        # Insert about content
        about_id = str(uuid.uuid4())
        await cursor.execute("""
            INSERT INTO about_content (
                id, page_title, hero_title, hero_description, story_title,
                story_content, story_image, team_title, team_members,
                values_title, values_data, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            about_id,
            "Über uns",
            "Willkommen bei Jimmy's Tapas Bar",
            "Authentische spanische Küche an der Ostsee",
            "Unsere Geschichte",
            """Jimmy's Tapas Bar wurde 2015 von Jimmy Rodriguez gegründet, einem leidenschaftlichen Koch aus Valencia. 
            Nach Jahren der Erfahrung in renommierten Restaurants Spaniens und Deutschlands, verwirklichte er seinen Traum: 
            Ein authentisches spanisches Restaurant an der malerischen Ostseeküste. 
            
            Unser Restaurant vereint die Wärme und Lebensfreude Spaniens mit der entspannten Atmosphäre der Ostsee. 
            Wir servieren traditionelle Tapas, fangfrische Meeresfrüchte und die beste Paella nördlich der Pyrenäen, 
            während Sie den Blick auf die Ostsee genießen können.""",
            "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
            "Unser Team",
            json.dumps(team_members),
            "Unsere Werte",
            json.dumps(values),
            datetime.now()
        ))
        
        print("✅ About content setup successful!")
        print(f"   📄 Page title: Über uns")
        print(f"   👥 Team members: {len(team_members)}")
        print(f"   💎 Values: {len(values)}")
        
    except Exception as e:
        print(f"❌ Error setting up about content: {e}")
        raise
    finally:
        await cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(setup_about_content())
#!/usr/bin/env python3
"""
Setup Standorte Enhanced Content for Jimmy's Tapas Bar
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

async def setup_standorte_enhanced():
    """Setup standorte enhanced content data"""
    print("🏖️  Setting up Standorte Enhanced content for Jimmy's Tapas Bar")
    print("=" * 60)
    
    # Connect to MySQL
    connection = await aiomysql.connect(**mysql_config)
    cursor = await connection.cursor()
    
    try:
        # Clear existing data
        await cursor.execute("DELETE FROM standorte_enhanced")
        print("🗑️  Cleared existing standorte enhanced content")
        
        # Neustadt data
        neustadt_data = {
            "name": "Jimmy's Tapas Bar Neustadt",
            "address": "Strandstraße 12, 23730 Neustadt in Holstein",
            "phone": "+49 4561 123456",
            "email": "neustadt@jimmys-tapasbar.de",
            "description": "Unser Hauptstandort direkt am Strand von Neustadt in Holstein",
            "image_url": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
            "opening_hours": {
                "Montag": "16:00 - 23:00 (Mai - September)",
                "Dienstag": "16:00 - 23:00 (Mai - September)",
                "Mittwoch": "16:00 - 23:00 (Mai - September)",
                "Donnerstag": "16:00 - 23:00 (Mai - September)",
                "Freitag": "16:00 - 24:00 (Mai - September)",
                "Samstag": "12:00 - 24:00 (Mai - September)",
                "Sonntag": "12:00 - 23:00 (Mai - September)"
            },
            "features": ["Direkte Strandlage", "Große Terrasse", "Live-Musik", "Familienfreundlich"]
        }
        
        # Großenbrode data
        grossenbrode_data = {
            "name": "Jimmy's Tapas Bar Großenbrode",
            "address": "Strandpromenade 8, 23775 Großenbrode",
            "phone": "+49 4367 987654",
            "email": "grossenbrode@jimmys-tapasbar.de",
            "description": "Gemütlich direkt an der Ostsee mit herrlichem Blick auf das Meer",
            "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d",
            "opening_hours": {
                "Montag": "17:00 - 23:00 (Mai - September)",
                "Dienstag": "17:00 - 23:00 (Mai - September)",
                "Mittwoch": "17:00 - 23:00 (Mai - September)",
                "Donnerstag": "17:00 - 23:00 (Mai - September)",
                "Freitag": "17:00 - 24:00 (Mai - September)",
                "Samstag": "12:00 - 24:00 (Mai - September)",
                "Sonntag": "12:00 - 23:00 (Mai - September)"
            },
            "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"]
        }
        
        # Info section data
        info_section_data = {
            "sections": [
                {
                    "title": "Anreise",
                    "icon": "🚗",
                    "description": "Beide Standorte sind gut mit dem Auto erreichbar. Kostenlose Parkplätze sind vorhanden."
                },
                {
                    "title": "Reservierung",
                    "icon": "📞",
                    "description": "Wir empfehlen eine Reservierung, besonders in der Hauptsaison."
                },
                {
                    "title": "Events",
                    "icon": "🎉",
                    "description": "Feiern Sie bei uns! Wir bieten Event-Packages für besondere Anlässe."
                }
            ]
        }
        
        # Insert standorte enhanced content
        standorte_id = str(uuid.uuid4())
        await cursor.execute("""
            INSERT INTO standorte_enhanced (
                id, page_title, page_subtitle, header_background,
                neustadt_data, grossenbrode_data, info_section_data,
                updated_at, updated_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            standorte_id,
            "Unsere Standorte",
            "Besuchen Sie uns an der malerischen Ostseeküste",
            "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
            json.dumps(neustadt_data),
            json.dumps(grossenbrode_data),
            json.dumps(info_section_data),
            datetime.now(),
            "system"
        ))
        
        print("✅ Standorte Enhanced content setup successful!")
        print(f"   📍 Neustadt: {neustadt_data['address']}")
        print(f"   📍 Großenbrode: {grossenbrode_data['address']}")
        print(f"   ℹ️ Info sections: {len(info_section_data['sections'])}")
        
    except Exception as e:
        print(f"❌ Error setting up standorte enhanced content: {e}")
        raise
    finally:
        await cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(setup_standorte_enhanced())
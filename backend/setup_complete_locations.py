#!/usr/bin/env python3
"""
Complete Locations Setup for Jimmy's Tapas Bar
Sets up the correct location data structure
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

# Complete locations data as specified
LOCATIONS_DATA = [
    {
        "id": "neustadt",
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
        "seasonal_note": "Saisonale Öffnungszeiten von Mai bis September",
        "specialties": [
            "Direkte Strandlage",
            "Große Terrasse mit Meerblick",
            "Familiäre Atmosphäre",
            "Authentische mediterrane Küche"
        ],
        "features": {
            "parking": True,
            "terrace": True,
            "sea_view": True,
            "family_friendly": True,
            "wheelchair_accessible": True
        },
        "coordinates": {
            "lat": 54.1047,
            "lng": 10.8156
        }
    },
    {
        "id": "grossenbrode",
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
        "seasonal_note": "Saisonale Öffnungszeiten von Mai bis September",
        "specialties": [
            "Panorama-Meerblick",
            "Ruhige Lage",
            "Romantische Atmosphäre",
            "Sonnenuntergänge"
        ],
        "features": {
            "parking": True,
            "terrace": True,
            "sea_view": True,
            "family_friendly": True,
            "wheelchair_accessible": False
        },
        "coordinates": {
            "lat": 54.3736,
            "lng": 11.0331
        }
    }
]

# Info sections for "Gut zu wissen"
INFO_SECTIONS = [
    {
        "id": "anreise",
        "title": "Anreise",
        "icon": "🚗",
        "description": "Beide Standorte sind gut mit dem Auto erreichbar. Kostenlose Parkplätze sind vorhanden. Mit öffentlichen Verkehrsmitteln erreichen Sie uns über die Regionalbahn bis Neustadt bzw. Großenbrode."
    },
    {
        "id": "reservierung", 
        "title": "Reservierung",
        "icon": "📞",
        "description": "Wir empfehlen eine Reservierung, besonders in der Hauptsaison. Rufen Sie uns an oder nutzen Sie unser Online-Reservierungssystem. Spontane Besuche sind natürlich auch willkommen!"
    },
    {
        "id": "events",
        "title": "Events & Feiern",
        "icon": "🎉", 
        "description": "Beide Restaurants eignen sich perfekt für private Feiern, Firmenevents oder besondere Anlässe. Sprechen Sie uns für individuelle Arrangements an."
    }
]

async def setup_complete_locations():
    """Setup complete locations data in MySQL database"""
    print("🏖️  Setting up complete locations for Jimmy's Tapas Bar")
    print("=" * 60)
    
    try:
        # Connect to MySQL
        conn = await aiomysql.connect(**mysql_config)
        cursor = await conn.cursor()
        
        # Clear existing locations data
        print("🗑️  Clearing existing locations data...")
        await cursor.execute("DELETE FROM locations")
        
        # Create complete locations data structure
        complete_data = {
            "page_title": "Unsere Standorte",
            "page_description": "Besuchen Sie uns an einem unserer beiden malerischen Standorte an der Ostsee",
            "locations": LOCATIONS_DATA,
            "info_sections": INFO_SECTIONS,
            "general_info": {
                "reservation_phone": "+49 4561 123456",
                "reservation_email": "reservierung@jimmys-tapasbar.de",
                "opening_season": "Mai bis September",
                "special_note": "Beide Standorte bieten authentische mediterrane Küche in unmittelbarer Strandnähe"
            }
        }
        
        # Insert new locations data
        content_id = str(uuid.uuid4())
        await cursor.execute("""
            INSERT INTO locations (id, page_title, page_description, locations_data, updated_at, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            content_id,
            complete_data["page_title"],
            complete_data["page_description"],
            json.dumps(complete_data, ensure_ascii=False),
            datetime.utcnow(),
            "system"
        ))
        
        print(f"✅ Successfully setup locations data")
        print(f"   📍 {len(LOCATIONS_DATA)} locations imported")
        print(f"   ℹ️ {len(INFO_SECTIONS)} info sections added")
        
        print("\n📊 Locations Summary:")
        for location in LOCATIONS_DATA:
            print(f"   {location['name']}: {location['address']}")
        
        print(f"\n🎉 Complete locations setup finished successfully!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Locations setup failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(setup_complete_locations())
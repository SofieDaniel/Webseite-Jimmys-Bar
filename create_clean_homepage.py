#!/usr/bin/env python3
"""
Erstelle Homepage-Daten OHNE Icons für Jimmy's Tapas Bar
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

async def create_clean_homepage():
    """Erstelle Homepage-Daten ohne Icons"""
    print("🏠 Erstelle saubere Homepage-Daten OHNE Icons")
    print("=" * 60)
    
    # Connect to MySQL
    connection = await aiomysql.connect(**mysql_config)
    cursor = await connection.cursor()
    
    try:
        # Clear existing data
        await cursor.execute("DELETE FROM homepage_content")
        print("🗑️ Bestehende Homepage-Daten gelöscht")
        
        # Features ohne Icons
        features_data = [
            {
                "title": "Authentische Tapas",
                "description": "Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
                "image": "https://images.unsplash.com/photo-1544025162-d76694265947"
            },
            {
                "title": "Frische Meeresfrüchte",
                "description": "Täglich frisch aus der Ostsee und dem Mittelmeer",
                "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"
            },
            {
                "title": "Strandlage",
                "description": "Genießen Sie Ihr Essen mit direktem Blick auf die Ostsee",
                "image": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
            }
        ]
        
        # Spezialitäten ohne Icons
        specialties_data = [
            {
                "title": "Paella Valenciana",
                "description": "Original spanische Paella mit Safran, Huhn und Gemüse",
                "price": "18,90€",
                "image": "https://images.unsplash.com/photo-1534080564583-6be75777b70a"
            },
            {
                "title": "Gambas al Ajillo", 
                "description": "Knoblauchgarnelen in Olivenöl mit frischen Kräutern",
                "price": "12,90€",
                "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"
            },
            {
                "title": "Pulpo a la Gallega",
                "description": "Galicischer Oktopus mit Paprika und Olivenöl",
                "price": "14,90€",
                "image": "https://images.unsplash.com/photo-1544025162-d76694265947"
            }
        ]
        
        # Delivery-Daten
        delivery_data = {
            "title": "Lieferservice",
            "subtitle": "Spanische Köstlichkeiten direkt zu Ihnen",
            "delivery_time": "30-45 Min",
            "minimum_order": "15,00€",
            "delivery_fee": "2,50€",
            "areas": ["Neustadt in Holstein", "Großenbrode", "Umgebung"],
            "image": "https://images.unsplash.com/photo-1586816001966-79b736744398"
        }
        
        # Homepage-Content einfügen
        homepage_id = str(uuid.uuid4())
        await cursor.execute("""
            INSERT INTO homepage_content (
                id, hero_title, hero_subtitle, hero_image,
                features_data, specialties_data, delivery_data,
                updated_at, updated_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            homepage_id,
            "JIMMY'S TAPAS BAR",
            "Authentische spanische Küche an der Ostsee",
            "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
            json.dumps(features_data),
            json.dumps(specialties_data),
            json.dumps(delivery_data),
            datetime.now(),
            "system"
        ))
        
        print("✅ Saubere Homepage-Daten erstellt!")
        print(f"   🎯 Features: {len(features_data)} (ohne Icons)")
        print(f"   🍽️ Spezialitäten: {len(specialties_data)} (ohne Icons)")
        print(f"   🚚 Delivery-Daten eingerichtet")
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen der Homepage-Daten: {e}")
        raise
    finally:
        await cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(create_clean_homepage())
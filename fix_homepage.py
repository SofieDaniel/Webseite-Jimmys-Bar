#!/usr/bin/env python3
"""
Korrekte Jimmy's Tapas Bar Homepage-Daten erstellen
"""

import asyncio
import aiomysql
import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# Database connection parameters
DB_CONFIG = {
    'host': os.environ['MYSQL_HOST'],
    'port': int(os.environ['MYSQL_PORT']),
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE'],
    'charset': 'utf8mb4'
}

async def fix_homepage_content():
    """Korrigiert die Homepage-Inhalte mit den richtigen Jimmy's Tapas Bar Daten"""
    
    print("🔧 KORREKTE JIMMY'S TAPAS BAR HOMEPAGE ERSTELLEN")
    print("=" * 60)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Lösche alte Homepage-Inhalte
        await cursor.execute("DELETE FROM homepage_content")
        
        # Korrekte Features-Daten mit echten Bildern
        features_data = {
            "features": [
                {
                    "title": "Authentische Tapas",
                    "description": "Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
                    "image_url": "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"
                },
                {
                    "title": "Frische Paella",
                    "description": "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn",
                    "image_url": "https://images.unsplash.com/photo-1694685367640-05d6624e57f1"
                },
                {
                    "title": "Strandnähe",
                    "description": "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden",
                    "image_url": "https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg"
                }
            ]
        }
        
        # Korrekte Spezialitäten mit 4 Gerichten
        specialties_data = {
            "specialties": [
                {
                    "name": "Patatas Bravas",
                    "description": "Klassische mediterrane Kartoffeln",
                    "price": "7.50€",
                    "image": "https://images.unsplash.com/photo-1565599837634-134bc3aadce8"
                },
                {
                    "name": "Paella Valenciana",
                    "description": "Traditionelle mediterrane Paella",
                    "price": "18.90€",
                    "image": "https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg"
                },
                {
                    "name": "Tapas Variación",
                    "description": "Auswahl mediterraner Köstlichkeiten",
                    "price": "12.50€",
                    "image": "https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg"
                },
                {
                    "name": "Gambas al Ajillo",
                    "description": "Garnelen in Knoblauchöl",
                    "price": "12.90€",
                    "image": "https://images.unsplash.com/photo-1619860705243-dbef552e7118"
                }
            ]
        }
        
        # Delivery-Daten
        delivery_data = {
            "delivery_time": "30-45 Min",
            "minimum_order": "15.00€",
            "delivery_fee": "2.50€"
        }
        
        # Homepage-Content einfügen
        homepage_sql = """
            INSERT INTO homepage_content (
                id, hero_title, hero_subtitle, hero_description, hero_background,
                features_data, specialties_data, delivery_data, updated_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        await cursor.execute(homepage_sql, (
            str(uuid.uuid4()),
            "JIMMY'S TAPAS BAR",
            "an der Ostsee",
            "Genießen Sie authentische mediterrane Spezialitäten direkt an der malerischen Ostseeküste",
            "https://images.unsplash.com/photo-1656423521731-9665583f100c",
            json.dumps(features_data),
            json.dumps(specialties_data),
            json.dumps(delivery_data),
            "system"
        ))
        
        # Commit changes
        await connection.commit()
        
        print("✅ Korrekte Jimmy's Tapas Bar Homepage erstellt!")
        print("   - Hero: JIMMY'S TAPAS BAR an der Ostsee")
        print("   - Features: 3 mit korrekten Bildern")
        print("   - Spezialitäten: 4 Gerichte mit Preisen")
        print("   - Hintergrund: Authentisches Tapas-Bild")
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(fix_homepage_content())
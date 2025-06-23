#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('/app/backend/.env')

async def fix_homepage():
    # MongoDB connection
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Delete existing homepage content
    await db.homepage_content.delete_many({})
    
    # Insert KORREKTE Homepage-Daten wie in den Bildern
    homepage_data = {
        "id": "fixed-homepage-2024",
        "hero_title": "JIMMY'S TAPAS BAR",
        "hero_subtitle": "an der Ostsee",
        "hero_description": "Genießen Sie authentische mediterrane Spezialitäten",
        "hero_location": "direkt an der malerischen Ostseeküste",
        "hero_background_image": "https://images.unsplash.com/photo-1656423521731-9665583f100c",
        "hero_menu_button_text": "Zur Speisekarte",
        "hero_locations_button_text": "Unsere Standorte",
        "hero_image": "https://images.unsplash.com/photo-1560472355-536de3962603",
        
        # Mediterrane Tradition (3 Karten wie im Bild)
        "features_data": {
            "title": "Mediterrane Tradition",
            "subtitle": "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste",
            "cards": [
                {
                    "title": "Authentische Tapas",
                    "description": "Traditionelle Rezepte aus verschiedenen Regionen Spaniens",
                    "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae",
                    "link_category": "Vorspeisen"
                },
                {
                    "title": "Frische Paellas",
                    "description": "Täglich frisch zubereitet nach originalen Rezepten",
                    "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a",
                    "link_category": "Paella"
                },
                {
                    "title": "Strandnähe",
                    "description": "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden",
                    "image_url": "https://images.unsplash.com/photo-1506377585622-bedcbb027afc",
                    "link_category": "Standorte"
                }
            ]
        },
        
        # Unsere Spezialitäten (4 Karten wie im Bild)
        "specialties_data": {
            "title": "Unsere Spezialitäten",
            "cards": [
                {
                    "title": "Patatas Bravas",
                    "description": "Klassische mediterrane Kartoffeln",
                    "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a",
                    "category_link": "Vorspeisen"
                },
                {
                    "title": "Paella Valenciana",
                    "description": "Traditionelle mediterrane Paella",
                    "image_url": "https://images.unsplash.com/photo-1558985250-3f1b04f44b25",
                    "category_link": "Paella"
                },
                {
                    "title": "Tapas Variación",
                    "description": "Auswahl mediterraner Köstlichkeiten",
                    "image_url": "https://images.unsplash.com/photo-1565299585323-38174c2a5aa4",
                    "category_link": "Vorspeisen"
                },
                {
                    "title": "Gambas al Ajillo",
                    "description": "Garnelen in Knoblauchöl",
                    "image_url": "https://images.unsplash.com/photo-1565299585323-38174c2a5aa4",
                    "category_link": "Vorspeisen"
                }
            ]
        },
        
        # Delivery-Sektion
        "delivery_data": {
            "title": "Jetzt auch bequem nach Hause bestellen",
            "description": "Genießen Sie unsere authentischen mediterranen Spezialitäten gemütlich zu Hause.",
            "description_2": "Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.",
            "delivery_feature_title": "Schnelle Lieferung",
            "delivery_feature_description": "Frisch und warm zu Ihnen",
            "delivery_feature_image": "https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg",
            "button_text": "Jetzt bei Lieferando bestellen",
            "button_url": "https://www.lieferando.de",
            "availability_text": "Verfügbar für beide Standorte",
            "authentic_feature_title": "Authentisch Mediterran",
            "authentic_feature_description": "Direkt vom Küchenchef",
            "authentic_feature_image": "https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg"
        },
        
        "updated_at": datetime.utcnow(),
        "updated_by": "system_fix"
    }
    
    await db.homepage_content.insert_one(homepage_data)
    print("✅ Homepage mit korrekten Daten (wie in Bildern) wiederhergestellt")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_homepage())
#!/usr/bin/env python3
"""
CMS-Daten Vervollständigung für Jimmy's Tapas Bar
Fügt Standard-CMS-Inhalte hinzu, die möglicherweise fehlen
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

async def populate_cms_data():
    """Fügt Standard-CMS-Inhalte hinzu"""
    
    print("🎨 CMS-DATEN VERVOLLSTÄNDIGUNG")
    print("=" * 50)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # 1. Homepage Content
        print("🏠 Homepage Content...")
        homepage_sql = """
            INSERT IGNORE INTO homepage_content (
                id, hero_title, hero_subtitle, hero_description, hero_background,
                features_data, specialties_data, delivery_data, updated_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        features_data = {
            "features": [
                {
                    "title": "Authentische Tapas",
                    "description": "Traditionelle spanische Rezepte mit frischen Zutaten",
                    "icon": "🍽️"
                },
                {
                    "title": "Direkt am Strand",
                    "description": "Genießen Sie Ihre Mahlzeit mit Blick auf die Ostsee",
                    "icon": "🏖️"
                },
                {
                    "title": "Familiär & Freundlich",
                    "description": "Warme Atmosphäre für die ganze Familie",
                    "icon": "👨‍👩‍👧‍👦"
                }
            ]
        }
        
        specialties_data = {
            "specialties": [
                {
                    "name": "Paella Valenciana",
                    "description": "Traditionelle Paella mit Huhn, Kaninchen und Gemüse",
                    "price": "18.90€",
                    "image": "https://images.unsplash.com/photo-1534080564583-6be75777b70a"
                },
                {
                    "name": "Gambas al Ajillo",
                    "description": "Garnelen in Knoblauchöl mit frischen Kräutern",
                    "price": "12.90€",
                    "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"
                }
            ]
        }
        
        delivery_data = {
            "delivery_time": "30-45 Min",
            "minimum_order": "15.00€",
            "delivery_fee": "2.50€"
        }
        
        await cursor.execute(homepage_sql, (
            str(uuid.uuid4()),
            "Willkommen bei Jimmy's Tapas Bar",
            "Authentische spanische Küche an der Ostsee",
            "Erleben Sie die Vielfalt Spaniens in unseren gemütlichen Restaurants direkt am Strand.",
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0",
            json.dumps(features_data),
            json.dumps(specialties_data),
            json.dumps(delivery_data),
            "system"
        ))
        print("   ✅ Homepage Content erstellt")
        
        # 2. About Content
        print("📖 About Content...")
        about_sql = """
            INSERT IGNORE INTO about_content (
                id, hero_title, story_content, team_data, values_data, updated_by
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        team_data = {
            "team": [
                {
                    "name": "Jimmy Rodríguez",
                    "position": "Inhaber & Küchenchef",
                    "description": "Mit über 20 Jahren Erfahrung in der spanischen Küche",
                    "image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e"
                },
                {
                    "name": "Maria González",
                    "position": "Sous Chef",
                    "description": "Spezialistin für traditionelle Tapas und Paella",
                    "image": "https://images.unsplash.com/photo-1494790108755-2616b612b789"
                }
            ]
        }
        
        values_data = {
            "values": [
                {
                    "title": "Qualität",
                    "description": "Nur die besten und frischesten Zutaten",
                    "icon": "⭐"
                },
                {
                    "title": "Tradition",
                    "description": "Authentische spanische Rezepte seit Generationen",
                    "icon": "🏛️"
                },
                {
                    "title": "Gastfreundschaft",
                    "description": "Jeder Gast ist bei uns herzlich willkommen",
                    "icon": "❤️"
                }
            ]
        }
        
        await cursor.execute(about_sql, (
            str(uuid.uuid4()),
            "Unsere Geschichte",
            "Jimmy's Tapas Bar wurde 2005 mit der Vision gegründet, authentische spanische Küche an die deutsche Ostseeküste zu bringen. Was als kleines Familienrestaurant begann, ist heute zu einer beliebten Anlaufstelle für Liebhaber der mediterranen Küche geworden.",
            json.dumps(team_data),
            json.dumps(values_data),
            "system"
        ))
        print("   ✅ About Content erstellt")
        
        # 3. Locations Content
        print("📍 Locations Content...")
        locations_sql = """
            INSERT IGNORE INTO locations_content (
                id, page_title, page_description, locations_data, updated_by
            ) VALUES (%s, %s, %s, %s, %s)
        """
        
        locations_data = {
            "locations": [
                {
                    "name": "Neustadt in Holstein",
                    "address": "Am Strande 21, 23730 Neustadt in Holstein",
                    "phone": "+49 (0) 4561 123456",
                    "email": "neustadt@jimmys-tapasbar.de",
                    "opening_hours": {
                        "monday": "12:00 - 22:00",
                        "tuesday": "12:00 - 22:00",
                        "wednesday": "12:00 - 22:00",
                        "thursday": "12:00 - 22:00",
                        "friday": "12:00 - 22:00",
                        "saturday": "12:00 - 22:00",
                        "sunday": "12:00 - 22:00"
                    },
                    "features": ["Terrasse mit Meerblick", "Parkplätze vorhanden", "Familienfreundlich"]
                },
                {
                    "name": "Großenbrode",
                    "address": "Südstrand 54, 23755 Großenbrode",
                    "phone": "+49 (0) 4561 789012",
                    "email": "grossenbrode@jimmys-tapasbar.de",
                    "opening_hours": {
                        "monday": "12:00 - 22:00",
                        "tuesday": "12:00 - 22:00",
                        "wednesday": "12:00 - 22:00",
                        "thursday": "12:00 - 22:00",
                        "friday": "12:00 - 22:00",
                        "saturday": "12:00 - 22:00",
                        "sunday": "12:00 - 22:00"
                    },
                    "features": ["Strandnähe", "Gemütliche Atmosphäre", "Hundefreundlich"]
                }
            ]
        }
        
        await cursor.execute(locations_sql, (
            str(uuid.uuid4()),
            "Unsere Standorte",
            "Besuchen Sie uns in unseren beiden Restaurants an der Ostseeküste",
            json.dumps(locations_data),
            "system"
        ))
        print("   ✅ Locations Content erstellt")
        
        # 4. Legal Pages
        print("⚖️ Legal Pages...")
        legal_sql = """
            INSERT IGNORE INTO legal_pages (
                id, page_type, title, content, updated_by
            ) VALUES (%s, %s, %s, %s, %s)
        """
        
        # Impressum
        imprint_content = """
Angaben gemäß § 5 TMG:

Jimmy's Tapas Bar GmbH
Am Strande 21
23730 Neustadt in Holstein

Handelsregister: HRB 12345
Registergericht: Amtsgericht Hamburg

Vertreten durch:
Jimmy Rodríguez (Geschäftsführer)

Kontakt:
Telefon: +49 (0) 4561 123456
E-Mail: info@jimmys-tapasbar.de

Umsatzsteuer-ID:
Umsatzsteuer-Identifikationsnummer gemäß §27 a Umsatzsteuergesetz: DE123456789

Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV:
Jimmy Rodríguez
Am Strande 21
23730 Neustadt in Holstein
"""
        
        await cursor.execute(legal_sql, (
            str(uuid.uuid4()),
            "imprint",
            "Impressum",
            imprint_content,
            "system"
        ))
        
        # Datenschutz
        privacy_content = """
Datenschutzerklärung

1. Datenschutz auf einen Blick

Allgemeine Hinweise
Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie unsere Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können.

2. Allgemeine Hinweise und Pflichtinformationen

Datenschutz
Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzbestimmungen sowie dieser Datenschutzerklärung.

3. Datenerfassung auf unserer Website

Kontaktformular
Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem Anfrageformular inklusive der von Ihnen dort angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert.

Kontakt:
Datenschutzbeauftragter: Jimmy Rodríguez
E-Mail: datenschutz@jimmys-tapasbar.de
"""
        
        await cursor.execute(legal_sql, (
            str(uuid.uuid4()),
            "privacy",
            "Datenschutzerklärung",
            privacy_content,
            "system"
        ))
        print("   ✅ Legal Pages erstellt")
        
        # Commit changes
        await connection.commit()
        
        print("\n✅ CMS-DATEN VERVOLLSTÄNDIGUNG ABGESCHLOSSEN")
        print("=" * 50)
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler bei der CMS-Daten Vervollständigung: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(populate_cms_data())
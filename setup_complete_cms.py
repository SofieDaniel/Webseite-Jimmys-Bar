#!/usr/bin/env python3
"""
Setup Complete CMS Content for Jimmy's Tapas Bar
Erstellt ALLE fehlenden CMS-Inhalte
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

async def setup_complete_cms():
    """Setup all missing CMS content"""
    print("🏖️  Setting up COMPLETE CMS content for Jimmy's Tapas Bar")
    print("=" * 60)
    
    # Connect to MySQL
    connection = await aiomysql.connect(**mysql_config)
    cursor = await connection.cursor()
    
    try:
        # 1. Homepage Content
        await cursor.execute("SELECT COUNT(*) FROM homepage_content")
        homepage_count = (await cursor.fetchone())[0]
        if homepage_count == 0:
            print("🏠 Erstelle Homepage-Daten...")
            
            features_data = [
                {
                    "title": "Authentische Tapas",
                    "description": "Traditionelle spanische Tapas zubereitet mit original Zutaten",
                    "icon": "🍤",
                    "image": "https://images.unsplash.com/photo-1544025162-d76694265947"
                },
                {
                    "title": "Frische Meeresfrüchte",
                    "description": "Täglich frisch aus der Ostsee und dem Mittelmeer",
                    "icon": "🦞",
                    "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"
                },
                {
                    "title": "Strandlage",
                    "description": "Genießen Sie Ihr Essen mit direktem Blick auf die Ostsee",
                    "icon": "🏖️",
                    "image": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
                }
            ]
            
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
            
            delivery_data = {
                "title": "Lieferservice",
                "subtitle": "Spanische Köstlichkeiten direkt zu Ihnen",
                "delivery_time": "30-45 Min",
                "minimum_order": "15,00€",
                "delivery_fee": "2,50€",
                "areas": ["Neustadt in Holstein", "Großenbrode", "Umgebung"],
                "image": "https://images.unsplash.com/photo-1586816001966-79b736744398"
            }
            
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
            print("✅ Homepage-Daten erstellt")
        
        # 2. Legal Pages
        await cursor.execute("SELECT COUNT(*) FROM legal_pages")
        legal_count = (await cursor.fetchone())[0]
        if legal_count == 0:
            print("⚖️ Erstelle Impressum und Datenschutz...")
            
            # Impressum
            impressum_id = str(uuid.uuid4())
            impressum_content = """
            <h2>Angaben gemäß § 5 TMG</h2>
            <p><strong>Jimmy's Tapas Bar</strong><br>
            Jimmy Rodriguez<br>
            Strandstraße 12<br>
            23730 Neustadt in Holstein</p>
            
            <h3>Kontakt</h3>
            <p>Telefon: +49 4561 123456<br>
            E-Mail: info@jimmys-tapasbar.de</p>
            
            <h3>Umsatzsteuer-ID</h3>
            <p>Umsatzsteuer-Identifikationsnummer gemäß §27 a Umsatzsteuergesetz:<br>
            DE123456789</p>
            
            <h3>Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h3>
            <p>Jimmy Rodriguez<br>
            Strandstraße 12<br>
            23730 Neustadt in Holstein</p>
            """
            
            await cursor.execute("""
                INSERT INTO legal_pages (id, page_type, title, content, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                impressum_id, "imprint", "Impressum", impressum_content.strip(),
                datetime.now(), "system"
            ))
            
            # Datenschutz
            privacy_id = str(uuid.uuid4())
            privacy_content = """
            <h2>Datenschutzerklärung</h2>
            
            <h3>1. Datenschutz auf einen Blick</h3>
            <p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, 
            wenn Sie unsere Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können.</p>
            
            <h3>2. Allgemeine Hinweise und Pflichtinformationen</h3>
            <h4>Datenschutz</h4>
            <p>Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen 
            Daten vertraulich und entsprechend der gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.</p>
            
            <h3>3. Datenerfassung auf unserer Website</h3>
            <h4>Kontaktformular</h4>
            <p>Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem Anfrageformular inklusive 
            der von Ihnen dort angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert.</p>
            
            <h3>4. Ihre Rechte</h3>
            <p>Sie haben jederzeit das Recht unentgeltlich Auskunft über Herkunft, Empfänger und Zweck Ihrer gespeicherten 
            personenbezogenen Daten zu erhalten. Sie haben außerdem ein Recht, die Berichtigung, Sperrung oder Löschung dieser Daten zu verlangen.</p>
            """
            
            await cursor.execute("""
                INSERT INTO legal_pages (id, page_type, title, content, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                privacy_id, "privacy", "Datenschutzerklärung", privacy_content.strip(),
                datetime.now(), "system"
            ))
            print("✅ Impressum und Datenschutz erstellt")
        
        # 3. Locations Content (für CMS)
        await cursor.execute("SELECT COUNT(*) FROM locations")
        locations_count = (await cursor.fetchone())[0]
        if locations_count == 0:
            print("📍 Erstelle Locations-Daten...")
            
            locations_data = [
                {
                    "id": "neustadt",
                    "name": "Jimmy's Tapas Bar Neustadt",
                    "address": "Strandstraße 12, 23730 Neustadt in Holstein",
                    "phone": "+49 4561 123456",
                    "email": "neustadt@jimmys-tapasbar.de",
                    "opening_hours": {
                        "Montag": "16:00 - 23:00",
                        "Dienstag": "16:00 - 23:00",
                        "Mittwoch": "16:00 - 23:00",
                        "Donnerstag": "16:00 - 23:00",
                        "Freitag": "16:00 - 24:00",
                        "Samstag": "12:00 - 24:00",
                        "Sonntag": "12:00 - 23:00"
                    }
                },
                {
                    "id": "grossenbrode",
                    "name": "Jimmy's Tapas Bar Großenbrode",
                    "address": "Strandpromenade 8, 23775 Großenbrode",
                    "phone": "+49 4367 987654",
                    "email": "grossenbrode@jimmys-tapasbar.de",
                    "opening_hours": {
                        "Montag": "17:00 - 23:00",
                        "Dienstag": "17:00 - 23:00",
                        "Mittwoch": "17:00 - 23:00",
                        "Donnerstag": "17:00 - 23:00",
                        "Freitag": "17:00 - 24:00",
                        "Samstag": "12:00 - 24:00",
                        "Sonntag": "12:00 - 23:00"
                    }
                }
            ]
            
            locations_id = str(uuid.uuid4())
            await cursor.execute("""
                INSERT INTO locations (
                    id, page_title, page_description, locations_data,
                    updated_at, updated_by
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                locations_id,
                "Unsere Standorte",
                "Besuchen Sie uns an der malerischen Ostseeküste. Authentische spanische Küche mit Meerblick.",
                json.dumps(locations_data),
                datetime.now(),
                "system"
            ))
            print("✅ Locations-Daten erstellt")
        
        await cursor.close()
        connection.close()
        
        print("🎉 ALLE CMS-INHALTE ERFOLGREICH ERSTELLT!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen der CMS-Inhalte: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(setup_complete_cms())
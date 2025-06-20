#!/usr/bin/env python3
"""
Setup Kontakt-Seite CMS für Jimmy's Tapas Bar
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

async def setup_kontakt_cms():
    """Setup kontakt page CMS content"""
    print("📞 Setting up Kontakt Page CMS for Jimmy's Tapas Bar")
    print("=" * 60)
    
    # Connect to MySQL
    connection = await aiomysql.connect(**mysql_config)
    cursor = await connection.cursor()
    
    try:
        # Create kontakt_page table if it doesn't exist
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS kontakt_page (
                id VARCHAR(36) PRIMARY KEY,
                page_title VARCHAR(200) NOT NULL,
                page_subtitle TEXT NOT NULL,
                header_background VARCHAR(500) NOT NULL,
                contact_form_title VARCHAR(200) NOT NULL,
                contact_form_subtitle TEXT NOT NULL,
                locations_section_title VARCHAR(200) NOT NULL,
                opening_hours_title VARCHAR(200) NOT NULL,
                additional_info TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                updated_by VARCHAR(50) NOT NULL
            )
        """)
        print("✅ Kontakt-Tabelle erstellt/überprüft")
        
        # Clear existing data
        await cursor.execute("DELETE FROM kontakt_page")
        print("🗑️ Existierende Kontakt-Daten gelöscht")
        
        # Insert kontakt page content
        kontakt_id = str(uuid.uuid4())
        await cursor.execute("""
            INSERT INTO kontakt_page (
                id, page_title, page_subtitle, header_background,
                contact_form_title, contact_form_subtitle,
                locations_section_title, opening_hours_title,
                additional_info, updated_at, updated_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            kontakt_id,
            "Kontakt",
            "Nehmen Sie Kontakt mit uns auf",
            "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
            "Schreiben Sie uns",
            "Wir freuen uns auf Ihre Nachricht und melden uns schnellstmöglich bei Ihnen zurück.",
            "Unsere Standorte",
            "Öffnungszeiten",
            "Telefonische Reservierungen werden bevorzugt behandelt. Online-Reservierungen sind über unser Kontaktformular möglich.",
            datetime.now(),
            "system"
        ))
        
        print("✅ Kontakt-CMS-Daten erfolgreich erstellt!")
        print(f"   📄 Page title: Kontakt")
        print(f"   📧 Contact form: Schreiben Sie uns")
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen der Kontakt-CMS-Daten: {e}")
        raise
    finally:
        await cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(setup_kontakt_cms())
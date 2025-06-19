#!/usr/bin/env python3
"""
Datenbank-Initialisierung für Jimmy's Tapas Bar
Erstellt alle notwendigen Tabellen basierend auf den Backend-Modellen
"""

import asyncio
import aiomysql
import os
import json
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

async def init_database():
    """Initialisiert die Datenbank mit allen notwendigen Tabellen"""
    
    print("🚀 DATENBANK-INITIALISIERUNG - JIMMY'S TAPAS BAR")
    print("=" * 60)
    
    try:
        # Verbindung zur Datenbank herstellen
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        print("✅ Datenbankverbindung erfolgreich")
        
        # SQL für alle Tabellen
        tables_sql = {
            "status_checks": """
                CREATE TABLE IF NOT EXISTS status_checks (
                    id VARCHAR(36) PRIMARY KEY,
                    client_name VARCHAR(255) NOT NULL,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'editor', 'viewer') DEFAULT 'viewer',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "reviews": """
                CREATE TABLE IF NOT EXISTS reviews (
                    id VARCHAR(36) PRIMARY KEY,
                    customer_name VARCHAR(255) NOT NULL,
                    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    comment TEXT NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_approved BOOLEAN DEFAULT FALSE,
                    approved_by VARCHAR(100) NULL,
                    approved_at DATETIME NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "menu_items": """
                CREATE TABLE IF NOT EXISTS menu_items (
                    id VARCHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    price VARCHAR(20) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    image LONGTEXT NULL,
                    details TEXT NULL,
                    vegan BOOLEAN DEFAULT FALSE,
                    vegetarian BOOLEAN DEFAULT FALSE,
                    glutenfree BOOLEAN DEFAULT FALSE,
                    order_index INT DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "contact_messages": """
                CREATE TABLE IF NOT EXISTS contact_messages (
                    id VARCHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    phone VARCHAR(50) NULL,
                    subject VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT FALSE,
                    responded BOOLEAN DEFAULT FALSE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "maintenance_mode": """
                CREATE TABLE IF NOT EXISTS maintenance_mode (
                    id VARCHAR(36) PRIMARY KEY,
                    is_active BOOLEAN DEFAULT FALSE,
                    message TEXT DEFAULT 'Die Website befindet sich derzeit im Wartungsmodus.',
                    activated_by VARCHAR(100) NULL,
                    activated_at DATETIME NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "delivery_info": """
                CREATE TABLE IF NOT EXISTS delivery_info (
                    id VARCHAR(36) PRIMARY KEY,
                    delivery_time_min INT NOT NULL DEFAULT 30,
                    delivery_time_max INT NOT NULL DEFAULT 45,
                    minimum_order_value DECIMAL(10,2) NOT NULL DEFAULT 15.00,
                    delivery_fee DECIMAL(10,2) NOT NULL DEFAULT 2.50,
                    available_locations JSON NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    updated_by VARCHAR(100) NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "standorte_enhanced": """
                CREATE TABLE IF NOT EXISTS standorte_enhanced (
                    id VARCHAR(36) PRIMARY KEY,
                    page_title VARCHAR(255) NOT NULL,
                    page_subtitle TEXT NULL,
                    header_background TEXT NULL,
                    neustadt_data JSON NULL,
                    grossenbrode_data JSON NULL,
                    info_section_data JSON NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by VARCHAR(100) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "bewertungen_page": """
                CREATE TABLE IF NOT EXISTS bewertungen_page (
                    id VARCHAR(36) PRIMARY KEY,
                    page_title VARCHAR(255) NOT NULL,
                    page_subtitle TEXT NULL,
                    header_background TEXT NULL,
                    reviews_section_title VARCHAR(255) NOT NULL,
                    feedback_section_title VARCHAR(255) NOT NULL,
                    feedback_note TEXT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by VARCHAR(100) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "homepage_content": """
                CREATE TABLE IF NOT EXISTS homepage_content (
                    id VARCHAR(36) PRIMARY KEY,
                    hero_title VARCHAR(255) NOT NULL,
                    hero_subtitle TEXT NULL,
                    hero_description TEXT NULL,
                    hero_background TEXT NULL,
                    features_data JSON NULL,
                    specialties_data JSON NULL,
                    delivery_data JSON NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by VARCHAR(100) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "locations_content": """
                CREATE TABLE IF NOT EXISTS locations_content (
                    id VARCHAR(36) PRIMARY KEY,
                    page_title VARCHAR(255) NOT NULL,
                    page_description TEXT NULL,
                    locations_data JSON NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by VARCHAR(100) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "about_content": """
                CREATE TABLE IF NOT EXISTS about_content (
                    id VARCHAR(36) PRIMARY KEY,
                    hero_title VARCHAR(255) NOT NULL,
                    story_content TEXT NULL,
                    team_data JSON NULL,
                    values_data JSON NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by VARCHAR(100) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "legal_pages": """
                CREATE TABLE IF NOT EXISTS legal_pages (
                    id VARCHAR(36) PRIMARY KEY,
                    page_type ENUM('imprint', 'privacy') NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    content LONGTEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by VARCHAR(100) NOT NULL,
                    UNIQUE KEY unique_page_type (page_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
            "backups": """
                CREATE TABLE IF NOT EXISTS backups (
                    id VARCHAR(36) PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL,
                    type ENUM('database', 'full') NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_by VARCHAR(100) NOT NULL,
                    size_bytes BIGINT NULL,
                    size_human VARCHAR(20) NULL,
                    file_path TEXT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
        }
        
        # Tabellen erstellen
        print("\n📋 Erstelle Tabellen...")
        for table_name, sql in tables_sql.items():
            print(f"   - {table_name}...")
            await cursor.execute(sql)
            print(f"     ✅ {table_name} erstellt/überprüft")
        
        # Standard-Daten einfügen
        print("\n🔧 Füge Standard-Daten ein...")
        
        # Default admin user
        print("   - Admin-Benutzer...")
        admin_sql = """
            INSERT IGNORE INTO users (id, username, email, password_hash, role, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        import uuid
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        admin_hash = pwd_context.hash("jimmy2024")
        
        await cursor.execute(admin_sql, (
            str(uuid.uuid4()),
            "admin",
            "admin@jimmys-tapasbar.de", 
            admin_hash,
            "admin",
            True,
            datetime.utcnow()
        ))
        print("     ✅ Admin-Benutzer erstellt")
        
        # Default delivery info
        print("   - Lieferinformationen...")
        delivery_sql = """
            INSERT IGNORE INTO delivery_info (id, delivery_time_min, delivery_time_max, 
                                            minimum_order_value, delivery_fee, 
                                            available_locations, is_active, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        default_locations = {
            "neustadt": {
                "name": "Neustadt",
                "available": True,
                "address": "Am Strande 21, 23730 Neustadt in Holstein"
            },
            "grossenbrode": {
                "name": "Großenbrode", 
                "available": True,
                "address": "Südstrand 54, 23755 Großenbrode"
            }
        }
        
        await cursor.execute(delivery_sql, (
            str(uuid.uuid4()),
            30, 45, 15.00, 2.50,
            json.dumps(default_locations),
            True, "system"
        ))
        print("     ✅ Lieferinformationen erstellt")
        
        # Sample menu items
        print("   - Sample-Speisekarte...")
        menu_items = [
            {
                "id": str(uuid.uuid4()),
                "name": "Gambas al Ajillo",
                "description": "Garnelen in Knoblauchöl mit frischen Kräutern",
                "price": "12.90€",
                "category": "Tapas Calientes"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Patatas Bravas",
                "description": "Geröstete Kartoffeln mit scharfer Bravas-Sauce",
                "price": "7.50€",
                "category": "Tapas Calientes"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Patatas Bravas Especiales",
                "description": "Geröstete Kartoffeln mit Alioli und Bravas-Sauce",
                "price": "8.90€",
                "category": "Tapas Calientes"
            }
        ]
        
        menu_sql = """
            INSERT IGNORE INTO menu_items (id, name, description, price, category, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for item in menu_items:
            await cursor.execute(menu_sql, (
                item["id"], item["name"], item["description"], 
                item["price"], item["category"], True,
                datetime.utcnow(), datetime.utcnow()
            ))
        print("     ✅ Sample-Speisekarte erstellt")
        
        # Commit changes
        await connection.commit()
        
        print("\n✅ DATENBANK-INITIALISIERUNG ABGESCHLOSSEN")
        print("=" * 60)
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler bei der Datenbank-Initialisierung: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(init_database())
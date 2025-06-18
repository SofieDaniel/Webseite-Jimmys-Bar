#!/usr/bin/env python3
import mysql.connector
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv("/app/backend/.env")

# MySQL connection parameters
config = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'jimmy_user'),
    'password': os.environ.get('MYSQL_PASSWORD', 'jimmy2024_db'),
    'database': os.environ.get('MYSQL_DATABASE', 'jimmys_tapas_bar')
}

print(f"Connecting to MySQL database: {config['database']} on {config['host']}:{config['port']}")

try:
    # Connect to MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # Create tables
    tables = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('admin', 'editor', 'viewer') NOT NULL DEFAULT 'viewer',
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at DATETIME NOT NULL,
            last_login DATETIME NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS status_checks (
            id VARCHAR(36) PRIMARY KEY,
            client_name VARCHAR(100) NOT NULL,
            timestamp DATETIME NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id VARCHAR(36) PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            rating INT NOT NULL,
            comment TEXT NOT NULL,
            date DATETIME NOT NULL,
            is_approved BOOLEAN NOT NULL DEFAULT FALSE,
            approved_by VARCHAR(50) NULL,
            approved_at DATETIME NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS menu_items (
            id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            price VARCHAR(20) NOT NULL,
            category VARCHAR(50) NOT NULL,
            image TEXT NULL,
            details TEXT NULL,
            vegan BOOLEAN NOT NULL DEFAULT FALSE,
            vegetarian BOOLEAN NOT NULL DEFAULT FALSE,
            glutenfree BOOLEAN NOT NULL DEFAULT FALSE,
            order_index INT NOT NULL DEFAULT 0,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NULL,
            subject VARCHAR(200) NOT NULL,
            message TEXT NOT NULL,
            date DATETIME NOT NULL,
            is_read BOOLEAN NOT NULL DEFAULT FALSE,
            responded BOOLEAN NOT NULL DEFAULT FALSE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS maintenance_mode (
            id VARCHAR(36) PRIMARY KEY,
            is_active BOOLEAN NOT NULL DEFAULT FALSE,
            message TEXT NOT NULL,
            activated_by VARCHAR(50) NULL,
            activated_at DATETIME NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS homepage_content (
            id VARCHAR(36) PRIMARY KEY,
            hero_title VARCHAR(100) NOT NULL,
            hero_subtitle VARCHAR(100) NOT NULL,
            hero_description TEXT NOT NULL,
            hero_location VARCHAR(200) NOT NULL,
            hero_background_image TEXT NULL,
            hero_menu_button_text VARCHAR(50) NOT NULL,
            hero_locations_button_text VARCHAR(50) NOT NULL,
            features_data JSON NULL,
            specialties_data JSON NULL,
            delivery_data JSON NULL,
            updated_at DATETIME NOT NULL,
            updated_by VARCHAR(50) NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS locations (
            id VARCHAR(36) PRIMARY KEY,
            page_title VARCHAR(100) NOT NULL,
            page_description TEXT NOT NULL,
            locations_data JSON NOT NULL,
            updated_at DATETIME NOT NULL,
            updated_by VARCHAR(50) NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS about_content (
            id VARCHAR(36) PRIMARY KEY,
            page_title VARCHAR(100) NOT NULL,
            hero_title VARCHAR(100) NOT NULL,
            hero_description TEXT NOT NULL,
            story_title VARCHAR(100) NOT NULL,
            story_content TEXT NOT NULL,
            story_image TEXT NULL,
            team_title VARCHAR(100) NOT NULL,
            team_members JSON NOT NULL,
            values_title VARCHAR(100) NOT NULL,
            values_data JSON NOT NULL,
            updated_at DATETIME NOT NULL,
            updated_by VARCHAR(50) NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS legal_pages (
            id VARCHAR(36) PRIMARY KEY,
            page_type VARCHAR(20) NOT NULL,
            title VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            contact_name VARCHAR(100) NULL,
            contact_address TEXT NULL,
            contact_phone VARCHAR(20) NULL,
            contact_email VARCHAR(100) NULL,
            company_info JSON NULL,
            updated_at DATETIME NOT NULL,
            updated_by VARCHAR(50) NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS website_texts (
            id VARCHAR(36) PRIMARY KEY,
            section VARCHAR(20) NOT NULL,
            navigation_data JSON NULL,
            footer_data JSON NULL,
            buttons_data JSON NULL,
            general_data JSON NULL,
            updated_at DATETIME NOT NULL,
            updated_by VARCHAR(50) NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS content_sections (
            id VARCHAR(36) PRIMARY KEY,
            page VARCHAR(50) NOT NULL,
            section VARCHAR(50) NOT NULL,
            content JSON NOT NULL,
            images JSON NOT NULL,
            updated_at DATETIME NOT NULL,
            updated_by VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS system_backups (
            id VARCHAR(36) PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            type VARCHAR(20) NOT NULL,
            created_at DATETIME NOT NULL,
            created_by VARCHAR(50) NOT NULL,
            size_bytes BIGINT NOT NULL,
            size_human VARCHAR(20) NOT NULL,
            collections_count INT NOT NULL,
            total_documents INT NOT NULL,
            includes_media BOOLEAN NOT NULL DEFAULT FALSE
        )
        """
    ]
    
    # Create each table
    for table_query in tables:
        print(f"Creating table: {table_query.strip().split('CREATE TABLE IF NOT EXISTS')[1].split('(')[0].strip()}")
        cursor.execute(table_query)
    
    # Insert sample menu items
    menu_items = [
        {
            'name': 'Gambas al Ajillo',
            'description': 'Garnelen in Knoblauchöl',
            'price': '9,90 €',
            'category': 'TAPAS DE PESCADO',
            'vegan': False,
            'vegetarian': False,
            'glutenfree': True,
            'order_index': 1
        },
        {
            'name': 'Patatas Bravas',
            'description': 'Knusprige Kartoffelwürfel mit scharfer Tomatensoße',
            'price': '5,90 €',
            'category': 'TAPAS VEGETARIAN',
            'vegan': True,
            'vegetarian': True,
            'glutenfree': True,
            'order_index': 2
        },
        {
            'name': 'Patatas Bravas Especiales',
            'description': 'Knusprige Kartoffelwürfel mit scharfer Tomatensoße und Aioli',
            'price': '6,90 €',
            'category': 'TAPAS VEGETARIAN',
            'vegan': False,
            'vegetarian': True,
            'glutenfree': True,
            'order_index': 3
        },
        {
            'name': 'Paella Valenciana',
            'description': 'Traditionelle spanische Paella mit Huhn, Meeresfrüchten und Gemüse',
            'price': '14,90 €',
            'category': 'TAPA PAELLA',
            'vegan': False,
            'vegetarian': False,
            'glutenfree': True,
            'order_index': 4
        },
        {
            'name': 'Paella Vegetariana',
            'description': 'Vegetarische Paella mit saisonalem Gemüse',
            'price': '12,90 €',
            'category': 'TAPA PAELLA',
            'vegan': True,
            'vegetarian': True,
            'glutenfree': True,
            'order_index': 5
        }
    ]
    
    # Insert menu items
    for item in menu_items:
        cursor.execute("""
            INSERT IGNORE INTO menu_items 
            (id, name, description, price, category, vegan, vegetarian, glutenfree, order_index, is_active, created_at, updated_at)
            VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, TRUE, NOW(), NOW())
        """, (
            item['name'], 
            item['description'], 
            item['price'], 
            item['category'],
            item['vegan'],
            item['vegetarian'],
            item['glutenfree'],
            item['order_index']
        ))
    
    # Commit changes
    conn.commit()
    
    print("Database initialization completed successfully!")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    sys.exit(1)
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")
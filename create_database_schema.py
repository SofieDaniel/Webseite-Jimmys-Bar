#!/usr/bin/env python3
import asyncio
import aiomysql
import hashlib
import uuid

async def create_database_schema():
    """Create all necessary database tables for Jimmy's Tapas Bar"""
    
    connection = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='jimmy_user',
        password='jimmy2024_db',
        db='jimmys_tapas_bar',
        autocommit=True
    )
    
    cursor = await connection.cursor()
    
    try:
        # Create users table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100),
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Users table created")
        
        # Create menu_items table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                detailed_description TEXT,
                price VARCHAR(20),
                category VARCHAR(100),
                ingredients TEXT,
                origin VARCHAR(255),
                allergens TEXT,
                additives TEXT,
                preparation_method TEXT,
                vegetarian BOOLEAN DEFAULT FALSE,
                vegan BOOLEAN DEFAULT FALSE,
                glutenfree BOOLEAN DEFAULT FALSE,
                available BOOLEAN DEFAULT TRUE,
                order_index INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_menu_category (category),
                INDEX idx_menu_available (available),
                INDEX idx_menu_order (order_index)
            )
        ''')
        print("✅ Menu items table created")
        
        # Create homepage_content table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS homepage_content (
                id VARCHAR(36) PRIMARY KEY,
                hero_title VARCHAR(255),
                hero_subtitle VARCHAR(255),
                hero_description TEXT,
                hero_location VARCHAR(255),
                hero_background_image TEXT,
                hero_menu_button_text VARCHAR(100),
                hero_locations_button_text VARCHAR(100),
                features_data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Homepage content table created")
        
        # Create locations table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address TEXT,
                phone VARCHAR(50),
                email VARCHAR(100),
                opening_hours TEXT,
                features TEXT,
                image_url TEXT,
                active BOOLEAN DEFAULT TRUE,
                order_index INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Locations table created")
        
        # Create reviews table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id VARCHAR(36) PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
                review_text TEXT,
                date_visited DATE,
                approved BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_reviews_approved (approved),
                INDEX idx_reviews_rating (rating)
            )
        ''')
        print("✅ Reviews table created")
        
        # Create contact_messages table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                subject VARCHAR(255),
                message TEXT NOT NULL,
                read_status BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_contact_read (read_status),
                INDEX idx_contact_date (created_at)
            )
        ''')
        print("✅ Contact messages table created")
        
        # Create newsletter_subscribers table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                subscribed BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_newsletter_email (email),
                INDEX idx_newsletter_subscribed (subscribed)
            )
        ''')
        print("✅ Newsletter subscribers table created")
        
        # Create about_page_content table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS about_page_content (
                id VARCHAR(36) PRIMARY KEY,
                main_title VARCHAR(255),
                main_description TEXT,
                story_title VARCHAR(255),
                story_content TEXT,
                team_title VARCHAR(255),
                team_description TEXT,
                values_title VARCHAR(255),
                values_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("✅ About page content table created")
        
        # Create website_texts table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS website_texts (
                id VARCHAR(36) PRIMARY KEY,
                section VARCHAR(100) NOT NULL,
                content JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_section (section)
            )
        ''')
        print("✅ Website texts table created")
        
        # Create delivery_info table
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS delivery_info (
                id VARCHAR(36) PRIMARY KEY,
                delivery_time_min INT DEFAULT 30,
                delivery_time_max INT DEFAULT 45,
                min_order_amount DECIMAL(10,2) DEFAULT 15.00,
                delivery_fee DECIMAL(10,2) DEFAULT 2.50,
                free_delivery_threshold DECIMAL(10,2) DEFAULT 30.00,
                delivery_areas TEXT,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Delivery info table created")
        
        # Create admin user
        admin_id = str(uuid.uuid4())
        password_hash = hashlib.md5("jimmy2024".encode()).hexdigest()
        
        await cursor.execute('''
            INSERT IGNORE INTO users (id, username, email, password_hash, role, is_active) 
            VALUES (%s, 'admin', 'admin@jimmystapasbar.com', %s, 'admin', TRUE)
        ''', (admin_id, password_hash))
        print("✅ Admin user created (username: admin, password: jimmy2024)")
        
        # Create default homepage content
        homepage_id = str(uuid.uuid4())
        await cursor.execute('''
            INSERT IGNORE INTO homepage_content 
            (id, hero_title, hero_subtitle, hero_description, features_data) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            homepage_id,
            "JIMMY'S TAPAS BAR",
            "an der Ostsee",
            "Genießen Sie authentische mediterrane Spezialitäten direkt an der malerischen Ostseeküste",
            '{"features": []}'
        ))
        print("✅ Default homepage content created")
        
        # Create default delivery info
        delivery_id = str(uuid.uuid4())
        await cursor.execute('''
            INSERT IGNORE INTO delivery_info 
            (id, delivery_time_min, delivery_time_max, min_order_amount, delivery_fee) 
            VALUES (%s, 30, 45, 15.00, 2.50)
        ''', (delivery_id,))
        print("✅ Default delivery info created")
        
        print("\n🎉 Database schema created successfully!")
        print("   - Admin login: admin / jimmy2024")
        print("   - All tables are ready for the CMS")
        
    except Exception as e:
        print(f"❌ Error creating database schema: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(create_database_schema())
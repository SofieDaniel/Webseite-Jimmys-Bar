#!/usr/bin/env python3
"""
Jimmy's Tapas Bar CMS - MongoDB to MySQL Migration Script
Migrates all data from MongoDB to the new MySQL database structure.
"""

import asyncio
import json
import aiomysql
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
mongo_client = AsyncIOMotorClient(mongo_url)
mongo_db = mongo_client[os.environ['DB_NAME']]

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

async def get_mysql_connection():
    return await aiomysql.connect(**mysql_config)

def convert_datetime(value):
    """Convert datetime objects to string format for JSON storage"""
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, dict):
        return {k: convert_datetime(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_datetime(item) for item in value]
    return value

async def migrate_users():
    """Migrate users from MongoDB to MySQL"""
    print("🔄 Migrating users...")
    
    # Get all users from MongoDB
    users = await mongo_db.users.find({}).to_list(length=None)
    
    if not users:
        print("   ✅ No users found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        migrated_count = 0
        for user in users:
            try:
                # Remove MongoDB ObjectId
                if '_id' in user:
                    del user['_id']
                
                await cursor.execute("""
                    INSERT INTO users (id, username, email, password_hash, role, is_active, created_at, last_login)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    email = VALUES(email), password_hash = VALUES(password_hash), 
                    role = VALUES(role), is_active = VALUES(is_active)
                """, (
                    user.get('id'), user.get('username'), user.get('email'),
                    user.get('password_hash'), user.get('role', 'viewer'),
                    user.get('is_active', True), user.get('created_at'),
                    user.get('last_login')
                ))
                migrated_count += 1
            except Exception as e:
                print(f"   ❌ Error migrating user {user.get('username', 'unknown')}: {e}")
        
        print(f"   ✅ Migrated {migrated_count} users")
    finally:
        mysql_conn.close()

async def migrate_reviews():
    """Migrate reviews from MongoDB to MySQL"""
    print("🔄 Migrating reviews...")
    
    reviews = await mongo_db.reviews.find({}).to_list(length=None)
    
    if not reviews:
        print("   ✅ No reviews found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        migrated_count = 0
        for review in reviews:
            try:
                if '_id' in review:
                    del review['_id']
                
                await cursor.execute("""
                    INSERT INTO reviews (id, customer_name, rating, comment, date, is_approved, approved_by, approved_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    customer_name = VALUES(customer_name), rating = VALUES(rating),
                    comment = VALUES(comment), is_approved = VALUES(is_approved)
                """, (
                    review.get('id'), review.get('customer_name'), review.get('rating'),
                    review.get('comment'), review.get('date'), review.get('is_approved', False),
                    review.get('approved_by'), review.get('approved_at')
                ))
                migrated_count += 1
            except Exception as e:
                print(f"   ❌ Error migrating review {review.get('id', 'unknown')}: {e}")
        
        print(f"   ✅ Migrated {migrated_count} reviews")
    finally:
        mysql_conn.close()

async def migrate_menu_items():
    """Migrate menu items from MongoDB to MySQL"""
    print("🔄 Migrating menu items...")
    
    menu_items = await mongo_db.menu_items.find({}).to_list(length=None)
    
    if not menu_items:
        print("   ✅ No menu items found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        migrated_count = 0
        for item in menu_items:
            try:
                if '_id' in item:
                    del item['_id']
                
                await cursor.execute("""
                    INSERT INTO menu_items (id, name, description, price, category, image, details,
                                           vegan, vegetarian, glutenfree, order_index, is_active,
                                           created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name), description = VALUES(description), price = VALUES(price),
                    category = VALUES(category), image = VALUES(image), details = VALUES(details),
                    vegan = VALUES(vegan), vegetarian = VALUES(vegetarian), 
                    glutenfree = VALUES(glutenfree), order_index = VALUES(order_index),
                    is_active = VALUES(is_active), updated_at = VALUES(updated_at)
                """, (
                    item.get('id'), item.get('name'), item.get('description'),
                    item.get('price'), item.get('category'), item.get('image'),
                    item.get('details'), item.get('vegan', False),
                    item.get('vegetarian', False), item.get('glutenfree', False),
                    item.get('order_index', 0), item.get('is_active', True),
                    item.get('created_at'), item.get('updated_at')
                ))
                migrated_count += 1
            except Exception as e:
                print(f"   ❌ Error migrating menu item {item.get('name', 'unknown')}: {e}")
        
        print(f"   ✅ Migrated {migrated_count} menu items")
    finally:
        mysql_conn.close()

async def migrate_contact_messages():
    """Migrate contact messages from MongoDB to MySQL"""
    print("🔄 Migrating contact messages...")
    
    messages = await mongo_db.contact_messages.find({}).to_list(length=None)
    
    if not messages:
        print("   ✅ No contact messages found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        migrated_count = 0
        for message in messages:
            try:
                if '_id' in message:
                    del message['_id']
                
                await cursor.execute("""
                    INSERT INTO contact_messages (id, name, email, phone, subject, message, date, is_read, responded)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name), email = VALUES(email), phone = VALUES(phone),
                    subject = VALUES(subject), message = VALUES(message), 
                    is_read = VALUES(is_read), responded = VALUES(responded)
                """, (
                    message.get('id'), message.get('name'), message.get('email'),
                    message.get('phone'), message.get('subject'), message.get('message'),
                    message.get('date'), message.get('is_read', False),
                    message.get('responded', False)
                ))
                migrated_count += 1
            except Exception as e:
                print(f"   ❌ Error migrating contact message {message.get('id', 'unknown')}: {e}")
        
        print(f"   ✅ Migrated {migrated_count} contact messages")
    finally:
        mysql_conn.close()

async def migrate_homepage_content():
    """Migrate homepage content from MongoDB to MySQL"""
    print("🔄 Migrating homepage content...")
    
    content = await mongo_db.homepage_content.find_one()
    
    if not content:
        print("   ✅ No homepage content found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        if '_id' in content:
            del content['_id']
        
        # Convert nested objects to JSON strings
        hero_data = content.get('hero', {})
        features_data = content.get('features', {})
        specialties_data = content.get('specialties', {})
        delivery_data = content.get('delivery', {})
        
        await cursor.execute("""
            INSERT INTO homepage_content (id, hero_title, hero_subtitle, hero_description,
                                         hero_location, hero_background_image, hero_menu_button_text,
                                         hero_locations_button_text, features_data, specialties_data,
                                         delivery_data, updated_at, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            hero_title = VALUES(hero_title), hero_subtitle = VALUES(hero_subtitle),
            hero_description = VALUES(hero_description), hero_location = VALUES(hero_location),
            features_data = VALUES(features_data), specialties_data = VALUES(specialties_data),
            delivery_data = VALUES(delivery_data), updated_at = VALUES(updated_at)
        """, (
            content.get('id'), hero_data.get('title', 'JIMMY\'S TAPAS BAR'),
            hero_data.get('subtitle', 'an der Ostsee'),
            hero_data.get('description', 'Genießen Sie authentische mediterrane Spezialitäten'),
            hero_data.get('location', 'direkt an der malerischen Ostseeküste'),
            hero_data.get('background_image'),
            hero_data.get('menu_button_text', 'Zur Speisekarte'),
            hero_data.get('locations_button_text', 'Unsere Standorte'),
            json.dumps(convert_datetime(features_data)),
            json.dumps(convert_datetime(specialties_data)),
            json.dumps(convert_datetime(delivery_data)),
            content.get('updated_at'), content.get('updated_by')
        ))
        
        print("   ✅ Migrated homepage content")
    except Exception as e:
        print(f"   ❌ Error migrating homepage content: {e}")
    finally:
        mysql_conn.close()

async def migrate_locations():
    """Migrate locations content from MongoDB to MySQL"""
    print("🔄 Migrating locations...")
    
    content = await mongo_db.locations.find_one()
    
    if not content:
        print("   ✅ No locations found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        if '_id' in content:
            del content['_id']
        
        await cursor.execute("""
            INSERT INTO locations (id, page_title, page_description, locations_data, updated_at, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            page_title = VALUES(page_title), page_description = VALUES(page_description),
            locations_data = VALUES(locations_data), updated_at = VALUES(updated_at)
        """, (
            content.get('id'), content.get('page_title', 'Unsere Standorte'),
            content.get('page_description', 'Besuchen Sie uns an einem unserer beiden Standorte'),
            json.dumps(convert_datetime(content.get('locations', []))),
            content.get('updated_at'), content.get('updated_by')
        ))
        
        print("   ✅ Migrated locations content")
    except Exception as e:
        print(f"   ❌ Error migrating locations: {e}")
    finally:
        mysql_conn.close()

async def migrate_about_content():
    """Migrate about content from MongoDB to MySQL"""
    print("🔄 Migrating about content...")
    
    content = await mongo_db.about_content.find_one()
    
    if not content:
        print("   ✅ No about content found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        if '_id' in content:
            del content['_id']
        
        await cursor.execute("""
            INSERT INTO about_content (id, page_title, hero_title, hero_description, story_title,
                                     story_content, story_image, team_title, team_members,
                                     values_title, values_data, updated_at, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            page_title = VALUES(page_title), hero_title = VALUES(hero_title),
            hero_description = VALUES(hero_description), story_title = VALUES(story_title),
            story_content = VALUES(story_content), story_image = VALUES(story_image),
            team_title = VALUES(team_title), team_members = VALUES(team_members),
            values_title = VALUES(values_title), values_data = VALUES(values_data),
            updated_at = VALUES(updated_at)
        """, (
            content.get('id'), content.get('page_title', 'Über uns'),
            content.get('hero_title', 'Unsere Geschichte'),
            content.get('hero_description', 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar'),
            content.get('story_title', 'Unsere Leidenschaft'),
            content.get('story_content', ''), content.get('story_image'),
            content.get('team_title', 'Unser Team'),
            json.dumps(convert_datetime(content.get('team_members', []))),
            content.get('values_title', 'Unsere Werte'),
            json.dumps(convert_datetime(content.get('values', []))),
            content.get('updated_at'), content.get('updated_by')
        ))
        
        print("   ✅ Migrated about content")
    except Exception as e:
        print(f"   ❌ Error migrating about content: {e}")
    finally:
        mysql_conn.close()

async def migrate_legal_pages():
    """Migrate legal pages from MongoDB to MySQL"""
    print("🔄 Migrating legal pages...")
    
    pages = await mongo_db.legal_pages.find({}).to_list(length=None)
    
    if not pages:
        print("   ✅ No legal pages found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        migrated_count = 0
        for page in pages:
            try:
                if '_id' in page:
                    del page['_id']
                
                await cursor.execute("""
                    INSERT INTO legal_pages (id, page_type, title, content, contact_name,
                                           contact_address, contact_phone, contact_email,
                                           company_info, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    title = VALUES(title), content = VALUES(content),
                    contact_name = VALUES(contact_name), contact_address = VALUES(contact_address),
                    contact_phone = VALUES(contact_phone), contact_email = VALUES(contact_email),
                    company_info = VALUES(company_info), updated_at = VALUES(updated_at)
                """, (
                    page.get('id'), page.get('page_type'), page.get('title'),
                    page.get('content'), page.get('contact_name'),
                    page.get('contact_address'), page.get('contact_phone'),
                    page.get('contact_email'),
                    json.dumps(convert_datetime(page.get('company_info', {}))),
                    page.get('updated_at'), page.get('updated_by')
                ))
                migrated_count += 1
            except Exception as e:
                print(f"   ❌ Error migrating legal page {page.get('page_type', 'unknown')}: {e}")
        
        print(f"   ✅ Migrated {migrated_count} legal pages")
    finally:
        mysql_conn.close()

async def migrate_website_texts():
    """Migrate website texts from MongoDB to MySQL"""
    print("🔄 Migrating website texts...")
    
    texts = await mongo_db.website_texts.find({}).to_list(length=None)
    
    if not texts:
        print("   ✅ No website texts found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        migrated_count = 0
        for text in texts:
            try:
                if '_id' in text:
                    del text['_id']
                
                await cursor.execute("""
                    INSERT INTO website_texts (id, section, navigation_data, footer_data,
                                             buttons_data, general_data, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    navigation_data = VALUES(navigation_data), footer_data = VALUES(footer_data),
                    buttons_data = VALUES(buttons_data), general_data = VALUES(general_data),
                    updated_at = VALUES(updated_at)
                """, (
                    text.get('id'), text.get('section'),
                    json.dumps(convert_datetime(text.get('navigation', {}))),
                    json.dumps(convert_datetime(text.get('footer', {}))),
                    json.dumps(convert_datetime(text.get('buttons', {}))),
                    json.dumps(convert_datetime(text.get('general', {}))),
                    text.get('updated_at'), text.get('updated_by')
                ))
                migrated_count += 1
            except Exception as e:
                print(f"   ❌ Error migrating website text {text.get('section', 'unknown')}: {e}")
        
        print(f"   ✅ Migrated {migrated_count} website text sections")
    finally:
        mysql_conn.close()

async def migrate_status_checks():
    """Migrate status checks from MongoDB to MySQL"""
    print("🔄 Migrating status checks...")
    
    status_checks = await mongo_db.status_checks.find({}).sort("timestamp", -1).limit(100).to_list(length=None)
    
    if not status_checks:
        print("   ✅ No status checks found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        migrated_count = 0
        for check in status_checks:
            try:
                if '_id' in check:
                    del check['_id']
                
                await cursor.execute("""
                    INSERT INTO status_checks (id, client_name, timestamp)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    client_name = VALUES(client_name), timestamp = VALUES(timestamp)
                """, (
                    check.get('id'), check.get('client_name'), check.get('timestamp')
                ))
                migrated_count += 1
            except Exception as e:
                print(f"   ❌ Error migrating status check {check.get('id', 'unknown')}: {e}")
        
        print(f"   ✅ Migrated {migrated_count} status checks")
    finally:
        mysql_conn.close()

async def migrate_maintenance_mode():
    """Migrate maintenance mode from MongoDB to MySQL"""
    print("🔄 Migrating maintenance mode...")
    
    maintenance = await mongo_db.maintenance_mode.find_one()
    
    if not maintenance:
        print("   ✅ No maintenance mode found in MongoDB")
        return
    
    mysql_conn = await get_mysql_connection()
    try:
        cursor = await mysql_conn.cursor()
        
        if '_id' in maintenance:
            del maintenance['_id']
        
        await cursor.execute("""
            INSERT INTO maintenance_mode (id, is_active, message, activated_by, activated_at)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            is_active = VALUES(is_active), message = VALUES(message),
            activated_by = VALUES(activated_by), activated_at = VALUES(activated_at)
        """, (
            maintenance.get('id', '1'), maintenance.get('is_active', False),
            maintenance.get('message', 'Die Website befindet sich derzeit im Wartungsmodus.'),
            maintenance.get('activated_by'), maintenance.get('activated_at')
        ))
        
        print("   ✅ Migrated maintenance mode")
    except Exception as e:
        print(f"   ❌ Error migrating maintenance mode: {e}")
    finally:
        mysql_conn.close()

async def main():
    """Main migration function"""
    print("🚀 Starting MongoDB to MySQL migration for Jimmy's Tapas Bar CMS")
    print("=" * 60)
    
    try:
        # Test MySQL connection
        mysql_conn = await get_mysql_connection()
        mysql_conn.close()
        print("✅ MySQL connection test successful")
        
        # Test MongoDB connection
        await mongo_db.list_collection_names()
        print("✅ MongoDB connection test successful")
        print()
        
        # Run migrations
        await migrate_users()
        await migrate_reviews()
        await migrate_menu_items()
        await migrate_contact_messages()
        await migrate_homepage_content()
        await migrate_locations()
        await migrate_about_content()
        await migrate_legal_pages()
        await migrate_website_texts()
        await migrate_status_checks()
        await migrate_maintenance_mode()
        
        print()
        print("=" * 60)
        print("🎉 Migration completed successfully!")
        print()
        print("📋 Next steps:")
        print("1. Verify data in MySQL database")
        print("2. Test the new MySQL-based backend")
        print("3. Update frontend to use new backend")
        print("4. Create backup of the migrated data")
        print("5. Consider decommissioning MongoDB after verification")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        # Close MongoDB connection
        mongo_client.close()

if __name__ == "__main__":
    asyncio.run(main())
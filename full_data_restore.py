#!/usr/bin/env python3
import asyncio
import aiomysql
import json
import uuid
from passlib.context import CryptContext

async def full_restore():
    """Completely restore ALL original data"""
    
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
        print("🔄 Starting FULL DATA RESTORATION...")
        
        # 1. ADMIN USER
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        admin_password_hash = pwd_context.hash('jimmy2024')
        admin_id = str(uuid.uuid4())
        
        await cursor.execute('DELETE FROM users WHERE username = "admin"')
        await cursor.execute('''
            INSERT INTO users (id, username, email, password_hash, role, is_active, last_login) 
            VALUES (%s, 'admin', 'admin@jimmystapasbar.com', %s, 'admin', TRUE, NULL)
        ''', (admin_id, admin_password_hash))
        print("✅ Admin user restored")
        
        # 2. HOMEPAGE CONTENT
        await cursor.execute('DELETE FROM homepage_content')
        homepage_id = str(uuid.uuid4())
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
                    "title": "Gemütliche Atmosphäre",
                    "description": "Entspannen Sie in unserem einladenden Restaurant mit authentisch spanischem Flair",
                    "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae"
                }
            ]
        }
        
        await cursor.execute('''
            INSERT INTO homepage_content 
            (id, hero_title, hero_subtitle, hero_description, hero_location, hero_background_image, 
             hero_menu_button_text, hero_locations_button_text, features_data) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            homepage_id,
            "JIMMY'S TAPAS BAR",
            "an der Ostsee",
            "Genießen Sie authentische mediterrane Spezialitäten direkt an der malerischen Ostseeküste",
            "Zingst, Deutschland",
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0",
            "Zur Speisekarte",
            "Unsere Standorte",
            json.dumps(features_data)
        ))
        print("✅ Homepage content restored")
        
        # 3. LOCATIONS
        await cursor.execute('DELETE FROM locations')
        location_id = str(uuid.uuid4())
        await cursor.execute('''
            INSERT INTO locations 
            (id, name, address, phone, email, opening_hours, features, image_url, active, order_index) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            location_id,
            "Jimmy's Tapas Bar Zingst",
            "Strandpromenade 15, 18374 Zingst",
            "+49 38232 15678",
            "info@jimmystapasbar.com",
            "Montag - Sonntag: 11:00 - 23:00",
            "Meerblick, Terrasse, Parkplätze verfügbar, Reservierungen möglich",
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0",
            True,
            1
        ))
        print("✅ Locations restored")
        
        # 4. STANDORTE ENHANCED
        await cursor.execute('DELETE FROM standorte_enhanced')
        standorte_id = str(uuid.uuid4())
        standorte_data = {
            "page_title": "Unsere Standorte",
            "page_subtitle": "Besuchen Sie uns an der malerischen Ostseeküste",
            "page_description": "Erleben Sie authentische spanische Küche in unserem Restaurant direkt am Strand von Zingst",
            "locations": [
                {
                    "id": location_id,
                    "name": "Jimmy's Tapas Bar Zingst",
                    "address": "Strandpromenade 15, 18374 Zingst",
                    "phone": "+49 38232 15678",
                    "email": "info@jimmystapasbar.com", 
                    "hours": "Montag - Sonntag: 11:00 - 23:00",
                    "features": ["Meerblick", "Terrasse", "Parkplätze"],
                    "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0",
                    "coordinates": {"lat": 54.4389, "lng": 12.6806},
                    "description": "Unser Hauptstandort direkt an der Strandpromenade von Zingst bietet Ihnen nicht nur exzellente Tapas, sondern auch einen atemberaubenden Blick auf die Ostsee."
                }
            ]
        }
        
        await cursor.execute('''
            INSERT INTO standorte_enhanced (id, name, data) 
            VALUES (%s, 'main_locations', %s)
        ''', (standorte_id, json.dumps(standorte_data)))
        print("✅ Standorte enhanced restored")
        
        # 5. ABOUT PAGE
        await cursor.execute('DELETE FROM about_page_content')
        about_id = str(uuid.uuid4())
        await cursor.execute('''
            INSERT INTO about_page_content 
            (id, main_title, main_description, story_title, story_content, team_title, team_description, values_title, values_content) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            about_id,
            "Über Jimmy's Tapas Bar",
            "Seit 2018 servieren wir authentische spanische Tapas an der wunderschönen Ostseeküste.",
            "Unsere Geschichte",
            "Jimmy's Tapas Bar wurde 2018 von einem leidenschaftlichen Koch gegründet, der seine Liebe zur spanischen Küche mit der Schönheit der deutschen Ostseeküste verbinden wollte. Was als kleiner Traum begann, hat sich zu einem beliebten Treffpunkt für Einheimische und Touristen entwickelt.",
            "Unser Team",
            "Unser erfahrenes Team besteht aus leidenschaftlichen Köchen und freundlichem Service-Personal, die alle ein Ziel haben: Ihnen ein unvergessliches kulinarisches Erlebnis zu bieten.",
            "Unsere Werte",
            "Wir glauben an frische, qualitativ hochwertige Zutaten, authentische Zubereitungsmethoden und herzliche Gastfreundschaft. Jedes Gericht wird mit Liebe zum Detail zubereitet."
        ))
        print("✅ About page content restored")
        
        # 6. BEWERTUNGEN PAGE
        await cursor.execute('DELETE FROM bewertungen_page')
        bewertungen_id = str(uuid.uuid4())
        await cursor.execute('''
            INSERT INTO bewertungen_page (id, title, subtitle, description) 
            VALUES (%s, %s, %s, %s)
        ''', (
            bewertungen_id,
            "Bewertungen",
            "Was unsere Gäste sagen",
            "Lesen Sie authentische Bewertungen unserer Gäste und erfahren Sie, warum Jimmy's Tapas Bar der perfekte Ort für ein unvergessliches kulinarisches Erlebnis ist."
        ))
        print("✅ Bewertungen page restored")
        
        # 7. DELIVERY INFO
        await cursor.execute('DELETE FROM delivery_info')
        delivery_id = str(uuid.uuid4())
        await cursor.execute('''
            INSERT INTO delivery_info 
            (id, delivery_time_min, delivery_time_max, min_order_amount, delivery_fee, free_delivery_threshold, delivery_areas, active) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            delivery_id, 30, 45, 15.00, 2.50, 30.00, 
            "Zingst, Prerow, Born, Wieck, Bresewitz",
            True
        ))
        print("✅ Delivery info restored")
        
        # 8. WEBSITE TEXTS
        await cursor.execute('DELETE FROM website_texts')
        
        # Navigation texts
        nav_id = str(uuid.uuid4())
        nav_content = {
            "brand_name": "Jimmy's Tapas Bar",
            "menu_items": [
                {"name": "Startseite", "href": "/"},
                {"name": "Standorte", "href": "/standorte"},
                {"name": "Speisekarte", "href": "/speisekarte"},
                {"name": "Bewertungen", "href": "/bewertungen"},
                {"name": "Über uns", "href": "/ueber-uns"},
                {"name": "Kontakt", "href": "/kontakt"}
            ]
        }
        
        await cursor.execute('''
            INSERT INTO website_texts (id, section, content) 
            VALUES (%s, 'navigation', %s)
        ''', (nav_id, json.dumps(nav_content)))
        
        # Footer texts
        footer_id = str(uuid.uuid4())
        footer_content = {
            "company_name": "Jimmy's Tapas Bar",
            "tagline": "Authentische spanische Küche an der Ostsee",
            "address": "Strandpromenade 15, 18374 Zingst",
            "phone": "+49 38232 15678",
            "email": "info@jimmystapasbar.com",
            "opening_hours": "Mo-So: 11:00-23:00",
            "social_media": {
                "facebook": "#",
                "instagram": "#",
                "tripadvisor": "#"
            },
            "newsletter_title": "Newsletter",
            "newsletter_description": "Erhalten Sie Updates zu neuen Gerichten und Events",
            "legal_links": [
                {"name": "Impressum", "href": "/impressum"},
                {"name": "Datenschutz", "href": "/datenschutz"}
            ]
        }
        
        await cursor.execute('''
            INSERT INTO website_texts (id, section, content) 
            VALUES (%s, 'footer', %s)
        ''', (footer_id, json.dumps(footer_content)))
        print("✅ Website texts restored")
        
        print("\n🎉 ALL CORE DATA RESTORED SUCCESSFULLY!")
        print("   Next: Menu items will be restored...")
        
    except Exception as e:
        print(f"❌ Error during restoration: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(full_restore())
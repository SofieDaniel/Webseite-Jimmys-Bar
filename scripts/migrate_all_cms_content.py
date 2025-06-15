#!/usr/bin/env python3
"""
Vollständige Migration aller CMS-Inhalte für Jimmy's Tapas Bar
Befüllt alle Content-Bereiche mit authentischen spanischen Inhalten
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

# CMS CONTENT DATA - Alle Bereiche vollständig auf Deutsch
CMS_CONTENT_DATA = {
    # Homepage Hero Section
    'homepage_hero': {
        'title': 'AUTÉNTICO SABOR ESPAÑOL',
        'subtitle': 'an der Ostsee',
        'description': 'Genießen Sie authentische spanische Spezialitäten direkt an der malerischen Ostseeküste',
        'location_text': 'Warnemünde & Kühlungsborn',
        'menu_button_text': 'Zur Speisekarte',
        'locations_button_text': 'Unsere Standorte',
        'background_image': 'https://images.unsplash.com/photo-1656423521731-9665583f100c'
    },
    
    # Homepage Features Section
    'homepage_features': {
        'section_title': 'Authentische Spanische Küche',
        'section_description': 'Erleben Sie die Geschmacksvielfalt Spaniens in gemütlicher Atmosphäre',
        'features': [
            {
                'title': 'Traditionelle Tapas',
                'description': 'Original spanische Tapas nach Familienrezepten aus Valencia und Andalusien',
                'image_url': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
                'image_alt': 'Spanische Tapas Variation'
            },
            {
                'title': 'Frische Paella',
                'description': 'Authentische Paella mit Bomba-Reis und echtem Safran aus Valencia',
                'image_url': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e',
                'image_alt': 'Traditionelle Paella'
            },
            {
                'title': 'Spanische Weine',
                'description': 'Erlesene Weine aus Rioja, Ribera del Duero und anderen spanischen Regionen',
                'image_url': 'https://images.unsplash.com/photo-1567522693444-038749b0f0ed',
                'image_alt': 'Spanische Weine'
            }
        ]
    },
    
    # Homepage Food Gallery
    'homepage_food_gallery': {
        'section_title': 'Unsere Spezialitäten',
        'gallery_items': [
            {
                'name': 'Jamón Ibérico',
                'description': 'Edler Iberico-Schinken aus Extremadura',
                'image_url': 'https://images.unsplash.com/photo-1598989519542-077da0f51c09',
                'category_link': '#inicio'
            },
            {
                'name': 'Gambas al Ajillo',
                'description': 'Garnelen in Knoblauchöl',
                'image_url': 'https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg',
                'category_link': '#tapas-pescado'
            },
            {
                'name': 'Tortilla Española',
                'description': 'Klassisches Kartoffel-Omelett',
                'image_url': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
                'category_link': '#tapas-vegetarian'
            },
            {
                'name': 'Paella Valenciana',
                'description': 'Original Paella aus Valencia',
                'image_url': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e',
                'category_link': '#tapa-paella'
            }
        ]
    },
    
    # Homepage Lieferando Section
    'homepage_lieferando': {
        'title': 'Jetzt auch Lieferservice',
        'description': 'Genießen Sie unsere spanischen Spezialitäten bequem zu Hause',
        'delivery_text': 'Schnelle Lieferung',
        'button_text': 'Bei Lieferando bestellen',
        'availability_text': 'Täglich 16:00 - 22:00 Uhr verfügbar',
        'authentic_text': 'Authentisch Spanisch',
        'lieferando_url': 'https://www.lieferando.de'
    },
    
    # About Us Content
    'about_content': {
        'page_title': 'Über Jimmy\'s Tapas Bar',
        'hero_title': 'Unsere Geschichte',
        'hero_description': 'Seit 2020 bringen wir authentische spanische Küche an die deutsche Ostseeküste',
        'hero_image': 'https://images.unsplash.com/photo-1559329007-40df8766a171',
        'story_title': 'Die Geschichte von Jimmy\'s',
        'story_content': '''
        <p>Jimmy's Tapas Bar wurde 2020 mit der Vision gegründet, authentische spanische Küche an die deutsche Ostseeküste zu bringen. Unser Gründer Jimmy verbrachte viele Jahre in Valencia und Andalusien, wo er die traditionelle Kunst der Tapas-Zubereitung erlernte.</p>
        
        <p>Heute führen wir zwei Standorte in Warnemünde und Kühlungsborn, wo wir täglich frische Tapas nach original spanischen Familienrezepten zubereiten. Unsere Zutaten importieren wir direkt aus Spanien - von Pimentón de la Vera über Jamón Ibérico bis hin zum echten Bomba-Reis für unsere Paellas.</p>
        
        <p>Bei uns erwartet Sie nicht nur ausgezeichnetes Essen, sondern auch die typisch spanische Gemütlichkeit und Gastfreundschaft. ¡Bienvenidos a nuestra casa!</p>
        ''',
        'team_title': 'Unser Team',
        'team_description': 'Leidenschaftliche Köche mit spanischen Wurzeln',
        'values_title': 'Unsere Werte',
        'values': [
            {
                'title': 'Authentizität',
                'description': 'Wir verwenden nur original spanische Rezepte und Zutaten',
                'icon': '🇪🇸'
            },
            {
                'title': 'Qualität',
                'description': 'Frische, hochwertige Produkte direkt aus Spanien',
                'icon': '⭐'
            },
            {
                'title': 'Gastfreundschaft',
                'description': 'Spanische Herzlichkeit und familiäre Atmosphäre',
                'icon': '❤️'
            }
        ]
    },
    
    # Contact & Legal Content
    'contact_legal': {
        'contact_title': 'Kontakt',
        'contact_description': 'Besuchen Sie uns in Warnemünde oder Kühlungsborn',
        'locations': [
            {
                'name': 'Jimmy\'s Tapas Bar Warnemünde',
                'address': 'Am Strom 12\n18119 Rostock-Warnemünde',
                'phone': '+49 381 12345',
                'email': 'warnemunde@jimmys-tapas.de',
                'opening_hours': '''
                Montag - Donnerstag: 17:00 - 23:00
                Freitag - Samstag: 17:00 - 24:00
                Sonntag: 16:00 - 22:00
                ''',
                'map_url': 'https://maps.google.com'
            },
            {
                'name': 'Jimmy\'s Tapas Bar Kühlungsborn',
                'address': 'Strandstraße 8\n18225 Kühlungsborn',
                'phone': '+49 38293 67890',
                'email': 'kuehlungsborn@jimmys-tapas.de',
                'opening_hours': '''
                Montag - Donnerstag: 17:00 - 23:00
                Freitag - Samstag: 17:00 - 24:00
                Sonntag: 16:00 - 22:00
                ''',
                'map_url': 'https://maps.google.com'
            }
        ],
        'privacy_policy': '''
        <h2>Datenschutzerklärung</h2>
        <p>Der Schutz Ihrer persönlichen Daten ist uns ein besonderes Anliegen. Wir verarbeiten Ihre Daten ausschließlich auf Grundlage der gesetzlichen Bestimmungen (DSGVO, TKG 2003).</p>
        
        <h3>Kontaktdaten des Verantwortlichen</h3>
        <p>Jimmy's Tapas Bar GmbH<br>
        Am Strom 12<br>
        18119 Rostock-Warnemünde<br>
        Tel: +49 381 12345<br>
        E-Mail: info@jimmys-tapas.de</p>
        
        <h3>Datenverarbeitung</h3>
        <p>Wir erheben und verwenden Ihre persönlichen Daten nur, soweit dies zur Erbringung einer funktionsfähigen Website sowie unserer Inhalte und Leistungen erforderlich ist.</p>
        ''',
        'imprint': '''
        <h2>Impressum</h2>
        <p><strong>Jimmy's Tapas Bar GmbH</strong><br>
        Am Strom 12<br>
        18119 Rostock-Warnemünde<br>
        Deutschland</p>
        
        <p><strong>Telefon:</strong> +49 381 12345<br>
        <strong>E-Mail:</strong> info@jimmys-tapas.de</p>
        
        <p><strong>Geschäftsführer:</strong> Jimmy Rodriguez<br>
        <strong>Registergericht:</strong> Amtsgericht Rostock<br>
        <strong>Registernummer:</strong> HRB 12345<br>
        <strong>Umsatzsteuer-ID:</strong> DE123456789</p>
        
        <p><strong>Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV:</strong><br>
        Jimmy Rodriguez<br>
        Am Strom 12<br>
        18119 Rostock-Warnemünde</p>
        '''
    }
}

async def migrate_all_cms_content():
    """Migrate all CMS content to MongoDB"""
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🚀 Starting complete CMS content migration...")
    
    try:
        # Clear existing CMS content
        print("🗑️  Clearing existing CMS content...")
        await db.homepage_hero.delete_many({})
        await db.homepage_features.delete_many({})
        await db.homepage_food_gallery.delete_many({})
        await db.homepage_lieferando.delete_many({})
        await db.about_content.delete_many({})
        await db.contact_legal.delete_many({})
        
        # Insert Homepage Hero
        print("🏠 Inserting Homepage Hero content...")
        hero_data = {
            'id': str(uuid.uuid4()),
            **CMS_CONTENT_DATA['homepage_hero'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_hero.insert_one(hero_data)
        print(f"  ✅ Hero section with title: {hero_data['title']}")
        
        # Insert Homepage Features
        print("🌟 Inserting Homepage Features content...")
        features_data = {
            'id': str(uuid.uuid4()),
            **CMS_CONTENT_DATA['homepage_features'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_features.insert_one(features_data)
        print(f"  ✅ Features section with {len(features_data['features'])} features")
        
        # Insert Homepage Food Gallery
        print("🍽️  Inserting Homepage Food Gallery...")
        gallery_data = {
            'id': str(uuid.uuid4()),
            **CMS_CONTENT_DATA['homepage_food_gallery'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_food_gallery.insert_one(gallery_data)
        print(f"  ✅ Food gallery with {len(gallery_data['gallery_items'])} items")
        
        # Insert Homepage Lieferando
        print("🚚 Inserting Homepage Lieferando section...")
        lieferando_data = {
            'id': str(uuid.uuid4()),
            **CMS_CONTENT_DATA['homepage_lieferando'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_lieferando.insert_one(lieferando_data)
        print(f"  ✅ Lieferando section: {lieferando_data['title']}")
        
        # Insert About Content
        print("ℹ️  Inserting About Us content...")
        about_data = {
            'id': str(uuid.uuid4()),
            **CMS_CONTENT_DATA['about_content'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.about_content.insert_one(about_data)
        print(f"  ✅ About section: {about_data['page_title']}")
        
        # Insert Contact & Legal
        print("📞 Inserting Contact & Legal content...")
        contact_data = {
            'id': str(uuid.uuid4()),
            **CMS_CONTENT_DATA['contact_legal'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.contact_legal.insert_one(contact_data)
        print(f"  ✅ Contact & Legal with {len(contact_data['locations'])} locations")
        
        print(f"\n🎉 Complete CMS migration successful!")
        print(f"📊 Summary:")
        print(f"   - Homepage sections: 4")
        print(f"   - About page: 1")
        print(f"   - Contact & Legal: 1")
        print(f"   - All content in German ✅")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise e
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(migrate_all_cms_content())
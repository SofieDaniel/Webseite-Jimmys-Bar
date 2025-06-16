#!/usr/bin/env python3
"""
VOLLSTÄNDIGE CMS-MIGRATION für Jimmy's Tapas Bar
Alle Inhalte werden ins CMS eingefügt und für deutschen Frontend optimiert
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

# VOLLSTÄNDIGE CMS-INHALTE - Nur Deutsch, Frontend-optimiert
COMPLETE_CMS_DATA = {
    # ===============================================
    # HOMEPAGE HERO SECTION
    # ===============================================
    'homepage_hero': {
        'title': 'AUTÉNTICO SABOR ESPAÑOL',
        'subtitle': 'an der Ostsee',
        'description': 'Genießen Sie authentische spanische Spezialitäten direkt an der malerischen Ostseeküste',
        'location_text': 'Warnemünde & Kühlungsborn',
        'menu_button_text': 'Zur Speisekarte',
        'locations_button_text': 'Unsere Standorte',
        'background_image': 'https://images.unsplash.com/photo-1656423521731-9665583f100c'
    },
    
    # ===============================================
    # HOMEPAGE FEATURES SECTION
    # ===============================================
    'homepage_features': {
        'section_title': 'Authentische Spanische Küche',
        'section_description': 'Erleben Sie die Geschmacksvielfalt Spaniens in gemütlicher Atmosphäre an der deutschen Ostseeküste',
        'features': [
            {
                'title': 'Traditionelle Tapas',
                'description': 'Original spanische Tapas nach Familienrezepten aus Valencia und Andalusien. Jede Tapa wird frisch zubereitet mit importierten Zutaten direkt aus Spanien.',
                'image_url': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
                'image_alt': 'Spanische Tapas Variation'
            },
            {
                'title': 'Frische Paella',
                'description': 'Authentische Paella mit original Bomba-Reis und echtem Safran aus Valencia. Täglich frisch zubereitet in traditioneller Paellera.',
                'image_url': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e',
                'image_alt': 'Traditionelle Paella Valencia'
            },
            {
                'title': 'Erlesene Weine',
                'description': 'Handverlesene Weine aus den besten spanischen Regionen: Rioja, Ribera del Duero, Rías Baixas und Penedès. Perfekt abgestimmt auf unsere Tapas.',
                'image_url': 'https://images.unsplash.com/photo-1567522693444-038749b0f0ed',
                'image_alt': 'Spanische Weine aus verschiedenen Regionen'
            }
        ]
    },
    
    # ===============================================
    # HOMEPAGE FOOD GALLERY
    # ===============================================
    'homepage_food_gallery': {
        'section_title': 'Unsere kulinarischen Highlights',
        'gallery_items': [
            {
                'name': 'Jamón Ibérico de Bellota',
                'description': 'Edler Iberico-Schinken aus Extremadura - 36 Monate gereift',
                'image_url': 'https://images.unsplash.com/photo-1598989519542-077da0f51c09',
                'category_link': '#inicio'
            },
            {
                'name': 'Gambas al Ajillo',
                'description': 'Garnelen in Knoblauchöl mit Guindilla-Chilis',
                'image_url': 'https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg',
                'category_link': '#tapas-pescado'
            },
            {
                'name': 'Tortilla Española',
                'description': 'Klassisches Kartoffel-Omelett nach Madrider Art',
                'image_url': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
                'category_link': '#tapas-vegetarian'
            },
            {
                'name': 'Paella Valenciana',
                'description': 'Original Paella mit Hähnchen, Kaninchen und grünen Bohnen',
                'image_url': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e',
                'category_link': '#tapa-paella'
            },
            {
                'name': 'Pulpo a la Gallega',
                'description': 'Galicischer Oktopus mit Paprikapulver und Olivenöl',
                'image_url': 'https://images.unsplash.com/photo-1559329007-40df8766a171',
                'category_link': '#tapas-pescado'
            },
            {
                'name': 'Manchego & Membrillo',
                'description': 'Gereifter Manchego-Käse mit Quittengelee',
                'image_url': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d',
                'category_link': '#inicio'
            }
        ]
    },
    
    # ===============================================
    # HOMEPAGE LIEFERANDO SECTION
    # ===============================================
    'homepage_lieferando': {
        'title': 'Jetzt auch Lieferservice & Abholung',
        'description': 'Genießen Sie unsere spanischen Spezialitäten bequem zu Hause oder holen Sie direkt bei uns ab',
        'delivery_text': 'Schnelle Lieferung',
        'button_text': 'Bei Lieferando bestellen',
        'availability_text': 'Täglich 17:00 - 22:00 Uhr verfügbar',
        'authentic_text': 'Authentisch Spanisch',
        'lieferando_url': 'https://www.lieferando.de/restaurants-jimmys-tapas-bar'
    },
    
    # ===============================================
    # ABOUT US / ÜBER UNS CONTENT
    # ===============================================
    'about_content': {
        'page_title': 'Über Jimmy\'s Tapas Bar',
        'hero_title': 'Unsere Geschichte',
        'hero_description': 'Seit 2020 bringen wir authentische spanische Küche und Lebensfreude an die deutsche Ostseeküste',
        'hero_image': 'https://images.unsplash.com/photo-1559329007-40df8766a171',
        'story_title': 'Die Geschichte von Jimmy\'s',
        'story_content': '''
        <div class="prose prose-lg max-w-none">
            <p class="text-lg text-gray-700 leading-relaxed mb-6">Jimmy's Tapas Bar wurde 2020 mit einer klaren Vision gegründet: Authentische spanische Küche und die typisch spanische Lebensfreude an die wunderschöne deutsche Ostseeküste zu bringen.</p>
            
            <p class="text-gray-700 leading-relaxed mb-6">Unser Gründer Jimmy verbrachte über 15 Jahre in verschiedenen Regionen Spaniens - von den lebhaften Märkten Valencias über die traditionellen Bodegas Andalusiens bis hin zu den Fischerdörfern Galiciens. Dort erlernte er nicht nur die traditionelle Kunst der Tapas-Zubereitung, sondern auch die spanische Philosophie des Genießens und Teilens.</p>
            
            <p class="text-gray-700 leading-relaxed mb-6">Heute führen wir zwei Standorte in den beliebten Ostseebädern Warnemünde und Kühlungsborn. In unseren Küchen werden täglich frische Tapas nach original spanischen Familienrezepten zubereitet - von der klassischen Tortilla Española bis hin zu raffinierten Meeresfrüchte-Kreationen.</p>
            
            <p class="text-gray-700 leading-relaxed mb-6">Unsere Zutaten importieren wir direkt aus Spanien: Pimentón de la Vera D.O.P. aus Extremadura, Jamón Ibérico de Bellota aus der Dehesa, echter Bomba-Reis aus Valencia für unsere Paellas und natürlich der beste Olivenöl extra vergine aus Andalusien.</p>
            
            <p class="text-gray-700 leading-relaxed">Bei uns erwartet Sie nicht nur ausgezeichnetes Essen, sondern auch die typisch spanische Gemütlichkeit und Gastfreundschaft. Unsere Restaurants sind Orte der Begegnung, wo Freunde und Familie zusammenkommen, um gemeinsam zu genießen. <em>¡Bienvenidos a nuestra casa!</em></p>
        </div>
        ''',
        'team_title': 'Unser leidenschaftliches Team',
        'team_description': 'Köche mit spanischen Wurzeln und deutsche Gastfreundschaft',
        'team_members': [
            {
                'name': 'Jimmy Rodriguez',
                'position': 'Gründer & Chefkoch',
                'description': 'Geboren in Valencia, lebt seit 2018 in Deutschland. Spezialist für authentische Paella und traditionelle Tapas.',
                'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d'
            },
            {
                'name': 'Carmen García',
                'position': 'Sous Chef',
                'description': 'Aus Sevilla stammend, Expertin für andalusische Küche und Meeresfrüchte-Tapas.',
                'image': 'https://images.unsplash.com/photo-1494790108755-2616c27ba1e0'
            },
            {
                'name': 'Hans Müller',
                'position': 'Restaurant Manager',
                'description': 'Sorgt für den perfekten Service und kennt jeden Wein unserer spanischen Kollektion.',
                'image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e'
            }
        ],
        'values_title': 'Unsere Werte & Philosophie',
        'values': [
            {
                'title': 'Authentizität',
                'description': 'Wir verwenden ausschließlich original spanische Rezepte und importieren unsere wichtigsten Zutaten direkt aus Spanien. Keine Kompromisse bei der Qualität.',
                'icon': '🇪🇸'
            },
            {
                'title': 'Qualität',
                'description': 'Frische, hochwertige Produkte direkt von spanischen Erzeugern. Unser Jamón Ibérico kommt aus Extremadura, unser Olivenöl aus Jaén.',
                'icon': '⭐'
            },
            {
                'title': 'Gastfreundschaft',
                'description': 'Spanische Herzlichkeit trifft auf deutsche Gründlichkeit. Bei uns sind Sie nicht nur Gast, sondern Teil der Familie.',
                'icon': '❤️'
            },
            {
                'title': 'Nachhaltigkeit',
                'description': 'Wir achten auf kurze Transportwege wo möglich und unterstützen kleine spanische Familienbetriebe bei unseren Importen.',
                'icon': '🌱'
            }
        ]
    },
    
    # ===============================================
    # LOCATIONS / STANDORTE CONTENT
    # ===============================================
    'locations_content': {
        'page_title': 'Unsere Standorte',
        'hero_title': 'Besuchen Sie uns an der Ostsee',
        'hero_description': 'Zwei wunderschöne Standorte direkt an der deutschen Ostseeküste',
        'locations': [
            {
                'id': 'warnemunde',
                'name': 'Jimmy\'s Tapas Bar Warnemünde',
                'subtitle': 'Direkt am historischen Strom',
                'address': 'Am Strom 12\n18119 Rostock-Warnemünde',
                'phone': '+49 381 12345',
                'email': 'warnemunde@jimmys-tapas.de',
                'description': 'Unser Stammhaus im Herzen von Warnemünde, nur wenige Schritte vom berühmten Leuchtturm entfernt. Die maritime Atmosphäre des alten Fischerdorfs trifft auf spanisches Flair.',
                'opening_hours': {
                    'monday': '17:00 - 23:00',
                    'tuesday': '17:00 - 23:00', 
                    'wednesday': '17:00 - 23:00',
                    'thursday': '17:00 - 23:00',
                    'friday': '17:00 - 24:00',
                    'saturday': '17:00 - 24:00',
                    'sunday': '16:00 - 22:00'
                },
                'features': [
                    'Terrasse mit Blick auf den Strom',
                    'Parkplätze in der Nähe',
                    'Reservierungen empfohlen',
                    'Kinderfreundlich'
                ],
                'image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4',
                'map_url': 'https://maps.google.com',
                'special_info': 'In den Sommermonaten mit wunderschöner Außenterrasse'
            },
            {
                'id': 'kuehlungsborn',
                'name': 'Jimmy\'s Tapas Bar Kühlungsborn',
                'subtitle': 'Direkt an der Strandpromenade',
                'address': 'Strandstraße 8\n18225 Kühlungsborn',
                'phone': '+49 38293 67890',
                'email': 'kuehlungsborn@jimmys-tapas.de',
                'description': 'Unser zweiter Standort mit direktem Blick auf die Ostsee. Hier können Sie spanische Küche mit Meeresrauschen im Hintergrund genießen.',
                'opening_hours': {
                    'monday': '17:00 - 23:00',
                    'tuesday': '17:00 - 23:00',
                    'wednesday': '17:00 - 23:00', 
                    'thursday': '17:00 - 23:00',
                    'friday': '17:00 - 24:00',
                    'saturday': '17:00 - 24:00',
                    'sunday': '16:00 - 22:00'
                },
                'features': [
                    'Meerblick von der Terrasse',
                    'Strandnähe (50m zum Strand)',
                    'Große Auswahl an Meeresfrüchten',
                    'Romantisches Ambiente'
                ],
                'image': 'https://images.unsplash.com/photo-1544148103-0773bf10d330',
                'map_url': 'https://maps.google.com',
                'special_info': 'Perfekt für romantische Abende mit Sonnenuntergang über der Ostsee'
            }
        ]
    },
    
    # ===============================================
    # CONTACT & LEGAL CONTENT
    # ===============================================
    'contact_legal': {
        'contact_title': 'Kontakt & Reservierung',
        'contact_description': 'Wir freuen uns auf Ihren Besuch! Reservierungen sind besonders an Wochenenden empfehlenswert.',
        'reservation_info': 'Reservierungen werden für beide Standorte gerne telefonisch oder per E-Mail entgegengenommen. Für größere Gruppen (ab 8 Personen) ist eine Voranmeldung erforderlich.',
        'privacy_policy': '''
        <div class="prose prose-lg max-w-none">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Datenschutzerklärung</h2>
            <p class="text-gray-700 mb-4">Der Schutz Ihrer persönlichen Daten ist uns ein besonderes Anliegen. Wir verarbeiten Ihre Daten ausschließlich auf Grundlage der gesetzlichen Bestimmungen (DSGVO, TKG 2003).</p>
            
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Kontaktdaten des Verantwortlichen</h3>
            <p class="text-gray-700 mb-4">Jimmy's Tapas Bar GmbH<br>
            Am Strom 12<br>
            18119 Rostock-Warnemünde<br>
            Tel: +49 381 12345<br>
            E-Mail: info@jimmys-tapas.de</p>
            
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Datenverarbeitung auf unserer Website</h3>
            <p class="text-gray-700 mb-4">Wir erheben und verwenden Ihre persönlichen Daten nur, soweit dies zur Erbringung einer funktionsfähigen Website sowie unserer Inhalte und Leistungen erforderlich ist.</p>
            
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Newsletter</h3>
            <p class="text-gray-700 mb-4">Falls Sie unseren Newsletter abonnieren, verwenden wir Ihre E-Mail-Adresse ausschließlich zum Versand unseres Newsletters. Sie können sich jederzeit wieder abmelden.</p>
            
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Ihre Rechte</h3>
            <p class="text-gray-700 mb-4">Sie haben das Recht auf Auskunft, Berichtigung, Löschung oder Einschränkung der Verarbeitung Ihrer gespeicherten Daten sowie ein Widerspruchsrecht gegen die Verarbeitung und ein Recht auf Datenübertragbarkeit.</p>
        </div>
        ''',
        'imprint': '''
        <div class="prose prose-lg max-w-none">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Impressum</h2>
            <div class="bg-gray-50 p-6 rounded-lg mb-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-3">Angaben gemäß § 5 TMG</h3>
                <p class="text-gray-700"><strong>Jimmy's Tapas Bar GmbH</strong><br>
                Am Strom 12<br>
                18119 Rostock-Warnemünde<br>
                Deutschland</p>
            </div>
            
            <div class="grid md:grid-cols-2 gap-6 mb-6">
                <div>
                    <h4 class="font-semibold text-gray-900 mb-2">Kontakt</h4>
                    <p class="text-gray-700">Telefon: +49 381 12345<br>
                    E-Mail: info@jimmys-tapas.de<br>
                    Internet: www.jimmys-tapas.de</p>
                </div>
                <div>
                    <h4 class="font-semibold text-gray-900 mb-2">Geschäftsführung</h4>
                    <p class="text-gray-700">Jimmy Rodriguez<br>
                    (Gründer & Geschäftsführer)</p>
                </div>
            </div>
            
            <div class="bg-blue-50 p-6 rounded-lg mb-6">
                <h4 class="font-semibold text-gray-900 mb-2">Handelsregister</h4>
                <p class="text-gray-700">Registergericht: Amtsgericht Rostock<br>
                Registernummer: HRB 12345<br>
                Umsatzsteuer-ID: DE123456789</p>
            </div>
            
            <h4 class="font-semibold text-gray-900 mb-2">Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h4>
            <p class="text-gray-700">Jimmy Rodriguez<br>
            Am Strom 12<br>
            18119 Rostock-Warnemünde</p>
            
            <div class="mt-6 p-4 bg-yellow-50 rounded-lg">
                <h4 class="font-semibold text-gray-900 mb-2">Haftungsausschluss</h4>
                <p class="text-sm text-gray-600">Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.</p>
            </div>
        </div>
        '''
    }
}

async def migrate_complete_cms():
    """Migrate complete CMS content to MongoDB - German only"""
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🚀 Starting COMPLETE CMS content migration (German only)...")
    
    try:
        # Clear ALL existing CMS content
        print("🗑️  Clearing ALL existing CMS content...")
        collections_to_clear = [
            'homepage_hero', 'homepage_features', 'homepage_food_gallery', 
            'homepage_lieferando', 'about_content', 'locations_content', 
            'contact_legal'
        ]
        
        for collection_name in collections_to_clear:
            collection = getattr(db, collection_name)
            await collection.delete_many({})
            print(f"   ✅ Cleared {collection_name}")
        
        # Insert Homepage Hero
        print("\n🏠 Inserting Homepage Hero content...")
        hero_data = {
            'id': str(uuid.uuid4()),
            **COMPLETE_CMS_DATA['homepage_hero'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_hero.insert_one(hero_data)
        print(f"   ✅ Hero: {hero_data['title']}")
        
        # Insert Homepage Features
        print("🌟 Inserting Homepage Features...")
        features_data = {
            'id': str(uuid.uuid4()),
            **COMPLETE_CMS_DATA['homepage_features'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_features.insert_one(features_data)
        print(f"   ✅ Features: {len(features_data['features'])} features")
        
        # Insert Homepage Food Gallery
        print("🍽️  Inserting Homepage Food Gallery...")
        gallery_data = {
            'id': str(uuid.uuid4()),
            **COMPLETE_CMS_DATA['homepage_food_gallery'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_food_gallery.insert_one(gallery_data)
        print(f"   ✅ Gallery: {len(gallery_data['gallery_items'])} items")
        
        # Insert Homepage Lieferando
        print("🚚 Inserting Homepage Lieferando...")
        lieferando_data = {
            'id': str(uuid.uuid4()),
            **COMPLETE_CMS_DATA['homepage_lieferando'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.homepage_lieferando.insert_one(lieferando_data)
        print(f"   ✅ Lieferando: {lieferando_data['title']}")
        
        # Insert About Content
        print("ℹ️  Inserting About Us content...")
        about_data = {
            'id': str(uuid.uuid4()),
            **COMPLETE_CMS_DATA['about_content'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.about_content.insert_one(about_data)
        print(f"   ✅ About: {about_data['page_title']}")
        print(f"   ✅ Team: {len(about_data['team_members'])} members")
        print(f"   ✅ Values: {len(about_data['values'])} values")
        
        # Insert Locations Content
        print("📍 Inserting Locations content...")
        locations_data = {
            'id': str(uuid.uuid4()),
            **COMPLETE_CMS_DATA['locations_content'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.locations_content.insert_one(locations_data)
        print(f"   ✅ Locations: {len(locations_data['locations'])} standorte")
        
        # Insert Contact & Legal
        print("📞 Inserting Contact & Legal...")
        contact_data = {
            'id': str(uuid.uuid4()),
            **COMPLETE_CMS_DATA['contact_legal'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        await db.contact_legal.insert_one(contact_data)
        print(f"   ✅ Contact & Legal: Complete")
        
        print(f"\n🎉 COMPLETE CMS migration successful!")
        print(f"📊 Summary:")
        print(f"   - Homepage sections: 4 ✅")
        print(f"   - About page with team & values: ✅") 
        print(f"   - Locations (2 standorte): ✅")
        print(f"   - Contact & Legal: ✅")
        print(f"   - All content in German: ✅")
        print(f"   - Frontend-optimized: ✅")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise e
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(migrate_complete_cms())
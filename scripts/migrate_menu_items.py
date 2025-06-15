#!/usr/bin/env python3
"""
Script to migrate menu items from frontend code to backend CMS
This will populate the database with all menu items from the static data
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

# Add parent directory to path to import from backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Menu items data extracted from frontend code
MENU_ITEMS_DATA = {
    'inicio': [
        {'name': 'Aioli', 'description': 'Hausgemachte Knoblauch-Mayonnaise', 'price': '3,50', 'image': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', 'details': 'Hausgemachte, cremige Knoblauch-Mayonnaise nach traditionellem valencianischem Rezept. Zubereitet mit frischem Knoblauch aus Spanien, nativem Olivenöl extra aus Andalusien und Zitronensaft. Serviert mit ofentrischem, spanischem Weißbrot. Perfekt zum Einstieg in einen mediterranen Abend.'},
        {'name': 'Oliven', 'description': 'Marinierte spanische Oliven', 'price': '3,90', 'image': 'https://images.unsplash.com/photo-1714583357992-98f0ad946902', 'details': 'Ausgewählte schwarze Arbequina-Oliven aus Katalonien und grüne Manzanilla-Oliven aus Sevilla, mariniert mit wildem Thymian, rosa Pfefferkörnern, Knoblauch und bestem Olivenöl extra vergine. 24 Stunden eingelegt für optimalen Geschmack.'},
        {'name': 'Extra Brot', 'description': 'Frisches spanisches Brot', 'price': '1,90', 'image': 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73', 'details': 'Warmes, knuspriges Pan de Pueblo nach traditionellem kastilischem Rezept. Täglich frisch gebacken mit Steinofenmehl aus der Region Castilla y León, Meersalz und natürlicher Hefe. Perfekt für Tapas und Dips.'},
        {'name': 'Hummus', 'description': 'Cremiger Kichererbsen-Dip', 'price': '3,90', 'image': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', 'details': 'Hausgemachter Hummus aus Kichererbsen (Garbanzo-Bohnen) aus Kastilien, Tahini aus Sesam, Zitrone und Kreuzkümmel. Nach mediterraner Tradition zubereitet. Serviert mit frischem Gemüse und warmem Brot.'},
        {'name': 'Spanischer Käseteller', 'description': 'Auswahl spanischer Käsesorten', 'price': '8,90', 'image': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d', 'details': 'Edle Auswahl aus der Mancha: Manchego D.O.P. (12 Monate gereift), Cabrales D.O.P. aus Asturien (Blauschimmelkäse) und Murcia al Vino aus Murcia (in Rotwein gereift). Serviert mit Walnüssen aus Kalifornien, Akazienhonig und frischen Moscatel-Trauben.'},
        {'name': 'Schinken-Käse-Wurst Teller', 'description': 'Spanische Charcuterie-Platte', 'price': '11,90', 'image': 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', 'details': 'Edle Auswahl aus Jamón Serrano, Chorizo, Lomo und spanischen Käsesorten mit Oliven, Nüssen und Feigenmarmelade.'},
        {'name': 'Jamón Serrano Teller', 'description': 'Hochwertiger spanischer Schinken', 'price': '9,90', 'image': 'https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg', 'details': '18 Monate gereifter Jamón Serrano D.O. aus den Bergen der Sierra Nevada, hauchdünn geschnitten. Serviert mit 12 Monate gereiftem Manchego-Käse D.O.P. und geröstetem Brot aus Kastilien. Von freilaufenden iberischen Schweinen.'},
        {'name': 'Pata Negra', 'description': 'Premium Iberico Schinken', 'price': '10,90', 'image': 'https://images.unsplash.com/photo-1598989519542-077da0f51c09', 'details': 'Der Edelste aller spanischen Schinken - Jamón Ibérico de Bellota D.O.P. aus Extremadura, 36 Monate gereift. Von schwarzfüßigen Iberico-Schweinen, die sich ausschließlich von Eicheln ernähren. Serviert mit Manchego Reserva und Tomaten-Brot.'},
        {'name': 'Tres (Hummus, Avocado Cream, Aioli mit Brot)', 'description': 'Drei köstliche Dips mit Brot', 'price': '10,90', 'image': 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', 'details': 'Trio aus hausgemachtem Hummus, cremiger Avocado-Creme und Aioli, serviert mit warmem spanischem Brot und Gemüse.'}
    ],
    'salat': [
        {'name': 'Ensalada Mixta', 'description': 'Gemischter Salat mit spanischen Zutaten', 'price': '8,90', 'details': 'Frischer Salat mit Tomaten, Gurken, Oliven, roten Zwiebeln und Manchego-Käse in Sherry-Vinaigrette.'},
        {'name': 'Ensalada Tonno', 'description': 'Salat mit Thunfisch', 'price': '14,90', 'details': 'Gemischter Salat mit saftigem Thunfisch, hartgekochten Eiern, Oliven und Kapern in mediteraner Vinaigrette.'},
        {'name': 'Ensalada Pollo', 'description': 'Salat mit gegrilltem Hähnchen', 'price': '14,90', 'details': 'Frischer Salat mit gegrillten Hähnchenstreifen, Cherrytomaten, Avocado und gerösteten Pinienkernen.'},
        {'name': 'Ensalada Garnelen', 'description': 'Salat mit frischen Garnelen', 'price': '15,90', 'details': 'Bunter Salat mit saftigen Garnelen, Avocado, Mango und einem Hauch von Chili in Limetten-Dressing.'}
    ],
    'kleiner-salat': [
        {'name': 'Tomaten/Gurken mit Zwiebeln', 'description': 'Frischer Gemüsesalat', 'price': '6,90', 'details': 'Saftige Tomaten und knackige Gurken mit roten Zwiebeln in aromatischem Olivenöl und Kräutern.'},
        {'name': 'Rote Beete mit Ziegenkäse', 'description': 'Süße rote Beete mit cremigem Ziegenkäse', 'price': '7,90', 'details': 'Geröstete rote Beete mit cremigem Ziegenkäse, Walnüssen und Honig-Thymian-Dressing.'},
        {'name': 'Kichererbsen mit Feta', 'description': 'Proteinreicher Salat mit Feta', 'price': '7,90', 'details': 'Warme Kichererbsen mit Feta-Käse, frischen Kräutern, Tomaten und Zitronendressing.'}
    ],
    'tapa-paella': [
        {'name': 'Paella mit Hähnchen & Meeresfrüchten', 'description': 'Traditionelle spanische Paella als Tapa-Portion', 'price': '8,90', 'details': 'Authentische Paella mit saftigem Hähnchen, frischen Garnelen, Muscheln und Bomba-Reis in würziger Safran-Brühe.'},
        {'name': 'Paella vegetarisch', 'description': 'Vegetarische Paella mit frischem Gemüse', 'price': '7,90', 'details': 'Vegetarische Paella mit grünen Bohnen, Paprika, Artischocken und Bomba-Reis in aromatischer Gemüsebrühe.'}
    ],
    'tapas-vegetarian': [
        {'name': 'Gebratenes Gemüse', 'description': 'Vegan - Saisonales Gemüse mediterran gewürzt', 'price': '6,90', 'vegan': True, 'glutenfree': True, 'details': 'Frisches Saisongemüse wie Zucchini, Paprika und Auberginen, gegrillt mit Rosmarin, Thymian und Olivenöl.'},
        {'name': 'Papas Bravas', 'description': 'Vegan - Klassische spanische Kartoffeln mit scharfer Soße', 'price': '6,90', 'vegan': True, 'glutenfree': True, 'details': 'Knusprig gebratene Kartoffelwürfel aus der Region Galicia mit pikanter Bravas-Sauce aus San Marzano-Tomaten, geröstetem Paprikapulver aus Murcia (Pimentón de la Vera D.O.P.) und einem Hauch Cayenne-Chili. Original Madrider Rezept.'},
        {'name': 'Tortilla de Patata mit Aioli', 'description': 'Spanisches Kartoffel-Omelett mit Aioli', 'price': '6,90', 'vegetarian': True, 'glutenfree': True, 'details': 'Klassische spanische Tortilla aus Kartoffeln der Region Castilla y León und frischen Eiern, golden gebraten nach traditionellem Rezept aus Madrid. Serviert mit hausgemachtem Aioli aus bestem andalusischem Olivenöl.'},
        {'name': 'Pimientos de Padrón', 'description': 'Vegan - Gebratene grüne Paprika', 'price': '6,90', 'vegan': True, 'glutenfree': True, 'details': 'Original Pimientos de Padrón D.O.P. aus Galicien - kleine grüne Paprikaschoten, gebraten in nativem Olivenöl extra aus Jaén und mit Flor de Sal (Meersalz) aus Cádiz bestreut. Traditionell: manche scharf, manche mild!'},
        {'name': 'Kanarische Kartoffeln', 'description': 'Vegan - Traditionelle Kartoffeln mit Meersalz', 'price': '6,90', 'vegan': True, 'glutenfree': True, 'details': 'Papas Arrugadas - kleine Kartoffeln aus Teneriffa in der Schale gekocht mit grobem Atlantik-Meersalz. Serviert mit grüner Mojo Verde (Koriander, Petersilie) und roter Mojo Rojo (geröstete Paprika) aus den Kanarischen Inseln.'},
        {'name': 'Fetahäppchen auf Johannisbeersauce', 'description': 'Cremiger Feta mit süß-saurer Sauce', 'price': '6,90', 'details': 'Warme Feta-Würfel auf einer Reduktion aus roten Johannisbeeren mit einem Hauch Balsamico und frischen Kräutern.'},
        {'name': 'Ziegenkäse auf Johannisbeersauce oder Honig-Senf', 'description': 'Mild-cremiger Ziegenkäse mit Sauce nach Wahl', 'price': '6,90', 'details': 'Warmer Ziegenkäse wahlweise mit süßer Johannisbeersauce oder würzigem Honig-Senf-Dressing und gerösteten Nüssen.'}
    ],
    'tapas-pescado': [
        {'name': 'Gambas al Ajillo', 'description': 'Garnelen in Knoblauchöl', 'price': '9,90', 'glutenfree': True, 'details': 'In bestem andalusischem Olivenöl extra vergine gebratene Garnelen aus Huelva mit frischem Knoblauch aus Las Pedroñeras (Cuenca), scharfem Guindilla-Chili aus dem Baskenland und frischer Petersilie. Ein Klassiker aus den Marisquerías von Cádiz, traditionell in der Cazuela de Barro (Tonschale) serviert.'},
        {'name': 'Calamares a la Romana', 'description': 'Panierte Tintenfischringe', 'price': '7,50', 'details': 'Knusprig panierte Tintenfischringe serviert mit Zitrone und Aioli.'},
        {'name': 'Boquerones Fritos', 'description': 'Frittierte Sardellen', 'price': '7,50', 'details': 'Frisch frittierte Sardellen in knuspriger Panade mit Zitrone und hausgemachter Aioli.'},
        {'name': 'Lachs mit Spinat', 'description': 'Frischer Lachs auf Spinatbett', 'price': '9,90', 'details': 'Gebratenes Lachsfilet auf cremigem Blattspinat mit Knoblauch und Pinienkernen.'}
    ]
}

MENU_CATEGORIES = [
    {'name': 'Inicio', 'slug': 'inicio', 'description': 'Vorspeisen und Einstieg'},
    {'name': 'Salate', 'slug': 'salat', 'description': 'Frische Salate'},
    {'name': 'Kleine Salate', 'slug': 'kleiner-salat', 'description': 'Kleine Beilagensalate'},
    {'name': 'Tapa Paella', 'slug': 'tapa-paella', 'description': 'Paella als Tapa-Portion'},
    {'name': 'Tapas Vegetarisch', 'slug': 'tapas-vegetarian', 'description': 'Vegetarische und vegane Tapas'},
    {'name': 'Tapas Fisch', 'slug': 'tapas-pescado', 'description': 'Tapas mit Fisch und Meeresfrüchten'},
]

async def migrate_menu_data():
    """Migrate menu data to MongoDB"""
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🚀 Starting menu data migration...")
    
    try:
        # Clear existing menu data
        print("🗑️  Clearing existing menu data...")
        await db.menu_categories.delete_many({})
        await db.menu_items.delete_many({})
        
        # Insert categories first
        print("📂 Inserting menu categories...")
        for i, category_data in enumerate(MENU_CATEGORIES):
            category = {
                'id': str(uuid.uuid4()),
                'name': category_data['name'],
                'slug': category_data['slug'],
                'description': category_data['description'],
                'order': i,
                'is_active': True,
                'created_at': datetime.utcnow()
            }
            await db.menu_categories.insert_one(category)
            print(f"  ✅ {category['name']} ({category['slug']})")
        
        # Insert menu items
        print("🍽️  Inserting menu items...")
        item_count = 0
        
        for category_slug, items in MENU_ITEMS_DATA.items():
            # Find category
            category = await db.menu_categories.find_one({'slug': category_slug})
            if not category:
                print(f"  ❌ Category not found: {category_slug}")
                continue
                
            for i, item_data in enumerate(items):
                # Convert price to float
                price_str = item_data['price'].replace('€', '').replace(',', '.')
                try:
                    price = float(price_str)
                except:
                    price = 0.0
                
                menu_item = {
                    'id': str(uuid.uuid4()),
                    'name': item_data['name'],
                    'description': item_data['description'],
                    'detailed_description': item_data.get('details', ''),
                    'price': price,
                    'category': category_slug,
                    'image': item_data.get('image', ''),
                    'vegan': item_data.get('vegan', False),
                    'vegetarian': item_data.get('vegetarian', False),
                    'glutenfree': item_data.get('glutenfree', False),
                    'order_index': i,
                    'is_active': True,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                
                await db.menu_items.insert_one(menu_item)
                item_count += 1
                print(f"  ✅ {item_data['name']} ({category_slug}) - {price}€")
        
        print(f"\n🎉 Migration completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Categories: {len(MENU_CATEGORIES)}")
        print(f"   - Menu Items: {item_count}")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise e
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(migrate_menu_data())
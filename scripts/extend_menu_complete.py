#!/usr/bin/env python3
"""
ERWEITERTE Menu-Migration - Alle fehlenden Kategorien und Items hinzufügen
Basierend auf dem ursprünglichen umfangreichen Inhalt vom Chat-Anfang
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

# VOLLSTÄNDIGE ERWEITERTE MENU-DATEN
EXTENDED_MENU_DATA = {
    # Bestehende Kategorien erweitern
    'inicio': [
        {'name': 'Aioli', 'description': 'Hausgemachte Knoblauch-Mayonnaise', 'price': 3.50, 'image': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', 'details': 'Hausgemachte, cremige Knoblauch-Mayonnaise nach traditionellem valencianischem Rezept. Zubereitet mit frischem Knoblauch aus Spanien, nativem Olivenöl extra aus Andalusien und Zitronensaft. Serviert mit ofentrischem, spanischem Weißbrot.'},
        {'name': 'Oliven', 'description': 'Marinierte spanische Oliven', 'price': 3.90, 'image': 'https://images.unsplash.com/photo-1714583357992-98f0ad946902', 'details': 'Ausgewählte schwarze Arbequina-Oliven aus Katalonien und grüne Manzanilla-Oliven aus Sevilla, mariniert mit wildem Thymian, rosa Pfefferkörnern, Knoblauch und bestem Olivenöl extra vergine.'},
        {'name': 'Extra Brot', 'description': 'Frisches spanisches Brot', 'price': 1.90, 'image': 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73', 'details': 'Warmes, knuspriges Pan de Pueblo nach traditionellem kastilischem Rezept. Täglich frisch gebacken mit Steinofenmehl, Meersalz und natürlicher Hefe.'},
        {'name': 'Hummus', 'description': 'Cremiger Kichererbsen-Dip', 'price': 3.90, 'image': 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', 'details': 'Hausgemachter Hummus aus Kichererbsen, Tahini aus Sesam, Zitrone und Kreuzkümmel. Serviert mit frischem Gemüse und warmem Brot.'},
        {'name': 'Spanischer Käseteller', 'description': 'Auswahl spanischer Käsesorten', 'price': 8.90, 'image': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d', 'details': 'Manchego D.O.P. (12 Monate), Cabrales D.O.P. (Blauschimmel) und Murcia al Vino. Serviert mit Walnüssen, Akazienhonig und Moscatel-Trauben.'},
        {'name': 'Schinken-Käse-Wurst Teller', 'description': 'Spanische Charcuterie-Platte', 'price': 11.90, 'image': 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', 'details': 'Jamón Serrano, Chorizo, Lomo und spanische Käse mit Oliven, Nüssen und Feigenmarmelade.'},
        {'name': 'Jamón Serrano Teller', 'description': 'Hochwertiger spanischer Schinken', 'price': 9.90, 'image': 'https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg', 'details': '18 Monate gereifter Jamón Serrano D.O. aus Sierra Nevada, mit Manchego-Käse und geröstetem Brot.'},
        {'name': 'Pata Negra', 'description': 'Premium Iberico Schinken', 'price': 10.90, 'image': 'https://images.unsplash.com/photo-1598989519542-077da0f51c09', 'details': 'Jamón Ibérico de Bellota D.O.P. aus Extremadura, 36 Monate gereift. Von Eichel-gefütterten Iberico-Schweinen.'},
        {'name': 'Tres Dips', 'description': 'Hummus, Avocado Cream, Aioli mit Brot', 'price': 10.90, 'image': 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', 'details': 'Trio aus hausgemachtem Hummus, cremiger Avocado-Creme und Aioli, serviert mit warmem spanischem Brot.'}
    ],
    
    # NEUE KATEGORIEN hinzufügen
    'tapas-carne': [
        {'name': 'Albóndigas en Salsa', 'description': 'Spanische Fleischbällchen in Tomatensauce', 'price': 8.90, 'image': 'https://images.unsplash.com/photo-1559329007-40df8766a171', 'details': 'Hausgemachte Fleischbällchen aus Rind und Schwein in würziger Tomatensauce mit Sherry und frischen Kräutern.'},
        {'name': 'Chorizo a la Plancha', 'description': 'Gegrillte spanische Paprikawurst', 'price': 7.50, 'image': 'https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg', 'details': 'Pikantwurst aus der Region Extremadura, gegrillt und mit Pimentón de la Vera gewürzt.'},
        {'name': 'Pinchitos Morunos', 'description': 'Maurische Fleischspieße', 'price': 9.90, 'image': 'https://images.unsplash.com/photo-1529256354694-69f81f6be3b1', 'details': 'Schweinefleischspieße mariniert mit nordafrikanischen Gewürzen: Kreuzkümmel, Koriander, Paprika und Knoblauch.'},
        {'name': 'Secreto Ibérico', 'description': 'Zartes Iberico-Schweinefleisch', 'price': 12.90, 'image': 'https://images.unsplash.com/photo-1598989519542-077da0f51c09', 'details': 'Das "Geheimstück" vom Iberico-Schwein, gegrillt mit grobem Meersalz und nativem Olivenöl.'},
        {'name': 'Costillas de Cordero', 'description': 'Lammrippchen mit Kräutern', 'price': 11.90, 'image': 'https://images.unsplash.com/photo-1529256354694-69f81f6be3b1', 'details': 'Zarte Lammrippchen mit Rosmarin, Thymian und Knoblauch, langsam geschmort.'}
    ],
    
    'bebidas': [
        {'name': 'Sangría Tinto', 'description': 'Klassische rote Sangría', 'price': 6.50, 'image': 'https://images.unsplash.com/photo-1567522693444-038749b0f0ed', 'details': 'Tempranillo-Wein mit frischen Früchten, Zimt und einem Hauch Brandy. Serviert im traditionellen Krug.'},
        {'name': 'Sangría Blanca', 'description': 'Weiße Sangría mit Früchten', 'price': 6.50, 'image': 'https://images.unsplash.com/photo-1567522693444-038749b0f0ed', 'details': 'Weißwein mit Pfirsich, Melone, Minze und einem Spritzer Cava aus Katalonien.'},
        {'name': 'Rioja Crianza', 'description': 'Rotwein aus der Rioja (Glas)', 'price': 7.90, 'image': 'https://images.unsplash.com/photo-1567522693444-038749b0f0ed', 'details': '14 Monate in Eichenfässern gereifter Tempranillo aus der Rioja Alta.'},
        {'name': 'Albariño', 'description': 'Weißwein aus Galicien (Glas)', 'price': 6.90, 'image': 'https://images.unsplash.com/photo-1567522693444-038749b0f0ed', 'details': 'Frischer Weißwein aus den Rías Baixas, perfekt zu Meeresfrüchten.'},
        {'name': 'Cava Brut', 'description': 'Spanischer Schaumwein (Glas)', 'price': 5.90, 'image': 'https://images.unsplash.com/photo-1567522693444-038749b0f0ed', 'details': 'Traditioneller Cava aus dem Penedès nach der Méthode Champenoise.'},
        {'name': 'Cerveza Estrella Galicia', 'description': 'Galicisches Bier (0,33l)', 'price': 3.90, 'image': 'https://images.pexels.com/photos/5693088/pexels-photo-5693088.jpeg', 'details': 'Hopfiges Lagerbier aus Galicien, gebraut seit 1906.'},
        {'name': 'Clara con Limón', 'description': 'Bier mit Zitronenlimonade', 'price': 3.90, 'image': 'https://images.pexels.com/photos/5693088/pexels-photo-5693088.jpeg', 'details': 'Erfrischende Mischung aus Bier und Zitronenlimonade - perfect für heiße Tage.'}
    ],
    
    'postres': [
        {'name': 'Crema Catalana', 'description': 'Karamellisierte Vanillecreme', 'price': 5.90, 'image': 'https://images.unsplash.com/photo-1563379091339-03246963d68a', 'details': 'Die katalanische Antwort auf Crème brûlée - mit Zimt und Zitronenschale verfeinert.'},
        {'name': 'Flan de Huevo', 'description': 'Traditioneller Karamellpudding', 'price': 4.90, 'image': 'https://images.unsplash.com/photo-1563379091339-03246963d68a', 'details': 'Klassischer spanischer Eierpudding mit flüssigem Karamell.'},
        {'name': 'Torrijas', 'description': 'Spanische geröstete Brotscheiben', 'price': 5.50, 'image': 'https://images.unsplash.com/photo-1563379091339-03246963d68a', 'details': 'In Milch und Ei getränktes Brot, gebraten und mit Zimt und Zucker bestreut.'},
        {'name': 'Helado de Turón', 'description': 'Mandel-Nougat-Eis', 'price': 4.50, 'image': 'https://images.unsplash.com/photo-1563379091339-03246963d68a', 'details': 'Hausgemachtes Eis mit Turrón de Alicante (Mandelcrocant) und gerösteten Mandeln.'},
        {'name': 'Queso Manchego con Membrillo', 'description': 'Manchego-Käse mit Quittengelee', 'price': 7.90, 'image': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d', 'details': 'Gereifter Manchego-Käse mit süßem Quittengelee - eine klassische spanische Kombination.'}
    ],
    
    'arroces': [
        {'name': 'Paella Valenciana (für 2 Personen)', 'description': 'Original Paella aus Valencia', 'price': 32.90, 'image': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e', 'details': 'Authentische Paella mit Huhn, Kaninchen, grünen Bohnen, Garrofón-Bohnen und Safran. Zubereitung: 25 Minuten.'},
        {'name': 'Paella de Mariscos (für 2 Personen)', 'description': 'Meeresfrüchte-Paella', 'price': 36.90, 'image': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e', 'details': 'Mit Garnelen, Muscheln, Calamares und Langostinos. Bomba-Reis mit Meeresfrüchte-Fond und Safran.'},
        {'name': 'Paella Mixta (für 2 Personen)', 'description': 'Gemischte Paella', 'price': 34.90, 'image': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e', 'details': 'Kombiniert Fleisch und Meeresfrüchte: Huhn, Garnelen, Muscheln und Chorizo.'},
        {'name': 'Arroz Negro', 'description': 'Schwarzer Reis mit Tintenfisch', 'price': 16.90, 'image': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e', 'details': 'Bomba-Reis gefärbt mit Tintenfischtinte, Calamares und Aioli.'},
        {'name': 'Arroz con Pollo', 'description': 'Reis mit Hähnchen', 'price': 14.90, 'image': 'https://images.unsplash.com/photo-1630409346606-9b8a5f9ba76e', 'details': 'Saftiges Hähnchen mit Bomba-Reis, Paprika und Erbsen in Safran-Brühe.'}
    ],
    
    'pescado-grande': [
        {'name': 'Lubina a la Sal', 'description': 'Wolfsbarsch in Salzkruste (ganze Portion)', 'price': 24.90, 'image': 'https://images.unsplash.com/photo-1559329007-40df8766a171', 'details': 'Ganzer Wolfsbarsch in Meersalzkruste gebacken, serviert mit geröstetem Gemüse und Zitronen-Olivenöl.'},
        {'name': 'Salmón a la Plancha', 'description': 'Gegrilltes Lachsfilet', 'price': 18.90, 'image': 'https://images.unsplash.com/photo-1559329007-40df8766a171', 'details': 'Frisches Lachsfilet gegrillt, serviert auf Spinat mit Pinienkernen und Rosinen.'},
        {'name': 'Bacalao al Pil Pil', 'description': 'Kabeljau in Olivenöl-Emulsion', 'price': 19.90, 'image': 'https://images.unsplash.com/photo-1559329007-40df8766a171', 'details': 'Traditionelles baskisches Gericht: Kabeljau in einer Emulsion aus Olivenöl, Knoblauch und Chili.'},
        {'name': 'Merluza a la Vasca', 'description': 'Seehecht auf baskische Art', 'price': 17.90, 'image': 'https://images.unsplash.com/photo-1559329007-40df8766a171', 'details': 'Seehecht mit grünen Erbsen, Spargel und hart gekochten Eiern in Weißweinsauce.'}
    ]
}

EXTENDED_CATEGORIES = [
    {'name': 'Inicio', 'slug': 'inicio', 'description': 'Vorspeisen und Einstieg', 'order': 0},
    {'name': 'Salate', 'slug': 'salat', 'description': 'Frische Salate', 'order': 1},
    {'name': 'Kleine Salate', 'slug': 'kleiner-salat', 'description': 'Kleine Beilagensalate', 'order': 2},
    {'name': 'Tapas Vegetarisch', 'slug': 'tapas-vegetarian', 'description': 'Vegetarische und vegane Tapas', 'order': 3},
    {'name': 'Tapas Fisch', 'slug': 'tapas-pescado', 'description': 'Tapas mit Fisch und Meeresfrüchten', 'order': 4},
    {'name': 'Tapas Fleisch', 'slug': 'tapas-carne', 'description': 'Fleisch-Tapas und Wurst', 'order': 5},
    {'name': 'Tapa Paella', 'slug': 'tapa-paella', 'description': 'Paella als Tapa-Portion', 'order': 6},
    {'name': 'Getränke', 'slug': 'bebidas', 'description': 'Weine, Bier und Sangría', 'order': 7},
    {'name': 'Nachspeisen', 'slug': 'postres', 'description': 'Traditionelle spanische Desserts', 'order': 8},
    {'name': 'Reis-Gerichte', 'slug': 'arroces', 'description': 'Paellas und Reis-Spezialitäten', 'order': 9},
    {'name': 'Fisch-Hauptgerichte', 'slug': 'pescado-grande', 'description': 'Große Fischgerichte', 'order': 10}
]

async def extend_menu_completely():
    """Erweitere das Menu um alle fehlenden Kategorien und Items"""
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🚀 Extending menu with ALL missing categories and items...")
    
    try:
        # Update/Insert categories
        print("📂 Updating menu categories...")
        await db.menu_categories.delete_many({})
        
        for category_data in EXTENDED_CATEGORIES:
            category = {
                'id': str(uuid.uuid4()),
                **category_data,
                'is_active': True,
                'created_at': datetime.utcnow()
            }
            await db.menu_categories.insert_one(category)
            print(f"  ✅ {category['name']} ({category['slug']})")
        
        # Add new menu items for new categories
        print("🍽️  Adding missing menu items...")
        item_count = 0
        
        for category_slug, items in EXTENDED_MENU_DATA.items():
            if category_slug in ['tapas-carne', 'bebidas', 'postres', 'arroces', 'pescado-grande']:
                # These are new categories
                for i, item_data in enumerate(items):
                    menu_item = {
                        'id': str(uuid.uuid4()),
                        'name': item_data['name'],
                        'description': item_data['description'],
                        'detailed_description': item_data.get('details', ''),
                        'price': item_data['price'],
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
                    print(f"  ✅ {item_data['name']} ({category_slug}) - {item_data['price']}€")
        
        print(f"\n🎉 Menu extension completed!")
        print(f"📊 Summary:")
        print(f"   - Total Categories: {len(EXTENDED_CATEGORIES)}")
        print(f"   - New Items Added: {item_count}")
        
        # Count total items
        total_items = await db.menu_items.count_documents({'is_active': True})
        print(f"   - Total Menu Items: {total_items}")
        
    except Exception as e:
        print(f"❌ Extension failed: {str(e)}")
        raise e
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(extend_menu_completely())
#!/usr/bin/env python3
"""
Complete Menu Import Script for Jimmy's Tapas Bar
Imports the complete menu with all categories and items
"""

import asyncio
import aiomysql
import os
import uuid
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

# Complete menu data
COMPLETE_MENU = {
    "INICIO": [
        {"name": "Aioli", "description": "Hausgemachte Knoblauch-Mayonnaise", "price": "3,50 €"},
        {"name": "Oliven", "description": "Marinierte spanische Oliven", "price": "3,90 €"},
        {"name": "Pan con Tomate", "description": "Geröstetes Brot mit Tomate und Olivenöl", "price": "4,50 €"},
        {"name": "Queso Manchego", "description": "Spanischer Schafskäse mit Honig", "price": "7,90 €"},
        {"name": "Jamón Serrano", "description": "Luftgetrockneter spanischer Schinken", "price": "9,90 €"},
        {"name": "Tabla de Quesos", "description": "Auswahl spanischer Käsesorten", "price": "12,90 €"},
    ],
    "SALAT": [
        {"name": "Ensalada Mixta", "description": "Gemischter Salat mit spanischen Zutaten", "price": "8,90 €"},
        {"name": "Ensalada de Cabra", "description": "Ziegenkäse-Salat mit Walnüssen und Honig", "price": "9,90 €"},
        {"name": "Ensalada Mediterránea", "description": "Mediterraner Salat mit Oliven und Feta", "price": "10,90 €"},
        {"name": "Ensalada de Pollo", "description": "Hähnchen-Salat mit Avocado", "price": "11,90 €"},
    ],
    "KLEINER SALAT": [
        {"name": "Ensalada Verde", "description": "Grüner Blattsalat", "price": "5,90 €"},
        {"name": "Ensalada de Tomate", "description": "Tomatensalat mit Zwiebeln", "price": "6,50 €"},
    ],
    "TAPA PAELLA": [
        {"name": "Paella Valenciana", "description": "Traditionelle Paella mit Huhn und Gemüse", "price": "16,90 €"},
        {"name": "Paella de Mariscos", "description": "Meeresfrüchte-Paella", "price": "18,90 €"},
        {"name": "Paella Mixta", "description": "Gemischte Paella mit Fleisch und Meeresfrüchten", "price": "17,90 €"},
        {"name": "Paella Vegetariana", "description": "Vegetarische Paella mit Gemüse", "price": "15,90 €"},
    ],
    "TAPAS VEGETARIAN": [
        {"name": "Patatas Bravas", "description": "Kartoffeln mit scharfer Sauce", "price": "5,90 €"},
        {"name": "Pimientos de Padrón", "description": "Gebratene grüne Paprika", "price": "6,50 €"},
        {"name": "Tortilla Española", "description": "Spanisches Kartoffel-Omelett", "price": "7,90 €"},
        {"name": "Champiñones al Ajillo", "description": "Champignons in Knoblauchöl", "price": "6,90 €"},
        {"name": "Espinacas con Garbanzos", "description": "Spinat mit Kichererbsen", "price": "7,50 €"},
        {"name": "Berenjenas con Miel", "description": "Auberginen mit Honig", "price": "7,90 €"},
    ],
    "TAPAS DE POLLO": [
        {"name": "Pollo al Ajillo", "description": "Hähnchen in Knoblauchöl", "price": "8,90 €"},
        {"name": "Alitas de Pollo", "description": "Hähnchen-Flügel mariniert", "price": "7,90 €"},
        {"name": "Pollo con Pimientos", "description": "Hähnchen mit Paprika", "price": "9,50 €"},
        {"name": "Pinchitos de Pollo", "description": "Hähnchen-Spieße", "price": "8,50 €"},
    ],
    "TAPAS DE CARNE": [
        {"name": "Chorizo al Vino", "description": "Chorizo in Rotwein", "price": "8,90 €"},
        {"name": "Albóndigas", "description": "Fleischbällchen in Tomatensauce", "price": "9,50 €"},
        {"name": "Morcilla", "description": "Spanische Blutwurst", "price": "7,90 €"},
        {"name": "Lomo al Ajillo", "description": "Schweinelende in Knoblauchöl", "price": "10,90 €"},
        {"name": "Pinchitos Morunos", "description": "Gewürzte Fleischspieße", "price": "9,90 €"},
    ],
    "TAPAS DE PESCADO": [
        {"name": "Gambas al Ajillo", "description": "Garnelen in Knoblauchöl", "price": "10,90 €"},
        {"name": "Gambas al Pil Pil", "description": "Garnelen scharf", "price": "11,50 €"},
        {"name": "Pulpo a la Gallega", "description": "Galicischer Oktopus", "price": "12,90 €"},
        {"name": "Calamares a la Romana", "description": "Tintenfischringe paniert", "price": "9,90 €"},
        {"name": "Boquerones", "description": "Eingelegte Sardellen", "price": "8,50 €"},
        {"name": "Bacalao al Pil Pil", "description": "Kabeljau in Olivenöl", "price": "13,90 €"},
    ],
    "KROKETTEN": [
        {"name": "Croquetas de Jamón", "description": "Schinken-Kroketten", "price": "7,90 €"},
        {"name": "Croquetas de Pollo", "description": "Hähnchen-Kroketten", "price": "7,50 €"},
        {"name": "Croquetas de Bacalao", "description": "Kabeljau-Kroketten", "price": "8,50 €"},
        {"name": "Croquetas de Espinacas", "description": "Spinat-Kroketten", "price": "7,50 €"},
    ],
    "PASTA": [
        {"name": "Spaghetti Aglio e Olio", "description": "Mit Knoblauch und Olivenöl", "price": "9,90 €"},
        {"name": "Penne Arrabbiata", "description": "Mit scharfer Tomatensauce", "price": "10,50 €"},
        {"name": "Linguine alle Vongole", "description": "Mit Venusmuscheln", "price": "13,90 €"},
        {"name": "Rigatoni Carbonara", "description": "Mit Speck und Ei", "price": "11,90 €"},
    ],
    "PIZZA": [
        {"name": "Pizza Margherita", "description": "Mit Tomaten und Mozzarella", "price": "8,90 €"},
        {"name": "Pizza Prosciutto", "description": "Mit Schinken", "price": "10,90 €"},
        {"name": "Pizza Quattro Stagioni", "description": "Vier Jahreszeiten", "price": "12,90 €"},
        {"name": "Pizza Española", "description": "Mit Chorizo und Manchego", "price": "13,50 €"},
    ],
    "SNACKS": [
        {"name": "Montaditos", "description": "Kleine belegte Brote (3 Stück)", "price": "6,90 €"},
        {"name": "Tostas", "description": "Geröstete Brotscheiben mit Belag", "price": "5,90 €"},
        {"name": "Bravas Especiales", "description": "Kartoffeln mit verschiedenen Saucen", "price": "7,50 €"},
    ],
    "DESSERT": [
        {"name": "Flan Casero", "description": "Hausgemachter Karamellpudding", "price": "4,90 €"},
        {"name": "Crema Catalana", "description": "Katalanische Creme", "price": "5,50 €"},
        {"name": "Torrijas", "description": "Spanische French Toast", "price": "5,90 €"},
        {"name": "Tarta de Santiago", "description": "Mandelkuchen aus Galicien", "price": "6,50 €"},
        {"name": "Churros con Chocolate", "description": "Mit heißer Schokolade", "price": "5,90 €"},
    ],
    "HELADOS": [
        {"name": "Helado de Vainilla", "description": "Vanilleeis", "price": "3,50 €"},
        {"name": "Helado de Chocolate", "description": "Schokoladeneis", "price": "3,50 €"},
        {"name": "Helado de Fresa", "description": "Erdbeereis", "price": "3,50 €"},
        {"name": "Helado de Turron", "description": "Nougat-Eis", "price": "4,50 €"},
        {"name": "Copa de Helado", "description": "Eisbecher mit Früchten", "price": "6,90 €"},
    ]
}

async def import_complete_menu():
    """Import the complete menu into MySQL database"""
    print("🍽️  Starting complete menu import for Jimmy's Tapas Bar")
    print("=" * 60)
    
    try:
        # Connect to MySQL
        conn = await aiomysql.connect(**mysql_config)
        cursor = await conn.cursor()
        
        # Clear existing menu items
        print("🗑️  Clearing existing menu items...")
        await cursor.execute("DELETE FROM menu_items")
        
        total_items = 0
        order_index = 0
        
        # Import each category
        for category, items in COMPLETE_MENU.items():
            print(f"📂 Importing category: {category} ({len(items)} items)")
            
            for item in items:
                order_index += 1
                item_id = str(uuid.uuid4())
                
                # Determine dietary flags based on category
                vegan = category in ["TAPAS VEGETARIAN"] and "Queso" not in item["name"] and "Jamón" not in item["name"]
                vegetarian = category in ["TAPAS VEGETARIAN", "PASTA"] or "Vegetariana" in item["name"]
                glutenfree = False  # Would need specific indication
                
                await cursor.execute("""
                    INSERT INTO menu_items (id, name, description, price, category, image, details,
                                           vegan, vegetarian, glutenfree, order_index, is_active,
                                           created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    item_id, item["name"], item["description"], item["price"], category, None,
                    None, vegan, vegetarian, glutenfree, order_index, True,
                    datetime.utcnow(), datetime.utcnow()
                ))
                
                total_items += 1
        
        print(f"✅ Successfully imported {total_items} menu items across {len(COMPLETE_MENU)} categories")
        
        # Display summary
        print("\n📊 Menu Import Summary:")
        for category, items in COMPLETE_MENU.items():
            print(f"   {category}: {len(items)} items")
        
        print(f"\n🎉 Complete menu import finished successfully!")
        print(f"Total items: {total_items}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Menu import failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(import_complete_menu())
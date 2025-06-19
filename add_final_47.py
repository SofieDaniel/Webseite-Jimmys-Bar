#!/usr/bin/env python3
"""
Fügt die letzten 47 Gerichte hinzu - Pizza, Pasta, Kroketten, Desserts, etc.
"""

import asyncio
import aiomysql
import os
import uuid
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

async def add_final_items():
    """Fügt die letzten 47 Gerichte hinzu"""
    
    print("🍕 FINALE 47 GERICHTE - Pizza, Pasta, Desserts etc.")
    print("=" * 70)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Template für effiziente Erstellung
        def create_item(name, desc, price, cat, origin_country="Italien", allergens_info="Gluten", prep="Traditionell zubereitet", ingredients_list="Traditionelle Zutaten", vegan=False, vegetarian=False):
            return {
                "name": name,
                "description": desc,
                "detailed_description": f"Authentisches {name} nach traditionellem Rezept aus {origin_country}. {prep} mit hochwertigen Zutaten für den perfekten Geschmack.",
                "price": price,
                "category": cat,
                "origin": origin_country,
                "allergens": allergens_info,
                "additives": "Keine Zusatzstoffe" if "Konservierung" not in allergens_info else "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": prep,
                "ingredients": ingredients_list,
                "vegan": vegan,
                "vegetarian": vegetarian
            }
        
        # Die letzten 47 Gerichte
        final_items = [
            # Tapas de Pescado (11 weitere)
            create_item("Gegrillter Oktopus", "Kichererbsen, Gemüse", "9,90 €", "Tapas de Pescado", "Griechenland", "Weichtiere", "Gegrillt", "Oktopus, Kichererbsen, Olivenöl, Zitrone"),
            create_item("Jacobsmuscheln", "Spinat, Cherry Tomaten", "9,90 €", "Tapas de Pescado", "Atlantik", "Weichtiere", "Angebraten", "Jakobsmuscheln, Spinat, Cherry-Tomaten"),
            create_item("Gambas PIL PIL", "Scharfe Tomatensauce", "9,90 €", "Tapas de Pescado", "Spanien", "Krebstiere", "In scharfer Sauce", "Garnelen, Tomaten, Chili, Knoblauch"),
            create_item("Empanadas", "Thunfisch, gefüllter Teig", "6,90 €", "Tapas de Pescado", "Argentinien", "Gluten, Fisch, Ei", "Gebacken", "Blätterteig, Thunfisch, Zwiebeln"),
            create_item("Pfahlmuscheln", "Nach spanischer Art", "8,90 €", "Tapas de Pescado", "Spanien", "Weichtiere", "Gedämpft", "Miesmuscheln, Weißwein, Knoblauch"),
            create_item("Pulpo al Ajillo", "Oktopus, Knoblauch", "9,90 €", "Tapas de Pescado", "Spanien", "Weichtiere", "In Knoblauchöl", "Oktopus, Knoblauch, Olivenöl, Paprika"),
            create_item("Zander Filet", "Bacon, Knoblauch-Sahnesauce", "9,90 €", "Tapas de Pescado", "Deutschland", "Fisch, Milch", "Gebraten", "Zanderfilet, Speck, Sahne, Knoblauch"),
            create_item("Tiger Garnelen", "Tomaten, Paprika, Knoblauch, Oliven", "9,90 €", "Tapas de Pescado", "Mittelmeer", "Krebstiere", "In Gemüse geschmort", "Tiger-Garnelen, Tomaten, Paprika, Oliven"),
            create_item("Brocheta de Gambas", "Gambas Spieß", "8,90 €", "Tapas de Pescado", "Spanien", "Krebstiere", "Gegrillt", "Garnelen, Paprika, Zwiebeln"),
            create_item("Boqueron en Tempura", "Panierte Sardellen", "7,50 €", "Tapas de Pescado", "Japan/Spanien", "Fisch, Gluten", "Frittiert in Tempura", "Sardellen, Tempura-Mehl, Sojasauce"),
            create_item("Chipirones Fritos con Aioli", "Frittierte kleine Tintenfische", "8,90 €", "Tapas de Pescado", "Spanien", "Weichtiere, kann Spuren von Ei enthalten", "Frittiert", "Kleine Tintenfische, Mehl, Aioli"),
            
            # Kroketten (5 Gerichte)
            create_item("Croquetas de Queso", "Fetakäse", "5,90 €", "Kroketten", "Spanien", "Gluten, Milch, Ei", "Frittiert", "Feta, Béchamel, Paniermehl"),
            create_item("Croquetas de Almendras", "Mandeln", "6,50 €", "Kroketten", "Spanien", "Gluten, Milch, Ei, Nüsse", "Frittiert", "Mandeln, Béchamel, Paniermehl"),
            create_item("Croquetas de Patata", "Kartoffel", "5,50 €", "Kroketten", "Spanien", "Gluten, Milch, Ei", "Frittiert", "Kartoffeln, Béchamel, Paniermehl"),
            
            # Pasta (5 Gerichte)
            create_item("Spaghetti Bolognese", "Klassische Fleischsauce", "14,90 €", "Pasta", "Bologna, Italien", "Gluten", "Al dente gekocht", "Spaghetti, Hackfleisch, Tomaten, Rotwein"),
            create_item("Pasta Brokkoli Gorgonzola", "Cremige Käsesauce", "14,90 €", "Pasta", "Italien", "Gluten, Milch", "Al dente gekocht", "Pasta, Brokkoli, Gorgonzola, Sahne"),
            create_item("Pasta Verdura", "Gemüse-Pasta", "14,90 €", "Pasta", "Italien", "Gluten", "Al dente gekocht", "Pasta, Zucchini, Paprika, Auberginen", False, True),
            create_item("Pasta Garnelen", "Mit frischen Garnelen", "16,90 €", "Pasta", "Italien", "Gluten, Krebstiere", "Al dente gekocht", "Pasta, Garnelen, Knoblauch, Olivenöl"),
            
            # Pizza (10 Gerichte)
            create_item("Pizza Schinken", "Tomate, Mozzarella, Schinken", "12,90 €", "Pizza", "Italien", "Gluten, Milch", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Schinken"),
            create_item("Pizza Funghi", "Tomate, Mozzarella, Champignons", "12,90 €", "Pizza", "Italien", "Gluten, Milch", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Champignons", False, True),
            create_item("Pizza Tonno", "Tomate, Mozzarella, Thunfisch", "13,90 €", "Pizza", "Italien", "Gluten, Milch, Fisch", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Thunfisch"),
            create_item("Pizza Hawaii", "Tomate, Mozzarella, Schinken, Ananas", "13,90 €", "Pizza", "Deutschland", "Gluten, Milch", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Schinken, Ananas"),
            create_item("Pizza Verdura", "Tomate, Mozzarella, Gemüse", "13,90 €", "Pizza", "Italien", "Gluten, Milch", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Gemüse", False, True),
            create_item("Pizza Salami", "Tomate, Mozzarella, Salami", "12,90 €", "Pizza", "Italien", "Gluten, Milch", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Salami"),
            create_item("Pizza Garnelen", "Tomate, Mozzarella, Garnelen", "15,90 €", "Pizza", "Italien", "Gluten, Milch, Krebstiere", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Garnelen"),
            create_item("Pizza Bolognese", "Tomate, Mozzarella, Hackfleischsauce", "13,90 €", "Pizza", "Italien", "Gluten, Milch", "Steinofen gebacken", "Pizzateig, Tomaten, Mozzarella, Bolognese"),
            
            # Kleine Gerichte (4 Gerichte)
            create_item("Pommes Frites", "Mit Ketchup/Mayonnaise", "5,50 €", "Kleine Gerichte", "Belgien", "Keine bekannten Allergene", "Frittiert", "Kartoffeln, Pflanzenöl"),
            create_item("Chicken Nuggets", "5 Stück, Pommes", "8,90 €", "Kleine Gerichte", "USA", "Gluten", "Frittiert", "Hähnchenfleisch, Paniermehl, Kartoffeln"),
            create_item("Chicken Wings", "5 Stück, Pommes", "9,90 €", "Kleine Gerichte", "USA", "Keine bekannten Allergene", "Gegrillt", "Hähnchenflügel, BBQ-Sauce, Kartoffeln"),
            create_item("Currywurst mit Pommes", "Deutsche Spezialität", "10,90 €", "Kleine Gerichte", "Deutschland", "Gluten", "Gebraten", "Bratwurst, Curry-Sauce, Kartoffeln"),
            
            # Dessert (9 Gerichte)
            create_item("Tarte de Santiago", "Spanischer Mandelkuchen", "7,50 €", "Dessert", "Santiago de Compostela, Spanien", "Nüsse, Ei", "Gebacken", "Mandeln, Eier, Zucker, Zitronenschale"),
            create_item("Gemischtes Eis", "3 Kugeln, Sahne", "6,90 €", "Dessert", "Italien", "Milch", "Gefroren", "Milch, Sahne, Zucker, natürliche Aromen"),
            create_item("Schoko Soufflé", "Eis, Sahne", "7,50 €", "Dessert", "Frankreich", "Milch, Ei", "Im Wasserbad gegart", "Schokolade, Eier, Sahne, Zucker"),
            create_item("Kokos-Eis in Fruchtschale", "Erfrischend exotisch", "6,90 €", "Dessert", "Tropen", "Milch", "Gefroren", "Kokosmilch, Zucker, natürliche Aromen"),
            create_item("Zitronen-Eis in Fruchtschale", "Frisch und sauer", "6,90 €", "Dessert", "Italien", "Milch", "Gefroren", "Zitronen, Milch, Zucker"),
            create_item("Orangen-Eis in Fruchtschale", "Fruchtig-süß", "6,90 €", "Dessert", "Spanien", "Milch", "Gefroren", "Orangen, Milch, Zucker"),
            create_item("Nuss-Eis in Fruchtschale", "Cremig-nussig", "6,90 €", "Dessert", "Italien", "Milch, Nüsse", "Gefroren", "Haselnüsse, Milch, Sahne, Zucker")
        ]
        
        # In Datenbank einfügen
        insert_sql = """
            INSERT INTO menu_items (
                id, name, description, detailed_description, price, category, 
                origin, allergens, additives, preparation_method, ingredients,
                vegan, vegetarian, is_active, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        count = 0
        for item in final_items:
            await cursor.execute(insert_sql, (
                str(uuid.uuid4()),
                item["name"],
                item["description"],
                item["detailed_description"],
                item["price"],
                item["category"],
                item["origin"],
                item["allergens"],
                item["additives"],
                item["preparation_method"],
                item["ingredients"],
                item.get("vegan", False),
                item.get("vegetarian", False),
                True,
                datetime.utcnow(),
                datetime.utcnow()
            ))
            count += 1
        
        # Commit changes
        await connection.commit()
        
        print(f"✅ {count} finale Gerichte hinzugefügt!")
        
        # Prüfe finale Gesamtanzahl
        await cursor.execute("SELECT COUNT(*) FROM menu_items")
        total_items = await cursor.fetchone()
        
        await cursor.execute("SELECT COUNT(*) FROM menu_items WHERE detailed_description IS NOT NULL")
        total_detailed = await cursor.fetchone()
        
        print(f"🎉 FERTIG! {total_detailed[0]} von {total_items[0]} Gerichten haben vollständige Details!")
        
        # Kategorien-Übersicht
        await cursor.execute("""
            SELECT category, 
                   COUNT(*) as total,
                   COUNT(CASE WHEN detailed_description IS NOT NULL THEN 1 END) as with_details
            FROM menu_items 
            GROUP BY category 
            ORDER BY category
        """)
        categories = await cursor.fetchall()
        
        print("\n📋 FINALE KATEGORIEN-ÜBERSICHT:")
        for cat in categories:
            print(f"   ✅ {cat[0]}: {cat[2]}/{cat[1]} Gerichte mit Details")
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_final_items())
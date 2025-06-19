#!/usr/bin/env python3
"""
Neue komplette Jimmy's Tapas Bar Speisekarte erstellen
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

async def create_complete_menu():
    """Erstellt die komplette neue Jimmy's Tapas Bar Speisekarte"""
    
    print("🍽️ NEUE JIMMY'S TAPAS BAR SPEISEKARTE ERSTELLEN")
    print("=" * 60)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Lösche alte Menu-Items
        await cursor.execute("DELETE FROM menu_items")
        print("✅ Alte Speisekarte gelöscht")
        
        # Neue komplette Speisekarte
        menu_items = [
            # 1. Inicio / Vorspeisen
            {"name": "Aioli", "description": "Knoblauchsauce mit Öl", "price": "3,50 €", "category": "Inicio / Vorspeisen"},
            {"name": "Oliven", "description": "Spanische Oliven", "price": "3,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Extra Brot", "description": "Frisches Brot", "price": "1,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Hummus", "description": "Kichererbsen Cream", "price": "3,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Guacamole", "description": "Avocado Cream", "price": "3,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Spanischer Käseteller", "description": "Manchego", "price": "8,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Schinken-Käse-Wurst Teller", "description": "Spanische Auswahl", "price": "11,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Jamón Serrano Teller", "description": "Spanischer Serrano Schinken", "price": "9,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Boquerones en Vinagre", "description": "Mit Essig und Öl", "price": "8,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Pata Negra", "description": "Spanischer Ibérico Schinken", "price": "8,90 €", "category": "Inicio / Vorspeisen"},
            {"name": "Tres", "description": "Hummus, Avocado Cream, Aioli mit Brot", "price": "10,90 €", "category": "Inicio / Vorspeisen"},
            
            # 2. Salat
            {"name": "Ensalada Mixta", "description": "Bunter Salat mit Essig und Öl", "price": "8,90 €", "category": "Salat"},
            {"name": "Ensalada Tonno", "description": "Bunter Salat mit Thunfisch", "price": "14,90 €", "category": "Salat"},
            {"name": "Ensalada Pollo", "description": "Bunter Salat mit Hähnchenstreifen", "price": "14,90 €", "category": "Salat"},
            {"name": "Ensalada Garnelen", "description": "Bunter Salat mit Garnelen", "price": "15,90 €", "category": "Salat"},
            {"name": "Tomaten/Gurken Salat", "description": "Mit Zwiebeln", "price": "6,90 €", "category": "Salat"},
            {"name": "Rote Beete Salat", "description": "Mit Ziegenkäse", "price": "7,90 €", "category": "Salat"},
            {"name": "Kichererbsen Salat", "description": "Mit Feta", "price": "7,90 €", "category": "Salat"},
            
            # 3. Tapa Paella
            {"name": "Paella", "description": "Mit Hähnchen und Meeresfrüchten", "price": "8,90 €", "category": "Tapa Paella"},
            {"name": "Paella Vegetarisch", "description": "Vegetarische Paella", "price": "7,90 €", "category": "Tapa Paella"},
            
            # 4. Tapas Vegetarian
            {"name": "Gebratenes Gemüse der Saison", "description": "Vegan", "price": "6,90 €", "category": "Tapas Vegetarian", "vegan": True},
            {"name": "Papas Bravas", "description": "Klassische spanische Kartoffeln - Vegan", "price": "6,90 €", "category": "Tapas Vegetarian", "vegan": True},
            {"name": "Tortilla de Patata con Aioli", "description": "Spanisches Kartoffel-Omelett mit Aioli", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Pimientos de Padrón", "description": "Gebratene kleine Paprika - Vegan", "price": "6,90 €", "category": "Tapas Vegetarian", "vegan": True},
            {"name": "Kanarische Kartoffeln im Salzmantel", "description": "Papas Arrugadas - Vegan", "price": "6,90 €", "category": "Tapas Vegetarian", "vegan": True},
            {"name": "Fetakäse Häppchen", "description": "Griechischer Feta", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Rosmarin Ziegenkäse", "description": "Mit frischem Rosmarin", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Falafel", "description": "Orientalische Kichererbsenbällchen", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Feta Käse überbacken Cherry", "description": "Mit Cherry Tomaten überbacken", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Überbackene Champignons", "description": "Mit Käse überbacken", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Überbackene Tomaten", "description": "Mit Käse und Kräutern", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Frittierte Auberginen mit Honig", "description": "Süß-salzige Kombination", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Champignons al Ajillo", "description": "In Knoblauchöl - Vegan", "price": "6,90 €", "category": "Tapas Vegetarian", "vegan": True},
            {"name": "Teigröllchen mit Spinat", "description": "Blätterteig gefüllt mit Spinat", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Feta Feigen", "description": "Feta mit frischen Feigen", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Ziegenkäse überbacken", "description": "Gratinierter Ziegenkäse", "price": "6,90 €", "category": "Tapas Vegetarian", "vegetarian": True},
            {"name": "Gebratener Spinat mit Cherry Tomaten", "description": "Frischer Spinat - Vegan", "price": "6,90 €", "category": "Tapas Vegetarian", "vegan": True},
            
            # 5. Tapas de Pollo
            {"name": "Hähnchen Filet mit Limetten Sauce", "description": "Zart gegrillt mit frischer Limette", "price": "7,20 €", "category": "Tapas de Pollo"},
            {"name": "Knusprige Hähnchen Tapas", "description": "Mit Honig-Senf Sauce", "price": "7,20 €", "category": "Tapas de Pollo"},
            {"name": "Hähnchen Spieß", "description": "Mit scharfer Sauce", "price": "7,20 €", "category": "Tapas de Pollo"},
            {"name": "Hähnchen Filet mit Curry Sauce", "description": "Exotische Gewürzmischung", "price": "7,20 €", "category": "Tapas de Pollo"},
            {"name": "Hähnchen Filet mit Mandel Sauce", "description": "Cremige Mandelsauce", "price": "7,20 €", "category": "Tapas de Pollo"},
            {"name": "Gegrillter Hähnchen-Chorizo-Spieß", "description": "Spanische Chorizo mit Hähnchen", "price": "7,20 €", "category": "Tapas de Pollo"},
            {"name": "Hähnchen Filet mit Brandy Sauce", "description": "In edler Brandy-Sauce", "price": "7,20 €", "category": "Tapas de Pollo"},
            
            # 6. Tapas de Carne
            {"name": "Dátiles con Bacon", "description": "Datteln im Speckmantel", "price": "6,90 €", "category": "Tapas de Carne"},
            {"name": "Albondigas a la Casera", "description": "Hackbällchen mit Tomatensauce", "price": "6,90 €", "category": "Tapas de Carne"},
            {"name": "Pincho de Cerdo", "description": "Schweinespieß scharf", "price": "7,90 €", "category": "Tapas de Carne"},
            {"name": "Pincho de Cordero", "description": "Lammspieß scharf", "price": "8,90 €", "category": "Tapas de Carne"},
            {"name": "Chuletas de Cordero", "description": "2 Lammkoteletts", "price": "9,90 €", "category": "Tapas de Carne"},
            {"name": "Rollitos de Serrano con Higo", "description": "Feigen/Serrano, Frischkäse", "price": "9,90 €", "category": "Tapas de Carne"},
            {"name": "Queso de Cabra con Bacon", "description": "Ziegenkäse/Speck", "price": "7,90 €", "category": "Tapas de Carne"},
            {"name": "Chorizo al Diablo", "description": "In Rotweinsauce", "price": "7,90 €", "category": "Tapas de Carne"},
            {"name": "Medallions de Carne", "description": "Rinderfilet, Pilz-Ragout", "price": "9,90 €", "category": "Tapas de Carne"},
            {"name": "Mit Käse gefüllte Champignons", "description": "Bacon, Kräuter", "price": "8,90 €", "category": "Tapas de Carne"},
            {"name": "Schweinefilet mit Cherry Tomaten", "description": "Mango-Honig", "price": "9,50 €", "category": "Tapas de Carne"},
            {"name": "Schweinefilet", "description": "Spinat, Pilze, Cremefraiche", "price": "9,50 €", "category": "Tapas de Carne"},
            {"name": "Chorizo a la Plancha", "description": "Gegrillt", "price": "7,90 €", "category": "Tapas de Carne"},
            {"name": "Lammfilet", "description": "Mit Pfeffersauce", "price": "9,90 €", "category": "Tapas de Carne"},
            {"name": "Spareribs mit BBQ-Sauce", "description": "Amerikanisch mariniert", "price": "9,90 €", "category": "Tapas de Carne"},
            {"name": "Chicken Wings", "description": "Mit süßer Chillisauce", "price": "9,90 €", "category": "Tapas de Carne"},
            
            # 7. Tapas de Pescado
            {"name": "Boquerones Fritos", "description": "Frittierte Sardellen", "price": "7,50 €", "category": "Tapas de Pescado"},
            {"name": "Calamares a la Plancha", "description": "Gegrillt", "price": "8,90 €", "category": "Tapas de Pescado"},
            {"name": "Calamares a la Romana", "description": "Frittiert mit Aioli", "price": "7,50 €", "category": "Tapas de Pescado"},
            {"name": "Salmon con Espinaca", "description": "Lachsfilet auf Spinat", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Gambas a la Plancha", "description": "Gegrillte Tiger-Garnelen, Gemüse", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Garnelen-Dattel-Spieß", "description": "Speckmantel, Honig-Senf", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Gambas al Ajillo", "description": "Knoblauch-Olivenöl", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Muslitos de Mar", "description": "Krebsfleischbällchen", "price": "6,90 €", "category": "Tapas de Pescado"},
            {"name": "Gegrillter Oktopus", "description": "Kichererbsen, Gemüse", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Jacobsmuscheln", "description": "Spinat, Cherry Tomaten", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Gambas PIL PIL", "description": "Scharfe Tomatensauce", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Empanadas", "description": "Thunfisch, gefüllter Teig", "price": "6,90 €", "category": "Tapas de Pescado"},
            {"name": "Pfahlmuscheln", "description": "Nach spanischer Art", "price": "8,90 €", "category": "Tapas de Pescado"},
            {"name": "Pulpo al Ajillo", "description": "Oktopus, Knoblauch", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Zander Filet", "description": "Bacon, Knoblauch-Sahnesauce", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Tiger Garnelen", "description": "Tomaten, Paprika, Knoblauch, Oliven", "price": "9,90 €", "category": "Tapas de Pescado"},
            {"name": "Brocheta de Gambas", "description": "Gambas Spieß", "price": "8,90 €", "category": "Tapas de Pescado"},
            {"name": "Boqueron en Tempura", "description": "Panierte Sardellen", "price": "7,50 €", "category": "Tapas de Pescado"},
            {"name": "Chipirones Fritos con Aioli", "description": "Frittierte kleine Tintenfische", "price": "8,90 €", "category": "Tapas de Pescado"},
            
            # 8. Kroketten
            {"name": "Croquetas de Bacalao", "description": "Stockfisch", "price": "5,90 €", "category": "Kroketten"},
            {"name": "Croquetas de Queso", "description": "Fetakäse", "price": "5,90 €", "category": "Kroketten"},
            {"name": "Croquetas de Almendras", "description": "Mandeln", "price": "6,50 €", "category": "Kroketten"},
            {"name": "Croquetas de Jamón", "description": "Serrano Schinken", "price": "5,90 €", "category": "Kroketten"},
            {"name": "Croquetas de Patata", "description": "Kartoffel", "price": "5,50 €", "category": "Kroketten"},
            
            # 9. Pasta
            {"name": "Spaghetti Aglio e Olio", "description": "Mit Knoblauch und Olivenöl", "price": "12,90 €", "category": "Pasta"},
            {"name": "Spaghetti Bolognese", "description": "Klassische Fleischsauce", "price": "14,90 €", "category": "Pasta"},
            {"name": "Pasta Brokkoli Gorgonzola", "description": "Cremige Käsesauce", "price": "14,90 €", "category": "Pasta"},
            {"name": "Pasta Verdura", "description": "Gemüse-Pasta", "price": "14,90 €", "category": "Pasta"},
            {"name": "Pasta Garnelen", "description": "Mit frischen Garnelen", "price": "16,90 €", "category": "Pasta"},
            
            # 10. Pizza
            {"name": "Pizza Margharita", "description": "Tomate, Mozzarella, Basilikum", "price": "9,90 €", "category": "Pizza"},
            {"name": "Pizza Schinken", "description": "Tomate, Mozzarella, Schinken", "price": "12,90 €", "category": "Pizza"},
            {"name": "Pizza Funghi", "description": "Tomate, Mozzarella, Champignons", "price": "12,90 €", "category": "Pizza"},
            {"name": "Pizza Tonno", "description": "Tomate, Mozzarella, Thunfisch", "price": "13,90 €", "category": "Pizza"},
            {"name": "Pizza Hawaii", "description": "Tomate, Mozzarella, Schinken, Ananas", "price": "13,90 €", "category": "Pizza"},
            {"name": "Pizza Verdura", "description": "Tomate, Mozzarella, Gemüse", "price": "13,90 €", "category": "Pizza"},
            {"name": "Pizza Salami", "description": "Tomate, Mozzarella, Salami", "price": "12,90 €", "category": "Pizza"},
            {"name": "Pizza Garnelen", "description": "Tomate, Mozzarella, Garnelen", "price": "15,90 €", "category": "Pizza"},
            {"name": "Pizza Bolognese", "description": "Tomate, Mozzarella, Hackfleischsauce", "price": "13,90 €", "category": "Pizza"},
            {"name": "Jimmy's Special Pizza", "description": "Hausspezialität", "price": "13,90 €", "category": "Pizza"},
            
            # 11. Für den kleinen und großen Hunger
            {"name": "Pommes Frites", "description": "Mit Ketchup/Mayonnaise", "price": "5,50 €", "category": "Kleine Gerichte"},
            {"name": "Chicken Nuggets", "description": "5 Stück, Pommes", "price": "8,90 €", "category": "Kleine Gerichte"},
            {"name": "Chicken Wings", "description": "5 Stück, Pommes", "price": "9,90 €", "category": "Kleine Gerichte"},
            {"name": "Currywurst mit Pommes", "description": "Deutsche Spezialität", "price": "10,90 €", "category": "Kleine Gerichte"},
            
            # 12. Dessert & Eis
            {"name": "Crema Catalana", "description": "Spanische Crème brûlée", "price": "5,50 €", "category": "Dessert"},
            {"name": "Tarte de Santiago", "description": "Spanischer Mandelkuchen", "price": "7,50 €", "category": "Dessert"},
            {"name": "Gemischtes Eis", "description": "3 Kugeln, Sahne", "price": "6,90 €", "category": "Dessert"},
            {"name": "Churros", "description": "Mit Schokolade", "price": "6,90 €", "category": "Dessert"},
            {"name": "Schoko Soufflé", "description": "Eis, Sahne", "price": "7,50 €", "category": "Dessert"},
            {"name": "Kokos-Eis in Fruchtschale", "description": "Erfrischend exotisch", "price": "6,90 €", "category": "Dessert"},
            {"name": "Zitronen-Eis in Fruchtschale", "description": "Frisch und sauer", "price": "6,90 €", "category": "Dessert"},
            {"name": "Orangen-Eis in Fruchtschale", "description": "Fruchtig-süß", "price": "6,90 €", "category": "Dessert"},
            {"name": "Nuss-Eis in Fruchtschale", "description": "Cremig-nussig", "price": "6,90 €", "category": "Dessert"},
        ]
        
        # Menu Items in Datenbank einfügen
        insert_sql = """
            INSERT INTO menu_items (
                id, name, description, price, category, 
                vegan, vegetarian, is_active, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        count = 0
        for item in menu_items:
            await cursor.execute(insert_sql, (
                str(uuid.uuid4()),
                item["name"],
                item["description"], 
                item["price"],
                item["category"],
                item.get("vegan", False),
                item.get("vegetarian", False),
                True,
                datetime.utcnow(),
                datetime.utcnow()
            ))
            count += 1
        
        # Commit changes
        await connection.commit()
        
        print(f"✅ {count} Menu-Items erfolgreich erstellt!")
        print("📋 Kategorien:")
        categories = set(item["category"] for item in menu_items)
        for cat in sorted(categories):
            items_in_cat = len([item for item in menu_items if item["category"] == cat])
            print(f"   - {cat}: {items_in_cat} Gerichte")
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_complete_menu())
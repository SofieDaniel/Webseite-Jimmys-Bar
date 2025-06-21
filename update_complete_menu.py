#!/usr/bin/env python3
"""
Aktualisierung der kompletten Speisekarte für Jimmy's Tapas Bar
Mit Beschreibungen und Allergenliste
"""

import asyncio
import aiomysql
import os
import uuid
import json
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

async def update_complete_menu():
    """Aktualisiert die komplette Speisekarte"""
    print("🍽️  Aktualisiere komplette Speisekarte für Jimmy's Tapas Bar")
    print("=" * 70)
    
    # Connect to MySQL
    connection = await aiomysql.connect(**mysql_config)
    cursor = await connection.cursor()
    
    try:
        # Clear existing menu items
        await cursor.execute("DELETE FROM menu_items")
        print("🗑️  Bestehende Speisekarte gelöscht")
        
        # Vollständige Speisekarte mit Beschreibungen und Allergenen
        menu_items = [
            # 1. Inicio / Vorspeisen
            {"category": "Inicio / Vorspeisen", "name": "Aioli", "price": 3.50, "description": "Traditionelle spanische Knoblauchsauce mit hochwertigem Olivenöl", "allergens": "Gluten, Senf, Sulfite"},
            {"category": "Inicio / Vorspeisen", "name": "Oliven", "price": 3.90, "description": "Marinierte spanische Oliven verschiedener Sorten", "allergens": "Sulfite"},
            {"category": "Inicio / Vorspeisen", "name": "Extra Brot", "price": 1.90, "description": "Frisches spanisches Brot", "allergens": "Gluten"},
            {"category": "Inicio / Vorspeisen", "name": "Hummus", "price": 3.90, "description": "Cremige Kichererbsen-Paste mit Tahini und Gewürzen", "allergens": "Sesam"},
            {"category": "Inicio / Vorspeisen", "name": "Guacamole", "price": 3.90, "description": "Frische Avocado-Creme mit Limette und Koriander", "allergens": "-"},
            {"category": "Inicio / Vorspeisen", "name": "Spanischer Käseteller", "price": 8.90, "description": "Auswahl verschiedener spanischer Käse mit Manchego", "allergens": "Milch"},
            {"category": "Inicio / Vorspeisen", "name": "Schinken-Käse-Wurst Teller", "price": 11.90, "description": "Auswahl spanischer Aufschnitt mit Käse", "allergens": "Milch, Sulfite"},
            {"category": "Inicio / Vorspeisen", "name": "Jamón Serrano Teller", "price": 9.90, "description": "18 Monate gereifter spanischer Bergschinken", "allergens": "Sulfite"},
            {"category": "Inicio / Vorspeisen", "name": "Boquerones en Vinagre", "price": 8.90, "description": "Eingelegte Sardellen in Essig und Olivenöl", "allergens": "Fisch, Sulfite"},
            {"category": "Inicio / Vorspeisen", "name": "Pata Negra", "price": 8.90, "description": "Premium iberischer Schinken von Eichelmast-Schweinen", "allergens": "Sulfite"},
            {"category": "Inicio / Vorspeisen", "name": "Tres", "price": 10.90, "description": "Dreierlei: Hummus, Guacamole und Aioli mit frischem Brot", "allergens": "Gluten, Sesam, Senf, Sulfite"},
            
            # 2. Salate
            {"category": "Salate", "name": "Ensalada Mixta", "price": 8.90, "description": "Bunter Salat mit Tomaten, Gurken, Zwiebeln in Essig-Öl-Dressing", "allergens": "Sulfite"},
            {"category": "Salate", "name": "Ensalada Tonno", "price": 14.90, "description": "Gemischter Salat mit hochwertigem Thunfisch", "allergens": "Fisch, Sulfite"},
            {"category": "Salate", "name": "Ensalada Pollo", "price": 14.90, "description": "Bunter Salat mit gegrillten Hähnchenstreifen", "allergens": "Sulfite"},
            {"category": "Salate", "name": "Ensalada Garnelen", "price": 15.90, "description": "Frischer Salat mit saftigen Garnelen", "allergens": "Krebstiere, Sulfite"},
            {"category": "Salate", "name": "Kleiner Salat", "price": 6.90, "description": "Tomaten und Gurken mit Zwiebeln", "allergens": "Sulfite"},
            {"category": "Salate", "name": "Rote Beete Salat mit Ziegenkäse", "price": 7.90, "description": "Geröstete rote Beete mit cremigem Ziegenkäse", "allergens": "Milch, Sulfite"},
            {"category": "Salate", "name": "Kichererbsen Salat mit Feta", "price": 7.90, "description": "Mediterrane Kichererbsen mit griechischem Feta", "allergens": "Milch, Sulfite"},
            
            # 3. Tapa Paella
            {"category": "Tapa Paella", "name": "Paella", "price": 8.90, "description": "Traditionelle Paella mit Hähnchen und frischen Meeresfrüchten", "allergens": "Krebstiere, Weichtiere, Sulfite"},
            {"category": "Tapa Paella", "name": "Paella Vegetarisch", "price": 7.90, "description": "Vegetarische Paella mit Gemüse der Saison", "allergens": "Sulfite"},
            
            # 4. Tapas Vegetarian
            {"category": "Tapas Vegetarian", "name": "Gebratenes Gemüse der Saison", "price": 6.90, "description": "Saisonales Gemüse schonend in Olivenöl gebraten - Vegan", "allergens": "-"},
            {"category": "Tapas Vegetarian", "name": "Papas Bravas", "price": 6.90, "description": "Knusprige Kartoffeln mit pikanter Bravas-Sauce - Vegan", "allergens": "Sulfite"},
            {"category": "Tapas Vegetarian", "name": "Tortilla de Patata con Aioli", "price": 6.90, "description": "Traditionelles spanisches Kartoffel-Omelett mit Aioli", "allergens": "Eier, Gluten, Senf, Sulfite"},
            {"category": "Tapas Vegetarian", "name": "Pimientos de Padrón", "price": 6.90, "description": "Kleine grüne Paprika mit grobem Meersalz - Vegan", "allergens": "-"},
            {"category": "Tapas Vegetarian", "name": "Kanarische Kartoffeln im Salzmantel", "price": 6.90, "description": "Papas Arrugadas mit Mojo-Sauce - Vegan", "allergens": "-"},
            {"category": "Tapas Vegetarian", "name": "Fetakäse Häppchen", "price": 6.90, "description": "Griechischer Feta in knuspriger Panade", "allergens": "Milch, Gluten, Eier"},
            {"category": "Tapas Vegetarian", "name": "Rosmarin Ziegenkäse", "price": 6.90, "description": "Cremiger Ziegenkäse mit frischem Rosmarin", "allergens": "Milch"},
            {"category": "Tapas Vegetarian", "name": "Falafel", "price": 6.90, "description": "Hausgemachte Kichererbsen-Bällchen mit Tahini", "allergens": "Sesam, Gluten"},
            {"category": "Tapas Vegetarian", "name": "Feta Käse überbacken Cherry", "price": 6.90, "description": "Überbackener Feta mit Cherry-Tomaten", "allergens": "Milch"},
            {"category": "Tapas Vegetarian", "name": "Überbackene Champignons", "price": 6.90, "description": "Frische Champignons mit Kräuter-Käse-Kruste", "allergens": "Milch, Gluten"},
            {"category": "Tapas Vegetarian", "name": "Überbackene Tomaten", "price": 6.90, "description": "Ofentomaten mit mediteraner Käse-Kräuter-Kruste", "allergens": "Milch, Gluten"},
            {"category": "Tapas Vegetarian", "name": "Frittierte Auberginen mit Honig", "price": 6.90, "description": "Knusprige Auberginen-Scheiben mit spanischem Honig", "allergens": "Gluten"},
            {"category": "Tapas Vegetarian", "name": "Champignons al Ajillo", "price": 6.90, "description": "Champignons in Knoblauch und Olivenöl - Vegan", "allergens": "-"},
            {"category": "Tapas Vegetarian", "name": "Teigröllchen mit Spinat", "price": 6.90, "description": "Knusprige Röllchen gefüllt mit Spinat und Kräutern", "allergens": "Gluten, Eier"},
            {"category": "Tapas Vegetarian", "name": "Feta Feigen", "price": 6.90, "description": "Süße Feigen mit salzigem Feta-Käse", "allergens": "Milch"},
            {"category": "Tapas Vegetarian", "name": "Ziegenkäse überbacken", "price": 6.90, "description": "Warmer Ziegenkäse mit Honig und Nüssen", "allergens": "Milch, Nüsse"},
            {"category": "Tapas Vegetarian", "name": "Gebratener Spinat mit Cherry Tomaten", "price": 6.90, "description": "Frischer Spinat mit Kirschtomaten - Vegan", "allergens": "-"},
            
            # 5. Tapas de Pollo
            {"category": "Tapas de Pollo", "name": "Hähnchen Filet mit Limetten Sauce", "price": 7.20, "description": "Zartes Hähnchenfilet mit frischer Limetten-Kräuter-Sauce", "allergens": "Sulfite"},
            {"category": "Tapas de Pollo", "name": "Knusprige Hähnchen Tapas mit Honig-Senf Sauce", "price": 7.20, "description": "Panierte Hähnchen-Stücke mit süß-scharfer Sauce", "allergens": "Gluten, Eier, Senf"},
            {"category": "Tapas de Pollo", "name": "Hähnchen Spieß mit scharfer Sauce", "price": 7.20, "description": "Gegrillter Hähnchen-Spieß mit pikanter Chili-Sauce", "allergens": "Sulfite"},
            {"category": "Tapas de Pollo", "name": "Hähnchen Filet mit Curry Sauce", "price": 7.20, "description": "Gebratenes Hähnchenfilet in cremiger Curry-Sauce", "allergens": "Milch, Sulfite"},
            {"category": "Tapas de Pollo", "name": "Hähnchen Filet mit Mandel Sauce", "price": 7.20, "description": "Hähnchenfilet in traditioneller spanischer Mandel-Sauce", "allergens": "Nüsse, Sulfite"},
            {"category": "Tapas de Pollo", "name": "Gegrillter Hähnchen-Chorizo-Spieß", "price": 7.20, "description": "Spanischer Hähnchen-Chorizo-Spieß vom Grill", "allergens": "Sulfite"},
            {"category": "Tapas de Pollo", "name": "Hähnchen Filet mit Brandy Sauce", "price": 7.20, "description": "Hähnchenfilet in edler Brandy-Sahne-Sauce", "allergens": "Milch, Sulfite"},
        ]
        
        # Fortsetzung der Menu-Items...
        menu_items_part2 = [
            # 6. Tapas de Carne
            {"category": "Tapas de Carne", "name": "Dátiles con Bacon", "price": 6.90, "description": "Süße Datteln umhüllt von knusprigem Speck", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Albondigas a la Casera", "price": 6.90, "description": "Hausgemachte Hackbällchen in aromatischer Tomatensauce", "allergens": "Gluten, Eier, Sulfite"},
            {"category": "Tapas de Carne", "name": "Pincho de Cerdo", "price": 7.90, "description": "Scharfer Schweinespieß mit spanischen Gewürzen", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Pincho de Cordero", "price": 8.90, "description": "Würziger Lammspieß mit mediterranen Kräutern", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Chuletas de Cordero", "price": 9.90, "description": "Zwei zarte Lammkoteletts perfekt gegrillt", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Rollitos de Serrano con Higo", "price": 9.90, "description": "Serrano-Schinken-Röllchen mit Feigen und Frischkäse", "allergens": "Milch, Sulfite"},
            {"category": "Tapas de Carne", "name": "Queso de Cabra con Bacon", "price": 7.90, "description": "Warmer Ziegenkäse umhüllt von knusprigem Speck", "allergens": "Milch, Sulfite"},
            {"category": "Tapas de Carne", "name": "Chorizo al Diablo", "price": 7.90, "description": "Pikante Chorizo geschmort in Rotweinsauce", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Medallions de Carne", "price": 9.90, "description": "Rinderfilet-Medaillons mit cremigem Pilz-Ragout", "allergens": "Milch, Sulfite"},
            {"category": "Tapas de Carne", "name": "Mit Käse gefüllte Champignons", "price": 8.90, "description": "Große Champignons gefüllt mit Käse, Bacon und Kräutern", "allergens": "Milch, Gluten, Sulfite"},
            {"category": "Tapas de Carne", "name": "Schweinefilet mit Cherry Tomaten", "price": 9.50, "description": "Zartes Schweinefilet mit Mango-Honig-Glasur", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Schweinefilet", "price": 9.50, "description": "Schweinefilet mit Spinat, Pilzen und Crème fraîche", "allergens": "Milch, Sulfite"},
            {"category": "Tapas de Carne", "name": "Chorizo a la Plancha", "price": 7.90, "description": "Gegrillte spanische Chorizo-Scheiben", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Lammfilet", "price": 9.90, "description": "Zartes Lammfilet mit aromatischer Pfeffersauce", "allergens": "Sulfite"},
            {"category": "Tapas de Carne", "name": "Spareribs mit BBQ-Sauce", "price": 9.90, "description": "Saftige Spareribs mit hausgemachter BBQ-Sauce", "allergens": "Sulfite, Senf"},
            {"category": "Tapas de Carne", "name": "Chicken Wings", "price": 9.90, "description": "Knusprige Hähnchen-Flügel mit süßer Chili-Sauce", "allergens": "Sulfite"},
            
            # 7. Tapas de Pescado
            {"category": "Tapas de Pescado", "name": "Boquerones Fritos", "price": 7.50, "description": "Frittierte Sardellen nach andalusischer Art", "allergens": "Fisch, Gluten"},
            {"category": "Tapas de Pescado", "name": "Calamares a la Plancha", "price": 8.90, "description": "Gegrillte Calamari mit Knoblauch und Petersilie", "allergens": "Weichtiere"},
            {"category": "Tapas de Pescado", "name": "Calamares a la Romana", "price": 7.50, "description": "Frittierte Tintenfisch-Ringe mit Aioli", "allergens": "Weichtiere, Gluten, Eier, Senf, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Salmon con Espinaca", "price": 9.90, "description": "Lachsfilet auf Spinat-Bett mit Sahnesauce", "allergens": "Fisch, Milch, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Gambas a la Plancha", "price": 9.90, "description": "Gegrillte Tiger-Garnelen mit saisonalem Gemüse", "allergens": "Krebstiere"},
            {"category": "Tapas de Pescado", "name": "Garnelen-Dattel-Spieß", "price": 9.90, "description": "Garnelen und Datteln im Speckmantel mit Honig-Senf", "allergens": "Krebstiere, Senf, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Gambas al Ajillo", "price": 9.90, "description": "Klassische Knoblauch-Garnelen in Olivenöl", "allergens": "Krebstiere"},
            {"category": "Tapas de Pescado", "name": "Muslitos de Mar", "price": 6.90, "description": "Krebsfleisch-Bällchen in knuspriger Panade", "allergens": "Krebstiere, Gluten, Eier"},
            {"category": "Tapas de Pescado", "name": "Gegrillter Oktopus", "price": 9.90, "description": "Oktopus mit Kichererbsen und mediteranem Gemüse", "allergens": "Weichtiere"},
            {"category": "Tapas de Pescado", "name": "Jacobsmuscheln", "price": 9.90, "description": "Jakobsmuscheln mit Spinat und Cherry-Tomaten", "allergens": "Weichtiere, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Gambas PIL PIL", "price": 9.90, "description": "Garnelen in scharfer Tomatensauce", "allergens": "Krebstiere, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Empanadas", "price": 6.90, "description": "Gefüllte Teigtaschen mit Thunfisch", "allergens": "Fisch, Gluten, Eier"},
            {"category": "Tapas de Pescado", "name": "Pfahlmuscheln", "price": 8.90, "description": "Miesmuscheln nach spanischer Art zubereitet", "allergens": "Weichtiere, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Pulpo al Ajillo", "price": 9.90, "description": "Oktopus mit Knoblauch und spanischen Gewürzen", "allergens": "Weichtiere"},
            {"category": "Tapas de Pescado", "name": "Zander Filet", "price": 9.90, "description": "Zanderfilet mit Bacon in Knoblauch-Sahnesauce", "allergens": "Fisch, Milch, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Tiger Garnelen", "price": 9.90, "description": "Tiger-Garnelen mit Tomaten, Paprika und Oliven", "allergens": "Krebstiere, Sulfite"},
            {"category": "Tapas de Pescado", "name": "Brocheta de Gambas", "price": 8.90, "description": "Garnelen-Spieß gegrillt mit mediterranen Kräutern", "allergens": "Krebstiere"},
            {"category": "Tapas de Pescado", "name": "Boqueron en Tempura", "price": 7.50, "description": "Panierte Sardellen in Tempura-Teig", "allergens": "Fisch, Gluten, Eier"},
            {"category": "Tapas de Pescado", "name": "Chipirones Fritos con Aioli", "price": 8.90, "description": "Frittierte Baby-Calamari mit hausgemachtem Aioli", "allergens": "Weichtiere, Gluten, Eier, Senf, Sulfite"},
            
            # 8. Kroketten
            {"category": "Kroketten", "name": "Croquetas de Bacalao", "price": 5.90, "description": "Traditionelle Stockfisch-Kroketten", "allergens": "Fisch, Gluten, Milch, Eier"},
            {"category": "Kroketten", "name": "Croquetas de Queso", "price": 5.90, "description": "Cremige Käse-Kroketten", "allergens": "Milch, Gluten, Eier"},
            {"category": "Kroketten", "name": "Croquetas de Almendras", "price": 6.50, "description": "Mandel-Kroketten mit feinem Mandelaroma", "allergens": "Nüsse, Gluten, Milch, Eier"},
            {"category": "Kroketten", "name": "Croquetas de Jamón", "price": 5.90, "description": "Klassische Serrano-Schinken-Kroketten", "allergens": "Gluten, Milch, Eier, Sulfite"},
            {"category": "Kroketten", "name": "Croquetas de Patata", "price": 5.50, "description": "Kartoffel-Kroketten mit spanischen Gewürzen", "allergens": "Gluten, Milch, Eier"},
        ]
        
        # Füge alle Menu-Items ein
        all_items = menu_items + menu_items_part2
        
        for item in all_items:
            item_id = str(uuid.uuid4())
            await cursor.execute("""
                INSERT INTO menu_items (id, category, name, price, description, allergens, is_available, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item_id, 
                item["category"], 
                item["name"], 
                item["price"], 
                item["description"], 
                item["allergens"], 
                True, 
                datetime.now()
            ))
        
        print(f"✅ {len(all_items)} Speisen erfolgreich eingefügt!")
        print("   📋 Kategorien: Vorspeisen, Salate, Paella, Vegetarisch, Hähnchen, Fleisch, Fisch, Kroketten")
        print("   📝 Alle Gerichte haben Beschreibungen und Allergen-Listen")
        
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren der Speisekarte: {e}")
        raise
    finally:
        await cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(update_complete_menu())
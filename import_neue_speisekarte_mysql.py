#!/usr/bin/env python3
import pymysql
import uuid
import os
from decimal import Decimal

# MySQL Verbindung
def get_mysql_connection():
    return pymysql.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'jimmy_user'),
        password=os.environ.get('MYSQL_PASSWORD', 'jimmy2024'),
        database=os.environ.get('MYSQL_DATABASE', 'jimmys_tapasbar'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def clear_existing_menu():
    """Löscht alle existierenden Menü-Artikel"""
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu_items")
        conn.commit()
        print("✅ Alle existierenden Menü-Artikel gelöscht")
    except Exception as e:
        print(f"❌ Fehler beim Löschen: {e}")
    finally:
        conn.close()

def import_complete_menu():
    """Importiert die komplette aktuelle Speisekarte"""
    
    # Komplette Speisekarte mit allen Positionen
    menu_items = [
        # Vorspeisen / Inicio
        {"name": "Aioli", "description": "Knoblauchsauce mit Öl", "price": 3.50, "category": "Vorspeisen / Inicio", "allergens": "Eier", "origin": "Spanien"},
        {"name": "Oliven", "description": "Spanische Oliven", "price": 3.90, "category": "Vorspeisen / Inicio", "allergens": "", "origin": "Spanien"},
        {"name": "Extra Brot", "description": "Frisches Brot", "price": 1.90, "category": "Vorspeisen / Inicio", "allergens": "Gluten", "origin": "Spanien"},
        {"name": "Hummus", "description": "Kichererbsen Cream", "price": 3.90, "category": "Vorspeisen / Inicio", "allergens": "Sesam", "origin": "Spanien"},
        {"name": "Guacamole", "description": "Avocado Cream", "price": 3.90, "category": "Vorspeisen / Inicio", "allergens": "", "origin": "Mexiko"},
        {"name": "Spanischer Käseteller", "description": "Manchego", "price": 8.90, "category": "Vorspeisen / Inicio", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Schinken-Käse-Wurst Teller", "description": "Auswahl an Wurst und Käse", "price": 11.90, "category": "Vorspeisen / Inicio", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Jamón Serrano Teller", "description": "Spanischer Serrano Schinken", "price": 9.90, "category": "Vorspeisen / Inicio", "allergens": "", "origin": "Spanien"},
        {"name": "Boquerones en Vinagre", "description": "mit Essig und Öl", "price": 8.90, "category": "Vorspeisen / Inicio", "allergens": "Fisch", "origin": "Spanien"},
        {"name": "Pata Negra", "description": "spanischer Ibérico Schinken", "price": 8.90, "category": "Vorspeisen / Inicio", "allergens": "", "origin": "Spanien"},
        {"name": "Tres", "description": "Hummus, Avocado Cream, Aioli mit Brot", "price": 10.90, "category": "Vorspeisen / Inicio", "allergens": "Gluten, Sesam, Eier", "origin": "Spanien"},

        # Salate
        {"name": "Ensalada Mixta", "description": "Bunter Salat mit Essig und Öl", "price": 8.90, "category": "Salate", "allergens": "", "origin": "Spanien"},
        {"name": "Ensalada Tonno", "description": "Bunter Salat mit Thunfisch", "price": 14.90, "category": "Salate", "allergens": "Fisch", "origin": "Spanien"},
        {"name": "Ensalada Pollo", "description": "Bunter Salat mit Hähnchenstreifen", "price": 14.90, "category": "Salate", "allergens": "", "origin": "Spanien"},
        {"name": "Ensalada Garnelen", "description": "Bunter Salat mit Garnelen", "price": 15.90, "category": "Salate", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Tomaten/Gurken Salat", "description": "mit Zwiebeln", "price": 6.90, "category": "Salate", "allergens": "", "origin": "Deutschland"},
        {"name": "Rote Beete Salat", "description": "mit Ziegenkäse", "price": 7.90, "category": "Salate", "allergens": "Milch", "origin": "Deutschland"},
        {"name": "Kichererbsen Salat", "description": "mit Feta", "price": 7.90, "category": "Salate", "allergens": "Milch", "origin": "Griechenland"},

        # Tapa Paella
        {"name": "Paella", "description": "mit Hähnchen und Meeresfrüchten", "price": 8.90, "category": "Tapa Paella", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Paella Vegetarisch", "description": "Vegetarische Paella", "price": 7.90, "category": "Tapa Paella", "allergens": "", "origin": "Spanien"},

        # Tapas Vegetarian
        {"name": "Gebratenes Gemüse der Saison", "description": "Vegan", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "", "origin": "Spanien"},
        {"name": "Papas Bravas", "description": "Vegan", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "", "origin": "Spanien"},
        {"name": "Tortilla de Patata", "description": "con Aioli", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Eier", "origin": "Spanien"},
        {"name": "Pimientos de Padrón", "description": "Vegan", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "", "origin": "Spanien"},
        {"name": "Kanarische Kartoffeln", "description": "im Salzmantel / Vegan", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "", "origin": "Spanien"},
        {"name": "Fetakäse Häppchen", "description": "Griechischer Feta", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Milch", "origin": "Griechenland"},
        {"name": "Rosmarin Ziegenkäse", "description": "Mit frischem Rosmarin", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Falafel", "description": "Orientalische Kichererbsenbällchen", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Sesam", "origin": "Orient"},
        {"name": "Feta Käse überbacken", "description": "Cherry", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Milch", "origin": "Griechenland"},
        {"name": "Überbackene Champignons", "description": "Mit Käse gratiniert", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Milch", "origin": "Deutschland"},
        {"name": "Überbackene Tomaten", "description": "Mit Käse", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Frittierte Auberginen", "description": "mit Honig", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "", "origin": "Spanien"},
        {"name": "Champignons al Ajillo", "description": "Vegan", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "", "origin": "Spanien"},
        {"name": "Teigröllchen mit Spinat", "description": "Gefüllte Teigtaschen", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Gluten", "origin": "Spanien"},
        {"name": "Feta Feigen", "description": "Süße Feigen mit Feta", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Milch", "origin": "Griechenland"},
        {"name": "Ziegenkäse überbacken", "description": "Gratinierter Ziegenkäse", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Gebratener Spinat", "description": "mit Cherry Tomaten / Vegan", "price": 6.90, "category": "Tapas Vegetarian", "allergens": "", "origin": "Spanien"},

        # Tapas de Pollo
        {"name": "Hähnchen Filet", "description": "mit Limetten Sauce", "price": 7.20, "category": "Tapas de Pollo", "allergens": "", "origin": "Deutschland"},
        {"name": "Knusprige Hähnchen Tapas", "description": "mit Honig-Senf Sauce", "price": 7.20, "category": "Tapas de Pollo", "allergens": "Senf", "origin": "Deutschland"},
        {"name": "Hähnchen Spieß", "description": "mit scharfer Sauce", "price": 7.20, "category": "Tapas de Pollo", "allergens": "", "origin": "Spanien"},
        {"name": "Hähnchen Filet Curry", "description": "mit Curry Sauce", "price": 7.20, "category": "Tapas de Pollo", "allergens": "", "origin": "Indien"},
        {"name": "Hähnchen Filet Mandel", "description": "mit Mandel Sauce", "price": 7.20, "category": "Tapas de Pollo", "allergens": "Nüsse", "origin": "Spanien"},
        {"name": "Hähnchen-Chorizo-Spieß", "description": "Gegrillt", "price": 7.20, "category": "Tapas de Pollo", "allergens": "", "origin": "Spanien"},
        {"name": "Hähnchen Filet Brandy", "description": "mit Brandy Sauce", "price": 7.20, "category": "Tapas de Pollo", "allergens": "", "origin": "Spanien"},

        # Tapas de Carne
        {"name": "Dátiles con Bacon", "description": "Datteln im Speckmantel", "price": 6.90, "category": "Tapas de Carne", "allergens": "", "origin": "Spanien"},
        {"name": "Albondigas a la Casera", "description": "Hackbällchen mit Tomatensauce", "price": 6.90, "category": "Tapas de Carne", "allergens": "", "origin": "Spanien"},
        {"name": "Pincho de Cerdo", "description": "Schweinespieß scharf", "price": 7.90, "category": "Tapas de Carne", "allergens": "", "origin": "Spanien"},
        {"name": "Pincho de Cordero", "description": "Lammspieß scharf", "price": 8.90, "category": "Tapas de Carne", "allergens": "", "origin": "Spanien"},
        {"name": "Chuletas de Cordero", "description": "2 Lammkoteletts", "price": 9.90, "category": "Tapas de Carne", "allergens": "", "origin": "Spanien"},
        {"name": "Rollitos de Serrano", "description": "Feigen/Serrano, Frischkäse", "price": 9.90, "category": "Tapas de Carne", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Queso de Cabra con Bacon", "description": "Ziegenkäse/Speck", "price": 7.90, "category": "Tapas de Carne", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Chorizo al Diablo", "description": "in Rotweinsauce", "price": 7.90, "category": "Tapas de Carne", "allergens": "", "origin": "Spanien"},
        {"name": "Medallions de Carne", "description": "Rinderfilet, Pilz-Ragout", "price": 9.90, "category": "Tapas de Carne", "allergens": "", "origin": "Deutschland"},
        {"name": "Champignons mit Käse", "description": "Bacon, Kräuter", "price": 8.90, "category": "Tapas de Carne", "allergens": "Milch", "origin": "Deutschland"},
        {"name": "Schweinefilet Cherry", "description": "mit Cherry Tomaten, Mango-Honig", "price": 9.50, "category": "Tapas de Carne", "allergens": "", "origin": "Deutschland"},
        {"name": "Schweinefilet Spinat", "description": "Spinat, Pilze, Cremefraiche", "price": 9.50, "category": "Tapas de Carne", "allergens": "Milch", "origin": "Deutschland"},
        {"name": "Chorizo a la Plancha", "description": "gegrillt", "price": 7.90, "category": "Tapas de Carne", "allergens": "", "origin": "Spanien"},
        {"name": "Lammfilet", "description": "mit Pfeffersauce", "price": 9.90, "category": "Tapas de Carne", "allergens": "", "origin": "Deutschland"},
        {"name": "Spareribs", "description": "mit BBQ-Sauce", "price": 9.90, "category": "Tapas de Carne", "allergens": "", "origin": "USA"},
        {"name": "Chicken Wings", "description": "mit süßer Chillisauce", "price": 9.90, "category": "Tapas de Carne", "allergens": "", "origin": "USA"},

        # Tapas de Pescado
        {"name": "Boquerones Fritos", "description": "frittierte Sardellen", "price": 7.50, "category": "Tapas de Pescado", "allergens": "Fisch", "origin": "Spanien"},
        {"name": "Calamares a la Plancha", "description": "gegrillt", "price": 8.90, "category": "Tapas de Pescado", "allergens": "Weichtiere", "origin": "Spanien"},
        {"name": "Calamares a la Romana", "description": "frittiert mit Aioli", "price": 7.50, "category": "Tapas de Pescado", "allergens": "Weichtiere", "origin": "Spanien"},
        {"name": "Salmon con Espinaca", "description": "Lachsfilet auf Spinat", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Fisch", "origin": "Norwegen"},
        {"name": "Gambas a la Plancha", "description": "gegrillte Tiger-Garnelen, Gemüse", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Garnelen-Dattel-Spieß", "description": "Speckmantel, Honig-Senf", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Gambas al Ajillo", "description": "Knoblauch-Olivenöl", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Muslitos de Mar", "description": "Krebsfleischbällchen", "price": 6.90, "category": "Tapas de Pescado", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Gegrillter Oktopus", "description": "Kichererbsen, Gemüse", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Weichtiere", "origin": "Spanien"},
        {"name": "Jacobsmuscheln", "description": "Spinat, Cherry Tomaten", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Weichtiere", "origin": "Frankreich"},
        {"name": "Gambas PIL PIL", "description": "scharfe Tomatensauce", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Empanadas", "description": "Thunfisch, gefüllter Teig", "price": 6.90, "category": "Tapas de Pescado", "allergens": "Fisch, Gluten", "origin": "Spanien"},
        {"name": "Pfahlmuscheln", "description": "nach spanischer Art", "price": 8.90, "category": "Tapas de Pescado", "allergens": "Weichtiere", "origin": "Spanien"},
        {"name": "Pulpo al Ajillo", "description": "Oktopus, Knoblauch", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Weichtiere", "origin": "Spanien"},
        {"name": "Zander Filet", "description": "Bacon, Knoblauch-Sahnesauce", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Fisch, Milch", "origin": "Deutschland"},
        {"name": "Tiger Garnelen", "description": "Tomaten, Paprika, Knoblauch, Oliven", "price": 9.90, "category": "Tapas de Pescado", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Brocheta de Gambas", "description": "Gambas Spieß", "price": 8.90, "category": "Tapas de Pescado", "allergens": "Krebstiere", "origin": "Spanien"},
        {"name": "Boqueron en Tempura", "description": "Panierte Sardellen", "price": 7.50, "category": "Tapas de Pescado", "allergens": "Fisch, Gluten", "origin": "Japan/Spanien"},
        {"name": "Chipirones Fritos", "description": "con Aioli", "price": 8.90, "category": "Tapas de Pescado", "allergens": "Weichtiere", "origin": "Spanien"},

        # Kroketten
        {"name": "Croquetas de Bacalao", "description": "Stockfisch", "price": 5.90, "category": "Kroketten", "allergens": "Fisch, Gluten", "origin": "Spanien"},
        {"name": "Croquetas de Queso", "description": "Fetakäse", "price": 5.90, "category": "Kroketten", "allergens": "Milch, Gluten", "origin": "Spanien"},
        {"name": "Croquetas de Almendras", "description": "Mandeln", "price": 6.50, "category": "Kroketten", "allergens": "Nüsse, Gluten", "origin": "Spanien"},
        {"name": "Croquetas de Jamón", "description": "Serrano Schinken", "price": 5.90, "category": "Kroketten", "allergens": "Gluten", "origin": "Spanien"},
        {"name": "Croquetas de Patata", "description": "Kartoffel", "price": 5.50, "category": "Kroketten", "allergens": "Gluten", "origin": "Spanien"},

        # Pasta
        {"name": "Spaghetti Aglio e Olio", "description": "Knoblauch und Olivenöl", "price": 12.90, "category": "Pasta", "allergens": "Gluten", "origin": "Italien"},
        {"name": "Spaghetti Bolognese", "description": "Mit Fleischsauce", "price": 14.90, "category": "Pasta", "allergens": "Gluten", "origin": "Italien"},
        {"name": "Pasta Brokkoli Gorgonzola", "description": "Mit Brokkoli und Gorgonzola", "price": 14.90, "category": "Pasta", "allergens": "Gluten, Milch", "origin": "Italien"},
        {"name": "Pasta Verdura", "description": "Mit Gemüse", "price": 14.90, "category": "Pasta", "allergens": "Gluten", "origin": "Italien"},
        {"name": "Pasta Garnelen", "description": "Mit Garnelen", "price": 16.90, "category": "Pasta", "allergens": "Gluten, Krebstiere", "origin": "Italien"},

        # Pizza
        {"name": "Pizza Margharita", "description": "Tomaten, Mozzarella, Basilikum", "price": 9.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Italien"},
        {"name": "Pizza Schinken", "description": "Mit Schinken", "price": 12.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Italien"},
        {"name": "Pizza Funghi", "description": "Mit Champignons", "price": 12.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Italien"},
        {"name": "Pizza Tonno", "description": "Mit Thunfisch", "price": 13.90, "category": "Pizza", "allergens": "Gluten, Milch, Fisch", "origin": "Italien"},
        {"name": "Pizza Hawaii", "description": "Mit Schinken und Ananas", "price": 13.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Deutschland"},
        {"name": "Pizza Verdura", "description": "Mit Gemüse", "price": 13.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Italien"},
        {"name": "Pizza Salami", "description": "Mit Salami", "price": 12.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Italien"},
        {"name": "Pizza Garnelen", "description": "Mit Garnelen", "price": 15.90, "category": "Pizza", "allergens": "Gluten, Milch, Krebstiere", "origin": "Italien"},
        {"name": "Pizza Bolognese", "description": "Mit Fleischsauce", "price": 13.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Italien"},
        {"name": "Jimmy's Special Pizza", "description": "Spezialrezept des Hauses", "price": 13.90, "category": "Pizza", "allergens": "Gluten, Milch", "origin": "Spanien"},

        # Für den kleinen und großen Hunger
        {"name": "Pommes Frites", "description": "mit Ketchup/Mayonnaise", "price": 5.50, "category": "Für den kleinen und großen Hunger", "allergens": "", "origin": "Belgien"},
        {"name": "Chicken Nuggets", "description": "5 Stück, Pommes", "price": 8.90, "category": "Für den kleinen und großen Hunger", "allergens": "Gluten", "origin": "USA"},
        {"name": "Chicken Wings", "description": "5 Stück, Pommes", "price": 9.90, "category": "Für den kleinen und großen Hunger", "allergens": "", "origin": "USA"},
        {"name": "Currywurst", "description": "mit Pommes", "price": 10.90, "category": "Für den kleinen und großen Hunger", "allergens": "Gluten", "origin": "Deutschland"},

        # Dessert & Eis
        {"name": "Crema Catalana", "description": "Spanische Creme", "price": 5.50, "category": "Dessert & Eis", "allergens": "Milch, Eier", "origin": "Spanien"},
        {"name": "Tarte de Santiago", "description": "Mandelkuchen", "price": 7.50, "category": "Dessert & Eis", "allergens": "Nüsse, Gluten, Eier", "origin": "Spanien"},
        {"name": "Gemischtes Eis", "description": "3 Kugeln, Sahne", "price": 6.90, "category": "Dessert & Eis", "allergens": "Milch", "origin": "Italien"},
        {"name": "Churros", "description": "mit Schokolade", "price": 6.90, "category": "Dessert & Eis", "allergens": "Gluten, Milch", "origin": "Spanien"},
        {"name": "Schoko Soufflé", "description": "Eis, Sahne", "price": 7.50, "category": "Dessert & Eis", "allergens": "Milch, Eier", "origin": "Frankreich"},
        {"name": "Kokos-Eis", "description": "in Fruchtschale", "price": 6.90, "category": "Dessert & Eis", "allergens": "Milch", "origin": "Tropen"},
        {"name": "Zitronen-Eis", "description": "in Fruchtschale", "price": 6.90, "category": "Dessert & Eis", "allergens": "Milch", "origin": "Italien"},
        {"name": "Orangen-Eis", "description": "in Fruchtschale", "price": 6.90, "category": "Dessert & Eis", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Nuss-Eis", "description": "in Fruchtschale", "price": 6.90, "category": "Dessert & Eis", "allergens": "Milch, Nüsse", "origin": "Italien"},

        # Heißgetränke & Tee
        {"name": "Café Crema", "description": "Aromatischer Kaffee", "price": 3.60, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Kolumbien"},
        {"name": "Cappuccino", "description": "Espresso mit Milchschaum", "price": 3.60, "category": "Heißgetränke & Tee", "allergens": "Milch", "origin": "Italien"},
        {"name": "Milchkaffee", "description": "Kaffee mit viel Milch", "price": 3.90, "category": "Heißgetränke & Tee", "allergens": "Milch", "origin": "Frankreich"},
        {"name": "Latte Macchiato", "description": "Geschichteter Kaffee", "price": 3.90, "category": "Heißgetränke & Tee", "allergens": "Milch", "origin": "Italien"},
        {"name": "Espresso", "description": "Starker italienischer Kaffee", "price": 2.80, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Italien"},
        {"name": "Espresso doppio", "description": "Doppelter Espresso", "price": 3.90, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Italien"},
        {"name": "Café Cortado", "description": "Espresso mit wenig Milch", "price": 3.90, "category": "Heißgetränke & Tee", "allergens": "Milch", "origin": "Spanien"},
        {"name": "Heiße Schokolade", "description": "mit Sahne", "price": 3.90, "category": "Heißgetränke & Tee", "allergens": "Milch", "origin": "Mexiko"},
        {"name": "Minz Tee", "description": "mit Ingwer und Honig", "price": 3.90, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Marokko"},
        {"name": "Ingwer Orangen Tee", "description": "mit Honig", "price": 3.90, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Asien"},
        {"name": "Schwarzer Tee", "description": "im Beutel", "price": 3.20, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Ceylon"},
        {"name": "Grüner Tee", "description": "im Beutel", "price": 3.20, "category": "Heißgetränke & Tee", "allergens": "", "origin": "China"},
        {"name": "Früchte Tee", "description": "im Beutel", "price": 3.20, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Deutschland"},
        {"name": "Kamillen Tee", "description": "im Beutel", "price": 3.20, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Deutschland"},
        {"name": "Rooibos Tee", "description": "im Beutel", "price": 3.20, "category": "Heißgetränke & Tee", "allergens": "", "origin": "Südafrika"},
    ]
    
    # Füge die Getränke hinzu (Fortsetzung der Liste)
    drinks = [
        # Softdrinks, Wasser & Limonaden
        {"name": "Coca Cola", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Coca Cola", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Coca Cola Zero", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Coca Cola Zero", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Spezi", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Spezi", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Fanta", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Fanta", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Sprite", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Sprite", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "USA"},
        {"name": "Milch", "description": "Frische Vollmilch", "price": 1.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "Milch", "origin": "Deutschland"},
        {"name": "Tonic Water", "description": "Bitter-süß", "price": 3.80, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "England"},
        {"name": "Ginger Ale", "description": "Ingwer-Limonade", "price": 3.80, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Irland"},
        {"name": "Bitter Lemon", "description": "Zitronen-Bitter", "price": 3.80, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "England"},
        {"name": "Wasser Magnus", "description": "Kohlensäure 0,25 l", "price": 2.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Wasser Magnus", "description": "Kohlensäure 0,75 l", "price": 5.80, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Wasser Magnus still", "description": "0,25 l", "price": 2.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Wasser Magnus still", "description": "0,75 l", "price": 5.80, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Minz-Zitrone", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Minz-Zitrone", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Ingwer-Orange", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Ingwer-Orange", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Wasser-Melone", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Wasser-Melone", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Gurken-Minze", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Limonade Gurken-Minze", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Deutschland"},
        {"name": "Jimmy's Passion Limonade", "description": "0,3 l", "price": 3.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Spanien"},
        {"name": "Jimmy's Passion Limonade", "description": "0,5 l", "price": 5.90, "category": "Softdrinks, Wasser & Limonaden", "allergens": "", "origin": "Spanien"},

        # Säfte/Nektar/Schorle
        {"name": "Apfelsaft", "description": "0,3 l", "price": 3.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Apfelsaft", "description": "0,5 l", "price": 5.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Rhabarbersaft", "description": "0,3 l", "price": 3.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Rhabarbersaft", "description": "0,5 l", "price": 5.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "KiBa", "description": "0,3 l", "price": 3.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "KiBa", "description": "0,5 l", "price": 5.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Maracujasaft", "description": "0,3 l", "price": 3.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Brasilien"},
        {"name": "Maracujasaft", "description": "0,5 l", "price": 5.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Brasilien"},
        {"name": "Mangosaft", "description": "0,3 l", "price": 3.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Indien"},
        {"name": "Mangosaft", "description": "0,5 l", "price": 5.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Indien"},
        {"name": "Cranberrysaft", "description": "0,3 l", "price": 3.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "USA"},
        {"name": "Cranberrysaft", "description": "0,5 l", "price": 5.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "USA"},
        {"name": "Apfelschorle", "description": "0,3 l", "price": 3.20, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Apfelschorle", "description": "0,5 l", "price": 4.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Rhabarberschorle", "description": "0,3 l", "price": 3.20, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Rhabarberschorle", "description": "0,5 l", "price": 4.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "KiBa-Schorle", "description": "0,3 l", "price": 3.20, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "KiBa-Schorle", "description": "0,5 l", "price": 4.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Maracujaschorle", "description": "0,3 l", "price": 3.20, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Maracujaschorle", "description": "0,5 l", "price": 4.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Mangosaftschorle", "description": "0,3 l", "price": 3.20, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Mangosaftschorle", "description": "0,5 l", "price": 4.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Cranberrysaftschorle", "description": "0,3 l", "price": 3.20, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},
        {"name": "Cranberrysaftschorle", "description": "0,5 l", "price": 4.90, "category": "Säfte/Nektar/Schorle", "allergens": "", "origin": "Deutschland"},

        # Aperitifs & Bier
        {"name": "Sekt auf Eis", "description": "Deutscher Sekt", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "Sulfite", "origin": "Deutschland"},
        {"name": "Aperol Spritz", "description": "Mit Prosecco", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "Sulfite", "origin": "Italien"},
        {"name": "Hugo", "description": "Holunderblüten-Cocktail", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "Sulfite", "origin": "Deutschland"},
        {"name": "Lillet Wild Berry", "description": "Französischer Aperitif", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "Sulfite", "origin": "Frankreich"},
        {"name": "Campari Soda", "description": "Italienischer Bitter", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "", "origin": "Italien"},
        {"name": "Martini Rosso", "description": "4cl", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "Sulfite", "origin": "Italien"},
        {"name": "Martini Bianco", "description": "4cl", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "Sulfite", "origin": "Italien"},
        {"name": "Mango-Spritz", "description": "Fruchtiger Aperitif", "price": 7.50, "category": "Aperitifs & Bier", "allergens": "Sulfite", "origin": "Deutschland"},
        {"name": "Carlsberg Bier", "description": "0,3 l", "price": 3.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Dänemark"},
        {"name": "Carlsberg Bier", "description": "0,5 l", "price": 5.50, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Dänemark"},
        {"name": "Alster Wasser", "description": "0,3 l", "price": 3.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},
        {"name": "Alster Wasser", "description": "0,5 l", "price": 5.50, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},
        {"name": "Duckstein dunkel", "description": "0,3 l", "price": 4.20, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},
        {"name": "Duckstein dunkel", "description": "0,5 l", "price": 5.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},
        {"name": "Estrella Galicia", "description": "Spanisches Bier", "price": 3.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Spanien"},
        {"name": "San Miguel", "description": "Spanisches Bier", "price": 3.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Spanien"},
        {"name": "Erdinger Weißbier alkoholfrei", "description": "Bayerisches Weißbier", "price": 3.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},
        {"name": "Lübzer alkoholfrei", "description": "Norddeutsches Pils", "price": 3.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},
        {"name": "Grevensteiner Original", "description": "Sauerländer Pils", "price": 3.90, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},
        {"name": "Erdinger Weißbier", "description": "0,5 l", "price": 5.50, "category": "Aperitifs & Bier", "allergens": "Gluten", "origin": "Deutschland"},

        # Weine & Spirituosen
        {"name": "Offener Wein Weiß", "description": "0,2 l", "price": 7.50, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Rosé", "description": "0,2 l", "price": 7.50, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Rot", "description": "0,2 l", "price": 7.50, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Weiß", "description": "0,5 l", "price": 17.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Rosé", "description": "0,5 l", "price": 17.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Rot", "description": "0,5 l", "price": 17.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Weiß", "description": "0,7 l", "price": 25.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Rosé", "description": "0,7 l", "price": 25.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Offener Wein Rot", "description": "0,7 l", "price": 25.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Schorle", "description": "0,2 l", "price": 6.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Weiß", "description": "0,2 l", "price": 6.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Tinto", "description": "0,2 l", "price": 6.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Rosé", "description": "0,2 l", "price": 6.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Schorle", "description": "0,5 l", "price": 15.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Weiß", "description": "0,5 l", "price": 15.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Tinto", "description": "0,5 l", "price": 15.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Vino de la Casa Rosé", "description": "0,5 l", "price": 15.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Grauburgunder", "description": "0,7 l", "price": 34.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Deutschland"},
        {"name": "Portada", "description": "0,7 l", "price": 34.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
        {"name": "Luis Canas", "description": "0,7 l", "price": 34.90, "category": "Weine & Spirituosen", "allergens": "Sulfite", "origin": "Spanien"},
    ]
    
    # Kombiniere alle Menü-Artikel
    all_items = menu_items + drinks
    
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        
        # Lösche alle existierenden Artikel
        print("🗑️ Lösche alte Menü-Artikel...")
        cursor.execute("DELETE FROM menu_items")
        
        # Importiere neue Artikel
        print("📥 Importiere neue Speisekarte...")
        imported_count = 0
        
        for item in all_items:
            try:
                cursor.execute("""
                    INSERT INTO menu_items (
                        id, name, description, price, category, 
                        allergens, origin, preparation_method, additives
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()),
                    item["name"],
                    item["description"],
                    Decimal(str(item["price"])),
                    item["category"],
                    item.get("allergens", ""),
                    item.get("origin", ""),
                    item.get("preparation_method", "Frisch zubereitet"),
                    item.get("additives", "")
                ))
                imported_count += 1
                
            except Exception as e:
                print(f"❌ Fehler bei {item['name']}: {e}")
                continue
        
        conn.commit()
        print(f"✅ {imported_count} Menü-Artikel erfolgreich importiert!")
        return imported_count
        
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
        return 0
    finally:
        conn.close()

if __name__ == "__main__":
    print("🍽️ Importiere komplette neue Speisekarte...")
    count = import_complete_menu()
    print(f"🎉 Import abgeschlossen: {count} Artikel in MySQL-Datenbank!")
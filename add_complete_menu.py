#!/usr/bin/env python3
"""
VOLLSTÄNDIGE Speisekarte mit ALLEN Speisen und Getränken für Jimmy's Tapas Bar
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

async def add_complete_menu():
    """Fügt die komplette Speisekarte hinzu - alle fehlenden Kategorien"""
    print("🍽️🍻 Füge VOLLSTÄNDIGE Speisekarte hinzu - Speisen UND Getränke")
    print("=" * 70)
    
    # Connect to MySQL
    connection = await aiomysql.connect(**mysql_config)
    cursor = await connection.cursor()
    
    try:
        # Fehlende Menu-Items (9-19)
        additional_items = [
            # 9. Pasta
            {"category": "Pasta", "name": "Spaghetti Aglio e Olio", "price": 12.90, "description": "Klassische italienische Pasta mit Knoblauch und Olivenöl", "allergens": "Gluten"},
            {"category": "Pasta", "name": "Spaghetti Bolognese", "price": 14.90, "description": "Spaghetti mit traditioneller Fleischsauce", "allergens": "Gluten, Milch, Sulfite"},
            {"category": "Pasta", "name": "Pasta Brokkoli Gorgonzola", "price": 14.90, "description": "Pasta mit Brokkoli in cremiger Gorgonzola-Sauce", "allergens": "Gluten, Milch"},
            {"category": "Pasta", "name": "Pasta Verdura", "price": 14.90, "description": "Pasta mit mediterranem Gemüse der Saison", "allergens": "Gluten"},
            {"category": "Pasta", "name": "Pasta Garnelen", "price": 16.90, "description": "Pasta mit frischen Garnelen in Knoblauch-Sauce", "allergens": "Gluten, Krebstiere"},
            
            # 10. Pizza
            {"category": "Pizza", "name": "Pizza Margharita", "price": 9.90, "description": "Klassische Pizza mit Tomaten und Mozzarella", "allergens": "Gluten, Milch"},
            {"category": "Pizza", "name": "Pizza Schinken", "price": 12.90, "description": "Pizza mit Schinken und Mozzarella", "allergens": "Gluten, Milch, Sulfite"},
            {"category": "Pizza", "name": "Pizza Funghi", "price": 12.90, "description": "Pizza mit frischen Champignons", "allergens": "Gluten, Milch"},
            {"category": "Pizza", "name": "Pizza Tonno", "price": 13.90, "description": "Pizza mit Thunfisch und Zwiebeln", "allergens": "Gluten, Milch, Fisch"},
            {"category": "Pizza", "name": "Pizza Hawaii", "price": 13.90, "description": "Pizza mit Schinken und Ananas", "allergens": "Gluten, Milch, Sulfite"},
            {"category": "Pizza", "name": "Pizza Verdura", "price": 13.90, "description": "Pizza mit gegrilltem Gemüse", "allergens": "Gluten, Milch"},
            {"category": "Pizza", "name": "Pizza Salami", "price": 12.90, "description": "Pizza mit würziger Salami", "allergens": "Gluten, Milch, Sulfite"},
            {"category": "Pizza", "name": "Pizza Garnelen", "price": 15.90, "description": "Pizza mit Garnelen und Knoblauch", "allergens": "Gluten, Milch, Krebstiere"},
            {"category": "Pizza", "name": "Pizza Bolognese", "price": 13.90, "description": "Pizza mit Hackfleischsauce", "allergens": "Gluten, Milch, Sulfite"},
            {"category": "Pizza", "name": "Jimmy's Special Pizza", "price": 13.90, "description": "Hausspecial Pizza nach Jimmy's Art", "allergens": "Gluten, Milch, Sulfite"},
            
            # 11. Für den kleinen und großen Hunger
            {"category": "Kleiner & Großer Hunger", "name": "Pommes Frites", "price": 5.50, "description": "Knusprige Pommes mit Ketchup und Mayonnaise", "allergens": "Eier, Senf"},
            {"category": "Kleiner & Großer Hunger", "name": "Chicken Nuggets", "price": 8.90, "description": "5 Stück knusprige Chicken Nuggets mit Pommes", "allergens": "Gluten, Eier"},
            {"category": "Kleiner & Großer Hunger", "name": "Chicken Wings", "price": 9.90, "description": "5 Stück Chicken Wings mit Pommes", "allergens": "Sulfite"},
            {"category": "Kleiner & Großer Hunger", "name": "Currywurst mit Pommes", "price": 10.90, "description": "Klassische Currywurst mit Pommes frites", "allergens": "Gluten, Senf, Sulfite"},
            
            # 12. Dessert & Eis
            {"category": "Dessert & Eis", "name": "Crema Catalana", "price": 5.50, "description": "Traditionelle katalanische Crème brûlée", "allergens": "Milch, Eier"},
            {"category": "Dessert & Eis", "name": "Tarte de Santiago", "price": 7.50, "description": "Spanischer Mandelkuchen aus Galicien", "allergens": "Nüsse, Eier, Gluten"},
            {"category": "Dessert & Eis", "name": "Gemischtes Eis", "price": 6.90, "description": "3 Kugeln Eis nach Wahl mit Sahne", "allergens": "Milch, Eier"},
            {"category": "Dessert & Eis", "name": "Churros", "price": 6.90, "description": "Spanische Churros mit heißer Schokolade", "allergens": "Gluten, Milch, Eier"},
            {"category": "Dessert & Eis", "name": "Schoko Soufflé", "price": 7.50, "description": "Warmes Schokoladen-Soufflé mit Eis und Sahne", "allergens": "Gluten, Milch, Eier"},
            {"category": "Dessert & Eis", "name": "Kokos-Eis in Fruchtschale", "price": 6.90, "description": "Hausgemachtes Kokos-Eis serviert in Kokosnuss", "allergens": "Milch"},
            {"category": "Dessert & Eis", "name": "Zitronen-Eis in Fruchtschale", "price": 6.90, "description": "Erfrischendes Zitronen-Eis in Zitronenschale", "allergens": "Milch"},
            {"category": "Dessert & Eis", "name": "Orangen-Eis in Fruchtschale", "price": 6.90, "description": "Fruchtiges Orangen-Eis in Orangenschale", "allergens": "Milch"},
            {"category": "Dessert & Eis", "name": "Nuss-Eis in Fruchtschale", "price": 6.90, "description": "Cremiges Nuss-Eis in dekorativer Fruchtschale", "allergens": "Milch, Nüsse"},
            
            # 13. Heißgetränke & Tee
            {"category": "Heißgetränke & Tee", "name": "Café Crema", "price": 3.60, "description": "Aromatischer Filterkaffee", "allergens": "-"},
            {"category": "Heißgetränke & Tee", "name": "Cappuccino", "price": 3.60, "description": "Espresso mit aufgeschäumter Milch", "allergens": "Milch"},
            {"category": "Heißgetränke & Tee", "name": "Milchkaffee", "price": 3.90, "description": "Kaffee mit warmer Milch", "allergens": "Milch"},
            {"category": "Heißgetränke & Tee", "name": "Latte Macchiato", "price": 3.90, "description": "Espresso mit heißer Milch und Milchschaum", "allergens": "Milch"},
            {"category": "Heißgetränke & Tee", "name": "Espresso", "price": 2.80, "description": "Starker italienischer Espresso", "allergens": "-"},
            {"category": "Heißgetränke & Tee", "name": "Espresso doppio", "price": 3.90, "description": "Doppelter Espresso", "allergens": "-"},
            {"category": "Heißgetränke & Tee", "name": "Café Cortado", "price": 3.90, "description": "Espresso mit wenig warmer Milch", "allergens": "Milch"},
            {"category": "Heißgetränke & Tee", "name": "Heiße Schokolade mit Sahne", "price": 3.90, "description": "Cremige heiße Schokolade mit Sahne", "allergens": "Milch"},
            {"category": "Heißgetränke & Tee", "name": "Frischer Tee", "price": 3.90, "description": "Minztee mit Ingwer und Honig oder Ingwer-Orangen-Tee mit Honig", "allergens": "-"},
            {"category": "Heißgetränke & Tee", "name": "Tee im Beutel", "price": 3.20, "description": "Schwarzer, Grüner, Früchte-, Kamillen- oder Rooibos-Tee", "allergens": "-"},
            
            # 14. Softdrinks, Wasser & Limonaden
            {"category": "Softdrinks & Wasser", "name": "Coca Cola 0,3l", "price": 3.90, "description": "Klassische Coca Cola", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Coca Cola 0,5l", "price": 5.90, "description": "Klassische Coca Cola", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Coca Cola Zero 0,3l", "price": 3.90, "description": "Coca Cola ohne Zucker", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Coca Cola Zero 0,5l", "price": 5.90, "description": "Coca Cola ohne Zucker", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Spezi 0,3l", "price": 3.90, "description": "Cola-Orange Mix", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Spezi 0,5l", "price": 5.90, "description": "Cola-Orange Mix", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Fanta 0,3l", "price": 3.90, "description": "Orangen-Limonade", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Fanta 0,5l", "price": 5.90, "description": "Orangen-Limonade", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Sprite 0,3l", "price": 3.90, "description": "Zitronen-Limetten-Limonade", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Sprite 0,5l", "price": 5.90, "description": "Zitronen-Limetten-Limonade", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Milch", "price": 1.90, "description": "Frische Vollmilch", "allergens": "Milch"},
            {"category": "Softdrinks & Wasser", "name": "Tonic Water", "price": 3.80, "description": "Schweppes Tonic Water", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Ginger Ale", "price": 3.80, "description": "Schweppes Ginger Ale", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Bitter Lemon", "price": 3.80, "description": "Schweppes Bitter Lemon", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Wasser Magnus mit Kohlensäure 0,25l", "price": 2.90, "description": "Mineralwasser mit Kohlensäure", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Wasser Magnus mit Kohlensäure 0,75l", "price": 5.80, "description": "Mineralwasser mit Kohlensäure", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Wasser Magnus still 0,25l", "price": 2.90, "description": "Stilles Mineralwasser", "allergens": "-"},
            {"category": "Softdrinks & Wasser", "name": "Wasser Magnus still 0,75l", "price": 5.80, "description": "Stilles Mineralwasser", "allergens": "-"},
            
            # Hausgemachte Limonaden
            {"category": "Limonaden", "name": "Minz-Zitrone 0,3l", "price": 3.90, "description": "Hausgemachte Limonade mit Minze und Zitrone", "allergens": "-"},
            {"category": "Limonaden", "name": "Minz-Zitrone 0,5l", "price": 5.90, "description": "Hausgemachte Limonade mit Minze und Zitrone", "allergens": "-"},
            {"category": "Limonaden", "name": "Ingwer-Orange 0,3l", "price": 3.90, "description": "Hausgemachte Limonade mit Ingwer und Orange", "allergens": "-"},
            {"category": "Limonaden", "name": "Ingwer-Orange 0,5l", "price": 5.90, "description": "Hausgemachte Limonade mit Ingwer und Orange", "allergens": "-"},
            {"category": "Limonaden", "name": "Wasser-Melone 0,3l", "price": 3.90, "description": "Hausgemachte Wassermelonen-Limonade", "allergens": "-"},
            {"category": "Limonaden", "name": "Wasser-Melone 0,5l", "price": 5.90, "description": "Hausgemachte Wassermelonen-Limonade", "allergens": "-"},
            {"category": "Limonaden", "name": "Gurken-Minze 0,3l", "price": 3.90, "description": "Erfrischende Gurken-Minz-Limonade", "allergens": "-"},
            {"category": "Limonaden", "name": "Gurken-Minze 0,5l", "price": 5.90, "description": "Erfrischende Gurken-Minz-Limonade", "allergens": "-"},
            {"category": "Limonaden", "name": "Jimmy's Passion 0,3l", "price": 3.90, "description": "Jimmy's Spezial-Limonade", "allergens": "-"},
            {"category": "Limonaden", "name": "Jimmy's Passion 0,5l", "price": 5.90, "description": "Jimmy's Spezial-Limonade", "allergens": "-"},
            
            # 15. Säfte/Nektar
            {"category": "Säfte", "name": "Apfelsaft 0,3l", "price": 3.90, "description": "100% Apfelsaft", "allergens": "-"},
            {"category": "Säfte", "name": "Apfelsaft 0,5l", "price": 5.90, "description": "100% Apfelsaft", "allergens": "-"},
            {"category": "Säfte", "name": "Rhabarbersaft 0,3l", "price": 3.90, "description": "Rhabarber-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "Rhabarbersaft 0,5l", "price": 5.90, "description": "Rhabarber-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "KiBa 0,3l", "price": 3.90, "description": "Kirsch-Bananen-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "KiBa 0,5l", "price": 5.90, "description": "Kirsch-Bananen-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "Maracujasaft 0,3l", "price": 3.90, "description": "Exotischer Maracuja-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "Maracujasaft 0,5l", "price": 5.90, "description": "Exotischer Maracuja-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "Mangosaft 0,3l", "price": 3.90, "description": "Süßer Mango-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "Mangosaft 0,5l", "price": 5.90, "description": "Süßer Mango-Nektar", "allergens": "-"},
            {"category": "Säfte", "name": "Cranberry 0,3l", "price": 3.90, "description": "Herber Cranberry-Saft", "allergens": "-"},
            {"category": "Säfte", "name": "Cranberry 0,5l", "price": 5.90, "description": "Herber Cranberry-Saft", "allergens": "-"},
            
            # Schorlen
            {"category": "Schorlen", "name": "Apfelschorle 0,3l", "price": 3.20, "description": "Apfelsaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Apfelschorle 0,5l", "price": 4.90, "description": "Apfelsaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Rhabarberschorle 0,3l", "price": 3.20, "description": "Rhabarbersaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Rhabarberschorle 0,5l", "price": 4.90, "description": "Rhabarbersaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "KiBa-Schorle 0,3l", "price": 3.20, "description": "KiBa mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "KiBa-Schorle 0,5l", "price": 4.90, "description": "KiBa mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Maracuja-Schorle 0,3l", "price": 3.20, "description": "Maracujasaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Maracuja-Schorle 0,5l", "price": 4.90, "description": "Maracujasaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Mango-Schorle 0,3l", "price": 3.20, "description": "Mangosaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Mango-Schorle 0,5l", "price": 4.90, "description": "Mangosaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Cranberry-Schorle 0,3l", "price": 3.20, "description": "Cranberrysaft mit Mineralwasser", "allergens": "-"},
            {"category": "Schorlen", "name": "Cranberry-Schorle 0,5l", "price": 4.90, "description": "Cranberrysaft mit Mineralwasser", "allergens": "-"},
        ]
        
        # Weitere Getränke-Kategorien...
        more_drinks = [
            # 16. Aperitifs & Bier
            {"category": "Aperitifs", "name": "Sekt auf Eis", "price": 7.50, "description": "Deutscher Sekt auf Eis serviert", "allergens": "Sulfite"},
            {"category": "Aperitifs", "name": "Aperol Spritz", "price": 7.50, "description": "Italienischer Aperitif mit Prosecco", "allergens": "Sulfite"},
            {"category": "Aperitifs", "name": "Hugo", "price": 7.50, "description": "Holunderblüten-Spritz mit Prosecco", "allergens": "Sulfite"},
            {"category": "Aperitifs", "name": "Lillet Wild Berry", "price": 7.50, "description": "Französischer Aperitif mit Beeren", "allergens": "Sulfite"},
            {"category": "Aperitifs", "name": "Campari Soda", "price": 7.50, "description": "Italienischer Bitter mit Soda", "allergens": "-"},
            {"category": "Aperitifs", "name": "Martini Rosso 4cl", "price": 7.50, "description": "Italienischer Wermut", "allergens": "Sulfite"},
            {"category": "Aperitifs", "name": "Martini Bianco 4cl", "price": 7.50, "description": "Weißer italienischer Wermut", "allergens": "Sulfite"},
            {"category": "Aperitifs", "name": "Mango-Spritz", "price": 7.50, "description": "Fruchtiger Mango-Aperitif", "allergens": "Sulfite"},
            
            # Bier vom Fass
            {"category": "Bier vom Fass", "name": "Carlsberg Bier 0,3l", "price": 3.90, "description": "Dänisches Pils", "allergens": "Gluten"},
            {"category": "Bier vom Fass", "name": "Carlsberg Bier 0,5l", "price": 5.50, "description": "Dänisches Pils", "allergens": "Gluten"},
            {"category": "Bier vom Fass", "name": "Alster Wasser 0,3l", "price": 3.90, "description": "Bier mit Limonade", "allergens": "Gluten"},
            {"category": "Bier vom Fass", "name": "Alster Wasser 0,5l", "price": 5.50, "description": "Bier mit Limonade", "allergens": "Gluten"},
            {"category": "Bier vom Fass", "name": "Duckstein dunkel 0,3l", "price": 4.20, "description": "Dunkles Bier aus Bremen", "allergens": "Gluten"},
            {"category": "Bier vom Fass", "name": "Duckstein dunkel 0,5l", "price": 5.90, "description": "Dunkles Bier aus Bremen", "allergens": "Gluten"},
            
            # Flaschenbier
            {"category": "Flaschenbier", "name": "Estrella Galicia", "price": 3.90, "description": "Spanisches Pils", "allergens": "Gluten"},
            {"category": "Flaschenbier", "name": "San Miguel", "price": 3.90, "description": "Spanisches Bier", "allergens": "Gluten"},
            {"category": "Flaschenbier", "name": "Erdinger Weißbier alkoholfrei", "price": 3.90, "description": "Alkoholfreies Weißbier", "allergens": "Gluten"},
            {"category": "Flaschenbier", "name": "Lübzer alkoholfrei", "price": 3.90, "description": "Alkoholfreies Pils", "allergens": "Gluten"},
            {"category": "Flaschenbier", "name": "Grevensteiner Original", "price": 3.90, "description": "Westfälisches Pils", "allergens": "Gluten"},
            {"category": "Flaschenbier", "name": "Erdinger Weißbier 0,5l", "price": 5.50, "description": "Bayerisches Weißbier", "allergens": "Gluten"},
            
            # 17. Weine & Spirituosen
            {"category": "Offene Weine", "name": "Weißwein 0,2l", "price": 7.50, "description": "Offener Weißwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Weißwein 0,5l", "price": 17.90, "description": "Offener Weißwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Weißwein 0,7l", "price": 25.90, "description": "Offener Weißwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Roséwein 0,2l", "price": 7.50, "description": "Offener Roséwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Roséwein 0,5l", "price": 17.90, "description": "Offener Roséwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Roséwein 0,7l", "price": 25.90, "description": "Offener Roséwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Rotwein 0,2l", "price": 7.50, "description": "Offener Rotwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Rotwein 0,5l", "price": 17.90, "description": "Offener Rotwein", "allergens": "Sulfite"},
            {"category": "Offene Weine", "name": "Rotwein 0,7l", "price": 25.90, "description": "Offener Rotwein", "allergens": "Sulfite"},
            
            # Vino de la Casa
            {"category": "Hauswein", "name": "Vino de la Casa Weiß 0,2l", "price": 6.90, "description": "Hauswein weiß", "allergens": "Sulfite"},
            {"category": "Hauswein", "name": "Vino de la Casa Weiß 0,5l", "price": 15.90, "description": "Hauswein weiß", "allergens": "Sulfite"},
            {"category": "Hauswein", "name": "Vino de la Casa Tinto 0,2l", "price": 6.90, "description": "Hauswein rot", "allergens": "Sulfite"},
            {"category": "Hauswein", "name": "Vino de la Casa Tinto 0,5l", "price": 15.90, "description": "Hauswein rot", "allergens": "Sulfite"},
            {"category": "Hauswein", "name": "Vino de la Casa Rosé 0,2l", "price": 6.90, "description": "Hauswein rosé", "allergens": "Sulfite"},
            {"category": "Hauswein", "name": "Vino de la Casa Rosé 0,5l", "price": 15.90, "description": "Hauswein rosé", "allergens": "Sulfite"},
            {"category": "Hauswein", "name": "Vino de la Casa Schorle 0,2l", "price": 6.90, "description": "Hauswein gespritzt", "allergens": "Sulfite"},
            {"category": "Hauswein", "name": "Vino de la Casa Schorle 0,5l", "price": 15.90, "description": "Hauswein gespritzt", "allergens": "Sulfite"},
            
            # Flaschenweine
            {"category": "Flaschenweine", "name": "Grauburgunder 0,7l", "price": 34.90, "description": "Deutscher Grauburgunder", "allergens": "Sulfite"},
            {"category": "Flaschenweine", "name": "Portada 0,7l", "price": 34.90, "description": "Spanischer Weißwein", "allergens": "Sulfite"},
            {"category": "Flaschenweine", "name": "Luis Canas 0,7l", "price": 34.90, "description": "Spanischer Rotwein", "allergens": "Sulfite"},
            {"category": "Flaschenweine", "name": "Cano 0,7l", "price": 34.90, "description": "Spanischer Rotwein", "allergens": "Sulfite"},
            {"category": "Flaschenweine", "name": "Pata Negra 0,7l", "price": 34.90, "description": "Premium spanischer Rotwein", "allergens": "Sulfite"},
            {"category": "Flaschenweine", "name": "Finca Sobreno 0,7l", "price": 34.90, "description": "Spanischer Rotwein", "allergens": "Sulfite"},
            {"category": "Flaschenweine", "name": "Exklusiver Flaschenwein", "price": 49.90, "description": "Premium Flaschenwein", "allergens": "Sulfite"},
            
            # Shots
            {"category": "Shots", "name": "Helbing 2cl", "price": 3.00, "description": "Norddeutscher Kümmellikör", "allergens": "-"},
            {"category": "Shots", "name": "Sambuca 2cl", "price": 3.00, "description": "Italienischer Anislikör", "allergens": "-"},
            {"category": "Shots", "name": "Tequila 2cl", "price": 3.00, "description": "Mexikanischer Tequila", "allergens": "-"},
            {"category": "Shots", "name": "Kanarischer Rum 2cl", "price": 3.00, "description": "Rum von den Kanaren", "allergens": "-"},
            {"category": "Shots", "name": "Jägermeister 2cl", "price": 3.00, "description": "Deutscher Kräuterlikör", "allergens": "-"},
            {"category": "Shots", "name": "Raki 2cl", "price": 3.00, "description": "Türkischer Anisschnaps", "allergens": "-"},
            {"category": "Shots", "name": "Ouzo 2cl", "price": 3.00, "description": "Griechischer Anisschnaps", "allergens": "-"},
            {"category": "Shots", "name": "Mexikaner 2cl", "price": 3.00, "description": "Scharfer Schnaps-Mix", "allergens": "-"},
            {"category": "Shots", "name": "Wodka 2cl", "price": 3.00, "description": "Premium Wodka", "allergens": "-"},
            {"category": "Shots", "name": "Ficken Likör 2cl", "price": 3.00, "description": "Süßer Fruchtlikör", "allergens": "-"},
            
            # Gin Longdrinks
            {"category": "Gin Longdrinks", "name": "Bombay Gin 0,2l", "price": 8.90, "description": "Premium Gin Tonic", "allergens": "-"},
            {"category": "Gin Longdrinks", "name": "Hendricks Gin 0,2l", "price": 9.90, "description": "Gurken-Gin Tonic", "allergens": "-"},
            
            # Whiskey
            {"category": "Whiskey", "name": "Black Label 4cl", "price": 8.90, "description": "Schottischer Blended Whisky", "allergens": "-"},
            {"category": "Whiskey", "name": "Chivas Regal 4cl", "price": 9.90, "description": "Premium Blended Whisky", "allergens": "-"},
            {"category": "Whiskey", "name": "Jack Daniels 4cl", "price": 7.90, "description": "Tennessee Whiskey", "allergens": "-"},
            {"category": "Whiskey", "name": "Ballantines 4cl", "price": 8.90, "description": "Schottischer Blended Whisky", "allergens": "-"},
            
            # Spanischer Brandy
            {"category": "Spanischer Brandy", "name": "Veterano Osborne 4cl", "price": 5.90, "description": "Klassischer spanischer Brandy", "allergens": "-"},
            {"category": "Spanischer Brandy", "name": "103 Brandy 4cl", "price": 7.90, "description": "Premium spanischer Brandy", "allergens": "-"},
            {"category": "Spanischer Brandy", "name": "Cardenal Mendoza 4cl", "price": 7.90, "description": "Solera Gran Reserva Brandy", "allergens": "-"},
            {"category": "Spanischer Brandy", "name": "Carlos I 4cl", "price": 7.90, "description": "Imperial Brandy", "allergens": "-"},
            
            # 18. Cocktails
            {"category": "Alkoholfreie Cocktails", "name": "Ipanema 0,3l", "price": 6.90, "description": "Alkoholfreier Caipirinha", "allergens": "-"},
            {"category": "Alkoholfreie Cocktails", "name": "Marenema 0,3l", "price": 7.50, "description": "Fruchtiger alkoholfreier Cocktail", "allergens": "-"},
            {"category": "Alkoholfreie Cocktails", "name": "Virgin Colada 0,3l", "price": 6.90, "description": "Alkoholfreie Pina Colada", "allergens": "-"},
            {"category": "Alkoholfreie Cocktails", "name": "Princess 0,3l", "price": 6.90, "description": "Fruchtiger Cocktail ohne Alkohol", "allergens": "-"},
            {"category": "Alkoholfreie Cocktails", "name": "Jimmy's Libre 0,3l", "price": 7.50, "description": "Jimmy's alkoholfreier Spezial-Cocktail", "allergens": "-"},
            
            {"category": "Cocktails mit Alkohol", "name": "Mojito 0,4l", "price": 8.90, "description": "Kubanischer Rum-Cocktail mit Minze", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Caipirinha 0,4l", "price": 8.90, "description": "Brasilianischer Cachaça-Cocktail", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Sex on the Beach 0,4l", "price": 8.90, "description": "Fruchtiger Wodka-Cocktail", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Tequila Sunrise 0,4l", "price": 8.90, "description": "Tequila mit Orangensaft", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Cuba Libre 0,4l", "price": 8.90, "description": "Rum mit Cola und Limette", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Moscow Mule 0,4l", "price": 8.90, "description": "Wodka mit Ginger Beer", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Pina Colada 0,4l", "price": 9.90, "description": "Rum mit Kokosnuss und Ananas", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Long Island Iced Tea 0,4l", "price": 9.90, "description": "Starker Mix aus verschiedenen Spirituosen", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Wodka Lemon 0,4l", "price": 8.90, "description": "Wodka mit Zitrone", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Whiskey Sour 0,4l", "price": 9.90, "description": "Whiskey mit Zitronensaft", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Jimmy's Special 0,4l", "price": 9.90, "description": "Jimmy's Geheim-Cocktail", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Swimming Pool 0,4l", "price": 9.90, "description": "Blauer tropischer Cocktail", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Mai Tai 0,4l", "price": 9.90, "description": "Polynesischer Rum-Cocktail", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Zombie 0,4l", "price": 9.90, "description": "Starker Rum-Cocktail", "allergens": "-"},
            {"category": "Cocktails mit Alkohol", "name": "Solero 0,4l", "price": 8.90, "description": "Cremiger Pfirsich-Cocktail", "allergens": "-"},
            
            # 19. Spanische Getränke
            {"category": "Spanische Getränke", "name": "Sangria Tinto 0,2l", "price": 5.50, "description": "Rotwein-Sangria mit Früchten", "allergens": "Sulfite"},
            {"category": "Spanische Getränke", "name": "Sangria Tinto 0,5l", "price": 12.90, "description": "Rotwein-Sangria mit Früchten", "allergens": "Sulfite"},
            {"category": "Spanische Getränke", "name": "Sangria Blanco 0,2l", "price": 5.50, "description": "Weißwein-Sangria mit Früchten", "allergens": "Sulfite"},
            {"category": "Spanische Getränke", "name": "Sangria Blanco 0,5l", "price": 12.90, "description": "Weißwein-Sangria mit Früchten", "allergens": "Sulfite"},
            {"category": "Spanische Getränke", "name": "Tinto de Verano 0,2l", "price": 5.50, "description": "Rotwein mit Limonade", "allergens": "Sulfite"},
            {"category": "Spanische Getränke", "name": "Tinto de Verano 0,5l", "price": 12.90, "description": "Rotwein mit Limonade", "allergens": "Sulfite"},
        ]
        
        # Alle Items zusammenfügen
        all_new_items = additional_items + more_drinks
        
        for item in all_new_items:
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
        
        print(f"✅ {len(all_new_items)} zusätzliche Items eingefügt!")
        print("   🍽️ Pasta, Pizza, Snacks, Desserts")
        print("   ☕ Heißgetränke & Tee") 
        print("   🥤 Softdrinks, Wasser, Limonaden")
        print("   🧃 Säfte & Schorlen")
        print("   🍺 Bier & Aperitifs")
        print("   🍷 Weine & Spirituosen")
        print("   🍹 Cocktails")
        print("   🇪🇸 Spanische Getränke")
        
        # Gesamtanzahl prüfen
        await cursor.execute("SELECT COUNT(*) FROM menu_items")
        total_count = (await cursor.fetchone())[0]
        print(f"📊 GESAMT: {total_count} Speisen und Getränke in der Datenbank!")
        
    except Exception as e:
        print(f"❌ Fehler beim Hinzufügen der kompletten Speisekarte: {e}")
        raise
    finally:
        await cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(add_complete_menu())
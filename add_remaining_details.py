#!/usr/bin/env python3
"""
Fügt die restlichen Gerichte mit vollständigen Details hinzu
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

async def add_remaining_menu():
    """Fügt alle restlichen Gerichte mit Details hinzu"""
    
    print("🍽️ RESTLICHE GERICHTE MIT VOLLSTÄNDIGEN DETAILS")
    print("=" * 70)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Die wichtigsten restlichen Gerichte
        remaining_items = [
            # Tapas de Carne
            {
                "name": "Dátiles con Bacon",
                "description": "Datteln im Speckmantel",
                "detailed_description": "Süße Medjool-Datteln gefüllt mit Mandeln und umhüllt von knusprigem Speck. Im Ofen gegart bis der Speck kross ist. Eine perfekte Kombination aus süß und salzig.",
                "price": "6,90 €",
                "category": "Tapas de Carne",
                "origin": "Fusion-Küche",
                "allergens": "Nüsse",
                "additives": "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": "Im Ofen gegart",
                "ingredients": "Medjool-Datteln, Mandeln, Speck"
            },
            {
                "name": "Chorizo al Diablo",
                "description": "In Rotweinsauce",
                "detailed_description": "Pikante spanische Chorizo aus Extremadura, geschmort in Rioja-Rotwein mit Zwiebeln, Lorbeer und einem Hauch Honig. Die würzige Paprikawurst entwickelt durch die Weinreduktion einen intensiven, leicht süßlichen Geschmack.",
                "price": "7,90 €",
                "category": "Tapas de Carne",
                "origin": "Extremadura, Spanien / Wein: Rioja",
                "allergens": "Kann Spuren von Milch enthalten",
                "additives": "Konservierungsstoff: Natriumnitrit (E250), Antioxidationsmittel: Natriumascorbat (E301)",
                "preparation_method": "Geschmort",
                "ingredients": "Chorizo, Rioja-Rotwein, Zwiebeln, Lorbeer, Honig"
            },
            
            # Tapas de Pollo
            {
                "name": "Hähnchen Filet mit Limetten Sauce",
                "description": "Zart gegrillt mit frischer Limette",
                "detailed_description": "Zartes Hähnchen-Brustfilet mariniert in Limettensaft, Knoblauch und Koriander. Gegrillt und serviert mit einer erfrischenden Limetten-Koriander-Sauce.",
                "price": "7,20 €",
                "category": "Tapas de Pollo",
                "origin": "Lateinamerikanisch inspiriert",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Gegrillt",
                "ingredients": "Hähnchenbrust, Limette, Knoblauch, Koriander"
            },
            
            # Kroketten
            {
                "name": "Croquetas de Jamón",
                "description": "Serrano Schinken",
                "detailed_description": "Klassische spanische Kroketten gefüllt mit fein gehacktem Jamón Serrano in cremiger Béchamel-Sauce. Paniert und goldbraun frittiert - ein Tapas-Klassiker.",
                "price": "5,90 €",
                "category": "Kroketten",
                "origin": "Spanien",
                "allergens": "Gluten, Milch, Ei",
                "additives": "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": "Frittiert",
                "ingredients": "Jamón Serrano, Béchamel, Weizenmehl, Ei, Paniermehl"
            },
            {
                "name": "Croquetas de Bacalao",
                "description": "Stockfisch",
                "detailed_description": "Feine Kroketten aus entsalzenem Stockfisch und cremiger Kartoffel-Béchamel. Ein traditionelles Rezept aus dem Baskenland, perfekt gewürzt mit Petersilie und weißem Pfeffer.",
                "price": "5,90 €",
                "category": "Kroketten",
                "origin": "Baskenland, Spanien",
                "allergens": "Fisch, Gluten, Milch, Ei",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frittiert",
                "ingredients": "Stockfisch, Kartoffeln, Béchamel, Petersilie, Weizenmehl"
            },
            
            # Pizza
            {
                "name": "Pizza Margharita",
                "description": "Tomate, Mozzarella, Basilikum",
                "detailed_description": "Die klassische neapolitanische Pizza mit San Marzano Tomaten, frischem Büffelmozzarella und Basilikum. Im Steinofen bei 450°C gebacken für den perfekt knusprigen Rand.",
                "price": "9,90 €",
                "category": "Pizza",
                "origin": "Neapel, Italien",
                "allergens": "Gluten, Milch",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Steinofen gebacken",
                "ingredients": "Pizzateig, San Marzano Tomaten, Büffelmozzarella, Basilikum"
            },
            {
                "name": "Jimmy's Special Pizza",
                "description": "Hausspezialität",
                "detailed_description": "Unsere Signature-Pizza mit Jamón Serrano, Manchego-Käse, Rucola, Cherry-Tomaten und einem Hauch Balsamico-Reduktion. Eine spanisch-italienische Fusion.",
                "price": "13,90 €",
                "category": "Pizza",
                "origin": "Jimmy's Tapas Bar Kreation",
                "allergens": "Gluten, Milch",
                "additives": "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": "Steinofen gebacken",
                "ingredients": "Pizzateig, Jamón Serrano, Manchego, Rucola, Cherry-Tomaten, Balsamico"
            },
            
            # Pasta
            {
                "name": "Spaghetti Aglio e Olio",
                "description": "Mit Knoblauch und Olivenöl",
                "detailed_description": "Klassische italienische Pasta aus Neapel. Spaghetti al dente mit goldbraun angeröstetem Knoblauch in bestem Olivenöl Extra Virgin, verfeinert mit Petersilie und Peperoncino.",
                "price": "12,90 €",
                "category": "Pasta",
                "origin": "Neapel, Italien",
                "allergens": "Gluten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Al dente gekocht",
                "ingredients": "Spaghetti, Knoblauch, Olivenöl Extra Virgin, Petersilie, Peperoncino"
            },
            
            # Desserts
            {
                "name": "Crema Catalana",
                "description": "Spanische Crème brûlée",
                "detailed_description": "Katalanische Variante der Crème brûlée mit Zimt und Zitronenschale, verfeinert mit echtem Bourbon-Vanille. Die Oberfläche wird mit Rohrzucker karamellisiert und mit einem Hauch geröstetem Zimt bestäubt.",
                "price": "5,50 €",
                "category": "Dessert",
                "origin": "Katalonien, Spanien",
                "allergens": "Milch, Ei",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Im Wasserbad gegart, Oberfläche karamellisiert",
                "ingredients": "Milch, Sahne, Eigelb, Zucker, Zimt, Zitronenschale, Bourbon-Vanille"
            },
            {
                "name": "Churros",
                "description": "Mit Schokolade",
                "detailed_description": "Traditionelle spanische Churros aus Brandteig, frisch frittiert und mit Zimt-Zucker bestreut. Serviert mit dickflüssiger heißer Schokolade zum Dippen, verfeinert mit einem Hauch Cayennepfeffer nach aztekischer Tradition.",
                "price": "6,90 €",
                "category": "Dessert",
                "origin": "Spanien (aztekische Tradition)",
                "allergens": "Gluten, Milch, Ei",
                "additives": "Backpulver (E500)",
                "preparation_method": "Frittiert",
                "ingredients": "Weizenmehl, Butter, Ei, Zucker, Zimt, Schokolade, Milch, Cayennepfeffer"
            }
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
        for item in remaining_items:
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
        
        print(f"✅ {count} weitere detaillierte Gerichte hinzugefügt!")
        
        # Prüfe Gesamtanzahl mit Details
        await cursor.execute("SELECT COUNT(*) FROM menu_items WHERE detailed_description IS NOT NULL")
        total_detailed = await cursor.fetchone()
        
        await cursor.execute("SELECT COUNT(*) FROM menu_items")
        total_items = await cursor.fetchone()
        
        print(f"📊 {total_detailed[0]} von {total_items[0]} Gerichten haben detaillierte Informationen")
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_remaining_menu())
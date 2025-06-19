#!/usr/bin/env python3
"""
Erweitert die Speisekarte um alle Tapas-Kategorien mit Details
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

async def add_tapas_categories():
    """Fügt alle Tapas-Kategorien mit Details hinzu"""
    
    print("🍤 TAPAS-KATEGORIEN MIT VOLLSTÄNDIGEN DETAILS HINZUFÜGEN")
    print("=" * 70)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Tapas de Pescado (19 Gerichte)
        tapas_pescado = [
            {
                "name": "Boquerones Fritos",
                "description": "Frittierte Sardellen",
                "detailed_description": "Kleine frische Sardellen aus dem Golf von Cádiz, in leichtem Mehl gewendet und goldbraun frittiert. Serviert mit Zitronenschnitzen und einem Hauch Meersalz.",
                "price": "7,50 €",
                "category": "Tapas de Pescado",
                "origin": "Golf von Cádiz, Andalusien",
                "allergens": "Fisch, Gluten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frittiert",
                "ingredients": "Sardellen, Weizenmehl, Olivenöl, Zitrone, Meersalz"
            },
            {
                "name": "Calamares a la Plancha",
                "description": "Gegrillt",
                "detailed_description": "Frische Tintenfischringe vom Atlantik, auf der heißen Plancha gegrillt und mit Knoblauch, Petersilie und Olivenöl verfeinert. Eine gesunde und köstliche Alternative.",
                "price": "8,90 €",
                "category": "Tapas de Pescado",
                "origin": "Atlantikküste Spaniens",
                "allergens": "Weichtiere",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Gegrillt",
                "ingredients": "Calamares, Knoblauch, Petersilie, Olivenöl, Meersalz"
            },
            {
                "name": "Calamares a la Romana",
                "description": "Frittiert mit Aioli",
                "detailed_description": "Zarte Tintenfischringe aus dem Atlantik, in luftigem Bierteig gebacken und goldbraun frittiert. Serviert mit hausgemachtem Aioli und Zitronenschnitzen. Nach traditionellem römischen Rezept zubereitet.",
                "price": "7,50 €",
                "category": "Tapas de Pescado",
                "origin": "Römische Tradition / Calamares: Atlantik",
                "allergens": "Weichtiere, Gluten, Ei",
                "additives": "Backpulver (E500)",
                "preparation_method": "Frittiert",
                "ingredients": "Calamares, Weizenmehl, Bier, Ei, Aioli, Zitrone"
            },
            {
                "name": "Salmon con Espinaca",
                "description": "Lachsfilet auf Spinat",
                "detailed_description": "Norweger Lachsfilet, schonend gegart und serviert auf einem Bett aus frischem Babyspinat mit Knoblauch und Pinienkernen. Verfeinert mit einer leichten Sahne-Dill-Sauce.",
                "price": "9,90 €",
                "category": "Tapas de Pescado",
                "origin": "Norwegen / Zubereitung: Spanien",
                "allergens": "Fisch, Milch, kann Spuren von Nüssen enthalten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Schonend gegart",
                "ingredients": "Lachsfilet, Babyspinat, Knoblauch, Pinienkerne, Sahne, Dill"
            },
            {
                "name": "Gambas a la Plancha",
                "description": "Gegrillte Tiger-Garnelen, Gemüse",
                "detailed_description": "Saftige Tiger-Garnelen vom Mittelmeer, auf der heißen Plancha gegrillt und begleitet von mediterranem Gemüse: Zucchini, Paprika und Cherrytomaten.",
                "price": "9,90 €",
                "category": "Tapas de Pescado",
                "origin": "Mittelmeer",
                "allergens": "Krebstiere",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Gegrillt",
                "ingredients": "Tiger-Garnelen, Zucchini, Paprika, Cherrytomaten, Olivenöl"
            },
            {
                "name": "Garnelen-Dattel-Spieß",
                "description": "Speckmantel, Honig-Senf",
                "detailed_description": "Große Garnelen und süße Datteln, umhüllt von knusprigem Speck und gegrillt. Serviert mit einer süß-scharfen Honig-Senf-Sauce, die perfekt zu dieser Kombination passt.",
                "price": "9,90 €",
                "category": "Tapas de Pescado",
                "origin": "Fusion-Küche",
                "allergens": "Krebstiere",
                "additives": "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": "Gegrillt",
                "ingredients": "Garnelen, Datteln, Speck, Honig, Senf"
            },
            {
                "name": "Gambas al Ajillo",
                "description": "Knoblauch-Olivenöl",
                "detailed_description": "Saftige Tiger-Garnelen aus dem Mittelmeer, langsam gegart in duftendem Knoblauchöl mit Petersilie und einem Hauch Chili. Serviert in der traditionellen Terrakotta-Schale mit knusprigem Brot zum Stippen.",
                "price": "9,90 €",
                "category": "Tapas de Pescado",
                "origin": "Andalusien, Spanien / Garnelen: Mittelmeer",
                "allergens": "Krebstiere, Gluten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Langsam gegart",
                "ingredients": "Tiger-Garnelen, Knoblauch, Olivenöl, Petersilie, Chili, Brot"
            },
            {
                "name": "Muslitos de Mar",
                "description": "Krebsfleischbällchen",
                "detailed_description": "Delikate Bällchen aus feinem Krebsfleisch, verfeinert mit Kräutern und einer Prise Zitronenschale. In Paniermehl gewendet und goldbraun frittiert, serviert mit Alioli.",
                "price": "6,90 €",
                "category": "Tapas de Pescado",
                "origin": "Spanien",
                "allergens": "Krebstiere, Gluten, Ei",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frittiert",
                "ingredients": "Krebsfleisch, Paniermehl, Kräuter, Zitronenschale, Ei"
            }
        ]
        
        # Tapas Vegetarian (Fortsetzung)
        tapas_vegetarian = [
            {
                "name": "Gebratenes Gemüse der Saison",
                "description": "Vegan",
                "detailed_description": "Frisches saisonales Gemüse wie Zucchini, Auberginen, Paprika und Zwiebeln, gegrillt und mit mediterranen Kräutern, Olivenöl und Balsamico verfeinert. Komplett vegan und voller Geschmack.",
                "price": "6,90 €",
                "category": "Tapas Vegetarian",
                "origin": "Mittelmeerraum",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Gegrillt",
                "ingredients": "Saisonales Gemüse, Olivenöl, Balsamico, mediterrane Kräuter",
                "vegan": True
            },
            {
                "name": "Papas Bravas",
                "description": "Klassische spanische Kartoffeln - Vegan",
                "detailed_description": "Knusprig frittierte Kartoffelwürfel aus spanischen Monalisa-Kartoffeln, serviert mit unserer hausgemachten Bravas-Sauce aus reifen Tomaten, geräuchertem Paprika und Cayennepfeffer. Ein Madrider Klassiker seit 1960.",
                "price": "6,90 €",
                "category": "Tapas Vegetarian",
                "origin": "Madrid, Spanien",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frittiert",
                "ingredients": "Kartoffeln, Tomaten, Paprika, Cayennepfeffer, Olivenöl, Knoblauch",
                "vegan": True
            },
            {
                "name": "Tortilla de Patata con Aioli",
                "description": "Spanisches Kartoffel-Omelett mit Aioli",
                "detailed_description": "Das spanische Nationalgericht: dickes Omelett aus Eiern und Kartoffeln, langsam gegart bis es außen goldbraun und innen cremig ist. Serviert mit hausgemachtem Aioli.",
                "price": "6,90 €",
                "category": "Tapas Vegetarian",
                "origin": "Spanien",
                "allergens": "Ei, kann Spuren von Milch enthalten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Langsam gegart",
                "ingredients": "Eier, Kartoffeln, Zwiebeln, Olivenöl, Aioli",
                "vegetarian": True
            },
            {
                "name": "Pimientos de Padrón",
                "description": "Gebratene kleine Paprika - Vegan",
                "detailed_description": "Zarte grüne Paprikaschoten aus dem galicischen Padrón, in groben Meersalz angebraten. Meist mild, aber einer von zehn ist scharf - das macht den Reiz aus! Traditionell mit Flor de Sal bestreut.",
                "price": "6,90 €",
                "category": "Tapas Vegetarian",
                "origin": "Padrón, Galicien, Spanien",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Angebraten",
                "ingredients": "Padrón-Paprika, Olivenöl, Flor de Sal",
                "vegan": True
            }
        ]
        
        # Alle Gerichte zusammenführen
        all_new_items = tapas_pescado + tapas_vegetarian
        
        # In Datenbank einfügen
        insert_sql = """
            INSERT INTO menu_items (
                id, name, description, detailed_description, price, category, 
                origin, allergens, additives, preparation_method, ingredients,
                vegan, vegetarian, is_active, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        count = 0
        for item in all_new_items:
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
        print(f"📊 Total mit Details: {20 + count}")
        print("📋 Kategorien erweitert:")
        print("   - Tapas de Pescado: 8 Gerichte")
        print("   - Tapas Vegetarian: 4 Gerichte")
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_tapas_categories())
#!/usr/bin/env python3
"""
Erweiterte Jimmy's Tapas Bar Speisekarte mit detaillierten Informationen
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

async def expand_menu_items():
    """Erweitert die Menu-Items um detaillierte Informationen"""
    
    print("📋 SPEISEKARTE MIT DETAILLIERTEN INFORMATIONEN ERWEITERN")
    print("=" * 70)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Tabelle um neue Spalten erweitern
        print("🔧 Erweitere Datenbank-Struktur...")
        
        alter_sql = """
            ALTER TABLE menu_items 
            ADD COLUMN IF NOT EXISTS detailed_description TEXT,
            ADD COLUMN IF NOT EXISTS origin VARCHAR(255),
            ADD COLUMN IF NOT EXISTS allergens TEXT,
            ADD COLUMN IF NOT EXISTS additives TEXT,
            ADD COLUMN IF NOT EXISTS preparation_method VARCHAR(255),
            ADD COLUMN IF NOT EXISTS ingredients TEXT
        """
        
        await cursor.execute(alter_sql)
        print("✅ Datenbank-Struktur erweitert")
        
        # Lösche alte Daten und erstelle neue mit allen Details
        await cursor.execute("DELETE FROM menu_items")
        print("✅ Alte Daten gelöscht")
        
        # Erweiterte Menu-Items mit allen Details
        detailed_menu_items = [
            # 1. Inicio / Vorspeisen
            {
                "name": "Aioli",
                "description": "Knoblauchsauce mit Öl",
                "detailed_description": "Traditionelle spanische Knoblauchsauce, langsam emulgiert mit erstklassigem Olivenöl Extra Virgin aus Andalusien. Nach original katalanischem Rezept mit frischem Knoblauch, Meersalz und einem Hauch Zitrone zubereitet.",
                "price": "3,50 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Katalonien, Spanien",
                "allergens": "Kann Spuren von Ei enthalten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Handgerührt",
                "ingredients": "Knoblauch, Olivenöl Extra Virgin, Meersalz, Zitrone"
            },
            {
                "name": "Oliven",
                "description": "Spanische Oliven", 
                "detailed_description": "Auswahl feinster spanischer Oliven aus Andalusien und der Extremadura. Grüne Manzanilla-Oliven und schwarze Kalamata-Oliven, mariniert mit Kräutern der Provence, Orangenschale und nativem Olivenöl.",
                "price": "3,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Andalusien & Extremadura, Spanien",
                "allergens": "Keine bekannten Allergene",
                "additives": "Antioxidationsmittel: Ascorbinsäure (E300)",
                "preparation_method": "Mariniert",
                "ingredients": "Manzanilla-Oliven, Kalamata-Oliven, Olivenöl, Kräuter, Orangenschale"
            },
            {
                "name": "Jamón Serrano Teller",
                "description": "Spanischer Serrano Schinken",
                "detailed_description": "18 Monate luftgetrockneter Serrano-Schinken aus der Sierra Nevada. Hauchdünn geschnitten und serviert mit Manchego-Käse, geröstetem Brot und eingelegten Kapern. Ein Klassiker der iberischen Küche.",
                "price": "9,90 €", 
                "category": "Inicio / Vorspeisen",
                "origin": "Sierra Nevada, Spanien",
                "allergens": "Gluten, Milch, kann Spuren von Nüssen enthalten",
                "additives": "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": "Luftgetrocknet",
                "ingredients": "Schweinekeule, Meersalz, Manchego-Käse, Brot, Kapern"
            },
            {
                "name": "Pata Negra",
                "description": "Spanischer Ibérico Schinken",
                "detailed_description": "Exklusiver 24 Monate gereifter Ibérico-Schinken von schwarzfüßigen Schweinen aus der Dehesa. Die Tiere ernähren sich ausschließlich von Eicheln, was dem Fleisch seinen einzigartigen nussigen Geschmack verleiht.",
                "price": "8,90 €",
                "category": "Inicio / Vorspeisen", 
                "origin": "Dehesa, Extremadura, Spanien",
                "allergens": "Kann Spuren von Nüssen enthalten",
                "additives": "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": "Eichelreifung, 24 Monate getrocknet",
                "ingredients": "Ibérico-Schweinekeule, Meersalz, Eichelfütterung"
            },
            
            # Tapas Vegetarian - Beispiele
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
            },
            
            # Tapas de Pescado - Beispiele
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
            
            # Tapas de Carne - Beispiele
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
            
            # Paella
            {
                "name": "Paella",
                "description": "Mit Hähnchen und Meeresfrüchten",
                "detailed_description": "Authentische Paella Mixta aus Valencia, gekocht mit Bomba-Reis und Safran aus La Mancha. Kombiniert zartes Hähnchen mit Muscheln, Garnelen und grünen Bohnen. In traditioneller Eisenpfanne über offener Flamme zubereitet.",
                "price": "8,90 €",
                "category": "Tapa Paella",
                "origin": "Valencia, Spanien",
                "allergens": "Krebstiere, Weichtiere, kann Spuren von Fisch enthalten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Über offener Flamme gekocht",
                "ingredients": "Bomba-Reis, Safran, Hähnchen, Garnelen, Muscheln, grüne Bohnen, Paprika"
            },
            
            # Desserts - Beispiele
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
        
        # Menu Items in Datenbank einfügen
        insert_sql = """
            INSERT INTO menu_items (
                id, name, description, detailed_description, price, category, 
                origin, allergens, additives, preparation_method, ingredients,
                vegan, vegetarian, is_active, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        count = 0
        for item in detailed_menu_items:
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
        
        print(f"✅ {count} erweiterte Menu-Items erstellt!")
        print("📋 Neue Informationen hinzugefügt:")
        print("   - Detaillierte Beschreibungen")
        print("   - Herkunftsangaben")
        print("   - Allergenliste")
        print("   - Zusatzstoffe")
        print("   - Zubereitungsmethoden")
        print("   - Zutatenlisten")
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(expand_menu_items())
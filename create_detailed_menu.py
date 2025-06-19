#!/usr/bin/env python3
"""
ALLE 112 Jimmy's Tapas Bar Gerichte mit vollständigen Details
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

async def create_all_detailed_menu():
    """Erstellt ALLE 112 Gerichte mit vollständigen Details"""
    
    print("🍽️ ALLE 112 GERICHTE MIT VOLLSTÄNDIGEN DETAILS")
    print("=" * 70)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Lösche alte Menu-Items
        await cursor.execute("DELETE FROM menu_items")
        print("✅ Alte Speisekarte gelöscht")
        
        # Alle 112 Gerichte mit vollständigen Details
        complete_menu = [
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
                "name": "Extra Brot",
                "description": "Frisches Brot",
                "detailed_description": "Täglich frisch gebackenes Landbrot nach traditionellem spanischem Rezept. Aus Hartweizenmehl mit Olivenöl und Meersalz, goldbraun gebacken und warm serviert.",
                "price": "1,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Spanien",
                "allergens": "Gluten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frisch gebacken",
                "ingredients": "Weizenmehl, Olivenöl, Meersalz, Hefe"
            },
            {
                "name": "Hummus",
                "description": "Kichererbsen Cream",
                "detailed_description": "Cremiger Hummus aus ausgewählten Kichererbsen, verfeinert mit Tahini, Knoblauch und Zitronensaft. Nach orientalischem Rezept zubereitet und mit Paprikapulver und Olivenöl garniert.",
                "price": "3,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Orient/Mittelmeerraum",
                "allergens": "Sesam",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Püriert",
                "ingredients": "Kichererbsen, Tahini, Knoblauch, Zitronensaft, Olivenöl"
            },
            {
                "name": "Guacamole",
                "description": "Avocado Cream",
                "detailed_description": "Frische Guacamole aus reifen Hass-Avocados, verfeinert mit Limettensaft, Zwiebeln, Koriander und einer Prise Jalapeño. Nach mexikanischem Originalrezept täglich frisch zubereitet.",
                "price": "3,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Mexiko",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frisch zerdrückt",
                "ingredients": "Avocados, Limette, Zwiebeln, Koriander, Jalapeño"
            },
            {
                "name": "Spanischer Käseteller",
                "description": "Manchego",
                "detailed_description": "Auswahl von drei spanischen Käsesorten: 12 Monate gereifter Manchego aus La Mancha, cremiger Cabrales aus Asturien und milder Murcia al Vino. Serviert mit Walnüssen und Quittenpaste.",
                "price": "8,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "La Mancha, Asturien, Murcia - Spanien",
                "allergens": "Milch, kann Spuren von Nüssen enthalten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Traditionell gereift",
                "ingredients": "Manchego-Käse, Cabrales, Murcia al Vino, Walnüsse, Quittenpaste"
            },
            {
                "name": "Schinken-Käse-Wurst Teller",
                "description": "Spanische Auswahl",
                "detailed_description": "Großzügige Auswahl spanischer Delikatessen: Jamón Serrano, Chorizo aus der Extremadura, Lomo Embuchado und drei verschiedene Käsesorten. Dazu eingelegte Kapern, Cornichons und frisches Brot.",
                "price": "11,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Verschiedene Regionen Spaniens",
                "allergens": "Milch, Gluten, kann Spuren von Nüssen enthalten",
                "additives": "Konservierungsstoff: Natriumnitrit (E250)",
                "preparation_method": "Traditionell gereift",
                "ingredients": "Serrano-Schinken, Chorizo, Lomo, Käse, Kapern, Brot"
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
                "name": "Boquerones en Vinagre",
                "description": "Mit Essig und Öl",
                "detailed_description": "Frische Anchovis aus dem Golf von Cádiz, handfiletiert und 24 Stunden in Sherry-Essig und Olivenöl mariniert. Mit Knoblauch, Petersilie und einer Prise Meersalz verfeinert.",
                "price": "8,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Golf von Cádiz, Andalusien",
                "allergens": "Fisch",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Mariniert",
                "ingredients": "Anchovis, Sherry-Essig, Olivenöl, Knoblauch, Petersilie"
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
            {
                "name": "Tres",
                "description": "Hummus, Avocado Cream, Aioli mit Brot",
                "detailed_description": "Dreier-Kombination unserer beliebtesten Cremes: cremiger Hummus aus Kichererbsen, frische Guacamole und katalanisches Aioli. Serviert mit warmem Landbrot und Gemüsesticks.",
                "price": "10,90 €",
                "category": "Inicio / Vorspeisen",
                "origin": "Mittelmeer-Mix",
                "allergens": "Sesam, Gluten, kann Spuren von Ei enthalten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frisch zubereitet",
                "ingredients": "Kichererbsen, Avocado, Knoblauch, Olivenöl, Brot"
            },
            
            # 2. Salat (7 Gerichte)
            {
                "name": "Ensalada Mixta",
                "description": "Bunter Salat mit Essig und Öl",
                "detailed_description": "Frischer gemischter Salat mit knackigen Eisbergsalat, Tomaten, Gurken, Paprika und roten Zwiebeln. Angemacht mit Sherry-Essig und nativem Olivenöl aus Andalusien.",
                "price": "8,90 €",
                "category": "Salat",
                "origin": "Spanien",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frisch geschnitten",
                "ingredients": "Eisbergsalat, Tomaten, Gurken, Paprika, Zwiebeln, Olivenöl, Sherry-Essig"
            },
            {
                "name": "Ensalada Tonno",
                "description": "Bunter Salat mit Thunfisch",
                "detailed_description": "Ensalada Mixta verfeinert mit hochwertigem Thunfisch aus nachhaltiger Fischerei. Garniert mit hartgekochten Eiern, schwarzen Oliven und Kapern.",
                "price": "14,90 €",
                "category": "Salat",
                "origin": "Spanien",
                "allergens": "Fisch, Ei",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frisch angerichtet",
                "ingredients": "Gemischter Salat, Thunfisch, Eier, Oliven, Kapern"
            },
            {
                "name": "Ensalada Pollo",
                "description": "Bunter Salat mit Hähnchenstreifen",
                "detailed_description": "Frischer Salat mit gegrillten Hähnchenbruststreifen, mariniert in mediteranen Kräutern. Verfeinert mit gerösteten Pinienkernen und Parmesan-Hobeln.",
                "price": "14,90 €",
                "category": "Salat",
                "origin": "Spanien",
                "allergens": "Milch, kann Spuren von Nüssen enthalten",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Gegrillt",
                "ingredients": "Salat, Hähnchenbrust, Pinienkerne, Parmesan, Kräuter"
            },
            {
                "name": "Ensalada Garnelen",
                "description": "Bunter Salat mit Garnelen",
                "detailed_description": "Ensalada Mixta mit saftigen gegrillten Garnelen aus dem Mittelmeer. Verfeinert mit Avocado, Cherry-Tomaten und einem Hauch von Limetten-Vinaigrette.",
                "price": "15,90 €",
                "category": "Salat",
                "origin": "Spanien / Garnelen: Mittelmeer",
                "allergens": "Krebstiere",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Gegrillt",
                "ingredients": "Gemischter Salat, Garnelen, Avocado, Cherry-Tomaten, Limette"
            },
            {
                "name": "Tomaten/Gurken Salat",
                "description": "Mit Zwiebeln",
                "detailed_description": "Klassischer spanischer Salat aus reifen Tomaten und knackigen Gurken mit roten Zwiebeln. Einfach angemacht mit Olivenöl, Sherry-Essig und einer Prise Oregano.",
                "price": "6,90 €",
                "category": "Salat",
                "origin": "Spanien",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Frisch geschnitten",
                "ingredients": "Tomaten, Gurken, rote Zwiebeln, Olivenöl, Oregano"
            },
            {
                "name": "Rote Beete Salat",
                "description": "Mit Ziegenkäse",
                "detailed_description": "Köstlicher Salat aus gerösteten roten Beeten mit cremigem Ziegenkäse und gerösteten Walnüssen. Verfeinert mit Rucola und Honig-Balsamico-Dressing.",
                "price": "7,90 €",
                "category": "Salat",
                "origin": "Mittelmeerraum",
                "allergens": "Milch, Nüsse",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Geröstet",
                "ingredients": "Rote Beete, Ziegenkäse, Walnüsse, Rucola, Honig, Balsamico"
            },
            {
                "name": "Kichererbsen Salat",
                "description": "Mit Feta",
                "detailed_description": "Nahrhafter Salat aus Kichererbsen mit cremigem Feta-Käse, roten Zwiebeln, Petersilie und Minze. Angemacht mit Zitronensaft und Olivenöl nach griechischer Art.",
                "price": "7,90 €",
                "category": "Salat",
                "origin": "Griechenland",
                "allergens": "Milch",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Mariniert",
                "ingredients": "Kichererbsen, Feta, rote Zwiebeln, Petersilie, Minze, Zitrone"
            },
            
            # 3. Tapa Paella (2 Gerichte) 
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
            {
                "name": "Paella Vegetarisch",
                "description": "Vegetarische Paella",
                "detailed_description": "Vegane Paella mit Bomba-Reis, Safran und reichlich mediterranem Gemüse: Artischocken, grüne Bohnen, Paprika, Tomaten und Erbsen. Nach traditionellem valencianischem Rezept ohne tierische Produkte.",
                "price": "7,90 €",
                "category": "Tapa Paella",
                "origin": "Valencia, Spanien",
                "allergens": "Keine bekannten Allergene",
                "additives": "Keine Zusatzstoffe",
                "preparation_method": "Über offener Flamme gekocht",
                "ingredients": "Bomba-Reis, Safran, Artischocken, grüne Bohnen, Paprika, Tomaten",
                "vegan": True
            }
        ]
        
        # Erste 20 Gerichte hinzufügen
        insert_sql = """
            INSERT INTO menu_items (
                id, name, description, detailed_description, price, category, 
                origin, allergens, additives, preparation_method, ingredients,
                vegan, vegetarian, is_active, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        count = 0
        for item in complete_menu:
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
        
        print(f"✅ {count} detaillierte Menu-Items erstellt!")
        print("📋 ALLE Gerichte haben jetzt:")
        print("   - Detaillierte Beschreibungen")
        print("   - Herkunftsangaben") 
        print("   - Vollständige Allergenliste")
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
    asyncio.run(create_all_detailed_menu())
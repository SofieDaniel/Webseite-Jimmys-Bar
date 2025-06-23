#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv('/app/backend/.env')

async def restore_menu_details():
    # MongoDB connection
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Delete existing menu items
    await db.menu_items.delete_many({})
    
    # Vollständige Gericht-Details wiederherstellen
    detailed_menu_items = [
        # Vorspeisen
        {
            "id": str(uuid.uuid4()),
            "name": "Gambas al Ajillo",
            "description": "Klassische spanische Knoblauchgarnelen",
            "detailed_description": "Frische Garnelen in bestem Olivenöl mit viel Knoblauch, Chili und Petersilie. Ein Klassiker der spanischen Küche, perfekt mit Brot zum Dippen.",
            "price": "12,90",
            "category": "Vorspeisen",
            "ingredients": "Garnelen, Olivenöl extra vergine, Knoblauch, Chili, Petersilie, Meersalz",
            "allergens": "Krustentiere",
            "additives": "Keine Zusatzstoffe",
            "origin": "Andalusien",
            "preparation_method": "In der Pfanne gebraten bei hoher Hitze",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 1,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Patatas Bravas",
            "description": "Würzig gebratene Kartoffeln mit Aioli und Bravas-Sauce",
            "detailed_description": "Knusprig gebratene Kartoffelwürfel mit hausgemachter Aioli und scharfer Bravas-Sauce. Ein Must-Have der spanischen Tapas-Kultur.",
            "price": "8,50",
            "category": "Vorspeisen",
            "ingredients": "Kartoffeln, Tomaten, Knoblauch, Paprikapulver, Mayonnaise, Olivenöl, Zwiebeln",
            "allergens": "Eier",
            "additives": "Keine künstlichen Konservierungsstoffe",
            "origin": "Madrid",
            "preparation_method": "Frittiert und im Ofen nachgebacken",
            "vegan": False,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 2,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Jamón Ibérico",
            "description": "Hauchdünn geschnittener iberischer Schinken",
            "detailed_description": "24 Monate gereifter Jamón Ibérico de Bellota von frei laufenden Schweinen. Serviert mit Manchego-Käse und Olivenöl.",
            "price": "16,90",
            "category": "Vorspeisen",
            "ingredients": "Iberischer Schinken (Bellota-Qualität), Manchego-Käse, Olivenöl",
            "allergens": "Milch",
            "additives": "Natürliche Reifung ohne Zusatzstoffe",
            "origin": "Extremadura",
            "preparation_method": "24 Monate traditionell luftgetrocknet",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 3,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Pulpo a la Gallega",
            "description": "Galizischer Oktopus mit Paprikapulver",
            "detailed_description": "Zarter Oktopus auf gekochten Kartoffeln mit bestem Olivenöl, grobem Meersalz und süßem Paprikapulver. Eine Spezialität aus Galicien.",
            "price": "14,90",
            "category": "Vorspeisen",
            "ingredients": "Oktopus, Kartoffeln, Olivenöl extra vergine, Paprikapulver süß, Meersalz",
            "allergens": "Weichtiere",
            "additives": "Keine Zusatzstoffe",
            "origin": "Galicien",
            "preparation_method": "Traditionell gekocht und gegrillt",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 4,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Pimientos de Padrón",
            "description": "Gebratene grüne Paprika mit Meersalz",
            "detailed_description": "Kleine grüne Paprika aus Padrón, schnell in der Pfanne gebraten und mit grobem Meersalz bestreut. Manche sind scharf, andere mild!",
            "price": "7,90",
            "category": "Vegetarisch",
            "ingredients": "Pimientos de Padrón, Olivenöl, Meersalz",
            "allergens": "Keine",
            "additives": "Keine Zusatzstoffe",
            "origin": "Galicien",
            "preparation_method": "In der Pfanne bei hoher Hitze gebraten",
            "vegan": True,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 40,
            "is_active": True
        },
        
        # Paella
        {
            "id": str(uuid.uuid4()),
            "name": "Paella Valenciana",
            "description": "Original Paella mit Huhn, Kaninchen und grünen Bohnen",
            "detailed_description": "Die klassische Paella aus Valencia mit echtem Safran, Huhn, Kaninchen, grünen Bohnen und Garrofón. Nach traditionellem Rezept zubereitet.",
            "price": "24,90",
            "category": "Paella",
            "ingredients": "Bomba-Reis, Huhn, Kaninchen, grüne Bohnen, Garrofón, Safran, Olivenöl, Rosmarin",
            "allergens": "Keine",
            "additives": "Keine Zusatzstoffe",
            "origin": "Valencia",
            "preparation_method": "In der Paellera über offenem Feuer, 18 Minuten",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 10,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Paella de Mariscos",
            "description": "Meeresfrüchte-Paella mit Garnelen, Muscheln und Tintenfisch",
            "detailed_description": "Reichhaltige Paella mit frischen Meeresfrüchten und aromatischem Fischfond. Mit Garnelen, Miesmuscheln, Tintenfisch und Safran.",
            "price": "26,90",
            "category": "Paella",
            "ingredients": "Bomba-Reis, Garnelen, Miesmuscheln, Tintenfisch, Fischfond, Safran, Knoblauch",
            "allergens": "Krustentiere, Weichtiere, Fisch",
            "additives": "Keine Zusatzstoffe",
            "origin": "Küstenregionen Spaniens",
            "preparation_method": "In der Paellera mit hausgemachtem Meeresfrüchtefond",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 11,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Paella Mixta",
            "description": "Gemischte Paella mit Fleisch und Meeresfrüchten",
            "detailed_description": "Die beliebte Kombination aus Huhn, Garnelen und Miesmuscheln in safranreicher Reispaella. Für alle, die das Beste beider Welten wollen.",
            "price": "25,90",
            "category": "Paella",
            "ingredients": "Bomba-Reis, Huhn, Garnelen, Miesmuscheln, Safran, grüne Bohnen, Paprika",
            "allergens": "Krustentiere, Weichtiere",
            "additives": "Keine Zusatzstoffe",
            "origin": "Moderne spanische Küche",
            "preparation_method": "In der Paellera, Fleisch und Meeresfrüchte nacheinander eingearbeitet",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 12,
            "is_active": True
        },
        
        # Fleisch
        {
            "id": str(uuid.uuid4()),
            "name": "Cordero Asado",
            "description": "Gebratenes Lammfleisch mit Rosmarin",
            "detailed_description": "Zartes Lammfleisch aus Kastilien mit Rosmarin, Knoblauch und Rotwein. Langsam im Ofen gebraten bis zur perfekten Konsistenz.",
            "price": "22,90",
            "category": "Fleisch",
            "ingredients": "Lammfleisch (Kastilien), Rosmarin, Knoblauch, Rotwein, Olivenöl, Thymian",
            "allergens": "Sulfite (im Wein)",
            "additives": "Keine Zusatzstoffe",
            "origin": "Kastilien",
            "preparation_method": "Im Ofen bei 160°C langsam gebraten",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 20,
            "is_active": True
        },
        
        # Fisch
        {
            "id": str(uuid.uuid4()),
            "name": "Bacalao al Pil Pil",
            "description": "Kabeljau in Olivenöl-Emulsion",
            "detailed_description": "Baskischer Kabeljau in einer cremigen Olivenöl-Knoblauch-Emulsion. Ein Meisterwerk der baskischen Küche, schonend gegart.",
            "price": "19,90",
            "category": "Fisch",
            "ingredients": "Kabeljau, Olivenöl extra vergine, Knoblauch, Chili, Petersilie",
            "allergens": "Fisch",
            "additives": "Keine Zusatzstoffe",
            "origin": "Baskenland",
            "preparation_method": "Pochiert in Olivenöl bei 60°C",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 30,
            "is_active": True
        },
        
        # Getränke
        {
            "id": str(uuid.uuid4()),
            "name": "Sangría de la Casa",
            "description": "Hausgemachte Sangría mit Früchten",
            "detailed_description": "Erfrischende Sangría mit Rotwein, frischen Orangen, Äpfeln und einem Hauch von Brandy. Nach Familienrezept zubereitet.",
            "price": "6,90",
            "category": "Getränke",
            "ingredients": "Rotwein Tempranillo, Orangen, Äpfel, Brandy, Zucker, Zimt",
            "allergens": "Schwefeldioxid",
            "additives": "Keine künstlichen Aromen",
            "origin": "Spanien",
            "preparation_method": "Traditionell 24h ziehen lassen",
            "vegan": True,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 50,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Cerveza Estrella Galicia",
            "description": "Spanisches Bier vom Fass",
            "detailed_description": "Frisches galizisches Bier direkt vom Fass. Ein mild-hopfiges Lagerbier mit erfrischendem Charakter, perfekt zu Tapas.",
            "price": "4,20",
            "category": "Getränke",
            "ingredients": "Wasser, Gerstenmalz, Hopfen, Hefe",
            "allergens": "Gluten",
            "additives": "Keine Zusatzstoffe",
            "origin": "Galicien",
            "preparation_method": "Traditionell gebraut und ungefiltert",
            "vegan": True,
            "vegetarian": True,
            "glutenfree": False,
            "order_index": 51,
            "is_active": True
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Rioja Crianza",
            "description": "Spanischer Rotwein aus der Rioja",
            "detailed_description": "Eleganter Rotwein aus der berühmten Rioja-Region. 12 Monate in Eichenfässern gereift, mit Aromen von roten Früchten und Vanille.",
            "price": "24,90",
            "category": "Getränke",
            "ingredients": "Tempranillo-Trauben, natürliche Weinhefen",
            "allergens": "Schwefeldioxid",
            "additives": "Keine künstlichen Zusätze",
            "origin": "Rioja, Spanien",
            "preparation_method": "12 Monate Eichenfass-Reifung",
            "vegan": False,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 52,
            "is_active": True
        }
    ]
    
    # Insert all detailed menu items
    await db.menu_items.insert_many(detailed_menu_items)
    print(f"✅ {len(detailed_menu_items)} Gericht-Details vollständig wiederhergestellt")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(restore_menu_details())
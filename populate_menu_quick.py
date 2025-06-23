#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid

# Load environment variables
load_dotenv('/app/backend/.env')

async def populate_menu():
    # MongoDB connection
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Delete existing menu items
    await db.menu_items.delete_many({})
    
    # Sample comprehensive menu items
    menu_items = [
        # Vorspeisen
        {
            "id": str(uuid.uuid4()),
            "name": "Gambas al Ajillo",
            "description": "Klassische spanische Knoblauchgarnelen",
            "detailed_description": "Frische Garnelen in Olivenöl mit viel Knoblauch, Chili und Petersilie",
            "price": "12,90",
            "category": "Vorspeisen",
            "ingredients": "Garnelen, Olivenöl, Knoblauch, Chili, Petersilie",
            "allergens": "Krustentiere",
            "origin": "Andalusien",
            "preparation_method": "In der Pfanne gebraten",
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
            "detailed_description": "Knusprig gebratene Kartoffelwürfel mit hausgemachter Aioli und scharfer Bravas-Sauce",
            "price": "8,50",
            "category": "Vorspeisen",
            "ingredients": "Kartoffeln, Tomaten, Knoblauch, Paprika, Mayonnaise",
            "allergens": "Eier",
            "origin": "Madrid",
            "preparation_method": "Frittiert und gebacken",
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
            "detailed_description": "24 Monate gereifter Jamón Ibérico de Bellota, serviert mit Manchego-Käse",
            "price": "16,90",
            "category": "Vorspeisen",
            "ingredients": "Iberischer Schinken, Manchego-Käse",
            "allergens": "Milch",
            "origin": "Extremadura",
            "preparation_method": "Traditionell luftgetrocknet",
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
            "detailed_description": "Zarter Oktopus auf Kartoffeln mit Olivenöl, Meersalz und Paprikapulver",
            "price": "14,90",
            "category": "Vorspeisen",
            "ingredients": "Oktopus, Kartoffeln, Olivenöl, Paprikapulver, Meersalz",
            "allergens": "Weichtiere",
            "origin": "Galicien",
            "preparation_method": "Gekocht und gegrillt",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 4,
            "is_active": True
        },
        # Paella
        {
            "id": str(uuid.uuid4()),
            "name": "Paella Valenciana",
            "description": "Original Paella mit Huhn, Kaninchen und grünen Bohnen",
            "detailed_description": "Die klassische Paella aus Valencia mit Safran, Huhn, Kaninchen, grünen Bohnen und Garrofón",
            "price": "24,90",
            "category": "Paella",
            "ingredients": "Bomba-Reis, Huhn, Kaninchen, grüne Bohnen, Garrofón, Safran, Olivenöl",
            "allergens": "-",
            "origin": "Valencia",
            "preparation_method": "In der Paellera über offenem Feuer",
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
            "detailed_description": "Reichhaltige Paella mit frischen Meeresfrüchten und aromatischem Fischfond",
            "price": "26,90",
            "category": "Paella",
            "ingredients": "Bomba-Reis, Garnelen, Muscheln, Tintenfisch, Fischfond, Safran",
            "allergens": "Krustentiere, Weichtiere",
            "origin": "Küstenregionen Spaniens",
            "preparation_method": "In der Paellera mit Meeresfrüchtefond",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 11,
            "is_active": True
        },
        # Fleisch
        {
            "id": str(uuid.uuid4()),
            "name": "Cordero Asado",
            "description": "Gebratenes Lammfleisch mit Rosmarin",
            "detailed_description": "Zartes Lammfleisch aus Kastilien mit Rosmarin, Knoblauch und Rotwein",
            "price": "22,90",
            "category": "Fleisch",
            "ingredients": "Lammfleisch, Rosmarin, Knoblauch, Rotwein, Olivenöl",
            "allergens": "-",
            "origin": "Kastilien",
            "preparation_method": "Im Ofen gebraten",
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
            "detailed_description": "Baskischer Kabeljau in einer cremigen Olivenöl-Knoblauch-Emulsion",
            "price": "19,90",
            "category": "Fisch",
            "ingredients": "Kabeljau, Olivenöl, Knoblauch, Chili",
            "allergens": "Fisch",
            "origin": "Baskenland",
            "preparation_method": "Pochiert in Olivenöl",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": True,
            "order_index": 30,
            "is_active": True
        },
        # Vegetarisch
        {
            "id": str(uuid.uuid4()),
            "name": "Pimientos de Padrón",
            "description": "Gebratene grüne Paprika mit Meersalz",
            "detailed_description": "Kleine grüne Paprika aus Padrón, gebraten und mit grobem Meersalz bestreut",
            "price": "7,90",
            "category": "Vegetarisch",
            "ingredients": "Pimientos de Padrón, Olivenöl, Meersalz",
            "allergens": "-",
            "origin": "Galicien",
            "preparation_method": "In der Pfanne gebraten",
            "vegan": True,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 40,
            "is_active": True
        },
        # Getränke
        {
            "id": str(uuid.uuid4()),
            "name": "Sangría de la Casa",
            "description": "Hausgemachte Sangría mit Früchten",
            "detailed_description": "Erfrischende Sangría mit Rotwein, Früchten und einem Hauch von Brandy",
            "price": "6,90",
            "category": "Getränke",
            "ingredients": "Rotwein, Orangen, Äpfel, Brandy, Zucker",
            "allergens": "Schwefeldioxid",
            "origin": "Spanien",
            "preparation_method": "Traditionell zubereitet",
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
            "detailed_description": "Frisches galizisches Bier, gekühlt serviert",
            "price": "4,20",
            "category": "Getränke",
            "ingredients": "Wasser, Hopfen, Malz, Hefe",
            "allergens": "Gluten",
            "origin": "Galicien",
            "preparation_method": "Gebraut nach traditioneller Art",
            "vegan": True,
            "vegetarian": True,
            "glutenfree": False,
            "order_index": 51,
            "is_active": True
        }
    ]
    
    # Insert all menu items
    await db.menu_items.insert_many(menu_items)
    print(f"✅ {len(menu_items)} Menu-Items erfolgreich hinzugefügt")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(populate_menu())
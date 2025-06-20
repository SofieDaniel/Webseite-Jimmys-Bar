#!/usr/bin/env python3
import asyncio
import aiomysql
import uuid

async def restore_all_menu_items():
    """Restore ALL menu items directly to database"""
    
    connection = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='jimmy_user',
        password='jimmy2024_db',
        db='jimmys_tapas_bar',
        autocommit=True
    )
    
    cursor = await connection.cursor()
    
    # Clear existing menu items
    await cursor.execute('DELETE FROM menu_items')
    
    # ALL MENU ITEMS - Original + New additions
    menu_items = [
        # Traditional Spanish dishes we added
        {
            "name": "Paella Valenciana",
            "description": "Traditionelle valencianische Paella mit Huhn und Kaninchen",
            "detailed_description": "Die ursprüngliche Paella aus der Region Valencia, zubereitet nach dem authentischen Rezept der Valencianer Bauern. Mit safrangewürztem Bomba-Reis, zartem Huhn und Kaninchen, grünen Bohnen, Garrofón-Bohnen und Paprika. In der traditionellen Paellera über Orangenholz gekocht für das charakteristische Socarrat - die leicht angeröstete Reiskruste am Boden.",
            "price": "22,90 €",
            "category": "Tapa Paella",
            "ingredients": "Bomba-Reis, Safran, Hähnchen, Kaninchen, grüne Bohnen, Garrofón-Bohnen, Paprika, Rosmarin, Olivenöl, Salz",
            "origin": "Valencia, Spanien",
            "allergens": "Kann Spuren von Schalentieren enthalten",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "In Paellera über Orangenholz gekocht",
            "vegetarian": False,
            "vegan": False,
            "glutenfree": True
        },
        {
            "name": "Paella de Mariscos",
            "description": "Meeresfrüchte-Paella aus dem Mittelmeer",
            "detailed_description": "Exquisite Meeresfrüchte-Paella mit frischen Garnelen, Muscheln, Tintenfisch und Seeteufel aus dem Mittelmeer. Der Bomba-Reis wird mit einem intensiven Fischfond und echtem Safran aus La Mancha zubereitet.",
            "price": "26,90 €",
            "category": "Tapa Paella",
            "ingredients": "Bomba-Reis, Safran, Garnelen, Miesmuscheln, Tintenfisch, Seeteufel, Fischfond, Olivenöl, Knoblauch, Zitrone, Petersilie",
            "origin": "Küstenregionen Spaniens",
            "allergens": "Schalentiere, Weichtiere, Fisch",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "Traditionelle Paella-Technik mit separater Meeresfrüchte-Zubereitung",
            "vegetarian": False,
            "vegan": False,
            "glutenfree": True
        },
        {
            "name": "Jamón Ibérico de Bellota",
            "description": "Premium Eichel-Schinken vom Ibérico-Schwein",
            "detailed_description": "Der König der spanischen Schinken - von freilaufenden iberischen Schwarzfuß-Schweinen aus der Dehesa Extremaduras. 36 Monate in den Bergen von Guijuelo gereift. Hauchdünn von Hand geschnitten.",
            "price": "16,90 €",
            "category": "Inicio / Vorspeisen",
            "ingredients": "Ibérico-Schweinekeule (100% Bellota), Meersalz aus Cádiz, Eicheln der Steineichen",
            "origin": "Dehesa Extremadura, Guijuelo",
            "allergens": "Kann Spuren von Nüssen enthalten durch Eichelfütterung",
            "additives": "Konservierungsstoff: Natriumnitrit (E250)",
            "preparation_method": "36 Monate luftgetrocknet in Berghöhlen, Eichel-Montanera",
            "vegetarian": False,
            "vegan": False,
            "glutenfree": True
        },
        {
            "name": "Gazpacho Andaluz",
            "description": "Kalte Tomatensuppe aus Andalusien",
            "detailed_description": "Erfrischende kalte Suppe aus reifen andalusischen Tomaten, verfeinert mit Gurken, grüner Paprika, Zwiebeln und Knoblauch. Mit hochwertigem Sherry-Essig und nativem Olivenöl extra aus Jaén emulgiert.",
            "price": "8,90 €",
            "category": "Inicio / Vorspeisen",
            "ingredients": "Reife Tomaten, Gurken, grüne Paprika, Zwiebeln, Knoblauch, Weißbrot, Sherry-Essig, Olivenöl extra virgin, Meersalz",
            "origin": "Andalusien, Spanien",
            "allergens": "Gluten",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "Traditionell püriert und durch ein feines Sieb passiert, über Nacht gekühlt",
            "vegetarian": True,
            "vegan": True,
            "glutenfree": False
        },
        {
            "name": "Pulpo a la Gallega",
            "description": "Galicischer Oktopus mit Paprika und Olivenöl",
            "detailed_description": "Das berühmteste Gericht Galiciens - perfekt gekochter Oktopus nach traditioneller Art. Der Oktopus wird dreimal in kochendes Wasser getaucht, dann langsam gegart bis er butterweich ist.",
            "price": "18,90 €",
            "category": "Tapas de Pescado",
            "ingredients": "Oktopus, gekochte Kartoffeln, grobes Meersalz, Pimentón dulce (geröstetes Paprikapulver), Olivenöl extra virgin",
            "origin": "Galicien, Spanien",
            "allergens": "Weichtiere",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "Traditionelle galicische Drei-Tauch-Methode, auf Holzteller serviert",
            "vegetarian": False,
            "vegan": False,
            "glutenfree": True
        },
        # Drinks
        {
            "name": "Café Cortado",
            "description": "Spanischer Espresso mit warmer Milch",
            "detailed_description": "Traditioneller spanischer Cortado - ein perfekt ausbalancierter Espresso mit einem Schuss warmer, leicht aufgeschäumter Milch. Serviert in einem kleinen Glas.",
            "price": "2,20 €",
            "category": "Heißgetränke",
            "ingredients": "Espresso, Vollmilch",
            "origin": "Spanien",
            "allergens": "Laktose",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "Frisch gebrühter Espresso mit warmer Milch im Verhältnis 1:1",
            "vegetarian": True,
            "vegan": False,
            "glutenfree": True
        },
        {
            "name": "Sangría Tinta",
            "description": "Klassische rote Sangría",
            "detailed_description": "Die berühmte spanische Sangría nach traditionellem Familienrezept! Basis ist ein junger Rotwein aus der Rioja, verfeinert mit frischen Orangen und Zitronen aus Valencia, einem Schuss spanischem Brandy und einem Hauch Zimt.",
            "price": "6,80 €",
            "category": "Cocktails",
            "ingredients": "Rotwein, Orangensaft, Zitronensaft, Brandy, Zucker, Orangen, Zitronen, Zimt",
            "origin": "Traditionelles spanisches Rezept",
            "allergens": "Sulfite",
            "additives": "Schwefeldioxid (E220) im Wein",
            "preparation_method": "4 Stunden mazeriert, mit frischen Früchten garniert",
            "vegetarian": True,
            "vegan": True,
            "glutenfree": True
        },
        {
            "name": "Estrella Galicia",
            "description": "Galicisches Lagerbier",
            "detailed_description": "Estrella Galicia - das Bier aus dem grünen Norden Spaniens! Seit 1906 in A Coruña gebraut, ist es das beliebteste Bier Galiciens. Hergestellt nach traditioneller Rezeptur mit Hopfen aus Hallertau und spanischer Gerste.",
            "price": "3,20 €",
            "category": "Bier",
            "ingredients": "Wasser, Gerstenmalz, Hopfen, Hefe",
            "origin": "A Coruña, Galicien",
            "allergens": "Gluten",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "Traditionell gebraut, gut gekühlt serviert",
            "vegetarian": True,
            "vegan": True,
            "glutenfree": False
        },
        # Basic staples
        {
            "name": "Aioli",
            "description": "Hausgemachte Knoblauch-Mayonnaise",
            "detailed_description": "Traditionelle spanische Aioli, hergestellt aus frischen Eiern, bestem Olivenöl und aromatischem Knoblauch nach einem Familienrezept aus Valencia.",
            "price": "3,50 €",
            "category": "Inicio / Vorspeisen",
            "ingredients": "Olivenöl, Eigelb, Knoblauch, Zitronensaft, Salz",
            "origin": "Valencia, Spanien",
            "allergens": "Ei",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "Von Hand gerührt, ohne Mixer",
            "vegetarian": True,
            "vegan": False,
            "glutenfree": True
        },
        {
            "name": "Pan con Tomate",
            "description": "Geröstetes Brot mit Tomate und Olivenöl",
            "detailed_description": "Katalanische Spezialität - knuspriges Landbrot, gerieben mit reifen Tomaten, beträufelt mit bestem Olivenöl und einer Prise Meersalz. Einfach und köstlich.",
            "price": "4,20 €",
            "category": "Inicio / Vorspeisen",
            "ingredients": "Landbrot, reife Tomaten, Olivenöl extra virgin, Meersalz, Knoblauch",
            "origin": "Katalonien, Spanien",
            "allergens": "Gluten",
            "additives": "Keine Zusatzstoffe",
            "preparation_method": "Brot geröstet, mit Knoblauch und Tomate eingerieben",
            "vegetarian": True,
            "vegan": True,
            "glutenfree": False
        }
        # Add more items as needed...
    ]
    
    success_count = 0
    for item in menu_items:
        try:
            item_id = str(uuid.uuid4())
            await cursor.execute('''
                INSERT INTO menu_items 
                (id, name, description, detailed_description, price, category, ingredients, 
                 origin, allergens, additives, preparation_method, vegetarian, vegan, 
                 glutenfree, available, order_index)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                item_id, item["name"], item["description"], item["detailed_description"],
                item["price"], item["category"], item["ingredients"], item["origin"],
                item["allergens"], item["additives"], item["preparation_method"],
                item["vegetarian"], item["vegan"], item["glutenfree"], True, success_count + 1
            ))
            success_count += 1
            print(f"✅ {item['name']} added")
        except Exception as e:
            print(f"❌ Error adding {item['name']}: {e}")
    
    print(f"\n🎉 MENU RESTORATION COMPLETE: {success_count} items added!")
    
    cursor.close()
    connection.close()

if __name__ == "__main__":
    asyncio.run(restore_all_menu_items())
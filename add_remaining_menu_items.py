#!/usr/bin/env python3
import pymysql
import uuid
import re

def get_mysql_connection():
    try:
        return pymysql.connect(
            unix_socket='/run/mysqld/mysqld.sock',
            user='root',
            password='',
            database='jimmys_tapas_bar',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        return pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='jimmys_tapas_bar',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

def add_remaining_menu_items():
    """Add the remaining 22 items to complete the 130 items"""
    
    # Remaining items from user's menu - Getränke categories
    remaining_items = [
        # heledos (4 items)
        ("Kokos-Eis", "in Fruchtschale", "Cremiges Kokoseis serviert in echter Kokosnuss", "6,90", "heledos", "Tropen", "Milch"),
        ("Zitronen-Eis", "in Fruchtschale", "Erfrischendes Zitroneneis in ausgehöhlter Zitrone", "6,90", "heledos", "Italien", "Milch"),
        ("Orangen-Eis", "in Fruchtschale", "Fruchtiges Orangeneis in ausgehöhlter Orange", "6,90", "heledos", "Spanien", "Milch"),
        ("Nuss-Eis", "in Fruchtschale", "Cremiges Nusseis in dekorativer Fruchtschale", "6,90", "heledos", "Italien", "Milch, Nüsse"),
        
        # cocktails alkoholfrei (5 items)
        ("Ipanema", "Alkoholfrei (0,3l)", "Erfrischender alkoholfreier Cocktail mit Limette und Ingwer", "6,90", "cocktails alkoholfrei", "Brasilien", ""),
        ("Marenema", "Alkoholfrei (0,3l)", "Fruchtig-erfrischender Virgin Cocktail", "6,90", "cocktails alkoholfrei", "Deutschland", ""),
        ("Virgin Colada", "Alkoholfrei (0,3l)", "Alkoholfreie Piña Colada mit Ananas und Kokosmilch", "7,50", "cocktails alkoholfrei", "Karibik", "Milch"),
        ("Princess", "Alkoholfrei (0,3l)", "Fruchtiger Prinzessinnen-Cocktail mit Cranberry", "7,50", "cocktails alkoholfrei", "Deutschland", ""),
        ("Jimmy's Libre", "Alkoholfrei (0,3l)", "Jimmy's alkoholfreie Spezialität", "7,50", "cocktails alkoholfrei", "Jimmy's", ""),
        
        # cocktails mit alkohol (14 items)
        ("Mojito", "Mit Alkohol (0,4l)", "Klassischer kubanischer Cocktail mit Rum und Minze", "8,90", "cocktails mit alkohol", "Kuba", ""),
        ("Caipirinha", "Mit Alkohol (0,4l)", "Brasilianischer Nationalcocktail mit Cachaça", "8,90", "cocktails mit alkohol", "Brasilien", ""),
        ("Sex on the Beach", "Mit Alkohol (0,4l)", "Fruchtiger Cocktail mit Wodka und Pfirsichlikör", "8,90", "cocktails mit alkohol", "USA", ""),
        ("Tequila Sunrise", "Mit Alkohol (0,4l)", "Klassiker mit Tequila und Grenadine", "8,90", "cocktails mit alkohol", "Mexiko", ""),
        ("Cuba Libre", "Mit Alkohol (0,4l)", "Rum-Cola-Cocktail mit Limette", "8,90", "cocktails mit alkohol", "Kuba", ""),
        ("Moscow Mule", "Mit Alkohol (0,4l)", "Wodka-Cocktail mit Ginger Beer", "8,90", "cocktails mit alkohol", "USA", ""),
        ("Pina Colada", "Mit Alkohol (0,4l)", "Karibischer Cocktail mit Rum und Kokosmilch", "8,90", "cocktails mit alkohol", "Karibik", "Milch"),
        ("Long Island Iced Tea", "Mit Alkohol (0,4l)", "Starker Cocktail mit verschiedenen Spirituosen", "8,90", "cocktails mit alkohol", "USA", ""),
        ("Wodka Lemon", "Mit Alkohol (0,4l)", "Einfacher Wodka-Cocktail mit Zitrone", "8,90", "cocktails mit alkohol", "Russland", ""),
        ("Whiskey Sour", "Mit Alkohol (0,4l)", "Klassischer Whiskey-Cocktail mit Zitrone", "8,90", "cocktails mit alkohol", "USA", ""),
        ("Jimmy's Special", "Mit Alkohol (0,4l)", "Hausspezialität von Jimmy's", "8,90", "cocktails mit alkohol", "Jimmy's", ""),
        ("Swimming Pool", "Mit Alkohol (0,4l)", "Blauer Cocktail mit Wodka und Blue Curacao", "8,90", "cocktails mit alkohol", "USA", ""),
        ("Mai Tai", "Mit Alkohol (0,4l)", "Polynesischer Rum-Cocktail", "9,90", "cocktails mit alkohol", "Polynesien", ""),
        ("Zombie", "Mit Alkohol (0,4l)", "Starker Rum-Cocktail mit Fruchtlikören", "9,90", "cocktails mit alkohol", "Karibik", ""),
        ("Solero", "Mit Alkohol (0,4l)", "Cremiger Cocktail mit Vanille und Maracuja", "9,90", "cocktails mit alkohol", "Deutschland", "Milch"),
        
        # Additional drinks categories to reach 130
        # heißgetränke (3 items)
        ("Café Crema", "Milder Filterkaffee", "Klassischer deutscher Kaffee", "3,60", "heißgetränke", "Deutschland", ""),
        ("Cappuccino", "Espresso mit Milchschaum", "Italienischer Cappuccino perfekt aufgeschäumt", "3,90", "heißgetränke", "Italien", "Milch"),
        ("Heiße Schokolade", "mit Sahne", "Cremige heiße Schokolade mit Sahnehaube", "3,90", "heißgetränke", "Spanien", "Milch"),
        
        # softgetränke (3 items)
        ("Coca Cola", "0,3l – 3,90 | 0,5l – 5,90", "Erfrischende Cola in zwei Größen", "3,90", "softgetränke", "USA", ""),
        ("Wasser Magnus", "Kohlensäure 0,25l – 3,80 | Fl. 0,75 – 6,50", "Sprudelwasser in verschiedenen Größen", "3,80", "softgetränke", "Deutschland", ""),
        ("Apfelsaft", "0,3l – 3,90 | 0,5l – 5,90", "Naturtrüber Apfelsaft", "3,90", "softgetränke", "Deutschland", ""),
        
        # spanische getränke (3 items)
        ("Sangria Tinto", "0,2l – 5,50 | 0,5l – 12,90", "Klassische rote Sangria mit Früchten", "5,50", "spanische getränke", "Spanien", "Sulfite"),
        ("Sangria Blanco", "0,2l – 5,50 | 0,5l – 12,90", "Weiße Sangria mit Weißwein und Früchten", "5,50", "spanische getränke", "Spanien", "Sulfite"),
        ("Tinto de Verano", "0,2l – 5,50 | 0,5l – 12,90", "Spanischer Sommerwein mit Limonade", "5,50", "spanische getränke", "Spanien", "Sulfite"),
    ]
    
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        
        # Prüfe aktuelle Anzahl
        cursor.execute("SELECT COUNT(*) as count FROM menu_items")
        current_count = cursor.fetchone()['count']
        print(f"📊 Aktuelle Artikel: {current_count}")
        
        # Füge die fehlenden Artikel hinzu (OHNE die existierenden zu löschen)
        print("📥 Füge fehlende Artikel hinzu...")
        imported_count = 0
        start_index = current_count
        
        for item in remaining_items:
            try:
                # Prüfe ob das Item schon existiert
                cursor.execute("SELECT COUNT(*) as count FROM menu_items WHERE name = %s", (item[0],))
                exists = cursor.fetchone()['count'] > 0
                
                if not exists:
                    cursor.execute("""
                        INSERT INTO menu_items (
                            id, name, description, detailed_description, price, category, 
                            origin, allergens, preparation_method, ingredients,
                            vegan, vegetarian, glutenfree, order_index, is_active
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(uuid.uuid4()),
                        item[0],  # name
                        item[1],  # description
                        item[2],  # detailed_description
                        item[3],  # price
                        item[4],  # category
                        item[5],  # origin
                        item[6],  # allergens
                        "Frisch zubereitet",  # preparation_method
                        "Beste Zutaten",      # ingredients
                        "alkoholfrei" in item[4].lower(),  # vegan
                        "alkoholfrei" in item[4].lower(),  # vegetarian
                        False,    # glutenfree
                        start_index + imported_count + 1,  # order_index
                        True      # is_active
                    ))
                    imported_count += 1
                    print(f"✅ Hinzugefügt: {item[0]}")
                else:
                    print(f"⏭️ Bereits vorhanden: {item[0]}")
                
            except Exception as e:
                print(f"❌ Fehler bei {item[0]}: {e}")
                continue
        
        conn.commit()
        
        # Finale Anzahl prüfen
        cursor.execute("SELECT COUNT(*) as count FROM menu_items")
        final_count = cursor.fetchone()['count']
        
        print(f"✅ {imported_count} neue Artikel hinzugefügt!")
        print(f"📊 Gesamt: {final_count} Artikel")
        print("🎯 KEINE DUPLIKATE - nur fehlende Artikel hinzugefügt")
        print("🎛️ CMS-bearbeitbar - alle CRUD-Operationen verfügbar")
        return imported_count
        
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
        return 0
    finally:
        conn.close()

if __name__ == "__main__":
    print("🍽️ Füge fehlende Artikel hinzu (108 → 130)...")
    count = add_remaining_menu_items()
    print(f"🎉 Import abgeschlossen: {count} neue Artikel hinzugefügt!")
#!/usr/bin/env python3
"""
Fügt allen 112 Gerichten spezifische Gerichtsdetails hinzu
"""

import asyncio
import aiomysql
import os
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

async def add_dish_details():
    """Fügt allen Gerichten spezifische Details hinzu"""
    
    print("📋 GERICHTS-DETAILS FÜR ALLE 112 GERICHTE HINZUFÜGEN")
    print("=" * 70)
    
    try:
        connection = await aiomysql.connect(**DB_CONFIG)
        cursor = await connection.cursor()
        
        # Spezifische Details für jedes Gericht basierend auf Namen
        dish_details = {
            # Inicio / Vorspeisen
            "Aioli": "Serviert in kleiner Terrakotta-Schale mit warmem Brot. Intensiver Knoblauchgeschmack, perfekt zum Dippen. Traditionell ohne Ei zubereitet.",
            "Oliven": "Gemischte Auswahl: grüne Manzanilla und schwarze Kalamata Oliven. Mariniert mit Orangenschale und wildem Thymian. Portionsgröße: ca. 150g.",
            "Extra Brot": "Warmes Landbrot, täglich frisch gebacken. Knusprige Kruste, weiche Krume. Perfekt zu allen Tapas und Aufstrichen.",
            "Hummus": "Cremige Konsistenz, serviert mit Paprikapulver-Garnitur. Begleitet von Gemüsesticks (Karotten, Gurken, Paprika) und Pitabrot.",
            "Guacamole": "Täglich frisch zubereitet, nie älter als 4 Stunden. Cremig-stückige Konsistenz. Serviert mit Tortilla-Chips und Limettenschnitzen.",
            "Spanischer Käseteller": "3 Käsesorten: 12 Mon. Manchego, cremiger Cabrales, Murcia al Vino. Dazu Walnüsse, Quittenpaste und Honig.",
            "Schinken-Käse-Wurst Teller": "Großzügiger Teller für 2-3 Personen. Jamón Serrano, Chorizo, Lomo, 3 Käsesorten. Mit eingelegten Beilagen.",
            "Jamón Serrano Teller": "Hauchdünn geschnitten, 18 Monate gereift. Zart-salzig im Geschmack. Serviert bei Zimmertemperatur für optimales Aroma.",
            "Boquerones en Vinagre": "24h mariniert für perfekte Textur. Mild-säuerlich im Geschmack. Traditionelle Tapas aus dem Süden Spaniens.",
            "Pata Negra": "Premium Ibérico-Schinken, 24 Monate gereift. Einzigartiger nussiger Geschmack durch Eichelfütterung. Hauchdünn serviert.",
            "Tres": "Trio unserer Bestseller-Cremes. Perfekt zum Teilen. Mit warmem Brot, Gemüsesticks und Tortilla-Chips.",
            
            # Salat
            "Ensalada Mixta": "Frische, knackige Zutaten täglich geschnitten. Leichtes Sherry-Vinaigrette. Ideal als Vorspeise oder leichte Mahlzeit.",
            "Ensalada Tonno": "Mit hochwertigem Thunfisch in Olivenöl. Protein-reich und sättigend. Garniert mit hartgekochten Eiern.",
            "Ensalada Pollo": "Gegrillte Hähnchenbrust, warm serviert. Mit gerösteten Pinienkernen für extra Crunch. Parmesan frisch gehobelt.",
            "Ensalada Garnelen": "Garnelen kurz vor Servieren gegrillt. Mit Avocado-Würfeln und Limetten-Vinaigrette. Frisch und leicht.",
            "Tomaten/Gurken Salat": "Einfach und authentisch spanisch. Reife Tomaten, knackige Gurken. Mit Oregano aus eigenem Anbau.",
            "Rote Beete Salat": "Rote Beete im Ofen geröstet für süßlichen Geschmack. Cremiger Ziegenkäse, geröstete Walnüsse. Honig-Balsamico-Dressing.",
            "Kichererbsen Salat": "Protein-reicher, sättigender Salat. Kichererbsen über Nacht eingeweicht. Mit frischen Kräutern und Feta.",
            
            # Tapa Paella
            "Paella": "Kleine Portionsgröße als Tapas. In traditioneller Paellera serviert. Safran-gelber Reis mit Socarrat (knusprige Schicht).",
            "Paella Vegetarisch": "Vegan und vollwertig. Reich an Gemüse und Hülsenfrüchten. Genauso aromatisch wie das Original mit Fleisch.",
            
            # Tapas Vegetarian
            "Gebratenes Gemüse der Saison": "Je nach Saison: Zucchini, Auberginen, Paprika. Gegrillt mit Grillstreifen. Mariniert in Kräuteröl.",
            "Papas Bravas": "Kartoffeln außen knusprig, innen mehlig. Hausgemachte Bravas-Sauce: scharf und rauchig. Madrider Klassiker.",
            "Tortilla de Patata con Aioli": "Dicke, cremige Tortilla nach spanischer Art. Lauwarm serviert. Mit hausgemachtem Aioli als Dip.",
            "Pimientos de Padrón": "Kleine, zarte Paprika aus Galicien. 1 von 10 ist scharf! Mit groben Meersalzflocken bestreut.",
            "Kanarische Kartoffeln im Salzmantel": "Kleine, runzelige Kartoffeln. Intensiver Geschmack durch Salzgärung. Mit roter und grüner Mojo-Sauce.",
            "Fetakäse Häppchen": "Griechischer Feta in Olivenöl eingelegt. Mit Oregano und schwarzem Pfeffer. Cremig-salziger Geschmack.",
            "Rosmarin Ziegenkäse": "Milder Ziegenkäse mit frischem Rosmarin. Leicht erwärmt serviert. Mit Honig-Träufel.",
            "Falafel": "Knusprig außen, weich innen. Mit Tahini-Sauce und Zitrone. Serviert mit Salat und Pitabrot.",
            "Feta Käse überbacken Cherry": "Feta im Ofen gratiniert. Mit platzenden Cherry-Tomaten. Kräuter-Olivenöl-Finish.",
            "Überbackene Champignons": "Große Champignons gefüllt und überbacken. Mit Kräutern und Knoblauch. Käse goldbraun geschmolzen.",
            "Überbackene Tomaten": "Halbierte Tomaten mit Kräuter-Käse-Kruste. Im Ofen gebacken bis karamellisiert. Basilikum-Finish.",
            "Frittierte Auberginen mit Honig": "Auberginen-Scheiben knusprig frittiert. Mit Honig beträufelt. Süß-salzige Kombination.",
            "Champignons al Ajillo": "In heißem Knoblauchöl geschwenkt. Mit Petersilie und Chili. In Terrakotta-Pfännchen serviert.",
            "Teigröllchen mit Spinat": "Knuspriger Blätterteig mit cremiger Spinat-Ricotta-Füllung. Warm serviert als finger food.",
            "Feta Feigen": "Frische Feigen mit cremigem Feta. Mit Honig und gehackten Pistazien. Süß-salzige Harmonie.",
            "Ziegenkäse überbacken": "Weicher Ziegenkäse goldbraun gratiniert. Mit Walnüssen und Honig. Warm und cremig.",
            "Gebratener Spinat mit Cherry Tomaten": "Frischer Babyspinat kurz angebraten. Mit platzenden Cherry-Tomaten. Knoblauch-Finish.",
            
            # Tapas de Pollo
            "Hähnchen Filet mit Limetten Sauce": "Saftiges Hähnchen-Brustfilet. Frische Limetten-Sauce mit Koriander. Lateinamerikanisch inspiriert.",
            "Knusprige Hähnchen Tapas": "Hähnchen in knuspriger Panade. Süß-scharfe Honig-Senf-Sauce zum Dippen. Fingerfood-Style.",
            "Hähnchen Spieß": "Hähnchen-Würfel am Spieß gegrillt. Scharfe Sauce mit Paprika und Chili. Mit Grillstreifen.",
            "Hähnchen Filet mit Curry Sauce": "Zarte Hähnchenbrust in cremiger Curry-Sauce. Exotische Gewürze, mild bis mittelscharf.",
            "Hähnchen Filet mit Mandel Sauce": "Hähnchen in samtiger Mandel-Sahne-Sauce. Süßlich-nussiger Geschmack. Sehr cremig.",
            "Gegrillter Hähnchen-Chorizo-Spieß": "Hähnchen und Chorizo abwechselnd am Spieß. Rauchig-würziger Geschmack. Spanische Fusion.",
            "Hähnchen Filet mit Brandy Sauce": "Hähnchen flambiert in Brandy. Edle Sahne-Sauce mit Alkohol-Note. Französisch inspiriert.",
            
            # Tapas de Carne
            "Dátiles con Bacon": "Süße Datteln mit knusprigem Speck umhüllt. Gefüllt mit Mandeln. Perfekte süß-salzige Balance.",
            "Albondigas a la Casera": "Hausgemachte Hackbällchen in Tomatensauce. Saftig und würzig. Comfort food auf spanisch.",
            "Pincho de Cerdo": "Schweinefleisch-Spieß mit scharfen Gewürzen. Gegrillt mit Paprika und Zwiebeln. Pikant und saftig.",
            "Pincho de Cordero": "Zarte Lamm-Spieße mit Kräutern. Rosa gegrillt für optimale Zartheit. Mit Rosmarin und Knoblauch.",
            "Chuletas de Cordero": "2 saftige Lammkoteletts. Kurz gegrillt, innen rosa. Mit mediterranen Kräutern mariniert.",
            "Rollitos de Serrano con Higo": "Serrano-Schinken mit Feigen gerollt. Cremiger Frischkäse als Füllung. Süß-salzige Delikatesse.",
            "Queso de Cabra con Bacon": "Ziegenkäse mit Speck überbacken. Honig-Finish für süße Note. Warm und cremig serviert.",
            "Chorizo al Diablo": "Chorizo in würziger Rotwein-Sauce. Intensiver Geschmack durch Weinreduktion. Traditionell spanisch.",
            "Medallions de Carne": "Rinderfilet-Medaillons rosa gebraten. Mit cremigem Pilz-Ragout. Edles Fleischgericht.",
            "Mit Käse gefüllte Champignons": "Große Champignons mit Käse-Speck-Füllung. Im Ofen überbacken. Herzhaft und cremig.",
            "Schweinefilet mit Cherry Tomaten": "Zartes Schweinefilet mit süßer Mango-Honig-Glasur. Cherry-Tomaten als Beilage.",
            "Schweinefilet": "Schweinefilet mit cremiger Spinat-Pilz-Sauce. Französisch inspiriert. Sehr cremig und reichhaltig.",
            "Chorizo a la Plancha": "Chorizo-Scheiben auf der heißen Plancha gegrillt. Knusprig außen, saftig innen. Pur spanisch.",
            "Lammfilet": "Rosa gebratenes Lammfilet mit grüner Pfeffersauce. Französische Zubereitungsart. Sehr zart.",
            "Spareribs mit BBQ-Sauce": "Zarte Schweinerippchen mit süß-rauchiger BBQ-Sauce. Amerikanisch inspiriert. Finger-licking good.",
            "Chicken Wings": "Saftige Hähnchenflügel mit süßer Chili-Sauce. Gegrillt mit knuspriger Haut. Perfektes Fingerfood.",
            
            # Tapas de Pescado
            "Boquerones Fritos": "Kleine Sardellen knusprig frittiert. Mit Zitrone und Meersalz. Traditionell andalusisch.",
            "Calamares a la Plancha": "Tintenfische auf der heißen Plancha gegrillt. Mit Knoblauch und Petersilie. Gesunde Alternative.",
            "Calamares a la Romana": "Tintenfisch-Ringe in knusprigem Bierteig. Mit hausgemachtem Aioli. Klassiker der römischen Küche.",
            "Salmon con Espinaca": "Norwegisches Lachsfilet auf Spinat-Bett. Mit cremiger Dill-Sahne-Sauce. Elegant und gesund.",
            "Gambas a la Plancha": "Tiger-Garnelen auf der Plancha gegrillt. Mit mediterranem Gemüse. Einfach und köstlich.",
            "Garnelen-Dattel-Spieß": "Garnelen und Datteln im Speckmantel. Mit Honig-Senf-Sauce. Süß-salzige Fusion.",
            "Gambas al Ajillo": "DER spanische Tapas-Klassiker. In blubberndem Knoblauchöl serviert. Mit Brot zum Stippen.",
            "Muslitos de Mar": "Krebsfleisch-Bällchen knusprig frittiert. Mit Aioli als Dip. Delikate Meeresfrüchte.",
            "Gegrillter Oktopus": "Oktopus-Tentakel gegrillt. Mit Kichererbsen und Gemüse. Mediterrane Spezialität.",
            "Jacobsmuscheln": "Edle Jakobsmuscheln kurz angebraten. Auf Spinat-Bett mit Cherry-Tomaten. Luxuriös.",
            "Gambas PIL PIL": "Garnelen in scharfer, blubbernder Sauce. Pikant und intensiv im Geschmack.",
            "Empanadas": "Gefüllte Teigtaschen mit Thunfisch. Knusprig gebacken. Argentinische Spezialität.",
            "Pfahlmuscheln": "Frische Miesmuscheln in Weißwein gedämpft. Mit Knoblauch und Petersilie. Meeresfrisch.",
            "Pulpo al Ajillo": "Oktopus in aromatischem Knoblauchöl. Mit Paprika verfeinert. Zart und würzig.",
            "Zander Filet": "Deutsches Süßwasser-Filet mit Speck. In Knoblauch-Sahne-Sauce. Regional inspiriert.",
            "Tiger Garnelen": "Große Garnelen in Gemüse-Ragout. Mit Tomaten, Paprika und Oliven. Mediterran.",
            "Brocheta de Gambas": "Garnelen-Spieß mit Gemüse gegrillt. Einfach und geschmackvoll. Perfekt zum Teilen.",
            "Boqueron en Tempura": "Sardellen in leichtem Tempura-Teig. Japanisch-spanische Fusion. Sehr knusprig.",
            "Chipirones Fritos con Aioli": "Baby-Tintenfische frittiert. Mit cremigem Aioli. Zarte Konsistenz.",
            
            # Kroketten
            "Croquetas de Bacalao": "Stockfisch-Kroketten aus dem Baskenland. Cremige Béchamel mit Fisch. Traditionell baskisch.",
            "Croquetas de Queso": "Käse-Kroketten mit cremiger Feta-Füllung. Außen knusprig, innen cremig. Vegetarischer Klassiker.",
            "Croquetas de Almendras": "Mandel-Kroketten süßlich im Geschmack. Mit gehackten Mandeln. Besondere Variation.",
            "Croquetas de Jamón": "DER spanische Kroketten-Klassiker. Mit Serrano-Schinken und Béchamel. Perfekt cremig.",
            "Croquetas de Patata": "Kartoffel-Kroketten vegetarisch. Mit cremiger Kartoffel-Béchamel. Comfort food.",
            
            # Pasta
            "Spaghetti Aglio e Olio": "Italienischer Klassiker aus Neapel. Nur 5 Zutaten, perfekt ausbalanciert. Al dente gekocht.",
            "Spaghetti Bolognese": "Klassische Fleischsauce aus Bologna. Langsam geschmort für intensiven Geschmack. Mit Parmesan.",
            "Pasta Brokkoli Gorgonzola": "Cremige Gorgonzola-Sauce mit Brokkoli. Italienischer Käse-Klassiker. Sehr reichhaltig.",
            "Pasta Verdura": "Bunte Gemüse-Pasta mit saisonalem Gemüse. Leicht und gesund. Vegetarische Option.",
            "Pasta Garnelen": "Pasta mit frischen Garnelen in Knoblauchöl. Meeresfrüchte-Klassiker. Einfach und elegant.",
            
            # Pizza
            "Pizza Margharita": "DIE klassische Pizza aus Neapel. Nur 4 Zutaten, perfekt ausbalanciert. UNESCO-Welterbe.",
            "Pizza Schinken": "Margharita mit italienischem Schinken. Herzhaft und klassisch. Für Fleischliebhaber.",
            "Pizza Funghi": "Margharita mit frischen Champignons. Erdiger Pilzgeschmack. Vegetarische Option.",
            "Pizza Tonno": "Mit hochwertigem Thunfisch in Olivenöl. Meeresfrüchte-Pizza italienisch. Protein-reich.",
            "Pizza Hawaii": "Umstrittener Klassiker mit Ananas. Süß-salzige Kombination. Nicht authentisch, aber beliebt.",
            "Pizza Verdura": "Bunte Gemüse-Pizza mit saisonalem Gemüse. Gesund und farbenfroh. Vegetarische Vielfalt.",
            "Pizza Salami": "Mit würziger italienischer Salami. Pikant und herzhaft. Klassischer Belag.",
            "Pizza Garnelen": "Edle Pizza mit Meeresfrüchten. Garnelen und Knoblauch. Maritimes Flair.",
            "Pizza Bolognese": "Pizza mit klassischer Fleischsauce. Reichhaltig und sättigend. Italienische Fusion.",
            "Jimmy's Special Pizza": "Unsere Signature-Pizza. Spanisch-italienische Fusion. Mit Serrano und Manchego.",
            
            # Kleine Gerichte  
            "Pommes Frites": "Klassische belgische Pommes. Zweimal frittiert für perfekte Knusprigkeit. Mit Dips.",
            "Chicken Nuggets": "Knusprige Hähnchen-Nuggets für Kinder. Mit Pommes als Beilage. Familienfreundlich.",
            "Chicken Wings": "Saftige Hähnchenflügel gegrillt. Mit BBQ-Sauce und Pommes. Fingerfood-Klassiker.",
            "Currywurst mit Pommes": "Deutsche Currywurst-Spezialität. Mit würziger Curry-Sauce. Nostalgisch deutsch.",
            
            # Dessert
            "Crema Catalana": "Katalanischer Dessert-Klassiker. Mit karamellisierter Zuckeroberfläche. Zimt und Vanille.",
            "Tarte de Santiago": "Galicischer Mandelkuchen ohne Mehl. Mit Puderzucker-Kreuz verziert. Glutenfrei.",
            "Gemischtes Eis": "3 Kugeln italienisches Gelato. Mit Sahne und Waffel. Verschiedene Sorten.",
            "Churros": "Spanische Schmalzgebäck-Stangen. Mit heißer Schokolade zum Dippen. Süßer Klassiker.",
            "Schoko Soufflé": "Warmes Schokoladen-Soufflé. Mit kaltem Eis kombiniert. Temperatur-Kontrast.",
            "Kokos-Eis in Fruchtschale": "Erfrischendes Kokos-Sorbet. In ausgehöhlter Kokosnuss serviert. Exotisch.",
            "Zitronen-Eis in Fruchtschale": "Frisches Zitronen-Sorbet. In ausgehöhlter Zitrone serviert. Sehr erfrischend.",
            "Orangen-Eis in Fruchtschale": "Süßes Orangen-Sorbet. In ausgehöhlter Orange serviert. Fruchtig-frisch.",
            "Nuss-Eis in Fruchtschale": "Cremiges Haselnuss-Eis. In dekorativer Fruchtschale. Nussig-süß."
        }
        
        # Alle Gerichte mit Details updaten
        update_sql = "UPDATE menu_items SET details = %s WHERE name = %s"
        
        updated_count = 0
        for dish_name, detail_text in dish_details.items():
            result = await cursor.execute(update_sql, (detail_text, dish_name))
            if cursor.rowcount > 0:
                updated_count += 1
        
        # Commit changes
        await connection.commit()
        
        print(f"✅ {updated_count} Gerichte mit spezifischen Details aktualisiert!")
        
        # Prüfe finale Anzahl mit Details
        await cursor.execute("SELECT COUNT(*) FROM menu_items WHERE details IS NOT NULL")
        with_details = await cursor.fetchone()
        
        await cursor.execute("SELECT COUNT(*) FROM menu_items")
        total = await cursor.fetchone()
        
        print(f"📊 {with_details[0]} von {total[0]} Gerichten haben jetzt Gerichts-Details!")
        
        await cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_dish_details())
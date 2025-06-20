#!/usr/bin/env python3
import requests
import json

# Authentication token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MDM3NzIwM30.D8p1wtgw_F64643TP0zkGInsvmZnoAydCpShG-liqU8"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
BASE_URL = "http://localhost:8001/api"

# Getränke mit detaillierten Beschreibungen
drinks = [
    # Heißgetränke
    {
        "name": "Café Cortado",
        "description": "Spanischer Espresso mit warmer Milch",
        "detailed_description": "Traditioneller spanischer Cortado - ein perfekt ausbalancierter Espresso mit einem Schuss warmer, leicht aufgeschäumter Milch. Serviert in einem kleinen Glas, wie es in spanischen Cafés üblich ist. Der Kaffee wird aus hochwertigen Arabica-Bohnen aus Südamerika zubereitet und die Milch wird auf genau 65°C erhitzt, um die natürliche Süße zu bewahren.",
        "price": "2,20 €",
        "category": "Heißgetränke",
        "ingredients": "Espresso, Vollmilch",
        "origin": "Spanien",
        "allergens": "Laktose",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Frisch gebrühter Espresso mit warmer Milch im Verhältnis 1:1",
        "vegetarian": True,
        "vegan": False,
        "glutenfree": True,
        "order_index": 1
    },
    {
        "name": "Café con Leche",
        "description": "Spanischer Milchkaffee",
        "detailed_description": "Der klassische spanische Milchkaffee - eine perfekte Mischung aus starkem Espresso und heißer Vollmilch im Verhältnis 1:1. Traditionell zum Frühstück getrunken, oft mit einem Stück Zucker oder einem kleinen Gebäck. Die Milch wird dampfig heiß serviert und der Kaffee ist kräftig genug, um durch die Milch zu kommen.",
        "price": "2,50 €",
        "category": "Heißgetränke", 
        "ingredients": "Espresso, Vollmilch",
        "origin": "Spanien",
        "allergens": "Laktose",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Espresso mit heißer Milch, traditionell zubereitet",
        "vegetarian": True,
        "vegan": False,
        "glutenfree": True,
        "order_index": 2
    },
    {
        "name": "Chocolate Caliente",
        "description": "Spanische heiße Schokolade",
        "detailed_description": "Traditionelle spanische heiße Schokolade - so dick, dass man Churros hinein tunken kann! Hergestellt aus echter dunkler Schokolade mit 70% Kakaoanteil, Vollmilch und einem Hauch Zimt. Diese cremige, samtweiche Schokolade ist ein echter Genuss und wird nach einem jahrhundertealten Rezept aus Madrid zubereitet.",
        "price": "3,80 €",
        "category": "Heißgetränke",
        "ingredients": "Dunkle Schokolade 70%, Vollmilch, Zucker, Maisstärke, Zimt",
        "origin": "Madrid, Spanien",
        "allergens": "Laktose, kann Spuren von Nüssen enthalten",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Langsam erhitzt und kontinuierlich gerührt bis zur perfekten Konsistenz",
        "vegetarian": True,
        "vegan": False,
        "glutenfree": True,
        "order_index": 3
    },
    
    # Tee
    {
        "name": "Manzanilla",
        "description": "Spanischer Kamillentee",
        "detailed_description": "Echter spanischer Manzanilla-Tee aus den Feldern Andalusiens. Diese besondere Kamillen-Sorte wächst nur in bestimmten Regionen Spaniens und hat einen milderen, blumigeren Geschmack als gewöhnliche Kamille. Traditionell wird er zur Beruhigung und Entspannung getrunken, besonders nach dem Essen. Aufgebrüht mit heißem Wasser bei 80°C für optimale Entfaltung der Aromen.",
        "price": "2,80 €",
        "category": "Tee",
        "ingredients": "Manzanilla-Kamillenblüten aus Andalusien",
        "origin": "Andalusien, Spanien",
        "allergens": "Keine bekannten Allergene",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "5 Minuten bei 80°C ziehen lassen",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 4
    },
    {
        "name": "Té de Hierbas",
        "description": "Spanischer Kräutertee",
        "detailed_description": "Eine aromatische Mischung traditioneller spanischer Kräuter: Thymian aus der Sierra Nevada, Rosmarin aus Katalonien, Minze aus Valencia und Zitronengras aus Murcia. Diese Mischung wird seit Generationen in spanischen Familien zur Verdauungsförderung und allgemeinen Gesundheit verwendet. Jedes Kraut wird von Hand geerntet und schonend getrocknet.",
        "price": "3,20 €",
        "category": "Tee",
        "ingredients": "Thymian, Rosmarin, Pfefferminze, Zitronengras",
        "origin": "Verschiedene Regionen Spaniens",
        "allergens": "Keine bekannten Allergene",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "7 Minuten bei 90°C ziehen lassen",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 5
    },
    
    # Softdrinks
    {
        "name": "Kas Limón",
        "description": "Spanische Zitronenlimonade",
        "detailed_description": "Die beliebte spanische Zitronenlimonade Kas Limón - ein Klassiker seit 1954! Mit echtem Zitronensaft aus Valencia hergestellt, hat sie einen erfrischend säuerlichen Geschmack ohne zu süß zu sein. Perfekt an heißen Tagen oder als Begleitung zu würzigen Tapas. Die Kohlensäure ist fein und nicht zu stark, genau wie Spanier es mögen.",
        "price": "2,50 €",
        "category": "Softdrinks",
        "ingredients": "Wasser, Zucker, Zitronensaft 10%, Kohlensäure, natürliche Aromen",
        "origin": "Valencia, Spanien",
        "allergens": "Keine bekannten Allergene",
        "additives": "Konservierungsstoff: Kaliumsorbat (E202), Antioxidans: Ascorbinsäure (E300)",
        "preparation_method": "Industriell hergestellt, gut gekühlt serviert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 6
    },
    {
        "name": "Fanta Naranja Española",
        "description": "Spanische Orangenlimonade",
        "detailed_description": "Authentische spanische Fanta Naranja - schmeckt anders als die deutsche Version! Hergestellt mit echtem Orangensaft aus spanischen Orangen, hauptsächlich aus Valencia und Andalusien. Die spanische Rezeptur ist weniger süß und hat einen intensiveren Orangengeschmack. Ein Muss für jeden Spanien-Liebhaber!",
        "price": "2,50 €",
        "category": "Softdrinks",
        "ingredients": "Wasser, Orangensaft 12%, Zucker, Kohlensäure, natürliche Orangenaromen",
        "origin": "Spanien",
        "allergens": "Keine bekannten Allergene",
        "additives": "Konservierungsstoff: Natriumbenzoat (E211), Farbstoff: Beta-Carotin (E160a)",
        "preparation_method": "Industriell hergestellt nach spanischer Rezeptur",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 7
    },
    
    # Säfte
    {
        "name": "Zumo de Naranja Natural",
        "description": "Frisch gepresster Orangensaft",
        "detailed_description": "Frisch gepresster Orangensaft aus süßen Valencia-Orangen, täglich frisch zubereitet. Die Orangen stammen direkt aus der Region Valencia und werden ohne Zusätze verarbeitet. Reich an Vitamin C und natürlichem Fruchtzucker. Wird sofort nach dem Pressen serviert, um alle Vitamine und den vollen Geschmack zu bewahren.",
        "price": "4,20 €",
        "category": "Säfte",
        "ingredients": "100% Valencia-Orangen",
        "origin": "Valencia, Spanien",
        "allergens": "Keine bekannten Allergene",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Täglich frisch gepresst, sofort serviert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 8
    },
    
    # Aperitifs
    {
        "name": "Vermouth Rojo",
        "description": "Spanischer roter Wermut",
        "detailed_description": "Traditioneller spanischer Vermouth Rojo - ein aromatisierter Wein mit über 30 Kräutern und Gewürzen. Serviert mit Eis, einer Olivenscheibe und einem Spritzer Soda. In Spanien ein beliebter Aperitif vor dem Essen. Die Rezeptur basiert auf jahrhundertealten Traditionen aus Katalonien und hat einen süßlich-bitteren Geschmack mit Noten von Wermut, Zimt und Orangen.",
        "price": "4,50 €",
        "category": "Aperitifs",
        "ingredients": "Wein, Zucker, Kräuter- und Gewürzextrakte, Alkohol",
        "origin": "Katalonien, Spanien",
        "allergens": "Sulfite",
        "additives": "Schwefeldioxid (E220)",
        "preparation_method": "Mit Eis, Olive und Soda serviert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 9
    },
    
    # Bier
    {
        "name": "Estrella Galicia",
        "description": "Galicisches Lagerbier",
        "detailed_description": "Estrella Galicia - das Bier aus dem grünen Norden Spaniens! Seit 1906 in A Coruña gebraut, ist es das beliebteste Bier Galiciens. Hergestellt nach traditioneller Rezeptur mit Hopfen aus Hallertau und spanischer Gerste. Hat einen milden, ausgewogenen Geschmack mit einer leichten Hopfenbittere. Perfekt zu Meeresfrüchten und Tapas.",
        "price": "3,20 €",
        "category": "Bier",
        "ingredients": "Wasser, Gerstenmalz, Hopfen, Hefe",
        "origin": "A Coruña, Galicien",
        "allergens": "Gluten",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Traditionell gebraut, gut gekühlt serviert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": False,
        "order_index": 10
    },
    {
        "name": "Mahou Cinco Estrellas",
        "description": "Madrider Lagerbier",
        "detailed_description": "Mahou Cinco Estrellas - das Bier der Hauptstadt! Seit 1890 in Madrid gebraut und das meistgetrunkene Bier der Region. Die fünf Sterne stehen für die fünf Qualitätskriterien: Wasser aus der Sierra de Guadarrama, ausgewähltes Malz, erlesener Hopfen, natürliche Hefe und die traditionelle Braukunst. Frisch und spritzig mit einem charakteristischen Geschmack.",
        "price": "3,20 €", 
        "category": "Bier",
        "ingredients": "Wasser, Gerstenmalz, Hopfen, Hefe",
        "origin": "Madrid, Spanien",
        "allergens": "Gluten",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Traditionell gebraut nach Madrider Art",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": False,
        "order_index": 11
    },
    
    # Weine
    {
        "name": "Rioja Tinto Joven",
        "description": "Junger Rotwein aus der Rioja",
        "detailed_description": "Ein frischer, junger Rotwein aus der berühmten Rioja-Region. Hergestellt hauptsächlich aus Tempranillo-Trauben von 20-40 Jahre alten Reben. Dieser Wein wird ohne Holzfass-Ausbau produziert, um die frischen Fruchtaromen zu bewahren. Schmeckt nach roten Beeren, Kirschen und hat eine lebendige Säure. Perfekt zu gegrilltem Fleisch und würzigen Tapas.",
        "price": "18,50 €",
        "category": "Weine",
        "ingredients": "Tempranillo-Trauben 85%, Graciano 10%, Mazuelo 5%",
        "origin": "La Rioja, Spanien",
        "allergens": "Sulfite",
        "additives": "Schwefeldioxid (E220)",
        "preparation_method": "Traditionelle Weinherstellung ohne Holzfass-Ausbau",
        "vegetarian": True,
        "vegan": False,
        "glutenfree": True,
        "order_index": 12
    },
    {
        "name": "Albariño Rías Baixas",
        "description": "Weißwein aus Galicien",
        "detailed_description": "Exquisiter Albariño aus den Rías Baixas in Galicien - einer der besten Weißweine Spaniens! Die Trauben wachsen in Meeresnähe und profitieren vom atlantischen Klima. Der Wein hat eine brillante goldgelbe Farbe und duftet nach Pfirsich, Apfel und Meeresmineral. Am Gaumen ist er frisch, elegant und hat eine ausgeprägte Mineralität. Ideal zu Meeresfrüchten und Fisch.",
        "price": "22,80 €",
        "category": "Weine",
        "ingredients": "100% Albariño-Trauben",
        "origin": "Rías Baixas, Galicien",
        "allergens": "Sulfite",
        "additives": "Schwefeldioxid (E220)",
        "preparation_method": "Kaltgärung in Edelstahltanks, sur lie Ausbau",
        "vegetarian": True,
        "vegan": False,
        "glutenfree": True,
        "order_index": 13
    },
    
    # Cocktails
    {
        "name": "Sangría Tinta",
        "description": "Klassische rote Sangría",
        "detailed_description": "Die berühmte spanische Sangría nach traditionellem Familienrezept! Basis ist ein junger Rotwein aus der Rioja, verfeinert mit frischen Orangen und Zitronen aus Valencia, einem Schuss spanischem Brandy und einem Hauch Zimt. Garniert mit frischen Früchten der Saison. Mindestens 4 Stunden ziehen gelassen für optimalen Geschmack. Perfekt für warme Abende und gesellige Runden.",
        "price": "6,80 €",
        "category": "Cocktails",
        "ingredients": "Rotwein, Orangensaft, Zitronensaft, Brandy, Zucker, Orangen, Zitronen, Zimt",
        "origin": "Traditionelles spanisches Rezept",
        "allergens": "Sulfite",
        "additives": "Schwefeldioxid (E220) im Wein",
        "preparation_method": "4 Stunden mazeriert, mit frischen Früchten garniert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 14
    },
    {
        "name": "Tinto de Verano",
        "description": "Spanischer Sommerwein",
        "detailed_description": "Der erfrischende Sommerdrink der Spanier! Viel populärer als Sangría bei den Einheimischen. Eine einfache aber geniale Mischung aus jungem Rotwein und Zitronen-Limonade oder Gaseosa, serviert mit viel Eis und einer Zitronenscheibe. Leicht, erfrischend und perfekt für heiße Sommertage. In ganz Spanien der bevorzugte Drink an Strandchiringuitos und Terrassen.",
        "price": "4,20 €",
        "category": "Cocktails",
        "ingredients": "Rotwein, Zitronen-Limonade, Zitrone",
        "origin": "Ganz Spanien",
        "allergens": "Sulfite",
        "additives": "Konservierungsstoffe in der Limonade",
        "preparation_method": "Frisch gemischt, mit viel Eis und Zitrone serviert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 15
    },
    
    # Spanische Getränke
    {
        "name": "Horchata de Chufa",
        "description": "Valencianische Erdmandelmilch",
        "detailed_description": "Authentische Horchata de Chufa aus Valencia - das traditionelle Getränk der Region! Hergestellt aus Chufas (Erdmandeln), die nur in der Region um Valencia wachsen. Die Erdmandeln werden eingeweicht, gemahlen und zu einer cremigen, süßen Milch verarbeitet. Traditionell wird sie eiskalt getrunken und oft mit Fartons (süßes Gebäck) serviert. Ein erfrischender und nahrhafter Genuss mit nussigem Geschmack.",
        "price": "3,80 €",
        "category": "Spanische Getränke",
        "ingredients": "Chufas (Erdmandeln), Wasser, Zucker, Zimt",
        "origin": "Valencia, Spanien",
        "allergens": "Kann Spuren von Nüssen enthalten",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Traditionell hergestellt, gut gekühlt serviert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 16
    },
    {
        "name": "Granizado de Limón",
        "description": "Spanisches Zitronengranita",
        "detailed_description": "Erfrischender Granizado de Limón - das perfekte Getränk für heiße Tage! Hergestellt aus frisch gepressten Zitronen aus Murcia, Wasser und Zucker, zu einem köstlichen Slush-Eis verarbeitet. Die Konsistenz ist zwischen einem Getränk und einem Eis - cremig und erfrischend zugleich. Ein Klassiker an spanischen Stränden und ein beliebter Nachmittagssnack.",
        "price": "3,50 €",
        "category": "Spanische Getränke",
        "ingredients": "Zitronensaft, Wasser, Zucker, Eis",
        "origin": "Murcia, Spanien",
        "allergens": "Keine bekannten Allergene",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Frisch zubereitet, als Slush-Eis serviert",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 17
    },
    
    # Spirituosen
    {
        "name": "Brandy de Jerez",
        "description": "Andalusischer Weinbrand",
        "detailed_description": "Edler Brandy de Jerez aus den berühmten Bodegas von Jerez de la Frontera. Hergestellt aus Weindestillat, das in alten Sherry-Fässern nach dem traditionellen Solera-System gereift ist. Diese Methode verleiht dem Brandy seinen charakteristischen Geschmack mit Noten von getrockneten Früchten, Vanille und Nüssen. Mindestens 8 Jahre gereift, wird er pur oder mit Eis als Digestif serviert.",
        "price": "7,50 €",
        "category": "Spirituosen",
        "ingredients": "Weindestillat, gereift in Sherry-Fässern",
        "origin": "Jerez de la Frontera, Andalusien",
        "allergens": "Sulfite",
        "additives": "Karamell (E150a) zur Farbgebung",
        "preparation_method": "Solera-System Reifung in Sherry-Fässern",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 18
    },
    {
        "name": "Pacharán Navarro",
        "description": "Navarrischer Schlehenlikör",
        "detailed_description": "Traditioneller Pacharán aus Navarra - der beliebteste Likör Nordspaniens! Hergestellt durch Mazeration von wilden Schlehen (Pacharán-Beeren) in Anisschnaps über mehrere Monate. Die Beeren stammen aus den Bergen Navarras und werden von Hand gesammelt. Der Likör hat eine tiefrote Farbe und einen süßlich-fruchtigen Geschmack mit einer leichten Anisnote. Wird traditionell als Digestif nach dem Essen serviert.",
        "price": "6,80 €",
        "category": "Spirituosen",
        "ingredients": "Anisschnaps, wilde Schlehen, Zucker",
        "origin": "Navarra, Spanien",
        "allergens": "Keine bekannten Allergene",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Mehrmonatige Mazeration von Schlehen in Anisschnaps",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": True,
        "order_index": 19
    }
]

def add_drink(drink):
    """Add a single drink to the menu"""
    try:
        response = requests.post(f"{BASE_URL}/menu/items", json=drink, headers=HEADERS)
        if response.status_code == 200:
            print(f"✅ Successfully added: {drink['name']} ({drink['category']})")
            return True
        else:
            print(f"❌ Failed to add {drink['name']}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error adding {drink['name']}: {e}")
        return False

def main():
    print("🍺 Adding Spanish Drinks with Detailed Descriptions")
    print("=" * 80)
    
    success_count = 0
    total_count = len(drinks)
    
    for drink in drinks:
        if add_drink(drink):
            success_count += 1
        print("-" * 40)
    
    print(f"\n📊 Summary: {success_count}/{total_count} drinks added successfully")
    
    if success_count == total_count:
        print("🎉 All Spanish drinks added with detailed descriptions!")
    else:
        print(f"⚠️ {total_count - success_count} drinks failed to add")

if __name__ == "__main__":
    main()
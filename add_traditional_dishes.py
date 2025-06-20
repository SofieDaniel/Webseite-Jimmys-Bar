#!/usr/bin/env python3
import requests
import json

# Authentication token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MDQ1NTgwM30.8dKqfq2WRgtT-NR0i1qy-zSkV_x3SlyxmR7ukhDcrEc"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
BASE_URL = "http://localhost:8001/api"

# Traditional Spanish dishes with very detailed descriptions
dishes = [
    {
        "name": "Paella Valenciana",
        "description": "Traditionelle valencianische Paella mit Huhn und Kaninchen",
        "detailed_description": "Die ursprüngliche Paella aus der Region Valencia, zubereitet nach dem authentischen Rezept der Valencianer Bauern. Mit safrangewürztem Bomba-Reis, zartem Huhn und Kaninchen, grünen Bohnen, Garrofón-Bohnen und Paprika. In der traditionellen Paellera über Orangenholz gekocht für das charakteristische Socarrat - die leicht angeröstete Reiskruste am Boden. Ein UNESCO-geschütztes kulinarisches Erbe.",
        "price": "22,90 €",
        "category": "Tapa Paella",
        "ingredients": "Bomba-Reis, Safran, Hähnchen, Kaninchen, grüne Bohnen, Garrofón-Bohnen, Paprika, Rosmarin, Olivenöl, Salz",
        "origin": "Valencia, Spanien",
        "allergens": "Kann Spuren von Schalentieren enthalten",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "In Paellera über Orangenholz gekocht",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": True,
        "order_index": 1
    },
    {
        "name": "Paella de Mariscos",
        "description": "Meeresfrüchte-Paella aus dem Mittelmeer",
        "detailed_description": "Exquisite Meeresfrüchte-Paella mit frischen Garnelen, Muscheln, Tintenfisch und Seeteufel aus dem Mittelmeer. Der Bomba-Reis wird mit einem intensiven Fischfond und echtem Safran aus La Mancha zubereitet. Die Meeresfrüchte werden separat vorbereitet und erst zum Schluss hinzugefügt, um ihre zarte Textur zu bewahren. Garniert mit Zitronenschnitzen und frischer Petersilie.",
        "price": "26,90 €",
        "category": "Tapa Paella",
        "ingredients": "Bomba-Reis, Safran, Garnelen, Miesmuscheln, Tintenfisch, Seeteufel, Fischfond, Olivenöl, Knoblauch, Zitrone, Petersilie",
        "origin": "Küstenregionen Spaniens",
        "allergens": "Schalentiere, Weichtiere, Fisch",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Traditionelle Paella-Technik mit separater Meeresfrüchte-Zubereitung",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": True,
        "order_index": 2
    },
    {
        "name": "Gazpacho Andaluz",
        "description": "Kalte Tomatensuppe aus Andalusien",
        "detailed_description": "Erfrischende kalte Suppe aus reifen andalusischen Tomaten, verfeinert mit Gurken, grüner Paprika, Zwiebeln und Knoblauch. Mit hochwertigem Sherry-Essig und nativem Olivenöl extra aus Jaén emulgiert. Traditionell wird sie mit kleinen Würfeln von Brot, Gurke, Tomate und hartgekochtem Ei serviert. Perfect für heiße Sommertage - ein echter Gazpacho sollte eiskalt serviert werden.",
        "price": "8,90 €",
        "category": "Inicio / Vorspeisen",
        "ingredients": "Reife Tomaten, Gurken, grüne Paprika, Zwiebeln, Knoblauch, Weißbrot, Sherry-Essig, Olivenöl extra virgin, Meersalz",
        "origin": "Andalusien, Spanien",
        "allergens": "Gluten",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Traditionell püriert und durch ein feines Sieb passiert, über Nacht gekühlt",
        "vegetarian": True,
        "vegan": True,
        "glutenfree": False,
        "order_index": 3
    },
    {
        "name": "Salmorejo Cordobés",
        "description": "Cremige kalte Tomaten-Brotsuppe aus Córdoba",
        "detailed_description": "Dickflüssige Spezialität aus Córdoba, die dem Gazpacho ähnelt, aber viel cremiger ist. Hergestellt aus sonnengereiften Tomaten, Weißbrot von gestern, Knoblauch und bestem Olivenöl aus der Subbética. Die Konsistenz ist samtiger als Gazpacho, da mehr Brot verwendet wird. Traditionell garniert mit fein gehackten hartgekochten Eiern und knusprigen Serrano-Schinken-Würfeln. Ein Sommergericht par excellence aus dem Herzen Andalusiens.",
        "price": "9,50 €",
        "category": "Inicio / Vorspeisen",
        "ingredients": "Reife Tomaten, Weißbrot, Knoblauch, Olivenöl extra virgin, Sherry-Essig, Meersalz, hartgekochte Eier, Serrano-Schinken",
        "origin": "Córdoba, Andalusien",
        "allergens": "Gluten, Ei, Konservierungsstoff",
        "additives": "Konservierungsstoff: Natriumnitrit (E250) im Schinken",
        "preparation_method": "24 Stunden gekühlt, fein püriert bis zur samtigen Konsistenz",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": False,
        "order_index": 4
    },
    {
        "name": "Jamón Ibérico de Bellota",
        "description": "Premium Eichel-Schinken vom Ibérico-Schwein",
        "detailed_description": "Der König der spanischen Schinken - von freilaufenden iberischen Schwarzfuß-Schweinen aus der Dehesa Extremaduras. Die Tiere ernähren sich in der Montanera-Saison (Oktober-Februar) ausschließlich von Eicheln der Steineichen, was dem Fleisch seinen einzigartigen nussigen Geschmack und die marmorierten Fettadern verleiht. 36 Monate in den Bergen von Guijuelo gereift. Hauchdünn von Hand geschnitten und bei Zimmertemperatur serviert. Ein wahres Juwel der spanischen Gastronomie.",
        "price": "16,90 €",
        "category": "Inicio / Vorspeisen",
        "ingredients": "Ibérico-Schweinekeule (100% Bellota), Meersalz aus Cádiz, Eicheln der Steineichen",
        "origin": "Dehesa Extremadura, Guijuelo",
        "allergens": "Kann Spuren von Nüssen enthalten durch Eichelfütterung",
        "additives": "Konservierungsstoff: Natriumnitrit (E250)",
        "preparation_method": "36 Monate luftgetrocknet in Berghöhlen, Eichel-Montanera",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": True,
        "order_index": 5
    },
    {
        "name": "Arroz con Pollo",
        "description": "Traditioneller spanischer Hühner-Reis",
        "detailed_description": "Klassisches spanisches Reisgericht aus Valencia, das vor der berühmten Paella existierte. Bomba-Reis wird mit zartem Huhn, Safran und einer aromatischen Sofrito aus Tomaten, Zwiebeln und Paprika gekocht. Anders als Paella wird dieser Reis cremiger zubereitet, ähnlich einem Risotto. Mit grünen Erbsen, roten Paprikastreifen und Rosmarin verfeinert. Ein comfort food, das in jeder spanischen Familie unterschiedlich zubereitet wird.",
        "price": "16,90 €",
        "category": "Tapa Paella",
        "ingredients": "Bomba-Reis, Hähnchen, Safran, Sofrito (Tomaten, Zwiebeln, Paprika), grüne Erbsen, Hühnerbrühe, Olivenöl, Rosmarin",
        "origin": "Valencia und Murcia, Spanien",
        "allergens": "Kann Spuren von Gluten enthalten",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Langsam geschmort in flacher Paellera, cremiger als Paella",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": True,
        "order_index": 6
    },
    {
        "name": "Pulpo a la Gallega",
        "description": "Galicischer Oktopus mit Paprika und Olivenöl",
        "detailed_description": "Das berühmteste Gericht Galiciens - perfekt gekochter Oktopus nach traditioneller Art. Der Oktopus wird dreimal in kochendes Wasser getaucht (um die Haut nicht platzen zu lassen), dann langsam gegart bis er butterweich ist. Auf warmen Holztellern serviert, geschnitten in mundgerechte Stücke und bestreut mit grobem Meersalz, geröstetem Paprikapulver (Pimentón dulce) und bestem galicischen Olivenöl. Dazu werden traditionell gekochte Kartoffeln gereicht.",
        "price": "18,90 €",
        "category": "Tapas de Pescado",
        "ingredients": "Oktopus, gekochte Kartoffeln, grobes Meersalz, Pimentón dulce (geröstetes Paprikapulver), Olivenöl extra virgin",
        "origin": "Galicien, Spanien",
        "allergens": "Weichtiere",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Traditionelle galicische Drei-Tauch-Methode, auf Holzteller serviert",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": True,
        "order_index": 7
    },
    {
        "name": "Migas Extremeñas",
        "description": "Geröstete Brotkrumen nach Art der Extremadura",
        "detailed_description": "Traditionelles Hirtengericht aus der Extremadura, entstanden als Weg, altbackenes Brot zu verwerten. Weißbrotwürfel werden mit Knoblauch, Paprikapulver und bestem Olivenöl langsam geröstet bis sie goldbraun und knusprig sind. Traditionell mit Chorizo, Speck und Weintrauben serviert - die süßen Trauben bilden einen perfekten Kontrast zu den herzhaften Zutaten. Früher das Frühstück der Schafhirten, heute ein gefeiertes Gericht der spanischen Küche.",
        "price": "12,90 €",
        "category": "Tapas de Carne",
        "ingredients": "Altbackenes Weißbrot, Knoblauch, Pimentón dulce, Olivenöl, Chorizo, Speck, Weintrauben, Petersilie",
        "origin": "Extremadura, Spanien",
        "allergens": "Gluten, Konservierungsstoff",
        "additives": "Konservierungsstoff: Natriumnitrit (E250) in Fleischprodukten",
        "preparation_method": "Langsam geröstet in schwerem Eisentopf, traditionelle Hirten-Art",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": False,
        "order_index": 8
    },
    {
        "name": "Fabada Asturiana",
        "description": "Asturischer Bohneneintopf mit Morcilla und Chorizo",
        "detailed_description": "Der berühmte Bohneneintopf aus Asturien mit großen weißen Fabes-Bohnen von außergewöhnlicher Cremigkeit. Langsam geschmort mit Morcilla (asturische Blutwurst), Chorizo, Speck und Schulter vom Schwein. Die Fabes-Bohnen sind so zart, dass sie auf der Zunge zergehen. Das Geheimnis liegt im langsamen Kochen bei niedriger Temperatur ohne Umrühren. Traditionell an regnerischen Tagen serviert, ist es pure comfort food aus dem grünen Norden Spaniens.",
        "price": "14,90 €",
        "category": "Tapas de Carne",
        "ingredients": "Fabes-Bohnen (asturische weiße Bohnen), Morcilla asturiana, Chorizo, Speck, Schweinebacke, Zwiebeln, Knoblauch, Lorbeer, Safran",
        "origin": "Asturien, Spanien",
        "allergens": "Konservierungsstoff, kann Spuren von Gluten enthalten",
        "additives": "Konservierungsstoff: Natriumnitrit (E250) in Fleischprodukten",
        "preparation_method": "Langsam geschmort ohne Umrühren, traditionelle asturische Art",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": True,
        "order_index": 9
    },
    {
        "name": "Caldereta de Langosta",
        "description": "Menorquinischer Langusteneintopf",
        "detailed_description": "Luxuriöser Eintopf von den Balearen mit frischen Langusten aus dem Mittelmeer. Die Langusten werden mit Zwiebeln, Tomaten, Paprika und einem Schuss Brandy geschmort. Das Besondere: Die Schalen werden mitgekocht, um dem Eintopf eine intensive Meerestiefe zu verleihen. Mit Safran, Knoblauch und einem Picada (Mandel-Petersilien-Paste) verfeinert. Serviert mit knusprigem Pa amb Tomàquet (Tomatenbrot). Ein Festtagsgericht von den Inseln.",
        "price": "32,90 €",
        "category": "Tapas de Pescado",
        "ingredients": "Langusten, Zwiebeln, reife Tomaten, rote Paprika, Brandy, Safran, Knoblauch, Mandeln, Petersilie, Olivenöl, Weißwein",
        "origin": "Menorca, Balearen",
        "allergens": "Krebstiere, Nüsse",
        "additives": "Keine Zusatzstoffe",
        "preparation_method": "Traditionell menorquinisch, Schalen mitgeschmort für Tiefe",
        "vegetarian": False,
        "vegan": False,
        "glutenfree": True,
        "order_index": 10
    }
]

def add_dish(dish):
    """Add a single dish to the menu"""
    try:
        response = requests.post(f"{BASE_URL}/menu/items", json=dish, headers=HEADERS)
        if response.status_code == 200:
            print(f"✅ Successfully added: {dish['name']}")
            return True
        else:
            print(f"❌ Failed to add {dish['name']}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error adding {dish['name']}: {e}")
        return False

def main():
    print("🍽️ Adding Traditional Spanish Dishes with Detailed Descriptions")
    print("=" * 80)
    
    success_count = 0
    total_count = len(dishes)
    
    for dish in dishes:
        if add_dish(dish):
            success_count += 1
        print("-" * 40)
    
    print(f"\n📊 Summary: {success_count}/{total_count} dishes added successfully")
    
    if success_count == total_count:
        print("🎉 All traditional Spanish dishes added with detailed descriptions!")
    else:
        print(f"⚠️ {total_count - success_count} dishes failed to add")

if __name__ == "__main__":
    main()
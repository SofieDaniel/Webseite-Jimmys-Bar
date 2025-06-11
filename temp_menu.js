const Speisekarte = () => {
  const [selectedCategory, setSelectedCategory] = useState('alle');
  
  // Complete menu data with authentic images for hover display (Screenshot Style)
  const menuItems = {
    'inicio': [
      { name: 'Aioli', description: 'Hausgemachte Knoblauch-Mayonnaise', price: '3,50', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', details: 'Hausgemachte, cremige Knoblauch-Mayonnaise nach traditionellem valencianischem Rezept. Zubereitet mit frischem Knoblauch aus Spanien, nativem Olivenöl extra aus Andalusien und Zitronensaft. Serviert mit ofentrischem, spanischem Weißbrot. Perfekt zum Einstieg in einen mediterranen Abend.' },
      { name: 'Oliven', description: 'Marinierte spanische Oliven', price: '3,90', image: 'https://images.unsplash.com/photo-1714583357992-98f0ad946902', details: 'Ausgewählte schwarze Arbequina-Oliven aus Katalonien und grüne Manzanilla-Oliven aus Sevilla, mariniert mit wildem Thymian, rosa Pfefferkörnern, Knoblauch und bestem Olivenöl extra vergine. 24 Stunden eingelegt für optimalen Geschmack.' },
      { name: 'Extra Brot', description: 'Frisches spanisches Brot', price: '1,90', image: 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73', details: 'Warmes, knuspriges Pan de Pueblo nach traditionellem kastilischem Rezept. Täglich frisch gebacken mit Steinofenmehl aus der Region Castilla y León, Meersalz und natürlicher Hefe. Perfekt für Tapas und Dips.' },
      { name: 'Hummus', description: 'Cremiger Kichererbsen-Dip', price: '3,90', image: 'https://images.unsplash.com/photo-1571197119738-26123cb0d22f', details: 'Hausgemachter Hummus aus Kichererbsen (Garbanzo-Bohnen) aus Kastilien, Tahini aus Sesam, Zitrone und Kreuzkümmel. Nach mediterraner Tradition zubereitet. Serviert mit frischem Gemüse und warmem Brot.' },
      { name: 'Spanischer Käseteller', description: 'Auswahl spanischer Käsesorten', price: '8,90', image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d', details: 'Edle Auswahl aus der Mancha: Manchego D.O.P. (12 Monate gereift), Cabrales D.O.P. aus Asturien (Blauschimmelkäse) und Murcia al Vino aus Murcia (in Rotwein gereift). Serviert mit Walnüssen aus Kalifornien, Akazienhonig und frischen Moscatel-Trauben.' },
      { name: 'Schinken-Käse-Wurst Teller', description: 'Spanische Charcuterie-Platte', price: '11,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', details: 'Edle Auswahl aus Jamón Serrano, Chorizo, Lomo und spanischen Käsesorten mit Oliven, Nüssen und Feigenmarmelade.' },
      { name: 'Jamón Serrano Teller', description: 'Hochwertiger spanischer Schinken', price: '9,90', image: 'https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg', details: '18 Monate gereifter Jamón Serrano D.O. aus den Bergen der Sierra Nevada, hauchdünn geschnitten. Serviert mit 12 Monate gereiftem Manchego-Käse D.O.P. und geröstetem Brot aus Kastilien. Von freilaufenden iberischen Schweinen.' },
      { name: 'Pata Negra', description: 'Premium Iberico Schinken', price: '10,90', image: 'https://images.unsplash.com/photo-1598989519542-077da0f51c09', details: 'Der Edelste aller spanischen Schinken - Jamón Ibérico de Bellota D.O.P. aus Extremadura, 36 Monate gereift. Von schwarzfüßigen Iberico-Schweinen, die sich ausschließlich von Eicheln ernähren. Serviert mit Manchego Reserva und Tomaten-Brot.' },
      { name: 'Tres (Hummus, Avocado Cream, Aioli mit Brot)', description: 'Drei köstliche Dips mit Brot', price: '10,90', image: 'https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg', details: 'Trio aus hausgemachtem Hummus, cremiger Avocado-Creme und Aioli, serviert mit warmem spanischem Brot und Gemüse.' }
    ],
    'salat': [
      { name: 'Ensalada Mixta', description: 'Gemischter Salat mit spanischen Zutaten', price: '8,90', details: 'Frischer Salat mit Tomaten, Gurken, Oliven, roten Zwiebeln und Manchego-Käse in Sherry-Vinaigrette.' },
      { name: 'Ensalada Tonno', description: 'Salat mit Thunfisch', price: '14,90', details: 'Gemischter Salat mit saftigem Thunfisch, hartgekochten Eiern, Oliven und Kapern in mediteraner Vinaigrette.' },
      { name: 'Ensalada Pollo', description: 'Salat mit gegrilltem Hähnchen', price: '14,90', details: 'Frischer Salat mit gegrillten Hähnchenstreifen, Cherrytomaten, Avocado und gerösteten Pinienkernen.' },
      { name: 'Ensalada Garnelen', description: 'Salat mit frischen Garnelen', price: '15,90', details: 'Bunter Salat mit saftigen Garnelen, Avocado, Mango und einem Hauch von Chili in Limetten-Dressing.' }
    ],
    'kleiner-salat': [
      { name: 'Tomaten/Gurken mit Zwiebeln', description: 'Frischer Gemüsesalat', price: '6,90', details: 'Saftige Tomaten und knackige Gurken mit roten Zwiebeln in aromatischem Olivenöl und Kräutern.' },
      { name: 'Rote Beete mit Ziegenkäse', description: 'Süße rote Beete mit cremigem Ziegenkäse', price: '7,90', details: 'Geröstete rote Beete mit cremigem Ziegenkäse, Walnüssen und Honig-Thymian-Dressing.' },
      { name: 'Kichererbsen mit Feta', description: 'Proteinreicher Salat mit Feta', price: '7,90', details: 'Warme Kichererbsen mit Feta-Käse, frischen Kräutern, Tomaten und Zitronendressing.' }
    ],
    'tapa-paella': [
      { name: 'Paella mit Hähnchen & Meeresfrüchten', description: 'Traditionelle spanische Paella als Tapa-Portion', price: '8,90', details: 'Authentische Paella mit saftigem Hähnchen, frischen Garnelen, Muscheln und Bomba-Reis in würziger Safran-Brühe.' },
      { name: 'Paella vegetarisch', description: 'Vegetarische Paella mit frischem Gemüse', price: '7,90', details: 'Vegetarische Paella mit grünen Bohnen, Paprika, Artischocken und Bomba-Reis in aromatischer Gemüsebrühe.' }
    ],
    'tapas-vegetarian': [
      { name: 'Gebratenes Gemüse', description: 'Vegan - Saisonales Gemüse mediterran gewürzt', price: '6,90', vegan: true, glutenfree: true, details: 'Frisches Saisongemüse wie Zucchini, Paprika und Auberginen, gegrillt mit Rosmarin, Thymian und Olivenöl.' },
      { name: 'Papas Bravas', description: 'Vegan - Klassische spanische Kartoffeln mit scharfer Soße', price: '6,90', vegan: true, glutenfree: true, details: 'Knusprig gebratene Kartoffelwürfel aus der Region Galicia mit pikanter Bravas-Sauce aus San Marzano-Tomaten, geröstetem Paprikapulver aus Murcia (Pimentón de la Vera D.O.P.) und einem Hauch Cayenne-Chili. Original Madrider Rezept.' },
      { name: 'Tortilla de Patata mit Aioli', description: 'Spanisches Kartoffel-Omelett mit Aioli', price: '6,90', vegetarian: true, glutenfree: true, details: 'Klassische spanische Tortilla aus Kartoffeln der Region Castilla y León und frischen Eiern, golden gebraten nach traditionellem Rezept aus Madrid. Serviert mit hausgemachtem Aioli aus bestem andalusischem Olivenöl.' },
      { name: 'Pimientos de Padrón', description: 'Vegan - Gebratene grüne Paprika', price: '6,90', vegan: true, glutenfree: true, details: 'Original Pimientos de Padrón D.O.P. aus Galicien - kleine grüne Paprikaschoten, gebraten in nativem Olivenöl extra aus Jaén und mit Flor de Sal (Meersalz) aus Cádiz bestreut. Traditionell: manche scharf, manche mild!' },
      { name: 'Kanarische Kartoffeln', description: 'Vegan - Traditionelle Kartoffeln mit Meersalz', price: '6,90', vegan: true, glutenfree: true, details: 'Papas Arrugadas - kleine Kartoffeln aus Teneriffa in der Schale gekocht mit grobem Atlantik-Meersalz. Serviert mit grüner Mojo Verde (Koriander, Petersilie) und roter Mojo Rojo (geröstete Paprika) aus den Kanarischen Inseln.' },
      { name: 'Fetahäppchen auf Johannisbeersauce', description: 'Cremiger Feta mit süß-saurer Sauce', price: '6,90', details: 'Warme Feta-Würfel auf einer Reduktion aus roten Johannisbeeren mit einem Hauch Balsamico und frischen Kräutern.' },
      { name: 'Ziegenkäse auf Johannisbeersauce oder Honig-Senf', description: 'Mild-cremiger Ziegenkäse mit Sauce nach Wahl', price: '6,90', details: 'Warmer Ziegenkäse wahlweise mit süßer Johannisbeersauce oder würzigem Honig-Senf-Dressing und gerösteten Nüssen.' },
      { name: 'Falafel mit Joghurt-Minz-Sauce', description: 'Knusprige Kichererbsenbällchen mit erfrischender Sauce', price: '6,90', details: 'Hausgemachte Falafel aus Kichererbsen und orientalischen Gewürzen, serviert mit cremiger Joghurt-Minz-Sauce.' },
      { name: 'Überbackener Feta mit Cherrytomaten', description: 'Warmer Feta mit süßen Cherrytomaten', price: '6,90', details: 'Feta-Käse überbacken mit Cherrytomaten, Oliven, Oregano und einem Schuss Olivenöl, serviert mit frischem Brot.' },
      { name: 'Champignons mit Reis & Pinienkernen auf Roquefort', description: 'Aromatische Pilze mit würzigem Käse', price: '6,90', details: 'Gefüllte Champignons mit Reis, gerösteten Pinienkernen und würzigem Roquefort-Käse, überbacken und mit Kräutern garniert.' },
      { name: 'Überbackene Tomaten mit Spinat & Roquefort', description: 'Mediterrane Gemüse-Käse-Kombination', price: '6,90', details: 'Große Tomaten gefüllt mit frischem Spinat und würzigem Roquefort, überbacken und mit Basilikum garniert.' },
      { name: 'Frittierte Auberginen mit Honig', description: 'Süß-herzhafte Auberginen-Kreation', price: '6,90', details: 'Auberginenscheiben in leichtem Teig frittiert, mit spanischem Honig glasiert und mit frischen Kräutern garniert.' },
      { name: 'Champignons al Ajillo', description: 'Vegan - Pilze in Knoblauchöl', price: '6,90', details: 'Frische Champignons geschmort in Knoblauchöl mit Petersilie, Chili und einem Schuss Weißwein - ein Klassiker!' },
      { name: 'Teigtaschen mit Spinat & Kräutersauce', description: 'Hausgemachte Teigtaschen mit frischen Kräutern', price: '6,90', details: 'Hausgemachte Teigtaschen gefüllt mit Spinat und Ricotta, serviert mit einer cremigen Kräutersauce.' },
      { name: 'Feta Feigen', description: 'Süße Feigen mit salzigem Feta', price: '6,90', details: 'Frische Feigen gefüllt mit cremigem Feta-Käse, gerösteten Walnüssen und einem Hauch Honig.' },
      { name: 'Ziegenkäse auf Fenchel & Walnuss', description: 'Aromatische Kombination mit Nüssen', price: '6,90', details: 'Warmer Ziegenkäse auf einem Bett aus geröstetem Fenchel mit gerösteten Walnüssen und Honig-Balsamico-Glasur.' },
      { name: 'Gebratener Spinat mit Cherrytomaten', description: 'Vegan - Frischer Spinat mit süßen Tomaten', price: '6,90', details: 'Frischer Spinat geschmort mit Cherrytomaten, Knoblauch und Pinienkernen in bestem Olivenöl.' }
    ],
    'tapas-pollo': [
      { name: 'Hähnchen mit Limetten-Sauce', description: 'Zartes Hähnchen in frischer Zitrus-Sauce', price: '7,20', details: 'Saftige Hähnchenstücke in einer frischen Limetten-Sauce mit Koriander und einem Hauch Chili, serviert mit Kräuterreis.' },
      { name: 'Knuspriges Hähnchen mit Honig-Senf', description: 'Goldbraun gebratenes Hähnchen mit süß-scharfer Sauce', price: '7,20', details: 'Knusprig paniertes Hähnchen mit hausgemachter Honig-Senf-Sauce, garniert mit frischen Kräutern.' },
      { name: 'Hähnchenspieß mit Chili', description: 'Würziger Hähnchen-Spieß mit Chili', price: '7,20', details: 'Marinierte Hähnchenstücke am Spieß mit pikanter Chili-Sauce und gegrilltem Gemüse.' },
      { name: 'Hähnchen mit Curry', description: 'Exotisch gewürztes Hähnchen', price: '7,20', details: 'Zart geschmortes Hähnchen in aromatischer Curry-Sauce mit Kokosmilch und mediterranen Gewürzen.' },
      { name: 'Hähnchen mit Mandelsauce', description: 'Cremige Mandel-Sauce zu zartem Hähnchen', price: '7,20', details: 'Gebratenes Hähnchen in feiner Mandel-Sahne-Sauce mit gerösteten Mandelblättchen.' },
      { name: 'Hähnchen-Chorizo-Spieß', description: 'Spanische Wurst-Fleisch-Kombination', price: '7,20', details: 'Abwechselnd Hähnchen und würzige Chorizo am Spieß gegrillt, serviert mit Paprika und Zwiebeln.' },
      { name: 'Hähnchen mit Brandy-Sauce', description: 'Edle Brandy-Sauce zu saftigem Hähnchen', price: '7,20', details: 'Gebratenes Hähnchen in einer cremigen Sauce aus spanischem Brandy, Sahne und feinen Gewürzen.' }
    ],
    'tapas-carne': [
      { name: 'Dátiles con Bacon', description: 'Süße Datteln mit knusprigem Speck', price: '6,90', details: 'Saftige Datteln gefüllt mit Mandeln, umwickelt mit knusprigem Bacon und im Ofen gebacken.' },
      { name: 'Albondigas', description: 'Spanische Hackfleischbällchen in Tomatensoße', price: '6,90', details: 'Hausgemachte Fleischbällchen nach traditionellem Rezept in würziger Tomatensoße mit frischen Kräutern.' },
      { name: 'Pincho de Cerdo', description: 'Schweinefleisch-Spieß gegrillt', price: '7,90', details: 'Marinierte Schweinefleischstücke am Spieß mit Paprika und Zwiebeln, serviert mit Aioli.' },
      { name: 'Pincho de Cordero', description: 'Lammfleisch-Spieß mit Kräutern', price: '8,90', details: 'Zarte Lammfleischstücke am Spieß mit mediterranen Kräutern und Knoblauch mariniert.' },
      { name: 'Chuletas de Cordero', description: 'Gegrillte Lammkoteletts', price: '9,90', details: 'Saftige Lammkoteletts vom Grill mit Rosmarin und Thymian, serviert mit Knoblauchöl.' },
      { name: 'Rollitos Serrano mit Feige', description: 'Serrano-Schinken-Röllchen mit süßer Feige', price: '9,90', details: 'Hauchdünner Serrano-Schinken gefüllt mit süßen Feigen und Ziegenkäse.' },
      { name: 'Ziegenkäse mit Bacon', description: 'Cremiger Ziegenkäse mit knusprigem Speck', price: '7,90', details: 'Warmer Ziegenkäse in knusprigem Bacon eingewickelt, mit Honig und Pinienkernen.' },
      { name: 'Chorizo al Diablo', description: 'Scharfe Chorizo in Teufelssauce', price: '7,90', details: 'Gegrillte Chorizo in pikanter Sauce mit Rotwein und scharfen Chilischoten.' },
      { name: 'Medaillons vom Schwein', description: 'Zarte Schweinefilet-Medaillons', price: '9,90', details: 'Rosa gebratene Schweinefilet-Medaillons mit Sherrysoße und karamellisierten Zwiebeln.' },
      { name: 'Champignons mit Käse', description: 'Überbackene Pilze mit geschmolzenem Käse', price: '8,90', details: 'Frische Champignons gefüllt mit Serrano-Schinken und Käse überbacken.' },
      { name: 'Schweinefilet mit Cherrytomaten', description: 'Saftiges Filet mit süßen Tomaten', price: '9,50', details: 'Gebratenes Schweinefilet mit geschmorten Cherrytomaten und Basilikum.' },
      { name: 'Schweinefilet in Sauce', description: 'Zartes Filet in aromatischer Sauce', price: '9,50', details: 'Schweinefilet in cremiger Pilz-Sahne-Sauce mit frischen Kräutern.' },
      { name: 'Chorizo a la Plancha', description: 'Gegrillte spanische Wurst', price: '7,90', details: 'Traditionelle spanische Chorizo vom Grill mit Paprika und Zwiebeln.' },
      { name: 'Lammfilet', description: 'Premium Lammfilet rosa gebraten', price: '9,90', details: 'Zartes Lammfilet rosa gebraten mit Rosmarin-Knoblauch-Öl und Thymianjus.' },
      { name: 'Spareribs mit BBQ', description: 'Zarte Rippchen mit BBQ-Sauce', price: '8,90', details: 'Geschmorte Spareribs in hausgemachter BBQ-Sauce mit spanischen Gewürzen.' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', details: 'Knusprige Chicken Wings mariniert in pikanter Sauce mit Knoblauch und Kräutern.' }
    ],
    'tapas-pescado': [
      { name: 'Boquerones Fritos', description: 'Frittierte Sardellen', price: '7,50', details: 'Frisch frittierte Sardellen in knuspriger Panade mit Zitrone und hausgemachter Aioli.' },
      { name: 'Calamares a la Plancha', description: 'Gegrillte Tintenfischringe', price: '8,90', details: 'Zart gegrillte Tintenfischringe mit Knoblauch, Petersilie und Zitrone.' },
      { name: 'Calamares a la Romana', description: 'Panierte Tintenfischringe', price: '7,50', details: 'Knusprig panierte Tintenfischringe serviert mit Zitrone und Aioli.' },
      { name: 'Lachs mit Spinat', description: 'Frischer Lachs auf Spinatbett', price: '9,90', details: 'Gebratenes Lachsfilet auf cremigem Blattspinat mit Knoblauch und Pinienkernen.' },
      { name: 'Gambas a la Plancha', description: 'Gegrillte Garnelen', price: '9,90', details: 'Große Garnelen vom Grill mit Meersalz und Knoblauchöl.' },
      { name: 'Garnelen-Dattel-Spieß', description: 'Süß-salzige Kombination am Spieß', price: '9,90', details: 'Garnelen und süße Datteln am Spieß mit Speck umwickelt.' },
      { name: 'Gambas al Ajillo', description: 'Garnelen in Knoblauchöl', price: '9,90', glutenfree: true, details: 'In bestem andalusischem Olivenöl extra vergine gebratene Garnelen aus Huelva mit frischem Knoblauch aus Las Pedroñeras (Cuenca), scharfem Guindilla-Chili aus dem Baskenland und frischer Petersilie. Ein Klassiker aus den Marisquerías von Cádiz, traditionell in der Cazuela de Barro (Tonschale) serviert.' },
      { name: 'Muslitos de Mar', description: 'Gebackene Muscheln', price: '6,90', details: 'Gratinierte Miesmuscheln mit Knoblauch-Kräuter-Kruste.' },
      { name: 'Gegrillter Oktopus', description: 'Zarter Oktopus vom Grill', price: '9,90', details: 'Gegrillter Oktopus mit Paprikapulver, Olivenöl und Meersalz.' },
      { name: 'Jacobsmuscheln', description: 'Edle Jakobsmuscheln gegrillt', price: '9,90', details: 'Gegrillte Jakobsmuscheln mit Knoblauchbutter und Petersilie.' },
      { name: 'Gambas PIL PIL', description: 'Garnelen in würzigem Olivenöl', price: '9,90', details: 'Garnelen in scharfem Olivenöl mit Knoblauch und Cayennepfeffer.' },
      { name: 'Empanadas', description: 'Spanische Teigtaschen mit Füllung', price: '6,90', details: 'Hausgemachte Teigtaschen gefüllt mit Thunfisch und Tomaten.' },
      { name: 'Pfahlmuscheln', description: 'Frische Miesmuscheln in Sud', price: '8,90', details: 'Miesmuscheln in Weißwein-Knoblauch-Sud mit frischen Kräutern.' },
      { name: 'Pulpo al Ajillo', description: 'Oktopus in Knoblauchöl', price: '9,90', details: 'Zarter Oktopus in Knoblauchöl mit Paprikapulver und Petersilie.' },
      { name: 'Zanderfilet', description: 'Zartes Zanderfilet gebraten', price: '9,90', details: 'Gebratenes Zanderfilet mit Zitronenbutter und mediterranem Gemüse.' },
      { name: 'Tiger Garnelen', description: 'Große Tiger-Garnelen gegrillt', price: '9,90', details: 'Gegrillte Tiger-Garnelen mit Knoblauch-Limetten-Butter.' },
      { name: 'Brocheta de Gambas', description: 'Garnelen-Spieß mit Gemüse', price: '8,90', details: 'Garnelen-Spieß mit Paprika und Zwiebeln vom Grill.' },
      { name: 'Boqueron in Tempura', description: 'Sardellen im Tempura-Teig', price: '7,50', details: 'Sardellen im leichten Tempura-Teig mit Zitronen-Aioli.' },
      { name: 'Chipirones', description: 'Baby-Tintenfische gegrillt', price: '8,90', details: 'Gegrillte Baby-Tintenfische mit Knoblauch und Petersilie.' }
    ],
    'kroketten': [
      { name: 'Bacalao', description: 'Stockfisch-Kroketten', price: '5,90', details: 'Cremige Kroketten aus Stockfisch und Kartoffeln, traditionell zubereitet.' },
      { name: 'Käse', description: 'Cremige Käse-Kroketten', price: '5,90', details: 'Hausgemachte Kroketten mit einer Füllung aus spanischen Käsesorten.' },
      { name: 'Mandeln', description: 'Mandel-Kroketten mit feinem Aroma', price: '6,50', details: 'Süße Kroketten aus gemahlenen Mandeln mit Honig und Zimt.' },
      { name: 'Jamón', description: 'Schinken-Kroketten klassisch', price: '5,90', details: 'Traditionelle Kroketten mit feiner Serrano-Schinken-Füllung.' },
      { name: 'Kartoffel', description: 'Traditionelle Kartoffel-Kroketten', price: '5,50', details: 'Klassische Kartoffelkroketten mit Kräutern und Gewürzen.' }
    ],
    'pasta': [
      { name: 'Spaghetti Aglio e Olio', description: 'Klassisch mit Knoblauch und Olivenöl', price: '12,90', details: 'Al dente gekochte Spaghetti mit bestem Olivenöl, frischem Knoblauch und Peperoncini.' },
      { name: 'Spaghetti Bolognese', description: 'Mit hausgemachter Fleischsauce', price: '14,90', details: 'Traditionelle Bolognese-Sauce mit Rinderhack, langsam geschmort mit Rotwein und Kräutern.' },
      { name: 'Pasta Brokkoli Gorgonzola', description: 'Cremige Gorgonzola-Sauce mit Brokkoli', price: '14,90', details: 'Frischer Brokkoli in cremiger Gorgonzola-Sauce mit gerösteten Pinienkernen.' },
      { name: 'Pasta Verdura', description: 'Mit frischem Saisongemüse', price: '14,90', details: 'Mediterranes Gemüse der Saison mit Olivenöl und frischen Kräutern.' },
      { name: 'Pasta Garnelen', description: 'Mit frischen Garnelen und Knoblauch', price: '16,90', details: 'Saftige Garnelen in Knoblauch-Weißwein-Sauce mit Kirschtomaten und Basilikum.' }
    ],
    'pizza': [
      { name: 'Margherita', description: 'Tomaten, Mozzarella, Basilikum', price: '9,90', details: 'Klassische Pizza mit hausgemachter Tomatensauce, frischem Mozzarella und Basilikum.' },
      { name: 'Schinken', description: 'Mit spanischem Schinken', price: '12,90', details: 'Pizza mit Serrano-Schinken, Mozzarella und frischen Rucola.' },
      { name: 'Funghi', description: 'Mit frischen Champignons', price: '12,90', details: 'Pizza mit sautierten Champignons, Mozzarella und frischen Kräutern.' },
      { name: 'Tonno', description: 'Mit Thunfisch und Zwiebeln', price: '13,90', details: 'Pizza mit Thunfisch, roten Zwiebeln, Kapern und schwarzen Oliven.' },
      { name: 'Hawaii', description: 'Mit Schinken und Ananas', price: '13,90', details: 'Pizza mit gekochtem Schinken, frischer Ananas und extra Käse.' },
      { name: 'Verdura', description: 'Mit gegrilltem Gemüse', price: '13,90', details: 'Pizza mit verschiedenem Grillgemüse, Mozzarella und Basilikumpesto.' },
      { name: 'Salami', description: 'Mit würziger Salami', price: '12,90', details: 'Pizza mit italienischer Salami, Mozzarella und frischen Kräutern.' },
      { name: 'Garnelen', description: 'Mit frischen Garnelen', price: '15,90', details: 'Pizza mit Garnelen, Knoblauch, Cherrytomaten und Rucola.' },
      { name: 'Bolognese', description: 'Mit Hackfleischsauce', price: '13,90', details: 'Pizza mit hausgemachter Bolognese-Sauce und extra Käse.' },
      { name: "Jimmy's Special", description: 'Unsere Haus-Spezial-Pizza', price: '13,90', details: 'Geheimrezept des Hauses mit ausgewählten spanischen Zutaten.' }
    ],
    'snacks': [
      { name: 'Pommes', description: 'Goldgelbe Kartoffel-Pommes', price: '5,50', details: 'Knusprige Pommes frites mit hausgemachten Dips nach Wahl.' },
      { name: 'Chicken Nuggets', description: 'Knusprige Hähnchen-Nuggets', price: '8,90', details: 'Hausgemachte Chicken Nuggets aus frischem Hähnchenfilet mit verschiedenen Dips.' },
      { name: 'Chicken Wings', description: 'Würzige Hähnchenflügel', price: '9,90', details: 'Marinierte und knusprig gebratene Chicken Wings mit BBQ-Sauce.' },
      { name: 'Currywurst', description: 'Deutsche Currywurst klassisch', price: '10,90', details: 'Klassische Currywurst mit hausgemachter Sauce und Pommes frites.' }
    ],
    'dessert': [
      { name: 'Crema Catalana', description: 'Katalanische Crème brûlée', price: '5,50', details: 'Traditionelle spanische Crème brûlée mit karamellisierter Zuckerkruste.' },
      { name: 'Tarte de Santiago', description: 'Spanischer Mandelkuchen', price: '7,50', details: 'Klassischer spanischer Mandelkuchen nach Originalrezept aus Galizien.' },
      { name: 'Eis', description: 'Hausgemachtes Eis nach Wahl', price: '6,90', details: 'Verschiedene Sorten hausgemachtes Eis mit frischen Früchten.' },
      { name: 'Churros mit Schokolade', description: 'Spanisches Spritzgebäck mit warmer Schokolade', price: '6,90', details: 'Frisch zubereitete Churros mit heißer Schokoladensauce zum Dippen.' },
      { name: 'Schoko Soufflé', description: 'Warmes Schokoladen-Soufflé', price: '7,50', details: 'Warmes Schokoladen-Soufflé mit flüssigem Kern und Vanilleeis.' }
    ],
    'helados': [
      { name: 'Kokos', description: 'Eis im Fruchtschälchen - Kokos', price: '6,90', details: 'Cremiges Kokoseis serviert in einer echten Kokosnussschale mit Kokosflocken.' },
      { name: 'Zitrone', description: 'Eis im Fruchtschälchen - Zitrone', price: '6,90', details: 'Erfrischendes Zitronensorbet in einer ausgehöhlten Zitrone serviert.' },
      { name: 'Orange', description: 'Eis im Fruchtschälchen - Orange', price: '6,90', details: 'Fruchtiges Orangensorbet in einer halbierten Orange präsentiert.' },
      { name: 'Nuss', description: 'Eis im Fruchtschälchen - Nuss', price: '6,90', details: 'Nusseis mit karamellisierten Nüssen in einer Kokosschale serviert.' }
    ]
  };

  const categories = [
    { id: 'alle', name: 'Alle Kategorien' },
    { id: 'inicio', name: 'Inicio' },
    { id: 'salat', name: 'Salat' },
    { id: 'kleiner-salat', name: 'Kleiner Salat' },
    { id: 'tapa-paella', name: 'Tapa Paella' },
    { id: 'tapas-vegetarian', name: 'Tapas Vegetarian' },
    { id: 'tapas-pollo', name: 'Tapas de Pollo' },
    { id: 'tapas-carne', name: 'Tapas de Carne' },
    { id: 'tapas-pescado', name: 'Tapas de Pescado' },
    { id: 'kroketten', name: 'Kroketten' },
    { id: 'pasta', name: 'Pasta' },
    { id: 'pizza', name: 'Pizza' },
    { id: 'snacks', name: 'Snacks' },
    { id: 'dessert', name: 'Dessert' },
    { id: 'helados', name: 'Helados' }
  ];

  const getDisplayItems = () => {
    if (selectedCategory === 'alle') {
      return Object.entries(menuItems).flatMap(([category, items]) => 
        items.map(item => ({ ...item, category }))
      );
    }
    return menuItems[selectedCategory]?.map(item => ({ ...item, category: selectedCategory })) || [];
  };

  return (
    <div className="min-h-screen speisekarte-background" style={{position: 'relative', zIndex: 0}}>
      {/* Elegant Header Section with Background Image */}
      <div className="relative bg-cover bg-center" style={{backgroundImage: `url('https://images.pexels.com/photos/24706530/pexels-photo-24706530.jpeg')`}}>
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-6xl font-serif text-warm-beige mb-4 tracking-wide drop-shadow-text">
              Speisekarte
            </h1>
            <p className="text-xl text-light-beige font-light tracking-wide drop-shadow-text">
              Authentische spanische Küche - Bewegen Sie die Maus über Gerichte für Bildvorschau
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12" style={{position: 'relative', zIndex: 1}}>        
        {/* Category Filter Buttons - No Icons */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`menu-category px-6 py-3 rounded-lg transition-all duration-300 font-light tracking-wide text-sm ${
                selectedCategory === category.id
                  ? 'bg-warm-beige text-dark-brown shadow-lg'
                  : 'border border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown hover:shadow-lg'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items - Screenshot Style Two-Column Layout with Hover Info */}
        <div className="grid md:grid-cols-2 gap-6 max-w-7xl mx-auto" style={{position: 'relative', zIndex: 1}}>
          {getDisplayItems().map((item, index) => (
            <div key={index} className="menu-item rounded-lg p-6 hover:bg-medium-brown transition-all duration-300 relative group">
              <div className="flex justify-between items-start">
                {/* Dish name and description */}
                <div className="flex-1 pr-4">
                  <h3 className="text-xl font-serif text-warm-beige mb-2 tracking-wide">
                    {item.name}
                    {item.vegan && <span className="ml-2 text-green-400 text-sm">🌱</span>}
                    {item.vegetarian && <span className="ml-2 text-green-300 text-sm">🥬</span>}
                    {item.glutenfree && <span className="ml-2 text-yellow-400 text-sm">GF</span>}
                  </h3>
                  <p className="text-light-beige mb-2 font-light leading-relaxed text-sm">{item.description}</p>
                  <span className="text-xs text-warm-beige capitalize font-light tracking-wide opacity-75">
                    {categories.find(c => c.id === item.category)?.name}
                  </span>
                </div>
                
                {/* Price - Right aligned like in screenshot */}
                <div className="text-2xl font-serif text-warm-beige tracking-wide flex-shrink-0">
                  {item.price} €
                </div>
              </div>
              
              {/* Enhanced Hover Details Popup - Only text without images - ALWAYS ON TOP */}
              <div className="menu-image-tooltip">
                <div className="tooltip-content bg-dark-brown border-2 border-warm-beige rounded-lg p-6 max-w-md">
                  <h4 className="text-lg font-serif text-warm-beige mb-3">{item.name}</h4>
                  <p className="text-light-beige text-sm mb-3 leading-relaxed">{item.details}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-warm-beige opacity-75">
                      {categories.find(c => c.id === item.category)?.name}
                    </span>
                    <span className="text-xl font-serif text-warm-beige">{item.price} €</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Menu Footer */}
        <div className="text-center mt-16 p-8 bg-dark-brown rounded-lg border border-warm-brown">
          <h3 className="text-2xl font-serif text-warm-beige mb-4">Allergien und Unverträglichkeiten</h3>
          <p className="text-light-beige font-light leading-relaxed max-w-3xl mx-auto mb-4">
            Bitte informieren Sie uns über eventuelle Allergien oder Unverträglichkeiten. 
            Unsere Küche berücksichtigt gerne Ihre individuellen Bedürfnisse.
          </p>
          <div className="flex flex-wrap justify-center gap-6 text-sm">
            <span className="flex items-center text-light-beige">
              <span className="text-green-400 text-lg mr-2">🌱</span>
              Vegan
            </span>
            <span className="flex items-center text-light-beige">
              <span className="text-green-300 text-lg mr-2">🥬</span>
              Vegetarisch
            </span>
            <span className="flex items-center text-light-beige">
              <span className="text-yellow-400 text-sm font-bold mr-2">GF</span>
              Glutenfrei
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Enhanced Locations Page Component

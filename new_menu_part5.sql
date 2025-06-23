USE jimmys_tapas_bar;

-- 15. Säfte/Nektar (0,3 l/0,5 l)
INSERT INTO menu_items (id, name, description, detailed_description, price, category, allergens, ingredients, vegan, vegetarian, glutenfree, order_index, is_active) VALUES
('saft001', 'Apfelsaft 0,3l', 'Naturtrüb', 'Naturtrüber Apfelsaft aus deutschen Äpfeln.', '3,90', 'Säfte', '', 'Apfelsaft naturtrüb', true, true, true, 1, true),
('saft002', 'Apfelsaft 0,5l', 'Naturtrüb', 'Naturtrüber Apfelsaft aus deutschen Äpfeln.', '5,90', 'Säfte', '', 'Apfelsaft naturtrüb', true, true, true, 2, true),
('saft003', 'Rhabarbersaft 0,3l', 'Fruchtig-sauer', 'Erfrischender Rhabarbersaft mit natürlicher Säure.', '3,90', 'Säfte', '', 'Rhabarbersaft', true, true, true, 3, true),
('saft004', 'Rhabarbersaft 0,5l', 'Fruchtig-sauer', 'Erfrischender Rhabarbersaft mit natürlicher Säure.', '5,90', 'Säfte', '', 'Rhabarbersaft', true, true, true, 4, true),
('saft005', 'KiBa 0,3l', 'Kirsch-Banane', 'Klassische Mischung aus Kirsch- und Bananensaft.', '3,90', 'Säfte', '', 'Kirschsaft, Bananennektar', true, true, true, 5, true),
('saft006', 'KiBa 0,5l', 'Kirsch-Banane', 'Klassische Mischung aus Kirsch- und Bananensaft.', '5,90', 'Säfte', '', 'Kirschsaft, Bananennektar', true, true, true, 6, true),
('saft007', 'Maracujasaft 0,3l', 'Exotisch', 'Exotischer Maracujasaft mit intensivem Aroma.', '3,90', 'Säfte', '', 'Maracujasaft', true, true, true, 7, true),
('saft008', 'Maracujasaft 0,5l', 'Exotisch', 'Exotischer Maracujasaft mit intensivem Aroma.', '5,90', 'Säfte', '', 'Maracujasaft', true, true, true, 8, true),
('saft009', 'Mangosaft 0,3l', 'Tropisch', 'Süßer tropischer Mangosaft.', '3,90', 'Säfte', '', 'Mangosaft', true, true, true, 9, true),
('saft010', 'Mangosaft 0,5l', 'Tropisch', 'Süßer tropischer Mangosaft.', '5,90', 'Säfte', '', 'Mangosaft', true, true, true, 10, true),
('saft011', 'Cranberrysaft 0,3l', 'Herb-fruchtig', 'Herb-fruchtiger Cranberrysaft, reich an Vitaminen.', '3,90', 'Säfte', '', 'Cranberrysaft', true, true, true, 11, true),
('saft012', 'Cranberrysaft 0,5l', 'Herb-fruchtig', 'Herb-fruchtiger Cranberrysaft, reich an Vitaminen.', '5,90', 'Säfte', '', 'Cranberrysaft', true, true, true, 12, true),

-- Schorlen
('schorle001', 'Apfelschorle 0,3l', 'Mit Mineralwasser', 'Apfelsaft gemischt mit frischem Mineralwasser.', '3,20', 'Schorlen', '', 'Apfelsaft, Mineralwasser', true, true, true, 1, true),
('schorle002', 'Apfelschorle 0,5l', 'Mit Mineralwasser', 'Apfelsaft gemischt mit frischem Mineralwasser.', '4,90', 'Schorlen', '', 'Apfelsaft, Mineralwasser', true, true, true, 2, true),
('schorle003', 'Rhabarberschorle 0,3l', 'Mit Mineralwasser', 'Rhabarbersaft gemischt mit Mineralwasser.', '3,20', 'Schorlen', '', 'Rhabarbersaft, Mineralwasser', true, true, true, 3, true),
('schorle004', 'Rhabarberschorle 0,5l', 'Mit Mineralwasser', 'Rhabarbersaft gemischt mit Mineralwasser.', '4,90', 'Schorlen', '', 'Rhabarbersaft, Mineralwasser', true, true, true, 4, true),
('schorle005', 'KiBa-Schorle 0,3l', 'Mit Mineralwasser', 'Kirsch-Bananen-Saft mit Mineralwasser.', '3,20', 'Schorlen', '', 'Kirschsaft, Bananennektar, Mineralwasser', true, true, true, 5, true),
('schorle006', 'KiBa-Schorle 0,5l', 'Mit Mineralwasser', 'Kirsch-Bananen-Saft mit Mineralwasser.', '4,90', 'Schorlen', '', 'Kirschsaft, Bananennektar, Mineralwasser', true, true, true, 6, true),
('schorle007', 'Maracuja-Schorle 0,3l', 'Mit Mineralwasser', 'Maracujasaft mit frischem Mineralwasser.', '3,20', 'Schorlen', '', 'Maracujasaft, Mineralwasser', true, true, true, 7, true),
('schorle008', 'Maracuja-Schorle 0,5l', 'Mit Mineralwasser', 'Maracujasaft mit frischem Mineralwasser.', '4,90', 'Schorlen', '', 'Maracujasaft, Mineralwasser', true, true, true, 8, true),
('schorle009', 'Mango-Schorle 0,3l', 'Mit Mineralwasser', 'Mangosaft mit erfrischendem Mineralwasser.', '3,20', 'Schorlen', '', 'Mangosaft, Mineralwasser', true, true, true, 9, true),
('schorle010', 'Mango-Schorle 0,5l', 'Mit Mineralwasser', 'Mangosaft mit erfrischendem Mineralwasser.', '4,90', 'Schorlen', '', 'Mangosaft, Mineralwasser', true, true, true, 10, true),
('schorle011', 'Cranberry-Schorle 0,3l', 'Mit Mineralwasser', 'Cranberrysaft mit Mineralwasser.', '3,20', 'Schorlen', '', 'Cranberrysaft, Mineralwasser', true, true, true, 11, true),
('schorle012', 'Cranberry-Schorle 0,5l', 'Mit Mineralwasser', 'Cranberrysaft mit Mineralwasser.', '4,90', 'Schorlen', '', 'Cranberrysaft, Mineralwasser', true, true, true, 12, true),

-- 16. Aperitifs & Bier
('ap001', 'Sekt auf Eis', 'Deutscher Sekt', 'Gekühlter deutscher Sekt auf Eis mit Zitronenzeste.', '7,50', 'Aperitifs', '', 'Deutscher Sekt, Eis, Zitrone', true, true, true, 1, true),
('ap002', 'Aperol Spritz', 'Italienischer Klassiker', 'Aperol mit Prosecco und Soda, serviert mit Orange.', '7,50', 'Aperitifs', '', 'Aperol, Prosecco, Soda, Orange', true, true, true, 2, true),
('ap003', 'Hugo', 'Österreichischer Cocktail', 'Prosecco mit Holunderblüten-Sirup, Minze und Limette.', '7,50', 'Aperitifs', '', 'Prosecco, Holunderblüten-Sirup, Minze, Limette', true, true, true, 3, true),
('ap004', 'Lillet Wild Berry', 'Französischer Aperitif', 'Lillet Blanc mit Beeren und Tonic Water.', '7,50', 'Aperitifs', '', 'Lillet Blanc, Beeren, Tonic Water', true, true, true, 4, true),
('ap005', 'Campari Soda', 'Italienisch herb', 'Campari mit Soda Water und Eis, garniert mit Orange.', '7,50', 'Aperitifs', '', 'Campari, Soda Water, Orange', true, true, true, 5, true),
('ap006', 'Martini Rosso 4cl', 'Süßer Wermut', 'Martini Rosso pur oder auf Eis.', '7,50', 'Aperitifs', '', 'Martini Rosso', true, true, true, 6, true),
('ap007', 'Martini Bianco 4cl', 'Weißer Wermut', 'Martini Bianco pur oder auf Eis.', '7,50', 'Aperitifs', '', 'Martini Bianco', true, true, true, 7, true),
('ap008', 'Mango-Spritz', 'Exotisch', 'Prosecco mit Mango-Püree und frischer Minze.', '7,50', 'Aperitifs', '', 'Prosecco, Mango-Püree, Minze, Limette', true, true, true, 8, true),

-- Bier vom Fass
('bier001', 'Carlsberg Bier 0,3l', 'Dänisches Pils', 'Frisches Carlsberg Pils vom Fass.', '3,90', 'Bier', '', 'Carlsberg Bier', true, true, true, 1, true),
('bier002', 'Carlsberg Bier 0,5l', 'Dänisches Pils', 'Frisches Carlsberg Pils vom Fass.', '5,50', 'Bier', '', 'Carlsberg Bier', true, true, true, 2, true),
('bier003', 'Alster Wasser 0,3l', 'Bier-Limonade-Mix', 'Erfrischende Mischung aus Bier und Limonade.', '3,90', 'Bier', '', 'Bier, Limonade', true, true, true, 3, true),
('bier004', 'Alster Wasser 0,5l', 'Bier-Limonade-Mix', 'Erfrischende Mischung aus Bier und Limonade.', '5,50', 'Bier', '', 'Bier, Limonade', true, true, true, 4, true),
('bier005', 'Duckstein dunkel 0,3l', 'Dunkles Bier', 'Würziges dunkles Bier mit malzigem Geschmack.', '4,20', 'Bier', '', 'Duckstein dunkel', true, true, true, 5, true),
('bier006', 'Duckstein dunkel 0,5l', 'Dunkles Bier', 'Würziges dunkles Bier mit malzigem Geschmack.', '5,90', 'Bier', '', 'Duckstein dunkel', true, true, true, 6, true),

-- Flaschenbier
('bier007', 'Estrella Galicia Fl.', 'Spanisches Bier', 'Authentisches spanisches Bier aus Galicien.', '3,90', 'Bier', '', 'Estrella Galicia', true, true, true, 7, true),
('bier008', 'San Miguel Fl.', 'Spanisches Bier', 'Beliebtes spanisches Bier mit mildem Geschmack.', '3,90', 'Bier', '', 'San Miguel', true, true, true, 8, true),
('bier009', 'Erdinger Weißbier alkoholfrei Fl.', 'Alkoholfrei', 'Alkoholfreies Weißbier mit vollem Geschmack.', '3,90', 'Bier', '', 'Erdinger Weißbier alkoholfrei', true, true, true, 9, true),
('bier010', 'Lübzer alkoholfrei Fl.', 'Alkoholfrei', 'Alkoholfreies Pils aus Mecklenburg.', '3,90', 'Bier', '', 'Lübzer alkoholfrei', true, true, true, 10, true),
('bier011', 'Grevensteiner Original Fl.', 'Deutsches Pils', 'Traditionelles deutsches Pils aus dem Sauerland.', '3,90', 'Bier', '', 'Grevensteiner Original', true, true, true, 11, true),
('bier012', 'Erdinger Weißbier 0,5l', 'Bayerisches Weißbier', 'Traditionelles bayerisches Weißbier mit Hefe.', '5,50', 'Bier', '', 'Erdinger Weißbier', true, true, true, 12, true),

-- 17. Weine & Spirituosen
('wein001', 'Offener Weißwein 0,2l', 'Diverse Sorten', 'Wechselnde Auswahl an Weißweinen aus verschiedenen Regionen.', '7,50', 'Weine', '', 'Weißwein', true, true, true, 1, true),
('wein002', 'Offener Weißwein 0,5l', 'Diverse Sorten', 'Wechselnde Auswahl an Weißweinen aus verschiedenen Regionen.', '17,90', 'Weine', '', 'Weißwein', true, true, true, 2, true),
('wein003', 'Offener Weißwein 0,7l', 'Diverse Sorten', 'Wechselnde Auswahl an Weißweinen aus verschiedenen Regionen.', '25,90', 'Weine', '', 'Weißwein', true, true, true, 3, true),
('wein004', 'Offener Roséwein 0,2l', 'Diverse Sorten', 'Frische Roséweine aus verschiedenen Weinregionen.', '7,50', 'Weine', '', 'Roséwein', true, true, true, 4, true),
('wein005', 'Offener Roséwein 0,5l', 'Diverse Sorten', 'Frische Roséweine aus verschiedenen Weinregionen.', '17,90', 'Weine', '', 'Roséwein', true, true, true, 5, true),
('wein006', 'Offener Roséwein 0,7l', 'Diverse Sorten', 'Frische Roséweine aus verschiedenen Weinregionen.', '25,90', 'Weine', '', 'Roséwein', true, true, true, 6, true),
('wein007', 'Offener Rotwein 0,2l', 'Diverse Sorten', 'Kräftige Rotweine aus verschiedenen Anbaugebieten.', '7,50', 'Weine', '', 'Rotwein', true, true, true, 7, true),
('wein008', 'Offener Rotwein 0,5l', 'Diverse Sorten', 'Kräftige Rotweine aus verschiedenen Anbaugebieten.', '17,90', 'Weine', '', 'Rotwein', true, true, true, 8, true),
('wein009', 'Offener Rotwein 0,7l', 'Diverse Sorten', 'Kräftige Rotweine aus verschiedenen Anbaugebieten.', '25,90', 'Weine', '', 'Rotwein', true, true, true, 9, true),

-- Vino de la Casa
('wein010', 'Vino de la Casa Schorle 0,2l', 'Hauswein-Schorle', 'Unser Hauswein als erfrischende Schorle.', '6,90', 'Weine', '', 'Hauswein, Mineralwasser', true, true, true, 10, true),
('wein011', 'Vino de la Casa Schorle 0,5l', 'Hauswein-Schorle', 'Unser Hauswein als erfrischende Schorle.', '15,90', 'Weine', '', 'Hauswein, Mineralwasser', true, true, true, 11, true),
('wein012', 'Vino de la Casa Weiß 0,2l', 'Hauswein', 'Unser Hauswein weiß, trocken und fruchtig.', '6,90', 'Weine', '', 'Weißwein (Hauswein)', true, true, true, 12, true),
('wein013', 'Vino de la Casa Weiß 0,5l', 'Hauswein', 'Unser Hauswein weiß, trocken und fruchtig.', '15,90', 'Weine', '', 'Weißwein (Hauswein)', true, true, true, 13, true),
('wein014', 'Vino de la Casa Tinto 0,2l', 'Hauswein rot', 'Unser Hauswein rot, trocken und vollmundig.', '6,90', 'Weine', '', 'Rotwein (Hauswein)', true, true, true, 14, true),
('wein015', 'Vino de la Casa Tinto 0,5l', 'Hauswein rot', 'Unser Hauswein rot, trocken und vollmundig.', '6,90', 'Weine', '', 'Rotwein (Hauswein)', true, true, true, 15, true),
('wein016', 'Vino de la Casa Rosé 0,2l', 'Hauswein rosé', 'Unser Hauswein rosé, frisch und fruchtig.', '6,90', 'Weine', '', 'Roséwein (Hauswein)', true, true, true, 16, true),
('wein017', 'Vino de la Casa Rosé 0,5l', 'Hauswein rosé', 'Unser Hauswein rosé, frisch und fruchtig.', '15,90', 'Weine', '', 'Roséwein (Hauswein)', true, true, true, 17, true),

-- Flaschenweine
('wein018', 'Grauburgunder 0,7l', 'Deutsche Qualität', 'Eleganter deutscher Grauburgunder, trocken ausgebaut.', '34,90', 'Weine', '', 'Grauburgunder', true, true, true, 18, true),
('wein019', 'Portada 0,7l', 'Spanischer Wein', 'Spanischer Qualitätswein aus der Rioja-Region.', '34,90', 'Weine', '', 'Portada Rioja', true, true, true, 19, true),
('wein020', 'Luis Canas 0,7l', 'Rioja Crianza', 'Spanischer Rotwein aus der Rioja mit 12 Monaten Barrique.', '34,90', 'Weine', '', 'Luis Canas Rioja Crianza', true, true, true, 20, true),
('wein021', 'Cano 0,7l', 'Spanischer Tempranillo', 'Vollmundiger spanischer Rotwein aus Tempranillo-Trauben.', '34,90', 'Weine', '', 'Cano Tempranillo', true, true, true, 21, true),
('wein022', 'Pata Negra 0,7l', 'Premium Rioja', 'Hochwertiger spanischer Rotwein aus der Rioja.', '34,90', 'Weine', '', 'Pata Negra Rioja', true, true, true, 22, true),
('wein023', 'Finca Sobreno 0,7l', 'Spanischer Rotwein', 'Kräftiger spanischer Rotwein mit intensivem Aroma.', '34,90', 'Weine', '', 'Finca Sobreno', true, true, true, 23, true),
('wein024', 'Exklusiver Flaschenwein', 'Premium Auswahl', 'Wechselnde Auswahl exklusiver Weine aus besonderen Jahrgängen.', '49,90', 'Weine', '', 'Premium Wein (wechselnd)', true, true, true, 24, true);
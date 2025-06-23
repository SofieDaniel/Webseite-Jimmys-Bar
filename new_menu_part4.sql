USE jimmys_tapas_bar;

-- 11. Für den kleinen und großen Hunger
INSERT INTO menu_items (id, name, description, detailed_description, price, category, allergens, ingredients, vegan, vegetarian, glutenfree, order_index, is_active) VALUES
('h001', 'Pommes Frites', 'Mit Ketchup/Mayonnaise', 'Goldgelbe, knusprige Pommes Frites serviert mit Ketchup und Mayonnaise.', '5,50', 'Snacks', 'Eier', 'Kartoffeln, Olivenöl, Ketchup, Mayonnaise, Salz', false, true, true, 1, true),
('h002', 'Chicken Nuggets', '5 Stück, Pommes', 'Fünf knusprige Chicken Nuggets mit Pommes Frites und Dip-Sauce.', '8,90', 'Snacks', 'Glutenhaltiges Getreide, Eier', 'Hähnchenfilet, Paniermehl, Kartoffeln, Eier, Gewürze', false, false, false, 2, true),
('h003', 'Chicken Wings', '5 Stück, Pommes', 'Fünf würzige Chicken Wings mit Pommes Frites und BBQ-Sauce.', '9,90', 'Snacks', 'Eier', 'Chicken Wings, Kartoffeln, BBQ-Sauce, Gewürze', false, false, true, 3, true),
('h004', 'Currywurst mit Pommes', 'Deutsche Spezialität', 'Bratwurst mit Curry-Ketchup-Sauce und knusprigen Pommes Frites.', '10,90', 'Snacks', 'Glutenhaltiges Getreide, Eier', 'Bratwurst, Curry-Ketchup, Kartoffeln, Zwiebeln', false, false, false, 4, true),

-- 12. Dessert & Eis
('d001', 'Crema Catalana', 'Spanische Crème brûlée', 'Traditionelle katalanische Creme mit karamellisierter Zuckerkruste und Zimt.', '5,50', 'Dessert', 'Milch, Eier', 'Milch, Sahne, Eigelb, Zucker, Zimt, Zitronenschale', false, true, true, 1, true),
('d002', 'Tarte de Santiago', 'Spanischer Mandelkuchen', 'Traditioneller galicischer Mandelkuchen mit Puderzucker und Santiago-Kreuz.', '7,50', 'Dessert', 'Schalenfrüchte, Eier, Glutenhaltiges Getreide', 'Mandeln, Eier, Zucker, Mehl, Zitronenschale', false, true, false, 2, true),
('d003', 'Gemischtes Eis', '3 Kugeln, Sahne', 'Drei Kugeln Eis nach Wahl mit Schlagsahne und Waffel.', '6,90', 'Dessert', 'Milch, Eier, Glutenhaltiges Getreide', 'Speiseeis, Sahne, Waffel', false, true, false, 3, true),
('d004', 'Churros', 'Mit Schokolade', 'Traditionelle spanische Churros mit warmer Schokoladen-Sauce zum Dippen.', '6,90', 'Dessert', 'Glutenhaltiges Getreide, Milch, Eier', 'Mehl, Eier, Butter, Zucker, Schokolade, Zimt', false, true, false, 4, true),
('d005', 'Schoko Soufflé', 'Eis, Sahne', 'Warmes Schokoladen-Soufflé mit Vanille-Eis und Schlagsahne.', '7,50', 'Dessert', 'Milch, Eier, Glutenhaltiges Getreide', 'Schokolade, Eier, Mehl, Butter, Vanille-Eis, Sahne', false, true, false, 5, true),
('d006', 'Kokos-Eis in Fruchtschale', 'Helados', 'Cremiges Kokos-Eis serviert in einer frischen Kokosnuss-Schale.', '6,90', 'Dessert', 'Milch', 'Kokosmilch, Sahne, Zucker, Kokosnuss-Schale', false, true, true, 6, true),
('d007', 'Zitronen-Eis in Fruchtschale', 'Helados', 'Erfrischendes Zitronen-Eis serviert in einer ausgehöhlten Zitrone.', '6,90', 'Dessert', 'Milch', 'Zitronensaft, Sahne, Zucker, Zitronenschale', false, true, true, 7, true),
('d008', 'Orangen-Eis in Fruchtschale', 'Helados', 'Fruchtiges Orangen-Eis serviert in einer frischen Orange.', '6,90', 'Dessert', 'Milch', 'Orangensaft, Sahne, Zucker, Orangenschale', false, true, true, 8, true),
('d009', 'Nuss-Eis in Fruchtschale', 'Helados', 'Cremiges Nuss-Eis mit karamellisierten Nüssen in natürlicher Schale.', '6,90', 'Dessert', 'Milch, Schalenfrüchte', 'Sahne, Haselnüsse, Walnüsse, Zucker, Karamell', false, true, true, 9, true),

-- 13. Heißgetränke & Tee
('hg001', 'Café Crema', 'Deutscher Filterkaffee', 'Milder, aromatischer Filterkaffee aus besten Arabica-Bohnen.', '3,60', 'Heißgetränke', '', 'Kaffeebohnen, Wasser', true, true, true, 1, true),
('hg002', 'Cappuccino', 'Mit Milchschaum', 'Italienischer Cappuccino mit perfektem Milchschaum und Kakao-Pulver.', '3,60', 'Heißgetränke', 'Milch', 'Espresso, Milch, Milchschaum, Kakao', false, true, true, 2, true),
('hg003', 'Milchkaffee', 'Café au Lait', 'Starker Kaffee mit heißer Milch im Verhältnis 1:1.', '3,90', 'Heißgetränke', 'Milch', 'Kaffee, Milch', false, true, true, 3, true),
('hg004', 'Latte Macchiato', 'Geschichteter Milchkaffee', 'Espresso mit heißer Milch und cremigem Milchschaum, schön geschichtet.', '3,90', 'Heißgetränke', 'Milch', 'Espresso, Milch, Milchschaum', false, true, true, 4, true),
('hg005', 'Espresso', 'Italienischer Kaffee', 'Starker italienischer Espresso aus besten Arabica-Bohnen.', '2,80', 'Heißgetränke', '', 'Espresso-Bohnen, Wasser', true, true, true, 5, true),
('hg006', 'Espresso doppio', 'Doppelter Espresso', 'Doppelte Portion italienischer Espresso für Kaffee-Liebhaber.', '3,90', 'Heißgetränke', '', 'Espresso-Bohnen, Wasser', true, true, true, 6, true),
('hg007', 'Café Cortado', 'Spanische Spezialität', 'Espresso mit einem Schuss warmer Milch nach spanischer Art.', '3,90', 'Heißgetränke', 'Milch', 'Espresso, warme Milch', false, true, true, 7, true),
('hg008', 'Heiße Schokolade mit Sahne', 'Cremig und süß', 'Traditionelle heiße Schokolade mit Schlagsahne und Kakao-Pulver.', '3,90', 'Heißgetränke', 'Milch', 'Schokolade, Milch, Sahne, Zucker, Kakao', false, true, true, 8, true),
('hg009', 'Frischer Minz Tee mit Ingwer und Honig', 'Hausgemacht', 'Frisch aufgebrühter Minz-Tee mit Ingwer und spanischem Honig.', '3,90', 'Heißgetränke', '', 'Frische Minze, Ingwer, Honig, Wasser', true, true, true, 9, true),
('hg010', 'Ingwer Orangen Tee mit Honig', 'Hausgemacht', 'Wärmender Tee aus frischem Ingwer, Orange und Honig.', '3,90', 'Heißgetränke', '', 'Ingwer, Orangenschale, Honig, Wasser', true, true, true, 10, true),
('hg011', 'Schwarzer Tee', 'Im Beutel', 'Kräftiger schwarzer Tee aus besten Teegärten.', '3,20', 'Heißgetränke', '', 'Schwarzer Tee, Wasser', true, true, true, 11, true),
('hg012', 'Grüner Tee', 'Im Beutel', 'Milder grüner Tee mit zartem, frischem Geschmack.', '3,20', 'Heißgetränke', '', 'Grüner Tee, Wasser', true, true, true, 12, true),
('hg013', 'Früchte Tee', 'Im Beutel', 'Fruchtiger Tee mit natürlichen Fruchtaromen.', '3,20', 'Heißgetränke', '', 'Früchtetee, Wasser', true, true, true, 13, true),
('hg014', 'Kamillen Tee', 'Im Beutel', 'Beruhigender Kamillentee, perfekt für entspannte Momente.', '3,20', 'Heißgetränke', '', 'Kamille, Wasser', true, true, true, 14, true),
('hg015', 'Rooibos Tee', 'Im Beutel', 'Koffeinfreier Rooibos-Tee mit natürlich süßem Geschmack.', '3,20', 'Heißgetränke', '', 'Rooibos, Wasser', true, true, true, 15, true),

-- Getränke (als separate Kategorien da sehr umfangreich)
-- 14. Softdrinks, Wasser & Limonaden
('sd001', 'Coca Cola 0,3l', 'Klassisch', 'Original Coca Cola, eisgekühlt serviert.', '3,90', 'Softdrinks', '', 'Coca Cola', true, true, true, 1, true),
('sd002', 'Coca Cola 0,5l', 'Klassisch', 'Original Coca Cola, eisgekühlt serviert.', '5,90', 'Softdrinks', '', 'Coca Cola', true, true, true, 2, true),
('sd003', 'Coca Cola Zero 0,3l', 'Zuckerfrei', 'Coca Cola Zero, zuckerfrei und kalorienarm.', '3,90', 'Softdrinks', '', 'Coca Cola Zero', true, true, true, 3, true),
('sd004', 'Coca Cola Zero 0,5l', 'Zuckerfrei', 'Coca Cola Zero, zuckerfrei und kalorienarm.', '5,90', 'Softdrinks', '', 'Coca Cola Zero', true, true, true, 4, true),
('sd005', 'Spezi 0,3l', 'Cola-Mix', 'Erfrischende Mischung aus Cola und Orange.', '3,90', 'Softdrinks', '', 'Spezi', true, true, true, 5, true),
('sd006', 'Spezi 0,5l', 'Cola-Mix', 'Erfrischende Mischung aus Cola und Orange.', '5,90', 'Softdrinks', '', 'Spezi', true, true, true, 6, true),
('sd007', 'Fanta 0,3l', 'Orange', 'Fruchtige Fanta Orange, eisgekühlt.', '3,90', 'Softdrinks', '', 'Fanta Orange', true, true, true, 7, true),
('sd008', 'Fanta 0,5l', 'Orange', 'Fruchtige Fanta Orange, eisgekühlt.', '5,90', 'Softdrinks', '', 'Fanta Orange', true, true, true, 8, true),
('sd009', 'Sprite 0,3l', 'Zitrone-Limette', 'Erfrischende Sprite mit Zitrone und Limette.', '3,90', 'Softdrinks', '', 'Sprite', true, true, true, 9, true),
('sd010', 'Sprite 0,5l', 'Zitrone-Limette', 'Erfrischende Sprite mit Zitrone und Limette.', '5,90', 'Softdrinks', '', 'Sprite', true, true, true, 10, true),
('sd011', 'Milch', 'Frische Vollmilch', 'Frische Vollmilch aus der Region.', '1,90', 'Softdrinks', 'Milch', 'Vollmilch', false, true, true, 11, true),
('sd012', 'Tonic Water', 'Schweppes', 'Klassisches Tonic Water von Schweppes.', '3,80', 'Softdrinks', '', 'Tonic Water', true, true, true, 12, true),
('sd013', 'Ginger Ale', 'Schweppes', 'Würziges Ginger Ale mit natürlichem Ingwer.', '3,80', 'Softdrinks', '', 'Ginger Ale', true, true, true, 13, true),
('sd014', 'Bitter Lemon', 'Schweppes', 'Bitter Lemon mit natürlichen Zitrusaromen.', '3,80', 'Softdrinks', '', 'Bitter Lemon', true, true, true, 14, true),
('sd015', 'Wasser Magnus Kohlensäure 0,25l', 'Sprudelwasser', 'Magnus Mineralwasser mit Kohlensäure.', '2,90', 'Softdrinks', '', 'Mineralwasser mit Kohlensäure', true, true, true, 15, true),
('sd016', 'Wasser Magnus Kohlensäure 0,75l', 'Sprudelwasser', 'Magnus Mineralwasser mit Kohlensäure.', '5,80', 'Softdrinks', '', 'Mineralwasser mit Kohlensäure', true, true, true, 16, true),
('sd017', 'Wasser Magnus still 0,25l', 'Stilles Wasser', 'Magnus Mineralwasser ohne Kohlensäure.', '2,90', 'Softdrinks', '', 'Stilles Mineralwasser', true, true, true, 17, true),
('sd018', 'Wasser Magnus still 0,75l', 'Stilles Wasser', 'Magnus Mineralwasser ohne Kohlensäure.', '5,80', 'Softdrinks', '', 'Stilles Mineralwasser', true, true, true, 18, true);

-- Hausgemachte Limonaden (0,3l)
INSERT INTO menu_items (id, name, description, detailed_description, price, category, allergens, ingredients, vegan, vegetarian, glutenfree, order_index, is_active) VALUES
('lim001', 'Minz-Zitrone 0,3l', 'Hausgemacht', 'Erfrischende Limonade mit frischer Minze und Zitrone.', '3,90', 'Limonaden', '', 'Frische Minze, Zitrone, Zucker, Wasser, Eis', true, true, true, 1, true),
('lim002', 'Minz-Zitrone 0,5l', 'Hausgemacht', 'Erfrischende Limonade mit frischer Minze und Zitrone.', '5,90', 'Limonaden', '', 'Frische Minze, Zitrone, Zucker, Wasser, Eis', true, true, true, 2, true),
('lim003', 'Ingwer-Orange 0,3l', 'Hausgemacht', 'Würzige Limonade mit frischem Ingwer und Orange.', '3,90', 'Limonaden', '', 'Ingwer, Orange, Zucker, Wasser, Eis', true, true, true, 3, true),
('lim004', 'Ingwer-Orange 0,5l', 'Hausgemacht', 'Würzige Limonade mit frischem Ingwer und Orange.', '5,90', 'Limonaden', '', 'Ingwer, Orange, Zucker, Wasser, Eis', true, true, true, 4, true),
('lim005', 'Wasser-Melone 0,3l', 'Hausgemacht', 'Süße Limonade mit frischer Wassermelone.', '3,90', 'Limonaden', '', 'Wassermelone, Zucker, Limette, Wasser, Eis', true, true, true, 5, true),
('lim006', 'Wasser-Melone 0,5l', 'Hausgemacht', 'Süße Limonade mit frischer Wassermelone.', '5,90', 'Limonaden', '', 'Wassermelone, Zucker, Limette, Wasser, Eis', true, true, true, 6, true),
('lim007', 'Gurken-Minze 0,3l', 'Hausgemacht', 'Erfrischende Limonade mit Gurke und Minze.', '3,90', 'Limonaden', '', 'Gurke, Minze, Limette, Zucker, Wasser, Eis', true, true, true, 7, true),
('lim008', 'Gurken-Minze 0,5l', 'Hausgemacht', 'Erfrischende Limonade mit Gurke und Minze.', '5,90', 'Limonaden', '', 'Gurke, Minze, Limette, Zucker, Wasser, Eis', true, true, true, 8, true),
('lim009', 'Jimmy\'s Passion 0,3l', 'Hausgemacht', 'Jimmys spezielle Limonade mit Passionsfrucht und Mango.', '3,90', 'Limonaden', '', 'Passionsfrucht, Mango, Limette, Zucker, Wasser', true, true, true, 9, true),
('lim010', 'Jimmy\'s Passion 0,5l', 'Hausgemacht', 'Jimmys spezielle Limonade mit Passionsfrucht und Mango.', '5,90', 'Limonaden', '', 'Passionsfrucht, Mango, Limette, Zucker, Wasser', true, true, true, 10, true);
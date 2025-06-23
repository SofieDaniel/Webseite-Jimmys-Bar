USE jimmys_tapas_bar;

-- Shots und Spirituosen
INSERT INTO menu_items (id, name, description, detailed_description, price, category, allergens, ingredients, vegan, vegetarian, glutenfree, order_index, is_active) VALUES
('shot001', 'Helbing 2cl', 'Hamburger Kümmellikör', 'Traditioneller Hamburger Kümmellikör, eisgekühlt serviert.', '3,00', 'Shots', '', 'Helbing Kümmellikör', true, true, true, 1, true),
('shot002', 'Sambuca 2cl', 'Italienischer Anislikör', 'Klassischer italienischer Sambuca, optional mit Kaffeebohnen.', '3,00', 'Shots', '', 'Sambuca', true, true, true, 2, true),
('shot003', 'Tequila 2cl', 'Mexikanischer Agavenschnaps', 'Echter mexikanischer Tequila mit Salz und Limette.', '3,00', 'Shots', '', 'Tequila', true, true, true, 3, true),
('shot004', 'Kanarischer Rum 2cl', 'Spanischer Rum', 'Kanarischer Rum aus spanischer Produktion.', '3,00', 'Shots', '', 'Kanarischer Rum', true, true, true, 4, true),
('shot005', 'Jägermeister 2cl', 'Deutscher Kräuterlikör', 'Klassischer deutscher Jägermeister aus 56 Kräutern.', '3,00', 'Shots', '', 'Jägermeister', true, true, true, 5, true),
('shot006', 'Raki 2cl', 'Türkischer Anisschnaps', 'Traditioneller türkischer Raki, eisgekühlt.', '3,00', 'Shots', '', 'Raki', true, true, true, 6, true),
('shot007', 'Ouzo 2cl', 'Griechischer Anislikör', 'Echter griechischer Ouzo aus Griechenland.', '3,00', 'Shots', '', 'Ouzo', true, true, true, 7, true),
('shot008', 'Mexikaner 2cl', 'Tequila-Mix', 'Scharfer Mix aus Tequila, Tomatenmark und Gewürzen.', '3,00', 'Shots', '', 'Tequila, Tomatenmark, Gewürze', true, true, true, 8, true),
('shot009', 'Wodka 2cl', 'Russischer Wodka', 'Reiner russischer Wodka, eisgekühlt serviert.', '3,00', 'Shots', '', 'Wodka', true, true, true, 9, true),
('shot010', 'Ficken Likör 2cl', 'Fruchtlikör', 'Süßer Fruchtlikör mit provocantem Namen.', '3,00', 'Shots', '', 'Ficken Likör', true, true, true, 10, true),

-- Gin Longdrinks
('gin001', 'Bombay Gin 0,2l', 'Gin Tonic', 'Bombay Gin mit Tonic Water, Eis und Zitrone.', '8,90', 'Gin', '', 'Bombay Gin, Tonic Water, Zitrone, Eis', true, true, true, 1, true),
('gin002', 'Hendricks Gin 0,2l', 'Premium Gin Tonic', 'Hendricks Gin mit Premium Tonic, Gurke und Eis.', '9,90', 'Gin', '', 'Hendricks Gin, Premium Tonic, Gurke, Eis', true, true, true, 2, true),

-- Whiskey
('whiskey001', 'Black Label 4cl', 'Schottischer Whisky', 'Johnnie Walker Black Label, 12 Jahre gereift.', '8,90', 'Whiskey', '', 'Johnnie Walker Black Label', true, true, true, 1, true),
('whiskey002', 'Chivas Regal 4cl', 'Premium Blend', 'Chivas Regal 12 Jahre, premium schottischer Blend.', '9,90', 'Whiskey', '', 'Chivas Regal 12 Jahre', true, true, true, 2, true),
('whiskey003', 'Jack Daniels 4cl', 'Tennessee Whiskey', 'Original Jack Daniels aus Tennessee, USA.', '7,90', 'Whiskey', '', 'Jack Daniels', true, true, true, 3, true),
('whiskey004', 'Ballantines 4cl', 'Schottischer Blend', 'Ballantines Finest schottischer Whisky.', '7,90', 'Whiskey', '', 'Ballantines Finest', true, true, true, 4, true),

-- Spanischer Brandy
('brandy001', 'Veterano Osborne 4cl', 'Spanischer Brandy', 'Klassischer spanischer Brandy aus dem Hause Osborne.', '5,90', 'Brandy', '', 'Veterano Osborne', true, true, true, 1, true),
('brandy002', '103 Brandy 4cl', 'Spanischer Brandy', 'Hochwertiger spanischer Brandy 103.', '7,90', 'Brandy', '', '103 Brandy', true, true, true, 2, true),
('brandy003', 'Cardenal Mendoza 4cl', 'Premium Brandy', 'Exklusiver spanischer Brandy Cardenal Mendoza.', '7,90', 'Brandy', '', 'Cardenal Mendoza', true, true, true, 3, true),
('brandy004', 'Carlos I 4cl', 'Solera Gran Reserva', 'Carlos I Solera Gran Reserva, spanischer Brandy.', '7,90', 'Brandy', '', 'Carlos I Solera', true, true, true, 4, true),

-- 18. Cocktails

-- Alkoholfreie Cocktails (0,3 l)
('cocktail001', 'Ipanema 0,3l', 'Alkoholfrei', 'Caipirinha ohne Alkohol mit Limetten, Rohrzucker und Ginger Ale.', '6,90', 'Cocktails', '', 'Limetten, Rohrzucker, Ginger Ale, Eis', true, true, true, 1, true),
('cocktail002', 'Marenema 0,3l', 'Alkoholfrei', 'Fruchtige Mischung aus Ananas, Cranberry und Limette.', '7,50', 'Cocktails', '', 'Ananassaft, Cranberrysaft, Limette, Grenadine', true, true, true, 2, true),
('cocktail003', 'Virgin Colada 0,3l', 'Alkoholfrei', 'Pina Colada ohne Rum mit Kokosmilch und Ananas.', '6,90', 'Cocktails', '', 'Kokosmilch, Ananassaft, Sahne, Zucker, Eis', true, true, true, 3, true),
('cocktail004', 'Princess 0,3l', 'Alkoholfrei', 'Elegante Mischung aus Pfirsich, Orange und Grenadine.', '7,50', 'Cocktails', '', 'Pfirsichsaft, Orangensaft, Grenadine, Soda', true, true, true, 4, true),
('cocktail005', 'Jimmy\'s Libre 0,3l', 'Alkoholfrei', 'Jimmys alkoholfreie Interpretation der Cuba Libre.', '6,90', 'Cocktails', '', 'Cola, Limettensaft, Grenadine, Eis, Limette', true, true, true, 5, true),

-- Cocktails mit Alkohol (0,4 l)
('cocktail006', 'Mojito 0,4l', 'Mit Alkohol', 'Klassischer kubanischer Mojito mit weißem Rum, Minze und Limette.', '8,90', 'Cocktails', '', 'Weißer Rum, Limetten, Minze, Rohrzucker, Soda', true, true, true, 6, true),
('cocktail007', 'Caipirinha 0,4l', 'Mit Alkohol', 'Brasilianischer Nationalcocktail mit Cachaça, Limetten und Rohrzucker.', '8,90', 'Cocktails', '', 'Cachaça, Limetten, Rohrzucker, Eis', true, true, true, 7, true),
('cocktail008', 'Sex on the Beach 0,4l', 'Mit Alkohol', 'Fruchtiger Cocktail mit Wodka, Pfirsichlikör und Cranberry.', '9,90', 'Cocktails', '', 'Wodka, Pfirsichlikör, Ananassaft, Cranberrysaft', true, true, true, 8, true),
('cocktail009', 'Tequila Sunrise 0,4l', 'Mit Alkohol', 'Mexikanischer Klassiker mit Tequila, Orange und Grenadine.', '8,90', 'Cocktails', '', 'Tequila, Orangensaft, Grenadine, Eis', true, true, true, 9, true),
('cocktail010', 'Cuba Libre 0,4l', 'Mit Alkohol', 'Kubanischer Cocktail mit weißem Rum, Cola und Limette.', '8,90', 'Cocktails', '', 'Weißer Rum, Cola, Limettensaft, Eis, Limette', true, true, true, 10, true),
('cocktail011', 'Moscow Mule 0,4l', 'Mit Alkohol', 'Wodka-Cocktail mit Ginger Beer und Limette im Kupferbecher.', '9,90', 'Cocktails', '', 'Wodka, Ginger Beer, Limettensaft, Minze, Eis', true, true, true, 11, true),
('cocktail012', 'Pina Colada 0,4l', 'Mit Alkohol', 'Karibischer Cocktail mit weißem Rum, Kokosmilch und Ananas.', '9,90', 'Cocktails', '', 'Weißer Rum, Kokosmilch, Ananassaft, Sahne', true, true, true, 12, true),
('cocktail013', 'Long Island Iced Tea 0,4l', 'Mit Alkohol', 'Starker Cocktail-Mix mit fünf verschiedenen Spirituosen.', '9,90', 'Cocktails', '', 'Wodka, Rum, Gin, Tequila, Triple Sec, Cola, Zitrone', true, true, true, 13, true),
('cocktail014', 'Wodka Lemon 0,4l', 'Mit Alkohol', 'Einfacher Cocktail mit Wodka und frischem Zitronensaft.', '8,90', 'Cocktails', '', 'Wodka, Zitronensaft, Zucker, Soda, Eis', true, true, true, 14, true),
('cocktail015', 'Whiskey Sour 0,4l', 'Mit Alkohol', 'Klassischer Sour mit Whiskey, Zitronensaft und Zucker.', '9,90', 'Cocktails', 'Eier', 'Whiskey, Zitronensaft, Zucker, Eiweiß, Eis', false, true, true, 15, true),
('cocktail016', 'Jimmy\'s Special 0,4l', 'Mit Alkohol', 'Jimmys Hauscocktail mit geheimer Rezeptur.', '9,90', 'Cocktails', '', 'Rum, Fruchtliköre, Fruchtsäfte (Rezeptur variiert)', true, true, true, 16, true),
('cocktail017', 'Swimming Pool 0,4l', 'Mit Alkohol', 'Blauer Cocktail mit Wodka, Pfirsichlikör und Blue Curacao.', '9,90', 'Cocktails', '', 'Wodka, Pfirsichlikör, Blue Curacao, Ananassaft, Sahne', true, true, true, 17, true),
('cocktail018', 'Mai Tai 0,4l', 'Mit Alkohol', 'Polynesischer Cocktail mit dunklem und weißem Rum.', '9,90', 'Cocktails', '', 'Weißer Rum, dunkler Rum, Mandelsirup, Limettensaft', true, true, true, 18, true),
('cocktail019', 'Zombie 0,4l', 'Mit Alkohol', 'Starker Tiki-Cocktail mit verschiedenen Rum-Sorten.', '9,90', 'Cocktails', '', 'Weißer Rum, dunkler Rum, 151er Rum, Limette, Zucker', true, true, true, 19, true),
('cocktail020', 'Solero 0,4l', 'Mit Alkohol', 'Cremiger Cocktail mit Wodka, Pfirsichlikör und Maracuja.', '8,90', 'Cocktails', '', 'Wodka, Pfirsichlikör, Maracujasaft, Sahne, Vanilleeis', true, true, true, 20, true),

-- 19. Spanische Getränke
('sangria001', 'Sangria Tinto 0,2l', 'Rotwein-Sangria', 'Klassische spanische Sangria mit Rotwein und Früchten.', '5,50', 'Sangria', '', 'Rotwein, Früchte, Brandy, Zucker, Soda', true, true, true, 1, true),
('sangria002', 'Sangria Tinto 0,5l', 'Rotwein-Sangria', 'Klassische spanische Sangria mit Rotwein und Früchten.', '12,90', 'Sangria', '', 'Rotwein, Früchte, Brandy, Zucker, Soda', true, true, true, 2, true),
('sangria003', 'Sangria Blanco 0,2l', 'Weißwein-Sangria', 'Erfrischende weiße Sangria mit Weißwein und Früchten.', '5,50', 'Sangria', '', 'Weißwein, Früchte, Brandy, Zucker, Soda', true, true, true, 3, true),
('sangria004', 'Sangria Blanco 0,5l', 'Weißwein-Sangria', 'Erfrischende weiße Sangria mit Weißwein und Früchten.', '12,90', 'Sangria', '', 'Weißwein, Früchte, Brandy, Zucker, Soda', true, true, true, 4, true),
('sangria005', 'Tinto de Verano 0,2l', 'Rotwein mit Zitronen-Limo', 'Spanisches Sommergetränk aus Rotwein und Zitronenlimonade.', '5,50', 'Sangria', '', 'Rotwein, Zitronenlimonade, Eis, Zitrone', true, true, true, 5, true),
('sangria006', 'Tinto de Verano 0,5l', 'Rotwein mit Zitronen-Limo', 'Spanisches Sommergetränk aus Rotwein und Zitronenlimonade.', '12,90', 'Sangria', '', 'Rotwein, Zitronenlimonade, Eis, Zitrone', true, true, true, 6, true);
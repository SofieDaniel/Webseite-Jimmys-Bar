USE jimmys_tapas_bar;

-- Clear existing menu items
DELETE FROM menu_items;

-- 1. Inicio / Vorspeisen
INSERT INTO menu_items (id, name, description, detailed_description, price, category, allergens, ingredients, vegan, vegetarian, glutenfree, order_index, is_active) VALUES
('v001', 'Aioli', 'Knoblauchsauce mit Öl', 'Hausgemachte Aioli aus frischem Knoblauch und spanischem Olivenöl extra vergine. Perfekt als Dip für Brot oder Tapas.', '3,50', 'Vorspeisen', 'Eier', 'Knoblauch, Olivenöl, Eigelb, Zitronensaft, Salz', false, true, true, 1, true),
('v002', 'Oliven', 'Spanische Oliven', 'Auswahl von grünen und schwarzen Oliven aus verschiedenen spanischen Regionen, mariniert mit Kräutern und Gewürzen.', '3,90', 'Vorspeisen', '', 'Grüne Oliven, schwarze Oliven, Olivenöl, Knoblauch, Kräuter', true, true, true, 2, true),
('v003', 'Extra Brot', 'Frisches spanisches Brot', 'Warmes, knuspriges Brot nach traditionellem spanischen Rezept, perfekt zu unseren Tapas.', '1,90', 'Vorspeisen', 'Glutenhaltiges Getreide', 'Weizenmehl, Hefe, Salz, Olivenöl, Wasser', true, true, false, 3, true),
('v004', 'Hummus', 'Kichererbsen Cream', 'Cremiger Hummus aus pürierten Kichererbsen, Tahini, Knoblauch und Zitronensaft, serviert mit warmem Fladenbrot.', '3,90', 'Vorspeisen', 'Sesam, Glutenhaltiges Getreide', 'Kichererbsen, Tahini, Knoblauch, Zitronensaft, Olivenöl, Kreuzkümmel', true, true, false, 4, true),
('v005', 'Guacamole', 'Avocado Cream', 'Frische Guacamole aus reifen Avocados, Tomaten, Zwiebeln, Koriander und Limettensaft, serviert mit Tortilla-Chips.', '3,90', 'Vorspeisen', '', 'Avocado, Tomaten, Zwiebeln, Koriander, Limettensaft, Chili, Salz', true, true, true, 5, true),
('v006', 'Spanischer Käseteller', 'Manchego', 'Auswahl von spanischem Manchego-Käse verschiedener Reifegrade, serviert mit Feigenmarmelade und Nüssen.', '8,90', 'Vorspeisen', 'Milch, Schalenfrüchte', 'Manchego-Käse, Feigenmarmelade, Walnüsse, Honig', false, true, true, 6, true),
('v007', 'Schinken-Käse-Wurst Teller', 'Spanische Spezialitäten', 'Platte mit Jamón Serrano, Manchego-Käse, Chorizo und weiteren spanischen Delikatessen.', '11,90', 'Vorspeisen', 'Milch', 'Jamón Serrano, Manchego-Käse, Chorizo, Salami, Oliven', false, false, true, 7, true),
('v008', 'Jamón Serrano Teller', 'Spanischer Serrano-Schinken', 'Dünn geschnittener, luftgetrockneter Serrano-Schinken aus den Bergen Spaniens, serviert mit Manchego und Feigen.', '9,90', 'Vorspeisen', 'Milch', 'Jamón Serrano, Manchego-Käse, frische Feigen, Olivenöl', false, false, true, 8, true),
('v009', 'Boquerones en Vinagre', 'Mit Essig und Öl', 'In Essig eingelegte Anchovis-Filets, mariniert mit Knoblauch, Petersilie und spanischem Olivenöl.', '8,90', 'Vorspeisen', 'Fisch', 'Anchovis, Essig, Olivenöl, Knoblauch, Petersilie', false, false, true, 9, true),
('v010', 'Pata Negra', 'Spanischer Ibérico Schinken', 'Edelster iberischer Schinken von freilaufenden Schweinen, die sich von Eicheln ernähren. Ein Geschmackserlebnis der Extraklasse.', '8,90', 'Vorspeisen', '', 'Ibérico-Schinken Pata Negra', false, false, true, 10, true),
('v011', 'Tres', 'Hummus, Avocado Cream, Aioli mit Brot', 'Trio aus hausgemachtem Hummus, frischer Guacamole und Aioli, serviert mit warmem spanischen Brot.', '10,90', 'Vorspeisen', 'Eier, Sesam, Glutenhaltiges Getreide', 'Kichererbsen, Avocado, Knoblauch, Olivenöl, Tahini, Eigelb, Brot', false, true, false, 11, true),

-- 2. Salate
('s001', 'Ensalada Mixta', 'Bunter Salat mit Essig und Öl', 'Frischer gemischter Salat mit Tomaten, Gurken, Paprika, Zwiebeln und unserem hausgemachten Vinaigrette.', '8,90', 'Salate', '', 'Blattsalat, Tomaten, Gurken, Paprika, Zwiebeln, Olivenöl, Essig, Kräuter', true, true, true, 1, true),
('s002', 'Ensalada Tonno', 'Bunter Salat mit Thunfisch', 'Gemischter Salat mit saftigem Thunfisch, hart gekochten Eiern, Oliven und Spanish Dressing.', '14,90', 'Salate', 'Fisch, Eier', 'Blattsalat, Thunfisch, Eier, Tomaten, Gurken, Oliven, Zwiebeln', false, false, true, 2, true),
('s003', 'Ensalada Pollo', 'Bunter Salat mit Hähnchenstreifen', 'Frischer Salat mit gegrillten Hähnchenstreifen, Cherry-Tomaten, Avocado und Balsamico-Dressing.', '14,90', 'Salate', '', 'Blattsalat, Hähnchenfilet, Cherry-Tomaten, Avocado, Balsamico-Essig', false, false, true, 3, true),
('s004', 'Ensalada Garnelen', 'Bunter Salat mit Garnelen', 'Gemischter Salat mit gegrillten Garnelen, Mango, Rucola und Limetten-Dressing.', '15,90', 'Salate', 'Schalentiere', 'Blattsalat, Garnelen, Mango, Rucola, Limette, Olivenöl', false, false, true, 4, true),
('s005', 'Kleiner Salat', 'Tomaten/Gurken mit Zwiebeln', 'Kleiner Beilagensalat mit frischen Tomaten, Gurken und roten Zwiebeln in Olivenöl-Dressing.', '6,90', 'Salate', '', 'Tomaten, Gurken, rote Zwiebeln, Olivenöl, Essig, Salz, Pfeffer', true, true, true, 5, true),
('s006', 'Rote Beete Salat mit Ziegenkäse', 'Rote Beete mit cremigem Ziegenkäse', 'Geröstete rote Beete mit cremigem Ziegenkäse, Walnüssen und Honig-Balsamico-Dressing.', '7,90', 'Salate', 'Milch, Schalenfrüchte', 'Rote Beete, Ziegenkäse, Walnüsse, Honig, Balsamico-Essig, Rucola', false, true, true, 6, true),
('s007', 'Kichererbsen Salat mit Feta', 'Mediterrane Kichererbsen mit Feta', 'Warmer Kichererbsen-Salat mit Feta-Käse, Tomaten, Gurken, roten Zwiebeln und mediterranen Kräutern.', '7,90', 'Salate', 'Milch', 'Kichererbsen, Feta-Käse, Tomaten, Gurken, rote Zwiebeln, Petersilie, Olivenöl', false, true, true, 7, true),

-- 3. Tapa Paella
('p001', 'Paella', 'Mit Hähnchen und Meeresfrüchten', 'Traditionelle Paella-Portion mit Safranreis, Hähnchen, Garnelen, Muscheln und spanischen Gemüsesorten.', '8,90', 'Paella', 'Schalentiere, Weichtiere', 'Bomba-Reis, Safran, Hähnchen, Garnelen, Muscheln, grüne Bohnen, Paprika', false, false, true, 1, true),
('p002', 'Paella Vegetarisch', 'Vegetarische Paella', 'Safranreis mit gegrilltem Gemüse, Artischocken, grünen Bohnen, Paprika und frischen Kräutern.', '7,90', 'Paella', '', 'Bomba-Reis, Safran, Artischocken, grüne Bohnen, Paprika, Tomaten, Zwiebeln', true, true, true, 2, true);

-- Continue with rest of menu items...
-- This is getting very long, so I'll create the rest in chunks
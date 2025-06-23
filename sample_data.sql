USE jimmys_tapas_bar;

-- Insert sample menu items
INSERT IGNORE INTO menu_items (id, name, description, detailed_description, price, category, allergens, ingredients, vegan, vegetarian, glutenfree, order_index, is_active) VALUES
('aa1e8400-e29b-41d4-a716-446655440001', 'Paella Valenciana', 'Original spanische Paella mit Safran, Huhn und Gemüse', 'Traditionelle Paella aus Valencia mit safrangewürztem Reis, zartem Hühnchen, grünen Bohnen, Artischocken und weißen Bohnen. Nach authentischem Familienrezept zubereitet.', '18,90', 'Paella', 'Glutenhaltiges Getreide', 'Bomba-Reis, Safran, Hühnchen, grüne Bohnen, Artischocken, weiße Bohnen, Olivenöl, Knoblauch, Zwiebeln, Paprika, Hühnerbrühe', false, false, false, 1, true),
('bb1e8400-e29b-41d4-a716-446655440002', 'Gambas al Ajillo', 'Knoblauchgarnelen in Olivenöl mit frischen Kräutern', 'Frische Garnelen aus dem Mittelmeer, scharf angebraten mit viel Knoblauch und Petersilie in bestem spanischen Olivenöl. Serviert mit knusprigem Baguette.', '14,90', 'Vorspeisen', 'Schalentiere', 'Garnelen, Knoblauch, Olivenöl extra virgen, Petersilie, Chili, Meersalz, Baguette', false, false, true, 2, true),
('cc1e8400-e29b-41d4-a716-446655440003', 'Patatas Bravas', 'Würzige Kartoffeln mit scharfer Tomaten-Aioli', 'Knusprig gebratene Kartoffelwürfel mit hausgemachter Bravas-Sauce aus Tomaten, Paprika und Knoblauch. Ein Klassiker der spanischen Tapas-Küche.', '8,90', 'Vorspeisen', 'Eier, Soja', 'Kartoffeln, Tomaten, Paprika, Knoblauch, Mayonnaise, Olivenöl, Essig, Salz, Pfeffer', false, true, true, 3, true);

-- Insert sample reviews
INSERT IGNORE INTO reviews (id, customer_name, rating, comment, is_approved, approved_by, approved_at) VALUES
('dd1e8400-e29b-41d4-a716-446655440004', 'Maria Schmidt', 5, 'Fantastisches Essen! Die Paella war absolut authentisch und der Service war herzlich und aufmerksam. Wir kommen definitiv wieder!', true, 'admin', NOW()),
('ee1e8400-e29b-41d4-a716-446655440005', 'Thomas Müller', 4, 'Sehr gemütliche Atmosphäre direkt am Strand. Die Gambas waren perfekt zubereitet. Einzig die Wartezeit war etwas lang.', true, 'admin', NOW()),
('ff1e8400-e29b-41d4-a716-446655440006', 'Jennifer Lopez', 5, 'Bestes spanisches Restaurant an der Ostseeküste! Jimmy persönlich hat uns bedient und uns die Gerichte erklärt. Einfach wunderbar!', false, null, null);

-- Insert sample contact messages
INSERT IGNORE INTO contact_messages (id, name, email, phone, subject, message, is_read, responded) VALUES
('gg1e8400-e29b-41d4-a716-446655440007', 'Peter Hansen', 'peter.hansen@email.de', '+49 172 1234567', 'Reservierung für Hochzeitsfeier', 'Hallo, wir möchten gerne eine Hochzeitsfeier für 40 Personen im August buchen. Können Sie uns ein Angebot erstellen?', false, false),
('hh1e8400-e29b-41d4-a716-446655440008', 'Anna Weber', 'anna.weber@gmail.com', '+49 151 9876543', 'Lob für den Service', 'Vielen Dank für den wundervollen Abend gestern! Das Essen war fantastisch und der Service perfekt.', true, true);

-- Insert updated homepage content with proper structure
INSERT IGNORE INTO homepage_content (id, hero_title, hero_subtitle, hero_description, hero_location, hero_background_image, hero_menu_button_text, hero_locations_button_text, features_data, specialties_data, delivery_data, updated_by) VALUES
('ii1e8400-e29b-41d4-a716-446655440009', 
'JIMMY\'S TAPAS BAR', 
'Authentische spanische Küche an der Ostsee',
'Genießen Sie authentische mediterrane Spezialitäten',
'direkt an der malerischen Ostseeküste',
'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
'Zur Speisekarte',
'Unsere Standorte',
'[{"title": "Authentische Tapas", "description": "Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen", "image": "https://images.unsplash.com/photo-1544025162-d76694265947"}, {"title": "Frische Meeresfrüchte", "description": "Täglich frisch aus der Ostsee und dem Mittelmeer", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"}, {"title": "Strandlage", "description": "Genießen Sie Ihr Essen mit direktem Blick auf die Ostsee", "image": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"}]',
'[{"title": "Paella Valenciana", "description": "Original spanische Paella mit Safran, Huhn und Gemüse", "price": "18,90€", "image": "https://images.unsplash.com/photo-1534080564583-6be75777b70a"}, {"title": "Gambas al Ajillo", "description": "Knoblauchgarnelen in Olivenöl mit frischen Kräutern", "price": "12,90€", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b"}, {"title": "Pulpo a la Gallega", "description": "Galicischer Oktopus mit Paprika und Olivenöl", "price": "14,90€", "image": "https://images.unsplash.com/photo-1544025162-d76694265947"}]',
'{"title": "Lieferservice", "subtitle": "Spanische Köstlichkeiten direkt zu Ihnen", "delivery_time": "30-45 Min", "minimum_order": "15,00€", "delivery_fee": "2,50€", "areas": ["Neustadt in Holstein", "Großenbrode", "Umgebung"], "image": "https://images.unsplash.com/photo-1586816001966-79b736744398"}',
'system');

-- Update about page data with proper structure
INSERT IGNORE INTO locations (id, page_title, page_description, locations_data, updated_by) VALUES
('jj1e8400-e29b-41d4-a716-446655440010',
'Unsere Standorte',
'Besuchen Sie uns an einem unserer beiden Standorte',
'[{"id": "neustadt", "name": "Neustadt in Holstein", "address": "Strandstraße 12, 23730 Neustadt in Holstein", "phone": "+49 4561 123456", "email": "neustadt@jimmys-tapasbar.de", "opening_hours": {"monday": "17:00-23:00", "tuesday": "17:00-23:00", "wednesday": "17:00-23:00", "thursday": "17:00-23:00", "friday": "17:00-00:00", "saturday": "17:00-00:00", "sunday": "17:00-23:00"}, "features": ["Direkte Strandlage", "Große Terrasse", "Live-Musik", "Familienfreundlich"]}, {"id": "grossenbrode", "name": "Großenbrode", "address": "Strandpromenade 8, 23775 Großenbrode", "phone": "+49 4367 987654", "email": "grossenbrode@jimmys-tapasbar.de", "opening_hours": {"monday": "17:00-22:00", "tuesday": "17:00-22:00", "wednesday": "17:00-22:00", "thursday": "17:00-22:00", "friday": "17:00-23:00", "saturday": "17:00-23:00", "sunday": "17:00-22:00"}, "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"]}]',
'system');
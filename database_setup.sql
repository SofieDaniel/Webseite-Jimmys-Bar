USE jimmys_tapas_bar;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'editor', 'viewer') DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Status checks table
CREATE TABLE IF NOT EXISTS status_checks (
    id VARCHAR(36) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR(36) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT FALSE,
    approved_by VARCHAR(100) NULL,
    approved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    detailed_description TEXT,
    price VARCHAR(20) NOT NULL,
    category VARCHAR(100) NOT NULL,
    image TEXT,
    details TEXT,
    origin VARCHAR(255),
    allergens TEXT,
    additives TEXT,
    preparation_method TEXT,
    ingredients TEXT,
    vegan BOOLEAN DEFAULT FALSE,
    vegetarian BOOLEAN DEFAULT FALSE,
    glutenfree BOOLEAN DEFAULT FALSE,
    order_index INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Contact messages table
CREATE TABLE IF NOT EXISTS contact_messages (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    responded BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Maintenance mode table
CREATE TABLE IF NOT EXISTS maintenance_mode (
    id VARCHAR(36) PRIMARY KEY,
    is_active BOOLEAN DEFAULT FALSE,
    message TEXT DEFAULT 'Die Website befindet sich derzeit im Wartungsmodus.',
    activated_by VARCHAR(100),
    activated_at TIMESTAMP NULL
);

-- Delivery info table
CREATE TABLE IF NOT EXISTS delivery_info (
    id VARCHAR(36) PRIMARY KEY,
    delivery_time_min INT DEFAULT 30,
    delivery_time_max INT DEFAULT 45,
    minimum_order_value DECIMAL(10,2) DEFAULT 15.00,
    delivery_fee DECIMAL(10,2) DEFAULT 2.50,
    available_locations JSON,
    is_active BOOLEAN DEFAULT TRUE,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Enhanced Standorte table
CREATE TABLE IF NOT EXISTS standorte_enhanced (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(255) DEFAULT 'Unsere Standorte',
    page_subtitle VARCHAR(500),
    header_background VARCHAR(500),
    neustadt_data JSON,
    grossenbrode_data JSON,
    info_section_data JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

-- Bewertungen page table
CREATE TABLE IF NOT EXISTS bewertungen_page (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(255) DEFAULT 'Bewertungen & Feedback',
    page_subtitle VARCHAR(500),
    header_background VARCHAR(500),
    reviews_section_title VARCHAR(255),
    feedback_section_title VARCHAR(255),
    feedback_note TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

-- Kontakt page table
CREATE TABLE IF NOT EXISTS kontakt_page (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(255) DEFAULT 'Kontakt',
    page_subtitle VARCHAR(500),
    header_background VARCHAR(500),
    contact_form_title VARCHAR(255),
    contact_form_subtitle VARCHAR(500),
    locations_section_title VARCHAR(255),
    opening_hours_title VARCHAR(255),
    additional_info TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

-- Enhanced Über uns table
CREATE TABLE IF NOT EXISTS ueber_uns_enhanced (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(255) DEFAULT 'Über uns',
    page_subtitle VARCHAR(500),
    header_background VARCHAR(500),
    jimmy_data JSON,
    values_section_data JSON,
    team_section_data JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

-- Homepage content table
CREATE TABLE IF NOT EXISTS homepage_content (
    id VARCHAR(36) PRIMARY KEY,
    hero_title VARCHAR(255) DEFAULT 'JIMMY\'S TAPAS BAR',
    hero_subtitle VARCHAR(255) DEFAULT 'an der Ostsee',
    hero_description TEXT,
    hero_location VARCHAR(255),
    hero_background_image VARCHAR(500),
    hero_menu_button_text VARCHAR(100),
    hero_locations_button_text VARCHAR(100),
    hero_image VARCHAR(500),
    features_data JSON,
    specialties_data JSON,
    delivery_data JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

-- Locations table
CREATE TABLE IF NOT EXISTS locations (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(255) DEFAULT 'Unsere Standorte',
    page_description TEXT,
    locations_data JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

-- Legal pages table
CREATE TABLE IF NOT EXISTS legal_pages (
    id VARCHAR(36) PRIMARY KEY,
    page_type ENUM('imprint', 'privacy') NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    contact_name VARCHAR(255),
    contact_address TEXT,
    contact_phone VARCHAR(50),
    contact_email VARCHAR(255),
    company_info JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

-- Insert default admin user
INSERT IGNORE INTO users (id, username, email, password_hash, role, is_active, created_at) 
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'admin',
    'admin@jimmys-tapasbar.de',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewHx/Oj1xV9VT1t2',
    'admin',
    TRUE,
    NOW()
);

-- Insert default delivery info
INSERT IGNORE INTO delivery_info (id, delivery_time_min, delivery_time_max, minimum_order_value, delivery_fee, available_locations, is_active, updated_by) 
VALUES (
    '660e8400-e29b-41d4-a716-446655440000',
    30,
    45,
    15.00,
    2.50,
    '{"neustadt": {"name": "Neustadt", "available": true, "address": "Am Strande 21, 23730 Neustadt in Holstein"}, "grossenbrode": {"name": "Großenbrode", "available": true, "address": "Südstrand 54, 23755 Großenbrode"}}',
    TRUE,
    'system'
);

-- Insert default standorte enhanced data
INSERT IGNORE INTO standorte_enhanced (id, page_title, page_subtitle, header_background, neustadt_data, grossenbrode_data, info_section_data, updated_by) 
VALUES (
    '770e8400-e29b-41d4-a716-446655440000',
    'Unsere Standorte',
    'Besuchen Sie uns an der malerischen Ostseeküste',
    'https://images.unsplash.com/photo-1571197119738-26123cb0d22f',
    '{"name": "Neustadt in Holstein", "address": "Strandstraße 12, 23730 Neustadt in Holstein", "phone": "+49 4561 123456", "email": "neustadt@jimmys-tapasbar.de", "opening_hours": {"monday": "17:00 - 23:00", "tuesday": "17:00 - 23:00", "wednesday": "17:00 - 23:00", "thursday": "17:00 - 23:00", "friday": "17:00 - 00:00", "saturday": "17:00 - 00:00", "sunday": "17:00 - 23:00"}, "features": ["Direkte Strandlage", "Große Terrasse", "Familienfreundlich", "Parkplatz kostenlos"]}',
    '{"name": "Großenbrode", "address": "Strandpromenade 8, 23775 Großenbrode", "phone": "+49 4367 987654", "email": "grossenbrode@jimmys-tapasbar.de", "opening_hours": {"monday": "17:00 - 22:00", "tuesday": "17:00 - 22:00", "wednesday": "17:00 - 22:00", "thursday": "17:00 - 22:00", "friday": "17:00 - 23:00", "saturday": "17:00 - 23:00", "sunday": "17:00 - 22:00"}, "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"]}',
    '{"anreise_parken": {"title": "Anreise & Parken", "description": "Kostenlose Parkplätze direkt am Restaurant verfügbar", "image": "https://images.unsplash.com/photo-1496442226666"}, "oeffnungszeiten": {"title": "Öffnungszeiten", "description": "Täglich geöffnet. Warme Küche bis 22:00 Uhr", "image": "https://images.unsplash.com/photo-1501139083538"}, "familienfreundlich": {"title": "Familienfreundlich", "description": "Spezielle Kinderkarte und Spielbereich vorhanden", "image": "https://images.unsplash.com/photo-1414235077428"}}',
    'system'
);

-- Insert legal pages
INSERT IGNORE INTO legal_pages (id, page_type, title, content, contact_name, contact_address, contact_phone, contact_email) 
VALUES 
(
    '880e8400-e29b-41d4-a716-446655440000',
    'imprint',
    'Impressum',
    'Jimmy''s Tapas Bar\n\nInhaber: Jimmy Rodríguez\nStrandstraße 12\n23730 Neustadt in Holstein\n\nTelefon: +49 4561 123456\nE-Mail: info@jimmys-tapasbar.de\n\nUmsatzsteuer-Identifikationsnummer: DE123456789\nHandelsregistereintrag: HRB 12345 Hamburg\n\nVerantwortlich für den Inhalt nach § 55 Abs. 2 RStV:\nJimmy Rodríguez\nStrandstraße 12\n23730 Neustadt in Holstein',
    'Jimmy Rodríguez',
    'Strandstraße 12, 23730 Neustadt in Holstein',
    '+49 4561 123456',
    'info@jimmys-tapasbar.de'
),
(
    '990e8400-e29b-41d4-a716-446655440000',
    'privacy',
    'Datenschutzerklärung',
    'Datenschutzerklärung für Jimmy''s Tapas Bar\n\n1. Verantwortlicher\nJimmy Rodríguez\nStrandstraße 12\n23730 Neustadt in Holstein\nE-Mail: datenschutz@jimmys-tapasbar.de\n\n2. Erhebung und Verarbeitung personenbezogener Daten\nWir erheben und verarbeiten personenbezogene Daten nur, soweit dies zur Bereitstellung unserer Dienstleistungen erforderlich ist.\n\n3. Cookies\nUnsere Website verwendet Cookies zur Verbesserung der Nutzererfahrung.\n\n4. Ihre Rechte\nSie haben das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung Ihrer personenbezogenen Daten.',
    'Jimmy Rodríguez',
    'Strandstraße 12, 23730 Neustadt in Holstein',
    '+49 4561 123456',
    'datenschutz@jimmys-tapasbar.de'
);
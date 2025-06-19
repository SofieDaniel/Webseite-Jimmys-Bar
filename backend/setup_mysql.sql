-- Jimmy's Tapas Bar MySQL Database Setup

USE jimmys_tapas_bar;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'editor', 'viewer') DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL
);

-- Status checks table
CREATE TABLE IF NOT EXISTS status_checks (
    id VARCHAR(36) PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR(36) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT FALSE,
    approved_by VARCHAR(50) NULL,
    approved_at DATETIME NULL
);

-- Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    image LONGTEXT NULL,
    details TEXT NULL,
    vegan BOOLEAN DEFAULT FALSE,
    vegetarian BOOLEAN DEFAULT FALSE,
    glutenfree BOOLEAN DEFAULT FALSE,
    order_index INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Contact messages table
CREATE TABLE IF NOT EXISTS contact_messages (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    responded BOOLEAN DEFAULT FALSE
);

-- Maintenance mode table
CREATE TABLE IF NOT EXISTS maintenance_mode (
    id VARCHAR(36) PRIMARY KEY,
    is_active BOOLEAN DEFAULT FALSE,
    message TEXT DEFAULT 'Die Website befindet sich derzeit im Wartungsmodus.',
    activated_by VARCHAR(50) NULL,
    activated_at DATETIME NULL
);

-- CMS Homepage content
CREATE TABLE IF NOT EXISTS homepage_content (
    id VARCHAR(36) PRIMARY KEY,
    hero_title VARCHAR(200) NOT NULL,
    hero_subtitle TEXT NOT NULL,
    hero_image VARCHAR(500) NOT NULL,
    features_data JSON NOT NULL,
    specialties_data JSON NOT NULL,
    delivery_data JSON NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL
);

-- CMS Locations content
CREATE TABLE IF NOT EXISTS locations (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(200) NOT NULL,
    page_description TEXT NOT NULL,
    locations_data JSON NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL
);

-- CMS About content
CREATE TABLE IF NOT EXISTS about_content (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(200) NOT NULL,
    hero_title VARCHAR(200) NOT NULL,
    hero_description TEXT NOT NULL,
    story_title VARCHAR(200) NOT NULL,
    story_content TEXT NOT NULL,
    story_image VARCHAR(500) NOT NULL,
    team_title VARCHAR(200) NOT NULL,
    team_members JSON NOT NULL,
    values_title VARCHAR(200) NOT NULL,
    values_data JSON NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Legal pages
CREATE TABLE IF NOT EXISTS legal_pages (
    id VARCHAR(36) PRIMARY KEY,
    page_type ENUM('imprint', 'privacy') NOT NULL,
    title VARCHAR(200) NOT NULL,
    content LONGTEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL
);

-- Enhanced locations page (new for v7)
CREATE TABLE IF NOT EXISTS standorte_enhanced (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(200) NOT NULL,
    page_subtitle TEXT NOT NULL,
    header_background VARCHAR(500) NOT NULL,
    neustadt_data JSON NOT NULL,
    grossenbrode_data JSON NOT NULL,
    info_section_data JSON NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL
);

-- Reviews page configuration (new for v7)
CREATE TABLE IF NOT EXISTS bewertungen_page (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(200) NOT NULL,
    page_subtitle TEXT NOT NULL,
    header_background VARCHAR(500) NOT NULL,
    reviews_section_title VARCHAR(200) NOT NULL,
    feedback_section_title VARCHAR(200) NOT NULL,
    feedback_note TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL
);

-- Enhanced about page (new for v7)
CREATE TABLE IF NOT EXISTS ueber_uns_enhanced (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(200) NOT NULL,
    page_subtitle TEXT NOT NULL,
    header_background VARCHAR(500) NOT NULL,
    jimmy_data JSON NOT NULL,
    values_section_data JSON NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL
);

-- Delivery information (new for v7)
CREATE TABLE IF NOT EXISTS delivery_info (
    id VARCHAR(36) PRIMARY KEY,
    delivery_time_min INT DEFAULT 30,
    delivery_time_max INT DEFAULT 45,
    minimum_order_value DECIMAL(5,2) DEFAULT 15.00,
    delivery_fee DECIMAL(4,2) DEFAULT 2.50,
    available_locations JSON NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL
);

-- Insert some sample data
INSERT IGNORE INTO menu_items (id, name, description, price, category, order_index, is_active) VALUES
('1', 'Gambas al Ajillo', 'Knoblauch-Garnelen in Olivenöl', '12,90 €', 'Tapas Warme', 1, TRUE),
('2', 'Patatas Bravas', 'Würzige Kartoffeln mit Bravas-Sauce', '7,50 €', 'Tapas Warme', 2, TRUE),
('3', 'Tortilla Española', 'Spanisches Kartoffel-Omelett', '8,90 €', 'Tapas Warme', 3, TRUE);

-- Insert default delivery info
INSERT IGNORE INTO delivery_info (id, available_locations, updated_by) VALUES
('delivery-1', '{"neustadt": {"name": "Neustadt", "available": true}, "grossenbrode": {"name": "Großenbrode", "available": true}}', 'system');

-- Insert approved reviews for testing
INSERT IGNORE INTO reviews (id, customer_name, rating, comment, is_approved) VALUES
('review-1', 'Maria González', 5, 'Fantastisches Essen und tolles Ambiente! Die Paella war perfekt.', TRUE),
('review-2', 'Hans Müller', 4, 'Sehr leckere Tapas und freundlicher Service. Gerne wieder!', TRUE),
('review-3', 'Sofia Russo', 5, 'Authentische spanische Küche an der Ostsee. Einfach wunderbar!', TRUE);
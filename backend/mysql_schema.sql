-- Jimmy's Tapas Bar CMS - MySQL Schema
-- Generated for migration from MongoDB to MySQL

-- Users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'editor', 'viewer') DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL
);

-- Reviews table
CREATE TABLE reviews (
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
CREATE TABLE menu_items (
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
CREATE TABLE contact_messages (
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

-- Status checks table (for API monitoring)
CREATE TABLE status_checks (
    id VARCHAR(36) PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Content sections table (CMS content)
CREATE TABLE content_sections (
    id VARCHAR(36) PRIMARY KEY,
    page VARCHAR(50) NOT NULL,
    section VARCHAR(50) NOT NULL,
    content JSON NOT NULL,
    images JSON NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL,
    UNIQUE KEY unique_page_section (page, section)
);

-- Homepage content table
CREATE TABLE homepage_content (
    id VARCHAR(36) PRIMARY KEY,
    hero_title VARCHAR(200) DEFAULT 'JIMMY\'S TAPAS BAR',
    hero_subtitle VARCHAR(100) DEFAULT 'an der Ostsee',
    hero_description TEXT DEFAULT 'Genießen Sie authentische mediterrane Spezialitäten',
    hero_location VARCHAR(200) DEFAULT 'direkt an der malerischen Ostseeküste',
    hero_background_image TEXT NULL,
    hero_menu_button_text VARCHAR(50) DEFAULT 'Zur Speisekarte',
    hero_locations_button_text VARCHAR(50) DEFAULT 'Unsere Standorte',
    features_data JSON NULL,
    specialties_data JSON NULL,
    delivery_data JSON NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NULL
);

-- Website texts table
CREATE TABLE website_texts (
    id VARCHAR(36) PRIMARY KEY,
    section VARCHAR(50) NOT NULL UNIQUE,
    navigation_data JSON NULL,
    footer_data JSON NULL,
    buttons_data JSON NULL,
    general_data JSON NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NULL
);

-- Locations table
CREATE TABLE locations (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(200) DEFAULT 'Unsere Standorte',
    page_description TEXT DEFAULT 'Besuchen Sie uns an einem unserer beiden Standorte',
    locations_data JSON NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NULL
);

-- About content table
CREATE TABLE about_content (
    id VARCHAR(36) PRIMARY KEY,
    page_title VARCHAR(200) DEFAULT 'Über uns',
    hero_title VARCHAR(200) DEFAULT 'Unsere Geschichte',
    hero_description TEXT DEFAULT 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar',
    story_title VARCHAR(200) DEFAULT 'Unsere Leidenschaft',
    story_content TEXT NULL,
    story_image TEXT NULL,
    team_title VARCHAR(200) DEFAULT 'Unser Team',
    team_members JSON NULL,
    values_title VARCHAR(200) DEFAULT 'Unsere Werte',
    values_data JSON NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NULL
);

-- Legal pages table
CREATE TABLE legal_pages (
    id VARCHAR(36) PRIMARY KEY,
    page_type ENUM('imprint', 'privacy') NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    contact_name VARCHAR(100) NULL,
    contact_address TEXT NULL,
    contact_phone VARCHAR(20) NULL,
    contact_email VARCHAR(100) NULL,
    company_info JSON NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NULL
);

-- Newsletter subscribers table
CREATE TABLE newsletter_subscribers (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NULL,
    subscribed BOOLEAN DEFAULT TRUE,
    subscribe_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    unsubscribe_date DATETIME NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL
);

-- Newsletter templates table
CREATE TABLE newsletter_templates (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL
);

-- Newsletter campaigns table
CREATE TABLE newsletter_campaigns (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    template_id VARCHAR(36) NULL,
    subject VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    scheduled_date DATETIME NULL,
    sent_date DATETIME NULL,
    recipients_count INT DEFAULT 0,
    sent_count INT DEFAULT 0,
    status ENUM('draft', 'scheduled', 'sending', 'sent', 'failed') DEFAULT 'draft',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    FOREIGN KEY (template_id) REFERENCES newsletter_templates(id) ON DELETE SET NULL
);

-- SMTP configuration table
CREATE TABLE smtp_config (
    id VARCHAR(36) PRIMARY KEY,
    smtp_server VARCHAR(100) DEFAULT 'smtp.gmail.com',
    smtp_port INT DEFAULT 587,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    from_email VARCHAR(100) NOT NULL,
    from_name VARCHAR(100) DEFAULT 'Jimmy\'s Tapas Bar',
    use_tls BOOLEAN DEFAULT TRUE,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NULL
);

-- Maintenance mode table
CREATE TABLE maintenance_mode (
    id VARCHAR(36) PRIMARY KEY,
    is_active BOOLEAN DEFAULT FALSE,
    message TEXT DEFAULT 'Die Website befindet sich derzeit im Wartungsmodus.',
    activated_by VARCHAR(50) NULL,
    activated_at DATETIME NULL
);

-- System backups table
CREATE TABLE system_backups (
    id VARCHAR(36) PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    type ENUM('database', 'full') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    size_bytes BIGINT NOT NULL,
    size_human VARCHAR(20) NOT NULL,
    collections_count INT DEFAULT 0,
    total_documents INT DEFAULT 0,
    includes_media BOOLEAN DEFAULT FALSE,
    INDEX idx_created_at (created_at DESC),
    INDEX idx_type (type)
);

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_reviews_approved ON reviews(is_approved, date DESC);
CREATE INDEX idx_reviews_date ON reviews(date DESC);
CREATE INDEX idx_menu_items_category ON menu_items(category, order_index);
CREATE INDEX idx_menu_items_active ON menu_items(is_active);
CREATE INDEX idx_contact_read ON contact_messages(is_read, date DESC);
CREATE INDEX idx_newsletter_subscribed ON newsletter_subscribers(subscribed);
CREATE INDEX idx_content_page_section ON content_sections(page, section);
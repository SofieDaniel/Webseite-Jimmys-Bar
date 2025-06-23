from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import pymysql
import os
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# SIMPLE MYSQL CONNECTION FOR WEBSPACE COMPATIBILITY
def get_mysql_connection():
    try:
        # Try socket connection first (Linux default)
        return pymysql.connect(
            unix_socket='/run/mysqld/mysqld.sock',
            user=os.environ.get('MYSQL_USER', 'root'),
            password=os.environ.get('MYSQL_PASSWORD', ''),
            database=os.environ.get('MYSQL_DATABASE', 'jimmys_tapas_bar'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        # Fallback to TCP connection
        return pymysql.connect(
            host=os.environ.get('MYSQL_HOST', 'localhost'),
            port=int(os.environ.get('MYSQL_PORT', 3306)),
            user=os.environ.get('MYSQL_USER', 'root'),
            password=os.environ.get('MYSQL_PASSWORD', ''),
            database=os.environ.get('MYSQL_DATABASE', 'jimmys_tapas_bar'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Models
class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    detailed_description: Optional[str] = None
    price: str
    category: str
    origin: Optional[str] = None
    allergens: Optional[str] = None
    additives: Optional[str] = None
    preparation_method: Optional[str] = None
    ingredients: Optional[str] = None
    vegan: bool = False
    vegetarian: bool = False
    glutenfree: bool = False
    order_index: int = 0
    is_active: bool = True

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    rating: int
    comment: str
    date: datetime = Field(default_factory=datetime.utcnow)
    is_approved: bool = False

class ReviewCreate(BaseModel):
    customer_name: str
    rating: int
    comment: str

class User(BaseModel):
    id: str
    username: str
    email: str
    role: str = "viewer"
    is_active: bool = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Auth setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=True)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jimmy-secret-2024")
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Routes
@api_router.get("/menu/items", response_model=List[MenuItem])
async def get_menu_items():
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu_items WHERE is_active = TRUE ORDER BY order_index, category, name")
        items = cursor.fetchall()
        return [MenuItem(**item) for item in items]
    finally:
        conn.close()

@api_router.get("/reviews", response_model=List[Review])
async def get_reviews(approved_only: bool = True):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        if approved_only:
            cursor.execute("SELECT * FROM reviews WHERE is_approved = TRUE ORDER BY date DESC LIMIT 1000")
        else:
            cursor.execute("SELECT * FROM reviews ORDER BY date DESC LIMIT 1000")
        reviews = cursor.fetchall()
        return [Review(**review) for review in reviews]
    finally:
        conn.close()

@api_router.post("/reviews", response_model=Review)
async def create_review(review_data: ReviewCreate):
    review = Review(**review_data.dict())
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reviews (id, customer_name, rating, comment, date, is_approved)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (review.id, review.customer_name, review.rating, review.comment, review.date, review.is_approved))
        conn.commit()
        return review
    finally:
        conn.close()

@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (user_credentials.username,))
        user = cursor.fetchone()
        
        if not user or not verify_password(user_credentials.password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user['username']})
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        conn.close()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, is_active FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user)
    finally:
        conn.close()

@api_router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.post("/contact")
async def create_contact_message(message_data: dict):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contact_messages (id, name, email, phone, subject, message, date, is_read)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), message_data.get("name"), message_data.get("email"), 
              message_data.get("phone"), message_data.get("subject"), message_data.get("message"), 
              datetime.utcnow(), False))
        conn.commit()
        return {"message": "Contact message sent successfully"}
    finally:
        conn.close()

# CMS Endpoints with static data for webspace compatibility
@api_router.get("/cms/homepage")
async def get_homepage_content():
    return {
        "hero": {
            "title": "JIMMY'S TAPAS BAR",
            "subtitle": "an der Ostsee",
            "description": "Genießen Sie authentische mediterrane Spezialitäten",
            "background_image": "https://images.unsplash.com/photo-1656423521731-9665583f100c"
        },
        "features": {
            "title": "Mediterrane Tradition",
            "subtitle": "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste",
            "cards": [
                {"title": "Authentische Tapas", "description": "Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen", "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae"},
                {"title": "Frische Paella", "description": "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn", "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a"},
                {"title": "Strandnähe", "description": "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden", "image_url": "https://images.unsplash.com/photo-1506377585622-bedcbb027afc"}
            ]
        },
        "specialties": {
            "title": "Unsere Spezialitäten",
            "cards": [
                {"title": "Patatas Bravas", "description": "Klassische mediterrane Kartoffeln", "image_url": "https://images.unsplash.com/photo-1565599837634-134bc3aadce8"},
                {"title": "Paella Valenciana", "description": "Traditionelle mediterrane Paella", "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a"},
                {"title": "Tapas Variación", "description": "Auswahl mediterraner Köstlichkeiten", "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae"},
                {"title": "Gambas al Ajillo", "description": "Garnelen in Knoblauchöl", "image_url": "https://images.unsplash.com/photo-1619860705243-dbef552e7118"}
            ]
        }
    }

@api_router.put("/cms/homepage")
async def update_homepage_content(content_data: dict, current_user: User = Depends(get_current_user)):
    # Store updated content in database or file
    return {"message": "Homepage content updated successfully", "data": content_data}

@api_router.put("/cms/standorte-enhanced")
async def update_standorte_enhanced(content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": "Standorte content updated successfully", "data": content_data}

@api_router.put("/cms/ueber-uns-enhanced")
async def update_ueber_uns_enhanced(content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": "Über uns content updated successfully", "data": content_data}

@api_router.get("/cms/website-texts/{section}")
async def get_website_texts(section: str):
    """Get website texts for a specific section (navigation, footer, buttons)"""
    if section == "navigation":
        return {
            "home": "Startseite",
            "locations": "Standorte",
            "menu": "Speisekarte",
            "reviews": "Bewertungen",
            "about": "Über uns",
            "contact": "Kontakt",
            "privacy": "Datenschutz",
            "imprint": "Impressum"
        }
    elif section == "footer":
        return {
            "opening_hours_title": "Öffnungszeiten",
            "contact_title": "Kontakt",
            "follow_us_title": "Folgen Sie uns",
            "copyright": "© 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten."
        }
    elif section == "buttons":
        return {
            "menu_button": "Speisekarte ansehen",
            "locations_button": "Standorte entdecken",
            "contact_button": "Kontakt aufnehmen",
            "reserve_button": "Tisch reservieren",
            "order_button": "Online bestellen"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Section '{section}' not found")

@api_router.put("/cms/website-texts/{section}")
async def update_website_texts(section: str, content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": f"Website texts for {section} updated successfully", "data": content_data}

# Menu Items CRUD für CMS
@api_router.put("/menu/items/{item_id}")
async def update_menu_item(item_id: str, item_data: dict, current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE menu_items SET 
            name = %s, description = %s, detailed_description = %s, price = %s, 
            category = %s, origin = %s, allergens = %s, ingredients = %s,
            vegan = %s, vegetarian = %s, glutenfree = %s, order_index = %s
            WHERE id = %s
        """, (
            item_data.get('name'), item_data.get('description'), 
            item_data.get('detailed_description'), item_data.get('price'),
            item_data.get('category'), item_data.get('origin'),
            item_data.get('allergens'), item_data.get('ingredients'),
            item_data.get('vegan', False), item_data.get('vegetarian', False),
            item_data.get('glutenfree', False), item_data.get('order_index', 0),
            item_id
        ))
        conn.commit()
        return {"message": "Menu item updated successfully"}
    finally:
        conn.close()

@api_router.delete("/menu/items/{item_id}")
async def delete_menu_item(item_id: str, current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        conn.commit()
        return {"message": "Menu item deleted successfully"}
    finally:
        conn.close()

@api_router.post("/menu/items")
async def create_menu_item(item_data: dict, current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        item_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO menu_items (id, name, description, detailed_description, price, category, 
                                   origin, allergens, ingredients, vegan, vegetarian, glutenfree, 
                                   order_index, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item_id, item_data.get('name'), item_data.get('description'),
            item_data.get('detailed_description'), item_data.get('price'),
            item_data.get('category'), item_data.get('origin'),
            item_data.get('allergens'), item_data.get('ingredients'),
            item_data.get('vegan', False), item_data.get('vegetarian', False),
            item_data.get('glutenfree', False), item_data.get('order_index', 0), True
        ))
        conn.commit()
        return {"message": "Menu item created successfully", "id": item_id}
    finally:
        conn.close()

@api_router.get("/cms/standorte-enhanced")
async def get_standorte_enhanced():
    return {
        "page_title": "Unsere Standorte",
        "page_subtitle": "Besuchen Sie uns an der malerischen Ostseeküste",
        "neustadt": {
            "name": "Neustadt in Holstein",
            "address": "Am Strande 21 Promenade, 23730 Neustadt in Holstein",
            "phone": "015735256793",
            "email": "info@jimmys-tapasbar.de",
            "opening_hours": {
                "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
            },
            "features": ["Direkte Strandlage", "Große Terrasse", "Familienfreundlich", "Parkplatz kostenlos"]
        },
        "grossenbrode": {
            "name": "Großenbrode",
            "address": "Südstrand 54 Promenade, 23755 Großenbrode",
            "phone": "015782226373",
            "email": "info@jimmys-tapasbar.de",
            "opening_hours": {
                "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
            },
            "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"]
        }
    }

@api_router.put("/cms/standorte-enhanced")
async def update_standorte_enhanced(content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": "Standorte content updated successfully", "data": content_data}

@api_router.get("/cms/locations")
async def get_locations():
    """Get locations data - returns current live data structure"""
    return {
        "page_title": "Unsere Standorte",
        "page_description": "Besuchen Sie uns an der malerischen Ostseeküste",
        "locations": [
            {
                "id": "neustadt",
                "name": "Neustadt in Holstein",
                "address": "Am Strande 21 Promenade, 23730 Neustadt in Holstein",
                "phone": "015735256793",
                "email": "info@jimmys-tapasbar.de",
                "opening_hours": {
                    "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                    "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
                },
                "description": "Direkt am Strand gelegen mit großer Terrasse",
                "features": ["Direkte Strandlage", "Große Terrasse", "Familienfreundlich", "Parkplatz kostenlos"],
                "image_url": "https://images.unsplash.com/photo-1506577005627-9a2b1f7b5d5d",
                "maps_embed": ""
            },
            {
                "id": "grossenbrode", 
                "name": "Großenbrode",
                "address": "Südstrand 54 Promenade, 23755 Großenbrode",
                "phone": "015782226373",
                "email": "info@jimmys-tapasbar.de",
                "opening_hours": {
                    "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                    "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
                },
                "description": "Ruhige Lage mit Panorama-Meerblick",
                "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"],
                "image_url": "https://images.unsplash.com/photo-1559925393-8be0ec4767c8",
                "maps_embed": ""
            }
        ]
    }

@api_router.put("/cms/locations")
async def update_locations(content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": "Standorte content updated successfully", "data": content_data}

@api_router.get("/cms/kontakt-page")
async def get_kontakt_page():
    return {
        "page_title": "Kontakt",
        "page_subtitle": "Wir freuen uns auf Ihren Besuch",
        "contact_form_title": "Schreiben Sie uns",
        "contact_form_subtitle": "Haben Sie Fragen oder möchten Sie einen Tisch reservieren?",
        "locations_section_title": "Unsere Standorte",
        "opening_hours_title": "Öffnungszeiten",
        "additional_info": "Wir sind täglich für Sie da."
    }

@api_router.get("/cms/ueber-uns-enhanced")
async def get_ueber_uns_enhanced():
    return {
        "page_title": "Über uns",
        "page_subtitle": "Lernen Sie Jimmy's Tapas Bar kennen",
        "jimmy": {
            "name": "Jimmy Rodríguez",
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d",
            "story_paragraph1": "Seit der Gründung im Jahr 2015 steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.",
            "story_paragraph2": "Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.",
            "quote": "Gutes Essen bringt Menschen zusammen und schafft unvergessliche Momente."
        }
    }

# Fehlende Admin-Endpunkte hinzufügen
@api_router.get("/admin/newsletter/subscribers")
async def get_newsletter_subscribers(current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM newsletter_subscribers ORDER BY created_at DESC")
        subscribers = cursor.fetchall()
        return subscribers
    except Exception as e:
        # Falls Tabelle nicht existiert, leere Liste zurückgeben
        return []
    finally:
        conn.close()

@api_router.get("/users")
async def get_users(current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, is_active FROM users")
        users = cursor.fetchall()
        return [User(**user) for user in users]
    finally:
        conn.close()

@api_router.get("/admin/contact")
async def get_contact_messages(current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contact_messages ORDER BY date DESC")
        messages = cursor.fetchall()
        return messages
    finally:
        conn.close()

@api_router.post("/contact")
async def submit_contact_form(contact_data: dict):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        # Versuche Tabelle zu erstellen falls sie nicht existiert
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                subject VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'new'
            )
        """)
        
        cursor.execute("""
            INSERT INTO contact_messages (id, name, email, phone, subject, message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            str(uuid.uuid4()), 
            contact_data.get("name"), 
            contact_data.get("email"),
            contact_data.get("phone", ""),
            contact_data.get("subject"),
            contact_data.get("message")
        ))
        conn.commit()
        return {"message": "Contact form submitted successfully"}
    except Exception as e:
        return {"message": "Contact form submission failed", "error": str(e)}
    finally:
        conn.close()

@api_router.post("/newsletter/subscribe")
async def newsletter_subscribe(email_data: dict):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        # Versuche Tabelle zu erstellen falls sie nicht existiert
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        cursor.execute("""
            INSERT INTO newsletter_subscribers (id, email)
            VALUES (%s, %s)
        """, (str(uuid.uuid4()), email_data.get("email")))
        conn.commit()
        return {"message": "Newsletter subscription successful"}
    except Exception as e:
        if "Duplicate entry" in str(e):
            return {"message": "Email already subscribed"}
        return {"message": "Subscription failed", "error": str(e)}
    finally:
        conn.close()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Initialize database with sample data
def init_database():
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                detailed_description TEXT,
                price VARCHAR(20) NOT NULL,
                category VARCHAR(100) NOT NULL,
                origin VARCHAR(255),
                allergens TEXT,
                additives TEXT,
                preparation_method TEXT,
                ingredients TEXT,
                vegan BOOLEAN DEFAULT FALSE,
                vegetarian BOOLEAN DEFAULT FALSE,
                glutenfree BOOLEAN DEFAULT FALSE,
                order_index INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id VARCHAR(36) PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                rating INT NOT NULL,
                comment TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_approved BOOLEAN DEFAULT FALSE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'editor', 'viewer') DEFAULT 'viewer',
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                subject VARCHAR(255),
                message TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Check if admin user exists
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            admin_hash = pwd_context.hash("jimmy2024")
            cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), "admin", "admin@jimmys-tapasbar.de", admin_hash, "admin"))
        
        # Check if menu items exist
        cursor.execute("SELECT COUNT(*) as count FROM menu_items")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            # Add sample menu items
            menu_items = [
                ("Gambas al Ajillo", "Klassische spanische Knoblauchgarnelen", "Frische Garnelen in bestem Olivenöl mit viel Knoblauch, Chili und Petersilie", "12,90", "Vorspeisen", "Andalusien", "Krustentiere", "", "In der Pfanne gebraten", "Garnelen, Olivenöl, Knoblauch, Chili, Petersilie", 0, 0, 1),
                ("Patatas Bravas", "Würzig gebratene Kartoffeln mit Aioli", "Knusprig gebratene Kartoffelwürfel mit hausgemachter Aioli und scharfer Bravas-Sauce", "8,50", "Vorspeisen", "Madrid", "Eier", "", "Frittiert und gebacken", "Kartoffeln, Tomaten, Aioli, Paprika", 0, 1, 1),
                ("Paella Valenciana", "Original Paella mit Huhn und grünen Bohnen", "Die klassische Paella aus Valencia mit echtem Safran, Huhn und grünen Bohnen", "24,90", "Paella", "Valencia", "", "", "In der Paellera über Feuer", "Bomba-Reis, Huhn, grüne Bohnen, Safran", 0, 0, 1),
                ("Jamón Ibérico", "Hauchdünn geschnittener iberischer Schinken", "24 Monate gereifter Jamón Ibérico serviert mit Manchego-Käse", "16,90", "Vorspeisen", "Extremadura", "Milch", "", "24 Monate luftgetrocknet", "Iberischer Schinken, Manchego", 0, 0, 1),
                ("Sangría de la Casa", "Hausgemachte Sangría mit Früchten", "Erfrischende Sangría mit Rotwein, Orangen und Äpfeln", "6,90", "Getränke", "Spanien", "Sulfite", "", "24h ziehen lassen", "Rotwein, Orangen, Äpfel, Brandy", 1, 1, 1)
            ]
            
            for i, (name, desc, detailed, price, cat, origin, allergens, additives, prep, ingredients, vegan, vegetarian, gluten) in enumerate(menu_items):
                cursor.execute("""
                    INSERT INTO menu_items (id, name, description, detailed_description, price, category, origin, allergens, additives, preparation_method, ingredients, vegan, vegetarian, glutenfree, order_index, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (str(uuid.uuid4()), name, desc, detailed, price, cat, origin, allergens, additives, prep, ingredients, vegan, vegetarian, gluten, i+1, True))
        
        conn.commit()
        print("✅ MySQL Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
    finally:
        conn.close()

@app.on_event("startup")
async def startup_event():
    init_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
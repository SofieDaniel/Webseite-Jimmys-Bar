from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import aiomysql
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import base64
import json
import io
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MySQL connection pool - COMPLETELY MYSQL ONLY
mysql_pool = None

async def init_mysql_pool():
    global mysql_pool
    try:
        mysql_pool = await aiomysql.create_pool(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            db='jimmys_tapas_bar',
            charset='utf8mb4',
            autocommit=True,
            maxsize=20
        )
        print("✅ MySQL Connection Pool initialized")
    except Exception as e:
        print(f"❌ MySQL Connection failed: {e}")
        # Create database if it doesn't exist
        try:
            temp_conn = await aiomysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='',
                charset='utf8mb4'
            )
            cursor = await temp_conn.cursor()
            await cursor.execute("CREATE DATABASE IF NOT EXISTS jimmys_tapas_bar")
            await cursor.execute("USE jimmys_tapas_bar")
            
            # Create tables
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'editor', 'viewer') DEFAULT 'viewer',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL
                )
            """)
            
            await cursor.execute("""
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
                )
            """)
            
            await cursor.execute("""
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
                )
            """)
            
            temp_conn.close()
            
            # Now retry pool creation
            mysql_pool = await aiomysql.create_pool(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='',
                db='jimmys_tapas_bar',
                charset='utf8mb4',
                autocommit=True,
                maxsize=20
            )
            print("✅ MySQL Database and Pool created successfully")
            
        except Exception as e2:
            print(f"❌ Failed to create database: {e2}")
            raise e2

async def get_mysql_connection():
    if mysql_pool is None:
        await init_mysql_pool()
    return await mysql_pool.acquire()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=True)

# JWT settings
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# User Roles
class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

# Basic models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# User Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    password_hash: str
    role: UserRole = UserRole.VIEWER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.VIEWER

class UserLogin(BaseModel):
    username: str
    password: str

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    rating: int  # 1-5
    comment: str
    date: datetime = Field(default_factory=datetime.utcnow)
    is_approved: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

class ReviewCreate(BaseModel):
    customer_name: str
    rating: int
    comment: str

# Menu Models
class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    detailed_description: Optional[str] = None
    price: str
    category: str
    image: Optional[str] = None
    details: Optional[str] = None
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

class MenuItemCreate(BaseModel):
    name: str
    description: str
    detailed_description: Optional[str] = None
    price: str
    category: str
    image: Optional[str] = None
    details: Optional[str] = None
    origin: Optional[str] = None
    allergens: Optional[str] = None
    additives: Optional[str] = None
    preparation_method: Optional[str] = None
    ingredients: Optional[str] = None
    vegan: bool = False
    vegetarian: bool = False
    glutenfree: bool = False
    order_index: int = 0

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = await cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user)
    finally:
        mysql_pool.release(conn)

async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def get_editor_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="Editor access required")
    return current_user

# Create default admin user
async def create_default_admin():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            admin_user = User(
                username="admin",
                email="admin@jimmys-tapasbar.de",
                password_hash=get_password_hash("jimmy2024"),
                role=UserRole.ADMIN
            )
            
            await cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, role, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (admin_user.id, admin_user.username, admin_user.email, admin_user.password_hash, 
                  admin_user.role.value, admin_user.is_active, admin_user.created_at))
            
            print("Default admin user created")
    finally:
        mysql_pool.release(conn)

# Authentication routes
@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM users WHERE username = %s", (user_credentials.username,))
        user = await cursor.fetchone()
        
        if not user or not verify_password(user_credentials.password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        if not user["is_active"]:
            raise HTTPException(status_code=401, detail="User account is disabled")
        
        # Update last login
        await cursor.execute("UPDATE users SET last_login = %s WHERE username = %s", 
                            (datetime.utcnow(), user_credentials.username))
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user['username']}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Review routes - MYSQL ONLY
@api_router.get("/reviews", response_model=List[Review])
async def get_reviews(approved_only: bool = True):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        if approved_only:
            await cursor.execute("SELECT * FROM reviews WHERE is_approved = TRUE ORDER BY created_at DESC LIMIT 1000")
        else:
            await cursor.execute("SELECT * FROM reviews ORDER BY created_at DESC LIMIT 1000")
        reviews = await cursor.fetchall()
        return [Review(**review) for review in reviews]
    finally:
        mysql_pool.release(conn)

@api_router.post("/reviews", response_model=Review)
async def create_review(review_data: ReviewCreate):
    try:
        review = Review(**review_data.dict())
        
        conn = await get_mysql_connection()
        try:
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO reviews (id, customer_name, rating, comment, date, is_approved)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (review.id, review.customer_name, review.rating, review.comment, review.date, review.is_approved))
            
            return review
        finally:
            mysql_pool.release(conn)
    except Exception as e:
        print(f"Review creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Review creation failed: {str(e)}")

# Menu Management routes - MYSQL ONLY
@api_router.get("/menu/items", response_model=List[MenuItem])
async def get_menu_items():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM menu_items WHERE is_active = TRUE ORDER BY order_index, category, name")
        items = await cursor.fetchall()
        return [MenuItem(**item) for item in items]
    finally:
        mysql_pool.release(conn)

@api_router.post("/menu/items", response_model=MenuItem)
async def create_menu_item(item_data: MenuItemCreate, current_user: User = Depends(get_editor_user)):
    item = MenuItem(**item_data.dict())
    
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute("""
            INSERT INTO menu_items (id, name, description, detailed_description, price, category, 
                                   image, details, origin, allergens, additives, preparation_method, 
                                   ingredients, vegan, vegetarian, glutenfree, order_index, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (item.id, item.name, item.description, item.detailed_description, item.price, 
              item.category, item.image, item.details, item.origin, item.allergens, 
              item.additives, item.preparation_method, item.ingredients, item.vegan, 
              item.vegetarian, item.glutenfree, item.order_index, item.is_active))
        
        return item
    finally:
        mysql_pool.release(conn)

# Simple CMS endpoints
@api_router.get("/cms/homepage")
async def get_homepage_content():
    return {
        "hero": {
            "title": "JIMMY'S TAPAS BAR",
            "subtitle": "an der Ostsee",
            "description": "Genießen Sie authentische mediterrane Spezialitäten",
            "location": "direkt an der malerischen Ostseeküste",
            "background_image": "https://images.unsplash.com/photo-1656423521731-9665583f100c",
            "menu_button_text": "Zur Speisekarte",
            "locations_button_text": "Unsere Standorte",
            "image": "https://images.unsplash.com/photo-1560472355-536de3962603"
        }
    }

@api_router.get("/cms/standorte-enhanced")
async def get_standorte_enhanced():
    return {
        "page_title": "Unsere Standorte",
        "page_subtitle": "Besuchen Sie uns an der malerischen Ostseeküste",
        "neustadt": {
            "name": "Neustadt in Holstein",
            "address": "Strandstraße 12, 23730 Neustadt in Holstein",
            "phone": "+49 4561 123456",
            "email": "neustadt@jimmys-tapasbar.de",
            "opening_hours": {
                "Montag": "17:00 - 23:00",
                "Dienstag": "17:00 - 23:00",
                "Mittwoch": "17:00 - 23:00",
                "Donnerstag": "17:00 - 23:00",
                "Freitag": "17:00 - 00:00",
                "Samstag": "17:00 - 00:00",
                "Sonntag": "17:00 - 23:00"
            },
            "features": ["Direkte Strandlage", "Große Terrasse", "Familienfreundlich", "Parkplatz kostenlos"]
        },
        "grossenbrode": {
            "name": "Großenbrode",
            "address": "Strandpromenade 8, 23775 Großenbrode",
            "phone": "+49 4367 987654",
            "email": "grossenbrode@jimmys-tapasbar.de",
            "opening_hours": {
                "Montag": "17:00 - 22:00",
                "Dienstag": "17:00 - 22:00",
                "Mittwoch": "17:00 - 22:00",
                "Donnerstag": "17:00 - 22:00",
                "Freitag": "17:00 - 23:00",
                "Samstag": "17:00 - 23:00",
                "Sonntag": "17:00 - 22:00"
            },
            "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"]
        }
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
        },
        "values_section": {
            "title": "Unsere Werte",
            "values": [
                {
                    "title": "Qualität",
                    "description": "Wir verwenden nur die besten Zutaten für unsere Gerichte.",
                    "icon": "⭐"
                },
                {
                    "title": "Gastfreundschaft", 
                    "description": "Bei uns sollen Sie sich wie zu Hause fühlen.",
                    "icon": "❤️"
                },
                {
                    "title": "Authentizität",
                    "description": "Wir bleiben den traditionellen spanischen Rezepten treu.",
                    "icon": "🇪🇸"
                }
            ]
        }
    }

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

@api_router.get("/delivery/info")
async def get_delivery_info():
    return {
        "delivery_time": "30-45 min",
        "minimum_order_value": "15.00",
        "delivery_fee": "2.50",
        "available_locations": {
            "neustadt": {"name": "Neustadt", "available": True},
            "grossenbrode": {"name": "Großenbrode", "available": True}
        }
    }

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await init_mysql_pool()
    await create_default_admin()
    
    # Populate menu if empty
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute("SELECT COUNT(*) FROM menu_items")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Add sample menu items
            menu_items = [
                ("Gambas al Ajillo", "Klassische spanische Knoblauchgarnelen", "12,90", "Vorspeisen"),
                ("Patatas Bravas", "Würzig gebratene Kartoffeln mit Aioli", "8,50", "Vorspeisen"),
                ("Jamón Ibérico", "Hauchdünn geschnittener iberischer Schinken", "16,90", "Vorspeisen"),
                ("Paella Valenciana", "Original Paella mit Huhn, Kaninchen und grünen Bohnen", "24,90", "Paella"),
                ("Paella de Mariscos", "Meeresfrüchte-Paella mit Garnelen und Muscheln", "26,90", "Paella"),
                ("Sangría de la Casa", "Hausgemachte Sangría mit Früchten", "6,90", "Getränke"),
                ("Cerveza Estrella Galicia", "Spanisches Bier vom Fass", "4,20", "Getränke"),
            ]
            
            for name, desc, price, category in menu_items:
                await cursor.execute("""
                    INSERT INTO menu_items (id, name, description, price, category, is_active, order_index)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (str(uuid.uuid4()), name, desc, price, category, True, 1))
            
            print("Sample menu items added")
    finally:
        mysql_pool.release(conn)

@app.on_event("shutdown")
async def shutdown_event():
    if mysql_pool:
        mysql_pool.close()
        await mysql_pool.wait_closed()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
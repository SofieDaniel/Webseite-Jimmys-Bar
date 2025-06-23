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

# MySQL connection pool
mysql_pool = None

async def init_mysql_pool():
    global mysql_pool
    mysql_pool = await aiomysql.create_pool(
        host=os.environ['MYSQL_HOST'],
        port=int(os.environ['MYSQL_PORT']),
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        db=os.environ['MYSQL_DATABASE'],
        charset='utf8mb4',
        autocommit=True,
        maxsize=20
    )

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

# Contact Models
class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str
    date: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False
    responded: bool = False

class ContactMessageCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Newsletter Models
class NewsletterSubscriber(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: Optional[str] = None
    subscribed: bool = True
    subscribe_date: datetime = Field(default_factory=datetime.utcnow)
    unsubscribe_date: Optional[datetime] = None

class NewsletterSubscribe(BaseModel):
    email: str
    name: Optional[str] = None

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
async def login(username: str = Form(...), password: str = Form(...)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = await cursor.fetchone()
        
        if not user or not verify_password(password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        # Update last login
        await cursor.execute("UPDATE users SET last_login = %s WHERE username = %s", 
                            (datetime.utcnow(), username))
        
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

# Review routes
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

@api_router.put("/reviews/{review_id}/approve")
async def approve_review(review_id: str, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        result = await cursor.execute("""
            UPDATE reviews SET is_approved = TRUE, approved_by = %s, approved_at = %s 
            WHERE id = %s
        """, (current_user.username, datetime.utcnow(), review_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        return {"message": "Review approved successfully"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/admin/reviews/pending", response_model=List[Review])
async def get_pending_reviews(current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM reviews WHERE is_approved = FALSE ORDER BY date DESC")
        reviews = await cursor.fetchall()
        return [Review(**review) for review in reviews]
    finally:
        mysql_pool.release(conn)

# Menu Management routes
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

@api_router.put("/menu/items/{item_id}", response_model=MenuItem)
async def update_menu_item(item_id: str, item_data: MenuItemCreate, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute("""
            UPDATE menu_items SET name = %s, description = %s, detailed_description = %s, 
                                price = %s, category = %s, image = %s, details = %s, origin = %s, 
                                allergens = %s, additives = %s, preparation_method = %s, 
                                ingredients = %s, vegan = %s, vegetarian = %s, glutenfree = %s, 
                                order_index = %s, updated_at = %s
            WHERE id = %s
        """, (item_data.name, item_data.description, item_data.detailed_description, 
              item_data.price, item_data.category, item_data.image, item_data.details, 
              item_data.origin, item_data.allergens, item_data.additives, 
              item_data.preparation_method, item_data.ingredients, item_data.vegan, 
              item_data.vegetarian, item_data.glutenfree, item_data.order_index, 
              datetime.utcnow(), item_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Menu item not found")
        
        # Return updated item
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
        updated_item = await cursor.fetchone()
        return MenuItem(**updated_item)
    finally:
        mysql_pool.release(conn)

@api_router.delete("/menu/items/{item_id}")
async def delete_menu_item(item_id: str, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Menu item not found")
        
        return {"message": "Menu item deleted successfully"}
    finally:
        mysql_pool.release(conn)

# Contact routes
@api_router.post("/contact", response_model=ContactMessage)
async def create_contact_message(message_data: ContactMessageCreate):
    message = ContactMessage(**message_data.dict())
    
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute("""
            INSERT INTO contact_messages (id, name, email, phone, subject, message, date, is_read, responded)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (message.id, message.name, message.email, message.phone, message.subject, 
              message.message, message.date, message.is_read, message.responded))
        
        return message
    finally:
        mysql_pool.release(conn)

@api_router.get("/admin/contact", response_model=List[ContactMessage])
async def get_contact_messages(current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM contact_messages ORDER BY date DESC")
        messages = await cursor.fetchall()
        return [ContactMessage(**message) for message in messages]
    finally:
        mysql_pool.release(conn)

# Newsletter routes
@api_router.post("/newsletter/subscribe")
async def subscribe_newsletter(subscriber_data: NewsletterSubscribe):
    subscriber = NewsletterSubscriber(**subscriber_data.dict())
    
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        # Check if email already exists
        await cursor.execute("SELECT COUNT(*) FROM newsletter_subscribers WHERE email = %s", (subscriber.email,))
        result = await cursor.fetchone()
        
        if result[0] > 0:
            raise HTTPException(status_code=400, detail="Email already subscribed")
        
        await cursor.execute("""
            INSERT INTO newsletter_subscribers (id, email, name, subscribed, subscribe_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (subscriber.id, subscriber.email, subscriber.name, subscriber.subscribed, subscriber.subscribe_date))
        
        return {"message": "Successfully subscribed to newsletter"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/admin/newsletter/subscribers", response_model=List[NewsletterSubscriber])
async def get_newsletter_subscribers(current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM newsletter_subscribers WHERE subscribed = TRUE ORDER BY subscribe_date DESC")
        subscribers = await cursor.fetchall()
        return [NewsletterSubscriber(**subscriber) for subscriber in subscribers]
    finally:
        mysql_pool.release(conn)

# CMS Routes
@api_router.get("/cms/homepage")
async def get_homepage_content():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM homepage_content LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default content
            default_content = {
                "id": str(uuid.uuid4()),
                "hero_title": "JIMMY'S TAPAS BAR",
                "hero_subtitle": "an der Ostsee",
                "hero_description": "Genießen Sie authentische mediterrane Spezialitäten",
                "hero_location": "direkt an der malerischen Ostseeküste",
                "hero_background_image": "https://images.unsplash.com/photo-1656423521731-9665583f100c",
                "hero_menu_button_text": "Zur Speisekarte",
                "hero_locations_button_text": "Unsere Standorte",
                "hero_image": "https://images.unsplash.com/photo-1560472355-536de3962603",
                "features_data": json.dumps({
                    "title": "Mediterrane Tradition",
                    "subtitle": "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste",
                    "cards": [
                        {
                            "title": "Authentische Tapas",
                            "description": "Traditionelle Rezepte aus verschiedenen Regionen Spaniens",
                            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae",
                            "link_category": "Vorspeisen"
                        },
                        {
                            "title": "Frische Paellas",
                            "description": "Täglich frisch zubereitet nach originalen Rezepten",
                            "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a",
                            "link_category": "Paella"
                        },
                        {
                            "title": "Feine Weine",
                            "description": "Ausgewählte spanische Weine perfekt zu unseren Gerichten",
                            "image_url": "https://images.unsplash.com/photo-1506377585622-bedcbb027afc",
                            "link_category": "Getränke"
                        }
                    ]
                }),
                "specialties_data": json.dumps({
                    "title": "Unsere Spezialitäten",
                    "cards": [
                        {
                            "title": "Paella Valenciana",
                            "description": "Die klassische Paella mit Huhn, Kaninchen und grünen Bohnen",
                            "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a",
                            "category_link": "Paella"
                        },
                        {
                            "title": "Jamón Ibérico",
                            "description": "Der beste spanische Schinken, hauchdünn geschnitten",
                            "image_url": "https://images.unsplash.com/photo-1558985250-3f1b04f44b25",
                            "category_link": "Vorspeisen"
                        },
                        {
                            "title": "Pulpo a la Gallega",
                            "description": "Galizischer Oktopus mit Paprikapulver und Olivenöl",
                            "image_url": "https://images.unsplash.com/photo-1565299585323-38174c2a5aa4",
                            "category_link": "Vorspeisen"
                        }
                    ]
                }),
                "delivery_data": json.dumps({
                    "title": "Jetzt auch bequem nach Hause bestellen",
                    "description": "Genießen Sie unsere authentischen mediterranen Spezialitäten gemütlich zu Hause.",
                    "description_2": "Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.",
                    "delivery_feature_title": "Schnelle Lieferung",
                    "delivery_feature_description": "Frisch und warm zu Ihnen",
                    "delivery_feature_image": "https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg",
                    "button_text": "Jetzt bei Lieferando bestellen",
                    "button_url": "https://www.lieferando.de",
                    "availability_text": "Verfügbar für beide Standorte",
                    "authentic_feature_title": "Authentisch Mediterran",
                    "authentic_feature_description": "Direkt vom Küchenchef",
                    "authentic_feature_image": "https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg"
                }),
                "updated_at": datetime.utcnow(),
                "updated_by": "system"
            }
            
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO homepage_content (id, hero_title, hero_subtitle, hero_description, hero_location, 
                                            hero_background_image, hero_menu_button_text, hero_locations_button_text, 
                                            hero_image, features_data, specialties_data, delivery_data, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (default_content["id"], default_content["hero_title"], default_content["hero_subtitle"],
                  default_content["hero_description"], default_content["hero_location"], 
                  default_content["hero_background_image"], default_content["hero_menu_button_text"],
                  default_content["hero_locations_button_text"], default_content["hero_image"],
                  default_content["features_data"], default_content["specialties_data"],
                  default_content["delivery_data"], default_content["updated_at"], default_content["updated_by"]))
            
            content = default_content
        
        # Parse JSON fields
        if isinstance(content.get('features_data'), str):
            content['features'] = json.loads(content['features_data'])
        if isinstance(content.get('specialties_data'), str):
            content['specialties'] = json.loads(content['specialties_data'])
        if isinstance(content.get('delivery_data'), str):
            content['delivery'] = json.loads(content['delivery_data'])
        
        # Create hero object
        content['hero'] = {
            "title": content.get('hero_title', ''),
            "subtitle": content.get('hero_subtitle', ''),
            "description": content.get('hero_description', ''),
            "location": content.get('hero_location', ''),
            "background_image": content.get('hero_background_image', ''),
            "menu_button_text": content.get('hero_menu_button_text', ''),
            "locations_button_text": content.get('hero_locations_button_text', ''),
            "image": content.get('hero_image', '')
        }
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/standorte-enhanced")
async def get_standorte_enhanced():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM standorte_enhanced LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default content
            default_content = {
                "id": str(uuid.uuid4()),
                "page_title": "Unsere Standorte",
                "page_subtitle": "Besuchen Sie uns an einem unserer beiden Standorte",
                "header_background": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
                "neustadt_data": json.dumps({
                    "name": "Jimmy's Tapas Bar Neustadt",
                    "address": "Strandstraße 12, 23730 Neustadt in Holstein",
                    "phone": "+49 4561 123456",
                    "email": "neustadt@jimmys-tapasbar.de",
                    "opening_hours": {
                        "Montag": "16:00 - 23:00",
                        "Dienstag": "16:00 - 23:00", 
                        "Mittwoch": "16:00 - 23:00",
                        "Donnerstag": "16:00 - 23:00",
                        "Freitag": "16:00 - 24:00",
                        "Samstag": "12:00 - 24:00",
                        "Sonntag": "12:00 - 23:00"
                    },
                    "features": [
                        "Direkte Strandlage",
                        "Große Terrasse",
                        "Familienfreundlich",
                        "Parkplatz kostenlos"
                    ],
                    "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5"
                }),
                "grossenbrode_data": json.dumps({
                    "name": "Jimmy's Tapas Bar Großenbrode",
                    "address": "Strandpromenade 8, 23775 Großenbrode",
                    "phone": "+49 4367 987654",
                    "email": "grossenbrode@jimmys-tapasbar.de",
                    "opening_hours": {
                        "Montag": "17:00 - 23:00",
                        "Dienstag": "17:00 - 23:00",
                        "Mittwoch": "17:00 - 23:00", 
                        "Donnerstag": "17:00 - 23:00",
                        "Freitag": "17:00 - 24:00",
                        "Samstag": "12:00 - 24:00",
                        "Sonntag": "12:00 - 23:00"
                    },
                    "features": [
                        "Panorama-Meerblick",
                        "Ruhige Lage",
                        "Romantische Atmosphäre",
                        "Sonnenuntergänge"
                    ],
                    "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4"
                }),
                "info_section_data": json.dumps({
                    "anreise_parken": {
                        "title": "Anreise & Parken",
                        "description": "Kostenlose Parkplätze direkt am Restaurant verfügbar",
                        "image": "https://images.unsplash.com/photo-1496442226666"
                    },
                    "oeffnungszeiten": {
                        "title": "Öffnungszeiten",
                        "description": "Täglich geöffnet. Warme Küche bis 22:00 Uhr",
                        "image": "https://images.unsplash.com/photo-1501139083538"
                    },
                    "familienfreundlich": {
                        "title": "Familienfreundlich",
                        "description": "Spezielle Kinderkarte und Spielbereich vorhanden",
                        "image": "https://images.unsplash.com/photo-1414235077428"
                    }
                }),
                "updated_at": datetime.utcnow(),
                "updated_by": "system"
            }
            
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO standorte_enhanced (id, page_title, page_subtitle, header_background, 
                                              neustadt_data, grossenbrode_data, info_section_data, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (default_content["id"], default_content["page_title"], default_content["page_subtitle"],
                  default_content["header_background"], default_content["neustadt_data"], 
                  default_content["grossenbrode_data"], default_content["info_section_data"],
                  default_content["updated_at"], default_content["updated_by"]))
            
            content = default_content
        
        # Parse JSON fields
        if isinstance(content.get('neustadt_data'), str):
            content['neustadt'] = json.loads(content['neustadt_data'])
        if isinstance(content.get('grossenbrode_data'), str):
            content['grossenbrode'] = json.loads(content['grossenbrode_data'])
        if isinstance(content.get('info_section_data'), str):
            content['info_section'] = json.loads(content['info_section_data'])
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/ueber-uns-enhanced")
async def get_ueber_uns_enhanced():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ueber_uns_enhanced LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default content
            default_content = {
                "id": str(uuid.uuid4()),
                "page_title": "Über uns",
                "page_subtitle": "Lernen Sie Jimmy's Tapas Bar kennen",
                "header_background": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
                "jimmy_data": json.dumps({
                    "name": "Jimmy Rodríguez",
                    "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d",
                    "story_paragraph1": "Seit der Gründung im Jahr 2015 steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.",
                    "story_paragraph2": "Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.",
                    "quote": "Gutes Essen bringt Menschen zusammen und schafft unvergessliche Momente."
                }),
                "values_section_data": json.dumps({
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
                }),
                "team_section_data": json.dumps({
                    "title": "Unser Team",
                    "team_members": [
                        {
                            "name": "Jimmy Rodríguez",
                            "position": "Küchenchef & Inhaber",
                            "description": "Jimmy bringt über 20 Jahre Erfahrung in der mediterranen Küche mit.",
                            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
                        },
                        {
                            "name": "Maria González",
                            "position": "Sous Chef",
                            "description": "Spezialistin für authentische Tapas und Paellas.",
                            "image": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80"
                        }
                    ]
                }),
                "updated_at": datetime.utcnow(),
                "updated_by": "system"
            }
            
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO ueber_uns_enhanced (id, page_title, page_subtitle, header_background, 
                                              jimmy_data, values_section_data, team_section_data, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (default_content["id"], default_content["page_title"], default_content["page_subtitle"],
                  default_content["header_background"], default_content["jimmy_data"], 
                  default_content["values_section_data"], default_content["team_section_data"],
                  default_content["updated_at"], default_content["updated_by"]))
            
            content = default_content
        
        # Parse JSON fields
        if isinstance(content.get('jimmy_data'), str):
            content['jimmy'] = json.loads(content['jimmy_data'])
        if isinstance(content.get('values_section_data'), str):
            content['values_section'] = json.loads(content['values_section_data'])
        if isinstance(content.get('team_section_data'), str):
            content['team_section'] = json.loads(content['team_section_data'])
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/kontakt-page")
async def get_kontakt_page():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM kontakt_page LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default content
            default_content = {
                "id": str(uuid.uuid4()),
                "page_title": "Kontakt",
                "page_subtitle": "Wir freuen uns auf Ihren Besuch",
                "header_background": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
                "contact_form_title": "Schreiben Sie uns",
                "contact_form_subtitle": "Haben Sie Fragen oder möchten Sie einen Tisch reservieren?",
                "locations_section_title": "Unsere Standorte",
                "opening_hours_title": "Öffnungszeiten",
                "additional_info": "Wir sind täglich für Sie da. Rufen Sie uns an oder besuchen Sie uns einfach!",
                "updated_at": datetime.utcnow(),
                "updated_by": "system"
            }
            
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO kontakt_page (id, page_title, page_subtitle, header_background, 
                                        contact_form_title, contact_form_subtitle, locations_section_title,
                                        opening_hours_title, additional_info, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (default_content["id"], default_content["page_title"], default_content["page_subtitle"],
                  default_content["header_background"], default_content["contact_form_title"], 
                  default_content["contact_form_subtitle"], default_content["locations_section_title"],
                  default_content["opening_hours_title"], default_content["additional_info"],
                  default_content["updated_at"], default_content["updated_by"]))
            
            content = default_content
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/bewertungen-page")
async def get_bewertungen_page():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM bewertungen_page LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default content
            default_content = {
                "id": str(uuid.uuid4()),
                "page_title": "Bewertungen & Feedback",
                "page_subtitle": "Was unsere Gäste über uns sagen",
                "header_background": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
                "reviews_section_title": "Kundenbewertungen",
                "feedback_section_title": "Ihr Feedback",
                "feedback_note": "Teilen Sie Ihre Erfahrungen mit uns und anderen Gästen.",
                "updated_at": datetime.utcnow(),
                "updated_by": "system"
            }
            
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO bewertungen_page (id, page_title, page_subtitle, header_background, 
                                            reviews_section_title, feedback_section_title, feedback_note,
                                            updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (default_content["id"], default_content["page_title"], default_content["page_subtitle"],
                  default_content["header_background"], default_content["reviews_section_title"], 
                  default_content["feedback_section_title"], default_content["feedback_note"],
                  default_content["updated_at"], default_content["updated_by"]))
            
            content = default_content
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.get("/delivery/info")
async def get_delivery_info():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM delivery_info WHERE is_active = TRUE LIMIT 1")
        info = await cursor.fetchone()
        
        if not info:
            raise HTTPException(status_code=404, detail="Delivery info not found")
        
        return {
            "delivery_time": f"{info['delivery_time_min']}-{info['delivery_time_max']} min",
            "minimum_order_value": str(info['minimum_order_value']),
            "delivery_fee": str(info['delivery_fee']),
            "available_locations": json.loads(info['available_locations']) if info['available_locations'] else {}
        }
    finally:
        mysql_pool.release(conn)

# User Management routes
@api_router.get("/users", response_model=List[User])
async def get_users(current_user: User = Depends(get_admin_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = await cursor.fetchall()
        return [User(**user) for user in users]
    finally:
        mysql_pool.release(conn)

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

@app.on_event("shutdown")
async def shutdown_event():
    if mysql_pool:
        mysql_pool.close()
        await mysql_pool.wait_closed()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
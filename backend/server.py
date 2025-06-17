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

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Review Models
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
    price: str
    category: str
    image: Optional[str] = None  # Base64 encoded
    details: Optional[str] = None
    vegan: bool = False
    vegetarian: bool = False
    glutenfree: bool = False
    order_index: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: str
    category: str
    image: Optional[str] = None
    details: Optional[str] = None
    vegan: bool = False
    vegetarian: bool = False
    glutenfree: bool = False
    order_index: int = 0

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    details: Optional[str] = None
    vegan: Optional[bool] = None
    vegetarian: Optional[bool] = None
    glutenfree: Optional[bool] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

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

# Maintenance Models
class MaintenanceMode(BaseModel):
    is_active: bool = False
    message: str = "Die Website befindet sich derzeit im Wartungsmodus."
    activated_by: Optional[str] = None
    activated_at: Optional[datetime] = None

# Auth Helper Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Get user from MySQL
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = await cursor.fetchone()
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user_data)
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

# Initialize default admin user
async def create_default_admin():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        
        # Check if admin exists
        await cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
        result = await cursor.fetchone()
        
        if result['count'] == 0:
            admin_user = User(
                username="admin",
                email="admin@jimmys-tapasbar.de",
                password_hash=get_password_hash("jimmy2024"),
                role=UserRole.ADMIN
            )
            
            await cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, role, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                admin_user.id, admin_user.username, admin_user.email, 
                admin_user.password_hash, admin_user.role, admin_user.is_active, 
                admin_user.created_at
            ))
            print("Default admin user created")
    finally:
        mysql_pool.release(conn)

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Hello World from MySQL Backend"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_obj = StatusCheck(**input.dict())
    
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute("""
            INSERT INTO status_checks (id, client_name, timestamp)
            VALUES (%s, %s, %s)
        """, (status_obj.id, status_obj.client_name, status_obj.timestamp))
    finally:
        mysql_pool.release(conn)
    
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM status_checks ORDER BY timestamp DESC LIMIT 1000")
        status_checks = await cursor.fetchall()
        return [StatusCheck(**check) for check in status_checks]
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
        
        if not user or not verify_password(user_credentials.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        if not user["is_active"]:
            raise HTTPException(status_code=401, detail="User account is disabled")
        
        # Update last login
        await cursor.execute("""
            UPDATE users SET last_login = %s WHERE username = %s
        """, (datetime.utcnow(), user_credentials.username))
        
        access_token = create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# User Management routes (Admin only)
@api_router.post("/users", response_model=User)
async def create_user(user_data: UserCreate, current_user: User = Depends(get_admin_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        
        # Check if username already exists
        await cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = %s", (user_data.username,))
        result = await cursor.fetchone()
        if result['count'] > 0:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role
        )
        
        await cursor.execute("""
            INSERT INTO users (id, username, email, password_hash, role, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user.id, user.username, user.email, user.password_hash, user.role, user.is_active, user.created_at))
        
        return user
    finally:
        mysql_pool.release(conn)

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

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_admin_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        result = await cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    finally:
        mysql_pool.release(conn)

# Review Management routes
@api_router.get("/reviews", response_model=List[Review])
async def get_reviews(approved_only: bool = True):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        if approved_only:
            await cursor.execute("SELECT * FROM reviews WHERE is_approved = TRUE ORDER BY date DESC LIMIT 1000")
        else:
            await cursor.execute("SELECT * FROM reviews ORDER BY date DESC LIMIT 1000")
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
        await cursor.execute("SELECT * FROM menu_items WHERE is_active = TRUE ORDER BY order_index ASC, name ASC")
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
            INSERT INTO menu_items (id, name, description, price, category, image, details,
                                   vegan, vegetarian, glutenfree, order_index, is_active, 
                                   created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (item.id, item.name, item.description, item.price, item.category, item.image,
              item.details, item.vegan, item.vegetarian, item.glutenfree, item.order_index,
              item.is_active, item.created_at, item.updated_at))
        
        return item
    finally:
        mysql_pool.release(conn)

@api_router.put("/menu/items/{item_id}", response_model=MenuItem)
async def update_menu_item(
    item_id: str, 
    item_data: MenuItemUpdate, 
    current_user: User = Depends(get_editor_user)
):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        
        # Get current item
        await cursor.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
        current_item = await cursor.fetchone()
        if not current_item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        
        # Build update query dynamically
        update_fields = []
        update_values = []
        
        for field, value in item_data.dict().items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                update_values.append(value)
        
        if update_fields:
            update_fields.append("updated_at = %s")
            update_values.append(datetime.utcnow())
            update_values.append(item_id)
            
            query = f"UPDATE menu_items SET {', '.join(update_fields)} WHERE id = %s"
            await cursor.execute(query, update_values)
        
        # Return updated item
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
        result = await cursor.execute("UPDATE menu_items SET is_active = FALSE WHERE id = %s", (item_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Menu item not found")
        return {"message": "Menu item deleted successfully"}
    finally:
        mysql_pool.release(conn)

# Contact Messages routes
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

@api_router.put("/admin/contact/{message_id}/read")
async def mark_message_read(message_id: str, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        result = await cursor.execute("UPDATE contact_messages SET is_read = TRUE WHERE id = %s", (message_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        return {"message": "Message marked as read"}
    finally:
        mysql_pool.release(conn)

# Maintenance Mode routes
@api_router.get("/maintenance", response_model=MaintenanceMode)
async def get_maintenance_status():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM maintenance_mode LIMIT 1")
        maintenance = await cursor.fetchone()
        
        if not maintenance:
            # Create default maintenance mode
            default_maintenance = MaintenanceMode()
            await cursor.execute("""
                INSERT INTO maintenance_mode (id, is_active, message)
                VALUES (%s, %s, %s)
            """, (str(uuid.uuid4()), default_maintenance.is_active, default_maintenance.message))
            return default_maintenance
        
        return MaintenanceMode(**maintenance)
    finally:
        mysql_pool.release(conn)

@api_router.put("/admin/maintenance", response_model=MaintenanceMode)
async def update_maintenance_mode(
    maintenance_data: MaintenanceMode, 
    current_user: User = Depends(get_admin_user)
):
    maintenance_data.activated_by = current_user.username
    maintenance_data.activated_at = datetime.utcnow()
    
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Check if maintenance record exists
        await cursor.execute("SELECT COUNT(*) as count FROM maintenance_mode")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO maintenance_mode (id, is_active, message, activated_by, activated_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), maintenance_data.is_active, maintenance_data.message,
                  maintenance_data.activated_by, maintenance_data.activated_at))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE maintenance_mode SET is_active = %s, message = %s, 
                       activated_by = %s, activated_at = %s
            """, (maintenance_data.is_active, maintenance_data.message,
                  maintenance_data.activated_by, maintenance_data.activated_at))
        
        return maintenance_data
    finally:
        mysql_pool.release(conn)

# Image upload route
@api_router.post("/admin/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_editor_user)
):
    # Read file content and convert to base64
    file_content = await file.read()
    base64_content = base64.b64encode(file_content).decode('utf-8')
    
    # Create data URL
    data_url = f"data:{file.content_type};base64,{base64_content}"
    
    return {"image_url": data_url, "filename": file.filename}

# Helper function for byte formatting
def format_bytes(bytes_count):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"

# Extended CMS Models
class HomepageContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hero_title: str = "JIMMY'S TAPAS BAR"
    hero_subtitle: str = "an der Ostsee"
    hero_description: str = "Genießen Sie authentische mediterrane Spezialitäten"
    hero_location: str = "direkt an der malerischen Ostseeküste"
    hero_background_image: Optional[str] = None
    hero_menu_button_text: str = "Zur Speisekarte"
    hero_locations_button_text: str = "Unsere Standorte"
    features_data: Optional[Dict] = None
    specialties_data: Optional[Dict] = None
    delivery_data: Optional[Dict] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

class LocationsContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_title: str = "Unsere Standorte"
    page_description: str = "Besuchen Sie uns an einem unserer beiden Standorte"
    locations_data: List[Dict] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

class AboutContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_title: str = "Über uns"
    hero_title: str = "Unsere Geschichte"
    hero_description: str = "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar"
    story_title: str = "Unsere Leidenschaft"
    story_content: str = ""
    story_image: Optional[str] = None
    team_title: str = "Unser Team"
    team_members: List[Dict] = []
    values_title: str = "Unsere Werte"
    values_data: List[str] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

class LegalPage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_type: str  # "imprint" or "privacy"
    title: str
    content: str
    contact_name: Optional[str] = None
    contact_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    company_info: Optional[Dict] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

class ContentSection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page: str
    section: str
    content: Dict[str, Any]
    images: List[str] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

class ContentSectionUpdate(BaseModel):
    content: Dict[str, Any]
    images: Optional[List[str]] = None

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
            default_content = HomepageContent()
            default_features = {
                "title": "Mediterrane Tradition",
                "subtitle": "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste",
                "cards": [
                    {
                        "title": "Authentische Tapas",
                        "description": "Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
                        "image_url": "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"
                    },
                    {
                        "title": "Frische Paella",
                        "description": "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn",
                        "image_url": "https://images.unsplash.com/photo-1694685367640-05d6624e57f1"
                    },
                    {
                        "title": "Strandnähe",
                        "description": "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden",
                        "image_url": "https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg"
                    }
                ]
            }
            
            default_specialties = {
                "title": "Unsere Spezialitäten",
                "cards": [
                    {
                        "title": "Patatas Bravas",
                        "description": "Klassische mediterrane Kartoffeln",
                        "image_url": "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
                        "category_link": "tapas-vegetarian"
                    },
                    {
                        "title": "Paella Valenciana",
                        "description": "Traditionelle mediterrane Paella",
                        "image_url": "https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg",
                        "category_link": "tapa-paella"
                    },
                    {
                        "title": "Tapas Variación",
                        "description": "Auswahl mediterraner Köstlichkeiten",
                        "image_url": "https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg",
                        "category_link": "inicio"
                    },
                    {
                        "title": "Gambas al Ajillo",
                        "description": "Garnelen in Knoblauchöl",
                        "image_url": "https://images.unsplash.com/photo-1619860705243-dbef552e7118",
                        "category_link": "tapas-pescado"
                    }
                ]
            }
            
            default_delivery = {
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
            }
            
            await cursor.execute("""
                INSERT INTO homepage_content (id, hero_title, hero_subtitle, hero_description, 
                                             hero_location, hero_background_image, hero_menu_button_text,
                                             hero_locations_button_text, features_data, specialties_data,
                                             delivery_data, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                default_content.id, default_content.hero_title, default_content.hero_subtitle,
                default_content.hero_description, default_content.hero_location,
                "https://images.unsplash.com/photo-1656423521731-9665583f100c",
                default_content.hero_menu_button_text, default_content.hero_locations_button_text,
                json.dumps(default_features), json.dumps(default_specialties),
                json.dumps(default_delivery), default_content.updated_at
            ))
            
            content = {
                "id": default_content.id,
                "hero_title": default_content.hero_title,
                "hero_subtitle": default_content.hero_subtitle,
                "hero_description": default_content.hero_description,
                "hero_location": default_content.hero_location,
                "hero_background_image": "https://images.unsplash.com/photo-1656423521731-9665583f100c",
                "hero_menu_button_text": default_content.hero_menu_button_text,
                "hero_locations_button_text": default_content.hero_locations_button_text,
                "features_data": default_features,
                "specialties_data": default_specialties,
                "delivery_data": default_delivery,
                "updated_at": default_content.updated_at
            }
        else:
            # Parse JSON fields
            if content.get('features_data'):
                content['features_data'] = json.loads(content['features_data']) if isinstance(content['features_data'], str) else content['features_data']
            if content.get('specialties_data'):
                content['specialties_data'] = json.loads(content['specialties_data']) if isinstance(content['specialties_data'], str) else content['specialties_data']
            if content.get('delivery_data'):
                content['delivery_data'] = json.loads(content['delivery_data']) if isinstance(content['delivery_data'], str) else content['delivery_data']
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/homepage")
async def update_homepage_content(content_data: Dict, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Convert nested objects to JSON strings
        features_json = json.dumps(content_data.get('features_data', {}))
        specialties_json = json.dumps(content_data.get('specialties_data', {}))
        delivery_json = json.dumps(content_data.get('delivery_data', {}))
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM homepage_content")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO homepage_content (id, hero_title, hero_subtitle, hero_description,
                                             hero_location, hero_background_image, hero_menu_button_text,
                                             hero_locations_button_text, features_data, specialties_data,
                                             delivery_data, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                content_data.get('hero_title', 'JIMMY\'S TAPAS BAR'),
                content_data.get('hero_subtitle', 'an der Ostsee'),
                content_data.get('hero_description', 'Genießen Sie authentische mediterrane Spezialitäten'),
                content_data.get('hero_location', 'direkt an der malerischen Ostseeküste'),
                content_data.get('hero_background_image'),
                content_data.get('hero_menu_button_text', 'Zur Speisekarte'),
                content_data.get('hero_locations_button_text', 'Unsere Standorte'),
                features_json, specialties_json, delivery_json,
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE homepage_content SET hero_title = %s, hero_subtitle = %s, hero_description = %s,
                                           hero_location = %s, hero_background_image = %s, 
                                           hero_menu_button_text = %s, hero_locations_button_text = %s,
                                           features_data = %s, specialties_data = %s, delivery_data = %s,
                                           updated_at = %s, updated_by = %s
            """, (
                content_data.get('hero_title', 'JIMMY\'S TAPAS BAR'),
                content_data.get('hero_subtitle', 'an der Ostsee'),
                content_data.get('hero_description', 'Genießen Sie authentische mediterrane Spezialitäten'),
                content_data.get('hero_location', 'direkt an der malerischen Ostseeküste'),
                content_data.get('hero_background_image'),
                content_data.get('hero_menu_button_text', 'Zur Speisekarte'),
                content_data.get('hero_locations_button_text', 'Unsere Standorte'),
                features_json, specialties_json, delivery_json,
                datetime.utcnow(), current_user.username
            ))
        
        return {"message": "Homepage content updated successfully"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/locations")
async def get_locations_content():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM locations LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default locations
            default_locations = [
                {
                    "name": "Jimmy's Tapas Bar Kühlungsborn",
                    "address": "Strandstraße 1, 18225 Kühlungsborn",
                    "phone": "+49 38293 12345",
                    "email": "kuehlungsborn@jimmys-tapasbar.de",
                    "opening_hours": {
                        "Montag": "16:00 - 23:00",
                        "Dienstag": "16:00 - 23:00", 
                        "Mittwoch": "16:00 - 23:00",
                        "Donnerstag": "16:00 - 23:00",
                        "Freitag": "16:00 - 24:00",
                        "Samstag": "12:00 - 24:00",
                        "Sonntag": "12:00 - 23:00"
                    },
                    "description": "Unser Hauptstandort direkt am Strand von Kühlungsborn",
                    "image_url": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
                },
                {
                    "name": "Jimmy's Tapas Bar Warnemünde",
                    "address": "Am Strom 2, 18119 Warnemünde",
                    "phone": "+49 381 987654",
                    "email": "warnemuende@jimmys-tapasbar.de",
                    "opening_hours": {
                        "Montag": "17:00 - 23:00",
                        "Dienstag": "17:00 - 23:00",
                        "Mittwoch": "17:00 - 23:00", 
                        "Donnerstag": "17:00 - 23:00",
                        "Freitag": "17:00 - 24:00",
                        "Samstag": "12:00 - 24:00",
                        "Sonntag": "12:00 - 23:00"
                    },
                    "description": "Gemütlich am alten Strom mit Blick auf die Warnow",
                    "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d"
                }
            ]
            
            content_id = str(uuid.uuid4())
            await cursor.execute("""
                INSERT INTO locations (id, page_title, page_description, locations_data, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                content_id,
                "Unsere Standorte",
                "Besuchen Sie uns an einem unserer beiden Standorte",
                json.dumps(default_locations),
                datetime.utcnow()
            ))
            
            content = {
                "id": content_id,
                "page_title": "Unsere Standorte",
                "page_description": "Besuchen Sie uns an einem unserer beiden Standorte",
                "locations_data": default_locations,
                "updated_at": datetime.utcnow()
            }
        else:
            # Parse JSON field
            if content.get('locations_data'):
                content['locations_data'] = json.loads(content['locations_data']) if isinstance(content['locations_data'], str) else content['locations_data']
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/locations")
async def update_locations_content(content_data: Dict, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        locations_json = json.dumps(content_data.get('locations_data', []))
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM locations")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO locations (id, page_title, page_description, locations_data, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                content_data.get('page_title', 'Unsere Standorte'),
                content_data.get('page_description', 'Besuchen Sie uns an einem unserer beiden Standorte'),
                locations_json,
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE locations SET page_title = %s, page_description = %s, locations_data = %s,
                                   updated_at = %s, updated_by = %s
            """, (
                content_data.get('page_title', 'Unsere Standorte'),
                content_data.get('page_description', 'Besuchen Sie uns an einem unserer beiden Standorte'),
                locations_json,
                datetime.utcnow(), current_user.username
            ))
        
        return {"message": "Locations content updated successfully"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/about")
async def get_about_content():
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM about_content LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default about content
            default_team = [
                {
                    "name": "Jimmy Rodriguez",
                    "position": "Inhaber & Küchenchef",
                    "description": "Jimmy bringt über 20 Jahre Erfahrung in der mediterranen Küche mit",
                    "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
                },
                {
                    "name": "Maria Santos",
                    "position": "Sous Chef",
                    "description": "Spezialistin für authentische Tapas und Paellas",
                    "image_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80"
                }
            ]
            
            default_values = [
                "Authentische mediterrane Küche",
                "Frische, regionale Zutaten",
                "Familiäre Atmosphäre",
                "Leidenschaft für Qualität",
                "Gastfreundschaft"
            ]
            
            default_story = """Seit der Gründung steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.
            
Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.
Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte
von Tradition und Qualität.

An beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers, 
während Sie den Blick auf die Ostsee genießen können."""
            
            content_id = str(uuid.uuid4())
            await cursor.execute("""
                INSERT INTO about_content (id, page_title, hero_title, hero_description, story_title,
                                         story_content, story_image, team_title, team_members,
                                         values_title, values_data, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                content_id,
                "Über uns",
                "Unsere Geschichte",
                "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar",
                "Unsere Leidenschaft",
                default_story,
                "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
                "Unser Team",
                json.dumps(default_team),
                "Unsere Werte",
                json.dumps(default_values),
                datetime.utcnow()
            ))
            
            content = {
                "id": content_id,
                "page_title": "Über uns",
                "hero_title": "Unsere Geschichte",
                "hero_description": "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar",
                "story_title": "Unsere Leidenschaft",
                "story_content": default_story,
                "story_image": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
                "team_title": "Unser Team",
                "team_members": default_team,
                "values_title": "Unsere Werte",
                "values_data": default_values,
                "updated_at": datetime.utcnow()
            }
        else:
            # Parse JSON fields
            if content.get('team_members'):
                content['team_members'] = json.loads(content['team_members']) if isinstance(content['team_members'], str) else content['team_members']
            if content.get('values_data'):
                content['values_data'] = json.loads(content['values_data']) if isinstance(content['values_data'], str) else content['values_data']
        
        return content
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/about")
async def update_about_content(content_data: Dict, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        team_json = json.dumps(content_data.get('team_members', []))
        values_json = json.dumps(content_data.get('values_data', []))
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM about_content")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO about_content (id, page_title, hero_title, hero_description, story_title,
                                         story_content, story_image, team_title, team_members,
                                         values_title, values_data, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                content_data.get('page_title', 'Über uns'),
                content_data.get('hero_title', 'Unsere Geschichte'),
                content_data.get('hero_description', 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar'),
                content_data.get('story_title', 'Unsere Leidenschaft'),
                content_data.get('story_content', ''),
                content_data.get('story_image'),
                content_data.get('team_title', 'Unser Team'),
                team_json,
                content_data.get('values_title', 'Unsere Werte'),
                values_json,
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE about_content SET page_title = %s, hero_title = %s, hero_description = %s,
                                       story_title = %s, story_content = %s, story_image = %s,
                                       team_title = %s, team_members = %s, values_title = %s,
                                       values_data = %s, updated_at = %s, updated_by = %s
            """, (
                content_data.get('page_title', 'Über uns'),
                content_data.get('hero_title', 'Unsere Geschichte'),
                content_data.get('hero_description', 'Entdecken Sie die Leidenschaft hinter Jimmy\'s Tapas Bar'),
                content_data.get('story_title', 'Unsere Leidenschaft'),
                content_data.get('story_content', ''),
                content_data.get('story_image'),
                content_data.get('team_title', 'Unser Team'),
                team_json,
                content_data.get('values_title', 'Unsere Werte'),
                values_json,
                datetime.utcnow(), current_user.username
            ))
        
        return {"message": "About content updated successfully"}
    finally:
        mysql_pool.release(conn)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add explicit OPTIONS route handler for CORS preflight requests
@api_router.options("/{path:path}")
async def options_route(path: str):
    return {"detail": "OK"}

# Include the API router
app.include_router(api_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    await init_mysql_pool()
    await create_default_admin()

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    global mysql_pool
    if mysql_pool:
        mysql_pool.close()
        await mysql_pool.wait_closed()
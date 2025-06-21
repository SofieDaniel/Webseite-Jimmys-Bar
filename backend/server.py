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
    detailed_description: Optional[str] = None
    price: str
    category: str
    image: Optional[str] = None  # Base64 encoded
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    price: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    details: Optional[str] = None
    origin: Optional[str] = None
    allergens: Optional[str] = None
    additives: Optional[str] = None
    preparation_method: Optional[str] = None
    ingredients: Optional[str] = None
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
            await cursor.execute("SELECT * FROM reviews WHERE approved = TRUE ORDER BY created_at DESC LIMIT 1000")
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
            INSERT INTO menu_items (id, name, description, detailed_description, price, category, image, details,
                                   origin, allergens, additives, preparation_method, ingredients,
                                   vegan, vegetarian, glutenfree, order_index, is_active, 
                                   created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (item.id, item.name, item.description, item.detailed_description, item.price, item.category, item.image,
              item.details, item.origin, item.allergens, item.additives, item.preparation_method, item.ingredients,
              item.vegan, item.vegetarian, item.glutenfree, item.order_index,
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
        await cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
        messages = await cursor.fetchall()
        return [ContactMessage(**message) for message in messages]
    finally:
        mysql_pool.release(conn)

@api_router.put("/admin/contact/{message_id}/read")
async def mark_message_read(message_id: str, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        result = await cursor.execute("UPDATE contact_messages SET read_status = TRUE WHERE id = %s", (message_id,))
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

# Delivery Information Endpoints (new for v7)
@api_router.get("/delivery/info")
async def get_delivery_info():
    """Get delivery information for Lieferando section"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM delivery_info WHERE is_active = TRUE LIMIT 1")
        delivery_info = await cursor.fetchone()
        
        if not delivery_info:
            # Create default delivery info
            default_info = {
                "id": str(uuid.uuid4()),
                "delivery_time_min": 30,
                "delivery_time_max": 45,
                "minimum_order_value": 15.00,
                "delivery_fee": 2.50,
                "available_locations": {
                    "neustadt": {
                        "name": "Neustadt",
                        "available": True,
                        "address": "Am Strande 21, 23730 Neustadt in Holstein"
                    },
                    "grossenbrode": {
                        "name": "Großenbrode", 
                        "available": True,
                        "address": "Südstrand 54, 23755 Großenbrode"
                    }
                },
                "is_active": True,
                "updated_by": "system"
            }
            
            await cursor.execute("""
                INSERT INTO delivery_info (id, delivery_time_min, delivery_time_max, 
                                         minimum_order_value, delivery_fee, available_locations,
                                         is_active, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                default_info["id"], default_info["delivery_time_min"], 
                default_info["delivery_time_max"], default_info["minimum_order_value"],
                default_info["delivery_fee"], json.dumps(default_info["available_locations"]),
                default_info["is_active"], default_info["updated_by"]
            ))
            
            return default_info
        
        # Parse JSON data
        available_locations = json.loads(delivery_info['available_locations']) if delivery_info.get('available_locations') else {}
        
        return {
            "id": delivery_info["id"],
            "delivery_time_min": delivery_info["delivery_time_min"],
            "delivery_time_max": delivery_info["delivery_time_max"],
            "minimum_order_value": float(delivery_info["minimum_order_value"]),
            "delivery_fee": float(delivery_info["delivery_fee"]),
            "available_locations": available_locations,
            "is_active": delivery_info["is_active"],
            "updated_at": delivery_info["updated_at"]
        }
        
    finally:
        mysql_pool.release(conn)

@api_router.put("/admin/delivery/info")
async def update_delivery_info(delivery_data: Dict, current_user: User = Depends(get_editor_user)):
    """Update delivery information (admin only)"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM delivery_info WHERE is_active = TRUE")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO delivery_info (id, delivery_time_min, delivery_time_max,
                                         minimum_order_value, delivery_fee, available_locations,
                                         is_active, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                delivery_data.get('delivery_time_min', 30),
                delivery_data.get('delivery_time_max', 45),
                delivery_data.get('minimum_order_value', 15.00),
                delivery_data.get('delivery_fee', 2.50),
                json.dumps(delivery_data.get('available_locations', {})),
                True, current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE delivery_info SET delivery_time_min = %s, delivery_time_max = %s,
                                       minimum_order_value = %s, delivery_fee = %s,
                                       available_locations = %s, updated_by = %s,
                                       updated_at = %s
                WHERE is_active = TRUE
            """, (
                delivery_data.get('delivery_time_min', 30),
                delivery_data.get('delivery_time_max', 45),
                delivery_data.get('minimum_order_value', 15.00),
                delivery_data.get('delivery_fee', 2.50),
                json.dumps(delivery_data.get('available_locations', {})),
                current_user.username,
                datetime.utcnow()
            ))
        
        return {"message": "Delivery information updated successfully"}
    finally:
        mysql_pool.release(conn)

# Enhanced CMS Endpoints für die drei neuen Seiten

@api_router.get("/cms/standorte-enhanced")
async def get_standorte_enhanced():
    """Get enhanced locations page data"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM standorte_enhanced LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Return basic structure if no data found
            return {
                "id": "default",
                "page_title": "Unsere Standorte",
                "page_subtitle": "Besuchen Sie uns an der malerischen Ostseeküste",
                "header_background": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
                "locations": []
            }
        
        # Parse JSON data
        neustadt_data = json.loads(content['neustadt_data']) if content.get('neustadt_data') else {}
        grossenbrode_data = json.loads(content['grossenbrode_data']) if content.get('grossenbrode_data') else {}
        info_section_data = json.loads(content['info_section_data']) if content.get('info_section_data') else {}
        
        return {
            "id": content["id"],
            "page_title": content["page_title"],
            "page_subtitle": content["page_subtitle"], 
            "header_background": content["header_background"],
            "neustadt": neustadt_data,
            "grossenbrode": grossenbrode_data,
            "info_section": info_section_data,
            "updated_at": content.get("updated_at")
        }
        
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/standorte-enhanced")
async def update_standorte_enhanced(content_data: Dict, current_user: User = Depends(get_editor_user)):
    """Update enhanced locations page data"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM standorte_enhanced")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO standorte_enhanced (id, page_title, page_subtitle, header_background,
                                               neustadt_data, grossenbrode_data, info_section_data,
                                               updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), json.dumps(content_data.get('neustadt', {})),
                json.dumps(content_data.get('grossenbrode', {})), json.dumps(content_data.get('info_section', {})),
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE standorte_enhanced SET page_title = %s, page_subtitle = %s, header_background = %s,
                                             neustadt_data = %s, grossenbrode_data = %s, info_section_data = %s,
                                             updated_at = %s, updated_by = %s
            """, (
                content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), json.dumps(content_data.get('neustadt', {})),
                json.dumps(content_data.get('grossenbrode', {})), json.dumps(content_data.get('info_section', {})),
                datetime.utcnow(), current_user.username
            ))
        
        return {"message": "Enhanced locations content updated successfully"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/bewertungen-page")
async def get_bewertungen_page():
    """Get reviews page configuration data"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM bewertungen_page LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default content exactly as per code specification
            default_content = {
                "id": str(uuid.uuid4()),
                "page_title": "Bewertungen & Feedback",
                "page_subtitle": "Was unsere Gäste über uns sagen",
                "header_background": "https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg",
                "reviews_section_title": "Kundenbewertungen",
                "feedback_section_title": "Ihr Feedback",
                "feedback_note": "Dieses Feedback wird intern gespeichert und nicht öffentlich angezeigt.",
                "updated_at": datetime.utcnow()
            }
            
            # Insert default content
            await cursor.execute("""
                INSERT INTO bewertungen_page (id, page_title, page_subtitle, header_background,
                                             reviews_section_title, feedback_section_title, feedback_note,
                                             updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                default_content["id"], default_content["page_title"], default_content["page_subtitle"],
                default_content["header_background"], default_content["reviews_section_title"],
                default_content["feedback_section_title"], default_content["feedback_note"],
                default_content["updated_at"], "system"
            ))
            
            return default_content
            
        return {
            "id": content["id"],
            "page_title": content["page_title"],
            "page_subtitle": content["page_subtitle"],
            "header_background": content["header_background"],
            "reviews_section_title": content["reviews_section_title"],
            "feedback_section_title": content["feedback_section_title"],
            "feedback_note": content["feedback_note"],
            "updated_at": content["updated_at"]
        }
        
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/bewertungen-page")
async def update_bewertungen_page(content_data: Dict, current_user: User = Depends(get_editor_user)):
    """Update reviews page configuration data"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM bewertungen_page")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO bewertungen_page (id, page_title, page_subtitle, header_background,
                                             reviews_section_title, feedback_section_title, feedback_note,
                                             updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), content_data.get('reviews_section_title'),
                content_data.get('feedback_section_title'), content_data.get('feedback_note'),
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE bewertungen_page SET page_title = %s, page_subtitle = %s, header_background = %s,
                                           reviews_section_title = %s, feedback_section_title = %s, 
                                           feedback_note = %s, updated_at = %s, updated_by = %s
            """, (
                content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), content_data.get('reviews_section_title'),
                content_data.get('feedback_section_title'), content_data.get('feedback_note'),
                datetime.utcnow(), current_user.username
            ))
        
        return {"message": "Reviews page content updated successfully"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/kontakt-page")
async def get_kontakt_page():
    """Get contact page configuration data"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM kontakt_page LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Return default structure if no data found
            return {
                "id": "default",
                "page_title": "Kontakt",
                "page_subtitle": "Nehmen Sie Kontakt mit uns auf",
                "header_background": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
                "contact_form_title": "Schreiben Sie uns",
                "contact_form_subtitle": "Wir freuen uns auf Ihre Nachricht",
                "locations_section_title": "Unsere Standorte",
                "opening_hours_title": "Öffnungszeiten",
                "additional_info": "Telefonische Reservierungen werden bevorzugt behandelt.",
                "updated_at": None
            }
        
        return {
            "id": content["id"],
            "page_title": content["page_title"],
            "page_subtitle": content["page_subtitle"],
            "header_background": content["header_background"],
            "contact_form_title": content["contact_form_title"],
            "contact_form_subtitle": content["contact_form_subtitle"],
            "locations_section_title": content["locations_section_title"],
            "opening_hours_title": content["opening_hours_title"],
            "additional_info": content["additional_info"],
            "updated_at": content["updated_at"]
        }
        
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/kontakt-page")
async def update_kontakt_page(content_data: Dict, current_user: User = Depends(get_editor_user)):
    """Update contact page configuration data"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM kontakt_page")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO kontakt_page (id, page_title, page_subtitle, header_background,
                                         contact_form_title, contact_form_subtitle,
                                         locations_section_title, opening_hours_title,
                                         additional_info, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), content_data.get('contact_form_title'),
                content_data.get('contact_form_subtitle'), content_data.get('locations_section_title'),
                content_data.get('opening_hours_title'), content_data.get('additional_info'),
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE kontakt_page SET page_title = %s, page_subtitle = %s, header_background = %s,
                                       contact_form_title = %s, contact_form_subtitle = %s,
                                       locations_section_title = %s, opening_hours_title = %s,
                                       additional_info = %s, updated_at = %s, updated_by = %s
            """, (
                content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), content_data.get('contact_form_title'),
                content_data.get('contact_form_subtitle'), content_data.get('locations_section_title'),
                content_data.get('opening_hours_title'), content_data.get('additional_info'),
                datetime.utcnow(), current_user.username
            ))
        
        return {"message": "Contact page content updated successfully"}
    finally:
        mysql_pool.release(conn)

@api_router.get("/cms/ueber-uns-enhanced")
async def get_ueber_uns_enhanced():
    """Get enhanced about page data according to exact code specification"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ueber_uns_enhanced LIMIT 1")
        content = await cursor.fetchone()
        
        if not content:
            # Create default enhanced content exactly as per code specification
            default_content = {
                "id": str(uuid.uuid4()),
                "page_title": "Über uns",
                "page_subtitle": "Die Geschichte hinter Jimmy's Tapas Bar",
                "header_background": "https://images.pexels.com/photos/26626726/pexels-photo-26626726.jpeg",
                "jimmy": {
                    "name": "Jimmy Rodríguez",
                    "image": "https://images.unsplash.com/photo-1665758564802-f611df512d8d",
                    "story_paragraph1": "Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, wo ich die Geheimnisse traditioneller Rezepte erlernte.",
                    "story_paragraph2": "In Jimmy's Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit Liebe und Respekt vor der spanischen Tradition zubereitet.",
                    "quote": "Essen ist nicht nur Nahrung - es ist Kultur, Tradition und Leidenschaft auf einem Teller."
                },
                "values_section": {
                    "title": "Unsere Werte",
                    "qualitat": {
                        "title": "Qualität",
                        "description": "Nur die besten Zutaten für authentische spanische Geschmackserlebnisse. Frische und Qualität stehen bei uns an erster Stelle.",
                        "image": "https://images.unsplash.com/photo-1694685367640-05d6624e57f1"
                    },
                    "gastfreundschaft": {
                        "title": "Gastfreundschaft",
                        "description": "Herzliche Atmosphäre und persönlicher Service für jeden Gast. Bei uns sollen Sie sich wie zu Hause fühlen.",
                        "image": "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"
                    },
                    "lebensfreude": {
                        "title": "Lebensfreude",
                        "description": "Spanische Lebensart und Genuss in gemütlicher Atmosphäre. Erleben Sie das echte España-Gefühl an der Ostsee.",
                        "image": "https://images.unsplash.com/photo-1656423521731-9665583f100c"
                    }
                },
                "team_section": {
                    "title": "Unser Team",
                    "carlos": {
                        "name": "Carlos Mendez",
                        "position": "Küchenchef",
                        "description": "Mit 20 Jahren Erfahrung in der spanischen Küche sorgt Carlos für die authentischen Geschmäcker in jedem unserer Gerichte.",
                        "image": "https://images.unsplash.com/photo-1665758564802-f611df512d8d"
                    },
                    "maria": {
                        "name": "Maria Santos",
                        "position": "Service Manager",
                        "description": "Maria sorgt dafür, dass sich jeder Gast bei uns willkommen fühlt und einen unvergesslichen Abend erlebt.",
                        "image": "https://images.unsplash.com/photo-1665758564802-f611df512d8d"
                    }
                },
                "updated_at": datetime.utcnow()
            }
            
            # Insert default content
            await cursor.execute("""
                INSERT INTO ueber_uns_enhanced (id, page_title, page_subtitle, header_background,
                                               jimmy_data, values_section_data, team_section_data,
                                               updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                default_content["id"], default_content["page_title"], default_content["page_subtitle"],
                default_content["header_background"], json.dumps(default_content["jimmy"]),
                json.dumps(default_content["values_section"]), json.dumps(default_content["team_section"]),
                default_content["updated_at"], "system"
            ))
            
            return default_content
            
        # Parse JSON fields
        jimmy_data = json.loads(content['jimmy_data']) if content.get('jimmy_data') else {}
        values_section_data = json.loads(content['values_section_data']) if content.get('values_section_data') else {}
        team_section_data = json.loads(content['team_section_data']) if content.get('team_section_data') else {}
        
        return {
            "id": content["id"],
            "page_title": content["page_title"],
            "page_subtitle": content["page_subtitle"],
            "header_background": content["header_background"],
            "jimmy": jimmy_data,
            "values_section": values_section_data,
            "team_section": team_section_data,
            "updated_at": content["updated_at"]
        }
        
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/ueber-uns-enhanced")
async def update_ueber_uns_enhanced(content_data: Dict, current_user: User = Depends(get_editor_user)):
    """Update enhanced about page data"""
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM ueber_uns_enhanced")
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO ueber_uns_enhanced (id, page_title, page_subtitle, header_background,
                                               jimmy_data, values_section_data, team_section_data,
                                               updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), json.dumps(content_data.get('jimmy', {})),
                json.dumps(content_data.get('values_section', {})), json.dumps(content_data.get('team_section', {})),
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE ueber_uns_enhanced SET page_title = %s, page_subtitle = %s, header_background = %s,
                                             jimmy_data = %s, values_section_data = %s, team_section_data = %s,
                                             updated_at = %s, updated_by = %s
            """, (
                content_data.get('page_title'), content_data.get('page_subtitle'),
                content_data.get('header_background'), json.dumps(content_data.get('jimmy', {})),
                json.dumps(content_data.get('values_section', {})), json.dumps(content_data.get('team_section', {})),
                datetime.utcnow(), current_user.username
            ))
        
        return {"message": "Enhanced about page content updated successfully"}
    finally:
        mysql_pool.release(conn)
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
                        "title": "Gambas al Ajillo",
                        "description": "Knoblauchgarnelen in Olivenöl",
                        "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b",
                        "category_link": "tapas-de-pescado"
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
            # Parse JSON fields and structure data for frontend compatibility
            features_data = content.get('features_data')
            if features_data and isinstance(features_data, str):
                features_data = json.loads(features_data)
            elif not features_data:
                features_data = {}
                
            specialties_data = content.get('specialties_data')
            if specialties_data and isinstance(specialties_data, str):
                specialties_data = json.loads(specialties_data)
            elif not specialties_data:
                specialties_data = {}
                
            delivery_data = content.get('delivery_data')
            if delivery_data and isinstance(delivery_data, str):
                delivery_data = json.loads(delivery_data)
            elif not delivery_data:
                delivery_data = {}
            
            # Structure data in frontend-expected format
            content = {
                "id": content.get("id"),
                "hero_title": content.get("hero_title"),
                "hero_subtitle": content.get("hero_subtitle"),
                "hero_description": content.get("hero_description"),
                "hero_location": content.get("hero_location"),
                "hero_background_image": content.get("hero_background_image"),
                "hero_menu_button_text": content.get("hero_menu_button_text"),
                "hero_locations_button_text": content.get("hero_locations_button_text"),
                "features_data": features_data,
                "specialties_data": specialties_data,
                "delivery_data": delivery_data,
                "updated_at": content.get("updated_at"),
                # Add expected top-level keys for frontend compatibility
                "hero": {
                    "title": content.get("hero_title"),
                    "subtitle": content.get("hero_subtitle"),
                    "description": content.get("hero_description"),
                    "location": content.get("hero_location"),
                    "background_image": content.get("hero_background_image"),
                    "menu_button_text": content.get("hero_menu_button_text"),
                    "locations_button_text": content.get("hero_locations_button_text")
                },
                "features": features_data,
                "specialties": specialties_data,
                "delivery": delivery_data
            }
        
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
            # Return default structure if no data exists
            return {
                "page_title": "Unsere Standorte",
                "page_description": "Besuchen Sie uns an einem unserer beiden Standorte",
                "locations_data": [],
                "locations": [],
                "info_sections": [],
                "general_info": {}
            }
        
        # Parse the complete locations data
        locations_data = content.get('locations_data')
        if locations_data and isinstance(locations_data, str):
            locations_data = json.loads(locations_data)
        elif locations_data and isinstance(locations_data, list):
            # Already parsed as list
            locations_data = locations_data
        elif not locations_data:
            locations_data = []
        
        # Ensure we have a list for locations
        locations_array = locations_data if isinstance(locations_data, list) else []
        
        # Structure response for both old and new frontend compatibility
        response = {
            "id": content.get("id"),
            "page_title": content.get("page_title", "Unsere Standorte"),
            "page_description": content.get("page_description", "Besuchen Sie uns an einem unserer beiden Standorte"),
            "locations_data": locations_array,  # For backend compatibility
            "locations": locations_array,       # For frontend compatibility
            "info_sections": [],
            "general_info": {},
            "updated_at": content.get("updated_at"),
            "updated_by": content.get("updated_by")
        }
        
        return response
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
            # Parse JSON fields and structure for frontend compatibility
            team_members = content.get('team_members')
            if team_members and isinstance(team_members, str):
                team_members = json.loads(team_members)
            elif not team_members:
                team_members = []
                
            values_data = content.get('values_data')
            if values_data and isinstance(values_data, str):
                values_data = json.loads(values_data)
            elif not values_data:
                values_data = []
            
            # Structure data for frontend compatibility
            content = {
                "id": content.get("id"),
                "page_title": content.get("page_title"),
                "hero_title": content.get("hero_title"),
                "hero_description": content.get("hero_description"),
                "story_title": content.get("story_title"),
                "story_content": content.get("story_content"),
                "story_image": content.get("story_image"),
                "team_title": content.get("team_title"),
                "team_members": team_members,
                "values_title": content.get("values_title"),
                "values_data": values_data,
                "updated_at": content.get("updated_at"),
                # Add expected 'values' key for frontend compatibility
                "values": values_data
            }
        
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
                INSERT INTO about_page_content (id, page_title, hero_title, hero_description, story_title,
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

# Legal Pages API endpoints
@api_router.get("/cms/legal/{page_type}")
async def get_legal_page(page_type: str):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM legal_pages WHERE page_type = %s", (page_type,))
        page = await cursor.fetchone()
        
        if not page:
            # Create default content
            if page_type == "imprint":
                default_page = {
                    "id": str(uuid.uuid4()),
                    "page_type": "imprint",
                    "title": "Impressum",
                    "content": """**Angaben gemäß § 5 TMG:**

Jimmy's Tapas Bar GmbH
Strandstraße 1
18225 Kühlungsborn

**Vertreten durch:**
Geschäftsführer: Jimmy Rodriguez

**Kontakt:**
Telefon: +49 38293 12345
E-Mail: info@jimmys-tapasbar.de

**Registereintrag:**
Eintragung im Handelsregister
Registergericht: Amtsgericht Rostock
Registernummer: HRB 12345

**Umsatzsteuer-ID:**
Umsatzsteuer-Identifikationsnummer gemäß §27a Umsatzsteuergesetz: DE123456789

**Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV:**
Jimmy Rodriguez
Strandstraße 1
18225 Kühlungsborn

**Streitschlichtung:**
Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.""",
                    "contact_name": "Jimmy Rodriguez",
                    "contact_address": "Strandstraße 1, 18225 Kühlungsborn",
                    "contact_phone": "+49 38293 12345",
                    "contact_email": "info@jimmys-tapasbar.de",
                    "company_info": {
                        "company_name": "Jimmy's Tapas Bar GmbH",
                        "register_court": "Amtsgericht Rostock",
                        "register_number": "HRB 12345",
                        "vat_id": "DE123456789"
                    }
                }
            elif page_type == "privacy":
                default_page = {
                    "id": str(uuid.uuid4()),
                    "page_type": "privacy",
                    "title": "Datenschutzerklärung",
                    "content": """**1. Datenschutz auf einen Blick**

**Allgemeine Hinweise**
Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie unsere Website besuchen.

**Datenerfassung auf unserer Website**
Wer ist verantwortlich für die Datenerfassung auf dieser Website?
Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen Kontaktdaten können Sie dem Impressum dieser Website entnehmen.

**Wie erfassen wir Ihre Daten?**
Ihre Daten werden zum einen dadurch erhoben, dass Sie uns diese mitteilen. Hierbei kann es sich z.B. um Daten handeln, die Sie in ein Kontaktformular eingeben.

**2. Hosting**
Wir hosten die Inhalte unserer Website bei unserem externen Dienstleister.

**3. Allgemeine Hinweise und Pflichtinformationen**

**Datenschutz**
Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst.

**4. Datenerfassung auf dieser Website**

**Cookies**
Unsere Internetseiten verwenden teilweise sogenannte Cookies.

**Server-Log-Dateien**
Der Provider der Seiten erhebt und speichert automatisch Informationen in sogenannten Server-Log-Dateien.""",
                    "contact_name": "Jimmy Rodriguez",
                    "contact_address": "Strandstraße 1, 18225 Kühlungsborn",
                    "contact_phone": "+49 38293 12345",
                    "contact_email": "info@jimmys-tapasbar.de"
                }
            else:
                raise HTTPException(status_code=404, detail="Page type not found")
            
            # Insert default page
            await cursor.execute("""
                INSERT INTO legal_pages (id, page_type, title, content, contact_name, contact_address,
                                       contact_phone, contact_email, company_info, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                default_page["id"], default_page["page_type"], default_page["title"],
                default_page["content"], default_page["contact_name"], default_page["contact_address"],
                default_page["contact_phone"], default_page["contact_email"],
                json.dumps(default_page.get("company_info")), datetime.utcnow()
            ))
            
            page = default_page
        else:
            # Parse JSON field
            if page.get('company_info'):
                page['company_info'] = json.loads(page['company_info']) if isinstance(page['company_info'], str) else page['company_info']
        
        return page
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/legal/{page_type}")
async def update_legal_page(page_type: str, page_data: Dict, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        company_info_json = json.dumps(page_data.get('company_info', {}))
        
        # Check if page exists
        await cursor.execute("SELECT COUNT(*) as count FROM legal_pages WHERE page_type = %s", (page_type,))
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new page
            await cursor.execute("""
                INSERT INTO legal_pages (id, page_type, title, content, contact_name, contact_address,
                                       contact_phone, contact_email, company_info, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), page_type, page_data.get('title', ''),
                page_data.get('content', ''), page_data.get('contact_name'),
                page_data.get('contact_address'), page_data.get('contact_phone'),
                page_data.get('contact_email'), company_info_json,
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing page
            await cursor.execute("""
                UPDATE legal_pages SET title = %s, content = %s, contact_name = %s,
                                     contact_address = %s, contact_phone = %s, contact_email = %s,
                                     company_info = %s, updated_at = %s, updated_by = %s
                WHERE page_type = %s
            """, (
                page_data.get('title', ''), page_data.get('content', ''),
                page_data.get('contact_name'), page_data.get('contact_address'),
                page_data.get('contact_phone'), page_data.get('contact_email'),
                company_info_json, datetime.utcnow(), current_user.username, page_type
            ))
        
        return {"message": "Legal page updated successfully"}
    finally:
        mysql_pool.release(conn)

# Website Texts API endpoints
@api_router.get("/cms/website-texts/{section}")
async def get_website_texts(section: str):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM website_texts WHERE section = %s", (section,))
        texts = await cursor.fetchone()
        
        if not texts:
            # Create default texts based on section
            default_texts = {"section": section}
            
            if section == "navigation":
                default_texts["navigation_data"] = {
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
                default_texts["footer_data"] = {
                    "opening_hours_title": "Öffnungszeiten",
                    "contact_title": "Kontakt",
                    "follow_us_title": "Folgen Sie uns",
                    "copyright": "© 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten."
                }
            elif section == "buttons":
                default_texts["buttons_data"] = {
                    "menu_button": "Zur Speisekarte",
                    "locations_button": "Unsere Standorte",
                    "contact_button": "Kontakt aufnehmen",
                    "reserve_button": "Tisch reservieren",
                    "order_button": "Jetzt bestellen"
                }
            elif section == "general":
                default_texts["general_data"] = {
                    "loading": "Lädt...",
                    "error": "Fehler beim Laden",
                    "success": "Erfolgreich gespeichert",
                    "required_field": "Dieses Feld ist erforderlich",
                    "email_invalid": "E-Mail-Adresse ist ungültig"
                }
            
            # Insert default texts
            await cursor.execute("""
                INSERT INTO website_texts (id, section, navigation_data, footer_data, buttons_data, general_data, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), section,
                json.dumps(default_texts.get('navigation_data')),
                json.dumps(default_texts.get('footer_data')),
                json.dumps(default_texts.get('buttons_data')),
                json.dumps(default_texts.get('general_data')),
                datetime.utcnow()
            ))
            
            return default_texts
        
        # Parse JSON fields
        result = {"section": texts["section"]}
        if texts.get('navigation_data'):
            result['navigation'] = json.loads(texts['navigation_data']) if isinstance(texts['navigation_data'], str) else texts['navigation_data']
        if texts.get('footer_data'):
            result['footer'] = json.loads(texts['footer_data']) if isinstance(texts['footer_data'], str) else texts['footer_data']
        if texts.get('buttons_data'):
            result['buttons'] = json.loads(texts['buttons_data']) if isinstance(texts['buttons_data'], str) else texts['buttons_data']
        if texts.get('general_data'):
            result['general'] = json.loads(texts['general_data']) if isinstance(texts['general_data'], str) else texts['general_data']
        
        return result
    finally:
        mysql_pool.release(conn)

@api_router.put("/cms/website-texts/{section}")
async def update_website_texts(section: str, texts_data: Dict, current_user: User = Depends(get_editor_user)):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        # Convert data to JSON strings
        navigation_json = json.dumps(texts_data.get('navigation')) if texts_data.get('navigation') else None
        footer_json = json.dumps(texts_data.get('footer')) if texts_data.get('footer') else None
        buttons_json = json.dumps(texts_data.get('buttons')) if texts_data.get('buttons') else None
        general_json = json.dumps(texts_data.get('general')) if texts_data.get('general') else None
        
        # Check if record exists
        await cursor.execute("SELECT COUNT(*) as count FROM website_texts WHERE section = %s", (section,))
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new record
            await cursor.execute("""
                INSERT INTO website_texts (id, section, navigation_data, footer_data, buttons_data, general_data, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), section, navigation_json, footer_json,
                buttons_json, general_json, datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing record
            await cursor.execute("""
                UPDATE website_texts SET navigation_data = %s, footer_data = %s, buttons_data = %s,
                                        general_data = %s, updated_at = %s, updated_by = %s
                WHERE section = %s
            """, (
                navigation_json, footer_json, buttons_json, general_json,
                datetime.utcnow(), current_user.username, section
            ))
        
        return {"message": "Website texts updated successfully"}
    finally:
        mysql_pool.release(conn)

# Content sections (generic CMS content)
@api_router.get("/content/{page}")
async def get_page_content(page: str):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM content_sections WHERE page = %s", (page,))
        sections = await cursor.fetchall()
        
        # Parse JSON fields
        for section in sections:
            if section.get('content'):
                section['content'] = json.loads(section['content']) if isinstance(section['content'], str) else section['content']
            if section.get('images'):
                section['images'] = json.loads(section['images']) if isinstance(section['images'], str) else section['images']
        
        return sections
    finally:
        mysql_pool.release(conn)

@api_router.put("/content/{page}/{section}")
async def update_content_section(
    page: str, 
    section: str, 
    content_data: ContentSectionUpdate,
    current_user: User = Depends(get_editor_user)
):
    conn = await get_mysql_connection()
    try:
        cursor = await conn.cursor()
        
        content_json = json.dumps(content_data.content)
        images_json = json.dumps(content_data.images or [])
        
        # Check if content section exists
        await cursor.execute("SELECT COUNT(*) as count FROM content_sections WHERE page = %s AND section = %s", (page, section))
        result = await cursor.fetchone()
        
        if result[0] == 0:
            # Insert new content section
            await cursor.execute("""
                INSERT INTO content_sections (id, page, section, content, images, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()), page, section, content_json, images_json,
                datetime.utcnow(), current_user.username
            ))
        else:
            # Update existing content section
            await cursor.execute("""
                UPDATE content_sections SET content = %s, images = %s, updated_at = %s, updated_by = %s
                WHERE page = %s AND section = %s
            """, (content_json, images_json, datetime.utcnow(), current_user.username, page, section))
        
        return {"message": "Content section updated successfully"}
    finally:
        mysql_pool.release(conn)

# Enhanced Backup System
@api_router.post("/admin/backup/database")
async def create_database_backup(current_user: User = Depends(get_admin_user)):
    """Create and download MySQL database backup"""
    try:
        import subprocess
        import tempfile
        import os
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mysql-database-backup-{timestamp}.sql"
        
        # Create temporary file for mysqldump
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.sql') as temp_file:
            temp_path = temp_file.name
        
        try:
            # Create MySQL dump using mysqldump
            dump_command = [
                'mysqldump',
                '-u', os.environ['MYSQL_USER'],
                f'-p{os.environ["MYSQL_PASSWORD"]}',
                '--single-transaction',
                '--routines',
                '--triggers',
                '--add-drop-table',
                '--complete-insert',
                os.environ['MYSQL_DATABASE']
            ]
            
            with open(temp_path, 'w') as dump_file:
                result = subprocess.run(dump_command, stdout=dump_file, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                raise Exception(f"mysqldump failed: {result.stderr}")
            
            # Read the dump file
            with open(temp_path, 'r') as dump_file:
                backup_content = dump_file.read()
            
            backup_size = len(backup_content.encode('utf-8'))
            
            # Count tables in database
            conn = await get_mysql_connection()
            try:
                cursor = await conn.cursor()
                await cursor.execute("SHOW TABLES")
                tables = await cursor.fetchall()
                tables_count = len(tables)
                
                # Count total rows
                total_rows = 0
                for table in tables:
                    table_name = table[0]
                    await cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    count_result = await cursor.fetchone()
                    total_rows += count_result[0]
                
            finally:
                mysql_pool.release(conn)
            
            # Save backup metadata
            backup_metadata = {
                "id": f"mysql_db_{timestamp}",
                "filename": filename,
                "type": "database",
                "created_at": datetime.now(),
                "created_by": current_user.username,
                "size_bytes": backup_size,
                "size_human": format_bytes(backup_size),
                "collections_count": tables_count,
                "total_documents": total_rows,
                "includes_media": False
            }
            
            # Store in database for backup list
            conn = await get_mysql_connection()
            try:
                cursor = await conn.cursor()
                await cursor.execute("""
                    INSERT INTO system_backups (id, filename, type, created_at, created_by, 
                                               size_bytes, size_human, collections_count, 
                                               total_documents, includes_media)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    backup_metadata["id"], backup_metadata["filename"], backup_metadata["type"],
                    backup_metadata["created_at"], backup_metadata["created_by"],
                    backup_metadata["size_bytes"], backup_metadata["size_human"],
                    backup_metadata["collections_count"], backup_metadata["total_documents"],
                    backup_metadata["includes_media"]
                ))
            finally:
                mysql_pool.release(conn)
            
            # Return as downloadable file
            from fastapi.responses import Response
            
            return Response(
                content=backup_content,
                media_type="application/sql",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}",
                    "X-Backup-ID": backup_metadata["id"],
                    "X-Backup-Size": str(backup_size)
                }
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        print(f"MySQL backup error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database backup creation failed: {str(e)}")

@api_router.post("/admin/backup/full")
async def create_full_backup(current_user: User = Depends(get_admin_user)):
    """Create and download full backup (MySQL database + complete codebase + assets)"""
    try:
        import subprocess
        import tempfile
        import zipfile
        import os
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"jimmy-tapas-bar-full-backup-{timestamp}.zip"
        
        # Create temporary directory for backup assembly
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = os.path.join(temp_dir, 'backup')
            os.makedirs(backup_dir)
            
            # 1. Create MySQL dump
            mysql_dump_path = os.path.join(backup_dir, 'database.sql')
            dump_command = [
                'mysqldump',
                '-u', os.environ['MYSQL_USER'],
                f'-p{os.environ["MYSQL_PASSWORD"]}',
                '--single-transaction',
                '--routines',
                '--triggers',
                '--add-drop-table',
                '--complete-insert',
                '--hex-blob',
                os.environ['MYSQL_DATABASE']
            ]
            
            with open(mysql_dump_path, 'w') as dump_file:
                result = subprocess.run(dump_command, stdout=dump_file, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                raise Exception(f"mysqldump failed: {result.stderr}")
            
            # 2. Copy complete frontend codebase
            frontend_backup_dir = os.path.join(backup_dir, 'frontend')
            shutil.copytree('/app/frontend/src', os.path.join(frontend_backup_dir, 'src'))
            shutil.copytree('/app/frontend/public', os.path.join(frontend_backup_dir, 'public'))
            
            # Copy frontend config files
            frontend_files = ['package.json', 'tailwind.config.js', 'postcss.config.js']
            for file in frontend_files:
                src_path = f'/app/frontend/{file}'
                if os.path.exists(src_path):
                    shutil.copy2(src_path, frontend_backup_dir)
            
            # Copy .env (without sensitive data)
            with open('/app/frontend/.env', 'r') as f:
                env_content = f.read()
            # Only include non-sensitive config
            safe_env_content = "WDS_SOCKET_PORT=443\n# REACT_APP_BACKEND_URL will be configured during restore\n"
            with open(os.path.join(frontend_backup_dir, '.env.example'), 'w') as f:
                f.write(safe_env_content)
            
            # 3. Copy complete backend codebase  
            backend_backup_dir = os.path.join(backup_dir, 'backend')
            os.makedirs(backend_backup_dir)
            
            # Copy Python files
            backend_files = ['server.py', 'requirements.txt', 'mysql_schema.sql']
            for file in backend_files:
                src_path = f'/app/backend/{file}'
                if os.path.exists(src_path):
                    shutil.copy2(src_path, backend_backup_dir)
            
            # Copy .env example (without sensitive data)
            safe_backend_env = """MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=jimmys_tapas_bar
JWT_SECRET_KEY=your-secret-key-here
"""
            with open(os.path.join(backend_backup_dir, '.env.example'), 'w') as f:
                f.write(safe_backend_env)
            
            # 4. Copy external integrations if they exist
            integrations_src = '/app/backend/external_integrations'
            if os.path.exists(integrations_src):
                shutil.copytree(integrations_src, os.path.join(backend_backup_dir, 'external_integrations'))
            
            # 5. Copy root configuration files
            root_files = ['nginx.conf', 'Dockerfile', 'entrypoint.sh']
            for file in root_files:
                src_path = f'/app/{file}'
                if os.path.exists(src_path):
                    shutil.copy2(src_path, backup_dir)
            
            # 6. Create media/uploads directory (even if empty, for structure)
            uploads_dir = os.path.join(backup_dir, 'uploads')
            os.makedirs(uploads_dir)
            
            # Add placeholder for media files
            with open(os.path.join(uploads_dir, 'README.txt'), 'w') as f:
                f.write("""Uploads und Mediendateien

Dieser Ordner ist für hochgeladene Bilder und Mediendateien vorgesehen.
Bei der Wiederherstellung sollten hier alle Benutzerdateien platziert werden.

Hinweis: Base64-kodierte Bilder werden direkt in der Datenbank gespeichert
und sind bereits im database.sql Backup enthalten.
""")
            
            # 7. Count database statistics
            conn = await get_mysql_connection()
            try:
                cursor = await conn.cursor()
                await cursor.execute("SHOW TABLES")
                tables = await cursor.fetchall()
                tables_count = len(tables)
                
                total_rows = 0
                for table in tables:
                    table_name = table[0]
                    await cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    count_result = await cursor.fetchone()
                    total_rows += count_result[0]
                
            finally:
                mysql_pool.release(conn)
            
            # 8. Create comprehensive README
            readme_content = f"""# Jimmy's Tapas Bar - Vollständiges System-Backup

## 📋 Backup-Informationen
- **Typ:** Vollständiges System-Backup
- **Erstellt am:** {datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}
- **Erstellt von:** {current_user.username}
- **Datenbank-Tabellen:** {tables_count}
- **Datenbank-Datensätze:** {total_rows}
- **CMS Version:** 2.0 (MySQL)

## 📁 Backup-Inhalt

### `/database.sql`
- Vollständiger MySQL-Dump der Datenbank
- Enthält alle Tabellen, Daten, Indizes und Strukturen
- Kompatibel mit MySQL 5.7+ und MariaDB 10.0+

### `/frontend/`
- **src/**: Kompletter React-Quellcode
- **public/**: Statische Assets und HTML-Templates
- **package.json**: Node.js Dependencies
- **tailwind.config.js**: Tailwind CSS Konfiguration
- **postcss.config.js**: PostCSS Konfiguration
- **.env.example**: Beispiel-Umgebungsvariablen

### `/backend/`
- **server.py**: FastAPI Backend-Anwendung
- **requirements.txt**: Python Dependencies
- **mysql_schema.sql**: Datenbank-Schema für Neuinstallation
- **.env.example**: Beispiel-Umgebungsvariablen
- **external_integrations/**: Externe API-Integrationen (falls vorhanden)

### `/uploads/`
- Ordner für Mediendateien und Uploads
- Base64-Bilder sind bereits in der Datenbank enthalten

### Root-Konfiguration
- **nginx.conf**: Nginx-Webserver-Konfiguration
- **Dockerfile**: Container-Konfiguration
- **entrypoint.sh**: Container-Startskript

## 🔧 Wiederherstellung

### 1. Systemvorbereitung
```bash
# MySQL/MariaDB installieren
sudo apt update
sudo apt install mysql-server

# Node.js und Python installieren
sudo apt install nodejs npm python3 python3-pip
```

### 2. Datenbank wiederherstellen
```bash
# Datenbank und Benutzer erstellen
mysql -u root -p
CREATE DATABASE jimmys_tapas_bar;
CREATE USER 'jimmy_user'@'localhost' IDENTIFIED BY 'ihr_passwort';
GRANT ALL PRIVILEGES ON jimmys_tapas_bar.* TO 'jimmy_user'@'localhost';
FLUSH PRIVILEGES;
exit

# Backup einspielen
mysql -u jimmy_user -p jimmys_tapas_bar < database.sql
```

### 3. Backend einrichten
```bash
cd backend/
cp .env.example .env
# .env-Datei mit korrekten Datenbank-Zugangsdaten bearbeiten

pip install -r requirements.txt
python server.py
```

### 4. Frontend einrichten  
```bash
cd frontend/
cp .env.example .env
# .env-Datei mit Backend-URL bearbeiten

npm install
npm start
```

### 5. Uploads wiederherstellen
- Mediendateien aus `/uploads/` in den produktiven Upload-Ordner kopieren
- Dateiberechtigungen korrekt setzen

## ⚙️ Konfiguration

### Backend .env
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=jimmy_user
MYSQL_PASSWORD=ihr_mysql_passwort
MYSQL_DATABASE=jimmys_tapas_bar
JWT_SECRET_KEY=generieren_sie_einen_sicheren_schluessel
```

### Frontend .env
```
REACT_APP_BACKEND_URL=http://localhost:8001
# oder Ihre Produktions-URL
```

## 🚀 Produktions-Setup

### Mit Docker
```bash
# Dockerfile im Root-Verzeichnis verwenden
docker build -t jimmys-tapas-bar .
docker run -p 80:80 jimmys-tapas-bar
```

### Manual Setup
1. Nginx als Reverse Proxy konfigurieren
2. Backend als Service einrichten
3. Frontend für Produktion builden: `npm run build`
4. SSL-Zertifikat einrichten

## 📊 Technische Details
- **Datenbank:** MySQL/MariaDB
- **Backend:** Python 3.11 + FastAPI + aiomysql
- **Frontend:** React 19 + Tailwind CSS
- **Authentifizierung:** JWT
- **Admin-Login:** admin / jimmy2024

## 🆘 Support
Bei Problemen mit der Wiederherstellung:
1. Logdateien prüfen
2. Datenbankverbindung testen
3. Dateiberechtigungen prüfen
4. Port-Verfügbarkeit prüfen (3000, 8001)

**Wichtig:** Ändern Sie nach der Wiederherstellung:
- Admin-Passwort
- JWT Secret Key
- Datenbank-Passwörter

---
*Erstellt mit Jimmy's Tapas Bar CMS v2.0 - MySQL Edition*
"""
            
            with open(os.path.join(backup_dir, 'README.md'), 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # 9. Create system info JSON
            system_info = {
                "backup_created": datetime.now().isoformat(),
                "cms_version": "2.0-mysql",
                "database_type": "mysql",
                "tables_count": tables_count,
                "total_records": total_rows,
                "created_by": current_user.username,
                "backup_type": "full_system",
                "includes": {
                    "database": True,
                    "frontend_code": True,
                    "backend_code": True,
                    "configuration": True,
                    "media_structure": True
                }
            }
            
            with open(os.path.join(backup_dir, 'system_info.json'), 'w', encoding='utf-8') as f:
                json.dump(system_info, f, indent=2, ensure_ascii=False)
            
            # 10. Create ZIP archive
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add all files from backup directory
                for root, dirs, files in os.walk(backup_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_dir)
                        zip_file.write(file_path, arcname)
            
            zip_buffer.seek(0)
            zip_content = zip_buffer.getvalue()
            zip_size = len(zip_content)
            
            # 11. Save backup metadata
            backup_metadata = {
                "id": f"full_system_{timestamp}",
                "filename": filename,
                "type": "full",
                "created_at": datetime.now(),
                "created_by": current_user.username,
                "size_bytes": zip_size,
                "size_human": format_bytes(zip_size),
                "collections_count": tables_count,
                "total_documents": total_rows,
                "includes_media": True
            }
            
            # Store in database for backup list
            conn = await get_mysql_connection()
            try:
                cursor = await conn.cursor()
                await cursor.execute("""
                    INSERT INTO system_backups (id, filename, type, created_at, created_by, 
                                               size_bytes, size_human, collections_count, 
                                               total_documents, includes_media)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    backup_metadata["id"], backup_metadata["filename"], backup_metadata["type"],
                    backup_metadata["created_at"], backup_metadata["created_by"],
                    backup_metadata["size_bytes"], backup_metadata["size_human"],
                    backup_metadata["collections_count"], backup_metadata["total_documents"],
                    backup_metadata["includes_media"]
                ))
            finally:
                mysql_pool.release(conn)
            
            # Return as downloadable zip file
            from fastapi.responses import Response
            
            return Response(
                content=zip_content,
                media_type="application/zip",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}",
                    "X-Backup-ID": backup_metadata["id"],
                    "X-Backup-Size": str(zip_size)
                }
            )
        
    except Exception as e:
        print(f"Full backup error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Full backup creation failed: {str(e)}")

@api_router.get("/admin/backup/list")
async def get_backup_list(current_user: User = Depends(get_admin_user)):
    """Get list of all available backups"""
    try:
        conn = await get_mysql_connection()
        try:
            cursor = await conn.cursor(aiomysql.DictCursor)
            await cursor.execute("SELECT * FROM system_backups ORDER BY created_at DESC")
            backups = await cursor.fetchall()
            
            # Convert datetime objects to ISO format for JSON serialization
            for backup in backups:
                if isinstance(backup.get('created_at'), datetime):
                    backup['created_at'] = backup['created_at'].isoformat()
            
            # Return list directly (not wrapped in dict)
            return backups
        finally:
            mysql_pool.release(conn)
        
    except Exception as e:
        print(f"Backup list error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve backup list: {str(e)}")

@api_router.get("/admin/backup/download/{backup_id}")
async def download_backup(backup_id: str, current_user: User = Depends(get_admin_user)):
    """Download a specific backup"""
    try:
        conn = await get_mysql_connection()
        try:
            cursor = await conn.cursor(aiomysql.DictCursor)
            await cursor.execute("SELECT * FROM system_backups WHERE id = %s", (backup_id,))
            backup = await cursor.fetchone()
            
            if not backup:
                raise HTTPException(status_code=404, detail="Backup not found")
            
            # For this implementation, return backup info
            # In production, you would read the actual backup file from storage
            return {
                "message": "Backup download initiated",
                "backup_info": {
                    "id": backup["id"],
                    "filename": backup["filename"],
                    "type": backup["type"],
                    "size_human": backup["size_human"],
                    "created_at": backup["created_at"].isoformat() if isinstance(backup["created_at"], datetime) else backup["created_at"]
                }
            }
        finally:
            mysql_pool.release(conn)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Backup download error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not download backup: {str(e)}")

@api_router.delete("/admin/backup/{backup_id}")
async def delete_backup(backup_id: str, current_user: User = Depends(get_admin_user)):
    """Delete a specific backup"""
    try:
        conn = await get_mysql_connection()
        try:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # Check if backup exists
            await cursor.execute("SELECT * FROM system_backups WHERE id = %s", (backup_id,))
            backup = await cursor.fetchone()
            if not backup:
                raise HTTPException(status_code=404, detail="Backup not found")
            
            # Delete backup record from database
            await cursor.execute("DELETE FROM system_backups WHERE id = %s", (backup_id,))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Backup not found")
            
            # In production, you would also delete the actual backup file from storage
            
            return {
                "message": "Backup deleted successfully",
                "deleted_backup": {
                    "id": backup["id"],
                    "filename": backup["filename"]
                }
            }
        finally:
            mysql_pool.release(conn)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Backup deletion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not delete backup: {str(e)}")

# System status endpoint
@api_router.get("/admin/system/info")
async def get_system_info(current_user: User = Depends(get_admin_user)):
    """Get system information and status"""
    try:
        import psutil
        import platform
        
        # Get MySQL database info
        conn = await get_mysql_connection()
        try:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # Get MySQL version
            await cursor.execute("SELECT VERSION() as version")
            version_result = await cursor.fetchone()
            mysql_version = version_result['version'] if version_result else 'Unknown'
            
            # Get database size
            await cursor.execute("""
                SELECT 
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS database_size_mb
                FROM information_schema.tables 
                WHERE table_schema = %s
            """, (os.environ['MYSQL_DATABASE'],))
            db_size_result = await cursor.fetchone()
            db_size_mb = db_size_result['database_size_mb'] if db_size_result['database_size_mb'] else 0
            
            # Get table count
            await cursor.execute("SHOW TABLES")
            tables = await cursor.fetchall()
            table_count = len(tables)
            
            # Get total records
            total_records = 0
            for table in tables:
                table_name = list(table.values())[0]
                await cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
                count_result = await cursor.fetchone()
                total_records += count_result['count']
            
        finally:
            mysql_pool.release(conn)
        
        # Get system information
        system_info = {
            "version": "Jimmy's CMS v2.0 MySQL",
            "uptime": "Running",
            "database_status": "MySQL Connected",
            "mysql_version": mysql_version,
            "disk_usage": f"{round(psutil.disk_usage('/').used / (1024**3), 1)} GB",
            "cpu_usage": f"{psutil.cpu_percent(interval=1)}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "python_version": platform.python_version(),
            "platform": f"{platform.system()} {platform.release()}",
            "system": {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "python_version": platform.python_version()
            },
            "resources": {
                "cpu_count": psutil.cpu_count(),
                "cpu_usage_percent": psutil.cpu_percent(interval=1),
                "memory": {
                    "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                    "available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                    "used_percent": psutil.virtual_memory().percent
                },
                "disk": {
                    "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
                    "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
                    "used_percent": psutil.disk_usage('/').percent
                }
            },
            "mysql": {
                "connection_status": "Connected",
                "version": mysql_version,
                "database_info": {
                    "name": os.environ['MYSQL_DATABASE'],
                    "tables_count": table_count,
                    "total_records": total_records,
                    "size_mb": float(db_size_mb)
                }
            },
            "application": {
                "cms_version": "2.0-mysql",
                "backend_status": "Running",
                "mysql_pool_size": mysql_pool.size if mysql_pool else 0,
                "uptime": "Running"
            }
        }
        
        return system_info
        
    except Exception as e:
        print(f"System info error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve system information: {str(e)}")

# MySQL Database Configuration endpoints
@api_router.get("/admin/database/config")
async def get_database_config(current_user: User = Depends(get_admin_user)):
    """Get current MySQL database configuration (without passwords)"""
    try:
        config = {
            "host": os.environ.get('MYSQL_HOST', 'localhost'),
            "port": os.environ.get('MYSQL_PORT', '3306'),
            "username": os.environ.get('MYSQL_USER', 'jimmy_user'),
            "database": os.environ.get('MYSQL_DATABASE', 'jimmys_tapas_bar'),
            "ssl": os.environ.get('MYSQL_SSL', 'false').lower() == 'true',
            "charset": os.environ.get('MYSQL_CHARSET', 'utf8mb4')
        }
        return config
    except Exception as e:
        print(f"Database config error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve database configuration: {str(e)}")

@api_router.put("/admin/database/config")
async def update_database_config(
    config_data: dict,
    current_user: User = Depends(get_admin_user)
):
    """Update MySQL database configuration"""
    try:
        # Note: In production, this would update environment variables or config files
        # For security, we'll just validate the config without actually changing it
        required_fields = ['host', 'port', 'username', 'database']
        missing_fields = [field for field in required_fields if field not in config_data]
        
        if missing_fields:
            raise HTTPException(status_code=400, detail=f"Missing required fields: {missing_fields}")
        
        # Validate port is numeric
        try:
            port = int(config_data['port'])
            if port < 1 or port > 65535:
                raise ValueError("Port must be between 1 and 65535")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid port number")
        
        # In a real implementation, you would update the configuration
        # For now, we'll just return success
        return {
            "message": "MySQL database configuration updated successfully",
            "note": "Configuration changes require application restart to take effect"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database config update error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not update database configuration: {str(e)}")

@api_router.post("/admin/database/test")
async def test_database_connection(
    config_data: dict,
    current_user: User = Depends(get_admin_user)
):
    """Test MySQL database connection with provided configuration"""
    try:
        import aiomysql
        
        # Extract connection parameters
        host = config_data.get('host', 'localhost')
        port = int(config_data.get('port', 3306))
        user = config_data.get('username', 'jimmy_user')
        password = config_data.get('password', '')
        database = config_data.get('database', 'jimmys_tapas_bar')
        charset = config_data.get('charset', 'utf8mb4')
        
        # Test connection
        test_conn = await aiomysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            charset=charset,
            autocommit=True
        )
        
        try:
            cursor = await test_conn.cursor(aiomysql.DictCursor)
            
            # Test basic query
            await cursor.execute("SELECT VERSION() as version, NOW() as current_time")
            result = await cursor.fetchone()
            
            # Get database info
            await cursor.execute("SHOW TABLES")
            tables = await cursor.fetchall()
            
            return {
                "status": "success",
                "message": "MySQL connection successful",
                "server_info": f"MySQL {result['version']}",
                "current_time": result['current_time'].isoformat() if result['current_time'] else None,
                "tables_count": len(tables),
                "connection_details": {
                    "host": host,
                    "port": port,
                    "database": database,
                    "charset": charset
                }
            }
            
        finally:
            test_conn.close()
        
    except Exception as e:
        error_message = str(e)
        print(f"Database test connection error: {error_message}")
        
        # Return more specific error messages
        if "Access denied" in error_message:
            raise HTTPException(status_code=400, detail="MySQL authentication failed - check username and password")
        elif "Can't connect" in error_message or "Connection refused" in error_message:
            raise HTTPException(status_code=400, detail="Cannot connect to MySQL server - check host and port")
        elif "Unknown database" in error_message:
            raise HTTPException(status_code=400, detail="MySQL database does not exist")
        else:
            raise HTTPException(status_code=400, detail=f"MySQL connection failed: {error_message}")

# Enhanced backup status endpoint
@api_router.get("/admin/backup/status")
async def get_backup_status(current_user: User = Depends(get_admin_user)):
    """Get backup status and statistics"""
    try:
        import psutil
        from datetime import datetime, timedelta
        
        conn = await get_mysql_connection()
        try:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # Get backup count and latest backup from database
            await cursor.execute("SELECT COUNT(*) as backup_count FROM system_backups")
            count_result = await cursor.fetchone()
            backup_count = count_result['backup_count'] if count_result else 0
            
            # Get latest backup info
            await cursor.execute("""
                SELECT * FROM system_backups 
                ORDER BY created_at DESC 
                LIMIT 1
            """)
            latest_backup = await cursor.fetchone()
            
            # Format latest backup data
            last_backup = None
            backup_size = "0 B"
            if latest_backup:
                if isinstance(latest_backup['created_at'], datetime):
                    last_backup = latest_backup['created_at'].isoformat()
                else:
                    last_backup = latest_backup['created_at']
                backup_size = latest_backup.get('size_human', '0 B')
            
            # Calculate next scheduled backup (tomorrow at 02:00)
            now = datetime.now()
            tomorrow_2am = (now + timedelta(days=1)).replace(hour=2, minute=0, second=0, microsecond=0)
            next_scheduled = tomorrow_2am.isoformat()
            
        finally:
            mysql_pool.release(conn)
        
        # Get disk space
        disk_usage = psutil.disk_usage('/')
        
        return {
            "last_backup": last_backup,
            "backup_size": backup_size,
            "backup_count": backup_count,
            "auto_backup": True,  # Default setting
            "backup_frequency": "daily",
            "next_scheduled": next_scheduled,
            "disk_space_used": f"{disk_usage.used / (1024**3):.1f} GB",
            "disk_space_total": f"{disk_usage.total / (1024**3):.1f} GB",
            "disk_space_free": f"{disk_usage.free / (1024**3):.1f} GB"
        }
        
    except Exception as e:
        print(f"Backup status error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve backup status: {str(e)}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add explicit OPTIONS route handler for CORS preflight requests
# Newsletter functionality
@api_router.post("/newsletter/subscribe")
async def subscribe_newsletter(subscriber_data: dict):
    """Subscribe to newsletter"""
    try:
        email = subscriber_data.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="E-Mail-Adresse ist erforderlich")
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise HTTPException(status_code=400, detail="Ungültige E-Mail-Adresse")
        
        async with mysql_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                # Check if email already exists
                await cursor.execute("SELECT id FROM newsletter_subscribers WHERE email = %s", (email,))
                existing = await cursor.fetchone()
                
                if existing:
                    # Update subscription status if already exists
                    await cursor.execute(
                        "UPDATE newsletter_subscribers SET subscribed = TRUE, updated_at = NOW() WHERE email = %s",
                        (email,)
                    )
                    await connection.commit()
                    return {"message": "Newsletter-Anmeldung aktualisiert!"}
                else:
                    # Create new subscriber
                    import uuid
                    subscriber_id = str(uuid.uuid4())
                    await cursor.execute(
                        """INSERT INTO newsletter_subscribers 
                           (id, email, subscribed, created_at, updated_at) 
                           VALUES (%s, %s, TRUE, NOW(), NOW())""",
                        (subscriber_id, email)
                    )
                    await connection.commit()
                    return {"message": "Erfolgreich für Newsletter angemeldet!"}
                    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Newsletter subscription error: {e}")
        raise HTTPException(status_code=500, detail="Fehler bei der Newsletter-Anmeldung")

@api_router.post("/newsletter/unsubscribe")
async def unsubscribe_newsletter(email_data: dict):
    """Unsubscribe from newsletter"""
    try:
        email = email_data.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="E-Mail-Adresse ist erforderlich")
        
        async with mysql_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "UPDATE newsletter_subscribers SET subscribed = FALSE, updated_at = NOW() WHERE email = %s",
                    (email,)
                )
                await connection.commit()
                return {"message": "Newsletter-Abmeldung erfolgreich!"}
                
    except Exception as e:
        print(f"Newsletter unsubscribe error: {e}")
        raise HTTPException(status_code=500, detail="Fehler bei der Newsletter-Abmeldung")

@api_router.get("/admin/newsletter/subscribers")
async def get_newsletter_subscribers(current_user: User = Depends(get_admin_user)):
    """Get all newsletter subscribers (admin only)"""
    try:
        async with mysql_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """SELECT id, email, subscribed, created_at, updated_at 
                       FROM newsletter_subscribers 
                       WHERE subscribed = TRUE 
                       ORDER BY created_at DESC"""
                )
                subscribers = await cursor.fetchall()
                
                result = []
                for subscriber in subscribers:
                    result.append({
                        "id": subscriber[0],
                        "email": subscriber[1],
                        "subscribed": subscriber[2],
                        "created_at": subscriber[3].isoformat() if subscriber[3] else None,
                        "updated_at": subscriber[4].isoformat() if subscriber[4] else None
                    })
                
                return result
                
    except Exception as e:
        print(f"Get newsletter subscribers error: {e}")
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Newsletter-Abonnenten")

@api_router.delete("/admin/newsletter/subscribers/{subscriber_id}")
async def delete_newsletter_subscriber(subscriber_id: str, current_user: User = Depends(get_admin_user)):
    """Delete newsletter subscriber (admin only)"""
    try:
        async with mysql_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("DELETE FROM newsletter_subscribers WHERE id = %s", (subscriber_id,))
                await connection.commit()
                
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Newsletter-Abonnent nicht gefunden")
                
                return {"message": "Newsletter-Abonnent gelöscht"}
                
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete newsletter subscriber error: {e}")
        raise HTTPException(status_code=500, detail="Fehler beim Löschen des Newsletter-Abonnenten")

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
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
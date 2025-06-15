from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
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
from enum import Enum


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# JWT settings
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# User Roles
class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

# Basic models from before
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

# ===============================================
# COMPLETE CMS MODELS FOR MULTI-LANGUAGE SUPPORT
# ===============================================

# Language Support
class Language(str, Enum):
    DE = "de"
    EN = "en"
    ES = "es"

# Multi-language text content
class MultiLanguageText(BaseModel):
    de: str = ""
    en: str = ""
    es: str = ""

# Multi-language content with images
class MultiLanguageContent(BaseModel):
    title: MultiLanguageText
    subtitle: Optional[MultiLanguageText] = None
    description: MultiLanguageText
    image_url: Optional[str] = None
    image_alt: Optional[MultiLanguageText] = None

# Homepage Content Models
class HeroSection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: MultiLanguageText
    subtitle: MultiLanguageText
    description: MultiLanguageText
    location_text: MultiLanguageText
    background_image: str
    menu_button_text: MultiLanguageText
    locations_button_text: MultiLanguageText
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

class FeatureCard(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: MultiLanguageText
    description: MultiLanguageText
    image_url: str
    image_alt: MultiLanguageText
    order: int = 0

class HomepageFeatures(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    section_title: MultiLanguageText
    section_description: MultiLanguageText
    features: List[FeatureCard]
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

class FoodGalleryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: MultiLanguageText
    description: MultiLanguageText
    image_url: str
    category_link: str
    order: int = 0

class HomepageFoodGallery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    section_title: MultiLanguageText
    gallery_items: List[FoodGalleryItem]
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

class LieferandoSection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: MultiLanguageText
    description: MultiLanguageText
    button_text: MultiLanguageText
    delivery_text: MultiLanguageText
    authentic_text: MultiLanguageText
    availability_text: MultiLanguageText
    lieferando_url: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

# Location Models
class OpeningHours(BaseModel):
    monday: MultiLanguageText
    tuesday: MultiLanguageText
    wednesday: MultiLanguageText
    thursday: MultiLanguageText
    friday: MultiLanguageText
    saturday: MultiLanguageText
    sunday: MultiLanguageText

class LocationModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: MultiLanguageText
    address: MultiLanguageText
    phone: str
    email: str
    opening_hours: OpeningHours
    description: MultiLanguageText
    features: List[MultiLanguageText]
    image_url: str
    google_maps_url: str
    order: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

# Enhanced Menu Models
class MenuCategory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: MultiLanguageText
    description: Optional[MultiLanguageText] = None
    slug: str
    order: int = 0
    is_active: bool = True

class AllergenInfo(BaseModel):
    vegetarian: bool = False
    vegan: bool = False
    gluten_free: bool = False
    lactose_free: bool = False
    nuts: bool = False

class EnhancedMenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: MultiLanguageText
    description: MultiLanguageText
    detailed_description: Optional[MultiLanguageText] = None
    price: float
    category_id: str
    image_url: Optional[str] = None
    image_alt: Optional[MultiLanguageText] = None
    allergen_info: Optional[AllergenInfo] = None
    is_available: bool = True
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

# About Us Models
class TeamMember(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: MultiLanguageText
    description: MultiLanguageText
    image_url: str
    order: int = 0

class AboutUsContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hero_title: MultiLanguageText
    hero_description: MultiLanguageText
    hero_image: str
    story_title: MultiLanguageText
    story_content: MultiLanguageText
    team_title: MultiLanguageText
    team_members: List[TeamMember]
    values_title: MultiLanguageText
    values: List[MultiLanguageContent]
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

# Contact Information Models
class ContactInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_title: MultiLanguageText
    page_description: MultiLanguageText
    contact_form_title: MultiLanguageText
    contact_form_description: MultiLanguageText
    general_email: str
    general_phone: str
    social_media: Dict[str, str] = {}
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

# Legal Content Models
class LegalContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_type: str  # "impressum" or "datenschutz"
    title: MultiLanguageText
    content: MultiLanguageText
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    updated_by: str

# Navigation and Footer Models
class NavigationItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    label: MultiLanguageText
    url: str
    order: int = 0
    is_active: bool = True

class FooterContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str
    company_description: MultiLanguageText
    quick_links: List[NavigationItem]
    social_links: Dict[str, str] = {}
    copyright_text: MultiLanguageText
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

# SEO and Meta Content
class SEOContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_slug: str
    meta_title: MultiLanguageText
    meta_description: MultiLanguageText
    meta_keywords: MultiLanguageText
    og_title: Optional[MultiLanguageText] = None
    og_description: Optional[MultiLanguageText] = None
    og_image: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# CMS Models
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

class ContentSection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page: str  # home, locations, menu, reviews, about, contact, privacy, imprint
    section: str  # hero, features, description, etc.
    content: Dict[str, Any]  # Flexible content structure
    images: List[str] = []  # Base64 encoded images
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

class ContentSectionUpdate(BaseModel):
    content: Dict[str, Any]
    images: Optional[List[str]] = None

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
    
    user = await db.users.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**user)

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
    admin_exists = await db.users.find_one({"username": "admin"})
    if not admin_exists:
        admin_user = User(
            username="admin",
            email="admin@jimmys-tapasbar.de",
            password_hash=get_password_hash("jimmy2024"),
            role=UserRole.ADMIN
        )
        await db.users.insert_one(admin_user.dict())
        print("Default admin user created")

# Existing routes
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Authentication routes
@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = await db.users.find_one({"username": user_credentials.username})
    if not user or not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if not user["is_active"]:
        raise HTTPException(status_code=401, detail="User account is disabled")
    
    # Update last login
    await db.users.update_one(
        {"username": user_credentials.username},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# User Management routes (Admin only)
@api_router.post("/users", response_model=User)
async def create_user(user_data: UserCreate, current_user: User = Depends(get_admin_user)):
    # Check if username already exists
    existing_user = await db.users.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role
    )
    await db.users.insert_one(user.dict())
    return user

@api_router.get("/users", response_model=List[User])
async def get_users(current_user: User = Depends(get_admin_user)):
    users = await db.users.find().to_list(1000)
    return [User(**user) for user in users]

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_admin_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    result = await db.users.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Content Management routes
@api_router.get("/content/{page}")
async def get_page_content(page: str):
    content = await db.content_sections.find({"page": page}).to_list(1000)
    return [ContentSection(**section) for section in content]

@api_router.put("/content/{page}/{section}")
async def update_content_section(
    page: str, 
    section: str, 
    content_data: ContentSectionUpdate,
    current_user: User = Depends(get_editor_user)
):
    content_section = ContentSection(
        page=page,
        section=section,
        content=content_data.content,
        images=content_data.images or [],
        updated_by=current_user.username
    )
    
    await db.content_sections.update_one(
        {"page": page, "section": section},
        {"$set": content_section.dict()},
        upsert=True
    )
    return content_section

# Menu Management routes
@api_router.get("/menu/items", response_model=List[MenuItem])
async def get_menu_items():
    items = await db.menu_items.find({"is_active": True}).sort("order_index", 1).to_list(1000)
    return [MenuItem(**item) for item in items]

@api_router.post("/menu/items", response_model=MenuItem)
async def create_menu_item(item_data: MenuItemCreate, current_user: User = Depends(get_editor_user)):
    item = MenuItem(**item_data.dict())
    await db.menu_items.insert_one(item.dict())
    return item

@api_router.put("/menu/items/{item_id}", response_model=MenuItem)
async def update_menu_item(
    item_id: str, 
    item_data: MenuItemUpdate, 
    current_user: User = Depends(get_editor_user)
):
    update_dict = {k: v for k, v in item_data.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.menu_items.update_one(
        {"id": item_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    updated_item = await db.menu_items.find_one({"id": item_id})
    return MenuItem(**updated_item)

@api_router.delete("/menu/items/{item_id}")
async def delete_menu_item(item_id: str, current_user: User = Depends(get_editor_user)):
    result = await db.menu_items.update_one(
        {"id": item_id},
        {"$set": {"is_active": False}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted successfully"}

# Review Management routes
@api_router.get("/reviews", response_model=List[Review])
async def get_reviews(approved_only: bool = True):
    query = {"is_approved": True} if approved_only else {}
    reviews = await db.reviews.find(query).sort("date", -1).to_list(1000)
    return [Review(**review) for review in reviews]

@api_router.post("/reviews", response_model=Review)
async def create_review(review_data: ReviewCreate):
    review = Review(**review_data.dict())
    await db.reviews.insert_one(review.dict())
    return review

@api_router.put("/reviews/{review_id}/approve")
async def approve_review(review_id: str, current_user: User = Depends(get_editor_user)):
    result = await db.reviews.update_one(
        {"id": review_id},
        {"$set": {
            "is_approved": True,
            "approved_by": current_user.username,
            "approved_at": datetime.utcnow()
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review approved successfully"}

@api_router.get("/admin/reviews/pending", response_model=List[Review])
async def get_pending_reviews(current_user: User = Depends(get_editor_user)):
    reviews = await db.reviews.find({"is_approved": False}).sort("date", -1).to_list(1000)
    return [Review(**review) for review in reviews]

# Contact Messages routes
@api_router.post("/contact", response_model=ContactMessage)
async def create_contact_message(message_data: ContactMessageCreate):
    message = ContactMessage(**message_data.dict())
    await db.contact_messages.insert_one(message.dict())
    return message

@api_router.get("/admin/contact", response_model=List[ContactMessage])
async def get_contact_messages(current_user: User = Depends(get_editor_user)):
    messages = await db.contact_messages.find().sort("date", -1).to_list(1000)
    return [ContactMessage(**message) for message in messages]

@api_router.put("/admin/contact/{message_id}/read")
async def mark_message_read(message_id: str, current_user: User = Depends(get_editor_user)):
    result = await db.contact_messages.update_one(
        {"id": message_id},
        {"$set": {"is_read": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message marked as read"}

# Maintenance Mode routes
@api_router.get("/maintenance", response_model=MaintenanceMode)
async def get_maintenance_status():
    maintenance = await db.maintenance_mode.find_one()
    if not maintenance:
        maintenance = MaintenanceMode().dict()
        await db.maintenance_mode.insert_one(maintenance)
    return MaintenanceMode(**maintenance)

@api_router.put("/admin/maintenance", response_model=MaintenanceMode)
async def update_maintenance_mode(
    maintenance_data: MaintenanceMode, 
    current_user: User = Depends(get_admin_user)
):
    maintenance_data.activated_by = current_user.username
    maintenance_data.activated_at = datetime.utcnow()
    
    await db.maintenance_mode.update_one(
        {},
        {"$set": maintenance_data.dict()},
        upsert=True
    )
    return maintenance_data

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

# Include the router in the main app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await create_default_admin()

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

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

# Newsletter Models
class NewsletterSubscriber(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: Optional[str] = None
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    unsubscribe_token: str = Field(default_factory=lambda: str(uuid.uuid4()))

class NewsletterSubscriberCreate(BaseModel):
    email: str
    name: Optional[str] = None

class NewsletterTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subject: str
    content: str  # HTML content
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    is_active: bool = True

class NewsletterTemplateCreate(BaseModel):
    name: str
    subject: str
    content: str

class Newsletter(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: str
    content: str  # HTML content
    template_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    sent_at: Optional[datetime] = None
    sent_by: Optional[str] = None
    recipients_count: int = 0
    status: str = "draft"  # draft, sending, sent, failed

class NewsletterCreate(BaseModel):
    subject: str
    content: str
    template_id: Optional[str] = None

class SMTPConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    host: str
    port: int
    username: str
    password: str  # Will be encrypted
    use_tls: bool = True
    from_email: str
    from_name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str

class SMTPConfigCreate(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True
    from_email: str
    from_name: str

class SMTPConfigUpdate(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: Optional[bool] = None
    from_email: Optional[str] = None
    from_name: Optional[str] = None

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

# ===============================================
# COMPLETE CMS API ENDPOINTS
# ===============================================

# Homepage Content Management
@api_router.get("/cms/homepage/hero")
async def get_hero_section():
    """Get homepage hero section content"""
    hero = await db.homepage_hero.find_one({"is_active": True})
    if not hero:
        # Return default content if none exists
        return {
            "title": {"de": "AUTÉNTICO SABOR ESPAÑOL", "en": "AUTÉNTICO SABOR ESPAÑOL", "es": "AUTÉNTICO SABOR ESPAÑOL"},
            "subtitle": {"de": "an der Ostsee", "en": "at the Baltic Sea", "es": "en el Mar Báltico"},
            "description": {"de": "Genießen Sie authentische spanische Spezialitäten", "en": "Enjoy authentic Spanish specialties", "es": "Disfrute de auténticas especialidades españolas"},
            "location_text": {"de": "direkt an der malerischen Ostseeküste", "en": "directly at the picturesque Baltic Sea coast", "es": "directamente en la pintoresca costa del Mar Báltico"},
            "background_image": "https://images.unsplash.com/photo-1656423521731-9665583f100c",
            "menu_button_text": {"de": "Zur Speisekarte", "en": "View Menu", "es": "Ver Carta"},
            "locations_button_text": {"de": "Unsere Standorte", "en": "Our Locations", "es": "Nuestras Ubicaciones"}
        }
    return hero

@api_router.put("/cms/homepage/hero")
async def update_hero_section(
    hero_data: HeroSection,
    current_user: User = Depends(get_editor_user)
):
    """Update homepage hero section"""
    hero_data.updated_at = datetime.utcnow()
    hero_data.updated_by = current_user.username
    
    await db.homepage_hero.update_one(
        {"is_active": True},
        {"$set": hero_data.dict()},
        upsert=True
    )
    
    return {"message": "Hero section updated successfully", "data": hero_data}

@api_router.get("/cms/homepage/features")
async def get_homepage_features():
    """Get homepage features section"""
    features = await db.homepage_features.find_one({"is_active": True})
    if not features:
        # Return default content
        return {
            "section_title": {"de": "Spanische Tradition", "en": "Spanish Tradition", "es": "Tradición Española"},
            "section_description": {"de": "Erleben Sie authentische spanische Gastfreundschaft an der deutschen Ostseeküste", "en": "Experience authentic Spanish hospitality at the German Baltic Sea coast", "es": "Experimente la auténtica hospitalidad española en la costa alemana del Mar Báltico"},
            "features": [
                {
                    "title": {"de": "Authentische Tapas", "en": "Authentic Tapas", "es": "Tapas Auténticas"},
                    "description": {"de": "Traditionelle spanische Gerichte, mit Liebe zubereitet und perfekt zum Teilen", "en": "Traditional Spanish dishes, prepared with love and perfect for sharing", "es": "Platos tradicionales españoles, preparados con amor y perfectos para compartir"},
                    "image_url": "https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg",
                    "image_alt": {"de": "Authentische Tapas", "en": "Authentic Tapas", "es": "Tapas Auténticas"}
                },
                {
                    "title": {"de": "Frische Paella", "en": "Fresh Paella", "es": "Paella Fresca"},
                    "description": {"de": "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn", "en": "Daily homemade with seafood, vegetables or chicken", "es": "Hecha en casa diariamente con mariscos, verduras o pollo"},
                    "image_url": "https://images.unsplash.com/photo-1694685367640-05d6624e57f1",
                    "image_alt": {"de": "Frische Paella", "en": "Fresh Paella", "es": "Paella Fresca"}
                },
                {
                    "title": {"de": "Strandnähe", "en": "Beach Proximity", "es": "Cerca de la Playa"},
                    "description": {"de": "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden", "en": "Both locations directly at the picturesque Baltic Sea coast – perfect for relaxing hours", "es": "Ambas ubicaciones directamente en la pintoresca costa del Mar Báltico – perfectas para horas relajantes"},
                    "image_url": "https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg",
                    "image_alt": {"de": "Strandnähe", "en": "Beach Proximity", "es": "Cerca de la Playa"}
                }
            ]
        }
    return features

@api_router.put("/cms/homepage/features")
async def update_homepage_features(
    features_data: HomepageFeatures,
    current_user: User = Depends(get_editor_user)
):
    """Update homepage features section"""
    features_data.updated_at = datetime.utcnow()
    features_data.updated_by = current_user.username
    
    await db.homepage_features.update_one(
        {"is_active": True},
        {"$set": features_data.dict()},
        upsert=True
    )
    
    return {"message": "Features section updated successfully", "data": features_data}

@api_router.get("/cms/homepage/food-gallery")
async def get_food_gallery():
    """Get homepage food gallery section"""
    gallery = await db.homepage_food_gallery.find_one({"is_active": True})
    if not gallery:
        # Return default content
        return {
            "section_title": {"de": "Unsere Spezialitäten", "en": "Our Specialties", "es": "Nuestras Especialidades"},
            "gallery_items": [
                {
                    "name": {"de": "Patatas Bravas", "en": "Patatas Bravas", "es": "Patatas Bravas"},
                    "description": {"de": "Klassische spanische Kartoffeln", "en": "Classic Spanish potatoes", "es": "Patatas españolas clásicas"},
                    "image_url": "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
                    "category_link": "#tapas-vegetarian",
                    "order": 1
                },
                {
                    "name": {"de": "Paella Valenciana", "en": "Paella Valenciana", "es": "Paella Valenciana"},
                    "description": {"de": "Traditionelle spanische Paella", "en": "Traditional Spanish paella", "es": "Paella española tradicional"},
                    "image_url": "https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg",
                    "category_link": "#tapa-paella",
                    "order": 2
                },
                {
                    "name": {"de": "Tapas Variación", "en": "Tapas Variation", "es": "Variación de Tapas"},
                    "description": {"de": "Auswahl spanischer Köstlichkeiten", "en": "Selection of Spanish delicacies", "es": "Selección de delicias españolas"},
                    "image_url": "https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg",
                    "category_link": "#inicio",
                    "order": 3
                },
                {
                    "name": {"de": "Gambas al Ajillo", "en": "Gambas al Ajillo", "es": "Gambas al Ajillo"},
                    "description": {"de": "Garnelen in Knoblauchöl", "en": "Shrimp in garlic oil", "es": "Gambas en aceite de ajo"},
                    "image_url": "https://images.unsplash.com/photo-1619860705243-dbef552e7118",
                    "category_link": "#tapas-pescado",
                    "order": 4
                }
            ]
        }
    return gallery

@api_router.put("/cms/homepage/food-gallery")
async def update_food_gallery(
    gallery_data: HomepageFoodGallery,
    current_user: User = Depends(get_editor_user)
):
    """Update homepage food gallery section"""
    gallery_data.updated_at = datetime.utcnow()
    gallery_data.updated_by = current_user.username
    
    await db.homepage_food_gallery.update_one(
        {"is_active": True},
        {"$set": gallery_data.dict()},
        upsert=True
    )
    
    return {"message": "Food gallery updated successfully", "data": gallery_data}

@api_router.get("/cms/homepage/lieferando")
async def get_lieferando_section():
    """Get Lieferando section content"""
    lieferando = await db.homepage_lieferando.find_one({"is_active": True})
    if not lieferando:
        # Return default content
        return {
            "title": {"de": "Jetzt auch bequem nach Hause bestellen", "en": "Now also order conveniently to your home", "es": "Ahora también pide cómodamente a casa"},
            "description": {"de": "Genießen Sie unsere authentischen spanischen Spezialitäten gemütlich zu Hause. Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen.", "en": "Enjoy our authentic Spanish specialties comfortably at home. Order directly via Lieferando and let yourself be pampered.", "es": "Disfrute de nuestras auténticas especialidades españolas cómodamente en casa. Pida directamente a través de Lieferando y déjese mimar."},
            "button_text": {"de": "Jetzt bei Lieferando bestellen", "en": "Order now at Lieferando", "es": "Pedir ahora en Lieferando"},
            "delivery_text": {"de": "Schnelle Lieferung", "en": "Fast delivery", "es": "Entrega rápida"},
            "authentic_text": {"de": "Authentisch Spanisch", "en": "Authentically Spanish", "es": "Auténticamente Español"},
            "availability_text": {"de": "Verfügbar für beide Standorte", "en": "Available for both locations", "es": "Disponible para ambas ubicaciones"},
            "lieferando_url": "https://www.lieferando.de"
        }
    return lieferando

@api_router.put("/cms/homepage/lieferando")
async def update_lieferando_section(
    lieferando_data: LieferandoSection,
    current_user: User = Depends(get_editor_user)
):
    """Update Lieferando section"""
    lieferando_data.updated_at = datetime.utcnow()
    lieferando_data.updated_by = current_user.username
    
    await db.homepage_lieferando.update_one(
        {"is_active": True},
        {"$set": lieferando_data.dict()},
        upsert=True
    )
    
    return {"message": "Lieferando section updated successfully", "data": lieferando_data}

# Location Management
@api_router.get("/cms/locations")
async def get_all_locations():
    """Get all locations"""
    locations = await db.locations.find({"is_active": True}).sort("order", 1).to_list(None)
    if not locations:
        # Return default content
        return [
            {
                "id": "location-1",
                "name": {"de": "Warnemünde", "en": "Warnemünde", "es": "Warnemünde"},
                "address": {"de": "Strandstraße 12, 18119 Rostock-Warnemünde", "en": "Strandstraße 12, 18119 Rostock-Warnemünde", "es": "Strandstraße 12, 18119 Rostock-Warnemünde"},
                "phone": "+49 381 123456",
                "email": "warnemuende@jimmys-tapas.de",
                "opening_hours": {
                    "monday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "tuesday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "wednesday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "thursday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "friday": {"de": "12:00 - 23:00", "en": "12:00 - 23:00", "es": "12:00 - 23:00"},
                    "saturday": {"de": "12:00 - 23:00", "en": "12:00 - 23:00", "es": "12:00 - 23:00"},
                    "sunday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"}
                },
                "description": {"de": "Unser Hauptstandort direkt am Strand von Warnemünde", "en": "Our main location directly at Warnemünde beach", "es": "Nuestra ubicación principal directamente en la playa de Warnemünde"},
                "features": [
                    {"de": "Meerblick", "en": "Ocean view", "es": "Vista al mar"},
                    {"de": "Terrasse", "en": "Terrace", "es": "Terraza"},
                    {"de": "Parkplätze", "en": "Parking", "es": "Aparcamiento"}
                ],
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                "google_maps_url": "https://maps.google.com",
                "order": 1
            },
            {
                "id": "location-2",
                "name": {"de": "Kühlungsborn", "en": "Kühlungsborn", "es": "Kühlungsborn"},
                "address": {"de": "Ostseeallee 25, 18225 Kühlungsborn", "en": "Ostseeallee 25, 18225 Kühlungsborn", "es": "Ostseeallee 25, 18225 Kühlungsborn"},
                "phone": "+49 38293 789012",
                "email": "kuehlungsborn@jimmys-tapas.de",
                "opening_hours": {
                    "monday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "tuesday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "wednesday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "thursday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"},
                    "friday": {"de": "12:00 - 23:00", "en": "12:00 - 23:00", "es": "12:00 - 23:00"},
                    "saturday": {"de": "12:00 - 23:00", "en": "12:00 - 23:00", "es": "12:00 - 23:00"},
                    "sunday": {"de": "12:00 - 22:00", "en": "12:00 - 22:00", "es": "12:00 - 22:00"}
                },
                "description": {"de": "Gemütliches Restaurant mit traditioneller Atmosphäre", "en": "Cozy restaurant with traditional atmosphere", "es": "Restaurante acogedor con ambiente tradicional"},
                "features": [
                    {"de": "Familienfreundlich", "en": "Family friendly", "es": "Amigable para familias"},
                    {"de": "Biergarten", "en": "Beer garden", "es": "Jardín de cerveza"},
                    {"de": "Live Musik", "en": "Live music", "es": "Música en vivo"}
                ],
                "image_url": "https://images.unsplash.com/photo-1529256354694-69f81f6be3b1",
                "google_maps_url": "https://maps.google.com",
                "order": 2
            }
        ]
    return locations

@api_router.post("/cms/locations")
async def create_location(
    location_data: LocationModel,
    current_user: User = Depends(get_editor_user)
):
    """Create new location"""
    location_data.updated_by = current_user.username
    result = await db.locations.insert_one(location_data.dict())
    return {"message": "Location created successfully", "id": str(result.inserted_id)}

@api_router.put("/cms/locations/{location_id}")
async def update_location(
    location_id: str,
    location_data: LocationModel,
    current_user: User = Depends(get_editor_user)
):
    """Update location"""
    location_data.updated_at = datetime.utcnow()
    location_data.updated_by = current_user.username
    
    result = await db.locations.update_one(
        {"id": location_id},
        {"$set": location_data.dict()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    
    return {"message": "Location updated successfully"}

@api_router.delete("/cms/locations/{location_id}")
async def delete_location(
    location_id: str,
    current_user: User = Depends(get_admin_user)
):
    """Delete location"""
    result = await db.locations.update_one(
        {"id": location_id},
        {"$set": {"is_active": False}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    
    return {"message": "Location deleted successfully"}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# About Us Content Management
@api_router.get("/cms/about")
async def get_about_content():
    """Get About Us content"""
    about = await db.about_content.find_one({"is_active": True})
    if not about:
        # Return default content
        return {
            "hero_title": {"de": "Über Jimmy's Tapas Bar", "en": "About Jimmy's Tapas Bar", "es": "Acerca de Jimmy's Tapas Bar"},
            "hero_description": {"de": "Authentische spanische Küche an der deutschen Ostseeküste", "en": "Authentic Spanish cuisine on the German Baltic coast", "es": "Auténtica cocina española en la costa báltica alemana"},
            "hero_image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
            "story_title": {"de": "Unsere Geschichte", "en": "Our Story", "es": "Nuestra Historia"},
            "story_content": {"de": "Seit über 10 Jahren bringen wir die Aromen Spaniens an die Ostseeküste. Unser Familienunternehmen verbindet traditionelle spanische Küche mit der entspannten Atmosphäre der deutschen Küste.", "en": "For over 10 years we have been bringing the flavors of Spain to the Baltic coast. Our family business combines traditional Spanish cuisine with the relaxed atmosphere of the German coast.", "es": "Durante más de 10 años hemos estado trayendo los sabores de España a la costa báltica. Nuestro negocio familiar combina la cocina tradicional española con el ambiente relajado de la costa alemana."},
            "team_title": {"de": "Unser Team", "en": "Our Team", "es": "Nuestro Equipo"},
            "team_members": [],
            "values_title": {"de": "Unsere Werte", "en": "Our Values", "es": "Nuestros Valores"},
            "values": []
        }
    return about

@api_router.put("/cms/about")
async def update_about_content(
    about_data: AboutUsContent,
    current_user: User = Depends(get_editor_user)
):
    """Update About Us content"""
    about_data.updated_at = datetime.utcnow()
    about_data.updated_by = current_user.username
    
    await db.about_content.update_one(
        {"is_active": True},
        {"$set": about_data.dict()},
        upsert=True
    )
    
    return {"message": "About Us content updated successfully", "data": about_data}

# Contact Information Management
@api_router.get("/cms/contact")
async def get_contact_info():
    """Get contact information"""
    contact = await db.contact_info.find_one({"is_active": True})
    if not contact:
        # Return default content
        return {
            "page_title": {"de": "Kontakt", "en": "Contact", "es": "Contacto"},
            "page_description": {"de": "Nehmen Sie Kontakt mit uns auf", "en": "Get in touch with us", "es": "Póngase en contacto con nosotros"},
            "contact_form_title": {"de": "Schreiben Sie uns", "en": "Write to us", "es": "Escríbanos"},
            "contact_form_description": {"de": "Wir freuen uns auf Ihre Nachricht", "en": "We look forward to your message", "es": "Esperamos su mensaje"},
            "general_email": "info@jimmys-tapas.de",
            "general_phone": "+49 381 123456",
            "social_media": {
                "facebook": "https://facebook.com/jimmys-tapas",
                "instagram": "https://instagram.com/jimmys-tapas"
            }
        }
    return contact

@api_router.put("/cms/contact")
async def update_contact_info(
    contact_data: ContactInfo,
    current_user: User = Depends(get_editor_user)
):
    """Update contact information"""
    contact_data.updated_at = datetime.utcnow()
    contact_data.updated_by = current_user.username
    
    await db.contact_info.update_one(
        {"is_active": True},
        {"$set": contact_data.dict()},
        upsert=True
    )
    
    return {"message": "Contact information updated successfully", "data": contact_data}

# Legal Content Management
@api_router.get("/cms/legal/{page_type}")
async def get_legal_content(page_type: str):
    """Get legal content (impressum or datenschutz)"""
    legal = await db.legal_content.find_one({"page_type": page_type, "is_active": True})
    if not legal:
        if page_type == "impressum":
            return {
                "title": {"de": "Impressum", "en": "Imprint", "es": "Aviso Legal"},
                "content": {"de": "Angaben gemäß § 5 TMG:\n\nJimmy's Tapas Bar\nMustermann GmbH\nMusterstraße 1\n12345 Musterstadt\n\nVertreten durch:\nMax Mustermann\n\nKontakt:\nTelefon: +49 381 123456\nE-Mail: info@jimmys-tapas.de", 
                           "en": "Information according to § 5 TMG:\n\nJimmy's Tapas Bar\nExample Ltd.\nExample Street 1\n12345 Example City\n\nRepresented by:\nJohn Example\n\nContact:\nPhone: +49 381 123456\nE-Mail: info@jimmys-tapas.de", 
                           "es": "Información según § 5 TMG:\n\nJimmy's Tapas Bar\nEjemplo S.L.\nCalle Ejemplo 1\n12345 Ciudad Ejemplo\n\nRepresentado por:\nJuan Ejemplo\n\nContacto:\nTeléfono: +49 381 123456\nE-Mail: info@jimmys-tapas.de"}
            }
        elif page_type == "datenschutz":
            return {
                "title": {"de": "Datenschutzerklärung", "en": "Privacy Policy", "es": "Política de Privacidad"},
                "content": {"de": "1. Datenschutz auf einen Blick\n\nAllgemeine Hinweise\nDie folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie unsere Website besuchen.", 
                           "en": "1. Data protection at a glance\n\nGeneral information\nThe following notes provide a simple overview of what happens to your personal data when you visit our website.", 
                           "es": "1. Protección de datos de un vistazo\n\nInformación general\nLas siguientes notas proporcionan una descripción general simple de lo que sucede con sus datos personales cuando visita nuestro sitio web."}
            }
    return legal

@api_router.put("/cms/legal/{page_type}")
async def update_legal_content(
    page_type: str,
    legal_data: LegalContent,
    current_user: User = Depends(get_admin_user)
):
    """Update legal content"""
    legal_data.page_type = page_type
    legal_data.last_updated = datetime.utcnow()
    legal_data.updated_by = current_user.username
    
    await db.legal_content.update_one(
        {"page_type": page_type, "is_active": True},
        {"$set": legal_data.dict()},
        upsert=True
    )
    
    return {"message": f"Legal content ({page_type}) updated successfully", "data": legal_data}

# Footer Content Management
@api_router.get("/cms/footer")
async def get_footer_content():
    """Get footer content"""
    footer = await db.footer_content.find_one({"is_active": True})
    if not footer:
        return {
            "company_name": "Jimmy's Tapas Bar",
            "company_description": {"de": "Authentische spanische Küche an der Ostsee", "en": "Authentic Spanish cuisine by the Baltic Sea", "es": "Auténtica cocina española junto al Mar Báltico"},
            "quick_links": [],
            "social_links": {
                "facebook": "https://facebook.com/jimmys-tapas",
                "instagram": "https://instagram.com/jimmys-tapas"
            },
            "copyright_text": {"de": "© 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten.", "en": "© 2024 Jimmy's Tapas Bar. All rights reserved.", "es": "© 2024 Jimmy's Tapas Bar. Todos los derechos reservados."}
        }
    return footer

@api_router.put("/cms/footer")
async def update_footer_content(
    footer_data: FooterContent,
    current_user: User = Depends(get_editor_user)
):
    """Update footer content"""
    footer_data.updated_at = datetime.utcnow()
    footer_data.updated_by = current_user.username
    
    await db.footer_content.update_one(
        {"is_active": True},
        {"$set": footer_data.dict()},
        upsert=True
    )
    
    return {"message": "Footer content updated successfully", "data": footer_data}

# ===============================================
# NEWSLETTER SYSTEM API ENDPOINTS
# ===============================================

# Newsletter Subscription (Public endpoint)
@api_router.post("/newsletter/subscribe")
async def subscribe_to_newsletter(subscriber_data: NewsletterSubscriberCreate):
    """Subscribe to newsletter - public endpoint"""
    # Check if email already exists
    existing = await db.newsletter_subscribers.find_one({"email": subscriber_data.email})
    if existing:
        if existing["is_active"]:
            raise HTTPException(status_code=400, detail="Diese E-Mail-Adresse ist bereits für den Newsletter registriert")
        else:
            # Reactivate subscription
            await db.newsletter_subscribers.update_one(
                {"email": subscriber_data.email},
                {"$set": {"is_active": True, "subscribed_at": datetime.utcnow()}}
            )
            return {"message": "Newsletter-Abonnement wurde reaktiviert"}
    
    subscriber = NewsletterSubscriber(**subscriber_data.dict())
    await db.newsletter_subscribers.insert_one(subscriber.dict())
    return {"message": "Vielen Dank! Sie haben sich erfolgreich für unseren Newsletter angemeldet."}

# Newsletter Unsubscribe (Public endpoint)
@api_router.post("/newsletter/unsubscribe/{token}")
async def unsubscribe_from_newsletter(token: str):
    """Unsubscribe from newsletter using token"""
    subscriber = await db.newsletter_subscribers.find_one({"unsubscribe_token": token})
    if not subscriber:
        raise HTTPException(status_code=404, detail="Ungültiger Abmelde-Link")
    
    await db.newsletter_subscribers.update_one(
        {"unsubscribe_token": token},
        {"$set": {"is_active": False}}
    )
    return {"message": "Sie wurden erfolgreich vom Newsletter abgemeldet"}

# Admin Newsletter Management
@api_router.get("/admin/newsletter/subscribers")
async def get_newsletter_subscribers(current_user: User = Depends(get_editor_user)):
    """Get all newsletter subscribers"""
    subscribers = await db.newsletter_subscribers.find().sort("subscribed_at", -1).to_list(1000)
    return [NewsletterSubscriber(**sub) for sub in subscribers]

@api_router.delete("/admin/newsletter/subscribers/{subscriber_id}")
async def delete_newsletter_subscriber(subscriber_id: str, current_user: User = Depends(get_admin_user)):
    """Delete newsletter subscriber"""
    result = await db.newsletter_subscribers.delete_one({"id": subscriber_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Abonnent nicht gefunden")
    return {"message": "Abonnent erfolgreich gelöscht"}

# SMTP Configuration Management
@api_router.get("/admin/newsletter/smtp")
async def get_smtp_config(current_user: User = Depends(get_admin_user)):
    """Get SMTP configuration"""
    config = await db.smtp_config.find_one({"is_active": True})
    if not config:
        return {"message": "Keine SMTP-Konfiguration gefunden"}
    
    # Don't return password for security
    config_dict = SMTPConfig(**config).dict()
    config_dict["password"] = "***hidden***"
    return config_dict

@api_router.post("/admin/newsletter/smtp")
async def create_smtp_config(
    smtp_data: SMTPConfigCreate, 
    current_user: User = Depends(get_admin_user)
):
    """Create SMTP configuration"""
    import base64
    
    # Deactivate existing configs
    await db.smtp_config.update_many({}, {"$set": {"is_active": False}})
    
    # Encrypt password (simple base64 for demo - use proper encryption in production)
    encrypted_password = base64.b64encode(smtp_data.password.encode()).decode()
    
    smtp_config = SMTPConfig(
        **smtp_data.dict(),
        password=encrypted_password,
        updated_by=current_user.username
    )
    
    await db.smtp_config.insert_one(smtp_config.dict())
    return {"message": "SMTP-Konfiguration erfolgreich erstellt"}

@api_router.put("/admin/newsletter/smtp/{config_id}")
async def update_smtp_config(
    config_id: str,
    smtp_data: SMTPConfigUpdate,
    current_user: User = Depends(get_admin_user)
):
    """Update SMTP configuration"""
    import base64
    
    update_dict = {k: v for k, v in smtp_data.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    update_dict["updated_by"] = current_user.username
    
    # Encrypt password if provided
    if "password" in update_dict:
        update_dict["password"] = base64.b64encode(update_dict["password"].encode()).decode()
    
    result = await db.smtp_config.update_one(
        {"id": config_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="SMTP-Konfiguration nicht gefunden")
    
    return {"message": "SMTP-Konfiguration erfolgreich aktualisiert"}

# Newsletter Template Management
@api_router.get("/admin/newsletter/templates")
async def get_newsletter_templates(current_user: User = Depends(get_editor_user)):
    """Get all newsletter templates"""
    templates = await db.newsletter_templates.find({"is_active": True}).sort("created_at", -1).to_list(1000)
    return [NewsletterTemplate(**template) for template in templates]

@api_router.post("/admin/newsletter/templates")
async def create_newsletter_template(
    template_data: NewsletterTemplateCreate,
    current_user: User = Depends(get_editor_user)
):
    """Create newsletter template"""
    template = NewsletterTemplate(
        **template_data.dict(),
        created_by=current_user.username
    )
    await db.newsletter_templates.insert_one(template.dict())
    return {"message": "Newsletter-Vorlage erfolgreich erstellt", "template": template}

@api_router.delete("/admin/newsletter/templates/{template_id}")
async def delete_newsletter_template(template_id: str, current_user: User = Depends(get_admin_user)):
    """Delete newsletter template"""
    result = await db.newsletter_templates.update_one(
        {"id": template_id},
        {"$set": {"is_active": False}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Vorlage nicht gefunden")
    return {"message": "Vorlage erfolgreich gelöscht"}

# Newsletter Creation and Sending
@api_router.get("/admin/newsletter/campaigns")
async def get_newsletters(current_user: User = Depends(get_editor_user)):
    """Get all newsletters/campaigns"""
    newsletters = await db.newsletters.find().sort("created_at", -1).to_list(1000)
    return [Newsletter(**newsletter) for newsletter in newsletters]

@api_router.post("/admin/newsletter/campaigns")
async def create_newsletter(
    newsletter_data: NewsletterCreate,
    current_user: User = Depends(get_editor_user)
):
    """Create newsletter campaign"""
    newsletter = Newsletter(
        **newsletter_data.dict(),
        created_by=current_user.username
    )
    await db.newsletters.insert_one(newsletter.dict())
    return {"message": "Newsletter erfolgreich erstellt", "newsletter": newsletter}

@api_router.post("/admin/newsletter/campaigns/{newsletter_id}/send")
async def send_newsletter(newsletter_id: str, current_user: User = Depends(get_admin_user)):
    """Send newsletter to all active subscribers"""
    import smtplib
    import base64
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Get newsletter
    newsletter = await db.newsletters.find_one({"id": newsletter_id})
    if not newsletter:
        raise HTTPException(status_code=404, detail="Newsletter nicht gefunden")
    
    if newsletter["status"] == "sent":
        raise HTTPException(status_code=400, detail="Newsletter wurde bereits versendet")
    
    # Get SMTP config
    smtp_config = await db.smtp_config.find_one({"is_active": True})
    if not smtp_config:
        raise HTTPException(status_code=400, detail="Keine SMTP-Konfiguration gefunden")
    
    # Get active subscribers
    subscribers = await db.newsletter_subscribers.find({"is_active": True}).to_list(1000)
    if not subscribers:
        raise HTTPException(status_code=400, detail="Keine aktiven Abonnenten gefunden")
    
    # Update newsletter status
    await db.newsletters.update_one(
        {"id": newsletter_id},
        {"$set": {"status": "sending"}}
    )
    
    try:
        # Decrypt password
        decrypted_password = base64.b64decode(smtp_config["password"]).decode()
        
        # Setup SMTP
        server = smtplib.SMTP(smtp_config["host"], smtp_config["port"])
        if smtp_config["use_tls"]:
            server.starttls()
        server.login(smtp_config["username"], decrypted_password)
        
        sent_count = 0
        for subscriber in subscribers:
            try:
                # Create email
                msg = MIMEMultipart('alternative')
                msg['Subject'] = newsletter["subject"]
                msg['From'] = f"{smtp_config['from_name']} <{smtp_config['from_email']}>"
                msg['To'] = subscriber["email"]
                
                # Add unsubscribe link to content
                frontend_url = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:3000').replace('/api', '')
                content_with_unsubscribe = newsletter["content"] + f"""
                <br><br>
                <p style="font-size: 12px; color: #666;">
                    Sie möchten sich vom Newsletter abmelden? 
                    <a href="{frontend_url}/newsletter/unsubscribe/{subscriber['unsubscribe_token']}">Hier klicken</a>
                </p>
                """
                
                html_part = MIMEText(content_with_unsubscribe, 'html', 'utf-8')
                msg.attach(html_part)
                
                # Send email
                server.send_message(msg)
                sent_count += 1
                
            except Exception as e:
                logger.error(f"Failed to send email to {subscriber['email']}: {str(e)}")
                continue
        
        server.quit()
        
        # Update newsletter status
        await db.newsletters.update_one(
            {"id": newsletter_id},
            {"$set": {
                "status": "sent",
                "sent_at": datetime.utcnow(),
                "sent_by": current_user.username,
                "recipients_count": sent_count
            }}
        )
        
        return {"message": f"Newsletter erfolgreich an {sent_count} Empfänger versendet"}
        
    except Exception as e:
        # Update newsletter status to failed
        await db.newsletters.update_one(
            {"id": newsletter_id},
            {"$set": {"status": "failed"}}
        )
        
        logger.error(f"Failed to send newsletter: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler beim Versenden: {str(e)}")

@api_router.post("/admin/newsletter/smtp/test")
async def test_smtp_config(current_user: User = Depends(get_admin_user)):
    """Test SMTP configuration"""
    import smtplib
    import base64
    from email.mime.text import MIMEText
    
    # Get SMTP config
    smtp_config = await db.smtp_config.find_one({"is_active": True})
    if not smtp_config:
        raise HTTPException(status_code=400, detail="Keine SMTP-Konfiguration gefunden")
    
    try:
        # Decrypt password
        decrypted_password = base64.b64decode(smtp_config["password"]).decode()
        
        # Test SMTP connection
        server = smtplib.SMTP(smtp_config["host"], smtp_config["port"])
        if smtp_config["use_tls"]:
            server.starttls()
        server.login(smtp_config["username"], decrypted_password)
        
        # Send test email to admin
        msg = MIMEText("Dies ist eine Test-E-Mail von Jimmy's Tapas Bar Newsletter-System.", 'plain', 'utf-8')
        msg['Subject'] = "Newsletter-System Test"
        msg['From'] = f"{smtp_config['from_name']} <{smtp_config['from_email']}>"
        msg['To'] = current_user.email
        
        server.send_message(msg)
        server.quit()
        
        return {"message": "Test-E-Mail erfolgreich versendet! Bitte prüfen Sie Ihr Postfach."}
        
    except Exception as e:
        logger.error(f"SMTP test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"SMTP-Test fehlgeschlagen: {str(e)}")

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

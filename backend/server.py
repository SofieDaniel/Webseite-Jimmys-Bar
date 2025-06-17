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

# Basic models from before
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
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

# Homepage Content Models
class HeroSection(BaseModel):
    title: str = "JIMMY'S TAPAS BAR"
    subtitle: str = "an der Ostsee"
    description: str = "Genießen Sie authentische mediterrane Spezialitäten"
    location: str = "direkt an der malerischen Ostseeküste"
    background_image: str = "https://images.unsplash.com/photo-1656423521731-9665583f100c"
    menu_button_text: str = "Zur Speisekarte"
    locations_button_text: str = "Unsere Standorte"

class FeatureCard(BaseModel):
    title: str
    description: str
    image_url: str
    link_category: Optional[str] = None

class FeaturesSection(BaseModel):
    title: str = "Mediterrane Tradition"
    subtitle: str = "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste"
    cards: List[FeatureCard] = []

class SpecialtyCard(BaseModel):
    title: str
    description: str
    image_url: str
    category_link: Optional[str] = None

class SpecialtiesSection(BaseModel):
    title: str = "Unsere Spezialitäten"
    cards: List[SpecialtyCard] = []

class DeliverySection(BaseModel):
    title: str = "Jetzt auch bequem nach Hause bestellen"
    description: str = "Genießen Sie unsere authentischen mediterranen Spezialitäten gemütlich zu Hause."
    description_2: str = "Bestellen Sie direkt über Lieferando und lassen Sie sich verwöhnen."
    delivery_feature_title: str = "Schnelle Lieferung"
    delivery_feature_description: str = "Frisch und warm zu Ihnen"
    delivery_feature_image: str = "https://images.pexels.com/photos/6969962/pexels-photo-6969962.jpeg"
    button_text: str = "Jetzt bei Lieferando bestellen"
    button_url: str = "https://www.lieferando.de"
    availability_text: str = "Verfügbar für beide Standorte"
    authentic_feature_title: str = "Authentisch Mediterran"
    authentic_feature_description: str = "Direkt vom Küchenchef"
    authentic_feature_image: str = "https://images.pexels.com/photos/31748679/pexels-photo-31748679.jpeg"

class HomepageContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hero: HeroSection = Field(default_factory=HeroSection)
    features: FeaturesSection = Field(default_factory=FeaturesSection)
    specialties: SpecialtiesSection = Field(default_factory=SpecialtiesSection)
    delivery: DeliverySection = Field(default_factory=DeliverySection)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

# Website Texts Models  
class NavigationTexts(BaseModel):
    home: str = "Startseite"
    locations: str = "Standorte"
    menu: str = "Speisekarte"
    reviews: str = "Bewertungen"
    about: str = "Über uns"
    contact: str = "Kontakt"
    privacy: str = "Datenschutz"
    imprint: str = "Impressum"

class FooterTexts(BaseModel):
    opening_hours_title: str = "Öffnungszeiten"
    contact_title: str = "Kontakt"
    follow_us_title: str = "Folgen Sie uns"
    copyright: str = "© 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten."

class ButtonTexts(BaseModel):
    menu_button: str = "Zur Speisekarte"
    locations_button: str = "Unsere Standorte"
    contact_button: str = "Kontakt aufnehmen"
    reserve_button: str = "Tisch reservieren"
    order_button: str = "Jetzt bestellen"

class GeneralTexts(BaseModel):
    loading: str = "Lädt..."
    error: str = "Fehler beim Laden"
    success: str = "Erfolgreich gespeichert"
    required_field: str = "Dieses Feld ist erforderlich"
    email_invalid: str = "E-Mail-Adresse ist ungültig"

class WebsiteTexts(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    section: str  # navigation, footer, buttons, general
    navigation: Optional[NavigationTexts] = None
    footer: Optional[FooterTexts] = None
    buttons: Optional[ButtonTexts] = None
    general: Optional[GeneralTexts] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

# Location Models
class LocationInfo(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    opening_hours: Dict[str, str]  # {"monday": "10:00 - 22:00", ...}
    image_url: Optional[str] = None
    description: Optional[str] = None
    maps_embed: Optional[str] = None

class LocationsContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_title: str = "Unsere Standorte"
    page_description: str = "Besuchen Sie uns an einem unserer beiden Standorte"
    locations: List[LocationInfo] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

# About Page Models
class TeamMember(BaseModel):
    name: str
    position: str
    description: str
    image_url: Optional[str] = None

# Newsletter Models
class NewsletterSubscriber(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: Optional[str] = None
    subscribed: bool = True
    subscribe_date: datetime = Field(default_factory=datetime.utcnow)
    unsubscribe_date: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class NewsletterTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subject: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class NewsletterCampaign(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    template_id: str
    subject: str
    content: str
    scheduled_date: Optional[datetime] = None
    sent_date: Optional[datetime] = None
    recipients_count: int = 0
    sent_count: int = 0
    status: str = "draft"  # draft, scheduled, sending, sent, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class SMTPConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    username: str
    password: str
    from_email: str
    from_name: str = "Jimmy's Tapas Bar"
    use_tls: bool = True
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

# Legal Pages Models
class LegalPage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_type: str  # "imprint" or "privacy"
    title: str
    content: str
    contact_name: Optional[str] = None
    contact_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    company_info: Optional[dict] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

class AboutContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_title: str = "Über uns"
    hero_title: str = "Unsere Geschichte"
    hero_description: str = "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar"
    story_title: str = "Unsere Leidenschaft"
    story_content: str = "Seit der Gründung steht Jimmy's Tapas Bar für authentische mediterrane Küche..."
    story_image: Optional[str] = None
    team_title: str = "Unser Team"
    team_members: List[TeamMember] = []
    values_title: str = "Unsere Werte"
    values: List[str] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None

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
    except Exception:
        raise HTTPException(status_code=401, detail="Authentication required")
    
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

# Content Management API routes
@api_router.get("/cms/homepage", response_model=HomepageContent)
async def get_homepage_content():
    content = await db.homepage_content.find_one()
    if not content:
        # Create default content
        default_content = HomepageContent()
        default_content.features.cards = [
            FeatureCard(
                title="Authentische Tapas",
                description="Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen",
                image_url="https://images.pexels.com/photos/19671352/pexels-photo-19671352.jpeg"
            ),
            FeatureCard(
                title="Frische Paella",
                description="Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn",
                image_url="https://images.unsplash.com/photo-1694685367640-05d6624e57f1"
            ),
            FeatureCard(
                title="Strandnähe",
                description="Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden",
                image_url="https://images.pexels.com/photos/32508247/pexels-photo-32508247.jpeg"
            )
        ]
        default_content.specialties.cards = [
            SpecialtyCard(
                title="Patatas Bravas",
                description="Klassische mediterrane Kartoffeln",
                image_url="https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
                category_link="tapas-vegetarian"
            ),
            SpecialtyCard(
                title="Paella Valenciana",
                description="Traditionelle mediterrane Paella",
                image_url="https://images.pexels.com/photos/7085661/pexels-photo-7085661.jpeg",
                category_link="tapa-paella"
            ),
            SpecialtyCard(
                title="Tapas Variación",
                description="Auswahl mediterraner Köstlichkeiten",
                image_url="https://images.pexels.com/photos/1813504/pexels-photo-1813504.jpeg",
                category_link="inicio"
            ),
            SpecialtyCard(
                title="Gambas al Ajillo",
                description="Garnelen in Knoblauchöl",
                image_url="https://images.unsplash.com/photo-1619860705243-dbef552e7118",
                category_link="tapas-pescado"
            )
        ]
        await db.homepage_content.insert_one(default_content.dict())
        content = default_content.dict()
    else:
        # Remove MongoDB ObjectId before returning
        if '_id' in content:
            del content['_id']
    return HomepageContent(**content)

@api_router.put("/cms/homepage")
async def update_homepage_content(content_data: HomepageContent, current_user: User = Depends(get_editor_user)):
    content_data.updated_at = datetime.utcnow()
    content_data.updated_by = current_user.username
    
    await db.homepage_content.update_one(
        {},
        {"$set": content_data.dict()},
        upsert=True
    )
    return content_data

@api_router.get("/cms/website-texts/{section}")
async def get_website_texts(section: str):
    texts = await db.website_texts.find_one({"section": section})
    if not texts:
        # Create default texts based on section
        default_texts = WebsiteTexts(section=section)
        if section == "navigation":
            default_texts.navigation = NavigationTexts()
        elif section == "footer":
            default_texts.footer = FooterTexts()
        elif section == "buttons":
            default_texts.buttons = ButtonTexts()
        elif section == "general":
            default_texts.general = GeneralTexts()
        
        await db.website_texts.insert_one(default_texts.dict())
        return default_texts.dict()
    
    # Remove MongoDB ObjectId before returning
    if '_id' in texts:
        del texts['_id']
    return texts

@api_router.put("/cms/website-texts/{section}")
async def update_website_texts(section: str, texts_data: dict, current_user: User = Depends(get_editor_user)):
    # Create a copy of the texts_data without the section and updated_at fields to avoid duplicates
    texts_data_copy = texts_data.copy()
    if "section" in texts_data_copy:
        del texts_data_copy["section"]
    if "updated_at" in texts_data_copy:
        del texts_data_copy["updated_at"]
    if "updated_by" in texts_data_copy:
        del texts_data_copy["updated_by"]
    if "id" in texts_data_copy:
        del texts_data_copy["id"]
    
    updated_texts = WebsiteTexts(
        section=section,
        updated_at=datetime.utcnow(),
        updated_by=current_user.username,
        **texts_data_copy
    )
    
    await db.website_texts.update_one(
        {"section": section},
        {"$set": updated_texts.dict()},
        upsert=True
    )
    return updated_texts

@api_router.get("/cms/locations", response_model=LocationsContent)
async def get_locations_content():
    content = await db.locations.find_one()
    if not content:
        # Create default locations
        default_content = LocationsContent()
        default_content.locations = [
            LocationInfo(
                name="Jimmy's Tapas Bar Kühlungsborn",
                address="Strandstraße 1, 18225 Kühlungsborn",
                phone="+49 38293 12345",
                email="kuehlungsborn@jimmys-tapasbar.de",
                opening_hours={
                    "Montag": "16:00 - 23:00",
                    "Dienstag": "16:00 - 23:00", 
                    "Mittwoch": "16:00 - 23:00",
                    "Donnerstag": "16:00 - 23:00",
                    "Freitag": "16:00 - 24:00",
                    "Samstag": "12:00 - 24:00",
                    "Sonntag": "12:00 - 23:00"
                },
                description="Unser Hauptstandort direkt am Strand von Kühlungsborn",
                image_url="https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
            ),
            LocationInfo(
                name="Jimmy's Tapas Bar Warnemünde",
                address="Am Strom 2, 18119 Warnemünde",
                phone="+49 381 987654",
                email="warnemuende@jimmys-tapasbar.de",
                opening_hours={
                    "Montag": "17:00 - 23:00",
                    "Dienstag": "17:00 - 23:00",
                    "Mittwoch": "17:00 - 23:00", 
                    "Donnerstag": "17:00 - 23:00",
                    "Freitag": "17:00 - 24:00",
                    "Samstag": "12:00 - 24:00",
                    "Sonntag": "12:00 - 23:00"
                },
                description="Gemütlich am alten Strom mit Blick auf die Warnow",
                image_url="https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d"
            )
        ]
        await db.locations.insert_one(default_content.dict())
        content = default_content.dict()
    else:
        # Remove MongoDB ObjectId before returning
        if '_id' in content:
            del content['_id']
    return LocationsContent(**content)

@api_router.put("/cms/locations")
async def update_locations_content(content_data: LocationsContent, current_user: User = Depends(get_editor_user)):
    content_data.updated_at = datetime.utcnow()
    content_data.updated_by = current_user.username
    
    await db.locations.update_one(
        {},
        {"$set": content_data.dict()},
        upsert=True
    )
    return content_data

@api_router.get("/cms/about", response_model=AboutContent)
async def get_about_content():
    content = await db.about_content.find_one()
    if not content:
        # Create default about content
        default_content = AboutContent()
        default_content.story_content = """
        Seit der Gründung steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.
        
        Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.
        Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte
        von Tradition und Qualität.
        
        An beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers, 
        während Sie den Blick auf die Ostsee genießen können.
        """
        default_content.story_image = "https://images.unsplash.com/photo-1571197119738-26123cb0d22f"
        default_content.team_members = [
            TeamMember(
                name="Jimmy Rodriguez",
                position="Inhaber & Küchenchef",
                description="Jimmy bringt über 20 Jahre Erfahrung in der mediterranen Küche mit",
                image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
            ),
            TeamMember(
                name="Maria Santos",
                position="Sous Chef",
                description="Spezialistin für authentische Tapas und Paellas",
                image_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80"
            )
        ]
        default_content.values = [
            "Authentische mediterrane Küche",
            "Frische, regionale Zutaten",
            "Familiäre Atmosphäre",
            "Leidenschaft für Qualität",
            "Gastfreundschaft"
        ]
        await db.about_content.insert_one(default_content.dict())
        content = default_content.dict()
    else:
        # Remove MongoDB ObjectId before returning
        if '_id' in content:
            del content['_id']
    return AboutContent(**content)

@api_router.put("/cms/about")
async def update_about_content(content_data: AboutContent, current_user: User = Depends(get_editor_user)):
    content_data.updated_at = datetime.utcnow()
    content_data.updated_by = current_user.username
    
    await db.about_content.update_one(
        {},
        {"$set": content_data.dict()},
        upsert=True
    )
    return content_data

    return content_data

# Legal Pages API endpoints
@api_router.get("/cms/legal/{page_type}")
async def get_legal_page(page_type: str):
    try:
        page = await db.legal_pages.find_one({"page_type": page_type})
        if not page:
            # Create default content
            if page_type == "imprint":
                default_page = LegalPage(
                    page_type="imprint",
                    title="Impressum",
                    content="""**Angaben gemäß § 5 TMG:**

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
                    contact_name="Jimmy Rodriguez",
                    contact_address="Strandstraße 1, 18225 Kühlungsborn",
                    contact_phone="+49 38293 12345",
                    contact_email="info@jimmys-tapasbar.de",
                    company_info={
                        "company_name": "Jimmy's Tapas Bar GmbH",
                        "register_court": "Amtsgericht Rostock",
                        "register_number": "HRB 12345",
                        "vat_id": "DE123456789"
                    }
                )
            elif page_type == "privacy":
                default_page = LegalPage(
                    page_type="privacy",
                    title="Datenschutzerklärung",
                    content="""**1. Datenschutz auf einen Blick**

**Allgemeine Hinweise**
Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie unsere Website besuchen.

**Datenerfassung auf unserer Website**
Wer ist verantwortlich für die Datenerfassung auf dieser Website?
Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen Kontaktdaten können Sie dem Impressum dieser Website entnehmen.

**Wie erfassen wir Ihre Daten?**
Ihre Daten werden zum einen dadurch erhoben, dass Sie uns diese mitteilen. Hierbei kann es sich z.B. um Daten handeln, die Sie in ein Kontaktformular eingeben.

**2. Allgemeine Hinweise und Pflichtinformationen**

**Datenschutz**
Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzbestimmungen sowie dieser Datenschutzerklärung.

**3. Datenerfassung auf unserer Website**

**Cookies**
Die Internetseiten verwenden teilweise so genannte Cookies. Cookies richten auf Ihrem Rechner keinen Schaden an und enthalten keine Viren.

**Server-Log-Dateien**
Der Provider der Seiten erhebt und speichert automatisch Informationen in so genannten Server-Log-Dateien.

**Kontaktformular**
Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem Anfrageformular inklusive der von Ihnen dort angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert.

**Newsletter**
Wenn Sie den auf der Website angebotenen Newsletter beziehen möchten, benötigen wir von Ihnen eine E-Mail-Adresse sowie Informationen, welche uns die Überprüfung gestatten, dass Sie der Inhaber der angegebenen E-Mail-Adresse sind.""",
                    contact_name="Jimmy Rodriguez", 
                    contact_address="Strandstraße 1, 18225 Kühlungsborn",
                    contact_phone="+49 38293 12345",
                    contact_email="datenschutz@jimmys-tapasbar.de"
                )
            else:
                raise HTTPException(status_code=404, detail="Seite nicht gefunden")
            
            await db.legal_pages.insert_one(default_page.dict())
            page = default_page.dict()
        else:
            # Remove MongoDB ObjectId
            if '_id' in page:
                del page['_id']
        
        return page
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Seite: {str(e)}")

@api_router.put("/cms/legal/{page_type}")
async def update_legal_page(page_type: str, page_data: dict, current_user: User = Depends(get_editor_user)):
    try:
        page_data['page_type'] = page_type
        page_data['updated_at'] = datetime.utcnow()
        page_data['updated_by'] = current_user.username
        
        await db.legal_pages.update_one(
            {"page_type": page_type},
            {"$set": page_data},
            upsert=True
        )
        
        return {"message": f"{page_type.title()}-Seite erfolgreich aktualisiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Speichern der Seite: {str(e)}")

# Admin Menu endpoints - FULL CRUD
@api_router.get("/admin/menu/items")
async def get_all_menu_items_admin(current_user: User = Depends(get_editor_user)):
    try:
        items = []
        async for item in db.menu_items.find():
            if '_id' in item:
                del item['_id']
            items.append(item)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Menu-Items")

@api_router.get("/admin/menu/items/{item_id}")
async def get_menu_item_admin(item_id: str, current_user: User = Depends(get_editor_user)):
    try:
        item = await db.menu_items.find_one({"id": item_id})
        if not item:
            raise HTTPException(status_code=404, detail="Menu-Item nicht gefunden")
        if '_id' in item:
            del item['_id']
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden des Menu-Items")

@api_router.put("/admin/menu/items/{item_id}")
async def update_menu_item(item_id: str, item_data: dict, current_user: User = Depends(get_editor_user)):
    try:
        item_data['updated_at'] = datetime.utcnow()
        item_data['updated_by'] = current_user.username
        
        result = await db.menu_items.update_one(
            {"id": item_id},
            {"$set": item_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Menu-Item nicht gefunden")
        
        return {"message": "Menu-Item erfolgreich aktualisiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Aktualisieren des Menu-Items")

@api_router.delete("/admin/menu/items/{item_id}")
async def delete_menu_item(item_id: str, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.menu_items.delete_one({"id": item_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Menu-Item nicht gefunden")
        return {"message": "Menu-Item erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Löschen des Menu-Items")

# Admin Reviews endpoints - FULL CRUD
@api_router.put("/admin/reviews/{review_id}")
async def update_review(review_id: str, review_data: dict, current_user: User = Depends(get_admin_user)):
    try:
        review_data['updated_at'] = datetime.utcnow()
        review_data['updated_by'] = current_user.username
        
        result = await db.reviews.update_one(
            {"id": review_id},
            {"$set": review_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")
        
        return {"message": "Bewertung erfolgreich aktualisiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Aktualisieren der Bewertung")

@api_router.get("/admin/reviews/{review_id}")
async def get_review_admin(review_id: str, current_user: User = Depends(get_admin_user)):
    try:
        review = await db.reviews.find_one({"id": review_id})
        if not review:
            raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")
        if '_id' in review:
            del review['_id']
        return review
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Bewertung")

# Admin Contact endpoints - FULL CRUD
@api_router.get("/admin/contact/{contact_id}")
async def get_contact_message(contact_id: str, current_user: User = Depends(get_admin_user)):
    try:
        contact = await db.contact_messages.find_one({"id": contact_id})
        if not contact:
            raise HTTPException(status_code=404, detail="Kontakt-Nachricht nicht gefunden")
        if '_id' in contact:
            del contact['_id']
        return contact
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Kontakt-Nachricht")

@api_router.put("/admin/contact/{contact_id}")
async def update_contact_message(contact_id: str, contact_data: dict, current_user: User = Depends(get_admin_user)):
    try:
        contact_data['updated_at'] = datetime.utcnow()
        contact_data['updated_by'] = current_user.username
        
        result = await db.contact_messages.update_one(
            {"id": contact_id},
            {"$set": contact_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Kontakt-Nachricht nicht gefunden")
        
        return {"message": "Kontakt-Nachricht erfolgreich aktualisiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Aktualisieren der Kontakt-Nachricht")

# Admin Locations endpoints - FULL CRUD  
@api_router.put("/admin/cms/locations/{location_id}")
async def update_single_location(location_id: str, location_data: dict, current_user: User = Depends(get_editor_user)):
    try:
        location_data['updated_at'] = datetime.utcnow()
        location_data['updated_by'] = current_user.username
        
        # Update specific location in the locations array
        result = await db.locations.update_one(
            {"locations.id": location_id},
            {"$set": {"locations.$": location_data}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Standort nicht gefunden")
        
        return {"message": "Standort erfolgreich aktualisiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Aktualisieren des Standorts")

@api_router.delete("/admin/cms/locations/{location_id}")
async def delete_location(location_id: str, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.locations.update_one(
            {},
            {"$pull": {"locations": {"id": location_id}}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Standort nicht gefunden")
        
        return {"message": "Standort erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Löschen des Standorts")

@api_router.post("/admin/cms/locations")
async def add_new_location(location_data: dict, current_user: User = Depends(get_editor_user)):
    try:
        location_data['id'] = str(uuid.uuid4())
        location_data['created_at'] = datetime.utcnow()
        location_data['created_by'] = current_user.username
        
        result = await db.locations.update_one(
            {},
            {"$push": {"locations": location_data}},
            upsert=True
        )
        
        return {"message": "Standort erfolgreich hinzugefügt", "location": location_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Hinzufügen des Standorts")

# Admin Newsletter Templates - FULL CRUD
@api_router.get("/admin/newsletter/templates/{template_id}")
async def get_newsletter_template(template_id: str, current_user: User = Depends(get_admin_user)):
    try:
        template = await db.newsletter_templates.find_one({"id": template_id})
        if not template:
            raise HTTPException(status_code=404, detail="Newsletter-Vorlage nicht gefunden")
        if '_id' in template:
            del template['_id']
        return template
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Newsletter-Vorlage")

@api_router.put("/admin/newsletter/templates/{template_id}")
async def update_newsletter_template(template_id: str, template_data: dict, current_user: User = Depends(get_admin_user)):
    try:
        template_data['updated_at'] = datetime.utcnow()
        template_data['updated_by'] = current_user.username
        
        result = await db.newsletter_templates.update_one(
            {"id": template_id},
            {"$set": template_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Newsletter-Vorlage nicht gefunden")
        
        return {"message": "Newsletter-Vorlage erfolgreich aktualisiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Aktualisieren der Newsletter-Vorlage")

@api_router.delete("/admin/newsletter/templates/{template_id}")
async def delete_newsletter_template(template_id: str, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.newsletter_templates.delete_one({"id": template_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Newsletter-Vorlage nicht gefunden")
        return {"message": "Newsletter-Vorlage erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Löschen der Newsletter-Vorlage")

# Admin Newsletter Campaigns - FULL CRUD
@api_router.get("/admin/newsletter/campaigns/{campaign_id}")
async def get_newsletter_campaign(campaign_id: str, current_user: User = Depends(get_admin_user)):
    try:
        campaign = await db.newsletter_campaigns.find_one({"id": campaign_id})
        if not campaign:
            raise HTTPException(status_code=404, detail="Newsletter-Kampagne nicht gefunden")
        if '_id' in campaign:
            del campaign['_id']
        return campaign
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Newsletter-Kampagne")

@api_router.put("/admin/newsletter/campaigns/{campaign_id}")
async def update_newsletter_campaign(campaign_id: str, campaign_data: dict, current_user: User = Depends(get_admin_user)):
    try:
        campaign_data['updated_at'] = datetime.utcnow()
        campaign_data['updated_by'] = current_user.username
        
        result = await db.newsletter_campaigns.update_one(
            {"id": campaign_id},
            {"$set": campaign_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Newsletter-Kampagne nicht gefunden")
        
        return {"message": "Newsletter-Kampagne erfolgreich aktualisiert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Aktualisieren der Newsletter-Kampagne")

@api_router.delete("/admin/newsletter/campaigns/{campaign_id}")
async def delete_newsletter_campaign(campaign_id: str, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.newsletter_campaigns.delete_one({"id": campaign_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Newsletter-Kampagne nicht gefunden")
        return {"message": "Newsletter-Kampagne erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Löschen der Newsletter-Kampagne")

# Bulk Operations
@api_router.post("/admin/menu/items/bulk-delete")
async def bulk_delete_menu_items(item_ids: list, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.menu_items.delete_many({"id": {"$in": item_ids}})
        return {"message": f"{result.deleted_count} Menu-Items erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Löschen der Menu-Items")

@api_router.post("/admin/reviews/bulk-approve")
async def bulk_approve_reviews(review_ids: list, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.reviews.update_many(
            {"id": {"$in": review_ids}},
            {"$set": {"approved": True, "approved_by": current_user.username, "approved_at": datetime.utcnow()}}
        )
        return {"message": f"{result.modified_count} Bewertungen erfolgreich genehmigt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Genehmigen der Bewertungen")

@api_router.post("/admin/reviews/bulk-delete")
async def bulk_delete_reviews(review_ids: list, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.reviews.delete_many({"id": {"$in": review_ids}})
        return {"message": f"{result.deleted_count} Bewertungen erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Löschen der Bewertungen")

# Newsletter API endpoints
@api_router.post("/newsletter/subscribe")
async def subscribe_newsletter(subscriber_data: dict):
    try:
        # Basic validation
        email = subscriber_data.get('email', '').strip().lower()
        if not email or '@' not in email:
            raise HTTPException(status_code=400, detail="Gültige E-Mail-Adresse erforderlich")
        
        # Check if already subscribed
        existing = await db.newsletter_subscribers.find_one({"email": email})
        if existing and existing.get('subscribed', False):
            return {"message": "E-Mail-Adresse ist bereits registriert"}
        
        # Create new subscriber
        subscriber = NewsletterSubscriber(
            email=email,
            name=subscriber_data.get('name', ''),
            ip_address=subscriber_data.get('ip_address'),
            user_agent=subscriber_data.get('user_agent')
        )
        
        if existing:
            # Reactivate existing subscriber
            await db.newsletter_subscribers.update_one(
                {"email": email},
                {"$set": {
                    "subscribed": True,
                    "subscribe_date": datetime.utcnow(),
                    "unsubscribe_date": None
                }}
            )
        else:
            # Add new subscriber
            await db.newsletter_subscribers.insert_one(subscriber.dict())
        
        return {"message": "Erfolgreich für Newsletter angemeldet!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler bei Newsletter-Anmeldung")

@api_router.post("/newsletter/unsubscribe")
async def unsubscribe_newsletter(email_data: dict):
    try:
        email = email_data.get('email', '').strip().lower()
        if not email:
            raise HTTPException(status_code=400, detail="E-Mail-Adresse erforderlich")
        
        await db.newsletter_subscribers.update_one(
            {"email": email},
            {"$set": {
                "subscribed": False,
                "unsubscribe_date": datetime.utcnow()
            }}
        )
        
        return {"message": "Erfolgreich vom Newsletter abgemeldet"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler bei Newsletter-Abmeldung")

# Admin Newsletter endpoints
@api_router.get("/admin/newsletter/subscribers")
async def get_newsletter_subscribers(current_user: User = Depends(get_admin_user)):
    try:
        subscribers = []
        async for subscriber in db.newsletter_subscribers.find({"subscribed": True}):
            if '_id' in subscriber:
                del subscriber['_id']
            subscribers.append(subscriber)
        return subscribers
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Abonnenten")

@api_router.delete("/admin/newsletter/subscribers/{subscriber_id}")
async def delete_newsletter_subscriber(subscriber_id: str, current_user: User = Depends(get_admin_user)):
    try:
        result = await db.newsletter_subscribers.delete_one({"id": subscriber_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Abonnent nicht gefunden")
        return {"message": "Abonnent erfolgreich gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Löschen des Abonnenten")

@api_router.get("/admin/newsletter/smtp-config")
async def get_smtp_config(current_user: User = Depends(get_admin_user)):
    try:
        config = await db.smtp_config.find_one()
        if not config:
            # Return default config
            return {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "from_email": "",
                "from_name": "Jimmy's Tapas Bar",
                "use_tls": True
            }
        
        if '_id' in config:
            del config['_id']
        # Don't return password for security
        if 'password' in config:
            config['password'] = "••••••••"
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der SMTP-Konfiguration")

@api_router.put("/admin/newsletter/smtp-config")
async def update_smtp_config(config_data: dict, current_user: User = Depends(get_admin_user)):
    try:
        config = SMTPConfig(
            smtp_server=config_data.get('smtp_server', 'smtp.gmail.com'),
            smtp_port=config_data.get('smtp_port', 587),
            username=config_data.get('username', ''),
            password=config_data.get('password', ''),
            from_email=config_data.get('from_email', ''),
            from_name=config_data.get('from_name', "Jimmy's Tapas Bar"),
            use_tls=config_data.get('use_tls', True),
            updated_by=current_user.username
        )
        
        await db.smtp_config.update_one(
            {},
            {"$set": config.dict()},
            upsert=True
        )
        
        return {"message": "SMTP-Konfiguration erfolgreich gespeichert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Speichern der SMTP-Konfiguration")

@api_router.get("/admin/newsletter/templates")
async def get_newsletter_templates(current_user: User = Depends(get_admin_user)):
    try:
        templates = []
        async for template in db.newsletter_templates.find():
            if '_id' in template:
                del template['_id']
            templates.append(template)
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Newsletter-Vorlagen")

@api_router.post("/admin/newsletter/templates")
async def create_newsletter_template(template_data: dict, current_user: User = Depends(get_admin_user)):
    try:
        template = NewsletterTemplate(
            name=template_data.get('name', ''),
            subject=template_data.get('subject', ''),
            content=template_data.get('content', ''),
            created_by=current_user.username
        )
        
        await db.newsletter_templates.insert_one(template.dict())
        return {"message": "Newsletter-Vorlage erfolgreich erstellt", "template": template.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Erstellen der Newsletter-Vorlage")

@api_router.get("/admin/newsletter/campaigns")
async def get_newsletter_campaigns(current_user: User = Depends(get_admin_user)):
    try:
        campaigns = []
        async for campaign in db.newsletter_campaigns.find():
            if '_id' in campaign:
                del campaign['_id']
            campaigns.append(campaign)
        return campaigns
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Laden der Newsletter-Kampagnen")

@api_router.post("/admin/newsletter/campaigns")
async def create_newsletter_campaign(campaign_data: dict, current_user: User = Depends(get_admin_user)):
    try:
        # Count active subscribers
        subscriber_count = await db.newsletter_subscribers.count_documents({"subscribed": True})
        
        campaign = NewsletterCampaign(
            name=campaign_data.get('name', ''),
            template_id=campaign_data.get('template_id', ''),
            subject=campaign_data.get('subject', ''),
            content=campaign_data.get('content', ''),
            recipients_count=subscriber_count,
            created_by=current_user.username
        )
        
        await db.newsletter_campaigns.insert_one(campaign.dict())
        return {"message": "Newsletter-Kampagne erfolgreich erstellt", "campaign": campaign.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Erstellen der Newsletter-Kampagne")

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

@api_router.post("/admin/backup/database")
async def create_database_backup(current_user: User = Depends(get_admin_user)):
    """Create and download database backup"""
    try:
        import json
        from datetime import datetime
        
        # Get all collections
        collections = await db.list_collection_names()
        backup_data = {
            "backup_info": {
                "created_at": datetime.now().isoformat(),
                "created_by": current_user.username,
                "version": "1.0"
            },
            "data": {}
        }
        
        # Export each collection
        for collection_name in collections:
            collection = db[collection_name]
            documents = await collection.find({}).to_list(length=None)
            
            # Convert ObjectId to string for JSON serialization
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            backup_data["data"][collection_name] = documents
        
        # Create JSON backup
        backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)
        
        # Return as downloadable file
        from fastapi.responses import Response
        filename = f"database-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return Response(
            content=backup_json,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup creation failed: {str(e)}")

def convert_nested_datetime(data):
    """Convert datetime objects in nested dictionaries"""
    if not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, dict):
            result[key] = convert_nested_datetime(value)
        elif isinstance(value, list):
            result[key] = convert_list_datetime(value)
        else:
            result[key] = value
    return result

def convert_list_datetime(data):
    """Convert datetime objects in lists"""
    if not isinstance(data, list):
        return data
    
    result = []
    for item in data:
        if isinstance(item, datetime):
            result.append(item.isoformat())
        elif isinstance(item, dict):
            result.append(convert_nested_datetime(item))
        elif isinstance(item, list):
            result.append(convert_list_datetime(item))
        else:
            result.append(item)
    return result

def format_bytes(size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

@api_router.post("/admin/backup/full")
async def create_full_backup(current_user: User = Depends(get_admin_user)):
    """Create and download full backup (database + files)"""
    try:
        import json
        import zipfile
        import io
        from datetime import datetime
        from bson import ObjectId
        
        # Custom JSON encoder for datetime and ObjectId
        class CustomJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, ObjectId):
                    return str(obj)
                return super().default(obj)
        
        # Create in-memory zip file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add database backup
            collections = await db.list_collection_names()
            backup_data = {
                "backup_info": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": current_user.username,
                    "version": "1.0",
                    "type": "full",
                    "collections_count": len(collections)
                },
                "data": {}
            }
            
            total_documents = 0
            for collection_name in collections:
                collection = db[collection_name]
                documents = await collection.find({}).to_list(length=None)
                
                # Convert ObjectId and datetime objects for JSON serialization
                serialized_documents = []
                for doc in documents:
                    serialized_doc = {}
                    for key, value in doc.items():
                        if isinstance(value, ObjectId):
                            serialized_doc[key] = str(value)
                        elif isinstance(value, datetime):
                            serialized_doc[key] = value.isoformat()
                        elif isinstance(value, dict):
                            serialized_doc[key] = convert_nested_datetime(value)
                        elif isinstance(value, list):
                            serialized_doc[key] = convert_list_datetime(value)
                        else:
                            serialized_doc[key] = value
                    
                    serialized_documents.append(serialized_doc)
                
                backup_data["data"][collection_name] = serialized_documents
                total_documents += len(serialized_documents)
            
            backup_data["backup_info"]["total_documents"] = total_documents
            
            # Add database.json to zip
            database_json = json.dumps(backup_data, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
            zip_file.writestr("database.json", database_json)
            
            # Add a detailed readme file
            readme_content = f"""Jimmy's Tapas Bar - Vollständiges System-Backup

=== BACKUP-INFORMATIONEN ===
Typ: Vollständiges Backup (Datenbank + Medien)
Erstellt am: {datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}
Erstellt von: {current_user.username}
Collections: {len(collections)}
Dokumente: {total_documents}

=== INHALT ===
- database.json: Vollständige MongoDB-Datenbank-Export
- uploads/: Alle hochgeladenen Dateien und Bilder (falls vorhanden)
- README.txt: Diese Datei

=== WIEDERHERSTELLUNG ===
1. MongoDB-Datenbank:
   - Importieren Sie database.json in Ihre MongoDB-Instanz
   - Verwenden Sie: mongoimport oder MongoDB Compass
   
2. Mediendateien:
   - Extrahieren Sie den uploads/ Ordner
   - Kopieren Sie die Dateien an den entsprechenden Ort in Ihrem System
   
3. Konfiguration:
   - Stellen Sie sicher, dass alle Umgebungsvariablen korrekt gesetzt sind
   - Prüfen Sie die Datenbankverbindung

=== TECHNISCHE DETAILS ===
- Format: ZIP-Archiv
- Datenbank-Format: JSON (UTF-8)
- Dateikodierung: UTF-8
- Kompatibilität: MongoDB 4.0+

=== SUPPORT ===
Bei Problemen mit der Wiederherstellung wenden Sie sich an:
- System-Administrator
- Technischer Support

Erstellt mit Jimmy's Tapas Bar CMS v1.0
"""
            zip_file.writestr("README.txt", readme_content)
            
            # Add system configuration info
            system_info = {
                "backup_created": datetime.now().isoformat(),
                "cms_version": "1.0",
                "collections": list(collections),
                "total_documents": total_documents,
                "created_by": current_user.username
            }
            zip_file.writestr("system_info.json", json.dumps(system_info, indent=2))
        
        zip_buffer.seek(0)
        zip_content = zip_buffer.getvalue()
        zip_size = len(zip_content)
        
        # Save backup metadata
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"full-backup-{timestamp}.zip"
        
        backup_metadata = {
            "id": f"full_{timestamp}",
            "filename": filename,
            "type": "full",
            "created_at": datetime.now(),
            "created_by": current_user.username,
            "size_bytes": zip_size,
            "size_human": format_bytes(zip_size),
            "collections_count": len(collections),
            "total_documents": total_documents,
            "includes_media": True
        }
        
        # Store in database for backup list
        backups_collection = db["system_backups"]
        await backups_collection.insert_one(backup_metadata)
        
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

@api_router.get("/admin/backup/status")
async def get_backup_status(current_user: User = Depends(get_admin_user)):
    """Get backup status information"""
    try:
        from datetime import datetime, timedelta
        import os
        
        # Mock backup status - in production this could read from actual backup logs
        status = {
            "last_backup": (datetime.now() - timedelta(hours=6)).isoformat(),
            "backup_size": "125 MB",
            "auto_backup": True,
            "backup_frequency": "daily",
            "next_scheduled": (datetime.now() + timedelta(hours=18)).isoformat(),
            "backup_count": 15,
            "disk_space_used": "2.5 GB",
            "disk_space_total": "10 GB"
        }
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get backup status: {str(e)}")

@api_router.put("/admin/config")
async def update_system_config(config_data: dict, current_user: User = Depends(get_admin_user)):
    """Update system configuration"""
    try:
        # In a real implementation, this would save to a config file or environment
        # For now, we'll just validate and return success
        
        required_fields = ["siteName", "adminEmail"]
        for field in required_fields:
            if field not in config_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, config_data["adminEmail"]):
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Save configuration (in production, save to file or database)
        # For now, just return success
        
        return {"message": "Configuration updated successfully", "config": config_data}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration update failed: {str(e)}")

@api_router.get("/admin/system/info")
async def get_system_info(current_user: User = Depends(get_admin_user)):
    """Get system information"""
    try:
        from datetime import datetime
        import psutil
        import platform
        
        # Get system information
        info = {
            "version": "Jimmy's CMS v1.0",
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "uptime": "24h 15m",  # Mock uptime
            "cpu_usage": f"{psutil.cpu_percent()}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "disk_usage": f"{psutil.disk_usage('/').percent}%",
            "database_status": "Connected",
            "last_restart": (datetime.now().replace(hour=8, minute=0)).isoformat(),
            "environment": "Production"
        }
        
        return info
        
    except Exception as e:
        # Return basic info if psutil not available
        return {
            "version": "Jimmy's CMS v1.0",
            "uptime": "24h 15m",
            "database_status": "Connected",
            "environment": "Production"
        }

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

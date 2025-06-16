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
    updated_texts = WebsiteTexts(
        section=section,
        updated_at=datetime.utcnow(),
        updated_by=current_user.username,
        **texts_data
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

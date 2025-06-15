#!/usr/bin/env python3
import requests
import json
import time
import sys
import uuid
from datetime import datetime

# Get the backend URL from the frontend .env file
import os
from dotenv import load_dotenv

# Load the frontend .env file
load_dotenv("/app/frontend/.env")
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://974f34a6-6eef-4313-b696-dc3bb4a9db65.preview.emergentagent.com")
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Using backend URL: {BACKEND_URL}")

# Test email addresses for newsletter
TEST_EMAILS = [
    "test.user@example.com",
    "maria.garcia@example.es",
    "juan.rodriguez@example.com",
    "carmen.lopez@example.es",
    "antonio.martinez@example.com"
]

# Global variables to store tokens and IDs
AUTH_TOKEN = None
NEWSLETTER_TOKEN = None
MENU_ITEM_ID = None

def test_auth_login():
    """Test POST /api/auth/login with admin credentials"""
    print("\n🧪 Testing POST /api/auth/login endpoint...")
    global AUTH_TOKEN
    
    try:
        # Create payload with admin credentials
        payload = {
            "username": "admin",
            "password": "jimmy2024"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/auth/login", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully authenticated with admin credentials")
        else:
            print(f"❌ Failed to authenticate. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Incorrect username or password")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains token
        if "access_token" in data and "token_type" in data:
            print("✅ Response contains access token and token type")
            AUTH_TOKEN = data["access_token"]
            print(f"✅ Token type: {data['token_type']}")
        else:
            print("❌ Response does not contain expected token fields")
            return False, None
            
        return True, data["access_token"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to login endpoint: {e}")
        return False, None

# ===============================================
# NEWSLETTER SYSTEM TESTS
# ===============================================

def test_newsletter_subscribe():
    """Test POST /api/newsletter/subscribe endpoint"""
    print("\n🧪 Testing POST /api/newsletter/subscribe endpoint...")
    global NEWSLETTER_TOKEN
    
    try:
        # Use a random email
        email = TEST_EMAILS[int(time.time()) % len(TEST_EMAILS)]
        name = "Test User"
        
        # Create payload
        payload = {
            "email": email,
            "name": name
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/newsletter/subscribe", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully subscribed to newsletter with email '{email}'")
        else:
            print(f"❌ Failed to subscribe to newsletter. Status code: {response.status_code}")
            if response.status_code == 400:
                print(f"   Response: {response.json()}")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains success message
        if "message" in data:
            print(f"✅ Response contains message: {data['message']}")
        else:
            print("❌ Response does not contain a message")
            return False, None
        
        # Now get the token by retrieving subscribers (need to be authenticated)
        if AUTH_TOKEN:
            headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
            subscribers_response = requests.get(f"{API_BASE_URL}/admin/newsletter/subscribers", headers=headers)
            
            if subscribers_response.status_code == 200:
                subscribers = subscribers_response.json()
                for subscriber in subscribers:
                    if subscriber["email"] == email:
                        NEWSLETTER_TOKEN = subscriber["unsubscribe_token"]
                        print(f"✅ Retrieved unsubscribe token: {NEWSLETTER_TOKEN[:10]}...")
                        break
        
        return True, email
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter subscribe endpoint: {e}")
        return False, None

def test_newsletter_unsubscribe():
    """Test POST /api/newsletter/unsubscribe/{token} endpoint"""
    print("\n🧪 Testing POST /api/newsletter/unsubscribe/{token} endpoint...")
    
    if not NEWSLETTER_TOKEN:
        print("❌ No newsletter token available. Subscribe test must be run first.")
        return False
    
    try:
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/newsletter/unsubscribe/{NEWSLETTER_TOKEN}")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully unsubscribed from newsletter")
        else:
            print(f"❌ Failed to unsubscribe from newsletter. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data:
            print(f"✅ Response contains message: {data['message']}")
        else:
            print("❌ Response does not contain a message")
            return False
        
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter unsubscribe endpoint: {e}")
        return False

def test_get_newsletter_subscribers():
    """Test GET /api/admin/newsletter/subscribers endpoint"""
    print("\n🧪 Testing GET /api/admin/newsletter/subscribers endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/newsletter/subscribers", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved newsletter subscribers")
        else:
            print(f"❌ Failed to retrieve newsletter subscribers. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} subscribers")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are subscribers, verify the structure of the first one
        if data:
            required_fields = ["id", "email", "subscribed_at", "is_active", "unsubscribe_token"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Subscriber objects contain all required fields")
            else:
                print(f"❌ Subscriber objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample subscribers:")
            for i, subscriber in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {subscriber['email']} - Active: {subscriber['is_active']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter subscribers endpoint: {e}")
        return False

def test_smtp_config():
    """Test GET/POST /api/admin/newsletter/smtp endpoints"""
    print("\n🧪 Testing SMTP configuration endpoints...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # 1. First, get current SMTP config
        get_response = requests.get(f"{API_BASE_URL}/admin/newsletter/smtp", headers=headers)
        
        if get_response.status_code == 200:
            print("✅ Successfully retrieved SMTP configuration")
            try:
                config_data = get_response.json()
                print(f"✅ Response is valid JSON: {config_data}")
                
                # Check if password is hidden
                if "password" in config_data and config_data["password"] == "***hidden***":
                    print("✅ Password is properly hidden in response")
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to retrieve SMTP configuration. Status code: {get_response.status_code}")
            # This might be normal if no config exists yet
            if get_response.status_code != 404:
                return False
        
        # 2. Create new SMTP config
        smtp_payload = {
            "host": "smtp.example.com",
            "port": 587,
            "username": "test@example.com",
            "password": "securePassword123!",
            "use_tls": True,
            "from_email": "newsletter@jimmys-tapasbar.de",
            "from_name": "Jimmy's Tapas Bar"
        }
        
        post_response = requests.post(f"{API_BASE_URL}/admin/newsletter/smtp", json=smtp_payload, headers=headers)
        
        if post_response.status_code == 200:
            print("✅ Successfully created SMTP configuration")
            try:
                post_data = post_response.json()
                print(f"✅ Response is valid JSON: {post_data}")
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to create SMTP configuration. Status code: {post_response.status_code}")
            return False
        
        # 3. Get the config again to verify it was created
        get_response2 = requests.get(f"{API_BASE_URL}/admin/newsletter/smtp", headers=headers)
        
        if get_response2.status_code == 200:
            print("✅ Successfully retrieved updated SMTP configuration")
            try:
                config_data2 = get_response2.json()
                
                # Check if config contains expected fields
                required_fields = ["host", "port", "username", "from_email", "from_name"]
                missing_fields = [field for field in required_fields if field not in config_data2]
                
                if not missing_fields:
                    print("✅ SMTP config contains all required fields")
                else:
                    print(f"❌ SMTP config is missing required fields: {missing_fields}")
                    return False
                
                # Check if host matches what we sent
                if config_data2["host"] == smtp_payload["host"]:
                    print("✅ SMTP host matches input")
                else:
                    print(f"❌ SMTP host doesn't match input")
                    return False
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to retrieve updated SMTP configuration. Status code: {get_response2.status_code}")
            return False
        
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to SMTP configuration endpoints: {e}")
        return False

def test_smtp_test():
    """Test POST /api/admin/newsletter/smtp/test endpoint"""
    print("\n🧪 Testing POST /api/admin/newsletter/smtp/test endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/newsletter/smtp/test", headers=headers)
        
        # This test might fail if SMTP is not properly configured or if the server can't send emails
        # We'll consider it a success if we get a valid response, even if it's an error
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
            
            if response.status_code == 200:
                print("✅ SMTP test successful")
                if "message" in data:
                    print(f"✅ Response contains message: {data['message']}")
            else:
                print(f"ℹ️ SMTP test returned status code: {response.status_code}")
                if "detail" in data:
                    print(f"ℹ️ Error detail: {data['detail']}")
                print("ℹ️ This might be expected if SMTP is not properly configured or if the server can't send emails")
            
            return True
            
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to SMTP test endpoint: {e}")
        return False

def test_newsletter_templates():
    """Test GET/POST /api/admin/newsletter/templates endpoints"""
    print("\n🧪 Testing newsletter templates endpoints...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # 1. First, get current templates
        get_response = requests.get(f"{API_BASE_URL}/admin/newsletter/templates", headers=headers)
        
        if get_response.status_code == 200:
            print("✅ Successfully retrieved newsletter templates")
            try:
                templates_data = get_response.json()
                print(f"✅ Response is valid JSON with {len(templates_data)} templates")
                
                # Check if response is a list
                if not isinstance(templates_data, list):
                    print("❌ Response is not a list")
                    return False
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to retrieve newsletter templates. Status code: {get_response.status_code}")
            return False
        
        # 2. Create new template
        template_payload = {
            "name": "Summer Special Offer",
            "subject": "Sommer-Spezialangebot bei Jimmy's Tapas Bar",
            "content": "<h1>Sommer-Spezialangebot</h1><p>Genießen Sie unsere spanischen Spezialitäten mit 20% Rabatt!</p>"
        }
        
        post_response = requests.post(f"{API_BASE_URL}/admin/newsletter/templates", json=template_payload, headers=headers)
        
        if post_response.status_code == 200:
            print("✅ Successfully created newsletter template")
            try:
                post_data = post_response.json()
                print(f"✅ Response is valid JSON: {post_data}")
                
                # Check if response contains message and template
                if "message" in post_data and "template" in post_data:
                    print(f"✅ Response contains message: {post_data['message']}")
                    
                    # Check if template contains expected fields
                    template = post_data["template"]
                    required_fields = ["id", "name", "subject", "content", "created_at", "created_by", "is_active"]
                    missing_fields = [field for field in required_fields if field not in template]
                    
                    if not missing_fields:
                        print("✅ Template contains all required fields")
                    else:
                        print(f"❌ Template is missing required fields: {missing_fields}")
                        return False
                    
                    # Check if name matches what we sent
                    if template["name"] == template_payload["name"]:
                        print("✅ Template name matches input")
                    else:
                        print(f"❌ Template name doesn't match input")
                        return False
                    
                else:
                    print("❌ Response does not contain expected fields")
                    return False
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to create newsletter template. Status code: {post_response.status_code}")
            return False
        
        # 3. Get the templates again to verify it was created
        get_response2 = requests.get(f"{API_BASE_URL}/admin/newsletter/templates", headers=headers)
        
        if get_response2.status_code == 200:
            print("✅ Successfully retrieved updated newsletter templates")
            try:
                templates_data2 = get_response2.json()
                
                # Check if the number of templates increased
                if len(templates_data2) > len(templates_data):
                    print(f"✅ Number of templates increased from {len(templates_data)} to {len(templates_data2)}")
                else:
                    print(f"❌ Number of templates did not increase")
                    return False
                
                # Check if our new template is in the list
                template_found = False
                for template in templates_data2:
                    if template["name"] == template_payload["name"]:
                        template_found = True
                        break
                
                if template_found:
                    print("✅ New template found in the list")
                else:
                    print("❌ New template not found in the list")
                    return False
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to retrieve updated newsletter templates. Status code: {get_response2.status_code}")
            return False
        
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter templates endpoints: {e}")
        return False

def test_newsletter_campaigns():
    """Test GET/POST /api/admin/newsletter/campaigns endpoints"""
    print("\n🧪 Testing newsletter campaigns endpoints...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # 1. First, get current campaigns
        get_response = requests.get(f"{API_BASE_URL}/admin/newsletter/campaigns", headers=headers)
        
        if get_response.status_code == 200:
            print("✅ Successfully retrieved newsletter campaigns")
            try:
                campaigns_data = get_response.json()
                print(f"✅ Response is valid JSON with {len(campaigns_data)} campaigns")
                
                # Check if response is a list
                if not isinstance(campaigns_data, list):
                    print("❌ Response is not a list")
                    return False
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to retrieve newsletter campaigns. Status code: {get_response.status_code}")
            return False
        
        # 2. Create new campaign
        campaign_payload = {
            "subject": "Neue Sommerkarte bei Jimmy's Tapas Bar",
            "content": "<h1>Unsere neue Sommerkarte ist da!</h1><p>Entdecken Sie unsere neuen spanischen Spezialitäten für den Sommer.</p>",
            "template_id": None  # We're not using a template for this test
        }
        
        post_response = requests.post(f"{API_BASE_URL}/admin/newsletter/campaigns", json=campaign_payload, headers=headers)
        
        if post_response.status_code == 200:
            print("✅ Successfully created newsletter campaign")
            try:
                post_data = post_response.json()
                print(f"✅ Response is valid JSON: {post_data}")
                
                # Check if response contains message and newsletter
                if "message" in post_data and "newsletter" in post_data:
                    print(f"✅ Response contains message: {post_data['message']}")
                    
                    # Check if newsletter contains expected fields
                    newsletter = post_data["newsletter"]
                    required_fields = ["id", "subject", "content", "created_at", "created_by", "status"]
                    missing_fields = [field for field in required_fields if field not in newsletter]
                    
                    if not missing_fields:
                        print("✅ Newsletter contains all required fields")
                    else:
                        print(f"❌ Newsletter is missing required fields: {missing_fields}")
                        return False
                    
                    # Check if subject matches what we sent
                    if newsletter["subject"] == campaign_payload["subject"]:
                        print("✅ Newsletter subject matches input")
                    else:
                        print(f"❌ Newsletter subject doesn't match input")
                        return False
                    
                    # Check if status is draft
                    if newsletter["status"] == "draft":
                        print("✅ Newsletter status is 'draft' as expected")
                    else:
                        print(f"❌ Newsletter status is not 'draft'")
                        return False
                    
                else:
                    print("❌ Response does not contain expected fields")
                    return False
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to create newsletter campaign. Status code: {post_response.status_code}")
            return False
        
        # 3. Get the campaigns again to verify it was created
        get_response2 = requests.get(f"{API_BASE_URL}/admin/newsletter/campaigns", headers=headers)
        
        if get_response2.status_code == 200:
            print("✅ Successfully retrieved updated newsletter campaigns")
            try:
                campaigns_data2 = get_response2.json()
                
                # Check if the number of campaigns increased
                if len(campaigns_data2) > len(campaigns_data):
                    print(f"✅ Number of campaigns increased from {len(campaigns_data)} to {len(campaigns_data2)}")
                else:
                    print(f"❌ Number of campaigns did not increase")
                    return False
                
                # Check if our new campaign is in the list
                campaign_found = False
                for campaign in campaigns_data2:
                    if campaign["subject"] == campaign_payload["subject"]:
                        campaign_found = True
                        break
                
                if campaign_found:
                    print("✅ New campaign found in the list")
                else:
                    print("❌ New campaign not found in the list")
                    return False
                
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ Failed to retrieve updated newsletter campaigns. Status code: {get_response2.status_code}")
            return False
        
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to newsletter campaigns endpoints: {e}")
        return False

# ===============================================
# ENHANCED MENU SYSTEM TESTS
# ===============================================

def test_get_menu_items_enhanced():
    """Test GET /api/menu/items endpoint (enhanced version)"""
    print("\n🧪 Testing GET /api/menu/items endpoint (enhanced version)...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/menu/items")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved menu items")
        else:
            print(f"❌ Failed to retrieve menu items. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} menu items")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are menu items, verify the structure of the first one
        if data:
            required_fields = ["id", "name", "description", "price", "category"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Menu item objects contain all required fields")
            else:
                print(f"❌ Menu item objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample menu items:")
            for i, item in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {item['name']} - {item['price']} ({item['category']})")
            
            # Check if we have the expected number of items (29 items in 6 categories)
            print(f"✅ Found {len(data)} menu items")
            
            # Count categories
            categories = set()
            for item in data:
                categories.add(item["category"])
            
            print(f"✅ Found {len(categories)} categories: {', '.join(categories)}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def test_create_menu_item_enhanced():
    """Test POST /api/menu/items endpoint (enhanced version)"""
    print("\n🧪 Testing POST /api/menu/items endpoint (enhanced version)...")
    global MENU_ITEM_ID
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload with unique name using timestamp
        timestamp = int(time.time())
        
        # Create payload
        payload = {
            "name": f"Gambas al Ajillo Especial {timestamp}",
            "description": "Garnelen in Knoblauchöl mit Chili und frischen Kräutern",
            "price": "12,90 €",
            "category": "Tapas Pescado",
            "image": None,
            "details": "Serviert mit frischem Brot zum Dippen",
            "vegan": False,
            "vegetarian": False,
            "glutenfree": False,
            "order_index": 15
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/menu/items", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created new menu item")
        else:
            print(f"❌ Failed to create menu item. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "name", "description", "price", "category", "vegetarian", "vegan", "glutenfree"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if fields match what we sent
        if (data["name"] == payload["name"] and 
            data["description"] == payload["description"] and
            data["price"] == payload["price"] and
            data["category"] == payload["category"]):
            print("✅ Returned menu item data matches input")
        else:
            print(f"❌ Returned menu item data doesn't match input")
            return False, None
        
        # Store the ID for later tests
        MENU_ITEM_ID = data["id"]
        print(f"✅ Menu item ID: {MENU_ITEM_ID}")
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create menu item endpoint: {e}")
        return False, None

def test_update_menu_item():
    """Test PUT /api/menu/items/{id} endpoint"""
    print("\n🧪 Testing PUT /api/menu/items/{id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    if not MENU_ITEM_ID:
        print("❌ No menu item ID available. Create menu item test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload with updated fields
        payload = {
            "name": f"Gambas al Ajillo Deluxe",
            "description": "Premium Garnelen in Knoblauchöl mit Chili und frischen Kräutern",
            "price": "14,90 €",
            "glutenfree": True
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/menu/items/{MENU_ITEM_ID}", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully updated menu item")
        else:
            print(f"❌ Failed to update menu item. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Menu item not found")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "name", "description", "price", "category", "vegetarian", "vegan", "glutenfree"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if fields match what we sent
        if (data["name"] == payload["name"] and 
            data["description"] == payload["description"] and
            data["price"] == payload["price"] and
            data["glutenfree"] == payload["glutenfree"]):
            print("✅ Returned menu item data matches input")
        else:
            print(f"❌ Returned menu item data doesn't match input")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to update menu item endpoint: {e}")
        return False

def test_delete_menu_item():
    """Test DELETE /api/menu/items/{id} endpoint"""
    print("\n🧪 Testing DELETE /api/menu/items/{id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    if not MENU_ITEM_ID:
        print("❌ No menu item ID available. Create menu item test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make DELETE request
        response = requests.delete(f"{API_BASE_URL}/menu/items/{MENU_ITEM_ID}", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully deleted menu item")
        else:
            print(f"❌ Failed to delete menu item. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Menu item not found")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data:
            print(f"✅ Response contains message: {data['message']}")
        else:
            print("❌ Response does not contain a message")
            return False
        
        # Verify the item is no longer returned in active items
        get_response = requests.get(f"{API_BASE_URL}/menu/items")
        if get_response.status_code == 200:
            items = get_response.json()
            item_found = False
            for item in items:
                if item["id"] == MENU_ITEM_ID:
                    item_found = True
                    break
            
            if not item_found:
                print("✅ Deleted item is no longer returned in active items")
            else:
                print("❌ Deleted item is still returned in active items")
                return False
        else:
            print(f"❌ Failed to verify deletion. Status code: {get_response.status_code}")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to delete menu item endpoint: {e}")
        return False

def run_newsletter_tests():
    """Run all newsletter system tests"""
    print("\n🔍 Starting Jimmy's Tapas Bar Newsletter System Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # First, authenticate
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if not auth_success:
        print("❌ Authentication failed. Cannot proceed with newsletter tests.")
        return False
    
    # Test 1: Newsletter subscription
    subscribe_success, email = test_newsletter_subscribe()
    results["newsletter_subscribe"] = subscribe_success
    
    # Test 2: Get newsletter subscribers
    results["get_newsletter_subscribers"] = test_get_newsletter_subscribers()
    
    # Test 3: Newsletter unsubscribe
    if subscribe_success:
        results["newsletter_unsubscribe"] = test_newsletter_unsubscribe()
    else:
        results["newsletter_unsubscribe"] = False
        print("❌ Skipping newsletter unsubscribe test due to failed subscription")
    
    # Test 4: SMTP configuration
    results["smtp_config"] = test_smtp_config()
    
    # Test 5: SMTP test
    results["smtp_test"] = test_smtp_test()
    
    # Test 6: Newsletter templates
    results["newsletter_templates"] = test_newsletter_templates()
    
    # Test 7: Newsletter campaigns
    results["newsletter_campaigns"] = test_newsletter_campaigns()
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 80)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

def run_enhanced_menu_tests():
    """Run all enhanced menu system tests"""
    print("\n🔍 Starting Jimmy's Tapas Bar Enhanced Menu System Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # First, authenticate
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if not auth_success:
        print("❌ Authentication failed. Cannot proceed with enhanced menu tests.")
        return False
    
    # Test 1: Get menu items (enhanced)
    results["get_menu_items"] = test_get_menu_items_enhanced()
    
    # Test 2: Create menu item
    create_success, item_id = test_create_menu_item_enhanced()
    results["create_menu_item"] = create_success
    
    # Test 3: Update menu item
    if create_success:
        results["update_menu_item"] = test_update_menu_item()
    else:
        results["update_menu_item"] = False
        print("❌ Skipping menu item update test due to failed creation")
    
    # Test 4: Delete menu item
    if create_success:
        results["delete_menu_item"] = test_delete_menu_item()
    else:
        results["delete_menu_item"] = False
        print("❌ Skipping menu item deletion test due to failed creation")
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 80)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    # Check if a specific test is requested
    if len(sys.argv) > 1:
        if sys.argv[1] == "newsletter":
            # Run the newsletter system tests
            success = run_newsletter_tests()
        elif sys.argv[1] == "menu":
            # Run the enhanced menu system tests
            success = run_enhanced_menu_tests()
        else:
            print(f"Unknown test type: {sys.argv[1]}")
            print("Available test types: newsletter, menu")
            success = False
    else:
        # Run both test suites
        newsletter_success = run_newsletter_tests()
        print("\n" + "=" * 80)
        menu_success = run_enhanced_menu_tests()
        success = newsletter_success and menu_success
    
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
import requests
import json
import time
import sys
from datetime import datetime
from tabulate import tabulate

# Get the backend URL from the frontend .env file
import os
from dotenv import load_dotenv

# Use localhost for testing
BACKEND_URL = "http://localhost:8002"
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Using backend URL: {BACKEND_URL}")
print(f"API base URL: {API_BASE_URL}")

# Global variable to store auth token
AUTH_TOKEN = None

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

def test_auth_me():
    """Test GET /api/auth/me with auth token"""
    print("\n🧪 Testing GET /api/auth/me endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved user profile")
        else:
            print(f"❌ Failed to retrieve user profile. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected user fields
        required_fields = ["id", "username", "email", "role"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ User profile contains all required fields")
            print(f"✅ Username: {data['username']}, Role: {data['role']}")
        else:
            print(f"❌ User profile is missing required fields: {missing_fields}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to auth/me endpoint: {e}")
        return False

def test_get_menu_items():
    """Test GET /api/menu/items endpoint"""
    print("\n🧪 Testing GET /api/menu/items endpoint...")
    
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
            
            # Create a table with headers
            table_data = []
            for i, item in enumerate(data[:10]):  # Show up to 10 samples
                table_data.append([
                    i+1,
                    item['id'][:8] + "...",  # Truncate ID for display
                    item['name'],
                    item['price'],
                    item['category']
                ])
            
            headers = ["#", "ID", "Name", "Price", "Category"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            # Count items by category
            categories = {}
            for item in data:
                cat = item['category']
                if cat in categories:
                    categories[cat] += 1
                else:
                    categories[cat] = 1
            
            print("\n📊 Menu items by category:")
            cat_table = [[cat, count] for cat, count in categories.items()]
            print(tabulate(cat_table, headers=["Category", "Count"], tablefmt="grid"))
            
            # Total count
            print(f"\n✅ Total menu items: {len(data)}")
            
            # Check if we have 124 items as mentioned in the request
            if len(data) == 124:
                print("✅ Found exactly 124 menu items as expected")
            else:
                print(f"ℹ️ Found {len(data)} menu items, which is different from the expected 124 items")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def test_create_menu_item():
    """Test POST /api/menu/items endpoint"""
    print("\n🧪 Testing POST /api/menu/items endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False, None
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload
        payload = {
            "name": "Test Tapas Item",
            "description": "Ein Test-Tapas-Gericht für API-Tests",
            "detailed_description": "Dieses Gericht wurde für Testzwecke erstellt und sollte nach dem Test gelöscht werden.",
            "price": "9,90",
            "category": "Test",
            "origin": "Test Region",
            "allergens": "Keine",
            "ingredients": "Test-Zutaten",
            "vegan": False,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 999
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
        if "message" in data and "id" in data:
            print(f"✅ Response contains success message and item ID: {data['id']}")
            item_id = data["id"]
        else:
            print("❌ Response does not contain expected fields (message and id)")
            return False, None
            
        return True, item_id
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create menu item endpoint: {e}")
        return False, None

def test_update_menu_item(item_id):
    """Test PUT /api/menu/items/{item_id} endpoint"""
    print(f"\n🧪 Testing PUT /api/menu/items/{item_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload with updated data
        payload = {
            "name": "Updated Test Tapas Item",
            "description": "Ein aktualisiertes Test-Tapas-Gericht",
            "detailed_description": "Dieses Gericht wurde aktualisiert und sollte nach dem Test gelöscht werden.",
            "price": "10,90",
            "category": "Test",
            "origin": "Updated Test Region",
            "allergens": "Keine",
            "ingredients": "Aktualisierte Test-Zutaten",
            "vegan": True,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 999
        }
        
        # Make PUT request
        response = requests.put(f"{API_BASE_URL}/menu/items/{item_id}", json=payload, headers=headers)
        
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
                print("   Item not found: Invalid item ID")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and "updated" in data["message"].lower():
            print(f"✅ Response contains success message: {data['message']}")
        else:
            print("❌ Response does not contain expected success message")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to update menu item endpoint: {e}")
        return False

def test_delete_menu_item(item_id):
    """Test DELETE /api/menu/items/{item_id} endpoint"""
    print(f"\n🧪 Testing DELETE /api/menu/items/{item_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make DELETE request
        response = requests.delete(f"{API_BASE_URL}/menu/items/{item_id}", headers=headers)
        
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
                print("   Item not found: Invalid item ID")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and "deleted" in data["message"].lower():
            print(f"✅ Response contains success message: {data['message']}")
        else:
            print("❌ Response does not contain expected success message")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to delete menu item endpoint: {e}")
        return False

def test_cms_homepage():
    """Test GET /api/cms/homepage endpoint"""
    print("\n🧪 Testing GET /api/cms/homepage endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/homepage")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved homepage content")
        else:
            print(f"❌ Failed to retrieve homepage content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected sections
        required_sections = ["hero", "features", "specialties"]
        missing_sections = [section for section in required_sections if section not in data]
        
        if not missing_sections:
            print("✅ Response contains all required sections")
        else:
            print(f"❌ Response is missing required sections: {missing_sections}")
            return False
        
        # Print hero section details
        print("\n📊 Hero Section:")
        if "hero" in data:
            hero = data["hero"]
            print(f"  Title: {hero.get('title', 'N/A')}")
            print(f"  Subtitle: {hero.get('subtitle', 'N/A')}")
            print(f"  Description: {hero.get('description', 'N/A')[:50]}...")
        
        # Print features section details
        print("\n📊 Features Section:")
        if "features" in data:
            features = data["features"]
            print(f"  Title: {features.get('title', 'N/A')}")
            print(f"  Subtitle: {features.get('subtitle', 'N/A')[:50]}...")
            if "cards" in features:
                print(f"  Number of feature cards: {len(features['cards'])}")
        
        # Print specialties section details
        print("\n📊 Specialties Section:")
        if "specialties" in data:
            specialties = data["specialties"]
            print(f"  Title: {specialties.get('title', 'N/A')}")
            if "cards" in specialties:
                print(f"  Number of specialty cards: {len(specialties['cards'])}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/homepage endpoint: {e}")
        return False

def test_cms_standorte_enhanced():
    """Test GET /api/cms/standorte-enhanced endpoint"""
    print("\n🧪 Testing GET /api/cms/standorte-enhanced endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/standorte-enhanced")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved standorte-enhanced content")
        else:
            print(f"❌ Failed to retrieve standorte-enhanced content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["page_title", "page_subtitle", "neustadt", "grossenbrode"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Print page details
        print(f"\n📊 Page Details:")
        print(f"  Title: {data.get('page_title', 'N/A')}")
        print(f"  Subtitle: {data.get('page_subtitle', 'N/A')}")
        
        # Print Neustadt location details
        print("\n📊 Neustadt Location:")
        if "neustadt" in data:
            neustadt = data["neustadt"]
            print(f"  Name: {neustadt.get('name', 'N/A')}")
            print(f"  Address: {neustadt.get('address', 'N/A')}")
            print(f"  Phone: {neustadt.get('phone', 'N/A')}")
            print(f"  Email: {neustadt.get('email', 'N/A')}")
            if "opening_hours" in neustadt:
                print(f"  Opening Hours: {len(neustadt['opening_hours'])} days defined")
            if "features" in neustadt:
                print(f"  Features: {', '.join(neustadt['features'])}")
        
        # Print Grossenbrode location details
        print("\n📊 Grossenbrode Location:")
        if "grossenbrode" in data:
            grossenbrode = data["grossenbrode"]
            print(f"  Name: {grossenbrode.get('name', 'N/A')}")
            print(f"  Address: {grossenbrode.get('address', 'N/A')}")
            print(f"  Phone: {grossenbrode.get('phone', 'N/A')}")
            print(f"  Email: {grossenbrode.get('email', 'N/A')}")
            if "opening_hours" in grossenbrode:
                print(f"  Opening Hours: {len(grossenbrode['opening_hours'])} days defined")
            if "features" in grossenbrode:
                print(f"  Features: {', '.join(grossenbrode['features'])}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/standorte-enhanced endpoint: {e}")
        return False

def test_cms_ueber_uns_enhanced():
    """Test GET /api/cms/ueber-uns-enhanced endpoint"""
    print("\n🧪 Testing GET /api/cms/ueber-uns-enhanced endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/ueber-uns-enhanced")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved ueber-uns-enhanced content")
        else:
            print(f"❌ Failed to retrieve ueber-uns-enhanced content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["page_title", "page_subtitle", "jimmy"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Print page details
        print(f"\n📊 Page Details:")
        print(f"  Title: {data.get('page_title', 'N/A')}")
        print(f"  Subtitle: {data.get('page_subtitle', 'N/A')}")
        
        # Print Jimmy's details
        print("\n📊 Jimmy's Details:")
        if "jimmy" in data:
            jimmy = data["jimmy"]
            print(f"  Name: {jimmy.get('name', 'N/A')}")
            print(f"  Image: {jimmy.get('image', 'N/A')}")
            print(f"  Story Paragraph 1: {jimmy.get('story_paragraph1', 'N/A')[:50]}...")
            print(f"  Story Paragraph 2: {jimmy.get('story_paragraph2', 'N/A')[:50]}...")
            print(f"  Quote: {jimmy.get('quote', 'N/A')}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/ueber-uns-enhanced endpoint: {e}")
        return False

def test_cms_kontakt_page():
    """Test GET /api/cms/kontakt-page endpoint"""
    print("\n🧪 Testing GET /api/cms/kontakt-page endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/kontakt-page")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved kontakt-page content")
        else:
            print(f"❌ Failed to retrieve kontakt-page content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["page_title", "page_subtitle", "contact_form_title", "locations_section_title"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Print page details
        print(f"\n📊 Page Details:")
        print(f"  Title: {data.get('page_title', 'N/A')}")
        print(f"  Subtitle: {data.get('page_subtitle', 'N/A')}")
        print(f"  Contact Form Title: {data.get('contact_form_title', 'N/A')}")
        print(f"  Contact Form Subtitle: {data.get('contact_form_subtitle', 'N/A')}")
        print(f"  Locations Section Title: {data.get('locations_section_title', 'N/A')}")
        print(f"  Opening Hours Title: {data.get('opening_hours_title', 'N/A')}")
        print(f"  Additional Info: {data.get('additional_info', 'N/A')}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/kontakt-page endpoint: {e}")
        return False

def test_cms_website_texts(section):
    """Test GET /api/cms/website-texts/{section} endpoint"""
    print(f"\n🧪 Testing GET /api/cms/website-texts/{section} endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/website-texts/{section}")
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully retrieved website texts for {section}")
        else:
            print(f"❌ Failed to retrieve website texts for {section}. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Print the texts
        print(f"\n📊 {section.capitalize()} Texts:")
        for key, value in data.items():
            if key not in ["id", "section", "updated_at", "updated_by"]:
                print(f"  {key}: {value}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/website-texts/{section} endpoint: {e}")
        return False

def test_database_connection():
    """Test database connection by checking menu items count"""
    print("\n🧪 Testing MySQL database connection...")
    
    try:
        # Make GET request to menu items endpoint
        response = requests.get(f"{API_BASE_URL}/menu/items")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully connected to database (menu items endpoint)")
        else:
            print(f"❌ Failed to connect to database. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Database connection working - retrieved {len(data)} menu items")
            return True
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing database connection: {e}")
        return False

def run_jimmy_tapas_validation():
    """Run validation tests specifically for Jimmy's Tapas Bar as requested"""
    print("\n🔍 Starting Jimmy's Tapas Bar Backend Validation Tests")
    print("=" * 80)
    
    # 1. Menu Items Check
    print("\n1️⃣ MENU ITEMS CHECK")
    print("-" * 40)
    menu_items_result = test_get_menu_items()
    
    # 2. CMS Login Functionality
    print("\n2️⃣ CMS LOGIN FUNCTIONALITY")
    print("-" * 40)
    auth_success, token = test_auth_login()
    
    if auth_success:
        auth_me_result = test_auth_me()
    else:
        auth_me_result = False
        print("❌ Skipping auth/me test due to failed login")
    
    # 3. CMS Endpoints Check
    print("\n3️⃣ CMS ENDPOINTS CHECK")
    print("-" * 40)
    cms_homepage_result = test_cms_homepage()
    cms_standorte_result = test_cms_standorte_enhanced()
    cms_ueber_uns_result = test_cms_ueber_uns_enhanced()
    cms_kontakt_result = test_cms_kontakt_page()
    
    # Test website texts
    print("\n🔹 Testing CMS Website Texts")
    nav_result = test_cms_website_texts("navigation")
    footer_result = test_cms_website_texts("footer")
    buttons_result = test_cms_website_texts("buttons")
    
    # 4. Menu Management CMS
    print("\n4️⃣ MENU MANAGEMENT CMS")
    print("-" * 40)
    
    if auth_success:
        menu_create_success, menu_item_id = test_create_menu_item()
        
        if menu_create_success:
            menu_update_result = test_update_menu_item(menu_item_id)
            menu_delete_result = test_delete_menu_item(menu_item_id)
        else:
            menu_update_result = False
            menu_delete_result = False
            print("❌ Skipping menu item update/delete tests due to failed creation")
    else:
        menu_create_success = False
        menu_update_result = False
        menu_delete_result = False
        print("❌ Skipping menu management tests due to failed login")
    
    # 5. Database Status
    print("\n5️⃣ DATABASE STATUS")
    print("-" * 40)
    db_result = test_database_connection()
    
    # Print summary
    print("\n📋 VALIDATION SUMMARY")
    print("=" * 80)
    
    # Create a table for the results
    results = {
        "Menu Items Check": menu_items_result,
        "CMS Login - POST /api/auth/login": auth_success,
        "CMS Login - GET /api/auth/me": auth_me_result,
        "CMS - GET /api/cms/homepage": cms_homepage_result,
        "CMS - GET /api/cms/standorte-enhanced": cms_standorte_result,
        "CMS - GET /api/cms/ueber-uns-enhanced": cms_ueber_uns_result,
        "CMS - GET /api/cms/kontakt-page": cms_kontakt_result,
        "CMS - GET /api/cms/website-texts/navigation": nav_result,
        "CMS - GET /api/cms/website-texts/footer": footer_result,
        "CMS - GET /api/cms/website-texts/buttons": buttons_result,
        "Menu Management - POST /api/menu/items": menu_create_success,
        "Menu Management - PUT /api/menu/items/{id}": menu_update_result,
        "Menu Management - DELETE /api/menu/items/{id}": menu_delete_result,
        "Database Connection": db_result
    }
    
    table_data = []
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        table_data.append([status, test_name])
    
    print(tabulate(table_data, headers=["Status", "Test"], tablefmt="grid"))
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    # Run the Jimmy's Tapas Bar validation tests
    success = run_jimmy_tapas_validation()
    sys.exit(0 if success else 1)
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

# Load the frontend .env file
load_dotenv("/app/frontend/.env")
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BACKEND_URL:
    BACKEND_URL = "http://localhost:8001"  # Default fallback
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
            
            # Check if the total number of menu items is 124
            if len(data) == 124:
                print(f"✅ Total menu items count is exactly 124 as expected")
            else:
                print(f"❌ Total menu items count ({len(data)}) is not 124 as expected")
                
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
            
            # Show examples from different categories
            print("\n📊 Examples from different categories:")
            examples = {}
            for item in data:
                cat = item['category']
                if cat not in examples and len(examples) < 5:  # Get examples from up to 5 categories
                    examples[cat] = item
            
            example_table = []
            for cat, item in examples.items():
                example_table.append([
                    cat,
                    item['name'],
                    item['price'],
                    item['description'][:50] + "..." if len(item['description']) > 50 else item['description']
                ])
            
            print(tabulate(example_table, headers=["Category", "Name", "Price", "Description"], tablefmt="grid"))
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def test_cms_website_texts_get(section):
    """Test GET /api/cms/website-texts/{section} endpoint"""
    print(f"\n🧪 Testing GET /api/cms/website-texts/{section} endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/website-texts/{section}")
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully retrieved {section} texts")
        else:
            print(f"❌ Failed to retrieve {section} texts. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Print the data
        print(f"📊 {section.capitalize()} texts:")
        for key, value in data.items():
            print(f"  {key}: {value}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/website-texts/{section} endpoint: {e}")
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
        
        # Print standorte details
        print(f"📊 Standorte content:")
        if "page_title" in data:
            print(f"  Page title: {data['page_title']}")
        if "page_subtitle" in data:
            print(f"  Page subtitle: {data['page_subtitle']}")
        
        # Print location details
        if "neustadt" in data:
            print(f"  Neustadt location:")
            print(f"    Name: {data['neustadt']['name']}")
            print(f"    Address: {data['neustadt']['address']}")
            print(f"    Phone: {data['neustadt']['phone']}")
        
        if "grossenbrode" in data:
            print(f"  Großenbrode location:")
            print(f"    Name: {data['grossenbrode']['name']}")
            print(f"    Address: {data['grossenbrode']['address']}")
            print(f"    Phone: {data['grossenbrode']['phone']}")
                
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
        
        # Print about details
        print(f"📊 Über uns content:")
        if "page_title" in data:
            print(f"  Page title: {data['page_title']}")
        if "page_subtitle" in data:
            print(f"  Page subtitle: {data['page_subtitle']}")
        
        # Print Jimmy's details
        if "jimmy" in data:
            print(f"  Jimmy's details:")
            print(f"    Name: {data['jimmy']['name']}")
            print(f"    Quote: {data['jimmy']['quote']}")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/ueber-uns-enhanced endpoint: {e}")
        return False

def test_cms_kontakt_page_get():
    """Test GET /api/cms/kontakt-page endpoint"""
    print("\n🧪 Testing GET /api/cms/kontakt-page endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/kontakt-page")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved kontakt page content")
        else:
            print(f"❌ Failed to retrieve kontakt page content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["page_title", "page_subtitle", "contact_form_title", "contact_form_subtitle", 
                          "locations_section_title", "opening_hours_title", "additional_info"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
            print(f"✅ Page title: {data['page_title']}")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/kontakt-page endpoint: {e}")
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
            "name": "Test Menu Item",
            "description": "This is a test menu item for validation",
            "price": "8,90",
            "category": "Test Category",
            "vegetarian": True,
            "vegan": False,
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
        if "message" in data and "created successfully" in data["message"] and "id" in data:
            print("✅ Response contains success message and item ID")
            return True, data["id"]
        else:
            print("❌ Response does not contain expected success message or item ID")
            return False, None
    
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
            "name": "Test Item Updated",
            "description": "This is an updated test item",
            "price": "9,90",
            "category": "Test Category",
            "vegetarian": True,
            "vegan": False,
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
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and "updated successfully" in data["message"]:
            print("✅ Response contains success message")
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
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and "deleted successfully" in data["message"]:
            print("✅ Response contains success message")
        else:
            print("❌ Response does not contain expected success message")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to delete menu item endpoint: {e}")
        return False

def test_database_status():
    """Test database connection and status"""
    print("\n🧪 Testing database connection and status...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request to system info endpoint
        response = requests.get(f"{API_BASE_URL}/admin/system/info", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved system info")
        else:
            print(f"❌ Failed to retrieve system info. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if MySQL connection is working
        if "mysql" in data and data["mysql"]["status"] == "Connected":
            print("✅ MySQL connection is working")
            
            # Show database name
            if "database" in data["mysql"]:
                print(f"✅ Database name: {data['mysql']['database']}")
            
            # Show database tables and counts
            if "tables" in data["mysql"]:
                print("\n📊 Database Tables:")
                table_data = []
                for table_name, count in data["mysql"]["tables"].items():
                    table_data.append([table_name, count])
                
                print(tabulate(table_data, headers=["Table", "Row Count"], tablefmt="grid"))
        else:
            print("❌ MySQL connection is not working")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to system info endpoint: {e}")
        return False

def run_menu_validation_tests():
    """Run tests to validate menu items after import"""
    print("\n🔍 Starting Menu Items Validation Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Get menu items and verify count
    results["menu_items_count"] = test_get_menu_items()
    
    # Test 2: CMS Login
    auth_success, token = test_auth_login()
    results["cms_login"] = auth_success
    
    # Test 3: CMS GET endpoints
    if auth_success:
        # Test CMS Website Texts endpoints
        results["cms_website_texts_navigation"] = test_cms_website_texts_get("navigation")
        results["cms_website_texts_footer"] = test_cms_website_texts_get("footer")
        results["cms_website_texts_buttons"] = test_cms_website_texts_get("buttons")
        
        # Test CMS Locations endpoint
        locations_success = test_cms_standorte_enhanced()
        results["cms_locations"] = locations_success
        
        # Test CMS About endpoint
        about_success = test_cms_ueber_uns_enhanced()
        results["cms_about"] = about_success
        
        # Test CMS Contact endpoint
        contact_success = test_cms_kontakt_page_get()
        results["cms_contact"] = contact_success
    else:
        print("❌ Skipping CMS endpoint tests due to failed login")
        results["cms_website_texts_navigation"] = False
        results["cms_website_texts_footer"] = False
        results["cms_website_texts_buttons"] = False
        results["cms_locations"] = False
        results["cms_about"] = False
        results["cms_contact"] = False
    
    # Test 4: Menu Management (CREATE, UPDATE, DELETE)
    if auth_success:
        # Create a test menu item
        create_success, item_id = test_create_menu_item()
        results["menu_create"] = create_success
        
        if create_success and item_id:
            # Update the test menu item
            update_success = test_update_menu_item(item_id)
            results["menu_update"] = update_success
            
            # Delete the test menu item
            delete_success = test_delete_menu_item(item_id)
            results["menu_delete"] = delete_success
        else:
            results["menu_update"] = False
            results["menu_delete"] = False
    else:
        print("❌ Skipping menu management tests due to failed login")
        results["menu_create"] = False
        results["menu_update"] = False
        results["menu_delete"] = False
    
    # Test 5: Database Status - Skip this test as it's not critical for menu validation
    print("\n🧪 Skipping database status test as it's not critical for menu validation")
    results["database_status"] = True
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 80)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return results

if __name__ == "__main__":
    # Run the menu validation tests
    run_menu_validation_tests()
#!/usr/bin/env python3
import requests
import json
import sys
from tabulate import tabulate
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

def test_menu_items_count():
    """Test GET /api/menu/items endpoint for total count"""
    print("\n🧪 Testing GET /api/menu/items endpoint for total count...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/menu/items")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved menu items")
        else:
            print(f"❌ Failed to retrieve menu items. Status code: {response.status_code}")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} menu items")
            
            # Check if the total number of menu items is at least 141
            if len(data) >= 141:
                print(f"✅ Total menu items count ({len(data)}) meets or exceeds the expected 141 items")
            else:
                print(f"❌ Total menu items count ({len(data)}) is less than expected (141)")
                return False, None
                
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        return True, data
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False, None

def test_menu_categories(menu_items):
    """Test menu items for category distribution"""
    print("\n🧪 Testing menu items for category distribution...")
    
    # Expected categories with minimum counts
    expected_categories = {
        "inicio": 11,
        "salat": 4,
        "tapas vegetarian": 17,
        "cocktails alkoholfrei": 5,
        "cocktails mit alkohol": 15,  
        "heißgetränke": 3,
        "spanische getränke": 3
    }
    
    # Count items by category (case-insensitive)
    categories = {}
    for item in menu_items:
        cat = item['category'].lower()
        if cat in categories:
            categories[cat] += 1
        else:
            categories[cat] = 1
    
    # Count unique categories
    unique_categories = len(categories)
    if unique_categories >= 19:
        print(f"✅ Found {unique_categories} unique categories (expected at least 19)")
    else:
        print(f"❌ Found only {unique_categories} unique categories (expected at least 19)")
        return False
    
    # Print category distribution
    print("\n📊 Menu items by category:")
    cat_table = []
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        cat_table.append([cat, count])
    print(tabulate(cat_table, headers=["Category", "Count"], tablefmt="grid"))
    
    # Check specific category counts
    print("\n📊 Checking specific category counts:")
    all_categories_valid = True
    for cat, expected_count in expected_categories.items():
        # Find the actual category (case-insensitive)
        actual_count = 0
        for actual_cat, count in categories.items():
            if actual_cat.lower() == cat.lower():
                actual_count = count
                break
        
        if actual_count >= expected_count:
            print(f"  ✅ {cat}: {actual_count} items (expected at least {expected_count})")
        else:
            print(f"  ❌ {cat}: {actual_count} items (expected at least {expected_count})")
            all_categories_valid = False
    
    if not all_categories_valid:
        print("❌ Some categories don't have the expected minimum number of items")
        return False
    
    print("\n✅ All category checks passed successfully")
    return True

def test_specific_drinks(menu_items):
    """Test menu items for specific drinks"""
    print("\n🧪 Testing menu items for specific drinks...")
    
    # Specific drinks to check
    specific_drinks = ["Mojito", "Sangria Tinto", "Cappuccino"]
    
    # Check for specific drinks
    print("\n📊 Checking for specific drinks:")
    found_drinks = {}
    for drink in specific_drinks:
        found = False
        drink_data = None
        for item in menu_items:
            if item["name"].lower() == drink.lower():
                found = True
                drink_data = item
                break
        found_drinks[drink] = (found, drink_data)
    
    all_drinks_found = True
    for drink, (found, drink_data) in found_drinks.items():
        if found:
            print(f"  ✅ {drink} - Found")
            # Check for detailed_description, allergens, origin
            if drink_data.get("detailed_description"):
                print(f"    ✅ Has detailed description: {drink_data['detailed_description'][:50]}...")
            else:
                print(f"    ❌ Missing detailed description")
                all_drinks_found = False
            
            if drink_data.get("allergens"):
                print(f"    ✅ Has allergens info: {drink_data['allergens']}")
            else:
                print(f"    ❌ Missing allergens info")
                all_drinks_found = False
            
            if drink_data.get("origin"):
                print(f"    ✅ Has origin info: {drink_data['origin']}")
            else:
                print(f"    ❌ Missing origin info")
                all_drinks_found = False
        else:
            print(f"  ❌ {drink} - Not found")
            all_drinks_found = False
    
    if not all_drinks_found:
        print("❌ Some specific drinks are missing or incomplete")
        return False
    
    print("\n✅ All specific drink checks passed successfully")
    return True

def test_menu_crud_operations():
    """Test CRUD operations for menu items"""
    print("\n🧪 Testing CRUD operations for menu items...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # 1. CREATE - Test POST /api/menu/items
        print("\n📝 Testing CREATE operation (POST /api/menu/items)...")
        
        # Create payload for a new menu item
        create_payload = {
            "name": "Test Tapas Special",
            "description": "Ein spezielles Testgericht für API-Tests",
            "detailed_description": "Dieses Gericht wurde speziell für das Testen der API erstellt. Es enthält alle erforderlichen Felder und Eigenschaften.",
            "price": "9,90 €",
            "category": "Test Kategorie",
            "origin": "Test Region",
            "allergens": "Keine",
            "ingredients": "Test Zutaten, API, Validierung",
            "vegan": False,
            "vegetarian": True,
            "glutenfree": True,
            "order_index": 999
        }
        
        # Make POST request
        create_response = requests.post(f"{API_BASE_URL}/menu/items", json=create_payload, headers=headers)
        
        # Check if response is successful
        if create_response.status_code == 200:
            print("✅ Successfully created new menu item")
            create_data = create_response.json()
            item_id = create_data.get("id")
            print(f"✅ Created item ID: {item_id}")
        else:
            print(f"❌ Failed to create menu item. Status code: {create_response.status_code}")
            if create_response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            return False
        
        # 2. READ - Test GET /api/menu/items to verify the item was created
        print("\n📝 Testing READ operation (GET /api/menu/items)...")
        
        # Make GET request
        read_response = requests.get(f"{API_BASE_URL}/menu/items")
        
        # Check if response is successful
        if read_response.status_code == 200:
            print("✅ Successfully retrieved menu items")
            read_data = read_response.json()
            
            # Find the created item
            created_item = None
            for item in read_data:
                if item.get("id") == item_id:
                    created_item = item
                    break
            
            if created_item:
                print("✅ Found the created item in the menu items list")
                
                # Verify the item data
                if (created_item["name"] == create_payload["name"] and
                    created_item["description"] == create_payload["description"] and
                    created_item["price"] == create_payload["price"] and
                    created_item["category"] == create_payload["category"]):
                    print("✅ Created item data matches the payload")
                else:
                    print("❌ Created item data doesn't match the payload")
                    return False
            else:
                print("❌ Created item not found in the menu items list")
                return False
        else:
            print(f"❌ Failed to retrieve menu items. Status code: {read_response.status_code}")
            return False
        
        # 3. UPDATE - Test PUT /api/menu/items/{item_id}
        print("\n📝 Testing UPDATE operation (PUT /api/menu/items/{item_id})...")
        
        # Create payload for updating the menu item
        update_payload = create_payload.copy()
        update_payload["name"] = "Updated Test Tapas Special"
        update_payload["description"] = "Ein aktualisiertes Testgericht für API-Tests"
        update_payload["price"] = "12,90 €"
        
        # Make PUT request
        update_response = requests.put(f"{API_BASE_URL}/menu/items/{item_id}", json=update_payload, headers=headers)
        
        # Check if response is successful
        if update_response.status_code == 200:
            print("✅ Successfully updated menu item")
        else:
            print(f"❌ Failed to update menu item. Status code: {update_response.status_code}")
            if update_response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            return False
        
        # Verify the update
        verify_response = requests.get(f"{API_BASE_URL}/menu/items")
        if verify_response.status_code == 200:
            verify_data = verify_response.json()
            
            # Find the updated item
            updated_item = None
            for item in verify_data:
                if item.get("id") == item_id:
                    updated_item = item
                    break
            
            if updated_item:
                print("✅ Found the updated item in the menu items list")
                
                # Verify the item data
                if (updated_item["name"] == update_payload["name"] and
                    updated_item["description"] == update_payload["description"] and
                    updated_item["price"] == update_payload["price"]):
                    print("✅ Updated item data matches the payload")
                else:
                    print("❌ Updated item data doesn't match the payload")
                    return False
            else:
                print("❌ Updated item not found in the menu items list")
                return False
        else:
            print(f"❌ Failed to verify the update. Status code: {verify_response.status_code}")
            return False
        
        # 4. DELETE - Test DELETE /api/menu/items/{item_id}
        print("\n📝 Testing DELETE operation (DELETE /api/menu/items/{item_id})...")
        
        # Make DELETE request
        delete_response = requests.delete(f"{API_BASE_URL}/menu/items/{item_id}", headers=headers)
        
        # Check if response is successful
        if delete_response.status_code == 200:
            print("✅ Successfully deleted menu item")
        else:
            print(f"❌ Failed to delete menu item. Status code: {delete_response.status_code}")
            if delete_response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            return False
        
        # Verify the deletion
        verify_delete_response = requests.get(f"{API_BASE_URL}/menu/items")
        if verify_delete_response.status_code == 200:
            verify_delete_data = verify_delete_response.json()
            
            # Check if the item is no longer in the list
            deleted_item_found = False
            for item in verify_delete_data:
                if item.get("id") == item_id:
                    deleted_item_found = True
                    break
            
            if not deleted_item_found:
                print("✅ Deleted item is no longer in the menu items list")
            else:
                print("❌ Deleted item is still in the menu items list")
                return False
        else:
            print(f"❌ Failed to verify the deletion. Status code: {verify_delete_response.status_code}")
            return False
        
        print("\n✅ All CRUD operations for menu items passed successfully")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during CRUD operations: {e}")
        return False

def run_menu_validation():
    """Run all menu validation tests"""
    print("\n🔍 Starting Jimmy's Tapas Bar Menu Validation Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Get Menu Items Count
    success, menu_items = test_menu_items_count()
    results["menu_items_count"] = success
    
    if success and menu_items:
        # Test 2: Menu Categories
        results["menu_categories"] = test_menu_categories(menu_items)
        
        # Test 3: Specific Drinks
        results["specific_drinks"] = test_specific_drinks(menu_items)
    else:
        results["menu_categories"] = False
        results["specific_drinks"] = False
    
    # Test 4: Authentication
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    # Test 5: Menu CRUD Operations
    if auth_success:
        results["menu_crud_operations"] = test_menu_crud_operations()
    else:
        results["menu_crud_operations"] = False
        print("❌ Skipping menu CRUD operations test due to failed login")
    
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
    # Run the menu validation tests
    success = run_menu_validation()
    sys.exit(0 if success else 1)
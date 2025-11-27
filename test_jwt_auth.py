#!/usr/bin/env python3
"""
Test script to verify JWT authentication endpoints
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test user registration"""
    print("🧪 Testing User Registration...")
    
    url = f"{BASE_URL}/api/frontend/register/"
    data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration successful!")
            print(f"User ID: {result['user']['id']}")
            print(f"Username: {result['user']['username']}")
            print(f"Email: {result['user']['email']}")
            print(f"Access Token: {result['access_token'][:50]}...")
            print(f"Refresh Token: {result['refresh_token'][:50]}...")
            return result
        else:
            print("❌ Registration failed!")
            print(f"Error: {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_login():
    """Test user login with demo credentials"""
    print("\n🧪 Testing User Login...")
    
    url = f"{BASE_URL}/api/frontend/login/"
    data = {
        "username": "Rehaan",
        "password": "Rehaan@123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"User ID: {result['user']['id']}")
            print(f"Username: {result['user']['username']}")
            print(f"Email: {result['user']['email']}")
            print(f"Access Token: {result['access_token'][:50]}...")
            print(f"Refresh Token: {result['refresh_token'][:50]}...")
            return result
        else:
            print("❌ Login failed!")
            print(f"Error: {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_token_verification(access_token):
    """Test token verification"""
    print("\n🧪 Testing Token Verification...")
    
    url = f"{BASE_URL}/api/frontend/verify-token/"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Token verification successful!")
            print(f"Valid: {result['valid']}")
            print(f"User: {result['user']}")
            return True
        else:
            print("❌ Token verification failed!")
            print(f"Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Token verification error: {e}")
        return False

def test_token_refresh(refresh_token):
    """Test token refresh"""
    print("\n🧪 Testing Token Refresh...")
    
    url = f"{BASE_URL}/api/frontend/refresh-token/"
    data = {"refresh_token": refresh_token}
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Token refresh successful!")
            print(f"New Access Token: {result['access_token'][:50]}...")
            print(f"New Refresh Token: {result['refresh_token'][:50]}...")
            return result
        else:
            print("❌ Token refresh failed!")
            print(f"Error: {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Token refresh error: {e}")
        return None

def test_protected_endpoint(access_token):
    """Test accessing a protected endpoint"""
    print("\n🧪 Testing Protected Endpoint Access...")
    
    url = f"{BASE_URL}/api/frontend/verify-token/"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Protected endpoint access successful!")
            return True
        else:
            print("❌ Protected endpoint access failed!")
            print(f"Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False

def test_logout(refresh_token, access_token):
    """Test user logout"""
    print("\n🧪 Testing User Logout...")
    
    url = f"{BASE_URL}/api/frontend/logout/"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"refresh_token": refresh_token}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Logout successful!")
            print(f"Message: {result['message']}")
            return True
        else:
            print("❌ Logout failed!")
            print(f"Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return False

def main():
    """Run all JWT authentication tests"""
    print("🚀 Starting JWT Authentication Tests")
    print("=" * 50)
    
    # Test 1: Login with demo credentials
    login_result = test_login()
    if not login_result:
        print("❌ Login test failed. Cannot proceed with other tests.")
        return
    
    access_token = login_result['access_token']
    refresh_token = login_result['refresh_token']
    
    # Test 2: Verify token
    test_token_verification(access_token)
    
    # Test 3: Access protected endpoint
    test_protected_endpoint(access_token)
    
    # Test 4: Refresh token
    refresh_result = test_token_refresh(refresh_token)
    if refresh_result:
        new_access_token = refresh_result['access_token']
        new_refresh_token = refresh_result['refresh_token']
        
        # Test 5: Verify new token
        test_token_verification(new_access_token)
        
        # Test 6: Logout
        test_logout(new_refresh_token, new_access_token)
    
    # Test 7: Registration (optional - creates new user)
    print("\n" + "=" * 50)
    print("🧪 Testing Registration (creates new user)...")
    test_registration()
    
    print("\n" + "=" * 50)
    print("🎉 JWT Authentication Tests Complete!")

if __name__ == "__main__":
    main()

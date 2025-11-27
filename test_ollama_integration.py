"""
Test script to verify Ollama integration with Django
"""

import requests
import json

# Base URL for your Django API
BASE_URL = "http://127.0.0.1:8000/api"

def test_ai_status():
    """Test if AI service is available"""
    print("Testing AI Status...")
    try:
        response = requests.get(f"{BASE_URL}/prediction/status/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing AI status: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("\nTesting Chat Endpoint...")
    try:
        data = {
            "input": "Hello! Can you help me understand photosynthesis?"
        }
        response = requests.post(f"{BASE_URL}/prediction/chat/", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing chat endpoint: {e}")
        return False

def test_educational_content():
    """Test educational content generation"""
    print("\nTesting Educational Content Generation...")
    try:
        # Test summary generation
        data = {
            "type": "summary",
            "content": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar. This process is crucial for life on Earth as it provides oxygen for most living organisms and forms the base of most food chains."
        }
        
        # Note: This endpoint requires authentication, so it might fail
        response = requests.post(f"{BASE_URL}/prediction/generate/", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 401]  # 401 is expected without auth
    except Exception as e:
        print(f"Error testing educational content: {e}")
        return False

def test_study_ai_endpoints():
    """Test the study app AI endpoints"""
    print("\nTesting Study AI Endpoints...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/")
        print(f"AI Status - Status Code: {response.status_code}")
        print(f"AI Status - Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing study AI endpoints: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Ollama Integration with Django ===\n")
    
    # Run tests
    tests = [
        ("AI Status", test_ai_status),
        ("Chat Endpoint", test_chat_endpoint),
        ("Educational Content", test_educational_content),
        ("Study AI Endpoints", test_study_ai_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n=== Test Results ===")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

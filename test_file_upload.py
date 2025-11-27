"""
Test script for file upload processing functionality
"""

import requests
import json
import os

# Base URL for your Django API
BASE_URL = "http://127.0.0.1:8000/api"

def test_file_upload_processing():
    """Test file upload and processing functionality"""
    print("=== Testing File Upload Processing ===\n")
    
    # Test 1: Check AI status
    print("1. Testing AI Status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ AI Service Available: {response.json()}")
        else:
            print(f"❌ AI Service Issue: {response.json()}")
    except Exception as e:
        print(f"❌ Error testing AI status: {e}")
    
    # Test 2: Test file processors directly
    print("\n2. Testing File Processors...")
    try:
        import sys
        sys.path.append('backend')
        from study.file_processors import extract_text_from_file, get_file_type, validate_file_type
        
        # Create a test text file
        test_content = """
        This is a test document about photosynthesis.
        
        Photosynthesis is the process by which plants convert sunlight into energy.
        It involves chlorophyll, carbon dioxide, and water.
        The main products are glucose and oxygen.
        
        Key stages:
        1. Light-dependent reactions
        2. Calvin cycle
        3. Sugar production
        """
        
        with open('test_document.txt', 'w') as f:
            f.write(test_content)
        
        # Test text extraction
        extracted_text = extract_text_from_file('test_document.txt')
        file_type = get_file_type('test_document.txt')
        is_valid = validate_file_type('test_document.txt')
        
        print(f"✅ Text extracted: {len(extracted_text)} characters")
        print(f"✅ File type: {file_type}")
        print(f"✅ Valid file: {is_valid}")
        print(f"Content preview: {extracted_text[:100]}...")
        
        # Clean up
        os.remove('test_document.txt')
        
    except Exception as e:
        print(f"❌ Error testing file processors: {e}")
    
    # Test 3: Test document-based AI endpoints (requires authentication)
    print("\n3. Testing Document-based AI Endpoints...")
    print("Note: These endpoints require authentication, so they may return 401 errors")
    
    try:
        # Test study plan from documents
        data = {"days": 5, "material_ids": []}
        response = requests.post(f"{BASE_URL}/ai/study-plan-from-docs/", json=data)
        print(f"Study Plan from Docs - Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Authentication required (expected)")
        else:
            print(f"Response: {response.json()}")
        
        # Test quiz from documents
        data = {"num_questions": 3, "material_ids": []}
        response = requests.post(f"{BASE_URL}/ai/quiz-from-docs/", json=data)
        print(f"Quiz from Docs - Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Authentication required (expected)")
        else:
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error testing document-based endpoints: {e}")
    
    print("\n=== File Upload Processing Test Complete ===")
    print("\nNext steps to test with actual files:")
    print("1. Start Django server: python backend/manage.py runserver")
    print("2. Use a tool like Postman or create a frontend to upload PDF/DOCX files")
    print("3. Upload files to: POST /api/materials/ (with authentication)")
    print("4. Check that content, file_type, and summary fields are populated")
    print("5. Use the new endpoints to generate study plans and quizzes from uploaded documents")

if __name__ == "__main__":
    test_file_upload_processing()

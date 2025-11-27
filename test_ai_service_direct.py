"""
Direct test of the AI service without Django
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from ai_service import ollama_service

def test_ollama_connection():
    """Test direct connection to Ollama"""
    print("Testing Ollama Service Connection...")
    
    # Test if service is available
    is_available = ollama_service.is_available()
    print(f"Ollama Available: {is_available}")
    print(f"Model: {ollama_service.model}")
    
    if not is_available:
        print("❌ Ollama service is not available. Make sure Ollama is running.")
        return False
    
    # Test text generation
    try:
        print("\nTesting text generation...")
        response = ollama_service.generate_text(
            "Explain photosynthesis in simple terms for a student.",
            "You are a helpful educational AI assistant."
        )
        print(f"✅ Text generation successful!")
        print(f"Response: {response[:200]}...")
        
        # Test summarization
        print("\nTesting summarization...")
        text_to_summarize = """
        Photosynthesis is a process used by plants and other organisms to convert light energy 
        into chemical energy that, through cellular respiration, can later be released to fuel 
        the organism's activities. This chemical energy is stored in carbohydrate molecules, 
        such as sugars and starches, which are synthesized from carbon dioxide and water. 
        In most cases, oxygen is also released as a waste product. Most plants, algae, and 
        cyanobacteria perform photosynthesis; such organisms are called photoautotrophs.
        """
        
        summary = ollama_service.summarize_text(text_to_summarize)
        print(f"✅ Summarization successful!")
        print(f"Summary: {summary[:200]}...")
        
        # Test quiz generation
        print("\nTesting quiz generation...")
        quiz = ollama_service.generate_quiz_questions("Photosynthesis", 2)
        print(f"✅ Quiz generation successful!")
        print(f"Generated {len(quiz)} questions")
        
        # Test study plan generation
        print("\nTesting study plan generation...")
        study_plan = ollama_service.generate_study_plan(["Photosynthesis", "Cell Biology"], 3)
        print(f"✅ Study plan generation successful!")
        print(f"Study plan type: {type(study_plan)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    print("=== Direct AI Service Test ===\n")
    success = test_ollama_connection()
    
    if success:
        print("\n🎉 All tests passed! Ollama integration is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check your Ollama setup.")

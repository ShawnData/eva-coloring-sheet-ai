#!/usr/bin/env python3
"""
Test script to verify core functionality of the coloring sheet AI
"""

import os
from dotenv import load_dotenv
from src.crews.coloring_sheet_crew import ColoringSheetCrew

def test_voice_processing():
    """Test the voice processing functionality"""
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is not set")
        return False
    
    print("✅ OpenAI API key found")
    
    # Create the crew
    try:
        crew = ColoringSheetCrew()
        print("✅ Crew created successfully")
    except Exception as e:
        print(f"❌ Failed to create crew: {e}")
        return False
    
    # Test cases
    test_cases = [
        "I want a cat coloring sheet",
        "Hello",
        "Can you make me a dog picture to color?",
        "What's the weather like?"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: '{test_input}' ---")
        
        try:
            result = crew.process_voice_input(test_input)
            print(f"✅ Processing successful")
            print(f"   Message: {result.get('message', 'No message')}")
            print(f"   Image URL: {result.get('image_url', 'None')}")
            
            if result.get('image_url'):
                print(f"   ✅ Image generation successful")
            else:
                print(f"   ℹ️  No image generated (expected for non-coloring requests)")
                
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return False
    
    print("\n🎉 All tests passed!")
    return True

if __name__ == "__main__":
    success = test_voice_processing()
    if success:
        print("\n✅ Core functionality is working correctly!")
    else:
        print("\n❌ Core functionality has issues that need to be fixed.") 
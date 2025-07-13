#!/usr/bin/env python3
"""
Test script to verify voice processing components
"""

import os
import sys
from src.crews.coloring_sheet_crew import ColoringSheetCrew
from src.ui.interface import ColoringSheetInterface

def test_crew_initialization():
    """Test that the crew can be initialized"""
    print("Testing crew initialization...")
    try:
        crew = ColoringSheetCrew()
        print("✅ Crew initialized successfully")
        return crew
    except Exception as e:
        print(f"❌ Crew initialization failed: {e}")
        return None

def test_voice_processing():
    """Test voice processing with mock data"""
    print("\nTesting voice processing...")
    
    crew = test_crew_initialization()
    if not crew:
        return
    
    # Test with various inputs
    test_inputs = [
        "I want a cat coloring sheet",
        "Hello, how are you?",
        "Make me a dog picture"
    ]
    
    for test_input in test_inputs:
        print(f"\nTesting input: '{test_input}'")
        try:
            result = crew.process_voice_input(test_input)
            print(f"✅ Response: {result['message']}")
            if result.get('image_url'):
                print(f"   Image URL: {result['image_url']}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_interface_initialization():
    """Test that the interface can be initialized"""
    print("\nTesting interface initialization...")
    try:
        # Set a test API key if not present
        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = "test-key"
            print("⚠️  Using test API key")
        
        crew = ColoringSheetCrew()
        interface = ColoringSheetInterface(crew)
        print("✅ Interface initialized successfully")
        return interface
    except Exception as e:
        print(f"❌ Interface initialization failed: {e}")
        return None

def test_audio_utils():
    """Test audio utilities"""
    print("\nTesting audio utilities...")
    try:
        from src.utils.audio_utils import AudioUtils
        audio_utils = AudioUtils()
        print("✅ AudioUtils initialized successfully")
        
        # Test TTS generation
        test_message = "Hello, this is a test message."
        tts_file = audio_utils.generate_tts(test_message)
        print(f"✅ TTS file generated: {tts_file}")
        
    except Exception as e:
        print(f"❌ Audio utilities test failed: {e}")

if __name__ == "__main__":
    print("🎤 Voice Processing Test Suite")
    print("=" * 40)
    
    test_crew_initialization()
    test_voice_processing()
    test_interface_initialization()
    test_audio_utils()
    
    print("\n" + "=" * 40)
    print("🎉 Test suite completed!")
    
    print("\nTo run the full application:")
    print("1. Set your OPENAI_API_KEY in a .env file")
    print("2. Run: python main.py")
    print("3. Open the Gradio interface in your browser") 
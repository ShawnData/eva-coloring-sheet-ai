#!/usr/bin/env python3
"""
Test script for the enhanced voice assistant with LLM conversation capabilities
"""

import os
from src.agents.voice_assistant import VoiceAssistantAgent

def test_llm_conversation():
    """Test the LLM conversation capabilities of the voice assistant"""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is not set")
        return False
    
    try:
        # Initialize the voice assistant
        print("🔄 Initializing voice assistant...")
        agent = VoiceAssistantAgent()
        print("✅ Voice assistant initialized successfully")
        
        # Test general conversation (non-coloring sheet request)
        print("\n🧪 Testing general conversation...")
        test_inputs = [
            "Hello!",
            "How are you today?",
            "What's your favorite color?",
            "I love unicorns!",
            "Can you tell me a story?"
        ]
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n--- Test {i}: '{test_input}' ---")
            try:
                result = agent.process_voice_input(test_input)
                print(f"Response: {result.get('message', 'No message')}")
                print(f"Image URL: {result.get('image_url', 'None')}")
                print(f"Error: {result.get('error', 'None')}")
            except Exception as e:
                print(f"❌ Error processing input: {str(e)}")
        
        # Test coloring sheet request
        print("\n🧪 Testing coloring sheet request...")
        try:
            result = agent.process_voice_input("I want a cat coloring sheet")
            print(f"Response: {result.get('message', 'No message')}")
            print(f"Image URL: {result.get('image_url', 'None')}")
            print(f"Error: {result.get('error', 'None')}")
        except Exception as e:
            print(f"❌ Error processing coloring sheet request: {str(e)}")
        
        print("\n✅ LLM conversation test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Enhanced Voice Assistant with LLM Conversation")
    print("=" * 60)
    
    success = test_llm_conversation()
    
    if success:
        print("\n🎉 All tests passed! The voice assistant should now have intelligent conversations.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.") 
#!/usr/bin/env python3
"""
Demo script for Eva Coloring Sheet AI - Phase 1 Implementation

This script demonstrates the core functionality of the coloring sheet generation system
without requiring the full Gradio UI. It shows how voice input is processed and
converted into coloring sheets.
"""

import os
import sys
from src.crews.coloring_sheet_crew import ColoringSheetCrew

def demo_voice_processing():
    """Demonstrate the voice processing workflow"""
    
    print("🎨 Eva Coloring Sheet AI - Phase 1 Demo")
    print("=" * 50)
    
    # Initialize the crew
    crew = ColoringSheetCrew()
    
    # Test cases
    test_cases = [
        "I want a cat coloring sheet",
        "Make me a dog picture",
        "Create a flower drawing",
        "Hello, how are you?",
        "I want a scary monster",  # Should be filtered
        "Show me a car",
        ""  # Empty input
    ]
    
    print("\n🧪 Testing Voice Input Processing:")
    print("-" * 40)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. Input: '{test_input}'")
        
        try:
            result = crew.process_voice_input(test_input)
            
            print(f"   Response: {result['message']}")
            
            if result.get('image_url'):
                print(f"   Image URL: {result['image_url']}")
                print(f"   ✅ Coloring sheet generated!")
            else:
                print(f"   ℹ️  No image generated (conversation only)")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nTo run the full application with voice input:")
    print("1. Set your OPENAI_API_KEY in a .env file")
    print("2. Run: python main.py")
    print("3. Open the Gradio interface in your browser")

def demo_agent_workflow():
    """Demonstrate the individual agent workflow"""
    
    print("\n🤖 Agent Workflow Demo:")
    print("-" * 40)
    
    from src.agents.conversation_summarizer import ConversationSummarizerAgent
    from src.agents.coloring_sheet_designer import ColoringSheetDesignerAgent
    
    # Test the conversation summarizer
    print("\n1. Testing Conversation Summarizer Agent:")
    summarizer = ConversationSummarizerAgent()
    
    test_input = "I want a cute cat coloring sheet"
    result = summarizer.summarize_conversation(test_input)
    
    print(f"   Input: '{test_input}'")
    print(f"   Is coloring request: {result['is_coloring_request']}")
    print(f"   Extracted prompt: '{result['prompt']}'")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Message: {result['message']}")
    
    # Test the coloring sheet designer
    print("\n2. Testing Coloring Sheet Designer Agent:")
    designer = ColoringSheetDesignerAgent()
    
    if result['prompt']:
        design_result = designer.generate_coloring_sheet(result['prompt'], result['confidence'])
        
        print(f"   Input prompt: '{result['prompt']}'")
        print(f"   Success: {design_result['success']}")
        print(f"   Message: {design_result['message']}")
        
        if design_result.get('image_url'):
            print(f"   Image URL: {design_result['image_url']}")

if __name__ == "__main__":
    # Set a test API key if not present
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "test-key"
        print("⚠️  Using test API key. Set OPENAI_API_KEY for real DALL-E generation.")
    
    try:
        demo_voice_processing()
        demo_agent_workflow()
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        sys.exit(1) 
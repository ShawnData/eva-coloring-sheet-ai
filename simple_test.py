#!/usr/bin/env python3
"""
Simple test to verify Gradio interface works
"""

import os
import gradio as gr
from src.crews.coloring_sheet_crew import ColoringSheetCrew

def simple_voice_handler(audio):
    """Simple voice handler for testing"""
    if audio is None:
        return "No audio detected", None
    
    # For testing, just return a simple response
    return "I heard your voice! This is a test response.", None

def create_simple_interface():
    """Create a simple Gradio interface for testing"""
    
    with gr.Blocks(title="Simple Voice Test") as interface:
        gr.Markdown("# Simple Voice Test")
        gr.Markdown("Test voice input functionality")
        
        with gr.Row():
            audio_input = gr.Audio(
                type="numpy",
                streaming=False,
                label="Voice Input",
                sources=["microphone"],
                interactive=True
            )
            
            text_output = gr.Textbox(label="Response")
            image_output = gr.Image(label="Image")
        
        audio_input.change(
            simple_voice_handler,
            inputs=[audio_input],
            outputs=[text_output, image_output]
        )
    
    return interface

if __name__ == "__main__":
    # Set test API key
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "test-key"
    
    print("🚀 Launching simple Gradio interface...")
    print("This will test basic voice input functionality")
    print("Open your browser to the URL shown below")
    
    interface = create_simple_interface()
    interface.launch(share=False, debug=True) 
#!/usr/bin/env python
import sys
import warnings
import speech_recognition as sr
import pyttsx3
from datetime import datetime

from eva_coloring_sheet_agent.crew import EvaColoringSheetAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def speak(text):
    """
    Convert text to speech using default system voice.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_voice_input():
    """
    Get voice input from microphone and convert to text.
    """
    recognizer = sr.Recognizer()
    
    speak("Please speak your subject for the coloring page")
    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                # Listen for audio input
                speak("Listening")
                audio = recognizer.listen(source, timeout=5)
                speak("Processing speech")
            
                # Convert speech to text
                subject = recognizer.recognize_google(audio)
                speak(f"You said: {subject}")
                response = input("Is this correct? (yes/no): ").lower()
                if response in ['yes', 'y']:
                    speak("Great! Let's create your coloring page")
                    return subject
                speak("Let's try again")
                continue
                
            except sr.WaitTimeoutError:
                speak("No speech detected within timeout period. Please try again")
                continue
            except sr.UnknownValueError:
                speak("Could not understand audio. Please try again")
                continue
            except sr.RequestError as e:
                speak(f"Could not request results: {str(e)}")
                return None
            except Exception as e:
                speak(f"An error occurred: {str(e)}")
                return None

def run():
    """
    Run the crew.
    """
    # Get subject from voice input
    subject = get_voice_input()
    if not subject:
        return None
    
    inputs = {
        'eva_age': '6',
        'subject': subject
    }
    
    try:
        EvaColoringSheetAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        speak(f"An error occurred while running the crew: {str(e)}")
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        EvaColoringSheetAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EvaColoringSheetAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        EvaColoringSheetAgent().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

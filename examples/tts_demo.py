"""
Interactive demo for testing the Text-to-Speech functionality.

This script demonstrates:
1. Prompting user for text input
2. Generating audio from the text
3. Playing back the generated audio
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tts.core import TextToSpeech

def main():
    """Main function to run the TTS demo."""
    print("Text-to-Speech Demo")
    print("Enter 'q' to quit")
    
    tts = TextToSpeech()
    if not tts.initialize_model():
        print("Failed to initialize TTS engine")
        sys.exit(1)
        
    while True:
        try:
            text = input("\nEnter text to convert to speech: ")
            if text.lower() == 'q':
                break
                
            if not text.strip():
                print("Error: Please enter some text")
                continue
                
            print("Generating audio...")
            try:
                tts.model.say(text)
                tts.model.runAndWait()
                print("Audio played successfully!")
            except Exception as e:
                print(f"Failed to generate audio: {str(e)}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
"""
Text-to-Speech Example Script

This script demonstrates basic usage of the TextToSpeech class from the tts module.
It follows the implementation steps from the specification document.
"""

import os
from tts import TextToSpeech

# Initialize the TTS system
tts = TextToSpeech()

# Example text to convert
example_text = "Hello, this is a test of the text-to-speech system."

# Output path for the generated audio
output_file = os.path.join(os.path.dirname(__file__), "output.wav")

# Step 1: Initialize the model (happens automatically when needed)
# Step 2 & 3: Process text and generate audio
success = tts.text_to_speech(example_text, output_file)

if success:
    print(f"Successfully generated audio file at: {output_file}")
else:
    print("Failed to generate audio file")
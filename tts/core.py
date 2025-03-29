"""
Core Text-to-Speech implementation for AI Voice Assistant.

This module contains the main TextToSpeech class that handles:
1. TTS model initialization
2. Text processing pipeline
3. Audio file generation
4. Error handling
"""

import os
import logging
from typing import Optional
import pyttsx3

class TextToSpeech:
    """
    Main class for text-to-speech conversion using Coqui XTTS v2.
    
    Attributes:
        model: The loaded TTS model
        logger: Logger instance for error tracking
    """
    
    def __init__(self):
        """Initialize the TTS system with default settings."""
        self.logger = logging.getLogger(__name__)
        self.model = None
        
    def initialize_model(self):
        """
        Load and initialize the pyttsx3 TTS engine.
        
        Returns:
            bool: True if initialization succeeded, False otherwise
        """
        try:
            self.model = pyttsx3.init()
            self.logger.info("TTS engine initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS engine: {str(e)}")
            return False
        
    def process_text(self, text: str) -> Optional[str]:
        """
        Process input text for TTS conversion (step 2).
        
        Args:
            text: Input text to process
            
        Returns:
            Processed text or None if invalid
        """
        if not text or not isinstance(text, str):
            self.logger.error("Invalid input text")
            return None
            
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = ''.join(char for char in text if char.isalnum() or char == ' ')
        return text.strip()
        
    def generate_audio(self, text: str, output_path: str = None) -> bool:
        """
        Generate WAV audio from text (step 3).
        
        Args:
            text: Processed text to convert
            output_path: Optional path to save the WAV file. If None, will generate
                        a timestamp-based filename in current directory
            
        Returns:
            True if successful, False otherwise
        """
        processed_text = self.process_text(text)
        if not processed_text:
            return False
            
        try:
            if output_path is None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"tts_output_{timestamp}.wav"
                
            if not self.model:
                if not self.initialize_model():
                    return False
                
            # Set properties before saving
            self.model.setProperty('rate', 150)  # Speed of speech
            self.model.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
            
            self.model.save_to_file(processed_text, output_path)
            self.model.runAndWait()
            
            if output_path is None:
                return True
            if os.path.exists(output_path):
                return True
            self.logger.error(f"Failed to create output file: {output_path}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to generate audio: {str(e)}")
            return False
        
    def text_to_speech(self, text: str, output_path: str) -> bool:
        """
        Complete text-to-speech pipeline with error handling (step 4).
        
        Combines all steps from the specification:
        1. Model initialization
        2. Text processing
        3. Audio generation
        4. Error handling
        
        Args:
            text: Input text to convert
            output_path: Where to save the WAV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.model:
                self.initialize_model()
                
            return self.generate_audio(text, output_path)
            
        except Exception as e:
            self.logger.error(f"TTS conversion failed: {str(e)}")
            return False
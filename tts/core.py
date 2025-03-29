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
import wave
from typing import Optional
from TTS.api import TTS
import torch

class TextToSpeech:
    """
    Main class for text-to-speech conversion using Coqui TTS (XTTS models).
    Handles model loading, audio generation, and voice cloning.

    Attributes:
        model: The loaded Coqui TTS model instance.
        logger: Logger instance for error tracking.
        device: The computing device ('cuda' or 'cpu') used by the model.
    """
    
    def __init__(self):
        """Initialize the TTS system."""
        self.logger = logging.getLogger(__name__)
        self.model: Optional[TTS] = None # Type hint for clarity
        self.device: Optional[str] = None
        
    def initialize_model(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2") -> bool:
        """
        Load and initialize the Coqui TTS model.

        Args:
            model_name (str): The name of the XTTS model to load.

        Returns:
            bool: True if initialization succeeded, False otherwise.
        """
        try:
            if self.model is not None:
                self.logger.info("TTS model already initialized.")
                return True

            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.logger.info(f"Initializing Coqui TTS model '{model_name}' on device: {self.device}")
            
            # Note: The model files will be downloaded on first run if not cached
            self.model = TTS(model_name=model_name, progress_bar=True).to(self.device)
            
            self.logger.info("Coqui TTS model initialized successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Coqui TTS model: {str(e)}", exc_info=True)
            self.model = None
            self.device = None
            return False
        
    def generate_audio(self, text: str, speaker_wav: str, language: str, output_path: str) -> bool:
        """
        Generate WAV audio from text using the specified speaker voice.

        Args:
            text (str): Text to convert to speech.
            speaker_wav (str): Path to the reference audio file (.wav) for voice cloning.
            language (str): Language code for the text (e.g., 'en').
            output_path (str): Path to save the generated WAV file.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.model:
            self.logger.error("TTS model not initialized. Call initialize_model() first.")
            return False
            
        # Validate speaker_wav exists before passing to the model
        if not os.path.exists(speaker_wav):
             self.logger.error(f"Reference speaker WAV file not found: {speaker_wav}")
             return False

        try:
            self.logger.info(f"Generating audio for text: '{text[:50]}...'")
            self.logger.info(f"Using speaker reference: {speaker_wav}")
            self.logger.info(f"Language: {language}")
            self.logger.info(f"Output path: {output_path}")

            # Use tts_to_file for synthesis
            self.model.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=output_path
            )
            
            if os.path.exists(output_path):
                self.logger.info(f"Successfully generated audio file: {output_path}")
                return True
            else:
                # This case might not be reached if tts_to_file raises an error on failure
                self.logger.error(f"Failed to create output file: {output_path}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to generate audio: {str(e)}", exc_info=True)
            return False
        
    def text_to_speech(self, text: str, speaker_wav: str, language: str, output_path: str) -> bool:
        """
        Complete text-to-speech pipeline using Coqui TTS for voice cloning.

        Args:
            text (str): Input text to convert.
            speaker_wav (str): Path to the reference audio file (.wav).
            language (str): Language code (e.g., 'en').
            output_path (str): Where to save the generated WAV file.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize model if it hasn't been already
            if not self.model:
                if not self.initialize_model():
                    # Initialization failed, error logged in initialize_model
                    return False
                
            # Proceed with generation
            return self.generate_audio(
                text=text, 
                speaker_wav=speaker_wav, 
                language=language, 
                output_path=output_path
            )
            
        except Exception as e:
            # Catch any unexpected errors during the process
            self.logger.error(f"TTS conversion failed: {str(e)}", exc_info=True)
            return False

def validate_voice_sample(file_path: str) -> None:
    """
    Validate a voice sample file meets basic requirements. 
    NOTE: XTTS typically needs at least 3-6 seconds of clear audio.

    Args:
        file_path: Path to the voice sample file (.wav)
        
    Raises:
        ValueError: If the file is invalid (not found, not WAV, empty, too short).
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
        
    if not file_path.lower().endswith('.wav'):
        raise ValueError("Only WAV files are supported")
        
    try:
        with wave.open(file_path, 'rb') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            
            if frames == 0 or rate == 0:
                raise ValueError("Empty or invalid WAV file properties")
                
            duration = frames / float(rate)
            # Keep minimum 1 second for basic check, but XTTS prefers longer. Add comment.
            min_duration = 1.0 # XTTS generally prefers >= 3 seconds
            if duration < min_duration:  
                raise ValueError(f"Audio sample too short ({duration:.1f}s). Minimum required: {min_duration}s (XTTS prefers >= 3s)")
                
            # Add a check for sample rate if possible (XTTS works best with 24kHz or 16kHz)
            # This basic check might not be sufficient for all cases.
            if rate < 16000:
                 self.logger.warning(f"Sample rate ({rate}Hz) is lower than typically recommended for XTTS (>= 16kHz).")

    except EOFError:
        raise ValueError("Empty or corrupted WAV file (EOFError)")
    except wave.Error as e:
        raise ValueError(f"Invalid WAV file: {str(e)}")
    except Exception as e: # Catch other potential issues
        raise ValueError(f"Failed to validate WAV file: {str(e)}")
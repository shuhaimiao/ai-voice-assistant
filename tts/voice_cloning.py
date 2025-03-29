"""
Voice Cloning implementation for AI Voice Assistant.

This module extends the base TextToSpeech class to add voice cloning capabilities.
"""

import os
import logging
import numpy as np
import soundfile as sf
from .core import TextToSpeech

class VoiceCloning(TextToSpeech):
    """
    Provides voice cloning capabilities using Coqui TTS XTTS models.
    Inherits the core TTS functionality and model loading from TextToSpeech.
    """
    
    def __init__(self):
        """Initialize the VoiceCloning system."""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info("VoiceCloning class initialized, using TextToSpeech base for TTS model.")
        
    def validate_voice_sample(self, file_path: str) -> bool:
        """
        Validate a voice sample file meets requirements for XTTS cloning.
        (Checks for existence, duration >= 3s, sample rate >= 16kHz, non-silence)

        Args:
            file_path: Path to audio file to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"Validation Error: File {file_path} does not exist")
                return False

            # Use soundfile to read audio properties
            audio, sample_rate = sf.read(file_path)
            duration = len(audio) / float(sample_rate)
            min_duration = 3.0 # XTTS typically requires at least 3 seconds
            if duration < min_duration:
                self.logger.error(f"Validation Error: Sample too short ({duration:.1f}s), minimum {min_duration} seconds required for XTTS.")
                return False

            min_sample_rate = 16000 # XTTS generally works well with >= 16kHz
            if sample_rate < min_sample_rate:
                self.logger.error(f"Validation Error: Sample rate {sample_rate}Hz is too low, minimum {min_sample_rate}Hz required.")
                return False

            # Check audio is not silent (using numpy)
            max_abs_amp = np.max(np.abs(audio))
            silence_threshold = 0.01
            if max_abs_amp < silence_threshold:
                self.logger.error(f"Validation Error: Audio appears to be silent (max absolute amplitude: {max_abs_amp:.4f}).")
                return False
                
            self.logger.info(f"Voice sample validation passed for: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Voice sample validation failed for {file_path}: {str(e)}", exc_info=True)
            return False
            
    def clone_voice(self, text: str, reference_audio: str, language: str, output_path: str) -> bool:
        """
        Generate speech with cloned voice characteristics using the loaded XTTS model.

        Args:
            text (str): Text to convert to speech.
            reference_audio (str): Path to the reference audio file (.wav) for voice cloning.
            language (str): Language code for the text (e.g., 'en').
            output_path (str): Where to save the generated audio file (.wav).

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.logger.info(f"Attempting voice cloning for text: '{text[:50]}...'")
            # Validate the reference audio file using this class's method
            if not self.validate_voice_sample(reference_audio):
                self.logger.error("Voice cloning failed due to invalid reference audio.")
                return False
                
            # Call the base class's text_to_speech method which handles model initialization and generation
            return super().text_to_speech(
                text=text,
                speaker_wav=reference_audio,
                language=language,
                output_path=output_path
            )
            
        except Exception as e:
            self.logger.error(f"Voice cloning process failed: {str(e)}", exc_info=True)
            return False
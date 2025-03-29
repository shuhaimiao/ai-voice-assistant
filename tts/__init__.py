"""Text-to-Speech (TTS) module for AI Voice Assistant.

This module provides functionality to convert text to speech using Coqui XTTS v2.
"""

from .core import TextToSpeech
from .voice_cloning import VoiceCloning

__all__ = ['TextToSpeech', 'VoiceCloning']
__version__ = '0.1.0'
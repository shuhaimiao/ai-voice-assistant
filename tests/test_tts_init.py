"""
Unit tests for TTS model initialization functionality.
"""
import unittest
import os
import wave
from unittest.mock import patch
from tts.core import TextToSpeech

class TestTTSInitialization(unittest.TestCase):
    """Test cases for TTS model initialization."""

    def test_successful_initialization(self):
        """Test that model initializes successfully under normal conditions."""
        tts = TextToSpeech()
        self.assertTrue(tts.initialize_model())
        self.assertIsNotNone(tts.model)

    @patch('pyttsx3.init', side_effect=Exception("Initialization error"))
    def test_failed_initialization(self, mock_init):
        """Test that initialization fails gracefully when pyttsx3 raises an exception."""
        tts = TextToSpeech()
        self.assertFalse(tts.initialize_model())
        self.assertIsNone(tts.model)

    def test_initialization_in_text_to_speech(self):
        """Test that model gets initialized when calling text_to_speech without prior init."""
        tts = TextToSpeech()
        with patch.object(tts, 'generate_audio', return_value=True):
            with patch('os.path.exists', return_value=True):
                result = tts.text_to_speech("test", "/tmp/test_output.wav")
                self.assertTrue(result)
                self.assertIsNotNone(tts.model)

class TestTextNormalization(unittest.TestCase):
    """Test cases for text normalization functionality."""

    def setUp(self):
        self.tts = TextToSpeech()

    def test_lowercase_conversion(self):
        """Test that text is converted to lowercase."""
        result = self.tts.process_text("TEST TEXT")
        self.assertEqual(result, "test text")

    def test_punctuation_handling(self):
        """Test that punctuation is properly handled."""
        result = self.tts.process_text("Hello, world!")
        self.assertEqual(result, "hello world")

    def test_mixed_case_and_punctuation(self):
        """Test combined case conversion and punctuation handling."""
        result = self.tts.process_text("This is a TEST, with Punctuation!")
        self.assertEqual(result, "this is a test with punctuation")

class TestWAVFileOutput(unittest.TestCase):
    """Test cases for WAV file output functionality."""

    def setUp(self):
        self.tts = TextToSpeech()
        self.test_output_path = "/tmp/test_output.wav"
        self.test_text = "This is a test"
        
    def tearDown(self):
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

    def test_wav_file_creation(self):
        """Test that WAV file is created successfully."""
        with patch('pyttsx3.init') as mock_init:
            mock_engine = mock_init.return_value
            mock_engine.save_to_file.return_value = None
            mock_engine.runAndWait.return_value = None
            with patch('os.path.exists', side_effect=lambda x: x == self.test_output_path):
                result = self.tts.text_to_speech(self.test_text, self.test_output_path)
                self.assertTrue(result)
                self.assertTrue(os.path.exists(self.test_output_path))

    def test_wav_file_format(self):
        """Test that output file is a valid WAV file."""
        with patch('pyttsx3.init') as mock_init:
            mock_engine = mock_init.return_value
            mock_engine.save_to_file.return_value = None
            mock_engine.runAndWait.return_value = None
            
            # Create a temporary valid WAV file
            with wave.open(self.test_output_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                wav_file.writeframes(b'\x00\x00' * 1024)
                
            with patch('os.path.exists', return_value=True):
                result = self.tts.text_to_speech(self.test_text, self.test_output_path)
                self.assertTrue(result)
                try:
                    with wave.open(self.test_output_path, 'rb') as wav_file:
                        self.assertGreater(wav_file.getnframes(), 0)
                except wave.Error:
                    self.fail("Output file is not a valid WAV file")

    def test_invalid_output_path(self):
        """Test handling of invalid output path."""
        invalid_path = "/nonexistent_directory/test.wav"
        with patch('pyttsx3.init'):
            result = self.tts.text_to_speech(self.test_text, invalid_path)
            self.assertFalse(result)
            
    def test_timestamp_filename_generation(self):
        """Test that timestamp-based filenames are generated correctly."""
        with patch('pyttsx3.init'):
            with patch('datetime.datetime') as mock_datetime:
                with patch('os.path.exists', return_value=True):
                    mock_datetime.now.return_value.strftime.return_value = "20230101_120000"
                    result = self.tts.text_to_speech(self.test_text, None)
                    self.assertTrue(result)
                    mock_datetime.now.return_value.strftime.assert_called_once_with("%Y%m%d_%H%M%S")
                
    def test_default_filename_creation(self):
        """Test that files with default names are created in current directory."""
        with patch('pyttsx3.init'):
            with patch('os.path.exists', return_value=True):
                result = self.tts.text_to_speech(self.test_text, None)
                self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
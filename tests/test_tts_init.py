"""
Unit tests for TTS model initialization functionality.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import wave
from tts.core import TextToSpeech

class TestTTSInitialization(unittest.TestCase):
    """Test cases for TextToSpeech initialization logic."""
    
    @patch('tts.core.TTS', side_effect=Exception("Mock TTS initialization error"))
    def test_failed_initialization(self, mock_tts_init):
        """Test that initialization fails gracefully when TTS raises an exception."""
        tts = TextToSpeech()
        self.assertFalse(tts.initialize_model())
        mock_tts_init.assert_called_once()
    
    @patch('tts.core.TTS')
    def test_successful_initialization(self, mock_tts_class):
        """Test that model initializes successfully with default settings."""
        # Set up the mock to return a proper model instance
        mock_model = MagicMock()
        mock_tts_class.return_value = mock_model
        mock_model.to.return_value = mock_model  # Handle the .to(device) call
        
        tts = TextToSpeech()
        self.assertTrue(tts.initialize_model())
        self.assertIsNotNone(tts.model)
        
        # Verify the TTS model was initialized with expected parameters
        mock_tts_class.assert_called_once_with(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
            progress_bar=True
        )
        # Verify .to(device) was called
        mock_model.to.assert_called_once()
    
    @patch('tts.core.TTS')
    def test_initialization_in_text_to_speech(self, mock_tts_class):
        """Test that model gets initialized when calling text_to_speech without prior init."""
        # Set up the mock to return a proper model instance
        mock_model = MagicMock()
        mock_tts_class.return_value = mock_model
        mock_model.to.return_value = mock_model  # Handle the .to(device) call
        
        # Create a temporary file for reference audio
        with tempfile.NamedTemporaryFile(suffix='.wav') as ref_file:
            # Create a simple WAV file
            with wave.open(ref_file.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(b'\0' * 16000 * 5)  # 5 seconds of silence
                
            tts = TextToSpeech()
            # Skip actual audio generation but test initialization flow
            with patch.object(tts, 'generate_audio', return_value=True) as mock_generate:
                result = tts.text_to_speech("test", ref_file.name, "en", "/tmp/test_output.wav")
                # Check that model was initialized
                self.assertIsNotNone(tts.model)
                mock_tts_class.assert_called_once()  # Verify TTS was initialized
                mock_generate.assert_called_once()   # Verify generate_audio was called
                self.assertTrue(result)              # Verify successful result

# Note: TestTextNormalization tests are removed as process_text is no longer needed with XTTS

class TestWAVFileOutput(unittest.TestCase):
    """Test cases for WAV file output functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tts = TextToSpeech()
        
        # Mock TTS initialization
        self.tts_patcher = patch('tts.core.TTS')
        self.mock_tts_class = self.tts_patcher.start()
        mock_model = MagicMock()
        self.mock_tts_class.return_value = mock_model
        mock_model.to.return_value = mock_model
        
        # Ensure model is initialized with mock
        self.tts.initialize_model()
        
        # Patch the generate_audio method to avoid actual synthesis
        self.generate_patcher = patch.object(self.tts, 'generate_audio', return_value=True)
        self.mock_generate = self.generate_patcher.start()
        
        self.test_text = "Hello world"
        self.test_output_path = "/tmp/test_output.wav"
        self.test_ref_path = self.create_temp_ref_file()
        
    def tearDown(self):
        """Tear down test fixtures."""
        self.generate_patcher.stop()
        self.tts_patcher.stop()
        
        # Clean up test files
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)
        if hasattr(self, 'test_ref_path') and os.path.exists(self.test_ref_path):
            os.remove(self.test_ref_path)
            
    def create_temp_ref_file(self):
        """Create a temporary reference audio file for testing."""
        ref_path = "/tmp/test_reference.wav"
        with wave.open(ref_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b'\0' * 16000 * 5)  # 5 seconds of silence
        return ref_path
    
    def test_wav_file_creation(self):
        """Test that the text_to_speech method calls generate_audio with correct params."""
        result = self.tts.text_to_speech(
            self.test_text, 
            self.test_ref_path, 
            "en", 
            self.test_output_path
        )
        self.assertTrue(result)
        # Check that generate_audio was called with the right parameters
        self.mock_generate.assert_called_once_with(
            text=self.test_text,
            speaker_wav=self.test_ref_path,
            language="en",
            output_path=self.test_output_path
        )

    def test_invalid_output_path(self):
        """Test handling of invalid output path by checking generate_audio call."""
        invalid_path = "/nonexistent/directory/output.wav"
        
        # Instead of testing actual file creation (which now happens inside generate_audio),
        # test that text_to_speech correctly passes the path to generate_audio
        result = self.tts.text_to_speech(
            self.test_text, 
            self.test_ref_path, 
            "en", 
            invalid_path
        )
        self.assertTrue(result)  # Mock returns True
        self.mock_generate.assert_called_once_with(
            text=self.test_text,
            speaker_wav=self.test_ref_path,
            language="en",
            output_path=invalid_path
        )

if __name__ == '__main__':
    unittest.main()
# Python Environment Setup Guide

## Prerequisites
- Python 3.11 installed (Required for TTS compatibility - note that Python 3.12+ is NOT compatible with Coqui TTS)
- pip package manager
- venv module (usually included with Python)

## Important Version Compatibility
- The Coqui TTS library requires Python 3.9 to 3.11 (does not work with Python 3.12+)
- Our voice cloning functionality requires Coqui XTTS v2 model which is available through the TTS library

## Setting Up Python 3.11 with pyenv (recommended)
If you have a different Python version installed, we recommend using pyenv to manage multiple Python versions:

1. Install pyenv (if not already installed):
   ```bash
   # macOS with Homebrew
   brew install pyenv
   ```

2. Install Python 3.11.9:
   ```bash
   pyenv install 3.11.9
   ```

3. Set Python 3.11.9 for this project:
   ```bash
   # Navigate to project directory
   cd path/to/ai-voice-assistant
   
   # Set local Python version for this directory
   pyenv local 3.11.9
   
   # Verify correct version
   python --version  # Should output Python 3.11.9
   ```

4. If the python command doesn't show 3.11.9, you can use the full path to create your virtual environment:
   ```bash
   ~/.pyenv/versions/3.11.9/bin/python -m venv venv
   ```

## Verification Steps
1. Check Python version:
   ```bash
   python3 --version
   ```

2. Check pip version:
   ```bash
   pip3 --version
   ```

## Virtual Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. Verify activation (should show venv in prompt):
   ```bash
   which python
   ```

## Installing Project Dependencies
1. Install project in development mode:
   ```bash
   pip install -e .
   ```

2. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install additional dependencies for voice cloning demo:
   ```bash
   pip install sounddevice
   ```

## PyTorch 2.6+ Fix for TTS
If you encounter errors loading TTS models with PyTorch 2.6+, you'll need to patch the TTS library:

1. Locate the io.py file in your virtual environment:
   ```bash
   # Find path to the file
   find venv -name "io.py" | grep TTS
   ```

2. Edit the file (will typically be at `venv/lib/python3.11/site-packages/TTS/utils/io.py`)
   Add the following code in the `load_fsspec` function before the `torch.load` call:
   ```python
   # Override the weights_only parameter to False to fix loading with PyTorch 2.6+
   if "weights_only" not in kwargs:
       kwargs["weights_only"] = False
   ```

3. Making the fix persistent:
   This fix will be lost if you reinstall TTS. For a more permanent solution, you can:
   - Create a post-install script that applies the patch automatically
   - Fork the TTS library, apply your fix, and install from your fork

4. **Recommended approach:**
   - **Manual editing** (as described above) is currently the fastest and simplest solution
   - For single-environment setups, this one-time edit is sufficient
   - If you need to set up multiple environments or frequently recreate your environment, consider creating an automation script like this:
     ```bash
     #!/bin/bash
     # patch_tts.sh - Script to patch TTS library for PyTorch 2.6+ compatibility
     
     # Find TTS io.py file
     IO_FILE=$(find venv -name "io.py" | grep "TTS/utils" | head -n 1)
     
     if [ -z "$IO_FILE" ]; then
       echo "Error: Could not find TTS/utils/io.py file"
       exit 1
     fi
     
     echo "Found TTS io.py at: $IO_FILE"
     
     # Check if the file already contains our fix
     if grep -q "weights_only" "$IO_FILE"; then
       echo "Patch already applied."
       exit 0
     fi
     
     # Apply the patch
     sed -i'.bak' '/with fsspec.open/i\
     \ \ \ \ # Override the weights_only parameter to False to fix loading with PyTorch 2.6+\
     \ \ \ \ if "weights_only" not in kwargs:\
     \ \ \ \ \ \ \ \ kwargs["weights_only"] = False\
     ' "$IO_FILE"
     
     echo "Patch applied successfully."
     ```
   - Make the script executable and run it after each TTS installation: `chmod +x patch_tts.sh && ./patch_tts.sh`

## Testing Your Setup
Run the voice cloning demo to test your setup:
```bash
python examples/voice_cloning_demo.py
```

## Common Issues
1. If 'python3' command not found:
   - Install Python from [python.org](https://www.python.org/downloads/)
   - Ensure Python is in your PATH

2. If pip commands fail:
   ```bash
   python3 -m ensurepip --upgrade
   ```

## Next Steps
1. Verify installation:
   ```bash
   pip list
   ```

2. Set up local LLM (if needed):
   ```bash
   python -m tts.setup_llm
   ```

3. Run tests to verify setup:
   ```bash
   python -m unittest discover tests
   ```

## Additional Configuration
- For voice processing features, ensure you have:
  - FFmpeg installed (for audio processing)
  - PortAudio development headers (for PyAudio)

## Troubleshooting
- If voice processing tests fail:
  ```bash
  brew install ffmpeg portaudio  # macOS
  sudo apt-get install ffmpeg portaudio19-dev  # Linux
  ```

- If you see `ModuleNotFoundError: No module named 'tts'`, ensure you ran `pip install -e .`
- If you encounter model loading errors mentioning `weights_only`, apply the PyTorch 2.6+ fix
- For XTTS model license issues, accept the license agreement when prompted
- For audio device errors, ensure your system's audio input/output is working correctly
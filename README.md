# AI Voice Assistant

## Project Goal

This AI Voice Assistant aims to automate podcast generation workflows using locally hosted LLMs and voice cloning capabilities while maintaining production-quality output. See [Problem Statement](docs/problem_statement.md) for details.

## Key Features

- Text-to-Speech with natural sounding voices
- Voice cloning using Coqui TTS XTTS v2 models
- Local processing for privacy and security

## Requirements

- Python 3.11 (required for Coqui TTS compatibility)
- See [requirements.txt](requirements.txt) for complete dependencies

## Installation

**Important:** This project requires Python 3.11 as the voice cloning functionality is not compatible with Python 3.12+.

For detailed setup instructions including Python version management, environment setup, and troubleshooting, please refer to:
[Python Setup Guide](docs/guidelines/python_setup.md)

Quick setup:
```bash
# Set up Python 3.11 environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .
pip install -r requirements.txt

# For voice cloning demo functionality
pip install sounddevice
```

## Voice Cloning

See [Voice Cloning Documentation](docs/features/voice_cloning.md) for implementation details and usage examples.

## Development

- Follow [Coding Standards](docs/guidelines/coding_standards.md) for contributions
- See [Prompt Evolution Guide](docs/guidelines/prompt_evolution.md) for AI-assisted development
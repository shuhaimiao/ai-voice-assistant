# Python Environment Setup Guide

## Prerequisites
- Python 3.8+ installed
- pip package manager
- venv module (usually included with Python)

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
   python3 -m venv venv
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

## Common Issues
1. If 'python3' command not found:
   - Install Python from [python.org](https://www.python.org/downloads/)
   - Ensure Python is in your PATH

2. If pip commands fail:
   ```bash
   python3 -m ensurepip --upgrade
   ```

## Next Steps
1. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Verify installation:
   ```bash
   pip list
   ```
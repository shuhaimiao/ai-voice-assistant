from setuptools import setup, find_packages

setup(
    name="ai-voice-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyttsx3>=2.90",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "librosa>=0.9.0",
        "soundfile>=0.12.0",
    ],
    python_requires=">=3.9",
)
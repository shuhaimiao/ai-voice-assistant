# ADR 0001: Text-to-Speech Library Selection

## Status

Accepted

## Context

We needed to implement text-to-speech functionality in Python for the AI Voice Assistant project. The key requirements were:
- Offline functionality
- Natural sounding voices
- macOS compatibility

## Decision

After evaluating alternatives, we selected pyttsx3 as our text-to-speech library because:
1. Provides offline functionality (unlike gTTS which requires internet)
2. Supports voice customization
3. Works natively on macOS
4. Simple API for basic TTS needs

## Consequences

### Positive
- No internet dependency for core functionality
- Easy to implement basic TTS features
- Supports voice parameter adjustments

### Negative
- Limited voice quality compared to cloud-based solutions
- Requires additional error handling for speech synthesis

## Alternatives Considered

- **gTTS (Google Text-to-Speech)**
  - Pros: Better voice quality, simple API
  - Cons: Requires internet connection, limited customization

- **Festival**
  - Pros: Open source, highly customizable
  - Cons: Complex setup, poor macOS support

## References

- [pyttsx3 documentation](https://pyttsx3.readthedocs.io/)
- [Prompt Evolution Guide](../guidelines/prompt_evolution.md)
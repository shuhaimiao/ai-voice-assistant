# AI-Assisted Development Guide

This document outlines an effective developer workflow for AI-assisted development, based on our collaboration on the text-to-speech project. The workflow incorporates problem discussion, design brainstorming, test-driven development, and iterative refinement.

## Workflow Overview

1. **Problem & Requirement Discussion**
   - Clearly define the problem space
   - Identify key requirements and constraints
   - Example: Our initial discussion about TTS functionality requirements (see [feature document](/docs/features/text_to_speech.md))
   - Effective Prompt Example: "We need to build a text-to-speech feature for our voice assistant. The key requirements are: 1) Support multiple languages, 2) Generate natural-sounding speech, 3) Work in real-time. What are the best approaches to implement this?"
   - Improvement Area: Initially I didn't specify the performance requirements clearly, which led to some back-and-forth. A better prompt would be: "We need real-time TTS with <500ms latency for English text under 100 characters. What implementation options meet this requirement?"

2. **Design Brainstorm**
   - Explore potential solutions
   - Evaluate trade-offs
   - Example: Deciding between different TTS implementation approaches (see [ADR](/docs/adr/0001-text-to-speech-library-selection.md))
   - Effective Prompt Example: "Compare these TTS options: 1) Cloud API like Google TTS, 2) Local model like Piper, 3) Python library like pyttsx3. List pros/cons for each in terms of quality, latency, and setup complexity."
   - Improvement Area: Early prompts were too open-ended like "What TTS options exist?" Better to specify comparison criteria upfront.

3. **Task Decomposition & Plan**
   - Break down features into manageable tasks
   - Prioritize implementation sequence
   - Example: Separating TTS model initialization from text processing (see [implementation steps](/docs/features/text_to_speech.md#implementation))
   - Effective Prompt Example: "Break down the TTS implementation into discrete steps we can tackle sequentially. Start with the minimal working prototype and list subsequent enhancements."
   - Improvement Area: Initially didn't specify the desired output format. Better prompt: "Create a numbered task list for TTS implementation, with estimated complexity (low/med/high) for each task."

4. **Test-Driven Development (TDD)**
   - Write tests before implementation
   - Iteratively develop to pass tests
   - Example: Our test cases for TTS initialization (see [test file](/tests/test_tts_init.py))
   - Effective Prompt Example: "Write pytest cases for TTS initialization covering: 1) Successful model load, 2) Error handling for invalid paths, 3) Performance benchmark setup."
   - Improvement Area: Early test prompts lacked specific assertions. Better to specify: "Include assertions for expected success/failure cases and performance thresholds."

5. **Incremental Implementation**
   - Implement features in small, verifiable steps
   - Regular checkpoints for review
   - Example: Building TTS demo incrementally (see [demo code](/examples/tts_demo.py))
   - Effective Prompt Example: "Implement just the TTS initialization first with error handling. Show me the minimal code to load the model and verify it works."
   - Improvement Area: Initially asked for complete solutions. Better to phrase as: "Show me the smallest working piece first, then we'll iterate."

6. **Documentation**
   - Document decisions and implementations
   - Keep docs updated with changes
   - Example: This guide and the TTS feature spec (see [feature documentation](/docs/features/text_to_speech.md))
   - Effective Prompt Example: "Generate documentation for our TTS implementation covering: 1) Setup instructions, 2) API reference, 3) Known limitations. Use Markdown format."
   - Improvement Area: Early documentation prompts were too vague. Better to specify: "Include code examples for common usage patterns and troubleshooting tips."

7. **Reflection & Iteration**
   - Review what worked well
   - Identify areas for improvement
   - Example: Our workflow refinements during development (see [prompt evolution](/docs/guidelines/prompt_evolution.md))
   - Effective Prompt Example: "Analyze our TTS implementation process. What aspects of our collaboration worked well? Where could we improve the workflow?"
   - Improvement Area: Initially didn't specify reflection scope. Better prompt: "Evaluate our prompt effectiveness and implementation velocity. Suggest 3 concrete workflow improvements."

## Case Study: Text-to-Speech Implementation

Our TTS project followed this workflow:
1. Discussed requirements for interactive demo
2. Brainstormed CLI vs GUI approaches
3. Decomposed into initialization, text processing, audio playback
4. Wrote initialization tests first
5. Built demo incrementally with voice feedback
6. Documented each step in specs and this guide
7. Refined based on testing experience

## Best Practices

- Regular sync points with AI assistant
- Clear communication of intent
- Small, focused iterations
- Comprehensive testing
- Continuous documentation

This workflow combines human creativity with AI efficiency, resulting in high-quality, maintainable software.
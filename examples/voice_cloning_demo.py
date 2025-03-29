"""
Voice Cloning Demo Script

This script demonstrates the voice cloning functionality using the VoiceCloning class.
It shows end-to-end usage including interactive voice sample collection, validation,
and test generation.
"""
from tts.voice_cloning import VoiceCloning
import soundfile as sf
import numpy as np
import sounddevice as sd
import time
import os

# Initialize VoiceCloning
vc = VoiceCloning()
# Initialization is now handled within the clone_voice/text_to_speech call if needed
# if not vc.initialize_model():
#     print("Failed to initialize TTS engine")
#     exit(1)

# Example: Validate a voice sample
def validate_sample(file_path):
    try:
        print(f"Validating sample: {file_path}")
        # Call the updated validation method (which now returns bool)
        if vc.validate_voice_sample(file_path):
            print("Sample validation passed!")
            return True
        else:
            # Error message is now logged within validate_voice_sample
            print("Sample validation failed (see logs for details).") 
            return False
    except Exception as e:
        # Catch potential exceptions during validation call itself
        print(f"Validation failed with exception: {str(e)}")
        return False

# Remove the process_sample function as preprocessing is internal to XTTS
# def process_sample(file_path):
#     ...

def record_sample(duration=10, sample_rate=44100):
    """Record audio sample from microphone."""
    print(f"Please speak clearly for {duration} seconds after the beep...")
    time.sleep(1)
    print("\a")  # System beep
    
    recording = sd.rec(int(duration * sample_rate), 
                      samplerate=sample_rate, 
                      channels=1,
                      dtype='float32')
    sd.wait()
    return recording, sample_rate

if __name__ == "__main__":
    print("Voice Cloning Demo (using Coqui TTS XTTS)")
    print("=================")
    
    # Step 1: Collect single voice sample
    print("\n=== Voice Sample Collection ===")
    samples = []
    print("\nSample 1/1:")
    audio, sr = record_sample()
    temp_file = "temp_sample.wav"
    sf.write(temp_file, audio, sr) # Save the original recording temporarily
    
    reference_file = "reference_sample.wav" # Define reference file path
    if validate_sample(temp_file):
        # If valid, save/rename it as the reference file for cloning
        # Use os.rename for efficiency, ensure it overwrites if exists
        try:
            os.rename(temp_file, reference_file)
            print(f"Sample accepted and saved as {reference_file}!")
            sample_accepted = True
        except OSError as e:
            print(f"Error renaming temp file: {e}")
            # Fallback to copy if rename fails (e.g., across different filesystems)
            try:
                 sf.write(reference_file, audio, sr)
                 os.remove(temp_file) # Clean up temp file after successful copy
                 print(f"Sample accepted and saved as {reference_file}! (using copy)")
                 sample_accepted = True
            except Exception as copy_e:
                 print(f"Failed to save reference file: {copy_e}")
                 sample_accepted = False
                 # Clean up temp file even if copy fails
                 if os.path.exists(temp_file):
                    os.remove(temp_file)
    else:
        print("Sample rejected, please try again.")
        sample_accepted = False
        # Clean up the temp file if rejected
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    # Remove Step 2: Processing Samples - no longer needed
    # print("\n=== Processing Samples ===")
    # processed_samples = []
    # ... (removed processing loop) ...
    
    # Step 3: Generate test output (renamed from Step 2)
    print("\n=== Generating Test Output ===")
    if sample_accepted:
        print("Generating cloned voice sample...")
        
        # Step 3.1: Get test prompt from user
        test_prompt = input("\nEnter text to generate with cloned voice: ")
        if not test_prompt:
            print("No text provided. Exiting.")
            exit(1)
            
        output_file = "cloned_voice_output.wav"
        language_code = "en" # Assuming English for the demo
        
        # Step 3.2: Call clone_voice with the reference file path and language
        # No need to manually handle processed_samples or check vc.model
        try:
            # Ensure the reference file exists before cloning
            if not os.path.exists(reference_file):
                print(f"Error: Reference file {reference_file} not found.")
                exit(1)
                
            print(f"Calling clone_voice with reference: {reference_file}, lang: {language_code}")
            success = vc.clone_voice(
                text=test_prompt, 
                reference_audio=reference_file, 
                language=language_code, 
                output_path=output_file
            )
            
            if success:
                print(f"Successfully generated cloned voice at {output_file}")
                
                # Play the generated audio
                print("Playing generated audio...")
                audio, sr = sf.read(output_file)
                sd.play(audio, sr)
                sd.wait()
                print("Demo completed successfully!")
            else:
                # Error logged within clone_voice/text_to_speech
                print("Failed to generate cloned voice (see logs for details).") 
        except Exception as e:
            print(f"Error during voice generation: {str(e)}")
    else:
        print("Demo cannot proceed without a valid voice sample.")
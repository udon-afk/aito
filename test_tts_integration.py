import sys
import os
import time

# Add the project root to sys.path
sys.path.append(os.path.abspath("F:/aisisterprogram.1/aito"))

try:
    from src.services.sbv2_client import SBV2Client

    print("Initializing SBV2Client...")
    client = SBV2Client()
    
    text = "テストです。音声生成の確認をしています。"
    print(f"Generating audio for text: {text}")
    
    start_time = time.time()
    audio_path = client.tts(text)
    end_time = time.time()
    
    if audio_path and os.path.exists(audio_path):
        print(f"Success! Audio saved to: {audio_path}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"File size: {os.path.getsize(audio_path)} bytes")
    else:
        print("Failed to generate audio.")

except ImportError as e:
    print(f"ImportError: {e}")
    print("Please make sure you are running this script from the correct directory or PYTHONPATH is set.")
except Exception as e:
    print(f"Error: {e}")

import os
import requests
from kokoro_onnx import Kokoro
import soundfile as sf

def download_file(url, local_filename):
    if not os.path.exists(local_filename):
        print(f"Downloading {local_filename}...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

def main():
    print("Setting up Kokoro TTS...")
    # These are the standard URLs from the official HuggingFace repo
    download_file("https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/kokoro-v1.0.onnx?download=true", "kokoro-v1.0.onnx")
    download_file("https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/voices.json?download=true", "voices.json")
    
    print("Loading model...")
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices.json")
    
    print("Generating audio...")
    # af_sarah or af_bella are good female voices, am_adam is a good male voice
    samples, sample_rate = kokoro.create("Hello world! This is Kokoro.", voice="af_sarah", speed=1.0, lang="en-us")
    
    sf.write("test_kokoro.wav", samples, sample_rate)
    print("Done! Saved to test_kokoro.wav")

if __name__ == "__main__":
    main()

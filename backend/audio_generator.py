import os
import requests
import soundfile as sf
from kokoro_onnx import Kokoro

# High-quality open-source voice options:
# 'af_bella' (Female, US), 'af_sarah' (Female, US), 'am_adam' (Male, US)
VOICE_NAME = "af_bella"

def download_file(url, local_filename):
    if not os.path.exists(local_filename):
        print(f"Downloading {local_filename} (This only happens once)...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded {local_filename}.")

def setup_kokoro():
    model_url = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
    voices_url = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
    
    # We download them to the current directory (backend/)
    download_file(model_url, "kokoro-v1.0.onnx")
    download_file(voices_url, "voices-v1.0.bin")
    
    return Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

def generate_podcast_audio(text_script, output_filename="podcast.mp3"):
    """Converts the text script to an audio file using free Kokoro TTS."""
    print("Setting up Kokoro TTS (High Quality, 100% Free)...")
    
    try:
        kokoro = setup_kokoro()
        print(f"Generating audio with voice {VOICE_NAME}...")
        
        # Create audio chunks
        samples, sample_rate = kokoro.create(text_script, voice=VOICE_NAME, speed=1.0, lang="en-us")
        
        wav_filename = output_filename.replace(".mp3", ".wav")
        sf.write(wav_filename, samples, sample_rate)
        
        # Convert WAV to MP3 using ffmpeg (required for Spotify)
        print("Converting to MP3 format for Spotify compatibility...")
        import subprocess
        subprocess.run(["ffmpeg", "-y", "-i", wav_filename, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", output_filename], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clean up the large WAV file
        if os.path.exists(wav_filename):
            os.remove(wav_filename)
            
        print(f"Audio saved successfully to {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

if __name__ == "__main__":
    generate_podcast_audio("Hello world. This is a test of the Neural Newz high quality audio system using Kokoro.", "test_podcast.wav")


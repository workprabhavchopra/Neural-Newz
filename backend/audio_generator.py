import asyncio
import edge_tts
import os

# We use the free Microsoft Edge TTS API
# "en-US-AriaNeural" is a high-quality, natural-sounding voice
VOICE = "en-US-AriaNeural"

async def _generate_edge_tts(text_script, output_filename):
    """Async helper to generate TTS using Edge TTS."""
    communicate = edge_tts.Communicate(text_script, VOICE)
    await communicate.save(output_filename)

def generate_podcast_audio(text_script, output_filename="podcast.mp3"):
    """Converts the text script to an audio file using free Edge TTS."""
    print("Generating audio with Edge-TTS (100% Free)...")
    
    try:
        # Run the async Edge-TTS function in the synchronous wrapper
        asyncio.run(_generate_edge_tts(text_script, output_filename))
        print(f"Audio saved successfully to {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

if __name__ == "__main__":
    # Simple test
    generate_podcast_audio("Hello world. This is a test of the Neural News free audio system using Edge TTS.")

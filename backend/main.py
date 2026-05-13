import os
from datetime import datetime
from email.utils import formatdate
import json

from fetcher import fetch_all_daily_content
from summarizer import generate_podcast_script, generate_newsletter_html
from audio_generator import generate_podcast_audio
from publisher import generate_rss_feed
from mailer import send_daily_newsletter

def main():
    print(f"--- Starting Neural News Daily Run: {datetime.now().isoformat()} ---")
    
    # 1. Fetch Content
    content = fetch_all_daily_content()
    
    # 2. Generate Podcast Script
    script = generate_podcast_script(content)
    print("Podcast Script preview:\n", script[:200] + "...")
    
    # 3. Generate Audio
    date_str = datetime.now().strftime("%Y%m%d")
    audio_filename = f"episode_{date_str}.mp3"
    
    # The audio should be saved into the frontend/public/episodes folder so it's hosted by Vercel
    os.makedirs("../frontend/public/episodes", exist_ok=True)
    audio_path = os.path.join("../frontend/public/episodes", audio_filename)
    
    generated_audio_path = generate_podcast_audio(script, output_filename=audio_path)
    
    # 4. Generate RSS Feed
    # Read existing episodes or create new list
    episodes_file = "../frontend/public/episodes_meta.json"
    episodes = []
    if os.path.exists(episodes_file):
        with open(episodes_file, 'r') as f:
            episodes = json.load(f)
            
    # Add new episode if audio was generated
    if generated_audio_path:
        audio_size = os.path.getsize(generated_audio_path)
        new_episode = {
            "title": f"Neural News Daily - {datetime.now().strftime('%b %d, %Y')}",
            "description": script[:500] + "...",  # Use first 500 chars of script as description
            "audio_url": f"episodes/{audio_filename}",
            "length": audio_size,
            "pub_date": formatdate(timeval=None, localtime=False, usegmt=True)
        }
        episodes.insert(0, new_episode) # Add to top
        
        # Save updated metadata
        with open(episodes_file, 'w') as f:
            json.dump(episodes, f, indent=2)
            
        # Update RSS feed
        generate_rss_feed(episodes)
        print("RSS feed updated.")
    
    # 5. Generate and Send Newsletter
    # Pass the audio URL so the newsletter can link to it
    base_url = os.getenv("BASE_URL", "https://neural-news-podcast.vercel.app")
    podcast_url = f"{base_url}/episodes/{audio_filename}" if generated_audio_path else None
    
    html_newsletter = generate_newsletter_html(content, podcast_url=podcast_url)
    send_daily_newsletter(html_newsletter)
    
    print("--- Neural News Daily Run Complete ---")

if __name__ == "__main__":
    main()

import os
from datetime import datetime
from email.utils import formatdate
import json

from fetcher import fetch_all_daily_content
from summarizer import generate_podcast_script, generate_newsletter_html, generate_episode_title, generate_episode_description, slugify
from audio_generator import generate_podcast_audio
from publisher import generate_rss_feed
from mailer import send_daily_newsletter

def main():
    print(f"--- Starting Neural Newz Daily Run: {datetime.now().isoformat()} ---")
    
    # 1. Fetch Content
    content = fetch_all_daily_content()
    
    # 2. Generate a catchy, news-based episode title
    episode_title = generate_episode_title(content)
    print(f"Episode title: {episode_title}")

    # 3. Generate Podcast Script
    script = generate_podcast_script(content)
    print("Podcast Script preview:\n", script[:200] + "...")

    # 4. Generate episode description (for Spotify, RSS feed, and newsletter)
    episode_description = generate_episode_description(content, episode_title)
    
    # 4. Generate Audio — filename is a slug of the episode title
    date_str = datetime.now().strftime("%Y%m%d")
    slug = slugify(episode_title)
    # Keep it reasonably short for the filesystem: slug up to 60 chars + date
    safe_slug = slug[:60].rstrip('-')
    audio_filename = f"{safe_slug}_{date_str}.mp3"
    
    # The audio should be saved into the frontend/public/episodes folder so it's hosted by Netlify
    os.makedirs("../frontend/public/episodes", exist_ok=True)
    audio_path = os.path.join("../frontend/public/episodes", audio_filename)
    
    generated_audio_path = generate_podcast_audio(script, output_filename=audio_path)
    
    # 4. Generate RSS Feed
    episodes_file = "../frontend/public/episodes_meta.json"
    episodes = []
    if os.path.exists(episodes_file):
        with open(episodes_file, 'r') as f:
            episodes = json.load(f)
            
    # Add new episode if audio was generated
    if generated_audio_path:
        audio_size = os.path.getsize(generated_audio_path)
        new_episode = {
            "title": episode_title,
            "description": episode_description,
            "audio_url": f"episodes/{audio_filename}",
            "length": audio_size,
            "pub_date": formatdate(timeval=None, localtime=False, usegmt=True)
        }
        episodes.insert(0, new_episode)
        
        with open(episodes_file, 'w') as f:
            json.dump(episodes, f, indent=2)
            
        generate_rss_feed(episodes)
        print("RSS feed updated.")
    
    # 5. Generate and Send Newsletter
    base_url = os.getenv("BASE_URL", "https://neural-newz-podcast.netlify.app")
    podcast_url = f"{base_url}/episodes/{audio_filename}" if generated_audio_path else None
    
    html_newsletter = generate_newsletter_html(content, podcast_url=podcast_url)
    send_daily_newsletter(html_newsletter)
    
    print("--- Neural Newz Daily Run Complete ---")

if __name__ == "__main__":
    main()

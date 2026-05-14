import os
import re
from datetime import datetime
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Gemini API Key not found. {e}")
    client = None

def slugify(text):
    """Converts a title string to a safe, lowercase filename slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)      # Remove special chars except hyphens
    text = re.sub(r'[\s_]+', '-', text)         # Replace spaces/underscores with hyphens
    text = re.sub(r'-+', '-', text)              # Collapse multiple hyphens
    return text.strip('-')

def generate_episode_title(content_items):
    """Uses Gemini to create a catchy, news-based episode title with the date."""
    date_str = datetime.now().strftime("%d %B %Y").lstrip("0")  # e.g. "14 May 2026"

    if not content_items or not client:
        return f"Neural Newz Daily — {date_str}"

    # Pull just the top headlines for the prompt
    headlines = "\n".join([f"- [{item['source']}] {item['title']}" for item in content_items[:6]])

    prompt = f"""
    You are writing a podcast episode title for "Neural Newz", a daily AI news podcast.
    Based on the top stories below, generate ONE catchy, punchy episode title that:
    - Highlights the 1-2 biggest stories of the day (mention company names, products, or themes)
    - Ends with the date: "{date_str}"
    - Uses a separator like " | " or " + " between the headline and the date
    - Is under 80 characters total
    - Sounds like a professional podcast episode, NOT a news headline

    Top stories today:
    {headlines}

    Return ONLY the title, nothing else. No quotes, no explanation.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        title = response.text.strip().strip('"').strip("'")
        print(f"Generated episode title: {title}")
        return title
    except Exception as e:
        print(f"Error generating episode title: {e}")
        return f"Neural Newz Daily — {date_str}"


def generate_episode_description(content_items, episode_title):
    """Uses Gemini to write a compelling, Spotify-ready episode description."""
    if not content_items or not client:
        return "Your daily deep-dive into the world of AI. Tune in for the latest breakthroughs, product launches, and research from the world's top labs."

    headlines = "\n".join([f"- [{item['source']}] {item['title']}" for item in content_items])

    prompt = f"""
    You are writing a podcast episode description for Spotify and Apple Podcasts for an episode titled:
    "{episode_title}"

    The episode covers these AI stories:
    {headlines}

    Write a compelling episode description that:
    - Opens with a punchy 1-sentence hook about why today's news is significant
    - Lists the top 3-5 stories as bullet points with a brief (1 sentence) tease for each
    - Closes with a 1-sentence call-to-action to subscribe and follow Neural Newz
    - Is between 150-300 words total
    - Uses plain text only (no markdown, no asterisks, no hashtags) since this will appear in podcast apps
    - Sounds like a human wrote it, not a robot

    Return ONLY the description text, nothing else.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        description = response.text.strip()
        print(f"Generated episode description ({len(description)} chars)")
        return description
    except Exception as e:
        print(f"Error generating episode description: {e}")
        # Fallback: join the top story titles into a readable description
        stories = ", ".join([item['title'] for item in content_items[:3]])
        return f"Today on Neural Newz: {stories}. Subscribe for your daily AI briefing."


def generate_podcast_script(content_items):
    """Generates a conversational podcast script from the news items using Gemini."""
    if not content_items:
        return "Welcome to Neural Newz. There were no major AI breakthroughs in the last 24 hours. See you tomorrow!"

    if not client:
        print("Gemini API key not configured. Falling back to default script.")
        return "Welcome to Neural Newz. This is a default placeholder script because the Gemini API key was not configured."

    print("Generating podcast script with Gemini...")
    
    content_text = ""
    for idx, item in enumerate(content_items):
        content_text += f"\n[{idx+1}] Source: {item['source']}\nTitle: {item['title']}\nDetailed Analysis: {item.get('detailed_analysis', item.get('summary', ''))}\n"
    
    prompt = f"""
    You are the host of a daily, highly educational podcast called "Neural Newz". 
    Your audience consists of people who are actively trying to learn about AI and stay up-to-date with the rapidly changing landscape.
    
    Your task is to write a deep-dive, 10-20 minute podcast script (APPROXIMATELY 1500 to 2500 WORDS). 
    Do NOT just read the news. Act as an expert educator. For each topic:
    - Explain the underlying technology and break down complex concepts using simple analogies.
    - Discuss *why* this development matters and its potential impact on the industry.
    - Provide practical context or real-world applications.
    
    Read like a solo host. Use smooth transitional phrases between topics. Keep the tone professional, insightful, and highly educational.
    
    Here is the detailed news and research for today:
    {content_text}
    
    Write the final script exactly as it should be read by the text-to-speech engine. Do not include instructions like "[Upbeat Intro Music]". Just the spoken text.
    Ensure the script is long enough and detailed enough to hit the 1500+ word count mark.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating script: {e}")
        return "Welcome to Neural Newz. Unfortunately, there was an error generating today's script."

def generate_newsletter_html(content_items, podcast_url=None):
    """Generates the HTML content for the daily email newsletter."""
    if not content_items:
        return "<h1>Neural Newz</h1><p>No major updates in the last 24 hours.</p>"
        
    print("Generating newsletter HTML...")
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
        <h1 style="color: #4F46E5; text-align: center;">Neural Newz Daily Intelligence</h1>
        <p style="text-align: center; color: #666;">The noise of AI, turned into signal.</p>
        <hr style="border: 1px solid #eee; margin: 20px 0;" />
    """
    
    if podcast_url:
        html += f"""
        <div style="background-color: #F3F4F6; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
            <h3>🎧 Today's Podcast is Ready</h3>
            <p>Prefer to listen? Catch up on today's AI news on the go.</p>
            <a href="{podcast_url}" style="background-color: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Listen Now</a>
        </div>
        """

    html += "<h2 style='color: #111;'>📰 Today's Top Stories</h2><ul style='padding-left: 20px;'>"
    for item in content_items:
        details = item.get('detailed_analysis', item.get('summary', ''))
        # Truncate details for the email if it's too long (over 600 chars), since the full analysis is huge now
        if len(details) > 600:
            details = details[:600] + "... <em>(Listen to the podcast for the full deep dive)</em>"
            
        html += f"""
        <li style="margin-bottom: 25px;">
            <span style="font-size: 12px; font-weight: bold; color: #4F46E5; text-transform: uppercase;">{item['source']}</span><br/>
            <a href="{item['link']}" style="font-size: 18px; color: #111; font-weight: bold; text-decoration: none;">{item['title']}</a>
            <p style="font-size: 14px; line-height: 1.6; color: #444; margin: 8px 0 0 0;">{details}</p>
        </li>
        """
    html += "</ul>"
        
    html += """
        <hr style="border: 1px solid #eee; margin: 20px 0;" />
        <p style="font-size: 12px; text-align: center; color: #999;">You are receiving this because you subscribed to Neural Newz.</p>
    </div>
    """
    return html

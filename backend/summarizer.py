import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Gemini API Key not found. {e}")
    client = None

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
        content_text += f"\n[{idx+1}] Source: {item['source']}\nTitle: {item['title']}\nSummary: {item['summary']}\n"
    
    prompt = f"""
    You are the host of a daily 3-5 minute podcast called "Neural Newz". 
    Your goal is to summarize the following daily AI news and research papers into an engaging, conversational, and highly technical but accessible script.
    Read like a solo host. Use transitional phrases. Do not use sound effects or multiple voices, just a single continuous monologue.
    Keep the tone professional, insightful, and slightly enthusiastic about AI breakthroughs.
    
    Here is the news for today:
    {content_text}
    
    Write the final script exactly as it should be read by a text-to-speech engine. Do not include instructions like "[Upbeat Intro Music]". Just the spoken text.
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
        html += f"""
        <li style="margin-bottom: 15px;">
            <span style="font-size: 12px; font-weight: bold; color: #4F46E5; text-transform: uppercase;">{item['source']}</span><br/>
            <a href="{item['link']}" style="font-size: 16px; color: #111; font-weight: bold; text-decoration: none;">{item['title']}</a>
            <p style="font-size: 14px; line-height: 1.5; color: #444; margin: 4px 0 0 0;">{item['summary']}</p>
        </li>
        """
    html += "</ul>"
        
    html += """
        <hr style="border: 1px solid #eee; margin: 20px 0;" />
        <p style="font-size: 12px; text-align: center; color: #999;">You are receiving this because you subscribed to Neural Newz.</p>
    </div>
    """
    return html

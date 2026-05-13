import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
# It automatically picks up GEMINI_API_KEY from the environment
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Gemini API Key not found. {e}")
    client = None

def generate_podcast_script(content_items):
    """Generates a conversational podcast script from the news items using Gemini (Free Tier)."""
    if not content_items:
        return "Welcome to Neural News. There were no major AI breakthroughs in the last 24 hours. See you tomorrow!"

    if not client:
        print("Gemini API key not configured. Falling back to default script.")
        return "Welcome to Neural News. This is a default placeholder script because the Gemini API key was not configured."

    print("Generating podcast script with Gemini...")
    
    # Format content for the prompt
    content_text = ""
    for idx, item in enumerate(content_items):
        content_text += f"\n[{idx+1}] Source: {item['source']}\nTitle: {item['title']}\nSummary: {item['summary']}\n"
    
    prompt = f"""
    You are the host of a daily 3-5 minute podcast called "Neural News". 
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
        return "Welcome to Neural News. Unfortunately, there was an error generating today's script."

def generate_newsletter_html(content_items, podcast_url=None):
    """Generates the HTML content for the daily email newsletter."""
    if not content_items:
        return "<h1>Neural News</h1><p>No major updates in the last 24 hours.</p>"
        
    print("Generating newsletter HTML...")
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
        <h1 style="color: #4F46E5; text-align: center;">Neural News Daily Intelligence</h1>
        <p style="text-align: center; color: #666;">The noise of AI, turned into signal.</p>
        <hr style="border: 1px solid #eee; margin: 20px 0;" />
    """
    
    if podcast_url:
        html += f"""
        <div style="background-color: #F3F4F6; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
            <h3>🎧 Today's Podcast is Ready</h3>
            <a href="{podcast_url}" style="background-color: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Listen Now</a>
        </div>
        """
        
    for item in content_items:
        html += f"""
        <div style="margin-bottom: 20px;">
            <span style="font-size: 12px; font-weight: bold; color: #4F46E5; text-transform: uppercase;">{item['source']}</span>
            <h2 style="font-size: 18px; margin: 5px 0;"><a href="{item['link']}" style="color: #111; text-decoration: none;">{item['title']}</a></h2>
            <p style="font-size: 14px; line-height: 1.5; color: #444;">{item['summary']}</p>
        </div>
        """
        
    html += """
        <hr style="border: 1px solid #eee; margin: 20px 0;" />
        <p style="font-size: 12px; text-align: center; color: #999;">You are receiving this because you subscribed to Neural News.</p>
    </div>
    """
    return html

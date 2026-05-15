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
    """Uses Gemini to write a compelling, curiosity-driven Spotify episode description."""
    if not content_items or not client:
        return "Your daily deep-dive into the world of AI. Tune in for the latest breakthroughs, product launches, and research from the world's top labs."

    # Give Gemini the companies and topics involved, but not the detailed analysis
    topics = "\n".join([f"- [{item['source']}] {item['title']}" for item in content_items])

    prompt = f"""
    You are a podcast producer writing an episode description for "Neural Newz", a daily AI intelligence podcast.
    The episode is titled: "{episode_title}"

    Study these real podcast description styles before writing:

    HARD FORK STYLE (NYT Tech): Conversational, journalistic. Teases topics as open questions or stakes without giving away the answer. Example: "This week: OpenAI made a move that's got everyone asking questions about what comes next. Plus, we dig into why the biggest labs are suddenly very interested in one particular corner of academia — and what it signals."

    NO PRIORS STYLE: Big-picture, strategic. Frames stories as inflection points. Uses "we unpack / we explore / we dig into" language. Focuses on WHY it matters, not WHAT happened.

    LATENT SPACE STYLE: Technical but insider. Builds stakes with a provocative claim or question, then promises to explain it. 

    The topics covered today are:
    {topics}

    Now write a description for Neural Newz that:
    1. FIRST TWO LINES (most important — Spotify shows only these on mobile): Start with a punchy atmospheric sentence about the current state of AI, then one sentence teasing today's biggest theme WITHOUT naming specific findings or conclusions (e.g., "A major player just shifted strategy — and the implications are bigger than anyone is saying.")
    2. A SHORT PARAGRAPH: Set the scene of today's AI landscape in 2-3 sentences. Reference which companies or domains are involved but frame it as questions or stakes — never reveal what actually happened.
    3. "In this episode:" followed by 3-5 bullet points. Each bullet should use a curiosity gap: start with WHY, HOW, or WHAT — but end on the intrigue, not the answer. Format: plain text dashes, not markdown asterisks.
    4. ONE closing sentence: A value proposition + soft CTA. E.g., "Follow Neural Newz and make every day in AI make sense."

    STRICT RULES:
    - Do NOT reveal conclusions, findings, benchmark scores, or specific outcomes
    - Do NOT use markdown (no asterisks, no hashtags, no bold)
    - Use plain text with line breaks between sections
    - Keep total length between 180-280 words
    - Sound like a human who's genuinely excited about AI wrote this

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
        stories = " | ".join([item['source'] for item in content_items[:4]])
        return f"Today on Neural Newz, we're cutting through the noise from {stories} and more. Tune in for your daily deep-dive into the world of AI. Follow Neural Newz to stay ahead of the curve."


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

def generate_newsletter_html(content_items, podcast_url=None, is_welcome=False):
    """Generates the HTML content for the daily email newsletter."""
    if not content_items:
        return "<h1 style='color: #F97316; font-family: sans-serif; text-align: center;'>Neural Newz</h1><p style='color: #fff; text-align: center; font-family: sans-serif;'>No major updates in the last 24 hours.</p>"
        
    print("Generating newsletter HTML...")
    
    spotify_url = "https://open.spotify.com/show/0333gy3Hgpg1RIR6RtNrtgX?si=8Uc0NxrdRpOR71wqg8_n5Q"
    
    html = f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0a0a0a; color: #ffffff; padding: 30px; border-radius: 12px; border: 1px solid #222;">
        
        <table width="100%" style="margin-bottom: 10px; border-collapse: collapse;">
            <tr>
                <td style="text-align: left; vertical-align: middle;">
                    <div style="display: inline-block; background-color: #F97316; color: #000; font-weight: 900; padding: 10px 14px; border-radius: 8px; font-size: 18px;">NN</div>
                </td>
                <td style="text-align: right; vertical-align: middle;">
                    <a href="{spotify_url}" style="background-color: #F97316; color: #000; padding: 6px 12px; text-decoration: none; border-radius: 99px; font-weight: 700; font-size: 12px;">🎧 Listen on Spotify</a>
                </td>
            </tr>
        </table>

        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;">Neural Newz</h1>
            <p style="color: #F97316; margin-top: 8px; font-size: 14px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Daily AI Intelligence</p>
        </div>
    """
    
    if is_welcome:
        html += """
        <div style="margin-bottom: 30px; padding: 20px; background-color: #111; border-left: 4px solid #F97316; border-radius: 0 8px 8px 0;">
            <h2 style="margin-top: 0; font-size: 20px;">Welcome to the club.</h2>
            <p style="color: #bbb; line-height: 1.6; margin-bottom: 0;">You're now subscribed to Neural Newz. To get you started instantly, here is a custom briefing on the absolute latest AI breakthroughs from the past 24 hours up to this very minute.</p>
        </div>
        """

    html += "<h2 style='color: #ffffff; font-size: 22px; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px;'>📰 Today's Intelligence</h2><div style='display: block;'>"
    for item in content_items:
        details = item.get('detailed_analysis', item.get('summary', ''))
        if len(details) > 600:
            details = details[:600] + "..."
            
        html += f"""
        <div style="background-color: #111; padding: 20px; border-radius: 10px; border: 1px solid #222; margin-bottom: 20px;">
            <span style="display: inline-block; background-color: rgba(249,115,22,0.15); color: #F97316; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; margin-bottom: 10px;">{item['source']}</span><br/>
            <a href="{item['link']}" style="font-size: 18px; color: #ffffff; font-weight: 700; text-decoration: none; line-height: 1.4; display: block; margin-bottom: 10px;">{item['title']}</a>
            <p style="font-size: 14px; line-height: 1.6; color: #aaa; margin: 0;">{details}</p>
        </div>
        """
    html += "</div>"
        
    html += """
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; text-align: center;">
            <p style="font-size: 12px; color: #666; margin: 0;">Neural Newz Automation · Built with AI</p>
            <p style="font-size: 11px; color: #555; margin-top: 8px;">You are receiving this because you subscribed to Neural Newz.</p>
        </div>
    </div>
    """
    
    return html

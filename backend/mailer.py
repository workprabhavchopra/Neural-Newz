import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def send_daily_newsletter(html_content, subject="Neural News Daily Intelligence"):
    """
    Sends the HTML newsletter to the subscriber audience via Resend.
    """
    if not resend.api_key:
        print("Resend API key not configured. Skipping email.")
        return False
        
    # In a real scenario, you would send this to an Audience ID using Resend Broadcasts
    # Or iterate over a database of subscribers.
    # For now, we will send to a designated "SUBSCRIBERS_EMAIL" env var (can be a comma-separated list)
    subscribers = os.getenv("SUBSCRIBERS_EMAIL", "test@example.com").split(",")
    
    print(f"Sending email newsletter to {len(subscribers)} subscribers...")
    
    try:
        # Resend free tier requires a verified domain to send FROM.
        # Ensure FROM_EMAIL is something like 'newsletter@yourdomain.com'
        from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev") 
        
        response = resend.Emails.send({
            "from": f"Neural News <{from_email}>",
            "to": subscribers,
            "subject": subject,
            "html": html_content
        })
        
        print(f"Email sent successfully. ID: {response.get('id')}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

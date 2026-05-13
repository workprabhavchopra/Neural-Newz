import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def send_daily_newsletter(html_content, subject="Neural Newz Daily Intelligence"):
    """
    Sends the HTML newsletter to the subscriber audience via Resend.
    """
    if not resend.api_key:
        print("Resend API key not configured. Skipping email.")
        return False
        
    subscribers = os.getenv("SUBSCRIBERS_EMAIL", "test@example.com").split(",")
    
    print(f"Sending email newsletter to {len(subscribers)} subscribers...")
    
    try:
        from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
        
        response = resend.Emails.send({
            "from": f"Neural Newz <{from_email}>",
            "to": subscribers,
            "subject": subject,
            "html": html_content
        })
        
        print(f"Email sent successfully. ID: {response.get('id')}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

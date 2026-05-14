import os
import resend
from dotenv import load_dotenv
from fetcher import fetch_all_daily_content
from summarizer import generate_newsletter_html

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

def send_instant_welcome():
    if not resend.api_key:
        print("Resend API key not configured. Exiting.")
        return

    target_email = os.getenv("TARGET_EMAIL")
    if not target_email:
        print("TARGET_EMAIL not provided in environment variables. Exiting.")
        return

    print(f"Starting instant welcome workflow for: {target_email}")
    
    # Fetch absolute latest news right now
    content = fetch_all_daily_content()
    
    # Generate the newsletter HTML with the welcome flag
    html_content = generate_newsletter_html(content, is_welcome=True)
    
    # Send the email specifically to the new subscriber
    from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
    subject = "Welcome to Neural Newz! Here is your first briefing."
    
    try:
        response = resend.Emails.send({
            "from": f"Neural Newz <{from_email}>",
            "to": target_email,
            "subject": subject,
            "html": html_content
        })
        print(f"Welcome email successfully sent to {target_email}. ID: {response.get('id')}")
    except Exception as e:
        print(f"Error sending welcome email to {target_email}: {e}")

if __name__ == "__main__":
    send_instant_welcome()

import { NextResponse } from 'next/server';
import { Resend } from 'resend';

// Initialize conditionally to avoid crashing if the key is missing during local testing
const resendApiKey = process.env.RESEND_API_KEY;
const resend = resendApiKey ? new Resend(resendApiKey) : null;

export async function POST(request: Request) {
  try {
    if (!resend) {
      return NextResponse.json(
        { error: 'Server configuration error: RESEND_API_KEY is missing. Please add it to your environment variables.' }, 
        { status: 500 }
      );
    }
    const { email } = await request.json();

    if (!email) {
      return NextResponse.json({ error: 'Email is required' }, { status: 400 });
    }

    const audienceId = process.env.RESEND_AUDIENCE_ID;

    if (audienceId) {
      // Add to Audience List
      await resend.contacts.create({
        email: email,
        unsubscribed: false,
        audienceId: audienceId,
      });
    } else {
      // Fallback: Send a welcome email directly if no Audience ID is configured
      await resend.emails.send({
        from: 'Neural Newz <onboarding@resend.dev>', // Change to your verified domain in production
        to: email,
        subject: 'Welcome to Neural Newz!',
        html: '<div style="font-family: sans-serif; text-align: center;"><h1 style="color: #4F46E5;">Welcome!</h1><p>You are now subscribed to Neural Newz daily AI intelligence updates.</p></div>'
      });
    }

    // Trigger GitHub Action to send instant welcome newsletter
    const githubPat = process.env.GITHUB_PAT;
    if (githubPat) {
      try {
        await fetch('https://api.github.com/repos/workprabhavchopra/Neural-Newz/dispatches', {
          method: 'POST',
          headers: {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': `token ${githubPat}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            event_type: 'welcome_subscriber',
            client_payload: { email: email }
          })
        });
      } catch (err) {
        console.error('Failed to trigger GitHub Action:', err);
        // We don't fail the subscription if the welcome email trigger fails
      }
    } else {
      console.warn('GITHUB_PAT not set. Skipping instant welcome email dispatch.');
    }

    return NextResponse.json({ success: true, message: 'Successfully subscribed' });
  } catch (error) {
    console.error('Subscription error:', error);
    return NextResponse.json({ error: 'Failed to subscribe. Please try again later.' }, { status: 500 });
  }
}

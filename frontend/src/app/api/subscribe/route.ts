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
        from: 'Neural News <onboarding@resend.dev>', // Change to your verified domain in production
        to: email,
        subject: 'Welcome to Neural News!',
        html: '<div style="font-family: sans-serif; text-align: center;"><h1 style="color: #4F46E5;">Welcome!</h1><p>You are now subscribed to Neural News daily AI intelligence updates.</p></div>'
      });
    }

    return NextResponse.json({ success: true, message: 'Successfully subscribed' });
  } catch (error) {
    console.error('Subscription error:', error);
    return NextResponse.json({ error: 'Failed to subscribe. Please try again later.' }, { status: 500 });
  }
}

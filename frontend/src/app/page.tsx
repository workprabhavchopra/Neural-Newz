"use client";

import { useState, useEffect, useRef } from "react";

// ─── Icons (inline SVG to avoid lucide dep issues) ───────────────────────────
const SpotifyIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
  </svg>
);

const PlayIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path d="M8 5v14l11-7z"/>
  </svg>
);

const MailIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
    <rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
  </svg>
);

const CheckIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="w-5 h-5">
    <path d="M20 6 9 17l-5-5"/>
  </svg>
);

const ArrowIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4 transition-transform group-hover:translate-x-1">
    <path d="M5 12h14M12 5l7 7-7 7"/>
  </svg>
);

const HeadphonesIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-6 h-6">
    <path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>
  </svg>
);

const ZapIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-6 h-6">
    <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
  </svg>
);

const BrainIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-6 h-6">
    <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/>
  </svg>
);

// ─── Sources Ticker ───────────────────────────────────────────────────────────
const SOURCES = [
  "OpenAI", "Google DeepMind", "Anthropic", "Meta AI", "Mistral",
  "Hugging Face", "Stability AI", "ArXiv", "a16z", "Cohere",
  "xAI", "Inflection", "Runway ML", "Scale AI", "Nvidia Research"
];


// ─── Main Page ────────────────────────────────────────────────────────────────
export default function Home() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");
  const [hasSubscribed, setHasSubscribed] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Persist subscription state in localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("nn_subscribed");
      if (stored === "true") setHasSubscribed(true);
    }
  }, []);

  const handleSubscribe = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (res.ok) {
        setStatus("success");
        setMessage("You're in! Check your inbox for a welcome email.");
        setEmail("");
        setHasSubscribed(true);
        localStorage.setItem("nn_subscribed", "true");
      } else {
        setStatus("error");
        setMessage(data.error || "Something went wrong. Try again.");
      }
    } catch {
      setStatus("error");
      setMessage("Network error. Please try again.");
    }
  };

  const doubledSources = [...SOURCES, ...SOURCES];

  return (
    <div style={{ background: "var(--bg)", color: "var(--white)", minHeight: "100vh" }}>

      {/* ── NAV ── */}
      <nav style={{
        position: "fixed", top: 0, width: "100%", zIndex: 50,
        borderBottom: "1px solid var(--border)",
        background: "rgba(10,10,10,0.85)", backdropFilter: "blur(16px)"
      }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px", height: 64, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          {/* Logo */}
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{
              width: 32, height: 32, background: "var(--orange)", borderRadius: 8,
              display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0
            }}>
              <span style={{ color: "#000", fontWeight: 900, fontSize: 14, letterSpacing: "-0.5px" }}>NN</span>
            </div>
            <span style={{ fontWeight: 700, fontSize: 17, letterSpacing: "-0.3px" }}>Neural Newz</span>
          </div>

          {/* Nav Actions */}
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            {hasSubscribed && (
              <a
                href="https://open.spotify.com"
                target="_blank"
                rel="noopener noreferrer"
                className="animate-slide-right"
                style={{
                  display: "flex", alignItems: "center", gap: 8,
                  background: "#1DB954", color: "#000",
                  fontWeight: 700, fontSize: 13, padding: "8px 16px",
                  borderRadius: 8, textDecoration: "none",
                  transition: "all 0.2s ease"
                }}
                onMouseEnter={e => (e.currentTarget.style.transform = "translateY(-1px)")}
                onMouseLeave={e => (e.currentTarget.style.transform = "translateY(0)")}
              >
                <SpotifyIcon />
                Listen on Spotify
              </a>
            )}
            <a
              href="#subscribe"
              style={{
                fontSize: 13, fontWeight: 600,
                color: "var(--white)",
                border: "1px solid var(--border)",
                padding: "8px 16px", borderRadius: 8,
                textDecoration: "none",
                transition: "all 0.2s ease",
                background: "transparent"
              }}
              onMouseEnter={e => {
                e.currentTarget.style.borderColor = "var(--orange)";
                e.currentTarget.style.color = "var(--orange)";
              }}
              onMouseLeave={e => {
                e.currentTarget.style.borderColor = "var(--border)";
                e.currentTarget.style.color = "var(--white)";
              }}
            >
              Subscribe Free
            </a>
          </div>
        </div>
      </nav>

      <main style={{ paddingTop: 64 }}>

        {/* ── HERO ── */}
        <section style={{ maxWidth: 1200, margin: "0 auto", padding: "80px 24px 64px", position: "relative" }}>
          {/* Orange glow blob */}
          <div style={{
            position: "absolute", top: "30%", left: "50%", transform: "translate(-50%,-50%)",
            width: 500, height: 500,
            background: "radial-gradient(circle, rgba(249,115,22,0.12) 0%, transparent 70%)",
            borderRadius: "50%", pointerEvents: "none",
            animation: "glow-breathe 6s ease-in-out infinite"
          }} />

          <div style={{ position: "relative", zIndex: 1, textAlign: "center" }}>

            {/* Live badge */}
            <div className="animate-fade-up" style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              padding: "6px 14px", borderRadius: 99,
              border: "1px solid rgba(249,115,22,0.3)",
              background: "rgba(249,115,22,0.08)",
              marginBottom: 32, fontSize: 12, fontWeight: 600,
              color: "var(--orange)", letterSpacing: "0.08em", textTransform: "uppercase"
            }}>
              <span className="pulse-dot" style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--orange)", display: "inline-block" }} />
              Daily at 6 PM IST · Fully Automated
            </div>

            {/* Headline */}
            <h1 className="animate-fade-up delay-100" style={{
              fontSize: "clamp(42px, 7vw, 88px)",
              fontWeight: 900, lineHeight: 1.0,
              letterSpacing: "-0.04em", marginBottom: 24,
              fontFamily: "'Inter', sans-serif"
            }}>
              AI moves fast.<br />
              <span style={{
                background: "linear-gradient(135deg, var(--orange) 0%, #fff 60%)",
                WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent"
              }}>
                We move faster.
              </span>
            </h1>

            {/* Sub */}
            <p className="animate-fade-up delay-200" style={{
              fontSize: "clamp(16px, 2vw, 20px)",
              color: "var(--muted)", maxWidth: 560, margin: "0 auto 48px",
              lineHeight: 1.65, fontWeight: 400
            }}>
              Every evening, we scan the world&apos;s top AI labs, research papers, and VC firms —
              and distill it into one sharp podcast and newsletter.
            </p>

            {/* Subscribe Form */}
            <div id="subscribe" className="animate-fade-up delay-300" style={{ maxWidth: 480, margin: "0 auto" }}>
              {status === "success" ? (
                <div style={{
                  background: "rgba(249,115,22,0.08)",
                  border: "1px solid rgba(249,115,22,0.3)",
                  borderRadius: 12, padding: "18px 24px",
                  display: "flex", alignItems: "center", justifyContent: "center", gap: 10,
                  color: "var(--orange)", fontWeight: 600
                }}>
                  <CheckIcon />
                  {message}
                </div>
              ) : (
                <form onSubmit={handleSubscribe} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                  <div style={{ position: "relative" }}>
                    <span style={{ position: "absolute", left: 16, top: "50%", transform: "translateY(-50%)", color: "var(--muted-2)" }}>
                      <MailIcon />
                    </span>
                    <input
                      ref={inputRef}
                      type="email"
                      value={email}
                      onChange={e => setEmail(e.target.value)}
                      placeholder="your@email.com"
                      required
                      disabled={status === "loading"}
                      style={{
                        width: "100%", padding: "15px 16px 15px 48px",
                        background: "var(--surface)", border: "1px solid var(--border)",
                        borderRadius: 10, color: "var(--white)", fontSize: 15,
                        outline: "none", transition: "border-color 0.2s",
                        fontFamily: "inherit"
                      }}
                      onFocus={e => (e.target.style.borderColor = "var(--orange)")}
                      onBlur={e => (e.target.style.borderColor = "var(--border)")}
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={status === "loading"}
                    className="btn-orange group"
                    style={{
                      width: "100%", padding: "15px",
                      fontSize: 15, fontWeight: 700,
                      display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
                      border: "none", cursor: status === "loading" ? "not-allowed" : "pointer",
                      opacity: status === "loading" ? 0.7 : 1
                    }}
                  >
                    {status === "loading" ? (
                      <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <svg className="animate-spin" style={{ width: 18, height: 18 }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
                        </svg>
                        Subscribing...
                      </span>
                    ) : (
                      <>
                        Get the Daily Brief — Free
                        <ArrowIcon />
                      </>
                    )}
                  </button>
                </form>
              )}
              {status === "error" && (
                <p style={{ color: "#f87171", fontSize: 13, marginTop: 8, textAlign: "center" }}>{message}</p>
              )}
              <p style={{ color: "var(--muted-2)", fontSize: 12, marginTop: 12 }}>
                Join engineers, researchers & founders. No spam. Unsubscribe anytime.
              </p>
            </div>
          </div>
        </section>

        {/* ── MARQUEE TICKER ── */}
        <div style={{
          borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)",
          overflow: "hidden", padding: "12px 0", marginBottom: 80,
          background: "var(--surface)"
        }}>
          <div className="marquee-track" style={{ display: "flex", whiteSpace: "nowrap", width: "max-content" }}>
            {doubledSources.map((s, i) => (
              <span key={i} style={{
                display: "inline-flex", alignItems: "center", gap: 20,
                fontSize: 12, fontWeight: 600, letterSpacing: "0.12em",
                textTransform: "uppercase", color: "var(--muted)",
                padding: "0 32px"
              }}>
                {s}
                <span style={{ color: "var(--orange)", fontSize: 8 }}>●</span>
              </span>
            ))}
          </div>
        </div>

        {/* ── FEATURES ── */}
        <section style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px 80px" }}>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16 }}>
            {[
              {
                icon: <BrainIcon />, label: "Autonomous Research",
                desc: "Our AI agent scans OpenAI, DeepMind, Anthropic, arXiv, and top VC firms every single day — so you never miss a breakthrough."
              },
              {
                icon: <HeadphonesIcon />, label: "10-20 Min Deep Dives",
                desc: "Not a surface-level summary. Every episode is a structured, expert-level breakdown of why today's news actually matters."
              },
              {
                icon: <ZapIcon />, label: "Zero Noise",
                desc: "No clickbait. No filler. No speculation. Just verified technical developments from the world's leading AI sources."
              }
            ].map((f, i) => (
              <div
                key={i}
                className={`feature-card animate-fade-up delay-${(i + 3) * 100}`}
              >
                <div className="feature-icon" style={{
                  width: 48, height: 48, borderRadius: 12,
                  display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 20
                }}>
                  {f.icon}
                </div>
                <h3 style={{ fontWeight: 700, fontSize: 18, marginBottom: 10, letterSpacing: "-0.02em" }}>{f.label}</h3>
                <p style={{ color: "var(--muted)", lineHeight: 1.65, fontSize: 14 }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </section>



      </main>

      {/* ── FOOTER ── */}
      <footer style={{ borderTop: "1px solid var(--border)", padding: "40px 24px" }}>
        <div style={{
          maxWidth: 1200, margin: "0 auto",
          display: "flex", flexWrap: "wrap", alignItems: "center", justifyContent: "space-between",
          gap: 16
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{
              width: 28, height: 28, background: "var(--orange)", borderRadius: 6,
              display: "flex", alignItems: "center", justifyContent: "center"
            }}>
              <span style={{ color: "#000", fontWeight: 900, fontSize: 11 }}>NN</span>
            </div>
            <span style={{ fontWeight: 700, fontSize: 15 }}>Neural Newz</span>
          </div>
          <p style={{ color: "var(--muted-2)", fontSize: 13 }}>
            © {new Date().getFullYear()} Neural Newz · Fully automated · Built with AI
          </p>
          <div style={{ display: "flex", gap: 24 }}>
            <a href="https://open.spotify.com" target="_blank" rel="noopener noreferrer"
              style={{ color: "var(--muted)", fontSize: 13, textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={e => (e.currentTarget.style.color = "var(--orange)")}
              onMouseLeave={e => (e.currentTarget.style.color = "var(--muted)")}>
              Spotify
            </a>
            <a href="/feed.xml" target="_blank" rel="noopener noreferrer"
              style={{ color: "var(--muted)", fontSize: 13, textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={e => (e.currentTarget.style.color = "var(--orange)")}
              onMouseLeave={e => (e.currentTarget.style.color = "var(--muted)")}>
              RSS Feed
            </a>
          </div>
        </div>
      </footer>

    </div>
  );
}

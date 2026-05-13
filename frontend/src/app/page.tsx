"use client";

import { useState } from "react";
import { Headphones, Mail, Sparkles, Zap, BrainCircuit, ArrowRight, Loader2, CheckCircle } from "lucide-react";

export default function Home() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

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
        setMessage("You're in! Welcome to the club.");
        setEmail("");
      } else {
        setStatus("error");
        setMessage(data.error || "Something went wrong.");
      }
    } catch {
      setStatus("error");
      setMessage("Network error. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-black text-slate-200 selection:bg-indigo-500/30 font-sans">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-black/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BrainCircuit className="w-6 h-6 text-indigo-500" />
            <span className="font-semibold text-lg tracking-tight text-white">Neural Newz</span>
          </div>
          <div className="flex items-center gap-4">
            <a href="#subscribe" className="text-sm font-medium bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-full transition-all">
              Subscribe
            </a>
          </div>
        </div>
      </nav>

      <main className="pt-32 pb-20">
        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-6 relative">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />
          
          <div className="relative z-10 flex flex-col items-center text-center space-y-8 mt-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-medium">
              <Sparkles className="w-4 h-4" />
              <span>Daily AI Intelligence, Distilled</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white max-w-4xl">
              The noise of AI, <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
                turned into signal.
              </span>
            </h1>
            
            <p className="text-lg md:text-xl text-slate-400 max-w-2xl leading-relaxed">
              We monitor the top AI labs, VC firms, and research papers daily. 
              Get a concise, expertly narrated podcast and newsletter delivered straight to you.
            </p>

            <div id="subscribe" className="w-full max-w-md mt-8">
              {status === "success" ? (
                <div className="bg-green-500/10 border border-green-500/20 text-green-400 rounded-xl p-4 flex items-center justify-center gap-2">
                  <CheckCircle className="w-5 h-5" />
                  <span className="font-medium">{message}</span>
                </div>
              ) : (
                <form onSubmit={handleSubscribe} className="flex flex-col sm:flex-row gap-3">
                  <div className="relative flex-1">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                    <input 
                      type="email" 
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@example.com"
                      required
                      disabled={status === "loading"}
                      className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all disabled:opacity-50"
                    />
                  </div>
                  <button 
                    type="submit"
                    disabled={status === "loading"}
                    className="bg-white text-black font-semibold py-3 px-6 rounded-xl hover:bg-slate-200 transition-colors flex items-center justify-center gap-2 group disabled:opacity-50 min-w-[140px]"
                  >
                    {status === "loading" ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <>
                        Join Free
                        <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                      </>
                    )}
                  </button>
                </form>
              )}
              {status === "error" && (
                <p className="text-red-400 text-sm mt-2 text-center">{message}</p>
              )}
            </div>
            
            <p className="text-sm text-slate-500">Join engineers, researchers, and founders.</p>
          </div>
        </section>

        {/* Features Section */}
        <section className="max-w-7xl mx-auto px-6 mt-40">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-indigo-500/30 transition-colors group">
              <div className="w-12 h-12 bg-indigo-500/20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <BrainCircuit className="w-6 h-6 text-indigo-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Curated Intelligence</h3>
              <p className="text-slate-400 leading-relaxed">
                We track OpenAI, DeepMind, Anthropic, a16z, and arXiv so you don&apos;t miss a single breakthrough.
              </p>
            </div>
            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-purple-500/30 transition-colors group">
              <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Headphones className="w-6 h-6 text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Studio Quality Podcast</h3>
              <p className="text-slate-400 leading-relaxed">
                Listen on Spotify or Apple Podcasts. Get your daily AI news while commuting.
              </p>
            </div>
            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-pink-500/30 transition-colors group">
              <div className="w-12 h-12 bg-pink-500/20 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Zap className="w-6 h-6 text-pink-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Zero Fluff</h3>
              <p className="text-slate-400 leading-relaxed">
                No clickbait. No filler. Just the technical details, papers, and product releases that matter.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-white/10 py-10 mt-10">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between text-slate-500 text-sm">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <BrainCircuit className="w-5 h-5 text-indigo-500" />
            <span className="font-semibold text-white">Neural Newz</span>
          </div>
          <p>© {new Date().getFullYear()} Neural Newz Automation. Built with AI.</p>
        </div>
      </footer>
    </div>
  );
}

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Search,
  ArrowRight,
  Mic,
  X,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

const SUGGESTED_QUESTIONS = [
  "What exams are coming up?",
  "What is happening on campus today?",
  "When is the next placement drive?",
  "Is there any event in the library today?",
  "Explain my study topic",
  "Show today's announcements",
];

export function HeroSection() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [voiceNotice, setVoiceNotice] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    router.push(`/assistant?q=${encodeURIComponent(query.trim())}`);
  };

  const handleChipClick = (question: string) => {
    setQuery(question);
  };

  const handleVoiceClick = () => {
    setVoiceNotice(true);
    setTimeout(() => setVoiceNotice(false), 3000);
  };

  return (
    <section className="relative bg-navy-800 text-white pt-10 pb-16 sm:pt-14 sm:pb-20 border-b border-navy-700">
      {/* Subtle institutional grid watermark background */}
      <div
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h40v40H0V0zm1 1h38v38H1V1z' fill='%23ffffff' fill-rule='evenodd'/%3E%3C/svg%3E")`,
        }}
        aria-hidden="true"
      />

      <div className="relative section-container max-w-4xl mx-auto text-center">
        {/* Small institutional label */}
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-navy-700/80 border border-navy-600/70 rounded-full text-caption text-navy-200 mb-5">
          <span className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" aria-hidden="true" />
          <span className="font-semibold tracking-wider uppercase text-[11px] text-gold-300">
            COLLEGE INTELLIGENT PORTAL
          </span>
        </div>

        {/* Main heading */}
        <h1 className="text-h1 sm:text-display text-white font-bold tracking-tight mb-3">
          How can we help you today?
        </h1>

        {/* Supporting text */}
        <p className="text-body sm:text-body-lg text-navy-200 max-w-2xl mx-auto mb-8 font-normal leading-relaxed">
          Ask about academics, examinations, campus services, study materials,
          events, or anything you need to know about college.
        </p>

        {/* Main Chatbox Input Container */}
        <div className="relative max-w-3xl mx-auto mb-4">
          <form
            onSubmit={handleSubmit}
            className="relative flex items-center bg-white rounded-xl shadow-lg border-2 border-navy-300/40 focus-within:border-gold-500 focus-within:ring-4 focus-within:ring-gold-500/20 transition-all duration-200"
          >
            <div className="pl-4 sm:pl-5 text-slate-400">
              <Search className="w-5 h-5 text-slate-400" aria-hidden="true" />
            </div>

            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything about your college..."
              className="w-full py-4 pl-3 pr-24 text-body text-slate-800 placeholder-slate-400 bg-transparent focus:outline-none"
              aria-label="Ask anything about your college"
            />

            {/* Clear Input Button */}
            {query && (
              <button
                type="button"
                onClick={() => setQuery("")}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-md transition-colors"
                aria-label="Clear input"
              >
                <X className="w-4 h-4" />
              </button>
            )}

            {/* Voice Input Placeholder Button */}
            <div className="relative">
              <button
                type="button"
                onClick={handleVoiceClick}
                className="p-2 mr-1 text-slate-400 hover:text-navy-700 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
                title="Voice input (UI placeholder)"
                aria-label="Voice input"
              >
                <Mic className="w-5 h-5" />
              </button>
              {voiceNotice && (
                <div className="absolute right-0 -bottom-10 bg-slate-900 text-white text-caption py-1 px-2.5 rounded shadow-lg whitespace-nowrap z-20">
                  Voice input will be enabled in Phase 4
                </div>
              )}
            </div>

            {/* Submit / Ask Button */}
            <button
              type="submit"
              disabled={!query.trim()}
              className="m-1.5 px-4 sm:px-5 py-2.5 bg-gold-500 hover:bg-gold-600 active:bg-gold-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-medium text-body-sm rounded-lg flex items-center gap-1.5 transition-colors cursor-pointer shadow-sm"
              aria-label="Send question to assistant"
            >
              <span>Ask</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Trust indicator */}
          <div className="mt-3 flex items-center justify-center gap-1.5 text-caption text-navy-300">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" aria-hidden="true" />
            <span>Answers are grounded in official college information.</span>
          </div>
        </div>

        {/* Suggested Question Chips */}
        <div className="max-w-3xl mx-auto pt-4 text-left">
          <div className="flex items-center gap-1.5 mb-2.5 text-caption font-semibold uppercase tracking-wider text-navy-300">
            <Sparkles className="w-3.5 h-3.5 text-gold-400" aria-hidden="true" />
            <span>Suggested questions:</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {SUGGESTED_QUESTIONS.map((question) => (
              <button
                key={question}
                type="button"
                onClick={() => handleChipClick(question)}
                className="text-left px-3.5 py-1.5 bg-navy-700/70 hover:bg-navy-700 active:bg-navy-600 border border-navy-600/70 hover:border-gold-500/50 rounded-lg text-body-sm text-navy-100 hover:text-white transition-all duration-150 cursor-pointer"
              >
                &ldquo;{question}&rdquo;
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

"use client";

import { CampusAIChatbox } from "@/components/chat";

export function HeroSection() {
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
          Ask about academics, examinations, campus services, regulations,
          schedules, or anything you need to know about college.
        </p>

        {/* Real Live AI Chatbox Component */}
        <div className="relative max-w-3xl mx-auto mb-4">
          <CampusAIChatbox />
        </div>
      </div>
    </section>
  );
}

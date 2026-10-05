"use client";

import { useState } from "react";
import {
  Search,
  ArrowRight,
  ShieldCheck,
  Sparkles,
  AlertCircle,
  RotateCcw,
  Loader2,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { sendChatMessage, type ChatResponse, type ChatSource } from "@/lib/api";
import { CleanAnswerRenderer } from "./CleanAnswerRenderer";

const SUGGESTED_QUESTIONS = [
  "What is the attendance requirement?",
  "What are the examination regulations?",
  "What is the academic calendar?",
  "What are the hostel rules?",
  "What is relative grading?",
];

interface CampusAIChatboxProps {
  initialQuery?: string;
  autoFocus?: boolean;
}

export function CampusAIChatbox({ initialQuery = "", autoFocus = false }: CampusAIChatboxProps) {
  const [query, setQuery] = useState(initialQuery);
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedSources, setExpandedSources] = useState(false);

  const executeSearch = async (searchQuery: string) => {
    const q = searchQuery.trim();
    if (!q) return;

    setCurrentQuestion(q);
    setLoading(true);
    setError(null);
    setResponse(null);
    setExpandedSources(false);

    try {
      const data = await sendChatMessage(q);
      setResponse(data);
    } catch (err) {
      console.error("Chat service error:", err);
      setError("CampusAI is temporarily unable to reach the AI service. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    executeSearch(query);
  };

  const handleChipClick = (question: string) => {
    setQuery(question);
    executeSearch(question);
  };

  const handleReset = () => {
    setQuery("");
    setCurrentQuestion("");
    setResponse(null);
    setError(null);
  };

  return (
    <div className="w-full">
      {/* Search Input Bar */}
      <form
        onSubmit={handleSubmit}
        className="relative flex items-center bg-white rounded-xl shadow-md border-2 border-navy-300/40 focus-within:border-gold-500 focus-within:ring-4 focus-within:ring-gold-500/20 transition-all duration-200"
      >
        <div className="pl-4 sm:pl-5 text-slate-400">
          <Search className="w-5 h-5 text-slate-400" aria-hidden="true" />
        </div>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask anything about your college..."
          autoFocus={autoFocus}
          className="w-full py-4 pl-3 pr-20 text-body text-slate-900 placeholder-slate-400 bg-transparent focus:outline-none"
          aria-label="Ask anything about your college"
        />

        {/* Submit / Ask Button */}
        <button
          type="submit"
          disabled={!query.trim() || loading}
          className="m-1.5 px-4 sm:px-5 py-2.5 bg-gold-500 hover:bg-gold-600 active:bg-gold-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-medium text-body-sm rounded-lg flex items-center gap-1.5 transition-colors cursor-pointer shadow-sm"
          aria-label="Ask assistant"
        >
          {loading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <>
              <span>Ask</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </form>

      {/* Trust indicator */}
      <div className="mt-2.5 flex items-center justify-center gap-1.5 text-caption text-navy-200 sm:text-navy-300">
        <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" aria-hidden="true" />
        <span>Answers are grounded strictly in official college documents.</span>
      </div>

      {/* Suggested Prompt Chips */}
      <div className="pt-4 text-left">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-1.5 text-caption font-semibold uppercase tracking-wider text-navy-200 sm:text-navy-300">
            <Sparkles className="w-3.5 h-3.5 text-gold-400" aria-hidden="true" />
            <span>Suggested questions:</span>
          </div>

          {(currentQuestion || response || error) && (
            <button
              type="button"
              onClick={handleReset}
              className="inline-flex items-center gap-1 text-caption text-gold-300 hover:text-gold-200 transition-colors cursor-pointer"
            >
              <RotateCcw className="w-3 h-3" />
              <span>New Question</span>
            </button>
          )}
        </div>

        <div className="flex flex-wrap gap-2">
          {SUGGESTED_QUESTIONS.map((question) => (
            <button
              key={question}
              type="button"
              onClick={() => handleChipClick(question)}
              disabled={loading}
              className="text-left px-3 py-1.5 bg-navy-700/70 hover:bg-navy-700 active:bg-navy-600 border border-navy-600/70 hover:border-gold-500/50 rounded-lg text-body-sm text-navy-100 hover:text-white transition-all duration-150 cursor-pointer disabled:opacity-50"
            >
              &ldquo;{question}&rdquo;
            </button>
          ))}
        </div>
      </div>

      {/* Live Question & Answer Card */}
      {(loading || currentQuestion || response || error) && (
        <div className="mt-6 text-left bg-white text-slate-800 rounded-xl shadow-xl border border-slate-200 overflow-hidden transition-all duration-300">
          {/* Active Query Header */}
          <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-gold-500" />
              <span className="text-caption font-semibold text-navy-700 uppercase tracking-wider">
                Question
              </span>
            </div>
            {response && (
              <span className="inline-flex items-center gap-1 text-caption font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                <ShieldCheck className="w-3 h-3" />
                Grounded in Official Regulations
              </span>
            )}
          </div>

          <div className="p-5 sm:p-6">
            <p className="text-body-lg font-semibold text-navy-900 mb-4">
              &ldquo;{currentQuestion}&rdquo;
            </p>

            {/* Loading State */}
            {loading && (
              <div className="py-6 flex flex-col items-center justify-center gap-3 text-slate-600">
                <Loader2 className="w-7 h-7 text-gold-500 animate-spin" />
                <p className="text-body font-medium text-navy-800 animate-pulse">
                  Searching official college information...
                </p>
                <p className="text-caption text-slate-500">
                  Retrieving regulatory sections and generating grounded response
                </p>
              </div>
            )}

            {/* Error State */}
            {error && (
              <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-body-sm text-red-900 mb-0.5">Connection Issue</h4>
                  <p className="text-body-sm">{error}</p>
                </div>
              </div>
            )}

            {/* Generated Answer */}
            {response && !loading && (
              <div>
                {/* Direct Answer Presentation */}
                <div className="mb-4">
                  <CleanAnswerRenderer content={response.answer} />
                </div>

                {/* Minimal Collapsed-by-Default Sources Section */}
                {response.sources && response.sources.length > 0 && (
                  <div className="pt-3 border-t border-slate-200 mt-4">
                    <button
                      type="button"
                      onClick={() => setExpandedSources(!expandedSources)}
                      className="inline-flex items-center gap-1.5 text-caption font-medium text-slate-500 hover:text-navy-800 transition-colors cursor-pointer select-none"
                      aria-expanded={expandedSources}
                    >
                      <span>Sources</span>
                      <span className="text-[11px] px-1.5 py-0.2 bg-slate-100 text-slate-600 rounded-full font-semibold">
                        {response.sources.length}
                      </span>
                      {expandedSources ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>

                    {expandedSources && (
                      <div className="mt-2.5 space-y-1.5 pl-2.5 border-l-2 border-slate-200">
                        {response.sources.map((src: ChatSource, idx: number) => (
                          <div
                            key={`${src.document_name}-${src.page_number || idx}`}
                            className="text-caption text-slate-600 flex flex-wrap items-baseline gap-1.5 py-0.5"
                          >
                            <span className="text-slate-400">•</span>
                            <span className="font-medium text-slate-800">{src.document_name}</span>
                            {src.page_number && <span className="text-slate-500">— Page {src.page_number}</span>}
                            {src.regulation && (
                              <span className="text-[11px] px-1.5 py-0.2 bg-navy-50 text-navy-700 font-medium rounded">
                                {src.regulation}
                              </span>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

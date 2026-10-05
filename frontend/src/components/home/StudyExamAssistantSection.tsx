import Link from "next/link";
import {
  BookOpen,
  HelpCircle,
  FileCheck,
  GraduationCap,
  Sparkles,
  ArrowRight,
} from "lucide-react";
import { Section, SectionHeading, Card, Badge } from "@/components/ui";

interface StudyCapability {
  title: string;
  description: string;
  examplePrompt: string;
  icon: typeof BookOpen;
  badge: string;
}

const STUDY_CAPABILITIES: StudyCapability[] = [
  {
    title: "Explain a Topic",
    description:
      "Break down difficult engineering theories, algorithm mechanics, or technical definitions into plain, step-by-step explanations.",
    examplePrompt: "Explain Virtual Memory & Page Faults with an example",
    icon: BookOpen,
    badge: "Conceptual Clarity",
  },
  {
    title: "Practice MCQs",
    description:
      "Generate unit-wise practice multiple-choice questions, gate-level questions, and conceptual quizzes from your syllabus.",
    examplePrompt: "Generate 5 MCQs on Thermodynamics 2nd Law",
    icon: HelpCircle,
    badge: "Self Assessment",
  },
  {
    title: "Summarize Notes",
    description:
      "Condense lengthy lecture transcripts, research papers, and textbook chapters into high-yield revision summaries.",
    examplePrompt: "Summarize the key differences between TCP and UDP",
    icon: FileCheck,
    badge: "Quick Revision",
  },
  {
    title: "Prepare for Exams",
    description:
      "Identify high-weightage topics, review past question patterns, and practice structured answers for upcoming semester exams.",
    examplePrompt: "What are the most frequent 16-mark questions in DBMS?",
    icon: GraduationCap,
    badge: "Exam Readiness",
  },
];

export function StudyExamAssistantSection() {
  return (
    <Section background="light" id="study-assistant">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
        <div>
          <div className="inline-flex items-center gap-2 mb-2 text-caption font-semibold uppercase tracking-wider text-gold-700">
            <Sparkles className="w-3.5 h-3.5 text-gold-600" />
            <span>Academic AI Copilot</span>
            <Badge variant="primary">Academic Prep</Badge>
          </div>
          <h2 className="text-h2 text-text-primary font-bold">
            Study & Exam Assistant
          </h2>
          <p className="mt-1 text-body text-text-secondary max-w-2xl">
            Prepare smarter with AI-assisted learning. Get concept explanations,
            structured practice questions, and chapter summaries grounded in your curriculum.
          </p>
        </div>

        <Link
          href="/assistant"
          className="self-start sm:self-auto inline-flex items-center gap-2 px-4 py-2 bg-navy-800 hover:bg-navy-700 text-white text-body-sm font-medium rounded-lg transition-colors shadow-xs"
        >
          <span>Open Academic AI</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* 4 Capability Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {STUDY_CAPABILITIES.map((cap) => {
          const Icon = cap.icon;
          return (
            <Card
              key={cap.title}
              hover
              padding="md"
              className="flex flex-col justify-between h-full bg-white border-border"
            >
              <div>
                <div className="flex items-center justify-between mb-3.5">
                  <div className="w-10 h-10 rounded-lg bg-navy-50 flex items-center justify-center text-navy-700">
                    <Icon className="w-5 h-5" />
                  </div>
                  <Badge variant="gold">{cap.badge}</Badge>
                </div>

                <h3 className="text-body font-semibold text-text-primary mb-2">
                  {cap.title}
                </h3>

                <p className="text-body-sm text-text-secondary leading-relaxed mb-4">
                  {cap.description}
                </p>
              </div>

              {/* Sample prompt chip */}
              <div className="pt-3 border-t border-slate-100">
                <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block mb-1.5">
                  Try asking:
                </span>
                <Link
                  href={`/assistant?q=${encodeURIComponent(cap.examplePrompt)}`}
                  className="block p-2 bg-slate-50 hover:bg-navy-50 hover:border-navy-200 border border-slate-200 rounded text-caption text-navy-800 transition-colors"
                >
                  &ldquo;{cap.examplePrompt}&rdquo;
                </Link>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Grounding note */}
      <p className="mt-6 text-center text-caption text-text-muted">
        Academic assistance is designed to support syllabus revision and is verified against official departmental course material.
      </p>
    </Section>
  );
}

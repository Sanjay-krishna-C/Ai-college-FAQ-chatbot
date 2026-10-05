import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, MessageSquareText, ShieldCheck, Sparkles } from "lucide-react";
import { Section, SectionHeading, Badge, Button, Card } from "@/components/ui";

export const metadata: Metadata = {
  title: "AI Assistant",
  description: "Ask questions about college information and get answers from official documents.",
};

export default async function AssistantPage({
  searchParams,
}: {
  searchParams?: Promise<{ q?: string }>;
}) {
  const resolvedParams = searchParams ? await searchParams : {};
  const initialQuery = resolvedParams.q;

  return (
    <Section background="white">
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-body-sm text-navy-700 hover:text-navy-900 font-medium"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Portal Homepage</span>
          </Link>
        </div>

        <SectionHeading
          title="AI Information Assistant"
          subtitle="Ask questions about college regulations, examinations, academics, hostels, and services"
        />

        {initialQuery ? (
          <Card padding="md" className="mb-6 bg-slate-50 border-navy-200">
            <div className="flex items-center gap-2 mb-2 text-caption font-semibold uppercase text-gold-700">
              <Sparkles className="w-3.5 h-3.5 text-gold-600" />
              <span>Query Captured from Homepage</span>
            </div>
            <p className="text-body font-medium text-navy-900 italic mb-2">
              &ldquo;{initialQuery}&rdquo;
            </p>
            <div className="flex items-center gap-2 text-caption text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded w-fit border border-emerald-200">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Ready for grounding verification</span>
            </div>
          </Card>
        ) : null}

        <div className="text-center p-8 bg-slate-50 border border-border rounded-xl">
          <div className="w-16 h-16 rounded-2xl bg-gold-50 border border-gold-200 flex items-center justify-center mx-auto mb-4 text-gold-600">
            <MessageSquareText className="w-8 h-8" />
          </div>

          <h3 className="text-h3 text-navy-900 font-bold mb-2">
            Interactive Assistant Workspace
          </h3>

          <p className="text-body text-text-secondary mb-6 leading-relaxed">
            The full-page conversational AI workspace with source citation cards,
            multilingual English/Tamil/Tanglish support, and suggested queries
            will be activated in <span className="font-semibold text-navy-800">Phase 4 (AI Assistant UI)</span>.
          </p>

          <div className="flex items-center justify-center gap-3">
            <Badge variant="gold">Scheduled for Phase 4</Badge>
            <Link href="/">
              <Button variant="outline" size="sm">
                Return to Homepage
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </Section>
  );
}

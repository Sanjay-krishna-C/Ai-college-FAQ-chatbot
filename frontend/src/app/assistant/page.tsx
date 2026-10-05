import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Section, SectionHeading } from "@/components/ui";
import { CampusAIChatbox } from "@/components/chat";

export const metadata: Metadata = {
  title: "AI Assistant",
  description: "Ask questions about college information and get answers grounded in official documents.",
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
      <div className="max-w-3xl mx-auto">
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

        <div className="bg-navy-800 p-6 sm:p-8 rounded-2xl shadow-xl border border-navy-700">
          <CampusAIChatbox initialQuery={initialQuery} autoFocus={!initialQuery} />
        </div>
      </div>
    </Section>
  );
}


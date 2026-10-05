import type { Metadata } from "next";
import { Section, SectionHeading, Badge } from "@/components/ui";
import { BookOpen } from "lucide-react";

export const metadata: Metadata = {
  title: "Library",
  description: "Library timings, digital resources, borrowing rules, and catalog access.",
};

export default function LibraryPage() {
  return (
    <Section background="white">
      <SectionHeading
        title="Library"
        subtitle="Library timings, digital resources, borrowing rules, and catalog access"
      />
      <div className="max-w-xl mx-auto text-center">
        <div className="w-14 h-14 rounded-xl bg-navy-50 flex items-center justify-center mx-auto mb-4">
          <BookOpen className="w-7 h-7 text-navy-500" />
        </div>
        <p className="text-body text-text-secondary mb-4">
          This section will contain library information including operating hours,
          digital resource access, borrowing rules, and online catalog.
        </p>
        <Badge variant="gold">Coming in Phase 3</Badge>
      </div>
    </Section>
  );
}

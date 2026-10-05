import type { Metadata } from "next";
import { Section, SectionHeading, Badge } from "@/components/ui";
import { FileText } from "lucide-react";

export const metadata: Metadata = {
  title: "Examinations",
  description: "Exam schedules, fee deadlines, results, and examination regulations.",
};

export default function ExaminationsPage() {
  return (
    <Section background="white">
      <SectionHeading
        title="Examinations"
        subtitle="Schedules, fee deadlines, results, hall tickets, and exam regulations"
      />
      <div className="max-w-xl mx-auto text-center">
        <div className="w-14 h-14 rounded-xl bg-navy-50 flex items-center justify-center mx-auto mb-4">
          <FileText className="w-7 h-7 text-navy-500" />
        </div>
        <p className="text-body text-text-secondary mb-4">
          This section will contain detailed examination information including schedules,
          fee deadlines, result publication, and exam regulations.
        </p>
        <Badge variant="gold">Coming in Phase 3</Badge>
      </div>
    </Section>
  );
}

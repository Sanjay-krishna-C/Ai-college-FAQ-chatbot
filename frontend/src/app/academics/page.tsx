import type { Metadata } from "next";
import { Section, SectionHeading, Badge } from "@/components/ui";
import { GraduationCap } from "lucide-react";

export const metadata: Metadata = {
  title: "Academics",
  description: "Academic departments, programs, regulations, and curriculum information.",
};

export default function AcademicsPage() {
  return (
    <Section background="white">
      <SectionHeading
        title="Academics"
        subtitle="Departments, programs, regulations, and academic calendar"
      />
      <div className="max-w-xl mx-auto text-center">
        <div className="w-14 h-14 rounded-xl bg-navy-50 flex items-center justify-center mx-auto mb-4">
          <GraduationCap className="w-7 h-7 text-navy-500" />
        </div>
        <p className="text-body text-text-secondary mb-4">
          This section will contain detailed academic information including departments,
          programs offered, academic regulations, and calendar.
        </p>
        <Badge variant="gold">Coming in Phase 3</Badge>
      </div>
    </Section>
  );
}

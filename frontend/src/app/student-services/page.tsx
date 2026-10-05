import type { Metadata } from "next";
import { Section, SectionHeading, Badge } from "@/components/ui";
import { Users } from "lucide-react";

export const metadata: Metadata = {
  title: "Student Services",
  description: "Scholarships, ID cards, transport, grievance redressal, and support services.",
};

export default function StudentServicesPage() {
  return (
    <Section background="white">
      <SectionHeading
        title="Student Services"
        subtitle="Scholarships, ID cards, transport, grievance redressal, and other support services"
      />
      <div className="max-w-xl mx-auto text-center">
        <div className="w-14 h-14 rounded-xl bg-navy-50 flex items-center justify-center mx-auto mb-4">
          <Users className="w-7 h-7 text-navy-500" />
        </div>
        <p className="text-body text-text-secondary mb-4">
          This section will contain information about student support services including
          scholarships, ID cards, transport, grievance redressal, and more.
        </p>
        <Badge variant="gold">Coming in Phase 3</Badge>
      </div>
    </Section>
  );
}

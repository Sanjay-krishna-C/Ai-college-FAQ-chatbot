import type { Metadata } from "next";
import { Section, SectionHeading, Badge } from "@/components/ui";
import { Briefcase } from "lucide-react";

export const metadata: Metadata = {
  title: "Placements",
  description: "Placement process, eligibility, recruiting companies, and career guidance.",
};

export default function PlacementsPage() {
  return (
    <Section background="white">
      <SectionHeading
        title="Placements"
        subtitle="Placement process, eligibility criteria, recruiting companies, and career guidance"
      />
      <div className="max-w-xl mx-auto text-center">
        <div className="w-14 h-14 rounded-xl bg-navy-50 flex items-center justify-center mx-auto mb-4">
          <Briefcase className="w-7 h-7 text-navy-500" />
        </div>
        <p className="text-body text-text-secondary mb-4">
          This section will contain placement information including the placement process,
          eligibility criteria, list of recruiting companies, and career guidance resources.
        </p>
        <Badge variant="gold">Coming in Phase 3</Badge>
      </div>
    </Section>
  );
}

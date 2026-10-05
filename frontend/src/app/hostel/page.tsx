import type { Metadata } from "next";
import { Section, SectionHeading, Badge } from "@/components/ui";
import { Building2 } from "lucide-react";

export const metadata: Metadata = {
  title: "Hostel",
  description: "Hostel facilities, rules, fee structure, mess details, and accommodation.",
};

export default function HostelPage() {
  return (
    <Section background="white">
      <SectionHeading
        title="Hostel"
        subtitle="Hostel facilities, rules, fee structure, mess details, and accommodation information"
      />
      <div className="max-w-xl mx-auto text-center">
        <div className="w-14 h-14 rounded-xl bg-navy-50 flex items-center justify-center mx-auto mb-4">
          <Building2 className="w-7 h-7 text-navy-500" />
        </div>
        <p className="text-body text-text-secondary mb-4">
          This section will contain hostel information including facilities,
          rules and regulations, fee structure, mess timings, and accommodation details.
        </p>
        <Badge variant="gold">Coming in Phase 3</Badge>
      </div>
    </Section>
  );
}

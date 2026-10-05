import { Section, SectionHeading, Card, Badge } from "@/components/ui";
import { Award, Users, BookOpen, Building, ShieldCheck } from "lucide-react";

/**
 * Institutional highlights section.
 * Uses neutral, professional placeholders without prominent raw bracketed text.
 */

const highlights = [
  {
    icon: Building,
    label: "Academic Departments",
    value: "—",
    statusText: "To be updated",
    description: "Core Engineering & Science Disciplines",
  },
  {
    icon: BookOpen,
    label: "Degree Programs",
    value: "—",
    statusText: "To be updated",
    description: "Undergraduate & Postgraduate Curricula",
  },
  {
    icon: Users,
    label: "Student Body",
    value: "—",
    statusText: "Official data pending",
    description: "Campus Enrolled Students",
  },
  {
    icon: Award,
    label: "Institutional Accreditation",
    value: "—",
    statusText: "Official data pending",
    description: "Regulatory Approvals & Affiliations",
  },
];

export function InstitutionalSection() {
  return (
    <Section background="white" id="about">
      <SectionHeading
        title="About the Institution"
        subtitle="Institutional overview and verified college directory"
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-8">
        {highlights.map((item) => {
          const Icon = item.icon;
          return (
            <Card key={item.label} padding="md" className="text-center bg-slate-50/60 border-border">
              <div className="w-10 h-10 rounded-lg bg-navy-50 flex items-center justify-center mx-auto mb-3 text-navy-700">
                <Icon className="w-5 h-5" />
              </div>
              <div className="text-h3 text-navy-800 font-bold mb-1">{item.value}</div>
              <div className="text-body-sm font-semibold text-text-primary">
                {item.label}
              </div>
              <div className="text-caption font-medium text-slate-500 mt-1">
                {item.statusText}
              </div>
              <div className="text-[12px] text-text-secondary mt-0.5">
                {item.description}
              </div>
            </Card>
          );
        })}
      </div>

      <div className="flex items-center justify-center gap-2 text-caption text-text-muted">
        <ShieldCheck className="w-4 h-4 text-slate-400" />
        <span>Official institutional metrics will be populated upon administration registry synchronization.</span>
      </div>
    </Section>
  );
}

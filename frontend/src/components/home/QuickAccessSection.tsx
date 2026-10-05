import Link from "next/link";
import { Section, SectionHeading, Card } from "@/components/ui";
import {
  GraduationCap,
  FileText,
  Briefcase,
  Building2,
  BookOpen,
  Users,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface ServiceItem {
  title: string;
  description: string;
  href: string;
  icon: LucideIcon;
}

const services: ServiceItem[] = [
  {
    title: "Academics",
    description:
      "Departments, programs, regulations, academic calendar, and curriculum details.",
    href: "/academics",
    icon: GraduationCap,
  },
  {
    title: "Examinations",
    description:
      "Exam schedules, fee deadlines, results, hall tickets, and exam regulations.",
    href: "/examinations",
    icon: FileText,
  },
  {
    title: "Placements",
    description:
      "Placement process, eligibility criteria, recruiting companies, and career guidance.",
    href: "/placements",
    icon: Briefcase,
  },
  {
    title: "Hostel",
    description:
      "Hostel facilities, rules, fee structure, mess details, and accommodation information.",
    href: "/hostel",
    icon: Building2,
  },
  {
    title: "Library",
    description:
      "Library timings, digital resources, borrowing rules, and catalog access.",
    href: "/library",
    icon: BookOpen,
  },
  {
    title: "Student Services",
    description:
      "Scholarships, ID cards, transport, grievance redressal, and other support services.",
    href: "/student-services",
    icon: Users,
  },
];

export function QuickAccessSection() {
  return (
    <Section background="white">
      <SectionHeading
        title="Student Services"
        subtitle="Quick access to everything you need across the college"
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {services.map((service) => {
          const Icon = service.icon;
          return (
            <Link key={service.title} href={service.href} className="group">
              <Card hover padding="md" className="h-full">
                <div className="flex items-start gap-4">
                  <div className="shrink-0 w-11 h-11 rounded-lg bg-navy-50 flex items-center justify-center group-hover:bg-navy-100 transition-colors duration-[var(--transition-base)]">
                    <Icon className="w-5 h-5 text-navy-600" />
                  </div>
                  <div className="min-w-0">
                    <h3 className="font-semibold text-body text-text-primary group-hover:text-navy-700 transition-colors duration-[var(--transition-base)]">
                      {service.title}
                    </h3>
                    <p className="mt-1.5 text-body-sm text-text-secondary leading-relaxed">
                      {service.description}
                    </p>
                  </div>
                </div>
              </Card>
            </Link>
          );
        })}
      </div>
    </Section>
  );
}

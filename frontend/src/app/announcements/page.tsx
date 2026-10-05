import type { Metadata } from "next";
import { Section, SectionHeading, Badge } from "@/components/ui";
import { Bell } from "lucide-react";

export const metadata: Metadata = {
  title: "Announcements",
  description: "Latest circulars, notices, and important announcements from the college.",
};

export default function AnnouncementsPage() {
  return (
    <Section background="white">
      <SectionHeading
        title="Announcements & Notices"
        subtitle="Latest circulars, notices, and important announcements"
      />
      <div className="max-w-xl mx-auto text-center">
        <div className="w-14 h-14 rounded-xl bg-navy-50 flex items-center justify-center mx-auto mb-4">
          <Bell className="w-7 h-7 text-navy-500" />
        </div>
        <p className="text-body text-text-secondary mb-4">
          This section will contain a complete list of college announcements,
          circulars, and notices with filtering and search capabilities.
        </p>
        <Badge variant="gold">Coming in Phase 3</Badge>
      </div>
    </Section>
  );
}

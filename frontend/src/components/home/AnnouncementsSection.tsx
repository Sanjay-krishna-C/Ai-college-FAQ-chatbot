import { Section, SectionHeading, Badge, Card } from "@/components/ui";
import { Calendar, ArrowRight, Bell, AlertCircle, ExternalLink } from "lucide-react";
import Link from "next/link";

interface AnnouncementItem {
  id: number;
  title: string;
  date: string;
  category: string;
  department: string;
  priority: "Urgent" | "High" | "Normal";
  badgeVariant: "warning" | "success" | "info" | "primary" | "default";
}

// Demo announcements with departments and priority levels
const DEMO_ANNOUNCEMENTS: AnnouncementItem[] = [
  {
    id: 1,
    title: "[Demo] End Semester Theory Examination Timetable Released — Even Semester 2026",
    date: "2026-10-03",
    category: "Examination",
    department: "Controller of Examinations",
    priority: "Urgent",
    badgeVariant: "warning",
  },
  {
    id: 2,
    title: "[Demo] Tier-1 IT & Product Companies Placement Drive: Registration Closes Monday",
    date: "2026-10-02",
    category: "Placement",
    department: "Career Development & Placement Cell",
    priority: "High",
    badgeVariant: "success",
  },
  {
    id: 3,
    title: "[Demo] Central Library Extended Night Reading Hours During Semester Exams",
    date: "2026-09-30",
    category: "Library",
    department: "Central Library Advisory Board",
    priority: "Normal",
    badgeVariant: "info",
  },
  {
    id: 4,
    title: "[Demo] Even Semester Hostel Maintenance & Mess Fee Payment Window Open",
    date: "2026-09-28",
    category: "Hostel",
    department: "Hostel Administration & Chief Warden Office",
    priority: "High",
    badgeVariant: "primary",
  },
  {
    id: 5,
    title: "[Demo] State Government Merit-Cum-Means Scholarship Application Verification",
    date: "2026-09-25",
    category: "Scholarship",
    department: "Student Welfare & Scholarship Section",
    priority: "Normal",
    badgeVariant: "default",
  },
];

function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function AnnouncementsSection() {
  return (
    <Section background="white" id="announcements">
      <SectionHeading
        title="Important Announcements"
        subtitle="Official college notifications, examination circulars, and departmental orders"
      />

      <Card padding="none" className="overflow-hidden border-border shadow-xs">
        {/* Header Bar */}
        <div className="px-5 sm:px-6 py-4 bg-navy-50 border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bell className="w-4 h-4 text-navy-700" />
            <span className="text-body-sm font-semibold text-navy-900">
              Official Notice Board
            </span>
          </div>
          <Badge variant="gold">DEMO DATA</Badge>
        </div>

        {/* Notices list */}
        <ul role="list" className="divide-y divide-border">
          {DEMO_ANNOUNCEMENTS.map((item) => (
            <li key={item.id} className="hover:bg-slate-50/80 transition-colors">
              <div className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-start gap-3.5 flex-1 min-w-0">
                  <div className="hidden sm:flex flex-col items-center justify-center shrink-0 w-24 py-1.5 px-2 bg-slate-100 rounded border border-slate-200 text-center">
                    <span className="text-caption font-semibold text-slate-800">
                      {formatDate(item.date)}
                    </span>
                    <span className="text-[10px] text-slate-500 uppercase tracking-wider">
                      Published
                    </span>
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-2 mb-1.5">
                      <Badge variant={item.badgeVariant}>{item.category}</Badge>
                      {item.priority === "Urgent" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-red-700 bg-red-50 px-2 py-0.5 rounded border border-red-200">
                          <AlertCircle className="w-3 h-3" />
                          Urgent
                        </span>
                      )}
                      {item.priority === "High" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                          Important
                        </span>
                      )}
                      <span className="sm:hidden text-caption text-text-muted">
                        • {formatDate(item.date)}
                      </span>
                    </div>

                    <h3 className="text-body font-semibold text-text-primary leading-snug">
                      {item.title}
                    </h3>

                    <p className="text-caption text-text-secondary mt-1">
                      Issued by: <span className="font-medium text-slate-700">{item.department}</span>
                    </p>
                  </div>
                </div>

                {/* Read Action */}
                <div className="shrink-0 flex items-center gap-2 sm:self-center">
                  <Link
                    href={`/assistant?q=${encodeURIComponent(`Details on announcement: ${item.title}`)}`}
                    className="inline-flex items-center gap-1 text-body-sm font-medium text-navy-700 hover:text-navy-900 bg-navy-50 hover:bg-navy-100 px-3 py-1.5 rounded border border-navy-200 transition-colors"
                  >
                    <span>View / Ask AI</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </li>
          ))}
        </ul>

        {/* View all footer */}
        <div className="px-5 sm:px-6 py-3.5 border-t border-border bg-slate-50 flex items-center justify-between">
          <span className="text-caption text-text-muted">
            All circulars are verified against official registrar records.
          </span>
          <Link
            href="/announcements"
            className="inline-flex items-center gap-1.5 text-body-sm text-navy-700 font-semibold hover:text-navy-900 transition-colors"
          >
            <span>View Archive</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </Card>
    </Section>
  );
}

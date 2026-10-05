"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Clock,
  MapPin,
  Calendar,
  Building,
  CheckCircle2,
  CalendarDays,
  Info,
  ArrowUpRight,
} from "lucide-react";
import { Badge, Card, Section } from "@/components/ui";

type TabPeriod = "today" | "tomorrow" | "week";

interface CampusEvent {
  id: string;
  time: string;
  title: string;
  venue: string;
  category: "Class" | "Placement" | "Workshop" | "Club" | "Library" | "Lab";
  department: string;
  status: "In Progress" | "Upcoming" | "Scheduled";
  badgeVariant: "primary" | "success" | "warning" | "info" | "gold";
}

const DEMO_EVENTS: Record<TabPeriod, CampusEvent[]> = {
  today: [
    {
      id: "ev-1",
      time: "09:00 AM - 11:00 AM",
      title: "AI & Data Science Advanced Lab Session",
      venue: "Block A — Room 204",
      category: "Class",
      department: "Dept. of Computer Science & Engineering",
      status: "In Progress",
      badgeVariant: "info",
    },
    {
      id: "ev-2",
      time: "11:30 AM - 01:00 PM",
      title: "Campus Placement Orientation & Resume Review",
      venue: "Main Auditorium — Ground Floor",
      category: "Placement",
      department: "Training & Placement Cell",
      status: "Upcoming",
      badgeVariant: "success",
    },
    {
      id: "ev-3",
      time: "02:00 PM - 03:30 PM",
      title: "Digital Library Research Workshop — IEEE Xplore Access",
      venue: "Central Library — E-Learning Center",
      category: "Library",
      department: "Central Library Division",
      status: "Upcoming",
      badgeVariant: "gold",
    },
    {
      id: "ev-4",
      time: "04:00 PM - 05:30 PM",
      title: "Open Source Developers & Competitive Coding Meet",
      venue: "Seminar Hall II — Innovation Wing",
      category: "Club",
      department: "Student Coding Club",
      status: "Scheduled",
      badgeVariant: "primary",
    },
  ],
  tomorrow: [
    {
      id: "ev-5",
      time: "10:00 AM - 12:00 PM",
      title: "Core Engineering Systems Lab Practical Evaluation",
      venue: "Block C — Machine Dynamics Lab",
      category: "Lab",
      department: "Dept. of Mechanical Engineering",
      status: "Scheduled",
      badgeVariant: "info",
    },
    {
      id: "ev-6",
      time: "02:30 PM - 04:30 PM",
      title: "Pre-Placement Technical Interview Prep Session",
      venue: "Convention Center — Hall B",
      category: "Placement",
      department: "Training & Placement Cell",
      status: "Scheduled",
      badgeVariant: "success",
    },
  ],
  week: [
    {
      id: "ev-7",
      time: "Wednesday, 10:00 AM",
      title: "Annual Tech Symposium Project Submissions Deadline",
      venue: "Dean Academic Office",
      category: "Workshop",
      department: "Academic Affairs",
      status: "Scheduled",
      badgeVariant: "warning",
    },
    {
      id: "ev-8",
      time: "Thursday, 03:00 PM",
      title: "Guest Lecture: Generative AI in Industrial Robotics",
      venue: "Main Auditorium",
      category: "Workshop",
      department: "Robotics & Automation Dept.",
      status: "Scheduled",
      badgeVariant: "primary",
    },
    {
      id: "ev-9",
      time: "Saturday, 09:00 AM",
      title: "Weekend Hackathon Orientation & Team Formation",
      venue: "Incubation Hub — Floor 3",
      category: "Club",
      department: "Student Affairs & Innovation Cell",
      status: "Scheduled",
      badgeVariant: "gold",
    },
  ],
};

export function CampusPulseSection() {
  const [activeTab, setActiveTab] = useState<TabPeriod>("today");

  const events = DEMO_EVENTS[activeTab];

  return (
    <Section background="light" id="campus-pulse">
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <div className="inline-flex items-center gap-2 mb-2 text-caption font-semibold uppercase tracking-wider text-navy-700">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" aria-hidden="true" />
            <span>Real-Time College Updates</span>
            <Badge variant="gold">DEMO DATA</Badge>
          </div>
          <h2 className="text-h2 text-text-primary font-bold">
            Campus Pulse
          </h2>
          <p className="mt-1 text-body text-text-secondary">
            What&apos;s happening on campus today —{" "}
            <span className="font-medium text-navy-800">
              stay informed before you reach the location.
            </span>
          </p>
        </div>

        {/* Tab Filters */}
        <div className="flex items-center gap-1.5 p-1 bg-white border border-border rounded-lg shadow-xs self-start md:self-auto">
          <button
            type="button"
            onClick={() => setActiveTab("today")}
            className={`px-3.5 py-1.5 rounded-md text-body-sm font-medium transition-colors cursor-pointer ${
              activeTab === "today"
                ? "bg-navy-800 text-white shadow-xs"
                : "text-text-secondary hover:text-text-primary hover:bg-slate-50"
            }`}
          >
            Today
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("tomorrow")}
            className={`px-3.5 py-1.5 rounded-md text-body-sm font-medium transition-colors cursor-pointer ${
              activeTab === "tomorrow"
                ? "bg-navy-800 text-white shadow-xs"
                : "text-text-secondary hover:text-text-primary hover:bg-slate-50"
            }`}
          >
            Tomorrow
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("week")}
            className={`px-3.5 py-1.5 rounded-md text-body-sm font-medium transition-colors cursor-pointer ${
              activeTab === "week"
                ? "bg-navy-800 text-white shadow-xs"
                : "text-text-secondary hover:text-text-primary hover:bg-slate-50"
            }`}
          >
            This Week
          </button>
        </div>
      </div>

      {/* Events Timeline / List */}
      <div className="space-y-3.5 mb-6">
        {events.map((item) => (
          <Card
            key={item.id}
            padding="none"
            hover
            className="overflow-hidden border-border transition-all"
          >
            <div className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              {/* Left Column: Time & Details */}
              <div className="flex items-start gap-4">
                <div className="shrink-0 w-12 h-12 rounded-lg bg-navy-50 flex flex-col items-center justify-center text-navy-800 border border-navy-100">
                  <Clock className="w-5 h-5 text-navy-700" />
                </div>

                <div>
                  <div className="flex flex-wrap items-center gap-2 mb-1">
                    <span className="text-body-sm font-semibold text-navy-800 flex items-center gap-1.5">
                      {item.time}
                    </span>
                    <Badge variant={item.badgeVariant}>{item.category}</Badge>
                    {item.status === "In Progress" && (
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        In Progress
                      </span>
                    )}
                  </div>

                  <h3 className="text-body font-semibold text-text-primary">
                    {item.title}
                  </h3>

                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-1 text-caption text-text-secondary">
                    <span className="flex items-center gap-1 text-navy-700 font-medium">
                      <MapPin className="w-3.5 h-3.5 text-navy-600" />
                      {item.venue}
                    </span>
                    <span className="flex items-center gap-1">
                      <Building className="w-3.5 h-3.5 text-slate-400" />
                      {item.department}
                    </span>
                  </div>
                </div>
              </div>

              {/* Right: Quick Action / Query Link */}
              <div className="sm:self-center shrink-0">
                <Link
                  href={`/assistant?q=${encodeURIComponent(`Tell me about ${item.title}`)}`}
                  className="inline-flex items-center gap-1 px-3 py-1.5 text-body-sm text-navy-700 bg-navy-50 hover:bg-navy-100 rounded-md border border-navy-200 transition-colors font-medium"
                >
                  <span>Ask Assistant</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Footer info note and calendar button */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 bg-white border border-border rounded-lg text-body-sm">
        <div className="flex items-center gap-2.5 text-text-secondary">
          <Info className="w-4 h-4 text-navy-600 shrink-0" />
          <span>
            Have a venue change or query? Ask the AI assistant anytime: &ldquo;Is the library available today?&rdquo;
          </span>
        </div>

        <Link
          href="/announcements"
          className="inline-flex items-center gap-1.5 font-medium text-navy-700 hover:text-navy-900 transition-colors shrink-0"
        >
          <CalendarDays className="w-4 h-4 text-gold-600" />
          <span>View Full College Calendar</span>
        </Link>
      </div>
    </Section>
  );
}

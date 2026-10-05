import {
  HeroSection,
  CampusPulseSection,
  AnnouncementsSection,
  QuickAccessSection,
  StudyExamAssistantSection,
  InstitutionalSection,
} from "@/components/home";

export default function HomePage() {
  return (
    <>
      {/* 1. Main AI Assistant Hero & Chatbox */}
      <HeroSection />

      {/* 2. Campus Pulse — What's happening on campus today? */}
      <CampusPulseSection />

      {/* 3. Important Announcements & Notices */}
      <AnnouncementsSection />

      {/* 4. Student Services (Academics, Exams, Placement, Hostel, Library, Services) */}
      <QuickAccessSection />

      {/* 5. Study & Exam Assistant */}
      <StudyExamAssistantSection />

      {/* 6. Institutional Information */}
      <InstitutionalSection />
    </>
  );
}

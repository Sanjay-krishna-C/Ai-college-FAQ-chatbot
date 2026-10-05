// Site-wide constants and configuration

export const SITE_CONFIG = {
  collegeName: "Demo College of Engineering & Technology",
  collegeShortName: "DCET",
  tagline: "Excellence in Education Since Establishment",
  // Placeholder — replace with actual college details when available
  address: "[College Address — To Be Updated]",
  phone: "[Phone — To Be Updated]",
  email: "[Email — To Be Updated]",
  website: "#",
} as const;

interface NavLink {
  label: string;
  href: string;
  highlight?: boolean;
}

export const NAV_LINKS: readonly NavLink[] = [
  { label: "Academics", href: "/academics" },
  { label: "Examinations", href: "/examinations" },
  { label: "Placements", href: "/placements" },
  { label: "Hostel", href: "/hostel" },
  { label: "Library", href: "/library" },
  { label: "Student Services", href: "/student-services" },
  { label: "AI Assistant", href: "/assistant", highlight: true },
];

export const FOOTER_LINKS = {
  academics: [
    { label: "Departments", href: "/academics" },
    { label: "Programs", href: "/academics" },
    { label: "Academic Calendar", href: "/academics" },
    { label: "Regulations", href: "/academics" },
  ],
  students: [
    { label: "Examinations", href: "/examinations" },
    { label: "Placements", href: "/placements" },
    { label: "Hostel", href: "/hostel" },
    { label: "Library", href: "/library" },
    { label: "Student Services", href: "/student-services" },
  ],
  quickLinks: [
    { label: "Announcements", href: "/announcements" },
    { label: "AI Assistant", href: "/assistant" },
    { label: "Contact Us", href: "#contact" },
  ],
} as const;

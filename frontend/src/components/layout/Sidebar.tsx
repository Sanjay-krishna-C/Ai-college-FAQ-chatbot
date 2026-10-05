"use client";

import { useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  MessageSquareText,
  GraduationCap,
  FileText,
  Briefcase,
  Building2,
  BookOpen,
  Users,
  CalendarDays,
  Bell,
  Settings,
  HelpCircle,
  X,
} from "lucide-react";

interface SidebarItem {
  label: string;
  href: string;
  icon: typeof Home;
}

const MAIN_NAV: SidebarItem[] = [
  { label: "Home", href: "/", icon: Home },
  { label: "AI Assistant", href: "/assistant", icon: MessageSquareText },
  { label: "Academics", href: "/academics", icon: GraduationCap },
  { label: "Examinations", href: "/examinations", icon: FileText },
  { label: "Placements", href: "/placements", icon: Briefcase },
  { label: "Hostel", href: "/hostel", icon: Building2 },
  { label: "Library", href: "/library", icon: BookOpen },
  { label: "Student Services", href: "/student-services", icon: Users },
  { label: "Campus Calendar", href: "/announcements", icon: CalendarDays },
  { label: "Announcements", href: "/announcements", icon: Bell },
];

const SECONDARY_NAV: SidebarItem[] = [
  { label: "Settings", href: "#settings", icon: Settings },
  { label: "Help & Support", href: "#help", icon: HelpCircle },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

export function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname();

  // Close sidebar on route change (mobile)
  useEffect(() => {
    onClose();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  // Lock body scroll when sidebar is open on mobile
  useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  // Close on escape key
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    if (open) document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [open, onClose]);

  function isActive(href: string) {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  }

  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Sidebar Header */}
      <div className="flex items-center justify-between px-4 h-14 border-b border-navy-700 shrink-0">
        <Link href="/" className="flex items-center gap-2.5" onClick={onClose}>
          <div className="w-8 h-8 rounded-full bg-gold-500 flex items-center justify-center text-white font-bold text-caption">
            CA
          </div>
          <span className="text-body font-bold text-white tracking-tight">
            CampusAI
          </span>
        </Link>
        <button
          type="button"
          onClick={onClose}
          className="p-1.5 text-navy-300 hover:text-white rounded-md hover:bg-navy-700 transition-colors cursor-pointer lg:hidden"
          aria-label="Close sidebar"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Main Navigation */}
      <nav className="flex-1 overflow-y-auto py-3 px-3" aria-label="Main navigation">
        <ul className="space-y-0.5">
          {MAIN_NAV.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);
            return (
              <li key={item.label}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-body-sm font-medium transition-colors ${
                    active
                      ? "bg-navy-700 text-white border-l-[3px] border-gold-500 pl-[9px]"
                      : "text-navy-200 hover:text-white hover:bg-navy-700/60"
                  }`}
                  onClick={onClose}
                >
                  <Icon className={`w-[18px] h-[18px] shrink-0 ${active ? "text-gold-400" : ""}`} />
                  <span>{item.label}</span>
                  {item.label === "AI Assistant" && (
                    <span className="ml-auto px-2 py-0.5 bg-gold-500/20 text-gold-300 text-[10px] font-bold rounded uppercase tracking-wider">
                      AI
                    </span>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>

        {/* Divider */}
        <div className="my-4 border-t border-navy-700" />

        {/* Secondary Navigation */}
        <ul className="space-y-0.5">
          {SECONDARY_NAV.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.label}>
                <a
                  href={item.href}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-body-sm font-medium text-navy-300 hover:text-white hover:bg-navy-700/60 transition-colors"
                  onClick={onClose}
                >
                  <Icon className="w-[18px] h-[18px] shrink-0" />
                  <span>{item.label}</span>
                </a>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="px-4 py-3 border-t border-navy-700 shrink-0">
        <p className="text-[11px] text-navy-400 leading-relaxed">
          CampusAI Student Portal
        </p>
        <p className="text-[10px] text-navy-500 mt-0.5">
          Demo portal for educational purposes
        </p>
      </div>
    </div>
  );

  return (
    <>
      {/* Backdrop overlay (mobile) */}
      {open && (
        <div
          className="fixed inset-0 bg-black/40 z-40 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar panel */}
      <aside
        className={`fixed top-0 left-0 z-50 h-full w-64 bg-navy-900 transform transition-transform duration-200 ease-in-out ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
        aria-label="Sidebar navigation"
      >
        {sidebarContent}
      </aside>
    </>
  );
}

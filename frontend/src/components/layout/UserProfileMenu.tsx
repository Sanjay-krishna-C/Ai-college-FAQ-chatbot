"use client";

import { useState, useRef, useEffect } from "react";
import {
  User,
  LayoutDashboard,
  GraduationCap,
  Settings,
  HelpCircle,
  LogOut,
  ChevronDown,
} from "lucide-react";

// Demo user data — replace with auth context when authentication is implemented
const DEMO_USER = {
  name: "Demo Student",
  role: "Student",
  avatarInitials: "DS",
};

interface ProfileMenuItem {
  label: string;
  icon: typeof User;
  href: string;
  separator?: boolean;
}

const PROFILE_MENU_ITEMS: ProfileMenuItem[] = [
  { label: "My Dashboard", icon: LayoutDashboard, href: "/dashboard" },
  { label: "Academic Profile", icon: GraduationCap, href: "/academics" },
  { label: "Settings", icon: Settings, href: "#settings", separator: true },
  { label: "Help & Support", icon: HelpCircle, href: "#help" },
];

export function UserProfileMenu() {
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  // Close on Escape key
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    if (open) {
      document.addEventListener("keydown", handleEscape);
    }
    return () => document.removeEventListener("keydown", handleEscape);
  }, [open]);

  return (
    <div ref={menuRef} className="relative">
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-navy-700 transition-colors cursor-pointer"
        aria-expanded={open}
        aria-haspopup="true"
        aria-label="User menu"
      >
        {/* Avatar */}
        <div className="w-8 h-8 rounded-full bg-gold-500 flex items-center justify-center text-white text-caption font-bold">
          {DEMO_USER.avatarInitials}
        </div>
        {/* Name (hidden on small screens) */}
        <span className="hidden sm:block text-body-sm text-white font-medium max-w-[120px] truncate">
          {DEMO_USER.name}
        </span>
        <ChevronDown className={`w-4 h-4 text-navy-300 transition-transform duration-150 ${open ? "rotate-180" : ""}`} />
      </button>

      {/* Dropdown */}
      {open && (
        <div
          className="absolute right-0 mt-2 w-64 bg-white border border-border rounded-lg shadow-lg z-50 overflow-hidden"
          role="menu"
        >
          {/* User Info Header */}
          <div className="px-4 py-3 border-b border-border bg-slate-50">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gold-500 flex items-center justify-center text-white font-bold text-body-sm">
                {DEMO_USER.avatarInitials}
              </div>
              <div className="min-w-0">
                <p className="text-body-sm font-semibold text-text-primary truncate">
                  {DEMO_USER.name}
                </p>
                <p className="text-caption text-text-secondary">{DEMO_USER.role}</p>
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-1.5">
            {PROFILE_MENU_ITEMS.map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.label}>
                  {item.separator && (
                    <div className="my-1.5 border-t border-border" />
                  )}
                  <a
                    href={item.href}
                    className="flex items-center gap-2.5 px-4 py-2 text-body-sm text-text-primary hover:bg-slate-50 transition-colors"
                    role="menuitem"
                    onClick={() => setOpen(false)}
                  >
                    <Icon className="w-4 h-4 text-slate-500" />
                    {item.label}
                  </a>
                </div>
              );
            })}
          </div>

          {/* Sign Out */}
          <div className="border-t border-border py-1.5">
            <button
              type="button"
              className="w-full flex items-center gap-2.5 px-4 py-2 text-body-sm text-red-600 hover:bg-red-50 transition-colors cursor-pointer"
              role="menuitem"
              onClick={() => setOpen(false)}
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>

          {/* Demo Notice */}
          <div className="px-4 py-2 bg-gold-50 border-t border-gold-200">
            <p className="text-[11px] text-gold-700 font-medium">
              Demo profile — authentication will be integrated in a later phase.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

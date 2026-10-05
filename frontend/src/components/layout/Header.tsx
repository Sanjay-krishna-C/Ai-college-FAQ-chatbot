"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu } from "lucide-react";
import { Sidebar } from "./Sidebar";
import { NotificationPopover } from "./NotificationPopover";
import { UserProfileMenu } from "./UserProfileMenu";

export function Header() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <>
      {/* Sidebar Drawer */}
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Top Header Bar */}
      <header className="sticky top-0 z-40 bg-navy-800 border-b border-navy-700">
        {/* Gold accent stripe */}
        <div className="h-0.5 bg-gold-500" aria-hidden="true" />

        <div className="px-4 sm:px-6">
          <div className="flex items-center justify-between h-14">
            {/* LEFT: Hamburger + Branding */}
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setSidebarOpen(true)}
                className="p-2 -ml-2 text-navy-200 hover:text-white hover:bg-navy-700 rounded-lg transition-colors cursor-pointer"
                aria-label="Open navigation menu"
              >
                <Menu className="w-5 h-5" />
              </button>

              <Link href="/" className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-full bg-gold-500 flex items-center justify-center text-white font-bold text-caption">
                  CA
                </div>
                <span className="text-body font-bold text-white tracking-tight">
                  CampusAI
                </span>
              </Link>
            </div>

            {/* RIGHT: Notifications + User Profile */}
            <div className="flex items-center gap-1">
              <NotificationPopover />
              <UserProfileMenu />
            </div>
          </div>
        </div>
      </header>
    </>
  );
}

"use client";

import { useState, useRef, useEffect } from "react";
import { Bell, Check, CheckCheck, AlertTriangle, Info, Calendar, ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui";

interface NotificationItemData {
  id: string;
  title: string;
  description: string;
  time: string;
  priority: "urgent" | "important" | "campus";
  read: boolean;
  category: string;
}

const DEMO_NOTIFICATIONS: NotificationItemData[] = [
  {
    id: "n1",
    title: "End Semester Examination Registration",
    description: "Registration deadline today. Submit exam fees before 5:00 PM.",
    time: "2 hours ago",
    priority: "urgent",
    read: false,
    category: "Examination",
  },
  {
    id: "n2",
    title: "Library Research Workshop",
    description: "IEEE Xplore access workshop scheduled tomorrow at Central Library.",
    time: "4 hours ago",
    priority: "important",
    read: false,
    category: "Library",
  },
  {
    id: "n3",
    title: "Placement Orientation",
    description: "Orientation for upcoming campus drives at Main Auditorium.",
    time: "6 hours ago",
    priority: "campus",
    read: false,
    category: "Placement",
  },
  {
    id: "n4",
    title: "Hostel Mess Fee Due",
    description: "Mess fee payment window closes this week.",
    time: "Yesterday",
    priority: "important",
    read: true,
    category: "Hostel",
  },
];

const priorityConfig = {
  urgent: {
    icon: AlertTriangle,
    color: "text-red-600",
    bg: "bg-red-50",
    border: "border-red-200",
    label: "Urgent",
  },
  important: {
    icon: Info,
    color: "text-amber-600",
    bg: "bg-amber-50",
    border: "border-amber-200",
    label: "Important",
  },
  campus: {
    icon: Calendar,
    color: "text-navy-600",
    bg: "bg-navy-50",
    border: "border-navy-200",
    label: "Campus",
  },
};

function NotificationItem({
  item,
  onMarkRead,
}: {
  item: NotificationItemData;
  onMarkRead: (id: string) => void;
}) {
  const config = priorityConfig[item.priority];
  const PriorityIcon = config.icon;

  return (
    <div
      className={`px-4 py-3 border-b border-border last:border-b-0 transition-colors ${
        item.read ? "bg-white" : "bg-slate-50/80"
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Priority Icon */}
        <div className={`shrink-0 w-8 h-8 rounded-lg ${config.bg} ${config.border} border flex items-center justify-center mt-0.5`}>
          <PriorityIcon className={`w-4 h-4 ${config.color}`} />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <span className={`text-[11px] font-semibold uppercase tracking-wider ${config.color}`}>
              {config.label}
            </span>
            <Badge variant="default">{item.category}</Badge>
            {!item.read && (
              <span className="w-2 h-2 rounded-full bg-gold-500 shrink-0" aria-label="Unread" />
            )}
          </div>
          <h4 className={`text-body-sm font-semibold leading-snug ${item.read ? "text-text-secondary" : "text-text-primary"}`}>
            {item.title}
          </h4>
          <p className="text-caption text-text-muted mt-0.5 leading-relaxed">
            {item.description}
          </p>
          <div className="flex items-center justify-between mt-1.5">
            <span className="text-[11px] text-text-muted">{item.time}</span>
            {!item.read && (
              <button
                type="button"
                onClick={() => onMarkRead(item.id)}
                className="text-[11px] text-navy-600 hover:text-navy-800 font-medium flex items-center gap-1 cursor-pointer"
              >
                <Check className="w-3 h-3" />
                Mark read
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export function NotificationPopover() {
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState(DEMO_NOTIFICATIONS);
  const popoverRef = useRef<HTMLDivElement>(null);

  const unreadCount = notifications.filter((n) => !n.read).length;

  const handleMarkRead = (id: string) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true } : n))
    );
  };

  const handleMarkAllRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    if (open) document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  // Close on Escape
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    if (open) document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [open]);

  return (
    <div ref={popoverRef} className="relative">
      {/* Bell Button */}
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="relative p-2 rounded-lg text-navy-200 hover:text-white hover:bg-navy-700 transition-colors cursor-pointer"
        aria-label={`Notifications${unreadCount > 0 ? `, ${unreadCount} unread` : ""}`}
        aria-expanded={open}
        aria-haspopup="true"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 flex items-center justify-center w-5 h-5 text-[10px] font-bold bg-red-500 text-white rounded-full border-2 border-navy-800">
            {unreadCount}
          </span>
        )}
      </button>

      {/* Popover Panel */}
      {open && (
        <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white border border-border rounded-lg shadow-xl z-50 overflow-hidden">
          {/* Header */}
          <div className="px-4 py-3 border-b border-border bg-slate-50 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <h3 className="text-body-sm font-semibold text-text-primary">Notifications</h3>
              {unreadCount > 0 && (
                <Badge variant="gold">{unreadCount} new</Badge>
              )}
            </div>
            {unreadCount > 0 && (
              <button
                type="button"
                onClick={handleMarkAllRead}
                className="text-caption text-navy-600 hover:text-navy-800 font-medium flex items-center gap-1 cursor-pointer"
              >
                <CheckCheck className="w-3.5 h-3.5" />
                Mark all read
              </button>
            )}
          </div>

          {/* Demo data badge */}
          <div className="px-4 py-1.5 bg-gold-50 border-b border-gold-200">
            <p className="text-[11px] text-gold-700 font-medium text-center">
              Demo notifications — will be connected to live college data
            </p>
          </div>

          {/* Notification List */}
          <div className="max-h-80 overflow-y-auto">
            {notifications.map((item) => (
              <NotificationItem
                key={item.id}
                item={item}
                onMarkRead={handleMarkRead}
              />
            ))}
          </div>

          {/* Footer */}
          <div className="px-4 py-2.5 border-t border-border bg-slate-50">
            <a
              href="/announcements"
              className="flex items-center justify-center gap-1.5 text-body-sm font-medium text-navy-700 hover:text-navy-900 transition-colors"
              onClick={() => setOpen(false)}
            >
              <span>View All Notifications</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

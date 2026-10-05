import Link from "next/link";
import { SITE_CONFIG, FOOTER_LINKS } from "@/lib/constants";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-navy-900 text-navy-200">
      <div className="section-container">
        {/* Main Footer Content */}
        <div className="py-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* College Info */}
          <div className="sm:col-span-2 lg:col-span-1">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-gold-500 flex items-center justify-center text-white font-bold text-body-sm">
                {SITE_CONFIG.collegeShortName.slice(0, 2)}
              </div>
              <div className="text-white font-semibold text-body">
                {SITE_CONFIG.collegeShortName}
              </div>
            </div>
            <p className="text-body-sm text-navy-300 leading-relaxed mb-4">
              {SITE_CONFIG.tagline}
            </p>
            <div className="space-y-1.5 text-body-sm text-navy-300">
              <p>{SITE_CONFIG.address}</p>
              <p>{SITE_CONFIG.email}</p>
            </div>
          </div>

          {/* Academics Links */}
          <div>
            <h3 className="text-white font-semibold text-body-sm uppercase tracking-wider mb-4">
              Academics
            </h3>
            <ul className="space-y-2.5">
              {FOOTER_LINKS.academics.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-body-sm text-navy-300 hover:text-white transition-colors duration-[var(--transition-fast)]"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Student Links */}
          <div>
            <h3 className="text-white font-semibold text-body-sm uppercase tracking-wider mb-4">
              Students
            </h3>
            <ul className="space-y-2.5">
              {FOOTER_LINKS.students.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-body-sm text-navy-300 hover:text-white transition-colors duration-[var(--transition-fast)]"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold text-body-sm uppercase tracking-wider mb-4">
              Quick Links
            </h3>
            <ul className="space-y-2.5">
              {FOOTER_LINKS.quickLinks.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-body-sm text-navy-300 hover:text-white transition-colors duration-[var(--transition-fast)]"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-navy-800 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-caption text-navy-400">
            &copy; {currentYear} {SITE_CONFIG.collegeName}. All rights reserved.
          </p>
          <p className="text-caption text-navy-500">
            Demo portal built for educational purposes
          </p>
        </div>
      </div>
    </footer>
  );
}

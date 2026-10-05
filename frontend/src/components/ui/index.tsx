import { type ReactNode } from "react";

// ============================================
// Button
// ============================================

type ButtonVariant = "primary" | "secondary" | "outline" | "ghost" | "gold";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  children: ReactNode;
  asChild?: boolean;
}

const buttonVariants: Record<ButtonVariant, string> = {
  primary:
    "bg-navy-800 text-white hover:bg-navy-700 active:bg-navy-900",
  secondary:
    "bg-slate-100 text-slate-800 hover:bg-slate-200 active:bg-slate-300 border border-border",
  outline:
    "bg-transparent text-navy-800 border border-navy-300 hover:bg-navy-50 active:bg-navy-100",
  ghost:
    "bg-transparent text-slate-700 hover:bg-slate-100 active:bg-slate-200",
  gold:
    "bg-gold-500 text-white hover:bg-gold-600 active:bg-gold-700",
};

const buttonSizes: Record<ButtonSize, string> = {
  sm: "px-3.5 py-1.5 text-body-sm",
  md: "px-5 py-2.5 text-body-sm font-medium",
  lg: "px-6 py-3 text-body font-medium",
};

export function Button({
  variant = "primary",
  size = "md",
  className = "",
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-md transition-colors duration-[var(--transition-fast)] cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${buttonVariants[variant]} ${buttonSizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

// ============================================
// Badge
// ============================================

type BadgeVariant = "default" | "primary" | "gold" | "success" | "warning" | "error" | "info";

interface BadgeProps {
  variant?: BadgeVariant;
  children: ReactNode;
  className?: string;
}

const badgeVariants: Record<BadgeVariant, string> = {
  default: "bg-slate-100 text-slate-700",
  primary: "bg-navy-100 text-navy-800",
  gold: "bg-gold-100 text-gold-700",
  success: "bg-emerald-50 text-emerald-700",
  warning: "bg-amber-50 text-amber-700",
  error: "bg-red-50 text-red-700",
  info: "bg-blue-50 text-blue-700",
};

export function Badge({ variant = "default", children, className = "" }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-caption font-medium ${badgeVariants[variant]} ${className}`}
    >
      {children}
    </span>
  );
}

// ============================================
// Card
// ============================================

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  padding?: "none" | "sm" | "md" | "lg";
}

const cardPadding = {
  none: "",
  sm: "p-4",
  md: "p-5 sm:p-6",
  lg: "p-6 sm:p-8",
};

export function Card({ children, className = "", hover = false, padding = "md" }: CardProps) {
  return (
    <div
      className={`bg-surface-raised border border-border rounded-lg shadow-[var(--shadow-sm)] ${
        hover ? "transition-shadow duration-[var(--transition-base)] hover:shadow-[var(--shadow-lg)]" : ""
      } ${cardPadding[padding]} ${className}`}
    >
      {children}
    </div>
  );
}

// ============================================
// SectionHeading
// ============================================

interface SectionHeadingProps {
  title: string;
  subtitle?: string;
  align?: "left" | "center";
  className?: string;
}

export function SectionHeading({
  title,
  subtitle,
  align = "center",
  className = "",
}: SectionHeadingProps) {
  return (
    <div className={`mb-10 ${align === "center" ? "text-center" : "text-left"} ${className}`}>
      <h2 className="text-h2 text-text-primary">{title}</h2>
      {subtitle && (
        <p className="mt-3 text-body-lg text-text-secondary max-w-2xl mx-auto">{subtitle}</p>
      )}
      <div
        className={`mt-4 h-1 w-12 rounded-full bg-gold-500 ${
          align === "center" ? "mx-auto" : ""
        }`}
        aria-hidden="true"
      />
    </div>
  );
}

// ============================================
// Container
// ============================================

interface ContainerProps {
  children: ReactNode;
  className?: string;
}

export function Container({ children, className = "" }: ContainerProps) {
  return <div className={`section-container ${className}`}>{children}</div>;
}

// ============================================
// Section
// ============================================

interface SectionProps {
  children: ReactNode;
  className?: string;
  background?: "white" | "light" | "navy";
  id?: string;
}

const sectionBg = {
  white: "bg-background",
  light: "bg-surface",
  navy: "bg-navy-800 text-text-inverse",
};

export function Section({ children, className = "", background = "white", id }: SectionProps) {
  return (
    <section id={id} className={`section-padding ${sectionBg[background]} ${className}`}>
      <div className="section-container">{children}</div>
    </section>
  );
}

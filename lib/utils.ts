/**
 * Utility functions
 */

/**
 * Format a CHDI score into a human-readable status badge config.
 */
export function getCHDIBadgeConfig(status: string): {
  label: string;
  color: string;
  bg: string;
  dot: string;
} {
  switch (status) {
    case "healthy":
      return { label: "Healthy", color: "text-emerald-700", bg: "bg-emerald-100", dot: "bg-emerald-500" };
    case "watch":
      return { label: "Watch", color: "text-amber-700", bg: "bg-amber-100", dot: "bg-amber-500" };
    case "at-risk":
      return { label: "At Risk", color: "text-red-700", bg: "bg-red-100", dot: "bg-red-500" };
    case "abstain":
    default:
      return { label: "Insufficient Data", color: "text-slate-600", bg: "bg-slate-100", dot: "bg-slate-400" };
  }
}

/**
 * Format a relative time string ("2 hours ago", "3 days ago")
 */
export function timeAgo(date: Date | string): string {
  const d = new Date(date);
  const diff = Date.now() - d.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return "Just now";
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 30) return `${days}d ago`;
  return d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

/**
 * Calculate age from date of birth
 */
export function calcAge(dob: Date | string): string {
  const d = new Date(dob);
  const now = new Date();
  const months =
    (now.getFullYear() - d.getFullYear()) * 12 + (now.getMonth() - d.getMonth());
  if (months < 1) return "< 1 month";
  if (months < 12) return `${months} months`;
  const years = Math.floor(months / 12);
  const rem = months % 12;
  return rem > 0 ? `${years}y ${rem}m` : `${years} years`;
}

/**
 * Format a number to a fixed decimal with fallback dash
 */
export function fmt(n: number | null | undefined, decimals = 1): string {
  if (n === null || n === undefined || isNaN(n)) return "—";
  return n.toFixed(decimals);
}

/**
 * Format date to clean Indian locale date string (e.g. 20 Sep 2026)
 */
export function fmtDate(d: Date | string | null | undefined): string {
  if (!d) return "—";
  return new Date(d).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

/**
 * Urgency label and color for vet cases
 */
export function getUrgencyConfig(urgency: string) {
  switch (urgency) {
    case "critical":
      return { label: "Critical", color: "text-red-600", bg: "bg-red-100 border-red-200" };
    case "high":
      return { label: "High", color: "text-orange-600", bg: "bg-orange-100 border-orange-200" };
    case "medium":
      return { label: "Medium", color: "text-amber-600", bg: "bg-amber-100 border-amber-200" };
    default:
      return { label: "Low", color: "text-slate-600", bg: "bg-slate-100 border-slate-200" };
  }
}

/**
 * Simple cuid-like ID generator (fallback when crypto is unavailable)
 */
export function cuid(): string {
  return `c${Date.now().toString(36)}${Math.random().toString(36).slice(2)}`;
}

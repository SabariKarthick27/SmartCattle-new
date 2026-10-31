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

/**
 * Breed-specific core body temperature thresholds and clinical interpretations.
 */
export interface BreedTemperatureConfig {
  category: string;
  breedMatched: string;
  normalMin: number;
  normalMax: number;
  watchMin: number;
  watchMax: number;
  feverMin: number;
  normalLabel: string;
  watchLabel: string;
  feverLabel: string;
  clinicalNote: string;
}

export function getBreedTemperatureConfig(breedName: string = ""): BreedTemperatureConfig {
  const b = (breedName || "").toLowerCase();

  // Native Indian Zebu / Bos indicus (e.g. Kangayam, Gir, Sahiwal, Hallikar, Umblachery, Bargur)
  if (
    b.includes("kangayam") ||
    b.includes("கங்கேயம்") ||
    b.includes("gir") ||
    b.includes("sahiwal") ||
    b.includes("red sindhi") ||
    b.includes("tharparkar") ||
    b.includes("ongole") ||
    b.includes("hallikar") ||
    b.includes("amritmahal") ||
    b.includes("bargur") ||
    b.includes("umblachery") ||
    b.includes("desi") ||
    b.includes("indicus")
  ) {
    return {
      category: "Native Zebu (Bos indicus)",
      breedMatched: "Kangayam / Native Zebu",
      normalMin: 38.0,
      normalMax: 38.6,
      watchMin: 38.7,
      watchMax: 39.1,
      feverMin: 39.2,
      normalLabel: "38.0°C – 38.6°C",
      watchLabel: "38.7°C – 39.1°C",
      feverLabel: "≥ 39.2°C",
      clinicalNote:
        "Native Zebu cattle possess superior heat tolerance (high sweat gland density, dewlap) and lower metabolic load. Physiological baseline rarely exceeds 38.6°C; an elevation to ≥ 39.2°C signifies active infection.",
    };
  }

  // Jersey Crossbred
  if (b.includes("jersey")) {
    return {
      category: "Jersey Crossbred",
      breedMatched: "Jersey Crossbred",
      normalMin: 38.2,
      normalMax: 38.8,
      watchMin: 38.9,
      watchMax: 39.4,
      feverMin: 39.5,
      normalLabel: "38.2°C – 38.8°C",
      watchLabel: "38.9°C – 39.4°C",
      feverLabel: "≥ 39.5°C",
      clinicalNote:
        "High-yielding dairy crossbreds generate higher internal metabolic heat. Subclinical thermal stress ranges between 38.9°C – 39.4°C, while acute pyrexia (fever) is confirmed at ≥ 39.5°C.",
    };
  }

  // Holstein Friesian Crossbred (HF)
  if (
    b.includes("holstein") ||
    b.includes("hf") ||
    b.includes("friesian") ||
    b.includes("ayrshire") ||
    b.includes("brown swiss")
  ) {
    return {
      category: "Holstein Friesian Crossbred",
      breedMatched: "HF Crossbred",
      normalMin: 38.3,
      normalMax: 38.9,
      watchMin: 39.0,
      watchMax: 39.4,
      feverMin: 39.5,
      normalLabel: "38.3°C – 38.9°C",
      watchLabel: "39.0°C – 39.4°C",
      feverLabel: "≥ 39.5°C",
      clinicalNote:
        "Heavy dairy breed producing large milk volumes. High baseline metabolic heat production. True infectious pyrexia is confirmed at ≥ 39.5°C.",
    };
  }

  // Default Standard Bovine
  return {
    category: "Standard Bovine",
    breedMatched: breedName || "Standard Bovine",
    normalMin: 38.0,
    normalMax: 38.8,
    watchMin: 38.9,
    watchMax: 39.4,
    feverMin: 39.5,
    normalLabel: "38.0°C – 38.8°C",
    watchLabel: "38.9°C – 39.4°C",
    feverLabel: "≥ 39.5°C",
    clinicalNote: "Standard veterinary bovine core body temperature threshold boundaries.",
  };
}

export function evaluateTemperatureStatus(
  val: number,
  breedName: string = ""
): {
  status: "normal" | "watch" | "fever" | "hypothermic";
  label: string;
  badgeClass: string;
  textClass: string;
} {
  const config = getBreedTemperatureConfig(breedName);
  if (val >= config.feverMin) {
    return {
      status: "fever",
      label: "High Fever (Pyrexia)",
      badgeClass: "bg-red-100 text-red-800 border border-red-200",
      textClass: "text-red-600",
    };
  }
  if (val >= config.watchMin) {
    return {
      status: "watch",
      label: "Low-Grade Elevation",
      badgeClass: "bg-amber-100 text-amber-800 border border-amber-200",
      textClass: "text-amber-600",
    };
  }
  if (val < config.normalMin - 0.5) {
    return {
      status: "hypothermic",
      label: "Hypothermia (Low Temp)",
      badgeClass: "bg-blue-100 text-blue-800 border border-blue-200",
      textClass: "text-blue-600",
    };
  }
  return {
    status: "normal",
    label: "Normal",
    badgeClass: "bg-emerald-100 text-emerald-800 border border-emerald-200",
    textClass: "text-emerald-700",
  };
}

import React from "react";

export function SmartCattleLogoIcon({ className = "w-9 h-9 sm:w-10 sm:h-10" }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="SmartCattle Logo"
    >
      <defs>
        {/* Warm Golden Harvest Medallion Gradient */}
        <linearGradient id="sc-gold-disc" x1="10" y1="10" x2="90" y2="90" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#f5b244" />
          <stop offset="45%" stopColor="#e5a035" />
          <stop offset="100%" stopColor="#d18a1a" />
        </linearGradient>

        {/* Forest Pine Subtle Outer Border */}
        <linearGradient id="sc-border-gradient" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#1b4332" stopOpacity="0.4" />
          <stop offset="100%" stopColor="#081c14" stopOpacity="0.7" />
        </linearGradient>
      </defs>

      {/* Golden Disc Medallion */}
      <circle cx="50" cy="50" r="48" fill="url(#sc-gold-disc)" />
      <circle cx="50" cy="50" r="48" stroke="url(#sc-border-gradient)" strokeWidth="1" />

      {/* ── Exact Reference Cow Silhouette with S-Cutout & Detailed Features ── */}
      <g fill="#0e2319">
        {/* Solid Silhouette of the Full Indigenous Cow */}
        <path
          fillRule="evenodd"
          clipRule="evenodd"
          d="
            M 67.5 32.8
            C 63.5 34.5 60.5 36.5 58.5 37.0
            C 58.0 34.2 57.5 34.0 57.0 34.5
            C 56.5 35.5 56.0 37.5 54.0 38.5
            C 50.0 40.2 46.0 42.2 43.5 42.5
            C 40.8 42.8 38.5 46.2 36.5 46.2
            C 34.5 46.2 33.0 42.5 31.5 39.5
            C 28.5 38.5 25.5 39.5 24.5 43.5
            C 23.5 47.5 24.2 52.0 25.5 55.5
            C 25.8 55.5 26.2 53.8 26.5 51.5
            C 26.8 48.5 26.2 45.5 27.2 43.0
            C 28.2 40.5 30.2 39.8 31.5 39.8
            C 32.5 43.0 33.5 47.5 32.5 52.0
            C 31.8 55.0 29.0 56.5 29.0 64.0
            L 32.5 64.0
            C 33.5 59.5 34.5 56.0 36.0 54.0
            C 38.5 54.5 43.0 54.5 46.5 53.5
            C 47.0 56.0 47.5 60.0 47.5 64.0
            L 50.5 64.0
            C 50.5 59.5 51.0 56.5 51.5 54.5
            C 52.5 54.8 53.0 57.0 53.0 64.0
            L 56.0 64.0
            C 56.2 59.0 56.5 55.0 57.5 52.5
            C 60.0 50.5 62.5 47.0 62.5 45.0
            C 65.5 45.0 68.0 43.5 69.5 42.5
            C 67.5 40.5 64.0 38.0 61.5 37.0
            C 63.5 35.8 66.0 34.2 67.5 32.8
            Z

            M 27.5 43.5
            C 26.2 46.0 26.5 49.5 27.5 51.8
            C 28.8 51.0 30.2 48.5 30.5 45.5
            C 30.5 43.5 29.2 42.2 27.5 43.5
            Z

            M 52.5 40.5
            C 55.5 40.8 58.2 41.5 58.0 43.0
            C 57.8 44.5 55.5 45.0 53.2 45.5
            C 51.0 46.0 49.5 47.0 50.0 49.0
            C 50.5 50.8 53.0 51.5 56.5 50.0
            C 57.5 51.5 55.5 52.8 52.5 53.0
            C 48.5 53.0 46.5 50.0 47.0 47.5
            C 47.5 45.0 50.0 44.0 52.5 43.5
            C 54.8 43.0 55.8 42.5 55.5 41.8
            C 55.2 41.2 53.5 41.0 51.5 41.2
            Z
          "
        />

        {/* Distinct Hind Knee / Belly Accent Bar */}
        <polygon points="34.5,58.5 39.5,60.5 39.0,63.5 34.0,61.5" />

        {/* Golden Eye Feature */}
        <circle cx="63.8" cy="39.8" r="1.6" fill="#e5a035" />
      </g>
    </svg>
  );
}

export function SmartCattleLogo({
  variant = "dark",
  subtitle,
  className = "",
}: {
  variant?: "dark" | "light";
  subtitle?: string;
  className?: string;
}) {
  const isLight = variant === "light";

  return (
    <div className={`flex items-center gap-2.5 sm:gap-3 ${className}`}>
      <SmartCattleLogoIcon className="w-9 h-9 sm:w-10 sm:h-10 shrink-0 drop-shadow-sm transition-transform hover:scale-105 duration-200" />
      <div className="flex flex-col">
        <div className="flex items-center">
          <span
            className={`font-extrabold tracking-tight text-lg sm:text-xl font-display leading-tight ${
              isLight ? "text-white" : "text-slate-950"
            }`}
          >
            Smart<span className={isLight ? "text-emerald-300" : "text-emerald-800"}>Cattle</span>
          </span>
        </div>
        {subtitle && (
          <span
            className={`text-[9.5px] sm:text-[10.5px] font-mono tracking-wider font-bold uppercase mt-0.5 ${
              isLight ? "text-emerald-300/90" : "text-emerald-800"
            }`}
          >
            {subtitle}
          </span>
        )}
      </div>
    </div>
  );
}


"use client";

import React from "react";
import {
  IconScan,
  IconStethoscope,
  IconShieldAlert,
  IconActivity,
  IconCheckCircle,
} from "@/components/icons";

export default function HeroInteractiveWorkbench() {
  return (
    <div className="relative w-full max-w-lg mx-auto select-none py-4">
      {/* Dynamic Ambient Background Glows */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-gradient-to-tr from-emerald-200/50 to-teal-300/30 rounded-full blur-3xl -z-10 pointer-events-none" />
      <div className="absolute -top-6 -right-6 w-48 h-48 bg-emerald-100/60 rounded-full blur-2xl -z-10 pointer-events-none" />

      {/* Modern Agri-Tech Visual Composition */}
      <div className="relative flex flex-col items-center justify-center p-6 sm:p-8">
        {/* Outer Circular Pulse Radar Ring */}
        <div className="relative w-72 h-72 sm:w-80 sm:h-80 flex items-center justify-center">
          {/* Concentric Radar Rings */}
          <div className="absolute inset-0 rounded-full border border-emerald-200/60 animate-[spin_40s_linear_infinite]" />
          <div className="absolute inset-4 rounded-full border border-dashed border-emerald-300/40 animate-[spin_30s_linear_infinite_reverse]" />
          <div className="absolute inset-12 rounded-full border border-slate-200/80" />
          <div className="absolute inset-20 rounded-full bg-gradient-to-b from-emerald-50/80 to-white/90 border border-emerald-100 shadow-inner" />

          {/* Central Intelligent Core */}
          <div className="relative z-10 w-28 h-28 sm:w-32 sm:h-32 rounded-2xl bg-gradient-to-br from-[#123326] via-[#0d2a1f] to-[#061811] border border-emerald-500/40 shadow-2xl flex flex-col items-center justify-center text-center p-3 group transition-transform duration-300 hover:scale-105">
            <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-400/40 flex items-center justify-center text-emerald-300 shadow-sm mb-1.5">
              <IconActivity className="w-6 h-6 text-emerald-300" />
            </div>
            <span className="text-[11px] font-mono font-bold tracking-wider text-emerald-300 uppercase">
              SMART CARE
            </span>
            <span className="text-[9px] font-mono text-emerald-400/80 tracking-tight">
              AI Health Engine
            </span>
          </div>

          {/* Orbiting Satellite Node 1: Fast QR Scan (Top Left) */}
          <div className="absolute -top-2 left-2 sm:left-4 z-20 bg-white/95 backdrop-blur-md px-3.5 py-2.5 rounded-xl border border-slate-200/90 shadow-lg flex items-center gap-2.5 transition-transform hover:-translate-y-1 duration-150">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700">
              <IconScan className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-bold text-slate-900 leading-tight">Instant QR Tagging</div>
              <div className="text-[10px] font-mono text-emerald-700 font-semibold">&lt; 15s Mobile Scan</div>
            </div>
          </div>

          {/* Orbiting Satellite Node 2: Weekly Vet Checkups (Bottom Right) */}
          <div className="absolute -bottom-2 right-2 sm:right-4 z-20 bg-white/95 backdrop-blur-md px-3.5 py-2.5 rounded-xl border border-slate-200/90 shadow-lg flex items-center gap-2.5 transition-transform hover:-translate-y-1 duration-150">
            <div className="w-8 h-8 rounded-lg bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700">
              <IconStethoscope className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-bold text-slate-900 leading-tight">Weekly Vet Checkups</div>
              <div className="text-[10px] font-mono text-teal-700 font-semibold">Routine Vitals &amp; Reports</div>
            </div>
          </div>

          {/* Orbiting Satellite Node 3: District Protection (Top Right) */}
          <div className="absolute top-12 -right-4 sm:-right-6 z-20 bg-white/95 backdrop-blur-md px-3.5 py-2.5 rounded-xl border border-slate-200/90 shadow-lg flex items-center gap-2.5 transition-transform hover:-translate-y-1 duration-150">
            <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-700">
              <IconShieldAlert className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-bold text-slate-900 leading-tight">Disease Shield</div>
              <div className="text-[10px] font-mono text-blue-700 font-semibold">Regional Coverage</div>
            </div>
          </div>

          {/* Orbiting Satellite Node 4: Weekly Health Baseline (Bottom Left) */}
          <div className="absolute bottom-10 -left-4 sm:-left-6 z-20 bg-white/95 backdrop-blur-md px-3.5 py-2.5 rounded-xl border border-slate-200/90 shadow-lg flex items-center gap-2.5 transition-transform hover:-translate-y-1 duration-150">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700">
              <IconCheckCircle className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-bold text-slate-900 leading-tight">Weekly Baseline</div>
              <div className="text-[10px] font-mono text-emerald-700 font-semibold">7-Day Health Cycle</div>
            </div>
          </div>
        </div>

        {/* Bottom Platform Feature Badges Strip */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-2.5 text-xs font-mono">
          <span className="px-3.5 py-1.5 bg-white/90 border border-slate-200 rounded-full text-slate-800 font-semibold shadow-xs">
            ✓ Weekly Vet Health Checkups
          </span>
          <span className="px-3.5 py-1.5 bg-white/90 border border-slate-200 rounded-full text-slate-800 font-semibold shadow-xs">
            ✓ Weekly Health Baseline
          </span>
          <span className="px-3.5 py-1.5 bg-emerald-50 border border-emerald-300 rounded-full text-emerald-900 font-bold shadow-xs">
            ✓ Mobile Phone Ready
          </span>
        </div>
      </div>
    </div>
  );
}

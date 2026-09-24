"use client";

import React from "react";

export default function HeroTelemetryPill() {
  return (
    <div className="pt-6 border-t border-slate-100 flex items-center">
      {/* ── Motion & Live Telemetry Pill ── */}
      <div 
        className="group relative h-10 px-4 sm:px-5 rounded-full bg-gradient-to-r from-emerald-50/90 via-teal-50/80 to-emerald-50/90 border border-emerald-200/90 hover:border-emerald-400/80 shadow-[0_2px_10px_rgba(16,185,129,0.08)] hover:shadow-[0_4px_20px_rgba(16,185,129,0.18)] flex items-center gap-3.5 transition-all duration-300 backdrop-blur-sm cursor-default"
      >
        {/* Tri-Dot Radar Cluster */}
        <div className="flex items-center gap-1.5" title="Live Health Stream">
          <span className="relative flex h-3 w-3 items-center justify-center">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 duration-1000" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]" />
          </span>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse duration-700 delay-150" />
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-300 animate-pulse duration-700 delay-300" />
        </div>

        {/* Subtle Divider */}
        <div className="h-4 w-px bg-emerald-300/80" />

        {/* Nodes & Flowing Energy Streams */}
        <div className="flex items-center gap-3 text-emerald-800">
          {/* Node 1: Fast QR Scan Lightning */}
          <div
            className="relative flex items-center justify-center group/node cursor-pointer"
            title="Instant QR Ear Tag Scan"
          >
            <div className="p-1 rounded-md transition-all duration-200 group-hover/node:bg-emerald-100/80 group-hover/node:scale-110">
              <svg 
                className="w-4 h-4 text-emerald-700 group-hover/node:text-emerald-950 transition-colors drop-shadow-xs" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth={2.2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
              </svg>
            </div>
          </div>

          {/* Flowing Energy Stream 1 */}
          <div className="h-2 w-14 sm:w-16 bg-emerald-200/60 rounded-full overflow-hidden relative shadow-inner">
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-300 via-teal-400 to-emerald-300 opacity-50" />
            {/* Pulsing Light Stream */}
            <div className="absolute top-0 bottom-0 w-8 bg-gradient-to-r from-transparent via-emerald-500 to-transparent rounded-full animate-flow-stream shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
          </div>

          {/* Node 2: Continuous Health Shield */}
          <div
            className="relative flex items-center justify-center group/node cursor-pointer"
            title="Weekly Health Baseline & Protection"
          >
            <div className="p-1 rounded-md transition-all duration-200 group-hover/node:bg-emerald-100/80 group-hover/node:scale-110">
              <svg 
                className="w-4 h-4 text-emerald-700 group-hover/node:text-emerald-950 transition-colors drop-shadow-xs" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth={2.2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
              </svg>
            </div>
          </div>

          {/* Flowing Energy Stream 2 */}
          <div className="h-2 w-14 sm:w-16 bg-emerald-200/60 rounded-full overflow-hidden relative shadow-inner">
            <div className="absolute inset-0 bg-gradient-to-r from-teal-400 via-emerald-300 to-teal-400 opacity-50" />
            {/* Pulsing Light Stream with offset timing */}
            <div className="absolute top-0 bottom-0 w-8 bg-gradient-to-r from-transparent via-teal-500 to-transparent rounded-full animate-flow-stream-delayed shadow-[0_0_8px_rgba(20,184,166,0.8)]" />
          </div>

          {/* Node 3: Rotating Global Farm Network */}
          <div
            className="relative flex items-center justify-center group/node cursor-pointer"
            title="District Cloud Disease Shield"
          >
            <div className="p-1 rounded-md transition-all duration-200 group-hover/node:bg-emerald-100/80 group-hover/node:scale-110">
              <svg 
                className="w-4 h-4 text-emerald-700 group-hover/node:text-emerald-950 transition-colors animate-[spin_12s_linear_infinite] group-hover/node:animate-[spin_3s_linear_infinite]" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth={2.2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

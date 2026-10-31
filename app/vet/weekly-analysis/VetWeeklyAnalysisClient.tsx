"use client";

import { useState } from "react";
import { IconCheckCircle, IconUser } from "@/components/icons";

interface WeeklyReport {
  cattleId: string;
  tagId: string;
  name: string | null;
  breed: string;
  region: string | null;
  farmerId: string;
  farmerName: string;
  farmerPhone: string;
  weekStartDate: string;
  weekEndDate: string;
  weekLabel?: string;
  avgCHDIScore: number | null;
  healthStatus: "healthy" | "watch" | "at-risk" | "abstain";
  avgMilkYield: number;
  weightTrendKg: number;
  avgTemperature: number;
  totalFeedKg: number;
  topRiskFactors: Array<{ factor: string; contribution: number; direction: string }>;
  sentToFarmer?: boolean;
}

interface Props {
  initialReports: WeeklyReport[];
  vetRegion?: string | null;
}

export default function VetWeeklyAnalysisClient({ initialReports, vetRegion }: Props) {
  const [reports] = useState<WeeklyReport[]>(initialReports);
  const [selectedReport, setSelectedReport] = useState<WeeklyReport | null>(null);
  const [vetNotes, setVetNotes] = useState("");
  const [sending, setSending] = useState(false);
  const [sentStatus, setSentStatus] = useState<Record<string, boolean>>({});
  const [msg, setMsg] = useState("");

  const handleSendToFarmer = async (report: WeeklyReport) => {
    setSending(true);
    setMsg("");

    const res = await fetch("/api/vet/weekly-analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cattleId: report.cattleId,
        healthStatus: report.healthStatus,
        vetNotes: vetNotes || `Weekly Health Report (${report.weekStartDate} to ${report.weekEndDate}): Health Score is ${report.avgCHDIScore}/100. Overall condition: ${report.healthStatus.toUpperCase()}.`,
      }),
    });

    const data = await res.json();
    setSending(false);

    if (res.ok) {
      const sentKey = `${report.cattleId}_${report.weekStartDate}`;
      setSentStatus((prev) => ({ ...prev, [sentKey]: true }));
      setMsg(`Weekly report sent to ${report.farmerName} (${report.farmerPhone})!`);
      setSelectedReport(null);
      setVetNotes("");
    } else {
      setMsg(data.error || "Failed to send report to farmer.");
    }
  };

  return (
    <div className="space-y-6">
      <div className="pb-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              Weekly Health Reports
            </h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
              7-DAY SUMMARY
            </span>
          </div>

        </div>
      </div>

      {msg && (
        <div className="p-3.5 rounded-lg bg-emerald-50 text-emerald-900 border border-emerald-300 font-medium text-xs flex items-center gap-2">
          <IconCheckCircle className="w-4 h-4 text-emerald-700" /> {msg}
        </div>
      )}

      {/* Reports Grid */}
      {reports.length === 0 ? (
        <div className="card p-12 text-center bg-white border border-slate-300 shadow-xs rounded-xl text-slate-500 text-xs">
          No cattle found in {vetRegion || "your assigned region"} to analyze.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {reports.map((r) => {
            const reportKey = `${r.cattleId}_${r.weekStartDate}`;
            const isSent = r.sentToFarmer || sentStatus[reportKey];
            return (
              <div key={reportKey} className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-mono font-bold text-slate-950 text-base">{r.tagId}</span>
                        {r.name && <span className="text-xs font-bold text-slate-700">({r.name})</span>}
                        {r.weekLabel && (
                          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                            {r.weekLabel}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-500">{r.breed} · {r.region || "Tamil Nadu"}</p>
                    </div>

                    <span className={`badge-${r.healthStatus} text-[10px]`}>
                      Score: {r.healthStatus === "abstain" ? "—" : r.avgCHDIScore} · {r.healthStatus === "abstain" ? "LEARNING" : r.healthStatus.toUpperCase()}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-[#f8faf9] rounded-lg p-3 border border-slate-200 text-center">
                    <div>
                      <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Daily Milk</p>
                      <p className="text-sm font-bold text-slate-900 mt-0.5">{r.avgMilkYield} L</p>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Feed Intake</p>
                      <p className="text-sm font-bold text-slate-900 mt-0.5">{r.totalFeedKg} kg</p>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Weight</p>
                      <p className={`text-sm font-bold mt-0.5 font-mono ${r.weightTrendKg < 0 ? "text-red-700" : "text-emerald-700"}`}>
                        {r.weightTrendKg > 0 ? `+${r.weightTrendKg}` : r.weightTrendKg} kg
                      </p>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Core Temp</p>
                      <p className={`text-sm font-bold mt-0.5 font-mono ${r.avgTemperature >= 39.5 ? "text-red-700" : r.avgTemperature >= 38.9 ? "text-amber-700" : "text-emerald-700"}`}>
                        {r.avgTemperature.toFixed(1)} °C
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-slate-500 mt-3">
                    <span className="flex items-center gap-1">
                      <IconUser className="w-3.5 h-3.5 text-slate-400" />
                      Farmer: <strong className="text-slate-800">{r.farmerName}</strong>
                    </span>
                    <span className="font-mono text-[11px]">{r.weekStartDate.slice(5)} to {r.weekEndDate.slice(5)}</span>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-100">
                  {(selectedReport?.cattleId === r.cattleId && selectedReport?.weekStartDate === r.weekStartDate) ? (
                    <div className="space-y-2">
                      {/* Quick Plain English Presets */}
                      <div>
                        <p className="text-[10px] font-mono font-bold text-slate-500 uppercase mb-1">
                          Quick Advice Presets:
                        </p>
                        <div className="flex flex-wrap gap-1.5 mb-2">
                          <button
                            type="button"
                            onClick={() => setVetNotes("Cow is healthy and doing well. Continue regular daily feed and clean drinking water.")}
                            className="text-[11px] px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 hover:bg-emerald-100 font-medium"
                          >
                            All Healthy
                          </button>
                          <button
                            type="button"
                            onClick={() => setVetNotes("Feed intake is slightly low. Provide more green fodder and fresh water today.")}
                            className="text-[11px] px-2.5 py-1 rounded-md bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 font-medium"
                          >
                            Add Fodder
                          </button>
                          <button
                            type="button"
                            onClick={() => setVetNotes("Mild temperature rise observed. The doctor will visit your farm today for a checkup.")}
                            className="text-[11px] px-2.5 py-1 rounded-md bg-red-50 text-red-800 border border-red-200 hover:bg-red-100 font-medium"
                          >
                            Doctor Visit
                          </button>
                        </div>
                      </div>

                      <textarea
                        className="input min-h-[70px] text-xs resize-none leading-relaxed font-medium"
                        placeholder="Type doctor advice in simple terms for the farmer..."
                        value={vetNotes}
                        onChange={(e) => setVetNotes(e.target.value)}
                      />
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => setSelectedReport(null)}
                          className="btn btn-secondary btn-sm text-xs"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={() => handleSendToFarmer(r)}
                          className="btn btn-primary btn-sm text-xs font-bold"
                          disabled={sending}
                        >
                          {sending ? "Sending..." : "Send Report to Farmer →"}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <button
                      onClick={() => {
                        if (isSent) return;
                        setSelectedReport(r);
                        setVetNotes(
                          r.healthStatus === "healthy"
                            ? "Cow is healthy and doing well. Continue regular daily feed and clean drinking water."
                            : r.healthStatus === "watch"
                            ? "Feed intake is slightly low. Provide more green fodder and fresh water today."
                            : r.healthStatus === "at-risk"
                            ? "Mild temperature rise observed. The doctor will visit your farm today for a checkup."
                            : "New cow registered. Baseline health data is currently being learned from daily records."
                        );
                      }}
                      disabled={isSent}
                      className={`btn btn-sm w-full justify-center text-xs font-semibold ${
                        isSent
                          ? "bg-emerald-50 text-emerald-900 border border-emerald-300 cursor-default"
                          : "btn-secondary"
                      }`}
                    >
                      {isSent ? "✓ Report Sent This Week" : "Send Weekly Report to Farmer →"}
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

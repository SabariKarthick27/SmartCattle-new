"use client";

import { useState } from "react";
import { IconActivity, IconCheckCircle, IconUser } from "@/components/icons";

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
  avgCHDIScore: number;
  healthStatus: "healthy" | "watch" | "at-risk";
  avgMilkYield: number;
  weightTrendKg: number;
  avgActivityScore: number;
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
      setSentStatus((prev) => ({ ...prev, [report.cattleId]: true }));
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
          <p className="text-xs text-slate-500 mt-0.5">
            7-day aggregated milk, weight trends, and one-click health reports for{" "}
            <span className="font-bold text-slate-800">{vetRegion || "Your District"}</span>
          </p>
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
            const isSent = r.sentToFarmer || sentStatus[r.cattleId];
            return (
              <div key={r.cattleId} className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-slate-950 text-base">{r.tagId}</span>
                        {r.name && <span className="text-xs font-bold text-slate-700">({r.name})</span>}
                      </div>
                      <p className="text-xs text-slate-500">{r.breed} · {r.region || "Tamil Nadu"}</p>
                    </div>

                    <span className={`badge-${r.healthStatus} text-[10px]`}>
                      Score: {r.avgCHDIScore} · {r.healthStatus.toUpperCase()}
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 bg-[#f8faf9] rounded-lg p-3 border border-slate-200 text-center">
                    <div>
                      <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Avg Milk</p>
                      <p className="text-sm font-bold text-slate-900 mt-0.5">{r.avgMilkYield} L/day</p>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Weight</p>
                      <p className={`text-sm font-bold mt-0.5 font-mono ${r.weightTrendKg < 0 ? "text-red-700" : "text-emerald-700"}`}>
                        {r.weightTrendKg > 0 ? `+${r.weightTrendKg}` : r.weightTrendKg} kg
                      </p>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Activity</p>
                      <p className="text-sm font-bold text-slate-900 mt-0.5">{r.avgActivityScore} / 100</p>
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
                  {selectedReport?.cattleId === r.cattleId ? (
                    <div className="space-y-2">
                      <textarea
                        className="input min-h-[70px] text-xs resize-none"
                        placeholder="Type doctor advice and notes for the farmer..."
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
                        setVetNotes(`Weekly Health Evaluation for Tag ${r.tagId}: 7-day average health score is ${r.avgCHDIScore}/100. Average milk yield is ${r.avgMilkYield} L/day. Overall condition is ${r.healthStatus.toUpperCase()}.`);
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

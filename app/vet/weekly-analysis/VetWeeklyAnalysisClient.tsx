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
        vetNotes: vetNotes || `Weekly Health Report (${report.weekStartDate} to ${report.weekEndDate}): Average CHDI Score ${report.avgCHDIScore}/100. Herd condition is ${report.healthStatus.toUpperCase()}.`,
      }),
    });

    const data = await res.json();
    setSending(false);

    if (res.ok) {
      setSentStatus((prev) => ({ ...prev, [report.cattleId]: true }));
      setMsg(`Weekly analysis report sent to ${report.farmerName} (${report.farmerPhone})!`);
      setSelectedReport(null);
      setVetNotes("");
    } else {
      setMsg(data.error || "Failed to send report to farmer.");
    }
  };

  const getStatusBadge = (status: string) => {
    if (status === "at-risk") return "bg-red-100 text-red-800 border-red-200";
    if (status === "watch") return "bg-amber-100 text-amber-800 border-amber-200";
    return "bg-emerald-100 text-emerald-800 border-emerald-200";
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
            <IconActivity className="w-6 h-6 text-teal-700" />
            Weekly Cattle Health Analysis
          </h1>
          <p className="text-slate-500 mt-1">
            7-day aggregated health trends, milk production averages, and once-a-week report dispatch for{" "}
            <span className="font-semibold text-slate-700">{vetRegion || "Assigned Region"}</span>
          </p>
        </div>
      </div>

      {msg && (
        <div className="p-4 rounded-xl bg-teal-50 text-teal-900 border border-teal-200 font-medium text-sm flex items-center gap-2">
          <IconCheckCircle className="w-5 h-5 text-teal-600" /> {msg}
        </div>
      )}

      {/* Reports Grid */}
      {reports.length === 0 ? (
        <div className="card p-8 text-center text-slate-500">
          No cattle registered in {vetRegion || "your assigned region"} to analyze.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {reports.map((r) => {
            const isSent = r.sentToFarmer || sentStatus[r.cattleId];
            return (
              <div key={r.cattleId} className="card p-6 flex flex-col justify-between hover:shadow-md transition-all">
                <div>
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-slate-900 text-lg">{r.tagId}</span>
                        {r.name && <span className="text-sm font-semibold text-slate-600">({r.name})</span>}
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">{r.breed} · {r.region || "Tamil Nadu"}</p>
                    </div>

                    <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getStatusBadge(r.healthStatus)}`}>
                      CHDI Avg: {r.avgCHDIScore} / 100 ({r.healthStatus.toUpperCase()})
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-3 bg-slate-50 rounded-xl p-3.5 mb-4 border border-slate-100 text-center">
                    <div>
                      <p className="text-xs text-slate-400">7-Day Avg Milk</p>
                      <p className="text-base font-bold text-slate-800 mt-0.5">{r.avgMilkYield} L/day</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-400">Weight Trend</p>
                      <p className={`text-base font-bold mt-0.5 ${r.weightTrendKg < 0 ? "text-red-600" : "text-emerald-600"}`}>
                        {r.weightTrendKg > 0 ? `+${r.weightTrendKg}` : r.weightTrendKg} kg
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-400">Activity Score</p>
                      <p className="text-base font-bold text-slate-800 mt-0.5">{r.avgActivityScore} / 100</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-slate-500 mb-4 px-1">
                    <span className="flex items-center gap-1.5">
                      <IconUser className="w-4 h-4 text-slate-400" />
                      Farmer: <strong className="text-slate-700">{r.farmerName}</strong>
                    </span>
                    <span>Week: {r.weekStartDate.slice(5)} to {r.weekEndDate.slice(5)}</span>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-100">
                  {selectedReport?.cattleId === r.cattleId ? (
                    <div className="space-y-3 animate-fade-in-up">
                      <textarea
                        className="input min-h-[80px] text-xs resize-none"
                        placeholder="Type weekly health notes & advice for farmer..."
                        value={vetNotes}
                        onChange={(e) => setVetNotes(e.target.value)}
                      />
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => setSelectedReport(null)}
                          className="btn-secondary btn-sm"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={() => handleSendToFarmer(r)}
                          className="btn-primary btn-sm"
                          disabled={sending}
                        >
                          {sending ? "Sending..." : "Confirm & Send Weekly Report →"}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <button
                      onClick={() => {
                        if (isSent) return;
                        setSelectedReport(r);
                        setVetNotes(`Weekly Health Evaluation for Tag ${r.tagId}: 7-day average CHDI score is ${r.avgCHDIScore}/100. Average milk yield is ${r.avgMilkYield} L/day. Condition is ${r.healthStatus.toUpperCase()}.`);
                      }}
                      disabled={isSent}
                      className={`btn-sm w-full justify-center ${
                        isSent
                          ? "bg-emerald-50 text-emerald-800 border border-emerald-200 cursor-default opacity-90"
                          : "bg-teal-700 text-white hover:bg-teal-800"
                      }`}
                    >
                      {isSent ? "✓ Report Sent for This Week (Once-a-Week Limit Active)" : "Send Weekly Analysis to Farmer →"}
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

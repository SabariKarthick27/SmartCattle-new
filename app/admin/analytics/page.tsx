"use client";

import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from "recharts";

const COLORS = ["#10b981", "#f59e0b", "#ef4444", "#94a3b8"];

export default function AdminAnalyticsPage() {
  const [data, setData] = useState<{
    summary: Record<string, number>;
    chdiByStatus: Array<{ status: string; _count: { status: number } }>;
    regionStats: Array<{ region: string; animalCount: number; avgCHDI: number }>;
    casesByMonth: Array<{ month: string; count: number }>;
    regionAlerts: Array<{ id: string; region: string; severity: string; triggeredAt: string }>;
  } | null>(null);

  useEffect(() => {
    fetch("/api/admin/analytics").then((r) => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="p-8 flex items-center justify-center h-96">
        <div className="text-center text-slate-400 font-mono text-xs">
          <div className="w-8 h-8 border-2 border-slate-300 border-t-[#123326] rounded-full animate-spin mx-auto mb-3" />
          Loading analytics...
        </div>
      </div>
    );
  }

  const pieData = (data.chdiByStatus ?? []).map((s) => ({
    name: s.status,
    value: s._count.status,
  }));

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div className="pb-4 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
            Herd Health Analytics
          </h1>
          <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
            STATE OVERVIEW
          </span>
        </div>
        <p className="text-xs text-slate-500 mt-0.5">
          Platform-wide cattle health metrics, sickness breakdown, and district reports.
        </p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: "Total Cattle", value: data.summary.totalCattle },
          { label: "Active Farmers", value: data.summary.totalFarmers },
          { label: "Active Vets", value: data.summary.totalVets },
          { label: "Resolved Cases (30d)", value: data.summary.resolvedCases },
        ].map((s) => (
          <div key={s.label} className="card p-3.5 bg-white border border-slate-300 shadow-xs rounded-xl">
            <div className="text-2xl font-extrabold text-slate-950 font-display tnum">{s.value ?? 0}</div>
            <div className="text-xs text-slate-600 font-medium mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CHDI status distribution */}
        <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-3">
          <h2 className="font-bold text-xs uppercase font-mono text-slate-800">Cattle Health Breakdown (30 Days)</h2>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" outerRadius={85} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="text-slate-400 text-center py-12 text-xs">No health records in last 30 days</p>}
        </div>

        {/* Cases resolved per month */}
        <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-3">
          <h2 className="font-bold text-xs uppercase font-mono text-slate-800">Cases Resolved per Month</h2>
          {data.casesByMonth.length > 0 ? (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={data.casesByMonth}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#123326" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="text-slate-400 text-center py-12 text-xs">No resolved cases yet</p>}
        </div>
      </div>

      {/* Regional stats */}
      <div className="card overflow-hidden bg-white border border-slate-300 shadow-xs rounded-xl">
        <div className="p-3.5 bg-[#f8faf9] border-b border-slate-200">
          <h2 className="font-bold text-xs uppercase font-mono text-slate-800">District Health Summary</h2>
        </div>
        <div className="table-container border-0 rounded-none">
          <table className="table">
            <thead>
              <tr><th>District</th><th>Animals Logged</th><th>Average Health Score</th></tr>
            </thead>
            <tbody>
              {data.regionStats.map((r, i) => (
                <tr key={i}>
                  <td className="font-bold text-slate-900 text-xs">{r.region}</td>
                  <td className="text-xs font-mono">{r.animalCount}</td>
                  <td>
                    <div className="flex items-center gap-2">
                      <span className="font-bold font-mono text-xs">{Math.round(r.avgCHDI)}</span>
                      <div className="w-24 h-1.5 bg-slate-200 rounded-full">
                        <div
                          className={`h-full rounded-full ${r.avgCHDI >= 75 ? "bg-emerald-600" : r.avgCHDI >= 50 ? "bg-amber-500" : "bg-red-600"}`}
                          style={{ width: `${Math.round(r.avgCHDI)}%` }}
                        />
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
              {data.regionStats.length === 0 && (
                <tr><td colSpan={3} className="text-center py-6 text-slate-400 text-xs">No district data yet</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Regional alerts */}
      {data.regionAlerts.length > 0 && (
        <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-3">
          <h2 className="font-bold text-xs uppercase font-mono text-slate-800">Active Disease Outbreak Alerts</h2>
          <div className="space-y-2">
            {data.regionAlerts.map((a) => (
              <div key={a.id} className={`p-3.5 rounded-lg border text-xs ${a.severity === "critical" ? "bg-red-50 border-red-300 text-red-900" : "bg-amber-50 border-amber-300 text-amber-900"}`}>
                <div className="flex items-center justify-between">
                  <p className="font-bold text-sm">{a.region}</p>
                  <span className={`font-mono font-bold text-[10px] px-2 py-0.5 rounded uppercase ${a.severity === "critical" ? "bg-red-100 text-red-800" : "bg-amber-100 text-amber-800"}`}>
                    {a.severity.toUpperCase()}
                  </span>
                </div>
                <p className="text-[11px] font-mono text-slate-500 mt-1">{new Date(a.triggeredAt).toLocaleString("en-IN")}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

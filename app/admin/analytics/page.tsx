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
        <div className="text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-slate-300 border-t-brand-600 rounded-full animate-spin mx-auto mb-3" />
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
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Herd Analytics</h1>
        <p className="text-slate-500 mt-1">Platform-wide health metrics and regional analysis</p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Total Cattle", value: data.summary.totalCattle },
          { label: "Active Farmers", value: data.summary.totalFarmers },
          { label: "Active Vets", value: data.summary.totalVets },
          { label: "Resolved (30d)", value: data.summary.resolvedCases },
        ].map((s) => (
          <div key={s.label} className="card p-4">
            <div className="text-2xl font-bold text-slate-900">{s.value ?? 0}</div>
            <div className="text-xs text-slate-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CHDI status distribution */}
        <div className="card p-6">
          <h2 className="font-semibold text-slate-900 mb-4">CHDI Status Distribution (30 days)</h2>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" outerRadius={90} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="text-slate-400 text-center py-12">No CHDI data in last 30 days</p>}
        </div>

        {/* Cases resolved per month */}
        <div className="card p-6">
          <h2 className="font-semibold text-slate-900 mb-4">Cases Resolved per Month</h2>
          {data.casesByMonth.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={data.casesByMonth}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#0F5132" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="text-slate-400 text-center py-12">No resolved cases yet</p>}
        </div>
      </div>

      {/* Regional stats */}
      <div className="card overflow-hidden">
        <div className="p-5 border-b border-slate-100">
          <h2 className="font-semibold text-slate-900">Regional Health Summary</h2>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr><th>Region</th><th>Animals Scored</th><th>Avg CHDI Score</th></tr>
            </thead>
            <tbody>
              {data.regionStats.map((r, i) => (
                <tr key={i}>
                  <td className="font-medium">{r.region}</td>
                  <td>{r.animalCount}</td>
                  <td>
                    <div className="flex items-center gap-2">
                      <span className="font-bold">{Math.round(r.avgCHDI)}</span>
                      <div className="w-24 h-1.5 bg-slate-200 rounded-full">
                        <div
                          className={`h-full rounded-full ${r.avgCHDI >= 75 ? "bg-emerald-500" : r.avgCHDI >= 50 ? "bg-amber-500" : "bg-red-500"}`}
                          style={{ width: `${Math.round(r.avgCHDI)}%` }}
                        />
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
              {data.regionStats.length === 0 && (
                <tr><td colSpan={3} className="text-center py-6 text-slate-400">No regional data yet</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Regional alerts */}
      {data.regionAlerts.length > 0 && (
        <div className="card p-5">
          <h2 className="font-semibold text-slate-900 mb-4">Active Regional Alerts</h2>
          <div className="space-y-3">
            {data.regionAlerts.map((a) => (
              <div key={a.id} className={`p-4 rounded-xl border ${a.severity === "critical" ? "bg-red-50 border-red-200" : "bg-amber-50 border-amber-200"}`}>
                <div className="flex items-center justify-between">
                  <p className="font-semibold text-slate-800">{a.region}</p>
                  <span className={`text-xs font-bold ${a.severity === "critical" ? "text-red-600" : "text-amber-600"}`}>
                    {a.severity.toUpperCase()}
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1">{new Date(a.triggeredAt).toLocaleString("en-IN")}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

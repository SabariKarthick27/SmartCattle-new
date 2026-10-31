"use client";

import { useEffect, useState } from "react";

interface AuditEntry {
  id: string;
  actorId: string;
  actorRole: string;
  action: string;
  targetId: string | null;
  timestamp: string;
  metadata: Record<string, unknown> | null;
  actor: { name: string; email: string };
}

export default function AdminAuditPage() {
  const [logs, setLogs] = useState<AuditEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({ action: "", role: "", from: "", to: "" });

  const fetchLogs = async () => {
    setLoading(true);
    const params = new URLSearchParams({ page: String(page), limit: "20" });
    if (filters.action) params.set("action", filters.action);
    if (filters.role) params.set("role", filters.role);
    if (filters.from) params.set("from", filters.from);
    if (filters.to) params.set("to", filters.to);

    const res = await fetch(`/api/admin/audit-log?${params}`);
    const data = await res.json();
    setLogs(data.logs ?? []);
    setTotal(data.total ?? 0);
    setLoading(false);
  };

  useEffect(() => { fetchLogs(); }, [page, filters]);

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              Activity &amp; Audit Logs
            </h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
              {total} EVENTS
            </span>
          </div>
        </div>
        <button
          onClick={fetchLogs}
          id="refresh-audit-btn"
          className="btn btn-secondary btn-sm text-xs font-semibold"
        >
          Refresh Logs
        </button>
      </div>

      {/* Filters */}
      <div className="card p-4 bg-white border border-slate-300 shadow-xs rounded-xl grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label className="label">Action Search</label>
          <input id="audit-action-filter" type="text" className="input text-xs" placeholder="e.g. login, create" value={filters.action} onChange={(e) => setFilters({ ...filters, action: e.target.value })} />
        </div>
        <div>
          <label className="label">Role Filter</label>
          <select id="audit-role-filter" className="input text-xs" value={filters.role} onChange={(e) => setFilters({ ...filters, role: e.target.value })}>
            <option value="">All roles</option>
            <option value="admin">Admin</option>
            <option value="vet">Veterinarian</option>
            <option value="farmer">Farmer</option>
            <option value="system">System</option>
          </select>
        </div>
        <div>
          <label className="label">From Date</label>
          <input id="audit-from" type="date" className="input text-xs" value={filters.from} onChange={(e) => setFilters({ ...filters, from: e.target.value })} />
        </div>
        <div>
          <label className="label">To Date</label>
          <input id="audit-to" type="date" className="input text-xs" value={filters.to} onChange={(e) => setFilters({ ...filters, to: e.target.value })} />
        </div>
      </div>

      {/* Table */}
      <div className="card overflow-hidden bg-white border border-slate-300 shadow-xs rounded-xl">
        <div className="table-container border-0 rounded-none">
          <table className="table">
            <thead>
              <tr><th>Timestamp</th><th>User / Actor</th><th>Role</th><th>Action</th><th>Target ID</th></tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id}>
                  <td className="text-xs font-mono text-slate-500 whitespace-nowrap">
                    {new Date(log.timestamp).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })}
                  </td>
                  <td>
                    <p className="font-bold text-slate-900 text-xs">{log.actor.name}</p>
                    <p className="text-[11px] text-slate-500 font-mono">{log.actor.email}</p>
                  </td>
                  <td>
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold font-mono uppercase bg-slate-100 text-slate-700 border border-slate-200">
                      {log.actorRole}
                    </span>
                  </td>
                  <td>
                    <code className="text-xs bg-slate-100 text-slate-800 px-2 py-0.5 rounded font-mono border border-slate-200">
                      {log.action}
                    </code>
                  </td>
                  <td className="text-xs text-slate-500 font-mono">{log.targetId?.slice(-8) ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {loading && <p className="p-8 text-center text-slate-400 text-xs font-mono">Loading activity...</p>}
          {!loading && logs.length === 0 && <p className="p-8 text-center text-slate-400 text-xs">No audit events match filters</p>}
        </div>

        {/* Pagination */}
        {total > 20 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-slate-200 bg-[#f8faf9]">
            <p className="text-xs font-mono text-slate-500">Showing {(page - 1) * 20 + 1}–{Math.min(page * 20, total)} of {total}</p>
            <div className="flex gap-2">
              <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1} className="btn btn-secondary btn-sm text-xs">← Prev</button>
              <button onClick={() => setPage((p) => p + 1)} disabled={page * 20 >= total} className="btn btn-secondary btn-sm text-xs">Next →</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

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
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Audit Log</h1>
          <p className="text-slate-500 mt-1">{total} total events recorded</p>
        </div>
        <button
          onClick={fetchLogs}
          id="refresh-audit-btn"
          className="btn-secondary"
        >
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="card p-4 grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label className="label">Action filter</label>
          <input id="audit-action-filter" type="text" className="input" placeholder="e.g. login" value={filters.action} onChange={(e) => setFilters({ ...filters, action: e.target.value })} />
        </div>
        <div>
          <label className="label">Role</label>
          <select id="audit-role-filter" className="input" value={filters.role} onChange={(e) => setFilters({ ...filters, role: e.target.value })}>
            <option value="">All roles</option>
            <option value="admin">Admin</option>
            <option value="vet">Vet</option>
            <option value="farmer">Farmer</option>
            <option value="system">System</option>
          </select>
        </div>
        <div>
          <label className="label">From date</label>
          <input id="audit-from" type="date" className="input" value={filters.from} onChange={(e) => setFilters({ ...filters, from: e.target.value })} />
        </div>
        <div>
          <label className="label">To date</label>
          <input id="audit-to" type="date" className="input" value={filters.to} onChange={(e) => setFilters({ ...filters, to: e.target.value })} />
        </div>
      </div>

      {/* Table */}
      <div className="card overflow-hidden">
        <div className="table-container">
          <table className="table">
            <thead>
              <tr><th>Time</th><th>Actor</th><th>Role</th><th>Action</th><th>Target</th></tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id}>
                  <td className="text-xs text-slate-400 whitespace-nowrap">
                    {new Date(log.timestamp).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })}
                  </td>
                  <td>
                    <p className="font-medium text-slate-800 text-sm">{log.actor.name}</p>
                    <p className="text-xs text-slate-400">{log.actor.email}</p>
                  </td>
                  <td>
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold uppercase bg-slate-100 text-slate-700">
                      {log.actorRole}
                    </span>
                  </td>
                  <td>
                    <code className="text-xs bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-mono">
                      {log.action}
                    </code>
                  </td>
                  <td className="text-xs text-slate-400 font-mono">{log.targetId?.slice(-8) ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {loading && <p className="p-8 text-center text-slate-400">Loading...</p>}
          {!loading && logs.length === 0 && <p className="p-8 text-center text-slate-400">No log entries found</p>}
        </div>

        {/* Pagination */}
        {total > 20 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-slate-100">
            <p className="text-xs text-slate-500">Showing {(page - 1) * 20 + 1}–{Math.min(page * 20, total)} of {total}</p>
            <div className="flex gap-2">
              <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary btn-sm">← Prev</button>
              <button onClick={() => setPage((p) => p + 1)} disabled={page * 20 >= total} className="btn-secondary btn-sm">Next →</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

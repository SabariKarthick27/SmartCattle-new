"use client";

import { useState, useEffect } from "react";
import { timeAgo } from "@/lib/utils";

interface User {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: string;
  farmId: string | null;
  assignedRegion: string | null;
  isVerified: boolean;
  isActive: boolean;
  createdAt: string;
}

export default function AdminUsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<{ role: string; verified: string }>({ role: "", verified: "" });
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [msg, setMsg] = useState("");

  const fetchUsers = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filter.role) params.set("role", filter.role);
    if (filter.verified) params.set("verified", filter.verified);
    const res = await fetch(`/api/admin/users?${params}`);
    const data = await res.json();
    setUsers(data.users ?? []);
    setLoading(false);
  };

  useEffect(() => { fetchUsers(); }, [filter]);

  const doAction = async (userId: string, action: string, region?: string) => {
    setActionLoading(userId);
    setMsg("");
    const res = await fetch("/api/admin/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId, action, assignedRegion: region }),
    });
    setActionLoading(null);
    if (res.ok) {
      setMsg(`User ${action}d successfully`);
      fetchUsers();
    } else {
      const d = await res.json();
      setMsg(d.error);
    }
  };

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">User Management</h1>
          <p className="text-slate-500 mt-1">Approve, manage, and configure user accounts</p>
        </div>
      </div>

      {msg && (
        <div className="p-3.5 rounded-xl text-sm bg-brand-50 text-brand-900 border border-brand-200">
          {msg}
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-3 flex-wrap">
        {[
          { label: "All Roles", value: "" },
          { label: "Farmers", value: "farmer" },
          { label: "Veterinarians", value: "vet" },
        ].map((f) => (
          <button
            key={f.value}
            id={`filter-role-${f.value || "all"}`}
            onClick={() => setFilter({ ...filter, role: f.value })}
            className={`btn-sm ${filter.role === f.value ? "btn-primary" : "btn-secondary"}`}
          >
            {f.label}
          </button>
        ))}
        <div className="h-8 w-px bg-slate-200" />
        {[
          { label: "All", value: "" },
          { label: "Pending", value: "false" },
          { label: "Verified", value: "true" },
        ].map((f) => (
          <button
            key={f.value}
            id={`filter-verified-${f.value || "all"}`}
            onClick={() => setFilter({ ...filter, verified: f.value })}
            className={`btn-sm ${filter.verified === f.value ? "btn-primary" : "btn-secondary"}`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="card overflow-hidden">
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Role</th>
                <th>Region / Farm</th>
                <th>Status</th>
                <th>Joined</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td className="font-medium text-slate-900">{u.name}</td>
                  <td className="text-slate-600 text-xs">{u.email}</td>
                  <td className="text-slate-500 text-xs">{u.phone}</td>
                  <td>
                    <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                      u.role === "admin" ? "bg-purple-100 text-purple-700" :
                      u.role === "vet" ? "bg-teal-100 text-teal-700" :
                      "bg-brand-100 text-brand-700"
                    }`}>
                      {u.role}
                    </span>
                  </td>
                  <td className="text-slate-500 text-xs">{u.assignedRegion ?? u.farmId ?? "—"}</td>
                  <td>
                    {!u.isActive ? (
                      <span className="text-xs font-medium text-red-600 bg-red-50 px-2 py-1 rounded-full">Deactivated</span>
                    ) : u.isVerified ? (
                      <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">Active</span>
                    ) : (
                      <span className="text-xs font-medium text-amber-600 bg-amber-50 px-2 py-1 rounded-full">Pending</span>
                    )}
                  </td>
                  <td className="text-xs text-slate-400">{timeAgo(u.createdAt)}</td>
                  <td>
                    <div className="flex items-center gap-1.5">
                      {!u.isVerified && u.isActive && (
                        <button id={`approve-${u.id}`} onClick={() => doAction(u.id, "approve")} disabled={actionLoading === u.id} className="btn-primary btn-sm">Approve</button>
                      )}
                      {!u.isVerified && u.isActive && (
                        <button id={`reject-${u.id}`} onClick={() => doAction(u.id, "reject")} disabled={actionLoading === u.id} className="btn-danger btn-sm">Reject</button>
                      )}
                      {u.isVerified && u.isActive && u.role !== "admin" && (
                        <button id={`deactivate-${u.id}`} onClick={() => doAction(u.id, "deactivate")} disabled={actionLoading === u.id} className="btn-secondary btn-sm text-red-600">Deactivate</button>
                      )}
                      {!u.isActive && (
                        <button id={`reactivate-${u.id}`} onClick={() => doAction(u.id, "reactivate")} disabled={actionLoading === u.id} className="btn-secondary btn-sm text-emerald-600">Reactivate</button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!loading && users.length === 0 && (
            <p className="p-8 text-center text-slate-400">No users found for the current filters</p>
          )}
          {loading && <p className="p-8 text-center text-slate-400">Loading...</p>}
        </div>
      </div>
    </div>
  );
}

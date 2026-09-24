"use client";

import { useState, useEffect, useMemo } from "react";
import { timeAgo } from "@/lib/utils";
import {
  IconUsers,
  IconCheck,
  IconAlert,
  IconClose,
  IconRefresh,
  IconPencil,
  IconTrash,
  IconPlus,
  IconMapPin,
  IconSearch,
  IconBuilding,
  IconShieldCheck,
  IconStethoscope,
  IconCow,
  IconClipboardList,
} from "@/components/icons";

interface UserItem {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: "farmer" | "vet" | "admin";
  farmId: string | null;
  assignedRegion: string | null;
  isVerified: boolean;
  isActive: boolean;
  createdAt: string;
  _count?: {
    cattle?: number;
    vetCases?: number;
    farmerCases?: number;
  };
}

interface VetOption {
  id: string;
  name: string;
  email: string;
  phone: string;
  assignedRegion: string | null;
}

const REGIONS = [
  "Coimbatore",
  "Erode",
  "Salem",
  "Madurai",
  "Tiruppur",
  "Namakkal",
  "Dindigul",
  "Thanjavur",
  "Trichy",
  "Vellore",
  "Dharmapuri",
  "Krishnagiri",
];

export default function AdminUsersPage() {
  const [users, setUsers] = useState<UserItem[]>([]);
  const [vets, setVets] = useState<VetOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [roleFilter, setRoleFilter] = useState<string>("");
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [regionFilter, setRegionFilter] = useState<string>("");
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<{ type: "success" | "error"; message: string } | null>(null);

  // Modals
  const [editingUser, setEditingUser] = useState<UserItem | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [deletingUser, setDeletingUser] = useState<UserItem | null>(null);

  // Edit Form State
  const [editForm, setEditForm] = useState({
    name: "",
    email: "",
    phone: "",
    role: "farmer" as "farmer" | "vet" | "admin",
    farmId: "",
    assignedRegion: "",
    isVerified: true,
    isActive: true,
    newPassword: "",
  });

  // Create Form State
  const [createForm, setCreateForm] = useState({
    name: "",
    email: "",
    phone: "",
    password: "",
    role: "farmer" as "farmer" | "vet" | "admin",
    farmId: "",
    assignedRegion: "Coimbatore",
    isVerified: true,
  });

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (roleFilter) params.set("role", roleFilter);
      if (statusFilter) params.set("verified", statusFilter);

      const res = await fetch(`/api/admin/users?${params.toString()}`);
      if (res.ok) {
        const data = await res.json();
        setUsers(data.users ?? []);
        setVets(data.vets ?? []);
      } else {
        setFeedback({ type: "error", message: "Failed to load user records." });
      }
    } catch {
      setFeedback({ type: "error", message: "Network error loading users." });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [roleFilter, statusFilter]);

  // Quick Action Handler (Approve / Reject / Deactivate / Reactivate)
  const handleQuickAction = async (userId: string, action: string) => {
    setActionLoading(userId);
    setFeedback(null);
    try {
      const res = await fetch("/api/admin/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, action }),
      });
      const data = await res.json();
      if (res.ok) {
        setFeedback({ type: "success", message: `Account status updated successfully.` });
        fetchUsers();
      } else {
        setFeedback({ type: "error", message: data.error || "Action failed." });
      }
    } catch {
      setFeedback({ type: "error", message: "An unexpected error occurred." });
    } finally {
      setActionLoading(null);
    }
  };

  // Open Edit Modal
  const handleOpenEdit = (u: UserItem) => {
    setEditingUser(u);
    setEditForm({
      name: u.name,
      email: u.email,
      phone: u.phone,
      role: u.role,
      farmId: u.farmId || "",
      assignedRegion: u.assignedRegion || "",
      isVerified: u.isVerified,
      isActive: u.isActive,
      newPassword: "",
    });
  };

  // Submit Edit Form
  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingUser) return;

    setActionLoading(editingUser.id);
    setFeedback(null);
    try {
      const res = await fetch("/api/admin/users", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId: editingUser.id,
          ...editForm,
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setFeedback({ type: "success", message: `Updated details for ${editForm.name}.` });
        setEditingUser(null);
        fetchUsers();
      } else {
        setFeedback({ type: "error", message: data.error || "Failed to update user." });
      }
    } catch {
      setFeedback({ type: "error", message: "Network error while saving user." });
    } finally {
      setActionLoading(null);
    }
  };

  // Submit Create Form
  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading("create");
    setFeedback(null);
    try {
      const res = await fetch("/api/admin/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "create",
          ...createForm,
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setFeedback({ type: "success", message: `Created new account for ${createForm.name}.` });
        setShowCreateModal(false);
        setCreateForm({
          name: "",
          email: "",
          phone: "",
          password: "",
          role: "farmer",
          farmId: "",
          assignedRegion: "Coimbatore",
          isVerified: true,
        });
        fetchUsers();
      } else {
        setFeedback({ type: "error", message: data.error || "Failed to create account." });
      }
    } catch {
      setFeedback({ type: "error", message: "Network error while creating account." });
    } finally {
      setActionLoading(null);
    }
  };

  // Submit Safe Deletion
  const handleDeleteUser = async () => {
    if (!deletingUser) return;
    setActionLoading(deletingUser.id);
    setFeedback(null);
    try {
      const res = await fetch(`/api/admin/users?userId=${encodeURIComponent(deletingUser.id)}`, {
        method: "DELETE",
      });
      const data = await res.json();
      if (res.ok) {
        setFeedback({ type: "success", message: data.message || "User account deleted." });
        setDeletingUser(null);
        fetchUsers();
      } else {
        setFeedback({ type: "error", message: data.error || "Could not delete user." });
      }
    } catch {
      setFeedback({ type: "error", message: "Network error while deleting user." });
    } finally {
      setActionLoading(null);
    }
  };

  // Filtered List
  const filteredUsers = useMemo(() => {
    return users.filter((u) => {
      const q = searchTerm.toLowerCase().trim();
      const matchesSearch =
        !q ||
        u.name.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q) ||
        u.phone.toLowerCase().includes(q) ||
        (u.farmId && u.farmId.toLowerCase().includes(q)) ||
        (u.assignedRegion && u.assignedRegion.toLowerCase().includes(q));

      const matchesRegion = !regionFilter || u.assignedRegion === regionFilter;

      return matchesSearch && matchesRegion;
    });
  }, [users, searchTerm, regionFilter]);

  // Metrics
  const stats = useMemo(() => {
    const total = users.length;
    const farmers = users.filter((u) => u.role === "farmer").length;
    const veterinarians = users.filter((u) => u.role === "vet").length;
    const pending = users.filter((u) => !u.isVerified && u.isActive).length;
    return { total, farmers, veterinarians, pending };
  }, [users]);

  return (
    <div className="p-6 md:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Top Banner & Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
              <IconUsers className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight font-display">
                User & Farm Management
              </h1>
              <p className="text-slate-500 text-xs sm:text-sm">
                Manage farmers, veterinarians, regional veterinary coverage, and farm assignments
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={fetchUsers}
            disabled={loading}
            className="btn btn-secondary btn-sm flex items-center gap-1.5"
            title="Refresh list"
          >
            <IconRefresh className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
          <button
            type="button"
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary btn-sm flex items-center gap-1.5 shadow-sm"
          >
            <IconPlus className="w-3.5 h-3.5" />
            <span>Add User / Staff</span>
          </button>
        </div>
      </div>

      {/* Feedback Alert */}
      {feedback && (
        <div
          className={`p-4 rounded-xl text-sm flex items-center justify-between border ${
            feedback.type === "success"
              ? "bg-emerald-50 text-emerald-900 border-emerald-200"
              : "bg-red-50 text-red-900 border-red-200"
          }`}
        >
          <div className="flex items-center gap-2">
            {feedback.type === "success" ? (
              <IconCheck className="w-4 h-4 text-emerald-600 shrink-0" />
            ) : (
              <IconAlert className="w-4 h-4 text-red-600 shrink-0" />
            )}
            <span className="font-medium">{feedback.message}</span>
          </div>
          <button
            type="button"
            onClick={() => setFeedback(null)}
            className="text-slate-400 hover:text-slate-700 p-1"
          >
            <IconClose className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card p-4 bg-white border border-slate-200">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Accounts</p>
          <p className="text-2xl font-black text-slate-900 mt-1">{stats.total}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">Across all registered roles</p>
        </div>
        <div className="card p-4 bg-white border border-slate-200">
          <p className="text-xs font-semibold text-emerald-700 uppercase tracking-wider">Dairy Farmers</p>
          <p className="text-2xl font-black text-emerald-950 mt-1">{stats.farmers}</p>
          <p className="text-[11px] text-emerald-600/80 mt-0.5">Managing active cattle herds</p>
        </div>
        <div className="card p-4 bg-white border border-slate-200">
          <p className="text-xs font-semibold text-teal-700 uppercase tracking-wider">Veterinarians</p>
          <p className="text-2xl font-black text-teal-950 mt-1">{stats.veterinarians}</p>
          <p className="text-[11px] text-teal-600/80 mt-0.5">Assigned to regional zones</p>
        </div>
        <div className="card p-4 bg-white border border-slate-200">
          <p className="text-xs font-semibold text-amber-700 uppercase tracking-wider">Pending Approvals</p>
          <p className="text-2xl font-black text-amber-950 mt-1">{stats.pending}</p>
          <p className="text-[11px] text-amber-600/80 mt-0.5">Awaiting admin review</p>
        </div>
      </div>

      {/* Search & Filter Controls */}
      <div className="card p-4 bg-white border border-slate-200 space-y-3">
        <div className="flex flex-col md:flex-row gap-3 items-center justify-between">
          {/* Live Search */}
          <div className="relative w-full md:w-80">
            <IconSearch className="w-4 h-4 text-slate-400 absolute left-3 top-2.5 pointer-events-none" />
            <input
              type="text"
              placeholder="Search by name, email, phone, farm ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input text-xs w-full pl-9 pr-8 py-2"
            />
            {searchTerm && (
              <button
                type="button"
                onClick={() => setSearchTerm("")}
                className="absolute right-2.5 top-2.5 text-slate-400 hover:text-slate-600 text-xs"
              >
                ✕
              </button>
            )}
          </div>

          {/* Quick Filters */}
          <div className="flex flex-wrap gap-2 w-full md:w-auto items-center">
            {/* Role Filter */}
            <div className="flex gap-1 bg-slate-100 p-0.5 rounded-lg border border-slate-200">
              {[
                { label: "All Roles", value: "" },
                { label: "Farmers", value: "farmer" },
                { label: "Veterinarians", value: "vet" },
                { label: "Admins", value: "admin" },
              ].map((rf) => (
                <button
                  key={rf.value}
                  type="button"
                  onClick={() => setRoleFilter(rf.value)}
                  className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-all ${
                    roleFilter === rf.value
                      ? "bg-white text-slate-900 shadow-xs border border-slate-200"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {rf.label}
                </button>
              ))}
            </div>

            {/* Status Filter */}
            <div className="flex gap-1 bg-slate-100 p-0.5 rounded-lg border border-slate-200">
              {[
                { label: "All Statuses", value: "" },
                { label: "Pending", value: "false" },
                { label: "Verified", value: "true" },
              ].map((sf) => (
                <button
                  key={sf.value}
                  type="button"
                  onClick={() => setStatusFilter(sf.value)}
                  className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-all ${
                    statusFilter === sf.value
                      ? "bg-white text-slate-900 shadow-xs border border-slate-200"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {sf.label}
                </button>
              ))}
            </div>

            {/* Region Select Filter */}
            <select
              value={regionFilter}
              onChange={(e) => setRegionFilter(e.target.value)}
              className="input text-xs py-1 px-2.5 bg-white"
            >
              <option value="">All Regions</option>
              {REGIONS.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="card overflow-hidden bg-white border border-slate-200 shadow-sm">
        <div className="table-container">
          <table className="table w-full">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                <th className="py-3 px-4">User / Operator</th>
                <th className="py-3 px-4">Role</th>
                <th className="py-3 px-4">Farm & Region Assignment</th>
                <th className="py-3 px-4">Herd / Case Activity</th>
                <th className="py-3 px-4">Account Status</th>
                <th className="py-3 px-4">Joined</th>
                <th className="py-3 px-4 text-right">Actions & Assignments</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredUsers.map((u) => (
                <tr key={u.id} className="hover:bg-slate-50/75 transition-colors">
                  {/* Name & Contact */}
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-full bg-slate-100 border border-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center shrink-0">
                        {u.name?.[0]?.toUpperCase() ?? "U"}
                      </div>
                      <div className="min-w-0">
                        <p className="font-bold text-slate-900 text-sm truncate">{u.name}</p>
                        <p className="text-slate-500 text-xs font-mono truncate">{u.email}</p>
                        {u.phone && <p className="text-slate-400 text-[11px] tnum">{u.phone}</p>}
                      </div>
                    </div>
                  </td>

                  {/* Role */}
                  <td className="py-3 px-4">
                    <span
                      className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full ${
                        u.role === "admin"
                          ? "bg-purple-50 text-purple-900 border border-purple-200"
                          : u.role === "vet"
                          ? "bg-teal-50 text-teal-900 border border-teal-200"
                          : "bg-emerald-50 text-emerald-900 border border-emerald-200"
                      }`}
                    >
                      {u.role === "vet" ? (
                        <>
                          <IconStethoscope className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                          <span>Veterinarian</span>
                        </>
                      ) : u.role === "farmer" ? (
                        <>
                          <IconCow className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                          <span>Dairy Farmer</span>
                        </>
                      ) : (
                        <>
                          <IconShieldCheck className="w-3.5 h-3.5 text-purple-600 shrink-0" />
                          <span>Admin</span>
                        </>
                      )}
                    </span>
                  </td>

                  {/* Farm & Region Assignment */}
                  <td className="py-3 px-4">
                    <div className="space-y-1">
                      {u.farmId ? (
                        <div className="flex items-center gap-1.5 text-slate-800">
                          <IconBuilding className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                          <span className="text-xs font-semibold">{u.farmId}</span>
                        </div>
                      ) : (
                        <span className="text-xs text-slate-400 italic">No farm registered</span>
                      )}
                      {u.assignedRegion && (
                        <div className="inline-flex items-center gap-1 text-[11px] font-mono font-medium px-2 py-0.5 bg-slate-100 text-slate-700 rounded border border-slate-200">
                          <IconMapPin className="w-3 h-3 text-slate-500 shrink-0" />
                          <span>{u.assignedRegion}</span>
                        </div>
                      )}
                    </div>
                  </td>

                  {/* Stats */}
                  <td className="py-3 px-4 text-xs">
                    {u.role === "farmer" ? (
                      <div className="inline-flex items-center gap-1.5 font-bold text-slate-700">
                        <IconCow className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                        <span>{u._count?.cattle ?? 0} Cattle logged</span>
                      </div>
                    ) : u.role === "vet" ? (
                      <div className="inline-flex items-center gap-1.5 font-bold text-teal-800">
                        <IconClipboardList className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                        <span>{u._count?.vetCases ?? 0} Cases handled</span>
                      </div>
                    ) : (
                      <span className="text-slate-400 text-xs">Full system scope</span>
                    )}
                  </td>

                  {/* Status */}
                  <td className="py-3 px-4">
                    {!u.isActive ? (
                      <span className="text-xs font-semibold text-red-800 bg-red-50 border border-red-200 px-2.5 py-1 rounded-md inline-flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-600"></span> Deactivated
                      </span>
                    ) : u.isVerified ? (
                      <span className="text-xs font-semibold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-md inline-flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span> Verified & Active
                      </span>
                    ) : (
                      <span className="text-xs font-semibold text-amber-800 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded-md inline-flex items-center gap-1.5 animate-pulse">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span> Pending Approval
                      </span>
                    )}
                  </td>

                  {/* Joined */}
                  <td className="py-3 px-4 text-xs text-slate-400">{timeAgo(u.createdAt)}</td>

                  {/* Actions */}
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      {/* Quick Approve / Reject for pending */}
                      {!u.isVerified && u.isActive && (
                        <>
                          <button
                            type="button"
                            onClick={() => handleQuickAction(u.id, "approve")}
                            disabled={actionLoading === u.id}
                            className="btn btn-primary btn-sm text-xs py-1 px-2.5"
                            title="Approve User Registration"
                          >
                            Approve
                          </button>
                          <button
                            type="button"
                            onClick={() => handleQuickAction(u.id, "reject")}
                            disabled={actionLoading === u.id}
                            className="btn btn-danger btn-sm text-xs py-1 px-2.5"
                            title="Reject and Deactivate"
                          >
                            Reject
                          </button>
                        </>
                      )}

                      {/* Edit Button */}
                      <button
                        type="button"
                        onClick={() => handleOpenEdit(u)}
                        className="btn btn-secondary btn-sm text-xs py-1 px-2.5 text-slate-700 hover:text-slate-900 border-slate-300 flex items-center gap-1.5"
                        title="Edit User, Role, Farm & Region"
                      >
                        <IconPencil className="w-3.5 h-3.5 text-slate-600" />
                        <span>Edit & Assign</span>
                      </button>

                      {/* Deactivate / Reactivate */}
                      {u.isVerified && u.isActive && u.role !== "admin" && (
                        <button
                          type="button"
                          onClick={() => handleQuickAction(u.id, "deactivate")}
                          disabled={actionLoading === u.id}
                          className="btn btn-secondary btn-sm text-xs py-1 px-2 text-red-600 hover:text-red-700 border-red-200 hover:bg-red-50"
                          title="Suspend Account"
                        >
                          Suspend
                        </button>
                      )}
                      {!u.isActive && (
                        <button
                          type="button"
                          onClick={() => handleQuickAction(u.id, "reactivate")}
                          disabled={actionLoading === u.id}
                          className="btn btn-secondary btn-sm text-xs py-1 px-2 text-emerald-700 hover:text-emerald-800 border-emerald-200 hover:bg-emerald-50"
                          title="Reactivate Account"
                        >
                          Reactivate
                        </button>
                      )}

                      {/* Safe Delete */}
                      <button
                        type="button"
                        onClick={() => setDeletingUser(u)}
                        className="btn btn-secondary btn-sm text-xs py-1 px-2 text-slate-400 hover:text-red-600 hover:bg-red-50 border-slate-200"
                        title="Delete User"
                      >
                        <IconTrash className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {!loading && filteredUsers.length === 0 && (
            <div className="p-12 text-center text-slate-500 space-y-2">
              <p className="text-base font-semibold">No accounts found</p>
              <p className="text-xs text-slate-400">Try adjusting your search terms or filter criteria.</p>
            </div>
          )}

          {loading && (
            <div className="p-12 text-center text-slate-400 flex items-center justify-center gap-2">
              <IconRefresh className="w-4 h-4 animate-spin text-emerald-600" />
              <span>Loading user records and assignments...</span>
            </div>
          )}
        </div>
      </div>

      {/* ── EDIT & ASSIGN MODAL ── */}
      {editingUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-slate-200">
            <div className="p-5 border-b border-slate-200 flex items-center justify-between sticky top-0 bg-white z-10">
              <div>
                <h3 className="text-lg font-bold text-slate-900 font-display">Edit User & Farm Assignment</h3>
                <p className="text-xs text-slate-500">Updating profile, roles, and regional coverage</p>
              </div>
              <button
                type="button"
                onClick={() => setEditingUser(null)}
                className="text-slate-400 hover:text-slate-700 p-1.5 rounded-lg"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveEdit} className="p-6 space-y-4">
              {/* Name & Email */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs font-bold text-slate-700">Full Name *</label>
                  <input
                    type="text"
                    required
                    value={editForm.name}
                    onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                    className="input text-xs w-full mt-1"
                  />
                </div>
                <div>
                  <label className="label text-xs font-bold text-slate-700">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={editForm.email}
                    onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                    className="input text-xs w-full mt-1"
                  />
                </div>
              </div>

              {/* Phone & Role */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs font-bold text-slate-700">Phone Number</label>
                  <input
                    type="text"
                    value={editForm.phone}
                    onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                    className="input text-xs w-full mt-1"
                    placeholder="+91 98765 43210"
                  />
                </div>
                <div>
                  <label className="label text-xs font-bold text-slate-700">Account Role *</label>
                  <select
                    value={editForm.role}
                    onChange={(e) =>
                      setEditForm({ ...editForm, role: e.target.value as "farmer" | "vet" | "admin" })
                    }
                    className="input text-xs w-full mt-1 bg-white font-medium"
                  >
                    <option value="farmer">Dairy Farmer</option>
                    <option value="vet">Field Veterinarian</option>
                    <option value="admin">System Administrator</option>
                  </select>
                </div>
              </div>

              {/* Farm Name & Region Assignment */}
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
                <p className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Farm & Regional Veterinary Coverage
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="label text-xs font-semibold text-slate-700">Farm Identifier / Name</label>
                    <input
                      type="text"
                      value={editForm.farmId}
                      onChange={(e) => setEditForm({ ...editForm, farmId: e.target.value })}
                      placeholder="e.g. Lakshmi Dairy Farm"
                      className="input text-xs w-full mt-1 bg-white"
                    />
                  </div>
                  <div>
                    <label className="label text-xs font-semibold text-slate-700">Assigned Region / Zone</label>
                    <select
                      value={editForm.assignedRegion}
                      onChange={(e) => setEditForm({ ...editForm, assignedRegion: e.target.value })}
                      className="input text-xs w-full mt-1 bg-white font-medium"
                    >
                      <option value="">Select or unassigned</option>
                      {REGIONS.map((r) => (
                        <option key={r} value={r}>
                          {r}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {editForm.role === "farmer" && (
                  <div className="pt-2">
                    <label className="label text-xs font-semibold text-slate-700">
                      Primary Veterinarian for this Region:
                    </label>
                    <div className="text-xs text-slate-600 mt-1">
                      {vets.filter((v) => v.assignedRegion === editForm.assignedRegion).length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                          {vets
                            .filter((v) => v.assignedRegion === editForm.assignedRegion)
                            .map((v) => (
                              <span
                                key={v.id}
                                className="inline-flex items-center gap-1 px-2.5 py-1 bg-teal-50 text-teal-800 border border-teal-200 rounded text-xs font-medium"
                              >
                                <IconStethoscope className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                                Dr. {v.name} ({v.phone || v.email})
                              </span>
                            ))}
                        </div>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2.5 py-1 rounded border border-amber-200 text-xs">
                          <IconAlert className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                          No vet assigned to {editForm.assignedRegion || "this region"} yet.
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Status & Verification Toggles */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-slate-800">Verification Status</p>
                    <p className="text-[11px] text-slate-500">Allow login & operations</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setEditForm({ ...editForm, isVerified: !editForm.isVerified })}
                    className={`btn btn-sm text-xs py-1 px-3 ${
                      editForm.isVerified ? "btn-primary" : "btn-secondary text-amber-700 border-amber-300"
                    }`}
                  >
                    {editForm.isVerified ? "Verified" : "Pending"}
                  </button>
                </div>

                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-slate-800">Account Access</p>
                    <p className="text-[11px] text-slate-500">Enable or suspend account</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setEditForm({ ...editForm, isActive: !editForm.isActive })}
                    className={`btn btn-sm text-xs py-1 px-3 ${
                      editForm.isActive ? "btn-primary" : "btn-danger"
                    }`}
                  >
                    {editForm.isActive ? "Active" : "Suspended"}
                  </button>
                </div>
              </div>

              {/* Reset Password */}
              <div>
                <label className="label text-xs font-semibold text-slate-700">
                  Reset Password (leave blank to keep unchanged)
                </label>
                <input
                  type="password"
                  value={editForm.newPassword}
                  onChange={(e) => setEditForm({ ...editForm, newPassword: e.target.value })}
                  placeholder="Enter new password (min. 6 chars)"
                  className="input text-xs w-full mt-1"
                />
              </div>

              {/* Submit Buttons */}
              <div className="pt-4 border-t border-slate-200 flex items-center justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setEditingUser(null)}
                  className="btn btn-secondary btn-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={actionLoading === editingUser.id}
                  className="btn btn-primary btn-sm flex items-center gap-1.5"
                >
                  {actionLoading === editingUser.id ? (
                    <>
                      <IconRefresh className="w-3.5 h-3.5 animate-spin" />
                      <span>Saving...</span>
                    </>
                  ) : (
                    <span>Save Changes</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ── CREATE NEW USER MODAL ── */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-slate-200">
            <div className="p-5 border-b border-slate-200 flex items-center justify-between sticky top-0 bg-white z-10">
              <div>
                <h3 className="text-lg font-bold text-slate-900 font-display">Create User or Staff Account</h3>
                <p className="text-xs text-slate-500">Register a new farmer, veterinarian, or administrator</p>
              </div>
              <button
                type="button"
                onClick={() => setShowCreateModal(false)}
                className="text-slate-400 hover:text-slate-700 p-1.5 rounded-lg"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateUser} className="p-6 space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs font-bold text-slate-700">Full Name *</label>
                  <input
                    type="text"
                    required
                    value={createForm.name}
                    onChange={(e) => setCreateForm({ ...createForm, name: e.target.value })}
                    className="input text-xs w-full mt-1"
                    placeholder="e.g. Ramesh Kumar"
                  />
                </div>
                <div>
                  <label className="label text-xs font-bold text-slate-700">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={createForm.email}
                    onChange={(e) => setCreateForm({ ...createForm, email: e.target.value })}
                    className="input text-xs w-full mt-1"
                    placeholder="user@smartcattle.org"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs font-bold text-slate-700">Phone Number *</label>
                  <input
                    type="text"
                    required
                    value={createForm.phone}
                    onChange={(e) => setCreateForm({ ...createForm, phone: e.target.value })}
                    className="input text-xs w-full mt-1"
                    placeholder="+91 98765 43210"
                  />
                </div>
                <div>
                  <label className="label text-xs font-bold text-slate-700">Initial Password *</label>
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={createForm.password}
                    onChange={(e) => setCreateForm({ ...createForm, password: e.target.value })}
                    className="input text-xs w-full mt-1"
                    placeholder="Min 6 characters"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs font-bold text-slate-700">Account Role *</label>
                  <select
                    value={createForm.role}
                    onChange={(e) =>
                      setCreateForm({ ...createForm, role: e.target.value as "farmer" | "vet" | "admin" })
                    }
                    className="input text-xs w-full mt-1 bg-white font-medium"
                  >
                    <option value="farmer">Dairy Farmer</option>
                    <option value="vet">Field Veterinarian</option>
                    <option value="admin">System Administrator</option>
                  </select>
                </div>
                <div>
                  <label className="label text-xs font-bold text-slate-700">Assigned Region / Hub *</label>
                  <select
                    value={createForm.assignedRegion}
                    onChange={(e) => setCreateForm({ ...createForm, assignedRegion: e.target.value })}
                    className="input text-xs w-full mt-1 bg-white font-medium"
                  >
                    {REGIONS.map((r) => (
                      <option key={r} value={r}>
                        {r}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {createForm.role === "farmer" && (
                <div>
                  <label className="label text-xs font-bold text-slate-700">Farm Name / Identifier</label>
                  <input
                    type="text"
                    value={createForm.farmId}
                    onChange={(e) => setCreateForm({ ...createForm, farmId: e.target.value })}
                    placeholder="e.g. Murugan Dairy Farm"
                    className="input text-xs w-full mt-1"
                  />
                </div>
              )}

              <div className="pt-4 border-t border-slate-200 flex items-center justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn btn-secondary btn-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={actionLoading === "create"}
                  className="btn btn-primary btn-sm flex items-center gap-1.5"
                >
                  {actionLoading === "create" ? (
                    <>
                      <IconRefresh className="w-3.5 h-3.5 animate-spin" />
                      <span>Creating...</span>
                    </>
                  ) : (
                    <span>Create Account</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ── DELETE CONFIRMATION MODAL ── */}
      {deletingUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-red-200 space-y-4">
            <div className="flex items-center gap-3 text-red-600">
              <div className="w-10 h-10 rounded-full bg-red-50 border border-red-200 flex items-center justify-center shrink-0">
                <IconAlert className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">Delete User Account?</h3>
                <p className="text-xs text-slate-500">This action cannot be undone</p>
              </div>
            </div>

            <div className="p-3 bg-red-50/50 rounded-xl border border-red-100 text-xs text-slate-700 space-y-1">
              <p>
                <span className="font-bold">Name:</span> {deletingUser.name}
              </p>
              <p>
                <span className="font-bold">Email:</span> {deletingUser.email}
              </p>
              <p>
                <span className="font-bold">Role:</span> {deletingUser.role.toUpperCase()}
              </p>
              {deletingUser.role === "farmer" && (
                <p className="text-red-700 mt-2 font-medium">
                  Deleting this farmer will also safely remove their registered cattle and health logs.
                </p>
              )}
            </div>

            <div className="flex items-center justify-end gap-2.5 pt-2">
              <button
                type="button"
                onClick={() => setDeletingUser(null)}
                className="btn btn-secondary btn-sm"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDeleteUser}
                disabled={actionLoading === deletingUser.id}
                className="btn btn-danger btn-sm flex items-center gap-1.5"
              >
                {actionLoading === deletingUser.id ? (
                  <>
                    <IconRefresh className="w-3.5 h-3.5 animate-spin" />
                    <span>Deleting...</span>
                  </>
                ) : (
                  <span>Yes, Delete Account</span>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

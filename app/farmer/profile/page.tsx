"use client";

import { useState, useEffect } from "react";
import { TAMIL_NADU_DISTRICTS } from "@/lib/constants";
import { fmtDate } from "@/lib/utils";

interface UserProfile {
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
  _count?: {
    cattle: number;
  };
}

export default function FarmerProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  
  // Profile details form state
  const [detailsForm, setDetailsForm] = useState({
    name: "",
    phone: "",
    farmId: "",
    assignedRegion: "",
  });
  const [detailsSaving, setDetailsSaving] = useState(false);
  const [detailsMsg, setDetailsMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Password reset form state
  const [passForm, setPassForm] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [showPass, setShowPass] = useState({
    current: false,
    new: false,
    confirm: false,
  });
  const [passSaving, setPassSaving] = useState(false);
  const [passMsg, setPassMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Load profile data
  const fetchProfile = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/farmer/profile");
      const data = await res.json();
      if (res.ok && data.user) {
        setProfile(data.user);
        setDetailsForm({
          name: data.user.name ?? "",
          phone: data.user.phone ?? "",
          farmId: data.user.farmId ?? "",
          assignedRegion: data.user.assignedRegion ?? "Tamil Nadu - Coimbatore",
        });
      }
    } catch (err) {
      console.error("Failed to load profile:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  // Save profile details
  const handleSaveDetails = async (e: React.FormEvent) => {
    e.preventDefault();
    setDetailsSaving(true);
    setDetailsMsg(null);

    try {
      const res = await fetch("/api/farmer/profile", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(detailsForm),
      });

      const data = await res.json();
      setDetailsSaving(false);

      if (!res.ok) {
        setDetailsMsg({ type: "error", text: data.error ?? "Failed to update profile." });
        return;
      }

      setProfile(data.user);
      setDetailsMsg({ type: "success", text: "Profile details updated successfully!" });
    } catch (err) {
      setDetailsSaving(false);
      setDetailsMsg({ type: "error", text: "An error occurred while saving profile." });
    }
  };

  // Reset password
  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPassMsg(null);

    if (passForm.newPassword !== passForm.confirmPassword) {
      setPassMsg({ type: "error", text: "New passwords do not match." });
      return;
    }

    if (passForm.newPassword.length < 8) {
      setPassMsg({ type: "error", text: "New password must be at least 8 characters." });
      return;
    }

    setPassSaving(true);

    try {
      const res = await fetch("/api/farmer/profile", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          currentPassword: passForm.currentPassword,
          newPassword: passForm.newPassword,
        }),
      });

      const data = await res.json();
      setPassSaving(false);

      if (!res.ok) {
        setPassMsg({ type: "error", text: data.error ?? "Password reset failed." });
        return;
      }

      setPassMsg({ type: "success", text: "Password changed successfully! Keep your new password secure." });
      setPassForm({ currentPassword: "", newPassword: "", confirmPassword: "" });
    } catch (err) {
      setPassSaving(false);
      setPassMsg({ type: "error", text: "An error occurred while updating password." });
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 max-w-4xl mx-auto">
        <div className="w-8 h-8 border-4 border-slate-300 border-t-brand-700 rounded-full animate-spin mx-auto mb-3" />
        Loading your farmer profile...
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2 font-sans">
          Farmer Profile & Account Settings
        </h1>
        <p className="text-slate-500 mt-1">
          Manage your personal details, farm information, and security settings
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (Forms) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Card 1: Personal & Farm Details */}
          <div className="card p-6 md:p-8">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-5">
              <h2 className="text-lg font-bold text-slate-900">Personal & Farm Information</h2>
              <span className="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full font-medium">
                Farmer Details
              </span>
            </div>

            {detailsMsg && (
              <div
                className={`mb-5 p-3.5 rounded-xl text-sm border ${
                  detailsMsg.type === "success"
                    ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                    : "bg-red-50 text-red-800 border-red-200"
                }`}
              >
                {detailsMsg.text}
              </div>
            )}

            <form onSubmit={handleSaveDetails} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="prof-name" className="label">Full Name *</label>
                  <input
                    id="prof-name"
                    type="text"
                    className="input"
                    value={detailsForm.name}
                    onChange={(e) => setDetailsForm({ ...detailsForm, name: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label htmlFor="prof-phone" className="label">Phone Number *</label>
                  <input
                    id="prof-phone"
                    type="tel"
                    className="input"
                    value={detailsForm.phone}
                    onChange={(e) => setDetailsForm({ ...detailsForm, phone: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div>
                <label htmlFor="prof-email" className="label">Email Address (Read-only)</label>
                <input
                  id="prof-email"
                  type="email"
                  className="input bg-slate-50 text-slate-500 cursor-not-allowed"
                  value={profile?.email ?? ""}
                  disabled
                />
                <p className="text-[11px] text-slate-400 mt-1">
                  Email is bound to your account credentials and cannot be modified.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="prof-region" className="label">Farm District / Region *</label>
                  <select
                    id="prof-region"
                    className="input"
                    value={detailsForm.assignedRegion}
                    onChange={(e) => setDetailsForm({ ...detailsForm, assignedRegion: e.target.value })}
                    required
                  >
                    <option value="">Select District</option>
                    {TAMIL_NADU_DISTRICTS.map((d) => (
                      <option key={d} value={d}>
                        {d}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label htmlFor="prof-farmid" className="label">Farm ID / Name</label>
                  <input
                    id="prof-farmid"
                    type="text"
                    className="input"
                    placeholder="e.g. FARM-001 or Kovai Dairy Farm"
                    value={detailsForm.farmId}
                    onChange={(e) => setDetailsForm({ ...detailsForm, farmId: e.target.value })}
                  />
                </div>
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  className="btn-primary"
                  disabled={detailsSaving}
                >
                  {detailsSaving ? (
                    <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> Saving...</>
                  ) : "Save Changes"}
                </button>
              </div>
            </form>
          </div>

          {/* Card 2: Security & Password Reset */}
          <div className="card p-6 md:p-8">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-5">
              <h2 className="text-lg font-bold text-slate-900">Security & Password Reset</h2>
              <span className="text-xs bg-amber-100 text-amber-800 px-2.5 py-1 rounded-full font-medium">
                Password Settings
              </span>
            </div>

            {passMsg && (
              <div
                className={`mb-5 p-3.5 rounded-xl text-sm border ${
                  passMsg.type === "success"
                    ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                    : "bg-red-50 text-red-800 border-red-200"
                }`}
              >
                {passMsg.text}
              </div>
            )}

            <form onSubmit={handleResetPassword} className="space-y-4">
              <div>
                <label htmlFor="pass-current" className="label">Current Password *</label>
                <div className="relative">
                  <input
                    id="pass-current"
                    type={showPass.current ? "text" : "password"}
                    className="input pr-11"
                    placeholder="Enter current password"
                    value={passForm.currentPassword}
                    onChange={(e) => setPassForm({ ...passForm, currentPassword: e.target.value })}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPass({ ...showPass, current: !showPass.current })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                    aria-label="Toggle password visibility"
                  >
                    {showPass.current ? (
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="pass-new" className="label">New Password *</label>
                  <div className="relative">
                    <input
                      id="pass-new"
                      type={showPass.new ? "text" : "password"}
                      className="input pr-11"
                      placeholder="At least 8 characters"
                      value={passForm.newPassword}
                      onChange={(e) => setPassForm({ ...passForm, newPassword: e.target.value })}
                      minLength={8}
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPass({ ...showPass, new: !showPass.new })}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                      aria-label="Toggle password visibility"
                    >
                      {showPass.new ? (
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                        </svg>
                      ) : (
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                          <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                      )}
                    </button>
                  </div>
                </div>

                <div>
                  <label htmlFor="pass-confirm" className="label">Confirm New Password *</label>
                  <div className="relative">
                    <input
                      id="pass-confirm"
                      type={showPass.confirm ? "text" : "password"}
                      className="input pr-11"
                      placeholder="Re-enter new password"
                      value={passForm.confirmPassword}
                      onChange={(e) => setPassForm({ ...passForm, confirmPassword: e.target.value })}
                      minLength={8}
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPass({ ...showPass, confirm: !showPass.confirm })}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                      aria-label="Toggle password visibility"
                    >
                      {showPass.confirm ? (
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                        </svg>
                      ) : (
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                          <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                      )}
                    </button>
                  </div>
                </div>
              </div>

              {passForm.newPassword && (
                <div className="text-xs space-y-1 pt-1">
                  <p className={passForm.newPassword.length >= 8 ? "text-emerald-600" : "text-slate-400"}>
                    {passForm.newPassword.length >= 8 ? "✓" : "•"} Minimum 8 characters
                  </p>
                  <p className={passForm.confirmPassword && passForm.newPassword === passForm.confirmPassword ? "text-emerald-600" : "text-amber-600"}>
                    {passForm.confirmPassword && passForm.newPassword === passForm.confirmPassword
                      ? "✓ Passwords match"
                      : "• Passwords must match"}
                  </p>
                </div>
              )}

              <div className="pt-2">
                <button
                  type="submit"
                  className="btn-secondary text-brand-800 border-brand-200 hover:bg-brand-50"
                  disabled={passSaving}
                >
                  {passSaving ? (
                    <><span className="w-4 h-4 border-2 border-brand-700/30 border-t-brand-700 rounded-full animate-spin" /> Updating...</>
                  ) : "Update Password →"}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Right Column (Sidebar Summary Card) */}
        <div className="space-y-6">
          <div className="card p-6 text-center">
            <div className="w-20 h-20 bg-brand-100 text-brand-800 rounded-full flex items-center justify-center font-bold text-3xl mx-auto mb-4 border-4 border-brand-50 shadow-sm">
              {profile?.name?.[0]?.toUpperCase() ?? "F"}
            </div>

            <h3 className="font-bold text-slate-900 text-lg">{profile?.name}</h3>
            <p className="text-xs text-slate-500 mb-3">{profile?.email}</p>

            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold mb-6">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              Verified Farmer Account
            </div>

            <div className="space-y-3 text-left border-t border-slate-100 pt-4 text-xs">
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Registered Animals</span>
                <span className="font-bold text-slate-900">{profile?._count?.cattle ?? 0} Head</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">District / Region</span>
                <span className="font-medium text-slate-800">{profile?.assignedRegion ?? "Tamil Nadu"}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Farm Identifier</span>
                <span className="font-mono text-slate-800">{profile?.farmId ?? "Not assigned"}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Account Joined</span>
                <span className="text-slate-700">{fmtDate(profile?.createdAt)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

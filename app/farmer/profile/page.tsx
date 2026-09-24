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
  photoUrl: string | null;
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
    photoUrl: "",
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
          photoUrl: data.user.photoUrl ?? "",
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

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 4 * 1024 * 1024) {
      setDetailsMsg({ type: "error", text: "Photo file size must be less than 4 MB." });
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setDetailsForm((prev) => ({ ...prev, photoUrl: reader.result as string }));
    };
    reader.readAsDataURL(file);
  };

  const handleRemovePhoto = () => {
    setDetailsForm((prev) => ({ ...prev, photoUrl: "" }));
  };

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
      setDetailsMsg({ type: "success", text: "Profile details & photo updated successfully!" });
    } catch {
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
        setPassMsg({ type: "error", text: data.error ?? "Password update failed." });
        return;
      }

      setPassMsg({ type: "success", text: "Password changed successfully!" });
      setPassForm({ currentPassword: "", newPassword: "", confirmPassword: "" });
    } catch {
      setPassSaving(false);
      setPassMsg({ type: "error", text: "An error occurred while updating password." });
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 max-w-4xl mx-auto">
        <div className="w-8 h-8 border-2 border-slate-300 border-t-[#123326] rounded-full animate-spin mx-auto mb-3" />
        <p className="text-xs font-mono">Loading profile details...</p>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="pb-4 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
            Farm Profile &amp; Settings
          </h1>
          <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
            SETTINGS
          </span>
        </div>
        <p className="text-xs text-slate-500 mt-0.5">
          Manage your contact information, farm district, and account password.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (Forms) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Card 1: Personal & Farm Details */}
          <div className="card p-5 sm:p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h2 className="text-base font-bold text-slate-900 font-display">Personal &amp; Farm Details</h2>
              <span className="text-[10px] font-mono bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-bold">
                PROFILE
              </span>
            </div>

            {detailsMsg && (
              <div
                className={`p-3 rounded-lg text-xs font-medium border ${
                  detailsMsg.type === "success"
                    ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                    : "bg-red-50 text-red-800 border-red-200"
                }`}
              >
                {detailsMsg.text}
              </div>
            )}

            <form onSubmit={handleSaveDetails} className="space-y-4">
              {/* Photo Upload Section */}
              <div className="flex flex-col sm:flex-row items-center gap-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
                <div className="w-16 h-16 rounded-full overflow-hidden bg-[#123326] text-emerald-300 flex items-center justify-center font-bold text-xl border-2 border-emerald-600 shrink-0 shadow-xs">
                  {detailsForm.photoUrl ? (
                    <img
                      src={detailsForm.photoUrl}
                      alt="Farmer Profile"
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span>{detailsForm.name?.[0]?.toUpperCase() || "F"}</span>
                  )}
                </div>

                <div className="space-y-1 text-center sm:text-left flex-1">
                  <p className="text-xs font-bold text-slate-800">Profile Photo</p>
                  <p className="text-[11px] text-slate-500">
                    Upload a square PNG, JPG, or WebP (max 4 MB). Visible on your profile &amp; sidebar.
                  </p>
                  <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2 pt-1.5">
                    <label className="btn btn-secondary btn-sm text-xs cursor-pointer inline-flex items-center gap-1.5">
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                      </svg>
                      <span>Upload Photo</span>
                      <input
                        type="file"
                        accept="image/*"
                        className="hidden"
                        onChange={handlePhotoUpload}
                      />
                    </label>
                    {detailsForm.photoUrl && (
                      <button
                        type="button"
                        onClick={handleRemovePhoto}
                        className="text-xs text-rose-600 hover:text-rose-700 hover:underline font-medium px-2 py-1"
                      >
                        Remove
                      </button>
                    )}
                  </div>
                </div>
              </div>

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
                  <label htmlFor="prof-phone" className="label">Mobile Phone *</label>
                  <input
                    id="prof-phone"
                    type="tel"
                    className="input font-mono"
                    value={detailsForm.phone}
                    onChange={(e) => setDetailsForm({ ...detailsForm, phone: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div>
                <label htmlFor="prof-email" className="label">Email Address (Login ID)</label>
                <input
                  id="prof-email"
                  type="email"
                  className="input bg-slate-50 text-slate-600 cursor-not-allowed font-mono"
                  value={profile?.email ?? ""}
                  disabled
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="prof-region" className="label">District / Location *</label>
                  <select
                    id="prof-region"
                    className="input"
                    value={detailsForm.assignedRegion}
                    onChange={(e) => setDetailsForm({ ...detailsForm, assignedRegion: e.target.value })}
                    required
                  >
                    <option value="">Select District</option>
                    {TAMIL_NADU_DISTRICTS.map((d) => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label htmlFor="prof-farmid" className="label">Farm Name or ID</label>
                  <input
                    id="prof-farmid"
                    type="text"
                    className="input"
                    placeholder="e.g. Kovai Dairy Farm"
                    value={detailsForm.farmId}
                    onChange={(e) => setDetailsForm({ ...detailsForm, farmId: e.target.value })}
                  />
                </div>
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  className="btn btn-primary btn-sm font-semibold text-xs px-4"
                  disabled={detailsSaving}
                >
                  {detailsSaving ? "Saving..." : "Save Profile Details"}
                </button>
              </div>
            </form>
          </div>

          {/* Card 2: Security & Password Reset */}
          <div className="card p-5 sm:p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h2 className="text-base font-bold text-slate-900 font-display">Change Password</h2>
              <span className="text-[10px] font-mono bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-bold">
                SECURITY
              </span>
            </div>

            {passMsg && (
              <div
                className={`p-3 rounded-lg text-xs font-medium border ${
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
                    className="input pr-10 font-mono"
                    placeholder="Enter your current password"
                    value={passForm.currentPassword}
                    onChange={(e) => setPassForm({ ...passForm, currentPassword: e.target.value })}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPass({ ...showPass, current: !showPass.current })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 text-xs"
                  >
                    {showPass.current ? "✕" : "👁"}
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="pass-new" className="label">New Password (Min 8 chars) *</label>
                  <div className="relative">
                    <input
                      id="pass-new"
                      type={showPass.new ? "text" : "password"}
                      className="input pr-10 font-mono"
                      placeholder="At least 8 characters"
                      value={passForm.newPassword}
                      onChange={(e) => setPassForm({ ...passForm, newPassword: e.target.value })}
                      minLength={8}
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPass({ ...showPass, new: !showPass.new })}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 text-xs"
                    >
                      {showPass.new ? "✕" : "👁"}
                    </button>
                  </div>
                </div>

                <div>
                  <label htmlFor="pass-confirm" className="label">Confirm New Password *</label>
                  <div className="relative">
                    <input
                      id="pass-confirm"
                      type={showPass.confirm ? "text" : "password"}
                      className="input pr-10 font-mono"
                      placeholder="Repeat new password"
                      value={passForm.confirmPassword}
                      onChange={(e) => setPassForm({ ...passForm, confirmPassword: e.target.value })}
                      minLength={8}
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPass({ ...showPass, confirm: !showPass.confirm })}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 text-xs"
                    >
                      {showPass.confirm ? "✕" : "👁"}
                    </button>
                  </div>
                </div>
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  className="btn btn-secondary btn-sm text-xs font-semibold px-4"
                  disabled={passSaving}
                >
                  {passSaving ? "Updating Password..." : "Update Password →"}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Right Column (Sidebar Summary Card) */}
        <div className="space-y-6">
          <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl text-center space-y-3">
            <div className="w-16 h-16 bg-[#123326] text-emerald-300 rounded-full flex items-center justify-center font-bold text-2xl mx-auto shadow-xs border border-[#0b2219] overflow-hidden">
              {profile?.photoUrl ? (
                <img
                  src={profile.photoUrl}
                  alt={profile.name || "Farmer"}
                  className="w-full h-full object-cover"
                />
              ) : (
                profile?.name?.[0]?.toUpperCase() ?? "F"
              )}
            </div>

            <div>
              <h3 className="font-bold text-slate-950 text-base">{profile?.name}</h3>
              <p className="text-xs text-slate-500 font-mono">{profile?.email}</p>
            </div>

            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded bg-emerald-100 text-emerald-900 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-600" />
              Verified Farmer Account
            </div>

            <div className="space-y-2 text-left border-t border-slate-100 pt-3 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="text-slate-500">Registered Cows</span>
                <span className="font-bold text-slate-900 font-mono">{profile?._count?.cattle ?? 0}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="text-slate-500">District</span>
                <span className="font-medium text-slate-800">{profile?.assignedRegion ?? "Tamil Nadu"}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-50">
                <span className="text-slate-500">Farm Name</span>
                <span className="font-semibold text-slate-800">{profile?.farmId || "My Farm"}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Member Since</span>
                <span className="text-slate-700 font-mono">{fmtDate(profile?.createdAt)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

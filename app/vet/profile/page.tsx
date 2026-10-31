"use client";

import { useState, useEffect } from "react";
import { TAMIL_NADU_REGIONS } from "@/lib/constants";
import { fmtDate } from "@/lib/utils";
import { IconStethoscope, IconEye, IconEyeOff, IconCheckCircle } from "@/components/icons";

interface VetProfile {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: string;
  assignedRegion: string | null;
  photoUrl: string | null;
  isVerified: boolean;
  isActive: boolean;
  createdAt: string;
  _count?: {
    vetCases: number;
  };
}

export default function VetProfilePage() {
  const [profile, setProfile] = useState<VetProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // Profile details form state
  const [detailsForm, setDetailsForm] = useState({
    name: "",
    phone: "",
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
      const res = await fetch("/api/vet/profile");
      const data = await res.json();
      if (res.ok && data.user) {
        setProfile(data.user);
        setDetailsForm({
          name: data.user.name ?? "",
          phone: data.user.phone ?? "",
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
      const res = await fetch("/api/vet/profile", {
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
      setDetailsMsg({ type: "success", text: "Veterinarian details & photo updated successfully!" });
    } catch {
      setDetailsSaving(false);
      setDetailsMsg({ type: "error", text: "Network error. Please try again." });
    }
  };

  // Change password
  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPassMsg(null);

    if (passForm.newPassword !== passForm.confirmPassword) {
      setPassMsg({ type: "error", text: "New passwords do not match." });
      return;
    }

    if (passForm.newPassword.length < 8) {
      setPassMsg({ type: "error", text: "New password must be at least 8 characters long." });
      return;
    }

    setPassSaving(true);

    try {
      const res = await fetch("/api/vet/profile", {
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
        setPassMsg({ type: "error", text: data.error ?? "Failed to change password." });
        return;
      }

      setPassMsg({ type: "success", text: "Password changed successfully!" });
      setPassForm({ currentPassword: "", newPassword: "", confirmPassword: "" });
    } catch {
      setPassSaving(false);
      setPassMsg({ type: "error", text: "Network error. Please try again." });
    }
  };

  if (loading) {
    return (
      <div className="p-6 md:p-8 space-y-6 max-w-4xl mx-auto">
        <div className="h-8 w-48 bg-slate-200 rounded animate-pulse" />
        <div className="h-48 bg-white border border-slate-200 rounded-xl p-6 animate-pulse" />
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 md:p-8 space-y-8 max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="pb-4 border-b border-slate-200">
        <h1 className="text-xl sm:text-2xl font-bold text-slate-950 font-display">
          Veterinarian Profile &amp; Settings
        </h1>
      </div>

      {/* Profile Overview Card */}
      {profile && (
        <div className="card p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3.5">
              <div className="w-14 h-14 bg-[#0f3d32] text-emerald-300 rounded-2xl flex items-center justify-center font-bold text-xl font-mono shadow-sm overflow-hidden border border-emerald-800">
                {profile.photoUrl ? (
                  <img
                    src={profile.photoUrl}
                    alt={profile.name || "Veterinarian"}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  profile.name?.[0]?.toUpperCase() ?? "V"
                )}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-lg font-bold text-slate-900">{profile.name}</h2>
                  <span className="badge-healthy text-[10px]">FIELD VET</span>
                  {profile.isVerified && (
                    <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full">
                      ✓ VERIFIED
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 mt-1 flex-wrap">
                  <span className="text-xs text-slate-500 font-mono">{profile.email}</span>
                  <span className="text-slate-300">•</span>
                  <span className="text-xs text-slate-600">
                    District: <span className="font-bold text-slate-900">{profile.assignedRegion || "Salem"}</span>
                  </span>
                </div>
              </div>
            </div>

            <div className="flex sm:flex-col items-end justify-between sm:justify-center border-t sm:border-t-0 pt-3 sm:pt-0 border-slate-100">
              <span className="text-[10px] font-mono text-slate-400 uppercase font-semibold">Active Since</span>
              <span className="text-xs font-mono font-bold text-slate-700">{fmtDate(profile.createdAt)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Edit Details Form */}
      <div className="card p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-5">
        <div>
          <h3 className="text-sm font-bold text-slate-900 uppercase font-mono tracking-wider">
            Edit Contact &amp; District
          </h3>
        </div>

        {detailsMsg && (
          <div
            className={`p-3 rounded-lg text-xs font-medium border flex items-center gap-2 ${
              detailsMsg.type === "success"
                ? "bg-emerald-50 text-emerald-900 border-emerald-300"
                : "bg-red-50 text-red-900 border-red-300"
            }`}
          >
            {detailsMsg.type === "success" && <IconCheckCircle className="w-4 h-4 text-emerald-700" />}
            {detailsMsg.text}
          </div>
        )}

        <form onSubmit={handleSaveDetails} className="space-y-4">
          {/* Photo Upload Section */}
          <div className="flex flex-col sm:flex-row items-center gap-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
            <div className="w-16 h-16 rounded-full overflow-hidden bg-[#0f3d32] text-emerald-300 flex items-center justify-center font-bold text-xl border-2 border-emerald-600 shrink-0 shadow-xs">
              {detailsForm.photoUrl ? (
                <img
                  src={detailsForm.photoUrl}
                  alt="Veterinarian Profile"
                  className="w-full h-full object-cover"
                />
              ) : (
                <span>{detailsForm.name?.[0]?.toUpperCase() || "V"}</span>
              )}
            </div>

            <div className="space-y-1 text-center sm:text-left flex-1">
              <p className="text-xs font-bold text-slate-800">Profile Photo</p>
              <p className="text-[11px] text-slate-500">
                Upload a square PNG, JPG, or WebP (max 4 MB). Visible across your veterinary workspace &amp; diagnosis reports.
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

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="vet-name" className="label">Full Name</label>
              <input
                id="vet-name"
                type="text"
                className="input"
                value={detailsForm.name}
                onChange={(e) => setDetailsForm({ ...detailsForm, name: e.target.value })}
                required
              />
            </div>

            <div>
              <label htmlFor="vet-phone" className="label">Mobile Number</label>
              <input
                id="vet-phone"
                type="tel"
                className="input font-mono"
                value={detailsForm.phone}
                onChange={(e) => setDetailsForm({ ...detailsForm, phone: e.target.value })}
                required
              />
            </div>
          </div>

          <div>
            <label htmlFor="vet-region" className="label">Veterinary Assigned Region</label>
            <select
              id="vet-region"
              className="input"
              value={detailsForm.assignedRegion}
              onChange={(e) => setDetailsForm({ ...detailsForm, assignedRegion: e.target.value })}
              required
            >
              {TAMIL_NADU_REGIONS.map((r) => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={detailsSaving}
              className="btn btn-primary btn-sm px-5 font-bold text-xs"
            >
              {detailsSaving ? "Saving..." : "Save Details"}
            </button>
          </div>
        </form>
      </div>

      {/* Change Password Form */}
      <div className="card p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-5">
        <div>
          <h3 className="text-sm font-bold text-slate-900 uppercase font-mono tracking-wider">
            Security &amp; Password
          </h3>
        </div>

        {passMsg && (
          <div
            className={`p-3 rounded-lg text-xs font-medium border flex items-center gap-2 ${
              passMsg.type === "success"
                ? "bg-emerald-50 text-emerald-900 border-emerald-300"
                : "bg-red-50 text-red-900 border-red-300"
            }`}
          >
            {passMsg.type === "success" && <IconCheckCircle className="w-4 h-4 text-emerald-700" />}
            {passMsg.text}
          </div>
        )}

        <form onSubmit={handleChangePassword} className="space-y-4">
          <div>
            <label htmlFor="vet-curr-pass" className="label">Current Password</label>
            <div className="relative flex items-center">
              <input
                id="vet-curr-pass"
                type={showPass.current ? "text" : "password"}
                className="input pr-12 font-mono text-sm w-full"
                placeholder="••••••••••••"
                value={passForm.currentPassword}
                onChange={(e) => setPassForm({ ...passForm, currentPassword: e.target.value })}
                required
              />
              <button
                type="button"
                onClick={() => setShowPass({ ...showPass, current: !showPass.current })}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-slate-500 hover:text-slate-900 focus:outline-none rounded-md hover:bg-slate-100 transition-colors z-20 cursor-pointer flex items-center justify-center"
                aria-label="Toggle password view"
              >
                {showPass.current ? (
                  <IconEyeOff className="w-4 h-4 text-emerald-700" />
                ) : (
                  <IconEye className="w-4 h-4 text-slate-500" />
                )}
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="vet-new-pass" className="label">New Password (Min 8 chars)</label>
              <div className="relative flex items-center">
                <input
                  id="vet-new-pass"
                  type={showPass.new ? "text" : "password"}
                  className="input pr-12 font-mono text-sm w-full"
                  placeholder="••••••••••••"
                  value={passForm.newPassword}
                  onChange={(e) => setPassForm({ ...passForm, newPassword: e.target.value })}
                  required
                  minLength={8}
                />
                <button
                  type="button"
                  onClick={() => setShowPass({ ...showPass, new: !showPass.new })}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-slate-500 hover:text-slate-900 focus:outline-none rounded-md hover:bg-slate-100 transition-colors z-20 cursor-pointer flex items-center justify-center"
                  aria-label="Toggle password view"
                >
                  {showPass.new ? (
                    <IconEyeOff className="w-4 h-4 text-emerald-700" />
                  ) : (
                    <IconEye className="w-4 h-4 text-slate-500" />
                  )}
                </button>
              </div>
            </div>

            <div>
              <label htmlFor="vet-confirm-pass" className="label">Confirm New Password</label>
              <div className="relative flex items-center">
                <input
                  id="vet-confirm-pass"
                  type={showPass.confirm ? "text" : "password"}
                  className="input pr-12 font-mono text-sm w-full"
                  placeholder="••••••••••••"
                  value={passForm.confirmPassword}
                  onChange={(e) => setPassForm({ ...passForm, confirmPassword: e.target.value })}
                  required
                  minLength={8}
                />
                <button
                  type="button"
                  onClick={() => setShowPass({ ...showPass, confirm: !showPass.confirm })}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-slate-500 hover:text-slate-900 focus:outline-none rounded-md hover:bg-slate-100 transition-colors z-20 cursor-pointer flex items-center justify-center"
                  aria-label="Toggle password view"
                >
                  {showPass.confirm ? (
                    <IconEyeOff className="w-4 h-4 text-emerald-700" />
                  ) : (
                    <IconEye className="w-4 h-4 text-slate-500" />
                  )}
                </button>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={passSaving || !passForm.newPassword}
              className="btn btn-primary btn-sm px-5 font-bold text-xs"
            >
              {passSaving ? "Updating Password..." : "Update Password"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

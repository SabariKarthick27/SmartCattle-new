"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { TAMIL_NADU_REGIONS, TAMIL_NADU_DISTRICTS } from "@/lib/constants";
import { SmartCattleLogo } from "@/components/SmartCattleLogo";
import { IconEye, IconEyeOff } from "@/components/icons";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "",
    phone: "",
    email: "",
    password: "",
    role: "farmer",
    farmId: "",
    assignedRegion: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    setLoading(false);

    if (!res.ok) {
      setError(data.error ?? "Registration failed. Please check your inputs.");
      return;
    }

    setSuccess(true);
  };

  if (success) {
    return (
      <div className="min-h-screen bg-[#0d2218] flex items-center justify-center p-4">
        <div className="card p-8 sm:p-10 max-w-md w-full text-center bg-white border border-slate-300 shadow-xl rounded-xl space-y-4">
          <div className="w-12 h-12 bg-emerald-100 text-emerald-800 rounded-full flex items-center justify-center font-bold text-xl mx-auto">
            ✓
          </div>
          <h2 className="text-xl font-bold text-slate-900 font-display">Account Created!</h2>
          <p className="text-slate-600 text-xs leading-relaxed">
            Your registration details have been submitted. An administrator will verify and approve your account shortly.
          </p>
          <div className="pt-2">
            <Link href="/login" className="btn btn-primary w-full">
              Go to Sign In →
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0d2218] flex flex-col justify-center py-10 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-lg flex justify-center mb-6">
        <Link href="/" className="group inline-block">
          <SmartCattleLogo variant="light" />
        </Link>
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-lg px-4 sm:px-0">
        <div className="card p-6 sm:p-8 bg-white border border-slate-300 shadow-xl rounded-xl space-y-5">
          <div className="border-b border-slate-100 pb-3">
            <h2 className="text-lg font-bold text-slate-900 tracking-tight font-display">Register New Account</h2>
            <p className="text-xs text-slate-500 mt-0.5">Sign up as a dairy farmer or field veterinarian.</p>
          </div>

          {error && (
            <div className="p-3 rounded-lg bg-red-50 border border-red-300 text-red-800 text-xs font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Role selector */}
            <div>
              <label className="label text-xs font-bold uppercase tracking-wider text-slate-700">I am a</label>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { id: "farmer", label: "Dairy Farmer", desc: "Manage cattle & log milk/feed" },
                  { id: "vet", label: "Field Veterinarian", desc: "Treat cattle & view alerts" },
                ].map((r) => {
                  const isSelected = form.role === r.id;
                  return (
                    <button
                      key={r.id}
                      type="button"
                      id={`role-${r.id}`}
                      onClick={() => setForm((prev) => ({ ...prev, role: r.id }))}
                      className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer relative ${
                        isSelected
                          ? "border-[#123326] bg-emerald-50/80 text-slate-950 shadow-sm ring-2 ring-[#123326]"
                          : "border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50"
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2">
                        <div className="text-xs font-bold">{r.label}</div>
                        <div
                          className={`w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${
                            isSelected ? "border-[#123326] bg-[#123326]" : "border-slate-300 bg-white"
                          }`}
                        >
                          {isSelected && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                        </div>
                      </div>
                      <div className="text-[11px] text-slate-500 mt-1 leading-snug">{r.desc}</div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label htmlFor="reg-name" className="label">Your Name</label>
                <input
                  id="reg-name"
                  type="text"
                  className="input"
                  placeholder="e.g. Ramesh Kumar"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  required
                  autoComplete="name"
                />
              </div>
              <div>
                <label htmlFor="reg-phone" className="label">Mobile Number</label>
                <input
                  id="reg-phone"
                  type="tel"
                  className="input font-mono"
                  placeholder="9876543210"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                  required
                  autoComplete="tel"
                />
              </div>
            </div>

            <div>
              <label htmlFor="reg-email" className="label">Email Address</label>
              <input
                id="reg-email"
                type="email"
                className="input"
                placeholder="ramesh@example.com"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
                autoComplete="email"
              />
            </div>

            <div>
              <label htmlFor="reg-password" className="label">Password (At least 8 characters)</label>
              <div className="relative flex items-center">
                <input
                  id="reg-password"
                  type={showPassword ? "text" : "password"}
                  className="input pr-12 font-mono text-sm w-full"
                  placeholder="••••••••••••"
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                  required
                  minLength={8}
                  autoComplete="new-password"
                />
                <button
                  type="button"
                  id="toggle-reg-password"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-slate-500 hover:text-slate-900 focus:outline-none rounded-md hover:bg-slate-100 transition-colors z-20 cursor-pointer flex items-center justify-center"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? (
                    <IconEyeOff className="w-5 h-5 text-emerald-700" />
                  ) : (
                    <IconEye className="w-5 h-5 text-slate-500" />
                  )}
                </button>
              </div>
            </div>

            {form.role === "farmer" && (
              <div>
                <label htmlFor="reg-farmid" className="label">Farm District / Location</label>
                <select
                  id="reg-farmid"
                  className="input"
                  value={form.farmId}
                  onChange={(e) => setForm({ ...form, farmId: e.target.value })}
                  required
                >
                  <option value="">Select your district</option>
                  {TAMIL_NADU_DISTRICTS.map((d) => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              </div>
            )}

            {form.role === "vet" && (
              <div>
                <label htmlFor="reg-region" className="label">Veterinary Region</label>
                <select
                  id="reg-region"
                  className="input"
                  value={form.assignedRegion}
                  onChange={(e) => setForm({ ...form, assignedRegion: e.target.value })}
                  required
                >
                  <option value="">Select assigned region</option>
                  {TAMIL_NADU_REGIONS.map((r) => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>
            )}

            <button
              id="reg-submit-btn"
              type="submit"
              className="btn btn-primary w-full btn-lg mt-2"
              disabled={loading}
            >
              {loading ? (
                <span className="inline-flex items-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Creating Account...
                </span>
              ) : "Create Account →"}
            </button>
          </form>

          <div className="pt-3 border-t border-slate-100 text-center text-xs text-slate-500">
            Already have an account?{" "}
            <Link href="/login" className="text-emerald-900 font-bold hover:underline">
              Sign in here
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

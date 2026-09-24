"use client";

import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { SmartCattleLogo } from "@/components/SmartCattleLogo";
import { IconEye, IconEyeOff } from "@/components/icons";

function ResetForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  if (!token) {
    return (
      <div className="card p-8 text-center space-y-4 bg-white border border-slate-300 rounded-xl shadow-md">
        <div className="text-3xl text-amber-600">⚠️</div>
        <h3 className="text-lg font-bold text-slate-900">Invalid Reset Link</h3>
        <p className="text-slate-600 text-xs">This password reset link is invalid or has expired.</p>
        <div className="pt-2">
          <Link href="/forgot-password" className="btn btn-secondary w-full">
            Request New Reset Link
          </Link>
        </div>
      </div>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }
    setLoading(true);
    setError("");

    const res = await fetch("/api/auth/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, password }),
    });

    setLoading(false);

    if (!res.ok) {
      const d = await res.json();
      setError(d.error ?? "Could not reset password. Please try again.");
      return;
    }

    setSuccess(true);
    setTimeout(() => router.push("/login"), 2500);
  };

  if (success) {
    return (
      <div className="card p-8 text-center space-y-4 bg-white border border-slate-300 rounded-xl shadow-md">
        <div className="w-12 h-12 bg-emerald-100 text-emerald-800 rounded-full flex items-center justify-center font-bold text-xl mx-auto">
          ✓
        </div>
        <h3 className="text-lg font-bold text-slate-900">Password Reset Successfully!</h3>
        <p className="text-slate-600 text-xs">Your password has been changed. Redirecting to sign in...</p>
      </div>
    );
  }

  return (
    <div className="card p-6 sm:p-8 bg-white border border-slate-300 shadow-xl rounded-xl space-y-6">
      <div className="border-b border-slate-100 pb-3">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight font-display">Create New Password</h2>
        <p className="text-xs text-slate-500 mt-1">Please enter your new password below.</p>
      </div>

      {error && (
        <div className="p-3.5 rounded-lg bg-red-50 border border-red-300 text-red-800 text-xs font-medium">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="reset-password" className="label">New Password</label>
          <div className="relative flex items-center">
            <input
              id="reset-password"
              type={showPassword ? "text" : "password"}
              className="input pr-12 font-mono text-sm w-full"
              placeholder="••••••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />
            <button
              type="button"
              id="toggle-reset-password"
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

        <div>
          <label htmlFor="reset-confirm" className="label">Confirm New Password</label>
          <input
            id="reset-confirm"
            type={showPassword ? "text" : "password"}
            className="input font-mono text-sm w-full"
            placeholder="••••••••••••"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
            minLength={8}
          />
        </div>

        <button
          id="reset-submit-btn"
          type="submit"
          className="btn btn-primary w-full btn-lg font-semibold"
          disabled={loading || (!!confirm && password !== confirm)}
        >
          {loading ? (
            <span className="inline-flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Saving Password...
            </span>
          ) : "Save New Password →"}
        </button>
      </form>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen bg-[#0d2218] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md flex justify-center mb-6">
        <Link href="/" className="group inline-block">
          <SmartCattleLogo variant="light" />
        </Link>
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <Suspense fallback={<div className="card p-8 text-center text-slate-400 font-mono text-xs">Loading form...</div>}>
          <ResetForm />
        </Suspense>
      </div>
    </div>
  );
}

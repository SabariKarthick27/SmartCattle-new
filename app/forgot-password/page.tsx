"use client";

import { useState } from "react";
import Link from "next/link";
import { SmartCattleLogo } from "@/components/SmartCattleLogo";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const res = await fetch("/api/auth/forgot-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    setLoading(false);

    if (!res.ok) {
      const d = await res.json();
      setError(d.error ?? "Something went wrong. Please try again.");
      return;
    }

    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-[#0d2218] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md flex justify-center mb-6">
        <Link href="/" className="group inline-block">
          <SmartCattleLogo variant="light" />
        </Link>
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div className="card p-6 sm:p-8 bg-white border border-slate-300 shadow-xl rounded-xl space-y-6">
          <div className="border-b border-slate-100 pb-3">
            <h2 className="text-xl font-bold text-slate-900 tracking-tight font-display">Forgot Password?</h2>
            <p className="text-xs text-slate-500 mt-1">We will send a secure reset link to your email.</p>
          </div>

          {submitted ? (
            <div className="text-center space-y-4 py-2">
              <div className="w-12 h-12 bg-emerald-100 text-emerald-800 rounded-full flex items-center justify-center font-bold text-xl mx-auto">
                ✓
              </div>
              <h3 className="text-lg font-bold text-slate-900">Check Your Email</h3>
              <p className="text-slate-600 text-xs leading-relaxed">
                If <strong>{email}</strong> is registered, we sent a password reset link. Please check your inbox and spam folder.
              </p>
              <div className="pt-2">
                <Link href="/login" className="btn btn-secondary w-full">
                  Back to Sign In
                </Link>
              </div>
            </div>
          ) : (
            <>
              {error && (
                <div className="p-3.5 rounded-lg bg-red-50 border border-red-300 text-red-800 text-xs font-medium">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="forgot-email" className="label">Email Address</label>
                  <input
                    id="forgot-email"
                    type="email"
                    className="input"
                    placeholder="farmer@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoFocus
                  />
                </div>

                <button
                  id="forgot-submit-btn"
                  type="submit"
                  className="btn btn-primary w-full btn-lg font-semibold"
                  disabled={loading}
                >
                  {loading ? (
                    <span className="inline-flex items-center gap-2">
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Sending Link...
                    </span>
                  ) : "Send Reset Link →"}
                </button>
              </form>

              <div className="text-center text-xs text-slate-500 pt-2 border-t border-slate-100">
                Remember your password?{" "}
                <Link href="/login" className="text-emerald-900 font-bold hover:underline">
                  Sign in
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

"use client";

import { useState, Suspense } from "react";
import { signIn, getSession } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { SmartCattleLogo } from "@/components/SmartCattleLogo";
import { IconEye, IconEyeOff } from "@/components/icons";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") ?? "";

  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const result = await signIn("credentials", {
      email: form.email,
      password: form.password,
      redirect: false,
    });

    if (result?.error) {
      setLoading(false);
      if (result.error === "PENDING_APPROVAL") {
        setError("Your account is waiting for approval from the administrator.");
      } else {
        setError("Invalid email or password. Please check and try again.");
      }
      return;
    }

    if (callbackUrl) {
      router.push(callbackUrl);
    } else {
      const session = await getSession();
      const userRole = session?.user?.role;
      if (userRole === "admin") {
        router.push("/admin");
      } else if (userRole === "vet") {
        router.push("/vet");
      } else {
        router.push("/farmer");
      }
    }
    router.refresh();
  };

  return (
    <div className="card p-6 sm:p-8 bg-white border border-slate-300 shadow-md rounded-xl space-y-6">
      <div className="border-b border-slate-100 pb-4">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight font-display">Sign In to SmartCattle</h2>
        <p className="text-xs text-slate-500 mt-1">Enter your email address and password to access your account.</p>
      </div>

      {error && (
        <div className="p-3.5 rounded-lg bg-red-50 border border-red-300 text-red-800 text-xs font-medium">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="login-email" className="label">Email Address</label>
          <input
            id="login-email"
            type="email"
            className="input"
            placeholder="farmer@example.com"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
            autoComplete="username"
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-1">
            <label htmlFor="login-password" className="label mb-0">Password</label>
            <Link href="/forgot-password" className="text-xs text-emerald-800 hover:text-emerald-950 font-semibold">
              Forgot password?
            </Link>
          </div>
          <div className="relative flex items-center">
            <input
              id="login-password"
              type={showPassword ? "text" : "password"}
              className="input pr-12 text-sm w-full font-mono"
              placeholder="••••••••••••"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
              autoComplete="current-password"
            />
            <button
              type="button"
              id="toggle-password-visibility"
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

        <button
          id="login-submit-btn"
          type="submit"
          className="btn btn-primary w-full btn-lg font-semibold tracking-wide justify-center"
          disabled={loading}
        >
          {loading ? (
            <span className="inline-flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Signing In...
            </span>
          ) : "Sign In →"}
        </button>
      </form>

      <div className="text-center text-xs text-slate-500 pt-2 border-t border-slate-100">
        Don&apos;t have an account yet?{" "}
        <Link href="/register" className="text-emerald-900 font-bold hover:underline">
          Create Account
        </Link>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-[#0d2218] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md flex justify-center mb-6">
        <Link href="/" className="group inline-block">
          <SmartCattleLogo variant="light" />
        </Link>
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <Suspense fallback={<div className="card p-8 text-center text-slate-400 font-mono text-xs">Loading login form...</div>}>
          <LoginForm />
        </Suspense>
      </div>
    </div>
  );
}


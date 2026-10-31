"use client";

import { useState, useEffect } from "react";
import { signOut } from "next-auth/react";
import { IconSignOut } from "@/components/icons";

interface SignOutModalProps {
  isOpen: boolean;
  onClose: () => void;
  userName?: string | null;
  userRole?: string | null;
  userEmail?: string | null;
  userImage?: string | null;
}

export default function SignOutModal({
  isOpen,
  onClose,
  userName,
  userRole = "User",
  userEmail,
  userImage,
}: SignOutModalProps) {
  const [loading, setLoading] = useState(false);

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen && !loading) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, loading, onClose]);

  if (!isOpen) return null;

  const handleConfirmSignOut = async () => {
    try {
      setLoading(true);
      // Perform NextAuth sign out without default hard navigation
      await signOut({ redirect: false, callbackUrl: "/" });
      
      // Use replace to prevent back-button from restoring the previous dashboard history entry
      window.location.replace("/");
    } catch (err) {
      console.error("Sign out error:", err);
      // Fallback redirect to landing page
      window.location.replace("/");
    }
  };

  const roleLabel =
    userRole?.toLowerCase() === "admin"
      ? "Administrator"
      : userRole?.toLowerCase() === "vet"
      ? "Veterinarian"
      : userRole?.toLowerCase() === "farmer"
      ? "Dairy Farmer"
      : userRole;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="signout-modal-title"
      className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm"
      onClick={() => {
        if (!loading) onClose();
      }}
    >
      <div
        className="relative w-full max-w-md bg-slate-900 border border-slate-700/90 rounded-2xl p-6 shadow-2xl text-slate-100 animate-in fade-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header Icon */}
        <div className="flex items-center gap-3.5 mb-4">
          <div className="w-11 h-11 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0">
            <IconSignOut className="w-5 h-5" />
          </div>
          <div>
            <h3
              id="signout-modal-title"
              className="text-lg font-bold text-white tracking-tight font-display"
            >
              Sign Out Confirmation
            </h3>
            <p className="text-xs text-slate-400">
              Are you sure you want to log out?
            </p>
          </div>
        </div>

        {/* User preview card */}
        <div className="p-3 mb-5 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center gap-3">
          {userImage ? (
            <img
              src={userImage}
              alt=""
              className="w-9 h-9 rounded-full object-cover border border-emerald-500/50 shrink-0"
            />
          ) : (
            <div className="w-9 h-9 rounded-full bg-slate-800 text-emerald-400 border border-slate-700 font-mono text-xs font-bold flex items-center justify-center shrink-0">
              {userName?.[0]?.toUpperCase() ?? "U"}
            </div>
          )}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-white truncate">
                {userName ?? "Signed in User"}
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 uppercase font-semibold">
                {roleLabel}
              </span>
            </div>
            <p className="text-[11px] font-mono text-slate-400 truncate">
              {userEmail ?? ""}
            </p>
          </div>
        </div>

        {/* Explanatory text */}
        <p className="text-xs text-slate-300 leading-relaxed mb-6">
          You will be safely logged out and redirected to the SmartCattle landing page. Any unsaved changes in active forms will be lost.
        </p>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            disabled={loading}
            onClick={onClose}
            className="px-4 py-2 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg transition-colors cursor-pointer disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={handleConfirmSignOut}
            className="btn btn-primary px-5 py-2 text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white border-rose-500 shadow-md transition-all flex items-center gap-2 cursor-pointer disabled:opacity-75"
          >
            {loading ? (
              <>
                <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Signing Out...</span>
              </>
            ) : (
              <>
                <IconSignOut className="w-3.5 h-3.5" />
                <span>Confirm Sign Out</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

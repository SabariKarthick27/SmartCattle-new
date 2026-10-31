"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  IconOverview,
  IconUsers,
  IconAnalytics,
  IconModel,
  IconAudit,
  IconSignOut,
} from "@/components/icons";
import { SmartCattleLogo } from "@/components/SmartCattleLogo";
import SignOutModal from "@/components/SignOutModal";

interface AdminSidebarProps {
  userName?: string | null;
  userEmail?: string | null;
  userImage?: string | null;
}

export default function AdminSidebar({ userName, userEmail, userImage }: AdminSidebarProps) {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [showSignOutModal, setShowSignOutModal] = useState(false);

  const links = [
    { href: "/admin", label: "Admin Dashboard", icon: IconOverview, exact: true },
    { href: "/admin/model", label: "Health AI Settings", icon: IconModel },
    { href: "/admin/analytics", label: "Herd Health Analytics", icon: IconAnalytics },
    { href: "/admin/users", label: "User & Farm Management", icon: IconUsers },
    { href: "/admin/audit", label: "Activity & Audit Logs", icon: IconAudit },
  ];

  const sidebarContent = (
    <div className="flex flex-col h-full bg-slate-950 text-slate-200 border-r border-slate-800">
      {/* Brand Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <Link href="/admin" prefetch={true} className="flex items-center gap-2 group">
          <SmartCattleLogo variant="light" subtitle="Admin Panel" />
        </Link>
        <button
          type="button"
          onClick={() => setMobileOpen(false)}
          className="md:hidden p-1.5 text-slate-400 hover:text-white"
          aria-label="Close menu"
        >
          ✕
        </button>
      </div>

      {/* Nav Rail */}
      <nav className="flex-1 px-3 py-3 space-y-1 overflow-y-auto">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = link.exact
            ? pathname === link.href
            : pathname.startsWith(link.href);

          return (
            <Link
              key={link.href}
              href={link.href}
              prefetch={true}
              onClick={() => setMobileOpen(false)}
              className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                isActive
                  ? "bg-emerald-950/80 text-emerald-400 border border-emerald-500 shadow-xs font-bold"
                  : "text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-emerald-400" : "text-slate-500"}`} />
              <span className="flex-1 truncate">{link.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Operator Session Info */}
      <div className="p-3 border-t border-slate-800 bg-slate-900/60">
        <div className="flex items-center gap-2.5 mb-2.5 p-1.5">
          {userImage ? (
            <img
              src={userImage}
              alt=""
              className="w-7 h-7 rounded-full object-cover border border-emerald-500 shrink-0"
            />
          ) : (
            <div className="w-7 h-7 bg-slate-800 text-emerald-400 rounded font-mono text-xs font-bold flex items-center justify-center border border-slate-700 shrink-0">
              {(!userName || userName.includes("Primary Admin") || userName === "SmartCattle Primary Admin" ? "A" : userName[0]?.toUpperCase())}
            </div>
          )}
          <div className="flex-1 min-w-0">
            <p className="text-xs font-bold text-white truncate">
              {!userName || userName.includes("Primary Admin") || userName === "SmartCattle Primary Admin" ? "Admin" : userName}
            </p>
            <p className="text-[10px] font-mono text-slate-400 truncate">{userEmail ?? "System Administrator"}</p>
          </div>
        </div>
        <button
          type="button"
          onClick={() => setShowSignOutModal(true)}
          className="btn btn-secondary btn-sm w-full justify-center text-slate-300 bg-slate-800 border-slate-700 hover:bg-slate-700 text-xs py-1.5 cursor-pointer"
        >
          <IconSignOut className="w-3.5 h-3.5 text-slate-400" />
          <span>Sign Out</span>
        </button>
      </div>

      <SignOutModal
        isOpen={showSignOutModal}
        onClose={() => setShowSignOutModal(false)}
        userName={userName}
        userEmail={userEmail}
        userImage={userImage}
        userRole="Administrator"
      />
    </div>
  );

  return (
    <>
      {/* Mobile Top App Bar */}
      <div className="md:hidden fixed top-0 left-0 right-0 h-14 bg-slate-950 border-b border-slate-800 z-40 px-4 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={() => setMobileOpen(true)}
            className="p-1.5 rounded-md border border-slate-800 text-slate-300 hover:bg-slate-900"
            aria-label="Open Navigation"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <span className="font-bold text-white text-sm font-display">SmartCattle Admin</span>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded">
          ADMIN
        </span>
      </div>

      {/* Mobile Drawer Overlay */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex">
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-xs transition-opacity"
            onClick={() => setMobileOpen(false)}
          />
          <div className="relative w-72 max-w-full h-full z-50 shadow-2xl">
            {sidebarContent}
          </div>
        </div>
      )}

      {/* Desktop Fixed Sidebar */}
      <aside className="hidden md:block w-60 fixed top-0 left-0 bottom-0 z-30">
        {sidebarContent}
      </aside>
    </>
  );
}

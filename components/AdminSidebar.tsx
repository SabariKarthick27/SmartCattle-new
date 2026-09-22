"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  IconOverview,
  IconUsers,
  IconAnalytics,
  IconModel,
  IconAudit,
  IconCow,
  IconSignOut,
} from "@/components/icons";

interface AdminSidebarProps {
  userName?: string | null;
  userEmail?: string | null;
}

export default function AdminSidebar({ userName, userEmail }: AdminSidebarProps) {
  const pathname = usePathname();

  const links = [
    { href: "/admin", label: "Overview", icon: IconOverview, exact: true },
    { href: "/admin/users", label: "User Management", icon: IconUsers },
    { href: "/admin/analytics", label: "Herd Analytics", icon: IconAnalytics },
    { href: "/admin/model", label: "Model Management", icon: IconModel },
    { href: "/admin/audit", label: "Audit Log", icon: IconAudit },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col fixed h-full z-40">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 gradient-hero rounded-xl flex items-center justify-center shadow-sm">
            <IconCow className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="font-bold text-slate-900 text-sm">SmartCattle</p>
            <p className="text-xs text-slate-500">Admin Console</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = link.exact
            ? pathname === link.href
            : pathname.startsWith(link.href);

          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? "bg-slate-900 text-white font-semibold shadow-sm"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-brand-400" : "text-slate-400"}`} />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* User info */}
      <div className="px-4 py-4 border-t border-slate-100">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-9 h-9 bg-slate-100 rounded-full flex items-center justify-center font-bold text-slate-800 text-sm">
            {userName?.[0]?.toUpperCase() ?? "A"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-slate-900 truncate">{userName ?? "Admin"}</p>
            <p className="text-xs text-slate-500 truncate">{userEmail ?? "System Admin"}</p>
          </div>
        </div>
        <form action="/api/auth/signout" method="POST">
          <button type="submit" className="btn-ghost btn-sm w-full justify-start text-slate-500 flex items-center gap-2">
            <IconSignOut className="w-4 h-4 text-slate-400" />
            <span>Sign out</span>
          </button>
        </form>
      </div>
    </aside>
  );
}

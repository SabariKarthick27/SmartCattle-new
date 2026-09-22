"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  IconOverview,
  IconCattle,
  IconScan,
  IconBell,
  IconAudit,
  IconUser,
  IconCow,
  IconSignOut,
} from "@/components/icons";

interface FarmerSidebarProps {
  userName?: string | null;
  userEmail?: string | null;
}

export default function FarmerSidebar({ userName, userEmail }: FarmerSidebarProps) {
  const pathname = usePathname();

  const links = [
    { href: "/farmer", label: "Overview", icon: IconOverview, exact: true },
    { href: "/farmer/cattle", label: "My Cattle", icon: IconCattle },
    { href: "/farmer/scan", label: "Scan QR", icon: IconScan },
    { href: "/farmer/notifications", label: "Notifications", icon: IconBell },
    { href: "/farmer/records", label: "Health Records", icon: IconAudit },
    { href: "/farmer/profile", label: "My Profile", icon: IconUser },
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
            <p className="text-xs text-slate-500">Farmer Portal</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = link.exact
            ? pathname === link.href
            : pathname.startsWith(link.href) ||
              (link.href === "/farmer/records" && pathname === "/farmer/health-records");

          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? "bg-brand-50 text-brand-900 font-semibold shadow-sm border border-brand-200/60"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-brand-700" : "text-slate-400"}`} />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* User info */}
      <div className="px-4 py-4 border-t border-slate-100">
        <Link
          href="/farmer/profile"
          className="flex items-center gap-3 mb-3 p-2 rounded-xl hover:bg-slate-50 transition-colors group"
        >
          <div className="w-9 h-9 bg-brand-100 rounded-full flex items-center justify-center text-brand-700 text-sm font-bold group-hover:scale-105 transition-transform">
            {userName?.[0]?.toUpperCase() ?? "F"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-slate-900 truncate group-hover:text-brand-700 transition-colors">
              {userName ?? "Farmer"}
            </p>
            <p className="text-xs text-slate-500 truncate">{userEmail ?? ""}</p>
          </div>
        </Link>
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

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  IconStethoscope,
  IconCattle,
  IconSyringe,
  IconActivity,
  IconCow,
  IconSignOut,
} from "@/components/icons";

interface VetSidebarProps {
  userName?: string | null;
  userEmail?: string | null;
}

export default function VetSidebar({ userName, userEmail }: VetSidebarProps) {
  const pathname = usePathname();

  const links = [
    { href: "/vet", label: "Case Queue", icon: IconStethoscope, exact: true },
    { href: "/vet/weekly-analysis", label: "Weekly Health Reports", icon: IconActivity },
    { href: "/vet/vaccinations", label: "Vaccination & Checkups", icon: IconSyringe },
    { href: "/vet/farms", label: "Assigned Farms", icon: IconCattle },
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
            <p className="text-xs text-slate-500">Vet Portal</p>
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
                  ? "bg-teal-50 text-teal-900 font-semibold shadow-sm border border-teal-200/60"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-teal-700" : "text-slate-400"}`} />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* User info */}
      <div className="px-4 py-4 border-t border-slate-100">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-9 h-9 bg-teal-100 text-teal-800 rounded-full flex items-center justify-center font-bold text-sm">
            {userName?.[0]?.toUpperCase() ?? "V"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-slate-900 truncate">{userName ?? "Veterinarian"}</p>
            <p className="text-xs text-slate-500 truncate">{userEmail ?? "District Vet"}</p>
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

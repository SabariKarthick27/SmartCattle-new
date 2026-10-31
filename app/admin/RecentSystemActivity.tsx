"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { IconAudit } from "@/components/icons";

export interface ActivityItem {
  id: string;
  action: string;
  actorRole: string;
  timestamp: string;
  actor?: {
    name: string;
    email?: string;
  } | null;
}

interface Props {
  initialLogs: ActivityItem[];
}

function formatRelativeTime(dateStr: string, now: Date): string {
  const d = new Date(dateStr);
  const diffSec = Math.floor((now.getTime() - d.getTime()) / 1000);

  if (diffSec < 45) return "Just now";
  if (diffSec < 3600) {
    const mins = Math.max(1, Math.floor(diffSec / 60));
    return `${mins}m ago`;
  }
  if (diffSec < 86400) {
    const hours = Math.floor(diffSec / 3600);
    return `${hours}h ago`;
  }
  const days = Math.floor(diffSec / 86400);
  if (days === 1) return "Yesterday";
  if (days < 7) return `${days}d ago`;

  return d.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
  });
}

function formatActionTitle(action: string): string {
  const map: Record<string, string> = {
    admin_approve: "Approved User Account",
    cattle_created: "Registered New Cattle",
    cattle_updated: "Updated Cattle Vitals",
    vet_request_submitted: "Requested Doctor Visit",
    case_diagnosed: "Logged Clinical Diagnosis",
    model_retrain_triggered: "Retrained AI Health Model",
    chdi_computed: "Computed Health Score",
    profile_updated: "Updated User Profile",
    vet_feedback_submitted: "Submitted Doctor Feedback",
  };
  return map[action] || action.replace(/_/g, " ");
}

export default function RecentSystemActivity({ initialLogs }: Props) {
  const [logs, setLogs] = useState<ActivityItem[]>(initialLogs);
  const [now, setNow] = useState<Date>(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchLatestLogs = useCallback(async () => {
    try {
      setIsRefreshing(true);
      const res = await fetch("/api/admin/audit-log?limit=8");
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data.logs)) {
          setLogs(
            data.logs.map((l: any) => ({
              id: l.id,
              action: l.action,
              actorRole: l.actorRole,
              timestamp: typeof l.timestamp === "string" ? l.timestamp : new Date(l.timestamp).toISOString(),
              actor: l.actor,
            }))
          );
        }
      }
    } catch {
      // Network error, keep current state
    } finally {
      setIsRefreshing(false);
      setNow(new Date());
    }
  }, []);

  // Update relative time clock every 10s & poll for new activity every 15s
  useEffect(() => {
    const clockTimer = setInterval(() => {
      setNow(new Date());
    }, 10000);

    const pollTimer = setInterval(() => {
      fetchLatestLogs();
    }, 15000);

    return () => {
      clearInterval(clockTimer);
      clearInterval(pollTimer);
    };
  }, [fetchLatestLogs]);

  return (
    <div className="card border border-slate-300 bg-white overflow-hidden shadow-xs rounded-xl">
      <div className="p-3.5 bg-[#f8faf9] border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <IconAudit className="w-4 h-4 text-slate-800" />
          <h2 className="font-bold text-xs uppercase font-mono text-slate-900 tracking-wider">
            Recent System Activity
          </h2>
          <span className="flex items-center gap-1 text-[10px] font-mono text-emerald-800 font-bold px-1.5 py-0.5 bg-emerald-50 border border-emerald-200 rounded">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            LIVE
          </span>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={fetchLatestLogs}
            disabled={isRefreshing}
            className="text-[11px] font-mono text-slate-500 hover:text-slate-900 transition-colors"
            title="Refresh activity logs"
          >
            {isRefreshing ? "Updating..." : "↻ Refresh"}
          </button>
          <span className="text-slate-300">|</span>
          <Link href="/admin/audit" className="text-xs font-mono font-bold text-emerald-900 hover:underline">
            Full Log →
          </Link>
        </div>
      </div>

      <div className="divide-y divide-slate-100">
        {logs.map((log) => {
          const relativeTime = formatRelativeTime(log.timestamp, now);
          const fullTime = new Date(log.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          });

          return (
            <div key={log.id} className="p-3 flex items-start justify-between gap-2 text-xs hover:bg-slate-50/60 transition-colors">
              <div className="min-w-0">
                <p className="font-semibold text-slate-800 truncate font-mono text-xs">
                  <span className="text-slate-400">[{log.actorRole.toUpperCase()}]</span>{" "}
                  <span className="text-slate-900 font-bold">{log.actor?.name ?? "User"}</span>
                </p>
                <p className="text-slate-600 text-[11px] truncate mt-0.5 font-medium">
                  {formatActionTitle(log.action)}
                </p>
              </div>

              <div className="text-right shrink-0">
                <span className="text-[11px] font-mono font-bold text-slate-700 block" title={new Date(log.timestamp).toLocaleString()}>
                  {relativeTime}
                </span>
                <span className="text-[10px] font-mono text-slate-400 block mt-0.5">
                  {fullTime}
                </span>
              </div>
            </div>
          );
        })}

        {logs.length === 0 && (
          <div className="p-8 text-center text-slate-400 text-xs font-mono">
            No recent audit events recorded.
          </div>
        )}
      </div>
    </div>
  );
}


"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  IconCheckCircle,
  IconShieldAlert,
  IconActivity,
  IconScan,
  IconCow,
  IconCalendar,
  IconRefresh,
} from "@/components/icons";
import { getCHDIBadgeConfig, calcAge } from "@/lib/utils";

export interface CattleProfileData {
  id: string;
  cattleId?: string;
  tagId: string;
  name?: string | null;
  breed: string;
  dob?: string | Date;
  gender?: string | null;
  purpose?: string | null;
  farmer?: { id?: string; name: string; phone?: string };
  chdiHistory?: Array<{
    score: number | null;
    status: string;
    confidence?: number;
    topFactors?: any[];
  }>;
  weightLogs?: Array<{ value: number; timestamp?: string }>;
  milkLogs?: Array<{ litres: number; timestamp?: string }>;
  feedLogs?: Array<{ quantity: number; feedType?: string; timestamp?: string }>;
  temperatureLogs?: Array<{ value: number; timestamp?: string }>;
  activityLogs?: Array<{ value: number; timestamp?: string }>;
  ruminationLogs?: Array<{ minutes: number; timestamp?: string }>;
}

interface DailyHealthLogFormProps {
  cattle: CattleProfileData;
  onSuccess?: (result: any) => void;
  onScanNext?: () => void;
  onCancel?: () => void;
}

export default function DailyHealthLogForm({
  cattle,
  onSuccess,
  onScanNext,
  onCancel,
}: DailyHealthLogFormProps) {
  // Current local ISO string for datetime-local input (YYYY-MM-DDTHH:mm)
  const nowStr = useMemo(() => {
    const d = new Date();
    const pad = (n: number) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }, []);

  const [date, setDate] = useState(nowStr);
  const [weight, setWeight] = useState<string>("");
  const [feedQuantity, setFeedQuantity] = useState<string>("");
  const [feedType, setFeedType] = useState<string>("Mixed Green Grass / Fodder");
  const [milkLitres, setMilkLitres] = useState<string>("");
  const [temperature, setTemperature] = useState<string>("");

  // Status & confirmation
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [submissionResult, setSubmissionResult] = useState<{
    success: boolean;
    message: string;
    savedMetrics: Record<string, any>;
    chdi: any;
  } | null>(null);

  const cattleRealId = cattle.cattleId || cattle.id;

  const latestCHDI = cattle.chdiHistory?.[0];
  const initialBadge = getCHDIBadgeConfig(latestCHDI?.status ?? "abstain");

  // Handle Form Submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    // 1. Client Validation
    const hasWeight = weight.trim() !== "";
    const hasFeed = feedQuantity.trim() !== "";
    const hasMilk = milkLitres.trim() !== "";
    const hasTemp = temperature.trim() !== "";

    if (!hasWeight && !hasFeed && !hasMilk && !hasTemp) {
      setFormError("Please enter at least one daily health vital metric before submitting.");
      return;
    }

    if (hasWeight) {
      const w = Number(weight);
      if (isNaN(w) || w <= 0 || w > 2000) {
        setFormError("Body Weight must be a valid number between 1 kg and 2000 kg.");
        return;
      }
    }

    if (hasFeed) {
      const f = Number(feedQuantity);
      if (isNaN(f) || f < 0 || f > 150) {
        setFormError("Feed Intake must be a valid number between 0 kg and 150 kg.");
        return;
      }
    }

    if (hasMilk) {
      const m = Number(milkLitres);
      if (isNaN(m) || m < 0 || m > 100) {
        setFormError("Daily Milk Yield must be a valid number between 0 L and 100 L.");
        return;
      }
    }

    if (hasTemp) {
      const t = Number(temperature);
      if (isNaN(t) || t < 30.0 || t > 45.0) {
        setFormError("Body Temperature must be realistic between 30.0°C and 45.0°C (Normal: ~38.6°C).");
        return;
      }
    }

    // 2. Dispatch to dedicated daily-log API
    setSubmitting(true);
    try {
      const payload = {
        date: new Date(date).toISOString(),
        weight: hasWeight ? Number(weight) : null,
        feedQuantity: hasFeed ? Number(feedQuantity) : null,
        feedType: hasFeed ? feedType : undefined,
        milkLitres: hasMilk ? Number(milkLitres) : null,
        temperature: hasTemp ? Number(temperature) : null,
        source: "qr_scan",
      };

      const res = await fetch(`/api/cattle/${cattleRealId}/daily-log`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        setSubmissionResult({
          success: true,
          message: data.message || "Daily health record saved successfully!",
          savedMetrics: data.savedMetrics || {},
          chdi: data.chdi || null,
        });
        if (onSuccess) onSuccess(data);
      } else {
        setFormError(data.error || "Failed to save daily health record. Please try again.");
      }
    } catch (err: any) {
      console.error("Submission error:", err);
      setFormError("Network error submitting health details. Please check connection.");
    } finally {
      setSubmitting(false);
    }
  };

  // ── SUCCESS CONFIRMATION VIEW ──────────────────────────────────────
  if (submissionResult) {
    const assessedStatus = submissionResult.chdi?.status ?? latestCHDI?.status ?? "abstain";
    const assessedScore = submissionResult.chdi?.score ?? latestCHDI?.score;
    const assessedBadge = getCHDIBadgeConfig(assessedStatus);
    const isWatchOrRisk = assessedStatus === "watch" || assessedStatus === "at-risk";

    return (
      <div className="bg-white border border-slate-300 rounded-2xl shadow-xl overflow-hidden text-slate-900 animate-in fade-in zoom-in-95 duration-200">
        {/* Success Header */}
        <div className="bg-[#123326] p-5 text-white flex items-center gap-3">
          <div className="w-12 h-12 bg-emerald-400 text-slate-950 rounded-2xl flex items-center justify-center font-black text-xl shrink-0 shadow-md">
            ✓
          </div>
          <div>
            <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-300 font-bold block">
              DAILY HEALTH RECORD LOGGED
            </span>
            <h3 className="font-bold text-lg text-white font-mono leading-tight">
              {cattle.tagId} {cattle.name ? `· ${cattle.name}` : ""}
            </h3>
          </div>
        </div>

        <div className="p-5 space-y-5">
          {/* Green Confirmation Notice */}
          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-300 text-emerald-950 flex items-start gap-3">
            <IconCheckCircle className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div className="space-y-0.5">
              <p className="font-bold text-sm text-emerald-950">
                Daily health details saved successfully!
              </p>
              <p className="text-xs text-emerald-800">
                Data tagged with source: <code className="font-mono font-bold bg-emerald-100/80 px-1.5 py-0.5 rounded">qr_scan</code>.
                CHDI analytical engine recalculated health metrics in real-time.
              </p>
            </div>
          </div>

          {/* CHDI Instant Assessment Card */}
          <div className="card p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <IconActivity className="w-4 h-4 text-emerald-800" />
                <span className="text-xs font-mono uppercase font-bold text-slate-700">
                  Instant CHDI Health Assessment
                </span>
              </div>
              <span className={`badge-${assessedStatus} text-xs py-1 px-3 font-bold`}>
                {assessedScore != null ? `${Math.round(assessedScore)} / 100 · ` : ""}
                {assessedBadge.label}
              </span>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              {submissionResult.chdi?.farmerText ||
                (assessedStatus === "healthy"
                  ? "All vital health indicators are normal and aligned with this animal's personalized baseline."
                  : assessedStatus === "abstain"
                  ? "Cattle is in baseline calibration phase (requires 7 days of logs)."
                  : "Advisory: Physiological departure detected from historical baseline.")}
            </p>

            {isWatchOrRisk && (
              <div className="p-3 bg-amber-50 border border-amber-300 rounded-lg text-xs text-amber-900 flex items-start gap-2.5">
                <IconShieldAlert className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold block">Veterinary Alert Generated</span>
                  A clinical triage ticket has been automatically created for veterinary review.
                </div>
              </div>
            )}
          </div>

          {/* Saved Metrics Summary Pills */}
          <div className="space-y-1.5">
            <span className="text-[11px] font-mono uppercase text-slate-500 font-bold block">
              Recorded Vitals for Today:
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs font-mono">
              {submissionResult.savedMetrics.weight !== undefined && (
                <div className="p-2 bg-white rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 block">WEIGHT</span>
                  <span className="font-bold text-slate-900">{submissionResult.savedMetrics.weight} kg</span>
                </div>
              )}
              {submissionResult.savedMetrics.feed !== undefined && (
                <div className="p-2 bg-white rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 block">FEED</span>
                  <span className="font-bold text-slate-900">{submissionResult.savedMetrics.feed} kg</span>
                </div>
              )}
              {submissionResult.savedMetrics.milk !== undefined && (
                <div className="p-2 bg-white rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 block">MILK</span>
                  <span className="font-bold text-slate-900">{submissionResult.savedMetrics.milk} L</span>
                </div>
              )}
              {submissionResult.savedMetrics.temperature !== undefined && (
                <div className="p-2 bg-white rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 block">TEMPERATURE</span>
                  <span className="font-bold text-slate-900">{submissionResult.savedMetrics.temperature}°C</span>
                </div>
              )}
            </div>
          </div>

          {/* Post-submission Navigation Actions */}
          <div className="space-y-2 pt-2 border-t border-slate-100">
            <button
              type="button"
              id="scan-next-btn"
              onClick={() => {
                setSubmissionResult(null);
                if (onScanNext) onScanNext();
              }}
              className="btn btn-primary w-full justify-center py-3 text-sm font-bold shadow-md gap-2 cursor-pointer"
            >
              <IconScan className="w-4 h-4 text-emerald-300" />
              <span>Scan Next Cattle Ear Tag →</span>
            </button>

            <div className="grid grid-cols-2 gap-2">
              <Link
                href={`/farmer/cattle/${cattleRealId}`}
                className="btn btn-secondary justify-center text-xs py-2 font-semibold text-center"
              >
                <span>View Full Profile</span>
              </Link>
              <button
                type="button"
                onClick={() => setSubmissionResult(null)}
                className="btn btn-secondary justify-center text-xs py-2 font-semibold"
              >
                <span>Log More Vitals</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ── MAIN ENTRY FORM VIEW ───────────────────────────────────────────
  return (
    <div className="bg-white border border-slate-300 rounded-2xl shadow-xl overflow-hidden text-slate-900 animate-in fade-in duration-150">
      {/* 1. Scanned Cattle Identification Banner */}
      <div className="bg-[#123326] p-4 sm:p-5 text-white flex items-center justify-between relative overflow-hidden">
        <div className="relative z-10">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-[10px] font-mono tracking-widest text-emerald-300 uppercase font-bold">
              CATTLE IDENTIFIED VIA QR
            </span>
          </div>
          <h2 className="font-black text-xl sm:text-2xl text-white font-mono leading-tight tracking-tight mt-0.5">
            {cattle.tagId}
          </h2>
          <p className="text-xs text-emerald-200/90 font-medium">
            {cattle.name ? <strong className="text-white font-bold">{cattle.name}</strong> : "Unnamed"} · {cattle.breed}
            {cattle.dob ? ` · ${calcAge(cattle.dob)}` : ""}
          </p>
        </div>

        {/* Current Health Score Pill */}
        <div className="relative z-10 text-right shrink-0">
          <span className={`badge-${latestCHDI?.status ?? "abstain"} text-xs py-1 px-2.5 font-bold block shadow-xs`}>
            {latestCHDI?.score != null ? `${Math.round(latestCHDI.score)}/100 ` : ""}{initialBadge.label}
          </span>
          <span className="text-[10px] font-mono text-emerald-300/80 block mt-1">
            {cattle.purpose ? cattle.purpose.toUpperCase() : "DAIRY"}
          </span>
        </div>
      </div>

      {/* Form Content */}
      <form onSubmit={handleSubmit} className="p-4 sm:p-6 space-y-5">
        {/* 2. Auto-Populated Identity & Timestamp Summary (Read-Only Identity) */}
        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold">
              Automatic Identity Verification
            </span>
            <span className="text-[11px] font-mono text-emerald-800 font-bold bg-emerald-100/80 px-2 py-0.5 rounded flex items-center gap-1">
              ✓ Ear Tag Matched
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
            <div>
              <label className="text-[10px] font-mono text-slate-400 uppercase block font-semibold">
                Cattle Tag ID
              </label>
              <input
                type="text"
                value={cattle.tagId}
                disabled
                className="input input-sm font-mono font-bold bg-slate-100 text-slate-700 w-full cursor-not-allowed text-xs"
              />
            </div>
            <div>
              <label className="text-[10px] font-mono text-slate-400 uppercase block font-semibold">
                Cattle Name
              </label>
              <input
                type="text"
                value={cattle.name || "—"}
                disabled
                className="input input-sm font-bold bg-slate-100 text-slate-700 w-full cursor-not-allowed text-xs"
              />
            </div>
            <div>
              <label htmlFor="log-datetime" className="text-[10px] font-mono text-slate-600 uppercase block font-semibold">
                Log Date &amp; Time *
              </label>
              <input
                id="log-datetime"
                type="datetime-local"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
                className="input input-sm font-mono text-xs w-full bg-white text-slate-900 border-slate-300 focus:border-brand-600"
              />
            </div>
          </div>
        </div>

        {/* Error notification */}
        {formError && (
          <div className="p-3 rounded-xl bg-red-50 border border-red-300 text-red-900 text-xs font-semibold flex items-center gap-2">
            <IconShieldAlert className="w-4 h-4 text-red-600 shrink-0" />
            <span>{formError}</span>
          </div>
        )}

        {/* 3. Core Daily Health Vitals Entry Grid */}
        <div>
          <div className="mb-2.5">
            <h3 className="font-bold text-sm text-slate-900">
              Daily Health Measurements
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            {/* Field 1: Body Weight */}
            <div className="p-3 bg-white border border-slate-300 rounded-xl space-y-1.5 focus-within:border-brand-600 focus-within:ring-1 focus-within:ring-brand-500">
              <label htmlFor="weight-input" className="text-xs font-bold text-slate-900 block">
                Body Weight (kg)
              </label>
              <div className="relative">
                <input
                  id="weight-input"
                  type="number"
                  step="0.1"
                  min="1"
                  max="1500"
                  placeholder="e.g. 350.0"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  disabled={submitting}
                  className="input input-sm w-full font-mono text-sm pr-10 text-slate-900"
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-mono text-slate-400">
                  kg
                </span>
              </div>
              <p className="text-[10px] text-slate-500">Liveweight scale or girth tape estimate</p>
            </div>

            {/* Field 2: Feed Intake */}
            <div className="p-3 bg-white border border-slate-300 rounded-xl space-y-1.5 focus-within:border-brand-600 focus-within:ring-1 focus-within:ring-brand-500">
              <label htmlFor="feed-input" className="text-xs font-bold text-slate-900 block">
                Feed Intake (kg)
              </label>
              <div className="relative">
                <input
                  id="feed-input"
                  type="number"
                  step="0.1"
                  min="0"
                  max="150"
                  placeholder="e.g. 12.5"
                  value={feedQuantity}
                  onChange={(e) => setFeedQuantity(e.target.value)}
                  disabled={submitting}
                  className="input input-sm w-full font-mono text-sm pr-10 text-slate-900"
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-mono text-slate-400">
                  kg
                </span>
              </div>
              <select
                value={feedType}
                onChange={(e) => setFeedType(e.target.value)}
                disabled={submitting}
                className="input input-sm text-[11px] w-full bg-slate-50 text-slate-700 py-1"
              >
                <option value="Mixed Green Grass / Fodder">Mixed Green Grass / Fodder</option>
                <option value="Dry Fodder / Hay / Straw">Dry Fodder / Hay / Straw</option>
                <option value="Concentrate Feed Mash">Concentrate Feed Mash</option>
                <option value="Silage / Fermented Feed">Silage / Fermented Feed</option>
              </select>
            </div>

            {/* Field 3: Milk Production */}
            <div className="p-3 bg-white border border-slate-300 rounded-xl space-y-1.5 focus-within:border-brand-600 focus-within:ring-1 focus-within:ring-brand-500">
              <label htmlFor="milk-input" className="text-xs font-bold text-slate-900 block">
                Daily Milk Yield (Litres)
              </label>
              <div className="relative">
                <input
                  id="milk-input"
                  type="number"
                  step="0.1"
                  min="0"
                  max="100"
                  placeholder="e.g. 14.0"
                  value={milkLitres}
                  onChange={(e) => setMilkLitres(e.target.value)}
                  disabled={submitting}
                  className="input input-sm w-full font-mono text-sm pr-10 text-slate-900"
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-mono text-slate-400">
                  L/day
                </span>
              </div>
              <p className="text-[10px] text-slate-500">
                Total morning + evening yield (leave blank if dry or non-dairy)
              </p>
            </div>

            {/* Field 4: Body Temperature */}
            <div className="p-3 bg-white border border-slate-300 rounded-xl space-y-1.5 focus-within:border-brand-600 focus-within:ring-1 focus-within:ring-brand-500">
              <label htmlFor="temp-input" className="text-xs font-bold text-slate-900 block">
                Body Temperature (°C)
              </label>
              <div className="relative">
                <input
                  id="temp-input"
                  type="number"
                  step="0.1"
                  min="30"
                  max="45"
                  placeholder="e.g. 38.6"
                  value={temperature}
                  onChange={(e) => setTemperature(e.target.value)}
                  disabled={submitting}
                  className="input input-sm w-full font-mono text-sm pr-10 text-slate-900"
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-mono text-slate-400">
                  °C
                </span>
              </div>
              <p className="text-[10px] text-emerald-800 font-medium">
                Normal bovine range: 38.0°C – 39.3°C (Pyrexia: &gt;39.5°C)
              </p>
            </div>
          </div>
        </div>

        {/* 5. Submit & Action Buttons */}
        <div className="space-y-2 pt-2 border-t border-slate-200">
          <button
            type="submit"
            id="submit-daily-health-btn"
            disabled={submitting}
            className="btn btn-primary w-full justify-center py-3.5 text-sm font-bold shadow-md gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Saving Health Details &amp; Calculating CHDI...</span>
              </>
            ) : (
              <>
                <IconCheckCircle className="w-4 h-4 text-emerald-300" />
                <span>Save Daily Health Record &amp; Update CHDI</span>
              </>
            )}
          </button>

          <div className="flex gap-2">
            {onScanNext && (
              <button
                type="button"
                onClick={onScanNext}
                disabled={submitting}
                className="btn btn-secondary flex-1 justify-center py-2 text-xs font-semibold text-slate-700"
              >
                Scan Another Tag
              </button>
            )}
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                disabled={submitting}
                className="btn btn-secondary flex-1 justify-center py-2 text-xs font-semibold text-slate-700"
              >
                Cancel
              </button>
            )}
            <Link
              href={`/farmer/cattle/${cattleRealId}`}
              className="btn btn-secondary flex-1 justify-center py-2 text-xs font-semibold text-slate-700 text-center"
            >
              Full Profile
            </Link>
          </div>
        </div>
      </form>
    </div>
  );
}


"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { IconScan, IconCow, IconActivity, IconSyringe } from "@/components/icons";
import DailyHealthLogForm, { type CattleProfileData } from "@/components/DailyHealthLogForm";

declare global {
  interface Window {
    Html5Qrcode: {
      new(id: string): {
        start: (constraint: object, config: object, callback: (text: string) => void, error: (err: unknown) => void) => Promise<void>;
        stop: () => Promise<void>;
        clear?: () => void;
        isScanning?: boolean;
        getState?: () => number;
      };
    };
  }
}

export default function ScanQRPage() {
  const router = useRouter();
  const [scanning, setScanning] = useState(false);
  const [scannedCattle, setScannedCattle] = useState<CattleProfileData | null>(null);
  const [error, setError] = useState("");
  const scannerRef = useRef<{
    start: (constraint: object, config: object, callback: (text: string) => void, error: (err: unknown) => void) => Promise<void>;
    stop: () => Promise<void>;
    clear?: () => void;
    isScanning?: boolean;
    getState?: () => number;
  } | null>(null);

  // Play pleasant chime on successful scan
  const playSuccessSound = useCallback(() => {
    try {
      if (typeof window !== "undefined" && window.AudioContext) {
        const ctx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.15); // A5
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.25);
      }
      if (typeof navigator !== "undefined" && navigator.vibrate) {
        navigator.vibrate([80, 40, 80]);
      }
    } catch {
      // AudioContext unavailable or blocked
    }
  }, []);

  // Safely stop and cleanup scanner
  const safeStopScanner = useCallback(async () => {
    const scanner = scannerRef.current;
    if (!scanner) {
      setScanning(false);
      return;
    }

    try {
      if (scanner.isScanning) {
        await scanner.stop();
      }
    } catch (err: unknown) {
      console.warn("Handled scanner stop warning:", err);
    } finally {
      try {
        if (typeof scanner.clear === "function") {
          scanner.clear();
        }
      } catch {}
      scannerRef.current = null;
      setScanning(false);
    }
  }, []);

  useEffect(() => {
    // Load html5-qrcode dynamically
    const script = document.createElement("script");
    script.src = "https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js";
    script.async = true;
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
      const scanner = scannerRef.current;
      if (scanner) {
        try {
          if (scanner.isScanning) {
            scanner.stop().catch(() => {});
          }
        } catch {}
        scannerRef.current = null;
      }
    };
  }, []);

  const handleDecodedToken = useCallback(async (tokenOrUrl: string) => {
    try {
      const tokenMatch = tokenOrUrl.match(/\/scan\/([^/?]+)/);
      const token = tokenMatch?.[1] ?? tokenOrUrl.trim();

      const res = await fetch(`/api/scan/${encodeURIComponent(token)}`);
      if (res.ok) {
        const data = await res.json();
        playSuccessSound();
        setScannedCattle({
          ...data.cattle,
          cattleId: data.cattleId ?? data.cattle.id,
        });
        setError("");
      } else {
        setError("QR code was scanned, but this ear tag is not registered in the system.");
      }
    } catch {
      setError("Network connection error while looking up cattle tag.");
    }
  }, [playSuccessSound]);

  const startScan = async () => {
    setError("");
    setScannedCattle(null);

    await safeStopScanner();
    setScanning(true);

    setTimeout(async () => {
      try {
        if (!window.Html5Qrcode) {
          setError("Initializing scanner camera. Please click again in 2 seconds.");
          setScanning(false);
          return;
        }

        const scanner = new window.Html5Qrcode("qr-reader");
        scannerRef.current = scanner;
        await scanner.start(
          { facingMode: "environment" },
          { fps: 15, qrbox: { width: 280, height: 280 } },
          async (decodedText: string) => {
            await safeStopScanner();
            await handleDecodedToken(decodedText);
          },
          () => {}
        );
      } catch (e: unknown) {
        console.warn("Scanner start error:", e);
        await safeStopScanner();
        setError("Camera permission was denied or no camera device was found.");
      }
    }, 300);
  };

  const stopScan = async () => {
    await safeStopScanner();
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-2xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="pb-4 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              Scan Ear Tag QR
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Instant livestock identification &amp; direct daily health logging
            </p>
          </div>
          <span className="text-[10px] font-mono font-bold px-2 py-0.5 bg-emerald-100 text-emerald-900 border border-emerald-300 rounded shrink-0">
            QR WORKFLOW
          </span>
        </div>
      </div>

      {/* ── CONDITIONAL VIEW: DAILY HEALTH LOGGING FORM ON SCANNED CATTLE ── */}
      {scannedCattle ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between pb-1">
            <span className="text-xs font-mono font-bold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200 flex items-center gap-1.5 shadow-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
              <span>Ear Tag Verified &bull; Daily Health Logging Active</span>
            </span>

            <button
              type="button"
              onClick={() => {
                setScannedCattle(null);
                startScan();
              }}
              className="btn btn-secondary btn-sm text-xs font-semibold gap-1.5 cursor-pointer"
            >
              <IconScan className="w-3.5 h-3.5 text-slate-500" />
              <span>Scan Another Tag</span>
            </button>
          </div>

          <DailyHealthLogForm
            cattle={scannedCattle}
            onScanNext={() => {
              setScannedCattle(null);
              startScan();
            }}
            onCancel={() => {
              setScannedCattle(null);
            }}
          />
        </div>
      ) : (
        <div className="space-y-6">
          {/* Camera Live Viewfinder Card */}
          <div className="card p-5 bg-white border border-slate-300 shadow-xs space-y-4">
            <div
              id="qr-reader"
              className={`w-full rounded-xl overflow-hidden bg-slate-950 border border-slate-800 ${scanning ? "" : "hidden"}`}
              style={{ minHeight: "320px" }}
            />

            {!scanning && (
              <div className="flex flex-col items-center justify-center py-10 text-center space-y-4">
                <div className="w-16 h-16 bg-emerald-50 border border-emerald-200 rounded-2xl flex items-center justify-center text-[#123326] shadow-xs">
                  <IconScan className="w-9 h-9" />
                </div>
                <div>
                  <p className="text-base font-bold text-slate-900">Live Ear Tag Scanner</p>
                  <p className="text-xs text-slate-500 max-w-xs mt-0.5">
                    Point your camera at the cattle ear tag. Instantly retrieves digital profile and opens daily health log form.
                  </p>
                </div>
                <button
                  id="start-scan-btn"
                  onClick={startScan}
                  className="btn btn-primary btn-lg font-bold text-xs shadow-md gap-2 px-6 cursor-pointer"
                >
                  <IconScan className="w-4 h-4 text-emerald-300" />
                  <span>Start Camera Scanner →</span>
                </button>
              </div>
            )}

            {scanning && (
              <div className="flex items-center justify-between pt-2">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
                  <span className="text-xs font-mono text-slate-700 font-bold">SCANNER ACTIVE • ALIGN QR IN BOX</span>
                </div>
                <button onClick={stopScan} className="btn btn-secondary btn-sm text-xs font-semibold cursor-pointer">
                  Stop Camera
                </button>
              </div>
            )}
          </div>

          {error && (
            <div className="card p-4 bg-red-50 border border-red-300 text-red-800 text-xs flex items-center justify-between gap-3">
              <p className="font-semibold">{error}</p>
              <button onClick={startScan} className="btn btn-secondary btn-sm text-xs font-bold text-red-900 shrink-0">
                Retry Scan
              </button>
            </div>
          )}

          {/* Manual Tag Override Input */}
          <div className="card p-4 bg-[#f8faf9] border border-slate-200 space-y-2">
            <label htmlFor="manual-tag-input" className="label text-slate-700 font-bold text-xs">
              Or Enter Tag ID / Cow Name Manually
            </label>
            <ManualLookup
              onFound={(cattle) => {
                playSuccessSound();
                setScannedCattle(cattle);
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function ManualLookup({ onFound }: { onFound: (cattle: CattleProfileData) => void }) {
  const [tagId, setTagId] = useState("");
  const [searching, setSearching] = useState(false);
  const [notFound, setNotFound] = useState(false);

  return (
    <div>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          if (!tagId.trim()) return;
          setSearching(true);
          setNotFound(false);

          try {
            // First try direct lookup by tag or token via /api/scan/[token]
            const scanRes = await fetch(`/api/scan/${encodeURIComponent(tagId.trim())}`);
            if (scanRes.ok) {
              const data = await scanRes.json();
              onFound({ ...data.cattle, cattleId: data.cattleId ?? data.cattle.id });
              return;
            }

            // Fallback: search farmer cattle list
            const res = await fetch(`/api/farmer/cattle`);
            if (res.ok) {
              const { cattle } = await res.json();
              const match = cattle.find(
                (c: { tagId: string; id: string; name: string }) =>
                  c.tagId.toLowerCase() === tagId.trim().toLowerCase() ||
                  (c.name && c.name.toLowerCase() === tagId.trim().toLowerCase())
              );
              if (match) {
                const fullRes = await fetch(`/api/scan/${match.qrToken ?? match.id}`);
                if (fullRes.ok) {
                  const data = await fullRes.json();
                  onFound({ ...data.cattle, cattleId: data.cattleId ?? match.id });
                } else {
                  onFound({ ...match, cattleId: match.id });
                }
                return;
              }
            }
            setNotFound(true);
          } catch {
            setNotFound(true);
          } finally {
            setSearching(false);
          }
        }}
        className="flex gap-2"
      >
        <input
          id="manual-tag-input"
          type="text"
          className="input font-mono flex-1 text-xs"
          placeholder="e.g. TN-SC-4891 or Lakshmi"
          value={tagId}
          onChange={(e) => {
            setTagId(e.target.value);
            setNotFound(false);
          }}
        />
        <button
          type="submit"
          className="btn btn-secondary btn-sm text-xs font-semibold px-4 cursor-pointer"
          disabled={searching}
        >
          {searching ? "Searching..." : "Lookup & Log"}
        </button>
      </form>
      {notFound && (
        <p className="text-[11px] text-red-600 mt-1.5 font-medium">
          No cattle found with tag or name &quot;{tagId}&quot;. Please check the number.
        </p>
      )}
    </div>
  );
}

"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { IconScan, IconCow } from "@/components/icons";

declare global {
  interface Window {
    Html5Qrcode: {
      new(id: string): {
        start: (constraint: object, config: object, callback: (text: string) => void, error: (err: unknown) => void) => Promise<void>;
        stop: () => Promise<void>;
      };
    };
  }
}

export default function ScanQRPage() {
  const router = useRouter();
  const [scanning, setScanning] = useState(false);
  const [, setResult] = useState<string | null>(null);
  const [cattleInfo, setCattleInfo] = useState<{ tagId: string; breed: string; cattleId: string } | null>(null);
  const [error, setError] = useState("");
  const scannerRef = useRef<{ stop: () => Promise<void> } | null>(null);

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
    };
  }, []);

  const startScan = async () => {
    setError("");
    setResult(null);
    setCattleInfo(null);
    setScanning(true);

    setTimeout(async () => {
      try {
        if (!window.Html5Qrcode) {
          setError("Starting scanner camera. Please try again in a moment.");
          setScanning(false);
          return;
        }

        const scanner = new window.Html5Qrcode("qr-reader");
        scannerRef.current = scanner;
        await scanner.start(
          { facingMode: "environment" },
          { fps: 12, qrbox: { width: 260, height: 260 } },
          async (decodedText: string) => {
            await scanner.stop().catch(() => {});
            scannerRef.current = null;
            setScanning(false);
            setResult(decodedText);

            const tokenMatch = decodedText.match(/\/scan\/([^/?]+)/);
            const token = tokenMatch?.[1] ?? decodedText;

            const res = await fetch(`/api/scan/${token}`);
            if (res.ok) {
              const data = await res.json();
              setCattleInfo({ ...data.cattle, cattleId: data.cattleId });
            } else {
              setError("This QR code was not found in your farm cattle list.");
            }
          },
          () => {}
        );
      } catch {
        setScanning(false);
        setError("Camera permission denied or camera not found on device.");
      }
    }, 400);
  };

  const stopScan = async () => {
    if (scannerRef.current) {
      await scannerRef.current.stop().catch(() => {});
      scannerRef.current = null;
    }
    setScanning(false);
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="pb-4 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
            Scan Ear Tag QR
          </h1>
          <span className="text-[10px] font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
            CAMERA SCAN
          </span>
        </div>
        <p className="text-xs text-slate-500 mt-0.5">
          Point your mobile camera at the cow&apos;s ear tag QR code to view its health and log daily records.
        </p>
      </div>

      {/* Scanner Terminal Card */}
      <div className="card p-5 bg-white border border-slate-300 shadow-xs space-y-4">
        <div
          id="qr-reader"
          className={`w-full rounded-lg overflow-hidden bg-slate-950 border border-slate-800 ${scanning ? "" : "hidden"}`}
          style={{ minHeight: "300px" }}
        />

        {!scanning && !cattleInfo && (
          <div className="flex flex-col items-center justify-center py-10 text-center space-y-4">
            <div className="w-14 h-14 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-center text-[#123326]">
              <IconScan className="w-8 h-8" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-900">Open Camera Scanner</p>
              <p className="text-xs text-slate-500 max-w-xs mt-0.5">
                Hold phone steady near the ear tag. Works on any smartphone camera.
              </p>
            </div>
            <button
              id="start-scan-btn"
              onClick={startScan}
              className="btn btn-primary btn-lg font-bold text-xs"
            >
              Start Camera Scanner →
            </button>
          </div>
        )}

        {scanning && (
          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
              <span className="text-xs font-mono text-slate-600 font-bold">CAMERA ACTIVE</span>
            </div>
            <button onClick={stopScan} className="btn btn-secondary btn-sm text-xs font-semibold">
              Stop Camera
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="card p-4 bg-red-50 border border-red-300 text-red-800 text-xs">
          <p className="font-bold">{error}</p>
          <button onClick={startScan} className="mt-2 text-xs font-bold text-red-900 underline">
            Try again
          </button>
        </div>
      )}

      {/* Scanned Tag Result Card */}
      {cattleInfo && (
        <div className="card p-5 bg-white border border-emerald-300 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-[#123326] text-emerald-300 rounded-lg flex items-center justify-center font-mono font-bold text-sm">
                {cattleInfo.tagId.slice(-4)}
              </div>
              <div>
                <span className="text-[10px] font-mono font-bold uppercase text-emerald-800 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                  COW FOUND
                </span>
                <h3 className="font-bold text-slate-900 text-base font-mono">{cattleInfo.tagId}</h3>
                <p className="text-xs text-slate-500">{cattleInfo.breed}</p>
              </div>
            </div>
          </div>

          <div className="flex gap-2.5 pt-1">
            <button onClick={startScan} className="btn btn-secondary btn-sm flex-1 text-xs">
              Scan Another Cow
            </button>
            <button
              onClick={() => router.push(`/farmer/cattle/${cattleInfo.cattleId}`)}
              className="btn btn-primary btn-sm flex-1 text-xs font-bold"
            >
              Open Cow Details →
            </button>
          </div>
        </div>
      )}

      {/* Manual Tag Override */}
      <div className="card p-4 bg-[#f8faf9] border border-slate-200 space-y-2">
        <label htmlFor="manual-tag-input" className="label text-slate-700">
          Or Enter Tag ID Manually
        </label>
        <ManualLookup />
      </div>
    </div>
  );
}

function ManualLookup() {
  const router = useRouter();
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
            const res = await fetch(`/api/farmer/cattle`);
            if (res.ok) {
              const { cattle } = await res.json();
              const match = cattle.find(
                (c: { tagId: string; id: string; name: string }) =>
                  c.tagId.toLowerCase() === tagId.trim().toLowerCase() ||
                  (c.name && c.name.toLowerCase() === tagId.trim().toLowerCase())
              );
              if (match) {
                router.push(`/farmer/cattle/${match.id}`);
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
          className="btn btn-secondary btn-sm text-xs font-semibold px-4"
          disabled={searching}
        >
          {searching ? "Searching..." : "Search"}
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

"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";

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
  const [result, setResult] = useState<string | null>(null);
  const [cattleInfo, setCattleInfo] = useState<{ tagId: string; breed: string; cattleId: string } | null>(null);
  const [error, setError] = useState("");
  const scannerRef = useRef<{ stop: () => Promise<void> } | null>(null);

  useEffect(() => {
    // Load html5-qrcode dynamically
    const script = document.createElement("script");
    script.src = "https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js";
    script.async = true;
    document.body.appendChild(script);
    return () => { document.body.removeChild(script); };
  }, []);

  const startScan = async () => {
    setError("");
    setResult(null);
    setCattleInfo(null);
    setScanning(true);

    setTimeout(async () => {
      try {
        const scanner = new window.Html5Qrcode("qr-reader");
        scannerRef.current = scanner;
        await scanner.start(
          { facingMode: "environment" },
          { fps: 10, qrbox: { width: 250, height: 250 } },
          async (decodedText: string) => {
            // Stop scanner
            await scanner.stop().catch(() => {});
            scannerRef.current = null;
            setScanning(false);
            setResult(decodedText);

            // Extract token from URL (expected: https://app.com/scan/TOKEN)
            const tokenMatch = decodedText.match(/\/scan\/([^/?]+)/);
            const token = tokenMatch?.[1] ?? decodedText;

            // Resolve token via API
            const res = await fetch(`/api/scan/${token}`);
            if (res.ok) {
              const data = await res.json();
              setCattleInfo({ ...data.cattle, cattleId: data.cattleId });
            } else {
              setError("QR code not recognized. Please try again.");
            }
          },
          () => {} // ignore scan errors
        );
      } catch (e) {
        setScanning(false);
        setError("Camera access denied or not available.");
      }
    }, 500);
  };

  const stopScan = async () => {
    if (scannerRef.current) {
      await scannerRef.current.stop().catch(() => {});
      scannerRef.current = null;
    }
    setScanning(false);
  };

  return (
    <div className="p-8 max-w-xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Scan QR Tag</h1>
        <p className="text-slate-500 mt-1">Point your camera at the animal's QR tag to view its health profile</p>
      </div>

      {/* Scanner area */}
      <div className="card p-6 mb-6">
        <div
          id="qr-reader"
          className={`w-full rounded-2xl overflow-hidden bg-slate-900 ${scanning ? "" : "hidden"}`}
          style={{ minHeight: "300px" }}
        />

        {!scanning && !cattleInfo && (
          <div className="flex flex-col items-center py-12">
            <div className="w-16 h-16 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-700 font-bold text-xl mb-4">
              QR
            </div>
            <p className="text-slate-500 mb-6 text-center">Tap the button below to activate your camera and scan an animal's QR tag</p>
            <button id="start-scan-btn" onClick={startScan} className="btn-primary btn-lg">
              Start Camera
            </button>
          </div>
        )}

        {scanning && (
          <div className="mt-4 text-center">
            <p className="text-slate-500 text-sm mb-3 animate-pulse">Scanning... point camera at QR tag</p>
            <button onClick={stopScan} className="btn-secondary">Stop</button>
          </div>
        )}
      </div>

      {error && (
        <div className="card p-4 bg-red-50 border-red-200 text-red-700 text-sm">
          {error}
          <button onClick={startScan} className="block mt-2 text-red-600 font-medium underline">Try again</button>
        </div>
      )}

      {cattleInfo && (
        <div className="card p-6 animate-fade-in-up">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 bg-brand-100 rounded-2xl flex items-center justify-center font-bold text-brand-700 text-lg">
              {cattleInfo.tagId[0]}
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-lg">{cattleInfo.tagId}</h3>
              <p className="text-slate-500 text-sm">{cattleInfo.breed}</p>
            </div>
          </div>
          <p className="text-emerald-600 text-sm mb-4">QR scan logged successfully</p>
          <div className="flex gap-3">
            <button onClick={startScan} className="btn-secondary flex-1">Scan another</button>
            <button
              onClick={() => router.push(`/farmer/cattle/${cattleInfo.cattleId}`)}
              className="btn-primary flex-1"
            >
              View Profile →
            </button>
          </div>
        </div>
      )}

      {/* Manual tag lookup */}
      <div className="card p-5 mt-6">
        <p className="text-sm text-slate-600 mb-3">Or enter tag ID manually:</p>
        <ManualLookup />
      </div>
    </div>
  );
}

function ManualLookup() {
  const router = useRouter();
  const [tagId, setTagId] = useState("");

  return (
    <form
      onSubmit={async (e) => {
        e.preventDefault();
        // Try to look up by tagId
        const res = await fetch(`/api/farmer/cattle`);
        if (res.ok) {
          const { cattle } = await res.json();
          const match = cattle.find((c: { tagId: string; id: string }) => c.tagId === tagId);
          if (match) router.push(`/farmer/cattle/${match.id}`);
        }
      }}
      className="flex gap-2"
    >
      <input
        id="manual-tag-input"
        type="text"
        className="input flex-1"
        placeholder="e.g. SC-001"
        value={tagId}
        onChange={(e) => setTagId(e.target.value)}
      />
      <button type="submit" className="btn-primary">Search</button>
    </form>
  );
}

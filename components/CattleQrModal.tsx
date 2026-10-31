"use client";

import React, { useState, useEffect, useRef } from "react";
import QRCode from "qrcode";
import { IconQrCode, IconDownload, IconPrinter } from "@/components/icons";

interface CattleQrModalProps {
  cattle: {
    id: string;
    tagId: string;
    name?: string | null;
    breed: string;
    qrToken: string;
    gender?: string | null;
    dob?: string | Date | null;
  };
  variant?: "icon" | "button" | "pill";
  className?: string;
}

export default function CattleQrModal({
  cattle,
  variant = "icon",
  className = "",
}: CattleQrModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [qrDataUrl, setQrDataUrl] = useState<string>("");
  const [copied, setCopied] = useState(false);
  const printRef = useRef<HTMLDivElement>(null);

  const scanUrl =
    typeof window !== "undefined"
      ? `${window.location.origin}/scan/${cattle.qrToken}`
      : `/scan/${cattle.qrToken}`;

  useEffect(() => {
    if (isOpen || variant === "button") {
      QRCode.toDataURL(scanUrl, {
        width: 320,
        margin: 2,
        color: {
          dark: "#0b2219",
          light: "#ffffff",
        },
      })
        .then((url) => setQrDataUrl(url))
        .catch((err) => console.error("Error generating QR code:", err));
    }
  }, [isOpen, scanUrl, variant]);

  // Generate high-resolution composite Ear Tag PNG
  const downloadEarTag = async () => {
    try {
      const qrImage = new Image();
      qrImage.crossOrigin = "anonymous";
      qrImage.src = qrDataUrl;

      await new Promise((resolve) => {
        qrImage.onload = resolve;
      });

      const canvas = document.createElement("canvas");
      canvas.width = 640;
      canvas.height = 800;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      // Background
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Outer Rounded Border
      ctx.strokeStyle = "#cbd5e1";
      ctx.lineWidth = 4;
      ctx.strokeRect(20, 20, canvas.width - 40, canvas.height - 40);

      // Top Tag Hole Ring
      ctx.fillStyle = "#f1f5f9";
      ctx.beginPath();
      ctx.arc(canvas.width / 2, 55, 18, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 3;
      ctx.stroke();

      // Top Brand Header Banner
      ctx.fillStyle = "#123326";
      ctx.fillRect(40, 95, canvas.width - 80, 110);

      // Header Text
      ctx.fillStyle = "#6ee7b7";
      ctx.font = "bold 15px 'Courier New', monospace";
      ctx.textAlign = "center";
      ctx.fillText("SMARTCATTLE • LIVESTOCK PASSPORT", canvas.width / 2, 130);

      ctx.fillStyle = "#ffffff";
      ctx.font = "900 32px 'Courier New', monospace";
      ctx.fillText(cattle.tagId, canvas.width / 2, 175);

      // Cow Name & Breed
      ctx.fillStyle = "#0f172a";
      ctx.font = "bold 24px sans-serif";
      const displayName = cattle.name ? `${cattle.name}` : cattle.tagId;
      ctx.fillText(displayName, canvas.width / 2, 245);

      ctx.fillStyle = "#64748b";
      ctx.font = "16px sans-serif";
      ctx.fillText(cattle.breed, canvas.width / 2, 275);

      // Draw QR Code
      const qrSize = 340;
      const qrX = (canvas.width - qrSize) / 2;
      const qrY = 305;

      // QR Container border
      ctx.fillStyle = "#f8fafc";
      ctx.fillRect(qrX - 10, qrY - 10, qrSize + 20, qrSize + 20);
      ctx.strokeStyle = "#e2e8f0";
      ctx.lineWidth = 2;
      ctx.strokeRect(qrX - 10, qrY - 10, qrSize + 20, qrSize + 20);

      ctx.drawImage(qrImage, qrX, qrY, qrSize, qrSize);

      // Scan Instructions
      ctx.fillStyle = "#334155";
      ctx.font = "bold 15px sans-serif";
      ctx.fillText("SCAN TO VERIFY CHDI HEALTH & VACCINES", canvas.width / 2, 690);

      // Footer
      ctx.fillStyle = "#94a3b8";
      ctx.font = "12px 'Courier New', monospace";
      ctx.fillText("IEEE CHDI ENGINE • PROVENANCE VERIFIED", canvas.width / 2, 730);

      // Trigger Download
      const link = document.createElement("a");
      link.download = `${cattle.tagId}-Ear-Tag.png`;
      link.href = canvas.toDataURL("image/png");
      link.click();
    } catch (e) {
      console.error("Failed to generate tag download", e);
    }
  };

  const downloadBareQr = () => {
    if (!qrDataUrl) return;
    const link = document.createElement("a");
    link.download = `${cattle.tagId}-QR.png`;
    link.href = qrDataUrl;
    link.click();
  };

  const handlePrint = () => {
    window.print();
  };

  const copyScanLink = () => {
    navigator.clipboard.writeText(scanUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <>
      {/* Trigger button */}
      {variant === "icon" ? (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            setIsOpen(true);
          }}
          className={`p-1.5 text-slate-500 hover:text-emerald-900 rounded hover:bg-emerald-50 transition-colors cursor-pointer ${className}`}
          title="Download & Print QR Ear Tag"
          aria-label={`Download QR tag for ${cattle.tagId}`}
        >
          <IconQrCode className="w-3.5 h-3.5" />
        </button>
      ) : variant === "pill" ? (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            setIsOpen(true);
          }}
          className={`inline-flex items-center gap-1 text-[11px] font-mono font-bold text-emerald-900 hover:text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-2 py-0.5 rounded transition-all cursor-pointer ${className}`}
          title="Download QR Tag"
        >
          <IconQrCode className="w-3 h-3" />
          <span>QR Tag</span>
        </button>
      ) : (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            setIsOpen(true);
          }}
          className={`btn btn-secondary btn-sm inline-flex items-center gap-1.5 font-mono text-xs font-semibold ${className}`}
        >
          <IconQrCode className="w-4 h-4 text-emerald-800" />
          <span>QR Ear Tag</span>
        </button>
      )}

      {/* Modal Dialog */}
      {isOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-150"
          onClick={() => setIsOpen(false)}
        >
          <div
            className="bg-white border border-slate-300 rounded-2xl shadow-2xl max-w-md w-full overflow-hidden text-slate-900 animate-in zoom-in-95 duration-150"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 border-b border-slate-100 bg-[#f8faf9]">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-[#123326] text-emerald-300 flex items-center justify-center font-mono font-bold text-xs">
                  QR
                </div>
                <div>
                  <h3 className="font-bold text-sm text-slate-950 font-display">
                    Cattle Ear Tag &amp; QR
                  </h3>
                  <p className="text-[11px] text-slate-500 font-mono">
                    {cattle.tagId} {cattle.name ? `(${cattle.name})` : ""}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 flex items-center justify-center text-sm font-bold transition-colors cursor-pointer"
              >
                ✕
              </button>
            </div>

            {/* Modal Body: Printable Ear Tag Preview */}
            <div className="p-6 text-center space-y-4">
              <div
                ref={printRef}
                className="bg-white p-5 rounded-xl border-2 border-dashed border-emerald-800/30 max-w-[280px] mx-auto shadow-xs space-y-3"
              >
                {/* Ear Tag Header */}
                <div className="bg-[#123326] text-white py-2 px-3 rounded-lg shadow-xs">
                  <span className="text-[10px] uppercase font-mono tracking-widest text-emerald-300 block">
                    EAR TAG ID
                  </span>
                  <span className="text-base font-black font-mono tracking-tight text-white block">
                    {cattle.tagId}
                  </span>
                </div>

                {/* QR Image */}
                <div className="bg-white p-2 border border-slate-200 rounded-lg flex items-center justify-center">
                  {qrDataUrl ? (
                    /* eslint-disable-next-line @next/next/no-img-element */
                    <img
                      src={qrDataUrl}
                      alt={`QR for ${cattle.tagId}`}
                      className="w-44 h-44 object-contain mx-auto"
                    />
                  ) : (
                    <div className="w-44 h-44 bg-slate-100 animate-pulse rounded flex items-center justify-center text-xs text-slate-400">
                      Generating QR...
                    </div>
                  )}
                </div>

                {/* Cow details */}
                <div>
                  <h4 className="font-bold text-slate-900 text-sm">
                    {cattle.name ? cattle.name : cattle.tagId}
                  </h4>
                  <p className="text-[11px] text-slate-500 font-medium">
                    {cattle.breed}
                  </p>
                </div>
              </div>

              <p className="text-xs text-slate-500 max-w-xs mx-auto">
                Stick this QR code on ear tags, barn gates, or logbooks. Scan with
                any smartphone camera to instantly view health and milk history.
              </p>
            </div>

            {/* Modal Footer Actions */}
            <div className="p-4 border-t border-slate-100 bg-slate-50 flex flex-col sm:flex-row items-center gap-2">
              <button
                type="button"
                onClick={downloadEarTag}
                className="btn btn-primary w-full sm:flex-1 justify-center py-2 text-xs font-bold gap-1.5 cursor-pointer"
              >
                <IconDownload className="w-4 h-4" />
                <span>Download Ear Tag</span>
              </button>

              <button
                type="button"
                onClick={downloadBareQr}
                className="btn btn-secondary w-full sm:w-auto justify-center py-2 text-xs font-semibold gap-1 cursor-pointer"
                title="Download QR code only (without badge frame)"
              >
                <span>Raw QR</span>
              </button>

              <button
                type="button"
                onClick={copyScanLink}
                className="btn btn-secondary w-full sm:w-auto justify-center py-2 text-xs font-semibold gap-1 cursor-pointer"
              >
                <span>{copied ? "✓ Copied!" : "Copy Link"}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

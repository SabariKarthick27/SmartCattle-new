"use client";

import { useState } from "react";
import { IconSyringe, IconCalendar } from "@/components/icons";

interface CattleOption {
  id: string;
  tagId: string;
  name: string | null;
  breed: string;
  farmer: { name: string };
}

interface RecordItem {
  id: string;
  cattleTagId: string;
  cattleName: string | null;
  breed: string;
  farmerName: string;
  farmerPhone: string;
  vaccineType: string;
  dueAt: string;
  administeredAt: string | null;
  status: string;
  notes: string | null;
}

interface Props {
  cattleList: CattleOption[];
  initialRecords: RecordItem[];
  vetRegion?: string | null;
}

const COMMON_VACCINES = [
  "Routine Health Checkup",
  "FMD - Foot & Mouth Disease",
  "HS - Haemorrhagic Septicaemia",
  "BQ - Black Quarter",
  "Brucellosis Vaccination",
  "Anthrax Spore Vaccine",
  "Deworming & Parasite Control",
  "Mastitis Check & Teat Care",
  "Follow-up Health Audit",
];

export default function VetVaccinationsClient({ cattleList, initialRecords, vetRegion }: Props) {
  const [records, setRecords] = useState<RecordItem[]>(initialRecords);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] = useState({
    cattleId: "",
    vaccineType: "Routine Health Checkup",
    customType: "",
    dueAt: new Date().toISOString().split("T")[0],
    notes: "",
  });

  const handleSchedule = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    const selectedType = form.vaccineType === "Other" ? form.customType : form.vaccineType;

    const res = await fetch("/api/vet/vaccinations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cattleId: form.cattleId,
        vaccineType: selectedType,
        dueAt: form.dueAt,
        notes: form.notes,
      }),
    });

    const data = await res.json();
    setLoading(false);

    if (!res.ok) {
      setError(data.error || "Failed to schedule vaccination");
      return;
    }

    setSuccess("Vaccination / Checkup date scheduled successfully!");
    setShowModal(false);
    window.location.reload();
  };

  const handleToggleStatus = async (id: string, currentStatus: string) => {
    const newStatus = currentStatus === "done" ? "upcoming" : "done";
    const res = await fetch("/api/vet/vaccinations", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, status: newStatus }),
    });

    if (res.ok) {
      setRecords((prev) =>
        prev.map((r) =>
          r.id === id
            ? {
                ...r,
                status: newStatus,
                administeredAt: newStatus === "done" ? new Date().toISOString().split("T")[0] : null,
              }
            : r
        )
      );
    }
  };

  return (
    <div className="space-y-6">
      <div className="pb-4 border-b border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              Vaccination &amp; Checkup Schedule
            </h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
              CLINIC
            </span>
          </div>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="btn btn-primary btn-sm flex items-center gap-1.5 text-xs font-semibold"
        >
          <IconCalendar className="w-3.5 h-3.5" />
          <span>+ Schedule Vaccine / Checkup</span>
        </button>
      </div>

      {success && (
        <div className="p-3.5 rounded-lg bg-emerald-50 text-emerald-900 border border-emerald-300 text-xs font-medium">
          ✓ {success}
        </div>
      )}

      {/* Schedule Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="card p-6 max-w-lg w-full bg-white border border-slate-300 shadow-xl rounded-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2 font-display">
                <IconSyringe className="w-4 h-4 text-emerald-800" />
                Schedule Vaccine / Checkup
              </h2>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 font-bold text-sm">
                ✕
              </button>
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-red-50 text-red-800 text-xs border border-red-200">
                {error}
              </div>
            )}

            <form onSubmit={handleSchedule} className="space-y-4">
              <div>
                <label className="label">Select Cattle / Animal *</label>
                <select
                  className="input text-xs"
                  value={form.cattleId}
                  onChange={(e) => setForm({ ...form, cattleId: e.target.value })}
                  required
                >
                  <option value="">— Select animal —</option>
                  {cattleList.map((c) => (
                    <option key={c.id} value={c.id}>
                      Tag: {c.tagId} {c.name ? `(${c.name})` : ""} · {c.breed} · Farmer: {c.farmer.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="label">Checkup / Vaccine Type *</label>
                <select
                  className="input text-xs"
                  value={form.vaccineType}
                  onChange={(e) => setForm({ ...form, vaccineType: e.target.value })}
                  required
                >
                  {COMMON_VACCINES.map((v) => (
                    <option key={v} value={v}>
                      {v}
                    </option>
                  ))}
                  <option value="Other">Other / Custom</option>
                </select>
              </div>

              {form.vaccineType === "Other" && (
                <div>
                  <label className="label">Custom Vaccine Name *</label>
                  <input
                    type="text"
                    className="input text-xs"
                    placeholder="e.g. Deworming Drive"
                    value={form.customType}
                    onChange={(e) => setForm({ ...form, customType: e.target.value })}
                    required
                  />
                </div>
              )}

              <div>
                <label className="label">Scheduled Date *</label>
                <input
                  type="date"
                  className="input text-xs"
                  value={form.dueAt}
                  onChange={(e) => setForm({ ...form, dueAt: e.target.value })}
                  required
                >
                </input>
              </div>

              <div>
                <label className="label">Notes / Instructions (optional)</label>
                <textarea
                  className="input min-h-[60px] resize-none text-xs"
                  placeholder="e.g. Dosage: 5ml, Administer morning before feeding..."
                  value={form.notes}
                  onChange={(e) => setForm({ ...form, notes: e.target.value })}
                />
              </div>

              <div className="flex items-center justify-end gap-2.5 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary btn-sm text-xs">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary btn-sm text-xs font-bold" disabled={loading}>
                  {loading ? "Scheduling..." : "Save Schedule →"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Scheduled Table */}
      <div className="card overflow-hidden bg-white border border-slate-300 shadow-xs rounded-xl">
        <div className="p-3.5 bg-[#f8faf9] border-b border-slate-200 flex items-center justify-between">
          <h2 className="font-bold text-xs uppercase font-mono text-slate-800">Vaccination Schedule &amp; Drives</h2>
          <span className="text-[11px] font-mono text-slate-500">{records.length} total</span>
        </div>

        {records.length === 0 ? (
          <div className="p-10 text-center text-slate-400 text-xs">
            No vaccines scheduled yet. Click &quot;Schedule Vaccine / Checkup&quot; above to add dates.
          </div>
        ) : (
          <div className="table-container border-0 rounded-none">
            <table className="table">
              <thead>
                <tr>
                  <th>Cattle</th>
                  <th>Farmer</th>
                  <th>Vaccine / Checkup</th>
                  <th>Due Date</th>
                  <th>Status</th>
                  <th>Notes</th>
                  <th className="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => (
                  <tr key={r.id}>
                    <td>
                      <div>
                        <span className="font-mono font-bold text-slate-900 text-xs">{r.cattleTagId}</span>
                        {r.cattleName && <span className="text-xs text-slate-500 block">{r.cattleName}</span>}
                        <span className="text-[11px] text-slate-400 block">{r.breed}</span>
                      </div>
                    </td>
                    <td>
                      <div>
                        <span className="font-semibold text-slate-800 text-xs">{r.farmerName}</span>
                        <span className="text-[11px] font-mono text-slate-500 block">{r.farmerPhone}</span>
                      </div>
                    </td>
                    <td>
                      <span className="font-semibold text-emerald-900 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-xs">
                        {r.vaccineType}
                      </span>
                    </td>
                    <td>
                      <span className="font-mono text-xs text-slate-700">{r.dueAt}</span>
                    </td>
                    <td>
                      <span
                        className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
                          r.status === "done"
                            ? "bg-emerald-100 text-emerald-900 border border-emerald-200"
                            : "bg-amber-100 text-amber-900 border border-amber-200"
                        }`}
                      >
                        {r.status === "done" ? "✓ Done" : "⏳ Due"}
                      </span>
                    </td>
                    <td className="max-w-xs truncate text-xs text-slate-500">
                      {r.notes || "—"}
                    </td>
                    <td className="text-right">
                      <button
                        onClick={() => handleToggleStatus(r.id, r.status)}
                        className={`btn btn-sm text-xs font-semibold ${
                          r.status === "done"
                            ? "btn-secondary"
                            : "btn-primary"
                        }`}
                      >
                        {r.status === "done" ? "Mark Due" : "Mark Done ✓"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

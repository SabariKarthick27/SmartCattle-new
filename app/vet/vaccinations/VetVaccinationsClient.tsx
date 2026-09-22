"use client";

import { useState } from "react";
import { IconSyringe, IconCheckCircle, IconCalendar } from "@/components/icons";

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
      setError(data.error || "Failed to schedule vaccination/checkup");
      return;
    }

    setSuccess("Checkup / Vaccination date scheduled successfully!");
    setShowModal(false);
    // Reload window to refresh state cleanly
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
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
            <IconSyringe className="w-6 h-6 text-teal-700" />
            Vaccination & Health Checkup Scheduler
          </h1>
          <p className="text-slate-500 mt-1">
            Assign checkup dates and schedule vaccination drives for cattle in{" "}
            <span className="font-semibold text-slate-700">{vetRegion || "Assigned Coverage"}</span>
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="btn-primary flex items-center gap-2"
        >
          <IconCalendar className="w-4 h-4" />
          <span>Schedule New Checkup / Vaccine</span>
        </button>
      </div>

      {success && (
        <div className="p-4 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200 text-sm font-medium">
          {success}
        </div>
      )}

      {/* Schedule Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="card p-6 max-w-lg w-full space-y-4 animate-fade-in-up">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <IconSyringe className="w-5 h-5 text-teal-700" />
                Schedule Checkup / Vaccination Date
              </h2>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 font-bold">
                ✕
              </button>
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-red-50 text-red-700 text-sm border border-red-200">
                {error}
              </div>
            )}

            <form onSubmit={handleSchedule} className="space-y-4">
              <div>
                <label className="label">Select Cattle / Animal *</label>
                <select
                  className="input"
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
                  className="input"
                  value={form.vaccineType}
                  onChange={(e) => setForm({ ...form, vaccineType: e.target.value })}
                  required
                >
                  {COMMON_VACCINES.map((v) => (
                    <option key={v} value={v}>
                      {v}
                    </option>
                  ))}
                  <option value="Other">Other / Custom Checkup</option>
                </select>
              </div>

              {form.vaccineType === "Other" && (
                <div>
                  <label className="label">Custom Checkup Name *</label>
                  <input
                    type="text"
                    className="input"
                    placeholder="e.g. Deworming Drive"
                    value={form.customType}
                    onChange={(e) => setForm({ ...form, customType: e.target.value })}
                    required
                  />
                </div>
              )}

              <div>
                <label className="label">Scheduled Checkup Date *</label>
                <input
                  type="date"
                  className="input"
                  value={form.dueAt}
                  onChange={(e) => setForm({ ...form, dueAt: e.target.value })}
                  required
                />
              </div>

              <div>
                <label className="label">Notes / Instructions (optional)</label>
                <textarea
                  className="input min-h-[70px] resize-none"
                  placeholder="e.g. Dosage: 5ml, Administer morning before feeding..."
                  value={form.notes}
                  onChange={(e) => setForm({ ...form, notes: e.target.value })}
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={loading}>
                  {loading ? "Scheduling..." : "Assign & Schedule Date"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Scheduled Table */}
      <div className="card overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <h2 className="font-bold text-slate-900">Assigned Schedule & Vaccination Drives</h2>
          <span className="text-xs text-slate-500">{records.length} total scheduled</span>
        </div>

        {records.length === 0 ? (
          <div className="p-8 text-center text-slate-500">
            No checkups or vaccination dates scheduled yet. Click &quot;Schedule New Checkup / Vaccine&quot; above to assign dates.
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Animal</th>
                  <th>Farmer</th>
                  <th>Checkup / Vaccine</th>
                  <th>Scheduled Date</th>
                  <th>Status</th>
                  <th>Notes</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => (
                  <tr key={r.id}>
                    <td>
                      <div>
                        <span className="font-mono font-bold text-slate-800">{r.cattleTagId}</span>
                        {r.cattleName && <span className="text-xs text-slate-500 block">{r.cattleName}</span>}
                        <span className="text-xs text-slate-400 block">{r.breed}</span>
                      </div>
                    </td>
                    <td>
                      <div>
                        <span className="font-medium text-slate-800">{r.farmerName}</span>
                        <span className="text-xs text-slate-400 block">{r.farmerPhone}</span>
                      </div>
                    </td>
                    <td>
                      <span className="font-semibold text-teal-800 bg-teal-50 px-2.5 py-1 rounded-lg border border-teal-200/60 text-xs">
                        {r.vaccineType}
                      </span>
                    </td>
                    <td>
                      <span className="font-medium text-slate-700">{r.dueAt}</span>
                    </td>
                    <td>
                      <span
                        className={`text-xs px-2.5 py-1 rounded-full font-bold ${
                          r.status === "done"
                            ? "bg-emerald-100 text-emerald-800"
                            : "bg-amber-100 text-amber-800"
                        }`}
                      >
                        {r.status === "done" ? "✓ Completed" : "⏳ Scheduled"}
                      </span>
                    </td>
                    <td className="max-w-xs truncate text-xs text-slate-500">
                      {r.notes || "—"}
                    </td>
                    <td>
                      <button
                        onClick={() => handleToggleStatus(r.id, r.status)}
                        className={`btn-sm text-xs ${
                          r.status === "done"
                            ? "bg-slate-100 text-slate-600 hover:bg-slate-200"
                            : "bg-emerald-600 text-white hover:bg-emerald-700"
                        }`}
                      >
                        {r.status === "done" ? "Mark Scheduled" : "Mark Completed ✓"}
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

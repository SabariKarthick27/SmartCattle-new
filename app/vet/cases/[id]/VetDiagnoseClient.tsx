"use client";

import { useState } from "react";

interface Props {
  caseId: string;
  breed?: string;
  cattleId: string;
  existingDiagnosis: {
    symptoms: string;
    diagnosis: string;
    treatment: string;
    medication: string;
    followUpDate: string;
    status: string;
  };
  predictedStatus: string;
}

export default function VetDiagnoseClient({ caseId, existingDiagnosis }: Props) {
  const [form, setForm] = useState(existingDiagnosis);
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState("");

  const handleDiagnose = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSavedMsg("");

    const res = await fetch(`/api/vet/cases/${caseId}/diagnose`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    setSaving(false);
    if (res.ok) {
      setSavedMsg("Diagnosis and treatment saved successfully!");
    } else {
      const d = await res.json();
      setSavedMsg(d.error ?? "Failed to save diagnosis.");
    }
  };

  return (
    <div className="card p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div>
          <h2 className="font-bold text-sm text-slate-950 uppercase font-mono tracking-wider">
            Clinical Diagnosis &amp; Treatment
          </h2>
        </div>
        <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-100 text-slate-600 rounded">
          CLINICAL ACTION
        </span>
      </div>

      {savedMsg && (
        <div className="p-3 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-900 border border-emerald-200">
          {savedMsg}
        </div>
      )}

      <form onSubmit={handleDiagnose} className="space-y-4">
        {/* Horizontal Row 1: Case Status, Confirmed Diagnosis, Follow-up Date */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label htmlFor="vet-status" className="label text-slate-800 font-bold mb-1">
              Case Status
            </label>
            <select
              id="vet-status"
              className="input text-xs bg-white font-semibold w-full"
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value })}
            >
              <option value="open">Open (Needs Attention)</option>
              <option value="in_progress">In Progress (Under Treatment)</option>
              <option value="resolved">Resolved / Fully Recovered</option>
            </select>
          </div>

          <div>
            <label htmlFor="vet-diagnosis" className="label text-slate-800 font-bold mb-1">
              Confirmed Diagnosis
            </label>
            <input
              id="vet-diagnosis"
              type="text"
              className="input text-xs font-semibold w-full"
              value={form.diagnosis}
              onChange={(e) => setForm({ ...form, diagnosis: e.target.value })}
              placeholder="e.g. Acute Clinical Mastitis, Milk Fever..."
            />
          </div>

          <div>
            <label htmlFor="vet-followup" className="label text-slate-800 font-bold mb-1">
              Next Follow-up Date
            </label>
            <input
              id="vet-followup"
              type="date"
              className="input text-xs w-full"
              value={form.followUpDate}
              onChange={(e) => setForm({ ...form, followUpDate: e.target.value })}
            />
          </div>
        </div>

        {/* Horizontal Row 2: Treatment & Medication */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label htmlFor="vet-treatment" className="label text-slate-800 font-bold mb-1">
              Treatment &amp; Care Plan
            </label>
            <input
              id="vet-treatment"
              type="text"
              className="input text-xs w-full"
              value={form.treatment}
              onChange={(e) => setForm({ ...form, treatment: e.target.value })}
              placeholder="e.g. Cold fomentation, frequent milk stripping, antiseptic wash"
            />
          </div>

          <div>
            <label htmlFor="vet-medication" className="label text-slate-800 font-bold mb-1">
              Prescribed Medicine &amp; Dosage
            </label>
            <input
              id="vet-medication"
              type="text"
              className="input text-xs w-full"
              value={form.medication}
              onChange={(e) => setForm({ ...form, medication: e.target.value })}
              placeholder="e.g. Ceftiofur 1mg/kg IM + Flunixin 2.2mg/kg"
            />
          </div>
        </div>

        {/* Action Button Row */}
        <div className="flex items-center justify-end pt-3 border-t border-slate-100">
          <button
            id="save-diagnosis-btn"
            type="submit"
            className="btn btn-primary btn-sm font-bold text-xs px-6 py-2.5"
            disabled={saving}
          >
            {saving ? "Saving Diagnosis..." : "Save Clinical Diagnosis & Update Case →"}
          </button>
        </div>
      </form>
    </div>
  );
}

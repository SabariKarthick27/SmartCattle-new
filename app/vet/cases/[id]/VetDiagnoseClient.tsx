"use client";

import { useState } from "react";

interface Props {
  caseId: string;
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

const OUTCOME_OPTIONS = [
  "healthy",
  "recovered",
  "diagnosed",
  "hospitalized",
  "deceased",
];

export default function VetDiagnoseClient({ caseId, existingDiagnosis }: Props) {
  const [form, setForm] = useState(existingDiagnosis);
  const [feedback, setFeedback] = useState("");
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

  const handleFeedback = async () => {
    if (!feedback) return;
    setSaving(true);

    const res = await fetch(`/api/vet/cases/${caseId}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ confirmedOutcome: feedback }),
    });

    setSaving(false);
    if (res.ok) {
      setSavedMsg("Outcome logged for AI model training!");
    }
  };

  return (
    <div className="space-y-4">
      {/* Diagnosis form */}
      <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
        <h2 className="font-bold text-sm text-slate-950 uppercase font-mono tracking-wider">Clinical Diagnosis</h2>

        {savedMsg && (
          <div className="p-3 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-900 border border-emerald-200">
            {savedMsg}
          </div>
        )}

        <form onSubmit={handleDiagnose} className="space-y-3.5">
          {/* Temperature & Vitals Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3 bg-[#f8faf9] rounded-lg border border-slate-200">
            <div>
              <label htmlFor="vet-temp" className="label text-slate-800 font-bold">
                Body Temperature (°C)
              </label>
              <div className="relative">
                <input
                  id="vet-temp"
                  type="number"
                  step="0.1"
                  min="35"
                  max="44"
                  className="input text-xs font-mono font-bold bg-white"
                  placeholder="e.g. 39.8"
                  value={form.symptoms.includes("Temp: ") ? (form.symptoms.match(/Temp: ([0-9.]+)°C/)?.[1] ?? "") : ""}
                  onChange={(e) => {
                    const tempVal = e.target.value;
                    const cleanSymptoms = form.symptoms.replace(/Temp: [0-9.]+°C;? ?/g, "").trim();
                    const newSymptoms = tempVal ? `Temp: ${tempVal}°C; ${cleanSymptoms}`.trim() : cleanSymptoms;
                    setForm({ ...form, symptoms: newSymptoms });
                  }}
                />
                <span className="absolute right-3 top-2.5 text-xs text-slate-400 font-mono">°C</span>
              </div>
              <p className="text-[10px] text-slate-500 mt-1">Normal: 38.0°C – 39.3°C</p>
            </div>

            <div>
              <label htmlFor="vet-status" className="label text-slate-800 font-bold">Case Status</label>
              <select id="vet-status" className="input text-xs bg-white font-semibold" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                <option value="open">Open (Needs Inspection)</option>
                <option value="in_progress">In Progress (Under Treatment)</option>
                <option value="resolved">Resolved / Fully Recovered</option>
              </select>
              <p className="text-[10px] text-slate-500 mt-1">Update clinical state</p>
            </div>
          </div>

          <div>
            <label htmlFor="vet-symptoms" className="label">Observed Symptoms &amp; Physical Vitals</label>
            <textarea
              id="vet-symptoms"
              className="input min-h-[60px] resize-none text-xs"
              value={form.symptoms}
              onChange={(e) => setForm({ ...form, symptoms: e.target.value })}
              placeholder="e.g. Mild fever, swollen right hind quarter, reduced feed intake, normal rumination..."
            />
          </div>

          <div>
            <label htmlFor="vet-diagnosis" className="label">Confirmed Diagnosis</label>
            <input
              id="vet-diagnosis"
              type="text"
              className="input text-xs font-semibold"
              value={form.diagnosis}
              onChange={(e) => setForm({ ...form, diagnosis: e.target.value })}
              placeholder="e.g. Early Acute Mastitis, Milk Fever, Foot Rot, FMD..."
            />
          </div>

          <div>
            <label htmlFor="vet-treatment" className="label">Treatment &amp; Care Plan</label>
            <textarea
              id="vet-treatment"
              className="input min-h-[60px] resize-none text-xs"
              value={form.treatment}
              onChange={(e) => setForm({ ...form, treatment: e.target.value })}
              placeholder="e.g. 3 days intramammary antibiotic infusion, cold fomentation, daily milk monitoring..."
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label htmlFor="vet-medication" className="label">Medicine &amp; Dosage</label>
              <input
                id="vet-medication"
                type="text"
                className="input text-xs"
                value={form.medication}
                onChange={(e) => setForm({ ...form, medication: e.target.value })}
                placeholder="e.g. Ceftiofur 1mg/kg + Flunixin"
              />
            </div>
            <div>
              <label htmlFor="vet-followup" className="label">Next Follow-up Date</label>
              <input
                id="vet-followup"
                type="date"
                className="input text-xs"
                value={form.followUpDate}
                onChange={(e) => setForm({ ...form, followUpDate: e.target.value })}
              />
            </div>
          </div>

          <button
            id="save-diagnosis-btn"
            type="submit"
            className="btn btn-primary w-full btn-sm font-bold text-xs mt-2 justify-center"
            disabled={saving}
          >
            {saving ? "Saving Diagnosis..." : "Save Clinical Diagnosis & Update Case →"}
          </button>
        </form>
      </div>

      {/* Model feedback training box */}
      <div className="card p-4 bg-[#f8faf9] border border-slate-200 rounded-xl space-y-2">
        <h3 className="font-bold text-xs uppercase font-mono text-slate-700">Confirm Final Outcome (AI Feedback)</h3>
        <p className="text-[11px] text-slate-500">Helps refine AI health score accuracy for this breed.</p>
        <div className="flex gap-2">
          <select
            className="input text-xs flex-1 bg-white"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          >
            <option value="">Select confirmed outcome</option>
            {OUTCOME_OPTIONS.map((o) => (
              <option key={o} value={o}>{o.toUpperCase()}</option>
            ))}
          </select>
          <button
            type="button"
            onClick={handleFeedback}
            disabled={!feedback || saving}
            className="btn btn-secondary btn-sm text-xs font-semibold"
          >
            Log Outcome
          </button>
        </div>
      </div>
    </div>
  );
}

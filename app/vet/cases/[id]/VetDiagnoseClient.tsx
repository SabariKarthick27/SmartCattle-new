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

export default function VetDiagnoseClient({ caseId, existingDiagnosis, predictedStatus }: Props) {
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
      setSavedMsg("Diagnosis saved!");
    } else {
      const d = await res.json();
      setSavedMsg(d.error);
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
      setSavedMsg("Feedback logged to improve the model!");
    }
  };

  return (
    <div className="space-y-4">
      {/* Diagnosis form */}
      <div className="card p-5">
        <h2 className="font-semibold text-slate-900 mb-4">Diagnosis</h2>

        {savedMsg && (
          <div className="mb-4 p-3 rounded-xl text-sm bg-brand-50 text-brand-900 border border-brand-200">
            {savedMsg}
          </div>
        )}

        <form onSubmit={handleDiagnose} className="space-y-3">
          <div>
            <label htmlFor="vet-symptoms" className="label">Symptoms</label>
            <textarea id="vet-symptoms" className="input min-h-[70px] resize-none" value={form.symptoms} onChange={(e) => setForm({ ...form, symptoms: e.target.value })} placeholder="Observed symptoms..." />
          </div>
          <div>
            <label htmlFor="vet-diagnosis" className="label">Diagnosis</label>
            <input id="vet-diagnosis" type="text" className="input" value={form.diagnosis} onChange={(e) => setForm({ ...form, diagnosis: e.target.value })} placeholder="Clinical diagnosis..." />
          </div>
          <div>
            <label htmlFor="vet-treatment" className="label">Treatment</label>
            <textarea id="vet-treatment" className="input min-h-[60px] resize-none" value={form.treatment} onChange={(e) => setForm({ ...form, treatment: e.target.value })} placeholder="Recommended treatment..." />
          </div>
          <div>
            <label htmlFor="vet-medication" className="label">Medication & Dosage</label>
            <input id="vet-medication" type="text" className="input" value={form.medication} onChange={(e) => setForm({ ...form, medication: e.target.value })} placeholder="e.g. Oxytetracycline 10mg/kg" />
          </div>
          <div>
            <label htmlFor="vet-followup" className="label">Follow-up Date</label>
            <input id="vet-followup" type="date" className="input" value={form.followUpDate} onChange={(e) => setForm({ ...form, followUpDate: e.target.value })} />
          </div>
          <div>
            <label htmlFor="vet-status" className="label">Update Case Status</label>
            <select id="vet-status" className="input" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <button id="diagnose-submit" type="submit" className="btn-primary w-full" disabled={saving}>
            {saving ? "Saving..." : "Save Diagnosis"}
          </button>
        </form>
      </div>

      {/* Feedback to ML model */}
      <div className="card p-5">
        <h2 className="font-semibold text-slate-900 mb-1">Model Feedback</h2>
        <p className="text-xs text-slate-500 mb-3">
          CHDI predicted: <strong className="text-slate-700">{predictedStatus}</strong>. Confirm or correct to improve Stage 3.
        </p>
        <select id="feedback-outcome" className="input mb-3" value={feedback} onChange={(e) => setFeedback(e.target.value)}>
          <option value="">— Select outcome —</option>
          {OUTCOME_OPTIONS.map((o) => <option key={o} value={o}>{o}</option>)}
        </select>
        <button id="feedback-submit" onClick={handleFeedback} className="btn-secondary w-full" disabled={!feedback || saving}>
          Submit Feedback
        </button>
      </div>
    </div>
  );
}

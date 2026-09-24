"use client";

import { useEffect, useState } from "react";

export default function AdminModelPage() {
  const [stats, setStats] = useState<{
    stage1: { method: string; windowDays: number };
    stage2: { abstentionRate: number; totalScored: number; abstainCount: number };
    stage3: { precision: number; recall: number; f1Score: number; accuracy: number; sampleCount: number; trainedAt: string | null };
    feedbackCount: number;
    modelVersions: Array<{ id: string; stage: number; version: string; precision: number | null; recall: number | null; f1Score: number | null; trainedAt: string; isActive: boolean }>;
  } | null>(null);

  const [thresholds, setThresholds] = useState<Array<{ key: string; value: string; description: string | null }>>([]);
  const [retraining, setRetraining] = useState(false);
  const [retainMsg, setRetainMsg] = useState("");

  useEffect(() => {
    fetch("/api/admin/model-stats")
      .then(r => r.json())
      .then(d => { if (d?.stage1) setStats(d); })
      .catch(console.error);
    fetch("/api/admin/chdi-config")
      .then(r => r.json())
      .then(d => setThresholds(d.settings ?? []))
      .catch(console.error);
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    setRetainMsg("");
    const res = await fetch("/api/admin/model-stats", { method: "POST" });
    setRetraining(false);
    if (res.ok) {
      const d = await res.json();
      setRetainMsg(`Retraining complete. F1 Score: ${d.metrics.f1Score.toFixed(3)}`);
      fetch("/api/admin/model-stats").then(r => r.json()).then(d => { if (d?.stage1) setStats(d); }).catch(console.error);
    } else {
      setRetainMsg("Retraining failed");
    }
  };

  const saveThresholds = async () => {
    const res = await fetch("/api/admin/chdi-config", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ updates: thresholds.map(t => ({ key: t.key, value: t.value })) }),
    });
    if (res.ok) setRetainMsg("Thresholds saved successfully");
  };

  return (
    <div className="p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Health AI Engine & Calibration</h1>
        <p className="text-slate-500 text-sm mt-1">Manage cow health scoring calculations, alert thresholds, and veterinarian learning</p>
      </div>

      {retainMsg && (
        <div className="p-3.5 rounded-xl text-sm bg-brand-50 text-brand-900 border border-brand-200">
          {retainMsg}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stage 1 */}
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="bg-brand-100 text-brand-800 text-xs font-bold px-2.5 py-1 rounded-md">Stage 1</span>
            <h2 className="font-semibold text-slate-900">Baseline Forecasting</h2>
          </div>
          <p className="text-xs text-slate-500 mb-4">Calculates normal rolling average for each individual cow.</p>
          <div className="space-y-2.5 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Calculation Method</span>
              <span className="font-semibold text-slate-900">{stats?.stage1.method ?? "Rolling Window"}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>Calibration Window</span>
              <span className="font-semibold text-slate-900">{stats?.stage1.windowDays ?? 7} days</span>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-4 border-t border-slate-100 pt-3">
            Accumulates daily weight, feed, and milk logs before generating health scores.
          </p>
        </div>

        {/* Stage 2 */}
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="bg-teal-100 text-teal-800 text-xs font-bold px-2.5 py-1 rounded-md">Stage 2</span>
            <h2 className="font-semibold text-slate-900">Anomaly Detection</h2>
          </div>
          <p className="text-xs text-slate-500 mb-4">Detects abnormal deviations across vital signs and production.</p>
          <div className="space-y-2.5 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Total Evaluations</span>
              <span className="font-semibold text-slate-900 tnum">{stats?.stage2.totalScored ?? 0}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>Learning Baseline Cases</span>
              <span className="font-semibold text-slate-900 tnum">{stats?.stage2.abstainCount ?? 0}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>Calibration Hold Rate</span>
              <span className={`font-bold tnum ${(stats?.stage2.abstentionRate ?? 0) > 0.3 ? "text-amber-600" : "text-emerald-700"}`}>
                {((stats?.stage2.abstentionRate ?? 0) * 100).toFixed(1)}%
              </span>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-4 border-t border-slate-100 pt-3">
            Cross-checks weight vs milk vs feed covariance for early illness signs.
          </p>
        </div>

        {/* Stage 3 */}
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2.5 py-1 rounded-md">Stage 3</span>
            <h2 className="font-semibold text-slate-900">Vet Feedback Learning</h2>
          </div>
          <p className="text-xs text-slate-500 mb-4">Learns from doctor diagnoses and field feedback.</p>
          <div className="space-y-2.5 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Doctor Feedback Records</span>
              <span className="font-semibold text-slate-900 tnum">{stats?.feedbackCount ?? 0} / 30 minimum</span>
            </div>
            {stats?.stage3.trainedAt ? (
              <>
                <div className="flex justify-between"><span>Precision</span><span className="font-bold text-slate-800 tnum">{((stats.stage3.precision ?? 0) * 100).toFixed(1)}%</span></div>
                <div className="flex justify-between"><span>Recall Rate</span><span className="font-bold text-slate-800 tnum">{((stats.stage3.recall ?? 0) * 100).toFixed(1)}%</span></div>
                <div className="flex justify-between"><span>Overall Accuracy (F1)</span><span className="font-bold text-emerald-700 tnum">{((stats.stage3.f1Score ?? 0) * 100).toFixed(1)}%</span></div>
              </>
            ) : (
              <p className="text-xs text-amber-700 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
                Awaiting 30+ doctor diagnosis logs to activate adaptive learning.
              </p>
            )}
          </div>
          <button id="retrain-btn" onClick={handleRetrain} disabled={retraining} className="btn btn-secondary btn-sm w-full mt-4">
            {retraining ? "Retraining AI Engine..." : "Retrain AI with Latest Vet Data"}
          </button>
        </div>
      </div>

      {/* CHDI Thresholds */}
      <div className="card p-6">
        <h2 className="font-semibold text-slate-900 mb-1">Health Score Alert Thresholds</h2>
        <p className="text-xs text-slate-500 mb-4">Configure the score levels that trigger green (Healthy), yellow (Needs Attention), or red (Critical) alerts for farmers and vets.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {thresholds.map((t, i) => (
            <div key={t.key}>
              <label className="label">{t.description ?? t.key}</label>
              <input
                id={`threshold-${t.key}`}
                type="number"
                step="0.01"
                className="input font-semibold"
                value={t.value}
                onChange={(e) => {
                  const updated = [...thresholds];
                  updated[i] = { ...t, value: e.target.value };
                  setThresholds(updated);
                }}
              />
            </div>
          ))}
        </div>
        <button id="save-thresholds-btn" onClick={saveThresholds} className="btn btn-primary mt-5">
          Save Alert Thresholds
        </button>
      </div>

      {/* Model version history */}
      {stats?.modelVersions && stats.modelVersions.length > 0 && (
        <div className="card overflow-hidden">
          <div className="p-5 border-b border-slate-100">
            <h2 className="font-semibold text-slate-900">AI Model Version History</h2>
            <p className="text-xs text-slate-500 mt-0.5">Audit log of all retrained algorithms and their accuracy benchmarks</p>
          </div>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr><th>Stage</th><th>Version ID</th><th>Precision</th><th>Recall</th><th>F1 Accuracy</th><th>Trained Date</th><th>Active Status</th></tr>
              </thead>
              <tbody>
                {stats.modelVersions.map((v) => (
                  <tr key={v.id}>
                    <td><span className="font-mono text-xs bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-medium">Stage {v.stage}</span></td>
                    <td className="font-mono text-xs text-slate-600">{v.version.slice(0, 16)}</td>
                    <td className="tnum">{v.precision != null ? `${(v.precision * 100).toFixed(1)}%` : "—"}</td>
                    <td className="tnum">{v.recall != null ? `${(v.recall * 100).toFixed(1)}%` : "—"}</td>
                    <td className="font-bold text-emerald-700 tnum">{v.f1Score != null ? `${(v.f1Score * 100).toFixed(1)}%` : "—"}</td>
                    <td className="text-xs text-slate-500">{new Date(v.trainedAt).toLocaleDateString("en-IN")}</td>
                    <td>{v.isActive ? <span className="text-emerald-700 text-xs font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">● Active</span> : <span className="text-slate-400 text-xs">—</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

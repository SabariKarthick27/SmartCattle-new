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
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Model Management</h1>
        <p className="text-slate-500 mt-1">CHDI engine performance, thresholds, and retraining</p>
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
            <span className="bg-brand-100 text-brand-800 text-xs font-bold px-2 py-1 rounded-lg">Stage 1</span>
            <h2 className="font-semibold text-slate-900">Baseline Forecasting</h2>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Method</span>
              <span className="font-medium">{stats?.stage1.method ?? "—"}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>Window</span>
              <span className="font-medium">{stats?.stage1.windowDays ?? "—"} days</span>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-3">Swappable with TensorFlow.js LSTM behind the same computeBaseline() interface</p>
        </div>

        {/* Stage 2 */}
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="bg-teal-100 text-teal-800 text-xs font-bold px-2 py-1 rounded-lg">Stage 2</span>
            <h2 className="font-semibold text-slate-900">Anomaly Detection</h2>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Total scored</span>
              <span className="font-medium">{stats?.stage2.totalScored ?? 0}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>Abstentions</span>
              <span className="font-medium">{stats?.stage2.abstainCount ?? 0}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>Abstention rate</span>
              <span className={`font-bold ${(stats?.stage2.abstentionRate ?? 0) > 0.3 ? "text-amber-600" : "text-emerald-600"}`}>
                {((stats?.stage2.abstentionRate ?? 0) * 100).toFixed(1)}%
              </span>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-3">Mahalanobis distance-based anomaly detection</p>
        </div>

        {/* Stage 3 */}
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded-lg">Stage 3</span>
            <h2 className="font-semibold text-slate-900">Vet-Feedback Classifier</h2>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Feedback rows</span>
              <span className="font-medium">{stats?.feedbackCount ?? 0} / 30 (min)</span>
            </div>
            {stats?.stage3.trainedAt ? (
              <>
                <div className="flex justify-between"><span>Precision</span><span className="font-bold text-slate-800">{((stats.stage3.precision ?? 0) * 100).toFixed(1)}%</span></div>
                <div className="flex justify-between"><span>Recall</span><span className="font-bold text-slate-800">{((stats.stage3.recall ?? 0) * 100).toFixed(1)}%</span></div>
                <div className="flex justify-between"><span>F1 Score</span><span className="font-bold text-emerald-700">{((stats.stage3.f1Score ?? 0) * 100).toFixed(1)}%</span></div>
              </>
            ) : (
              <p className="text-xs text-amber-600 mt-1">Not yet trained — needs 30+ vet feedback rows</p>
            )}
          </div>
          <button id="retrain-btn" onClick={handleRetrain} disabled={retraining} className="btn-secondary btn-sm w-full mt-4">
            {retraining ? "Retraining..." : "Trigger Retraining"}
          </button>
        </div>
      </div>

      {/* CHDI Thresholds */}
      <div className="card p-6">
        <h2 className="font-semibold text-slate-900 mb-4">CHDI Thresholds (Admin-Configurable)</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {thresholds.map((t, i) => (
            <div key={t.key}>
              <label className="label">{t.description ?? t.key}</label>
              <input
                id={`threshold-${t.key}`}
                type="number"
                step="0.01"
                className="input"
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
        <button id="save-thresholds-btn" onClick={saveThresholds} className="btn-primary mt-4">
          Save Thresholds
        </button>
      </div>

      {/* Model version history */}
      {stats?.modelVersions && stats.modelVersions.length > 0 && (
        <div className="card overflow-hidden">
          <div className="p-5 border-b border-slate-100">
            <h2 className="font-semibold text-slate-900">Model Version History</h2>
          </div>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr><th>Stage</th><th>Version</th><th>Precision</th><th>Recall</th><th>F1</th><th>Trained</th><th>Active</th></tr>
              </thead>
              <tbody>
                {stats.modelVersions.map((v) => (
                  <tr key={v.id}>
                    <td><span className="font-mono text-xs bg-slate-100 px-2 py-0.5 rounded">Stage {v.stage}</span></td>
                    <td className="font-mono text-xs">{v.version.slice(0, 16)}</td>
                    <td>{v.precision != null ? `${(v.precision * 100).toFixed(1)}%` : "—"}</td>
                    <td>{v.recall != null ? `${(v.recall * 100).toFixed(1)}%` : "—"}</td>
                    <td className="font-bold text-emerald-700">{v.f1Score != null ? `${(v.f1Score * 100).toFixed(1)}%` : "—"}</td>
                    <td className="text-xs text-slate-400">{new Date(v.trainedAt).toLocaleDateString("en-IN")}</td>
                    <td>{v.isActive ? <span className="text-emerald-600 text-xs font-bold">● Active</span> : <span className="text-slate-400 text-xs">—</span>}</td>
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

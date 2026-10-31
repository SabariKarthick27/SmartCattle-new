"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { COMMON_VACCINES } from "@/lib/constants";
import { getBreedTemperatureConfig, evaluateTemperatureStatus } from "@/lib/utils";

interface CHDIPoint {
  score: number | null;
  status: string;
  timestamp: string;
}

interface WeightPoint {
  value: number;
  timestamp: string;
  source: string;
}

interface FeedPoint {
  quantity: number;
  feedType: string;
  timestamp: string;
  source: string;
}

interface MilkPoint {
  id: string;
  litres: number;
  timestamp: string;
  source: string;
}

interface TemperaturePoint {
  value: number;
  timestamp: string;
  source: string;
}

interface VaccinationLogItem {
  id: string;
  vaccineName: string;
  dateGiven: string | null;
  nextDueDate: string | null;
}

interface Vaccination {
  id: string;
  vaccineType: string;
  dueAt: string;
  status: string;
  administeredAt: string | null;
}

interface VetCase {
  id: string;
  status: string;
  urgency: string;
  createdAt: string;
  vetName: string | null;
  diagnosis: string | null;
}

export interface AvailableVet {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  assignedRegion: string | null;
}

interface Props {
  cattleId: string;
  breed?: string;
  purpose: string;
  isAbstaining: boolean;
  minLogged: number;
  chdiHistory: CHDIPoint[];
  weightLogs: WeightPoint[];
  feedLogs: FeedPoint[];
  milkLogs: MilkPoint[];
  temperatureLogs?: TemperaturePoint[];
  vaccinationLogs: VaccinationLogItem[];
  vaccinations: Vaccination[];
  vetCases: VetCase[];
  availableVets?: AvailableVet[];
  farmerRegion?: string;
  farmerRole: boolean;
}

type Tab = "chdi" | "weight" | "feed" | "milk" | "temperature" | "logs" | "vaccines" | "vet";
type LogRange = "30" | "90";

export default function CattleProfileClient({
  cattleId,
  breed = "",
  purpose,
  isAbstaining,
  minLogged,
  chdiHistory,
  weightLogs: initialWeightLogs,
  feedLogs: initialFeedLogs,
  milkLogs: initialMilkLogs,
  temperatureLogs: initialTempLogs = [],
  vaccinationLogs: initialVaccinationLogs,
  vetCases: initialVetCases,
  availableVets = [],
  farmerRegion = "",
  farmerRole,
}: Props) {
  const [tab, setTab] = useState<Tab>("chdi");
  const [range, setRange] = useState<LogRange>("30");
  const breedTempConfig = getBreedTemperatureConfig(breed);

  // Local state for interactive recurring logs
  const [weightLogs, setWeightLogs] = useState<WeightPoint[]>(initialWeightLogs);
  const [feedLogs, setFeedLogs] = useState<FeedPoint[]>(initialFeedLogs);
  const [milkLogs, setMilkLogs] = useState<MilkPoint[]>(initialMilkLogs);
  const [temperatureLogs, setTemperatureLogs] = useState<TemperaturePoint[]>(initialTempLogs);
  const [vaccinationLogs, setVaccinationLogs] =
    useState<VaccinationLogItem[]>(initialVaccinationLogs);

  // Health data log form
  const [logForm, setLogForm] = useState({
    type: purpose === "dairy" ? "milk" : "weight",
    value: "",
    feedType: "grass",
    source: "manual",
    date: new Date().toISOString().split("T")[0],
  });
  const [logging, setLogging] = useState(false);
  const [logMsg, setLogMsg] = useState("");

  // Recurring vaccination form
  const [vacForm, setVacForm] = useState({
    vaccineName: COMMON_VACCINES[0] as string,
    customVaccine: "",
    dateGiven: new Date().toISOString().split("T")[0],
    nextDueDate: "",
  });
  const [vacLoading, setVacLoading] = useState(false);
  const [vacMsg, setVacMsg] = useState("");

  // Vet request form & local state
  const [localVetCases, setLocalVetCases] = useState<VetCase[]>(initialVetCases);
  const [vetReqForm, setVetReqForm] = useState({
    symptoms: "",
    urgency: "medium",
    vetId: availableVets.find((v) => farmerRegion && v.assignedRegion?.toLowerCase().trim() === farmerRegion)?.id || availableVets[0]?.id || "",
  });
  const [vetReqLoading, setVetReqLoading] = useState(false);
  const [vetReqMsg, setVetReqMsg] = useState("");

  const rangeN = parseInt(range);
  const validChdi = chdiHistory.filter((p) => p.score !== null);
  const chdiSlice = validChdi.slice(0, rangeN).reverse();
  const weightSlice = weightLogs.slice(0, rangeN);
  const feedSlice = feedLogs.slice(0, rangeN);
  const milkSlice = milkLogs.slice(0, rangeN);

  // Format for recharts
  const chdiChartData = chdiSlice.map((p) => ({
    date: new Date(p.timestamp).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
    }),
    score: Math.round(p.score!),
    status: p.status,
  }));

  const weightChartData = weightSlice.slice().reverse().map((p) => ({
    date: new Date(p.timestamp).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
    }),
    weight: p.value,
  }));

  const milkChartData = milkSlice.slice().reverse().map((m) => ({
    date: new Date(m.timestamp).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
    }),
    litres: m.litres,
  }));

  // Handle generic health logging
  const handleLog = async (e: React.FormEvent) => {
    e.preventDefault();
    setLogging(true);
    setLogMsg("");

    const val = parseFloat(logForm.value);
    if (isNaN(val)) {
      setLogging(false);
      setLogMsg("Please enter a valid numeric value.");
      return;
    }

    const selectedDate = logForm.date
      ? new Date(logForm.date + "T12:00:00.000Z")
      : new Date();
    const timestampStr = selectedDate.toISOString();

    try {
      if (logForm.type === "milk") {
        // Daily milk log
        const res = await fetch(`/api/cattle/${cattleId}/milk-log`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            litres: val,
            source: logForm.source,
            timestamp: timestampStr,
          }),
        });
        const d = await res.json();
        setLogging(false);
        if (res.ok) {
          setLogMsg("Milk yield recorded successfully! Health scores will reflect this update.");
          const newEntry = {
            id: d.log?.id || `temp_${Date.now()}`,
            litres: d.log?.litres ?? val,
            timestamp: d.log?.timestamp ?? timestampStr,
            source: d.log?.source ?? logForm.source,
          };
          setMilkLogs((prev) =>
            [newEntry, ...prev].sort(
              (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
            )
          );
          setLogForm({ ...logForm, value: "" });
        } else {
          setLogMsg(d.error || "Failed to save milk yield.");
        }
      } else {
        const endpoint =
          logForm.type === "weight"
            ? "weight-log"
            : logForm.type === "feed"
            ? "feed-log"
            : logForm.type === "temperature"
            ? "temperature-log"
            : "activity-log";

        const body: Record<string, unknown> = {
          source: logForm.source,
          timestamp: timestampStr,
        };
        if (logForm.type === "weight") body.value = val;
        else if (logForm.type === "feed") {
          body.quantity = val;
          body.feedType = logForm.feedType;
        } else {
          body.value = val;
        }

        const res = await fetch(`/api/cattle/${cattleId}/${endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });

        const d = await res.json();
        setLogging(false);

        if (res.ok) {
          setLogMsg("Daily check-in saved! Health metrics updated.");
          if (logForm.type === "weight") {
            const entry = {
              value: val,
              timestamp: d.log?.timestamp ?? timestampStr,
              source: logForm.source,
            };
            setWeightLogs((prev) =>
              [entry, ...prev].sort(
                (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
              )
            );
          } else if (logForm.type === "feed") {
            const entry = {
              quantity: val,
              feedType: logForm.feedType,
              timestamp: d.log?.timestamp ?? timestampStr,
              source: logForm.source,
            };
            setFeedLogs((prev) =>
              [entry, ...prev].sort(
                (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
              )
            );
          } else if (logForm.type === "temperature") {
            const entry = {
              value: val,
              timestamp: d.log?.timestamp ?? timestampStr,
              source: logForm.source,
            };
            setTemperatureLogs((prev) =>
              [entry, ...prev].sort(
                (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
              )
            );
          }
          setLogForm({ ...logForm, value: "" });
        } else {
          setLogMsg(d.error || "Failed to record check-in.");
        }
      }
    } catch {
      setLogging(false);
      setLogMsg("Network connection error while saving.");
    }
  };

  // Handle recurring vaccination entry
  const handleAddVaccination = async (e: React.FormEvent) => {
    e.preventDefault();
    setVacLoading(true);
    setVacMsg("");

    const nameToSave =
      vacForm.vaccineName === "Other"
        ? vacForm.customVaccine.trim()
        : vacForm.vaccineName;

    if (!nameToSave) {
      setVacLoading(false);
      setVacMsg("Please provide a vaccine name.");
      return;
    }

    try {
      const res = await fetch(`/api/cattle/${cattleId}/vaccination-log`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          vaccineName: nameToSave,
          dateGiven: vacForm.dateGiven || undefined,
          nextDueDate: vacForm.nextDueDate || undefined,
        }),
      });

      const d = await res.json();
      setVacLoading(false);

      if (res.ok) {
        setVacMsg("Vaccination entry recorded successfully!");
        setVaccinationLogs((prev) => [
          {
            id: d.log.id,
            vaccineName: d.log.vaccineName,
            dateGiven: d.log.dateGiven,
            nextDueDate: d.log.nextDueDate,
          },
          ...prev,
        ]);
        setVacForm({
          ...vacForm,
          customVaccine: "",
          nextDueDate: "",
        });
      } else {
        setVacMsg(d.error || "Failed to record vaccination log.");
      }
    } catch {
      setVacLoading(false);
      setVacMsg("Network error recording vaccination.");
    }
  };

  // Handle Vet visit request
  const handleVetRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    setVetReqLoading(true);
    setVetReqMsg("");

    try {
      const res = await fetch(`/api/cattle/${cattleId}/vet-request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(vetReqForm),
      });

      const d = await res.json();
      setVetReqLoading(false);
      if (res.ok) {
        const chosen = availableVets.find((v) => v.id === vetReqForm.vetId);
        const vetDisplayName = d.vetCase?.vet?.name || chosen?.name || "District Veterinarian";
        setVetReqMsg(d.message || `Doctor visit requested! Assigned to ${vetDisplayName}.`);
        if (d.vetCase) {
          setLocalVetCases((prev) => {
            const exists = prev.some((c) => c.id === d.vetCase.id);
            if (exists) {
              return prev.map((c) =>
                c.id === d.vetCase.id
                  ? {
                      ...c,
                      urgency: d.vetCase.urgency,
                      vetName: vetDisplayName,
                    }
                  : c
              );
            }
            return [
              {
                id: d.vetCase.id,
                status: d.vetCase.status,
                urgency: d.vetCase.urgency,
                createdAt: d.vetCase.createdAt,
                vetName: vetDisplayName,
                diagnosis: null,
              },
              ...prev,
            ];
          });
        }
        setVetReqForm((prev) => ({ ...prev, symptoms: "" }));
      } else {
        setVetReqMsg(d.error || "Failed to submit vet request.");
      }
    } catch {
      setVetReqLoading(false);
      setVetReqMsg("Network error submitting request.");
    }
  };

  // Construct dynamic tab bar based on purpose
  const TABS: { key: Tab; label: string }[] = [
    { key: "chdi", label: "Health Score Trend" },
    { key: "weight", label: "Weight History" },
    { key: "feed", label: "Feed Intake" },
  ];

  if (purpose === "dairy") {
    TABS.push({ key: "milk", label: "Milk Production" });
  }
  TABS.push({ key: "temperature", label: "Body Temperature" });

  TABS.push(
    { key: "logs", label: "Daily Check-In" },
    { key: "vaccines", label: "Vaccinations" },
    { key: "vet", label: "Doctor & Vet Care" }
  );

  return (
    <div className="space-y-6">
      {/* Tab bar */}
      <div className="flex gap-1.5 bg-slate-100/80 p-1.5 rounded-xl w-fit flex-wrap border border-slate-200">
        {TABS.map((t) => (
          <button
            key={t.key}
            id={`profile-tab-${t.key}`}
            onClick={() => setTab(t.key)}
            className={`px-3.5 py-1.5 rounded-lg text-xs md:text-sm font-semibold transition-all duration-150 ${
              tab === t.key
                ? "bg-white text-slate-900 shadow-sm border border-slate-200/60"
                : "text-slate-600 hover:text-slate-900 hover:bg-white/50"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Range selector (for charts) */}
      {(tab === "chdi" || tab === "weight" || tab === "feed" || tab === "milk" || tab === "temperature") && (
        <div className="flex gap-2">
          {(["30", "90"] as LogRange[]).map((r) => (
            <button
              key={r}
              onClick={() => setRange(r)}
              className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
                range === r
                  ? "bg-brand-950 text-white"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
              }`}
            >
              Past {r} days
            </button>
          ))}
        </div>
      )}

      {/* CHDI Chart */}
      {tab === "chdi" && (
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-semibold text-slate-900">
                Health Score Trend (0–100)
              </h3>
            </div>
            {validChdi.length > 0 && validChdi[0].score !== null && (
              <div className="text-right">
                <span className="text-2xl font-bold text-slate-900 tnum">
                  {Math.round(validChdi[0].score)}/100
                </span>
                <p className="text-xs text-slate-400">Latest score</p>
              </div>
            )}
          </div>

          {isAbstaining ? (
            <div className="text-center py-12 px-4 rounded-xl bg-amber-50/50 border border-amber-200">
              <div className="w-12 h-12 rounded-full bg-amber-100 text-amber-800 flex items-center justify-center font-bold mx-auto mb-3 text-lg">
                ⏳
              </div>
              <h4 className="font-semibold text-slate-900 text-base">
                Learning habits — {minLogged}/7 check-ins recorded
              </h4>
              <p className="text-slate-600 text-xs md:text-sm mt-1 max-w-md mx-auto leading-relaxed">
                SmartCattle calculates a weekly health baseline for this cow. Scores unlock once 7 daily logs are registered across the weekly checkup cycle.
              </p>
            </div>
          ) : chdiChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={chdiChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#94a3b8" }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: "#94a3b8" }} />
                <Tooltip
                  contentStyle={{
                    borderRadius: "8px",
                    border: "1px solid #e2e8f0",
                    fontSize: 12,
                  }}
                  formatter={(v: any) => [`${v}/100`, "Health Score"]}
                />
                <ReferenceLine
                  y={75}
                  stroke="#10b981"
                  strokeDasharray="4 4"
                  label={{ value: "Healthy", position: "right", fontSize: 10 }}
                />
                <ReferenceLine
                  y={50}
                  stroke="#f59e0b"
                  strokeDasharray="4 4"
                  label={{ value: "Needs Attention", position: "right", fontSize: 10 }}
                />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#0F5132"
                  strokeWidth={2.5}
                  dot={{ r: 3, fill: "#0F5132" }}
                  activeDot={{ r: 5 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-slate-400 text-center py-12 text-sm">
              No score records available yet.
            </p>
          )}
        </div>
      )}

      {/* Weight Chart */}
      {tab === "weight" && (
        <div className="card p-6">
          <h3 className="font-semibold text-slate-900 mb-1">
            Body Weight Over Time (kg)
          </h3>
          {weightChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={weightChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#94a3b8" }} />
                <YAxis tick={{ fontSize: 11, fill: "#94a3b8" }} />
                <Tooltip
                  contentStyle={{ borderRadius: "8px", fontSize: 12 }}
                  formatter={(v: any) => [`${v} kg`, "Weight"]}
                />
                <Line
                  type="monotone"
                  dataKey="weight"
                  stroke="#0D7A5F"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-slate-400 text-center py-12 text-sm">No weight records saved yet.</p>
          )}

          <div className="mt-6 table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Weight</th>
                  <th>Recorded Via</th>
                </tr>
              </thead>
              <tbody>
                {weightLogs.slice(0, 10).map((l, i) => (
                  <tr key={i}>
                    <td className="text-slate-600 text-xs">{new Date(l.timestamp).toLocaleDateString("en-IN")}</td>
                    <td className="font-bold text-slate-900 tnum">{l.value} kg</td>
                    <td>
                      <span className="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded font-medium">{l.source === "manual" ? "Farmer Entry" : l.source === "qr_scan" ? "QR Scan" : "Sensor Scale"}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      
      {/* Temperature Tab */}
      {tab === "temperature" && (
        <div className="card p-6">
          <div className="mb-4">
            <h3 className="font-semibold text-slate-900 text-lg">
              Core Body Temperature (°C)
            </h3>
          </div>

          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Body Temperature</th>
                  <th>Clinical Interpretation</th>
                  <th>Recorded Via</th>
                </tr>
              </thead>
              <tbody>
                {temperatureLogs.slice(0, rangeN).map((l, i) => {
                  const evalResult = evaluateTemperatureStatus(l.value, breed);
                  return (
                    <tr key={i}>
                      <td className="text-slate-600 text-xs">
                        {new Date(l.timestamp).toLocaleDateString("en-IN")}
                      </td>
                      <td className="font-bold text-slate-900 tnum">
                        {l.value.toFixed(1)} °C
                      </td>
                      <td>
                        <span className={`text-xs px-2.5 py-1 rounded-md font-bold ${evalResult.badgeClass}`}>
                          {evalResult.label}
                        </span>
                      </td>
                      <td>
                        <span className="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded font-medium">
                          {l.source === "manual" ? "Farmer Entry" : l.source === "qr_scan" ? "QR Scan" : "Thermal Probe"}
                        </span>
                      </td>
                    </tr>
                  );
                })}
                {temperatureLogs.length === 0 && (
                  <tr>
                    <td colSpan={4} className="text-center text-slate-400 py-6 text-sm">
                      No temperature entries logged yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      {/* Feed Chart / Logs */}
      {tab === "feed" && (
        <div className="card p-6">
          <h3 className="font-semibold text-slate-900 mb-1">
            Feed & Fodder Intake (kg)
          </h3>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Quantity Given</th>
                  <th>Feed Type</th>
                  <th>Recorded Via</th>
                </tr>
              </thead>
              <tbody>
                {feedSlice.map((l, i) => (
                  <tr key={i}>
                    <td className="text-slate-600 text-xs">{new Date(l.timestamp).toLocaleDateString("en-IN")}</td>
                    <td className="font-bold text-slate-900 tnum">{l.quantity} kg</td>
                    <td className="capitalize text-slate-800">{l.feedType}</td>
                    <td>
                      <span className="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded font-medium">{l.source === "manual" ? "Farmer Entry" : l.source === "qr_scan" ? "QR Scan" : "Sensor"}</span>
                    </td>
                  </tr>
                ))}
                {feedSlice.length === 0 && (
                  <tr>
                    <td colSpan={4} className="text-center text-slate-400 py-6 text-sm">
                      No feed intake recorded yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Milk Tab — Only if Dairy */}
      {tab === "milk" && purpose === "dairy" && (
        <div className="space-y-6">
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-semibold text-slate-900">
                  Daily Milk Yield (Litres)
                </h3>
              </div>
              {milkLogs.length > 0 && (
                <div className="text-right">
                  <span className="text-2xl font-bold text-brand-900 tnum">
                    {milkLogs[0].litres} L
                  </span>
                  <p className="text-xs text-slate-400">Latest yield</p>
                </div>
              )}
            </div>

            {milkChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={240}>
                <LineChart data={milkChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#94a3b8" }} />
                  <YAxis tick={{ fontSize: 11, fill: "#94a3b8" }} />
                  <Tooltip
                    contentStyle={{ borderRadius: "8px", fontSize: 12 }}
                    formatter={(v: any) => [`${v} Litres`, "Milk Yield"]}
                  />
                  <Line
                    type="monotone"
                    dataKey="litres"
                    stroke="#2563eb"
                    strokeWidth={2.5}
                    dot={{ r: 3, fill: "#2563eb" }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-slate-400 text-center py-8 text-sm">
                No milk yield logs recorded yet.
              </p>
            )}

            <div className="mt-6 table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Milk Yield</th>
                    <th>Recorded Via</th>
                  </tr>
                </thead>
                <tbody>
                  {milkSlice.map((m) => (
                    <tr key={m.id}>
                      <td className="text-slate-600 text-xs">{new Date(m.timestamp).toLocaleDateString("en-IN")}</td>
                      <td className="font-bold text-slate-900 tnum">{m.litres} Litres</td>
                      <td>
                        <span className="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded font-medium">{m.source === "manual" ? "Farmer Entry" : "Milking Meter"}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Daily Logs Tab */}
      {tab === "logs" && farmerRole && (
        <div className="max-w-2xl">
          <div className="card p-6">
            <h3 className="font-semibold text-slate-900 mb-1">
              Record Daily Health & Farm Data
            </h3>


            {logMsg && (
              <div className="mb-4 p-3.5 rounded-xl text-sm bg-brand-50 text-brand-900 border border-brand-200">
                {logMsg}
              </div>
            )}

            <form onSubmit={handleLog} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="label">What are you logging? *</label>
                  <select
                    id="log-type"
                    className="input"
                    value={logForm.type}
                    onChange={(e) =>
                      setLogForm({ ...logForm, type: e.target.value })
                    }
                  >
                    <option value="weight">Body Weight (kg)</option>
                    <option value="feed">Feed & Fodder (kg)</option>
                    <option value="temperature">Body Temperature (°C)</option>
                    {purpose === "dairy" && (
                      <option value="milk">Daily Milk Yield (Litres)</option>
                    )}
                  </select>
                </div>

                <div>
                  <label htmlFor="log-date" className="label">
                    Date of Measurement *
                  </label>
                  <input
                    id="log-date"
                    type="date"
                    className="input font-semibold"
                    value={logForm.date}
                    max={new Date().toISOString().split("T")[0]}
                    onChange={(e) =>
                      setLogForm({ ...logForm, date: e.target.value })
                    }
                    required
                  />
                </div>
              </div>

              {logForm.type === "feed" && (
                <div>
                  <label className="label">Feed Type</label>
                  <select
                    id="log-feedtype"
                    className="input capitalize"
                    value={logForm.feedType}
                    onChange={(e) =>
                      setLogForm({ ...logForm, feedType: e.target.value })
                    }
                  >
                    {[
                      "grass",
                      "green fodder",
                      "dry straw",
                      "concentrate",
                      "silage",
                      "mixed",
                    ].map((f) => (
                      <option key={f} value={f}>
                        {f}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              <div>
                <label htmlFor="log-value" className="label">
                  Amount / Value{" "}
                  {logForm.type === "weight"
                    ? "(kg)"
                    : logForm.type === "feed"
                    ? "(kg)"
                    : "(Litres today)"}
                </label>
                <input
                  id="log-value"
                  type="number"
                  step="0.1"
                  min="0"
                  className="input font-semibold"
                  placeholder={
                    logForm.type === "milk"
                      ? "e.g. 14.2"
                      : logForm.type === "weight"
                      ? "e.g. 385"
                      : "e.g. 18.0"
                  }
                  value={logForm.value}
                  onChange={(e) =>
                    setLogForm({ ...logForm, value: e.target.value })
                  }
                  required
                />
              </div>

              <div>
                <label className="label">How was this measured?</label>
                <select
                  id="log-source"
                  className="input"
                  value={logForm.source}
                  onChange={(e) =>
                    setLogForm({ ...logForm, source: e.target.value })
                  }
                >
                  <option value="manual">Manual farmer entry</option>
                  <option value="qr_scan">Scanned from QR Ear Tag</option>
                  <option value="sensor">Automated Sensor / Scale</option>
                </select>
              </div>

              <button
                id="log-submit"
                type="submit"
                className="btn btn-primary w-full justify-center"
                disabled={logging}
              >
                {logging ? "Saving Check-In..." : "Save Daily Check-In →"}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Recurring Vaccinations Tab */}
      {tab === "vaccines" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Add Vaccination Form */}
          {farmerRole && (
            <div className="card p-6">
              <h3 className="font-semibold text-slate-900 mb-1">
                Record Vaccine or Deworming
              </h3>


              {vacMsg && (
                <div className="mb-4 p-3.5 rounded-xl text-sm bg-brand-50 text-brand-900 border border-brand-200">
                  {vacMsg}
                </div>
              )}

              <form onSubmit={handleAddVaccination} className="space-y-4">
                <div>
                  <label className="label">Vaccine or Treatment *</label>
                  <select
                    className="input"
                    value={vacForm.vaccineName}
                    onChange={(e) =>
                      setVacForm({ ...vacForm, vaccineName: e.target.value })
                    }
                  >
                    {COMMON_VACCINES.map((v) => (
                      <option key={v} value={v}>
                        {v}
                      </option>
                    ))}
                    <option value="Other">Other / Custom Vaccine</option>
                  </select>
                </div>

                {vacForm.vaccineName === "Other" && (
                  <div>
                    <label className="label">Vaccine Name *</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g. Anthrax booster"
                      value={vacForm.customVaccine}
                      onChange={(e) =>
                        setVacForm({ ...vacForm, customVaccine: e.target.value })
                      }
                      required
                    />
                  </div>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="label">Date Given</label>
                    <input
                      type="date"
                      className="input"
                      value={vacForm.dateGiven}
                      onChange={(e) =>
                        setVacForm({ ...vacForm, dateGiven: e.target.value })
                      }
                      required
                    />
                  </div>
                  <div>
                    <label className="label">Next Due Date (optional)</label>
                    <input
                      type="date"
                      className="input"
                      value={vacForm.nextDueDate}
                      onChange={(e) =>
                        setVacForm({ ...vacForm, nextDueDate: e.target.value })
                      }
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-full justify-center"
                  disabled={vacLoading}
                >
                  {vacLoading ? "Saving Vaccine..." : "Save Vaccine Record"}
                </button>
              </form>
            </div>
          )}

          {/* Vaccination History Log */}
          <div className="card p-6">
            <h3 className="font-semibold text-slate-900 mb-4">
              Vaccination History & Upcoming Dues
            </h3>
            <div className="space-y-3">
              {vaccinationLogs.map((vl) => (
                <div
                  key={vl.id}
                  className="p-3.5 rounded-xl border border-slate-200 bg-slate-50"
                >
                  <div className="flex items-center justify-between">
                    <p className="font-bold text-sm text-slate-900">
                      {vl.vaccineName}
                    </p>
                    <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-md">
                      COMPLETED
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs text-slate-500 mt-1">
                    <span>
                      Given:{" "}
                      {vl.dateGiven
                        ? new Date(vl.dateGiven).toLocaleDateString("en-IN", {
                            day: "numeric",
                            month: "short",
                            year: "numeric",
                          })
                        : "Registration"}
                    </span>
                    {vl.nextDueDate && (
                      <span className="text-amber-700 font-medium">
                        Next Due:{" "}
                        {new Date(vl.nextDueDate).toLocaleDateString("en-IN", {
                          day: "numeric",
                          month: "short",
                          year: "numeric",
                        })}
                      </span>
                    )}
                  </div>
                </div>
              ))}

              {vaccinationLogs.length === 0 && (
                <p className="text-slate-400 text-sm text-center py-6">
                  No vaccination history on file.
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Vet Tab */}
      {tab === "vet" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {farmerRole && (
            <div className="card p-6 space-y-4">
              <div>
                <h3 className="font-semibold text-slate-900 text-base">
                  Request Doctor / Vet Visit
                </h3>
                {localVetCases.some((c) => c.status === "open" || c.status === "in_progress") && (
                  <p className="text-[11px] text-amber-700 font-medium mt-1">
                    ℹ️ An open visit request is currently active. Submitting below will update your doctor selection and symptoms.
                  </p>
                )}
              </div>

              {vetReqMsg && (
                <div className={`p-3.5 rounded-xl text-xs font-semibold ${vetReqMsg.includes("Failed") || vetReqMsg.includes("error") ? "bg-red-50 text-red-900 border border-red-200" : "bg-emerald-50 text-emerald-900 border border-emerald-200"}`}>
                  {vetReqMsg}
                </div>
              )}

              <form onSubmit={handleVetRequest} className="space-y-4">
                {/* 1. Choose Veterinarian */}
                <div>
                  <label htmlFor="vet-choice" className="label text-slate-900 font-bold mb-1">
                    Select Veterinarian *
                  </label>
                  <select
                    id="vet-choice"
                    className="input text-xs bg-white font-semibold"
                    value={vetReqForm.vetId}
                    onChange={(e) =>
                      setVetReqForm({ ...vetReqForm, vetId: e.target.value })
                    }
                  >
                                        {availableVets.map((v) => {
                      const isNearby = farmerRegion &&
                        v.assignedRegion?.toLowerCase().trim() === farmerRegion;
                      return (
                        <option key={v.id} value={v.id}>
                          {isNearby ? "📍 " : ""}{v.name} — {v.assignedRegion || "General Coverage"}{isNearby ? " (Nearby)" : ""}
                        </option>
                      );
                    })}
                  </select>
                </div>

                {/* Selected Vet Detail Preview */}
                {(() => {
                  const selectedVet = availableVets.find((v) => v.id === vetReqForm.vetId);
                  if (!selectedVet) return null;
                  return (
                    <div className="p-3 bg-[#f8faf9] rounded-xl border border-slate-200 text-xs flex items-center justify-between">
                      <div>
                        <p className="font-bold text-slate-900">{selectedVet.name}</p>
                        <p className="text-[11px] text-slate-500 font-mono mt-0.5">
                          District: <span className="text-slate-800 font-semibold">{selectedVet.assignedRegion || "General Coverage"}</span>
                          {selectedVet.phone && ` · Tel: ${selectedVet.phone}`}
                        </p>
                        {farmerRegion && selectedVet.assignedRegion?.toLowerCase().trim() === farmerRegion && (
                          <p className="text-[10px] text-emerald-700 font-semibold mt-0.5">📍 Covers your farm area</p>
                        )}
                      </div>
                      <span className="text-[10px] font-mono font-bold px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-full">
                        ✓ ACTIVE DOCTOR
                      </span>
                    </div>
                  );
                })()}

                {/* 2. Urgency Level */}
                <div>
                  <label htmlFor="vet-urgency" className="label text-slate-900 font-bold mb-1">
                    Urgency Level *
                  </label>
                  <select
                    id="vet-urgency"
                    className="input text-xs bg-white font-semibold"
                    value={vetReqForm.urgency}
                    onChange={(e) =>
                      setVetReqForm({ ...vetReqForm, urgency: e.target.value })
                    }
                  >
                    <option value="low">Low — Routine checkup / preventive care</option>
                    <option value="medium">Medium — Health score drop / mild symptoms noticed</option>
                    <option value="high">High — Cow seems sick / high fever / sharp milk drop</option>
                    <option value="critical">Critical — Immediate Emergency</option>
                  </select>
                </div>

                {/* 3. Observed Symptoms */}
                <div>
                  <label htmlFor="vet-symptoms" className="label text-slate-900 font-bold mb-1">
                    What symptoms do you notice? (optional)
                  </label>
                  <textarea
                    id="vet-symptoms"
                    className="input min-h-[80px] resize-none text-xs"
                    placeholder="Describe what you see (e.g. not eating well, low milk, coughing, swelling, fever)..."
                    value={vetReqForm.symptoms}
                    onChange={(e) =>
                      setVetReqForm({ ...vetReqForm, symptoms: e.target.value })
                    }
                  />
                </div>

                <button
                  id="vet-request-submit"
                  type="submit"
                  className="btn btn-primary w-full justify-center text-xs font-bold py-2.5"
                  disabled={vetReqLoading}
                >
                  {vetReqLoading ? "Submitting Request..." : "Request Doctor Visit →"}
                </button>
              </form>
            </div>
          )}

          <div className="card p-6 space-y-4">
            <div>
              <h3 className="font-semibold text-slate-900 text-base">
                Veterinary Case History
              </h3>
            </div>

            <div className="space-y-3">
              {localVetCases.map((c) => (
                <div
                  key={c.id}
                  className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 text-xs space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className={`badge-${c.urgency} text-[10px]`}>{c.urgency.toUpperCase()}</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        c.status === "resolved"
                          ? "text-emerald-800 bg-emerald-100 border border-emerald-300"
                          : "text-amber-800 bg-amber-100 border border-amber-300"
                      }`}
                    >
                      {c.status === "resolved" ? "Resolved" : "Pending Doctor Visit"}
                    </span>
                  </div>
                  {c.diagnosis && (
                    <p className="text-xs text-slate-800 pt-1 font-medium">
                      <span className="font-bold text-slate-900">Diagnosis:</span> {c.diagnosis}
                    </p>
                  )}
                  <p className="text-[11px] text-slate-500 font-mono pt-1 border-t border-slate-200/60 flex items-center justify-between">
                    <span>{new Date(c.createdAt).toLocaleDateString("en-IN")}</span>
                    <span className="font-bold text-slate-800">{c.vetName ? `Dr. ${c.vetName.replace(/^Dr\.\s*/i, "")}` : "Awaiting Doctor"}</span>
                  </p>
                </div>
              ))}
              {localVetCases.length === 0 && (
                <div className="p-8 text-center text-slate-400 text-xs">
                  No veterinary visits on record for this animal.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

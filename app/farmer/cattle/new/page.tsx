"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  CATTLE_BREEDS,
  TAMIL_NADU_REGIONS,
  COMMON_VACCINES,
  CATTLE_PURPOSES,
} from "@/lib/constants";

export default function AddCattlePage() {
  const router = useRouter();

  // 1. One-time registration fields (saved once, static)
  const [form, setForm] = useState({
    tagId: "",
    name: "",
    breed: "",
    gender: "female",
    ageInputType: "dob" as "dob" | "approxAge",
    dateOfBirth: "",
    approxAge: "", // in years
    photo: "",
    region: "",
    purpose: "dairy" as "dairy" | "breeding" | "draft",
    previousCalvings: 0,
    pastVaccinations: [] as string[],
    customVaccine: "",
    initialWeight: "",
    initialMilkYield: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [qrDataUrl, setQrDataUrl] = useState<string | null>(null);
  const [createdId, setCreatedId] = useState<string | null>(null);

  const generateTagId = () => {
    const randomNum = Math.floor(1000 + Math.random() * 9000);
    return `TN-SC-${randomNum}`;
  };

  useEffect(() => {
    setForm((prev) => {
      if (!prev.tagId) {
        return { ...prev, tagId: generateTagId() };
      }
      return prev;
    });
  }, []);

  const toggleVaccine = (vaccine: string) => {
    setForm((prev) => {
      const exists = prev.pastVaccinations.includes(vaccine);
      return {
        ...prev,
        pastVaccinations: exists
          ? prev.pastVaccinations.filter((v) => v !== vaccine)
          : [...prev.pastVaccinations, vaccine],
      };
    });
  };

  const addCustomVaccine = () => {
    if (!form.customVaccine.trim()) return;
    const val = form.customVaccine.trim();
    if (!form.pastVaccinations.includes(val)) {
      setForm((prev) => ({
        ...prev,
        pastVaccinations: [...prev.pastVaccinations, val],
        customVaccine: "",
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Prepare payload
    const payload = {
      tagId: form.tagId.trim(),
      name: form.name.trim() || undefined,
      breed: form.breed,
      gender: form.gender,
      dob: form.ageInputType === "dob" ? form.dateOfBirth : undefined,
      approxAge:
        form.ageInputType === "approxAge" ? parseFloat(form.approxAge) : undefined,
      photo: form.photo.trim() || undefined,
      region: form.region || undefined,
      purpose: form.purpose,
      previousCalvings: Math.max(0, parseInt(String(form.previousCalvings)) || 0),
      pastVaccinations: form.pastVaccinations,
      initialWeight: parseFloat(form.initialWeight),
      initialMilkYield:
        form.purpose === "dairy" && form.initialMilkYield
          ? parseFloat(form.initialMilkYield)
          : undefined,
    };

    try {
      const res = await fetch("/api/farmer/cattle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        setError(data.error ?? "Failed to register cattle.");
        return;
      }

      setQrDataUrl(data.qrDataUrl);
      setCreatedId(data.cattle.id);
    } catch {
      setLoading(false);
      setError("Network error while submitting registration.");
    }
  };

  if (qrDataUrl && createdId) {
    return (
      <div className="p-8 max-w-lg mx-auto">
        <div className="card p-8 text-center animate-fade-in-up">
          <div className="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 font-bold text-2xl mx-auto mb-3">
            ✓
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mb-2">
            Cattle Registered Successfully!
          </h2>
          <p className="text-slate-500 mb-4 text-sm">
            Initial weight {form.initialWeight} kg{" "}
            {form.purpose === "dairy" && form.initialMilkYield
              ? `and initial milk yield ${form.initialMilkYield} L `
              : ""}
            seeded into Day-1 logs. Baseline calibration is now active (abstaining status).
          </p>

          <div className="bg-slate-50 rounded-2xl p-5 inline-block mb-6 border border-slate-200 shadow-inner">
            <img src={qrDataUrl} alt="QR Code" className="w-52 h-52 mx-auto" />
            <p className="text-xs text-slate-600 font-mono mt-3 font-semibold">
              TAG ID: {form.tagId}
            </p>
            <p className="text-xs text-brand-700 font-medium capitalize mt-0.5">
              Purpose: {form.purpose}
            </p>
          </div>

          <div className="flex gap-3">
            <a
              href={qrDataUrl}
              download={`${form.tagId}-qr.png`}
              className="btn-secondary flex-1 justify-center py-2.5"
            >
              Download QR Tag
            </a>
            <button
              onClick={() => router.push(`/farmer/cattle/${createdId}`)}
              className="btn-primary flex-1 py-2.5"
            >
              View Cattle Profile →
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Add Cattle</h1>
        <p className="text-slate-500 mt-1">
          One-time cattle registration with Day-1 baseline log seeding
        </p>
      </div>

      <div className="card p-6 md:p-8">
        {error && (
          <div className="mb-5 p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Section 1: Identification */}
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
              1. Static Identification
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label htmlFor="cattle-tagid" className="label mb-0">
                    Tag ID *
                  </label>
                  <button
                    type="button"
                    onClick={() =>
                      setForm((prev) => ({ ...prev, tagId: generateTagId() }))
                    }
                    className="text-xs text-brand-700 hover:text-brand-800 hover:underline font-semibold flex items-center gap-1"
                    title="Generate new Tag ID"
                  >
                    <span>Auto-generate</span>
                  </button>
                </div>
                <input
                  id="cattle-tagid"
                  type="text"
                  className="input font-mono font-semibold text-brand-900"
                  placeholder="e.g. TN-SC-4891"
                  value={form.tagId}
                  onChange={(e) => setForm({ ...form, tagId: e.target.value })}
                  required
                />
              </div>

              <div>
                <label htmlFor="cattle-name" className="label">
                  Name (optional)
                </label>
                <input
                  id="cattle-name"
                  type="text"
                  className="input"
                  placeholder="e.g. Kamla / Lakshmi"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label htmlFor="cattle-breed" className="label">
                  Breed *
                </label>
                <select
                  id="cattle-breed"
                  className="input"
                  value={form.breed}
                  onChange={(e) => setForm({ ...form, breed: e.target.value })}
                  required
                >
                  <option value="">Select breed</option>
                  {CATTLE_BREEDS.map((b) => (
                    <option key={b} value={b}>
                      {b}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="cattle-gender" className="label">
                  Gender *
                </label>
                <select
                  id="cattle-gender"
                  className="input"
                  value={form.gender}
                  onChange={(e) => setForm({ ...form, gender: e.target.value })}
                >
                  <option value="female">Female (Cow / Heifer)</option>
                  <option value="male">Male (Bull / Steer)</option>
                </select>
              </div>
            </div>

            {/* Age Selection: Date of Birth OR Approx Age */}
            <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-slate-700">
                  Animal Age / Date of Birth *
                </span>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setForm({ ...form, ageInputType: "dob" })}
                    className={`text-xs px-2.5 py-1 rounded-lg font-medium transition-all ${
                      form.ageInputType === "dob"
                        ? "bg-brand-950 text-white"
                        : "bg-white text-slate-600 border border-slate-200"
                    }`}
                  >
                    Exact Date
                  </button>
                  <button
                    type="button"
                    onClick={() => setForm({ ...form, ageInputType: "approxAge" })}
                    className={`text-xs px-2.5 py-1 rounded-lg font-medium transition-all ${
                      form.ageInputType === "approxAge"
                        ? "bg-brand-950 text-white"
                        : "bg-white text-slate-600 border border-slate-200"
                    }`}
                  >
                    Approx. Age
                  </button>
                </div>
              </div>

              {form.ageInputType === "dob" ? (
                <div>
                  <input
                    id="cattle-dob"
                    type="date"
                    className="input bg-white"
                    max={new Date().toISOString().split("T")[0]}
                    value={form.dateOfBirth}
                    onChange={(e) =>
                      setForm({ ...form, dateOfBirth: e.target.value })
                    }
                    required={form.ageInputType === "dob"}
                  />
                  <p className="text-[11px] text-slate-400 mt-1">
                    Age group (calf, adult, senior) will be derived automatically.
                  </p>
                </div>
              ) : (
                <div>
                  <div className="relative">
                    <input
                      id="cattle-approx-age"
                      type="number"
                      step="0.1"
                      min="0.1"
                      max="30"
                      className="input bg-white pr-16"
                      placeholder="e.g. 3.5"
                      value={form.approxAge}
                      onChange={(e) =>
                        setForm({ ...form, approxAge: e.target.value })
                      }
                      required={form.ageInputType === "approxAge"}
                    />
                    <span className="absolute right-3 top-2.5 text-xs text-slate-400 font-medium">
                      years
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-1">
                    Enter approximate age in years (e.g. 0.5 for 6-month calf).
                  </p>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label htmlFor="cattle-photo" className="label">
                  Photo URL (optional)
                </label>
                <input
                  id="cattle-photo"
                  type="url"
                  className="input"
                  placeholder="https://..."
                  value={form.photo}
                  onChange={(e) => setForm({ ...form, photo: e.target.value })}
                />
              </div>

              <div>
                <label htmlFor="cattle-region" className="label">
                  Region / District
                </label>
                <select
                  id="cattle-region"
                  className="input"
                  value={form.region}
                  onChange={(e) => setForm({ ...form, region: e.target.value })}
                >
                  <option value="">Select District</option>
                  {TAMIL_NADU_REGIONS.map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Section 2: Purpose & Historical Facts */}
          <div className="pt-4 border-t border-slate-100">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
              2. Purpose & Historical Facts
            </h3>

            <div>
              <label className="label">Animal Purpose *</label>
              <div className="grid grid-cols-3 gap-3">
                {CATTLE_PURPOSES.map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setForm({ ...form, purpose: p })}
                    className={`p-3 rounded-xl border text-center font-medium capitalize transition-all ${
                      form.purpose === p
                        ? "bg-brand-950 text-white border-brand-950 shadow-sm"
                        : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
              <p className="text-[11px] text-slate-400 mt-1">
                {form.purpose === "dairy"
                  ? "Dairy cattle tracks daily milk yield and weights milk drop heavily in CHDI scoring."
                  : form.purpose === "breeding"
                  ? "Breeding cattle tracks reproductive status, calvings, and weight."
                  : "Draft animals track physical stamina, activity, and weight."}
              </p>
            </div>

            <div className="mt-4">
              <label htmlFor="cattle-calvings" className="label">
                Previous Calvings (historical fact, static)
              </label>
              <input
                id="cattle-calvings"
                type="number"
                min="0"
                step="1"
                className="input"
                placeholder="0"
                value={form.previousCalvings}
                onChange={(e) =>
                  setForm({
                    ...form,
                    previousCalvings: parseInt(e.target.value) || 0,
                  })
                }
              />
              <p className="text-[11px] text-slate-400 mt-1">
                Number of past deliveries prior to registration. Not a recurring field.
              </p>
            </div>

            {/* Past Vaccinations (historical list, static) */}
            <div className="mt-4">
              <label className="label">
                Past Vaccinations Received (historical list)
              </label>
              <div className="space-y-2 max-h-48 overflow-y-auto p-3 rounded-xl bg-slate-50 border border-slate-200">
                {COMMON_VACCINES.map((vac) => (
                  <label
                    key={vac}
                    className="flex items-center gap-2.5 text-xs text-slate-700 cursor-pointer hover:text-slate-900"
                  >
                    <input
                      type="checkbox"
                      checked={form.pastVaccinations.includes(vac)}
                      onChange={() => toggleVaccine(vac)}
                      className="rounded text-brand-900 focus:ring-brand-500 w-4 h-4"
                    />
                    <span>{vac}</span>
                  </label>
                ))}
              </div>

              {/* Add custom vaccine */}
              <div className="flex gap-2 mt-2">
                <input
                  type="text"
                  placeholder="Other vaccine..."
                  className="input text-xs py-1.5"
                  value={form.customVaccine}
                  onChange={(e) =>
                    setForm({ ...form, customVaccine: e.target.value })
                  }
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addCustomVaccine();
                    }
                  }}
                />
                <button
                  type="button"
                  onClick={addCustomVaccine}
                  className="btn-secondary text-xs px-3 py-1.5"
                >
                  + Add
                </button>
              </div>

              {form.pastVaccinations.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {form.pastVaccinations.map((v) => (
                    <span
                      key={v}
                      className="inline-flex items-center gap-1 text-xs bg-brand-50 text-brand-900 border border-brand-200 px-2 py-0.5 rounded-lg"
                    >
                      {v}
                      <button
                        type="button"
                        onClick={() => toggleVaccine(v)}
                        className="text-brand-600 hover:text-red-500 font-bold ml-1"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Section 3: Day-1 Log Seeding */}
          <div className="pt-4 border-t border-slate-100">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                3. Day-1 Log Entries
              </h3>
              <span className="text-[11px] font-semibold text-brand-700 bg-brand-50 px-2 py-0.5 rounded-md border border-brand-200">
                Seeded into Log Tables
              </span>
            </div>
            <p className="text-xs text-slate-500 mb-3">
              These initial values will be automatically inserted as the first records
              in the animal&apos;s recurring log tables, not stored as static cattle fields.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="cattle-weight" className="label">
                  Initial Weight (kg) *
                </label>
                <input
                  id="cattle-weight"
                  type="number"
                  step="0.5"
                  min="20"
                  max="1200"
                  className="input font-semibold"
                  placeholder="e.g. 380"
                  value={form.initialWeight}
                  onChange={(e) =>
                    setForm({ ...form, initialWeight: e.target.value })
                  }
                  required
                />
                <p className="text-[11px] text-slate-400 mt-1">
                  First entry in <span className="font-mono text-slate-600">WeightLog</span>
                </p>
              </div>

              {form.purpose === "dairy" ? (
                <div>
                  <label htmlFor="cattle-milkyield" className="label">
                    Initial Daily Milk Yield (L/day)
                  </label>
                  <input
                    id="cattle-milkyield"
                    type="number"
                    step="0.1"
                    min="0"
                    max="60"
                    className="input font-semibold"
                    placeholder="e.g. 12.5"
                    value={form.initialMilkYield}
                    onChange={(e) =>
                      setForm({ ...form, initialMilkYield: e.target.value })
                    }
                  />
                  <p className="text-[11px] text-slate-400 mt-1">
                    First entry in <span className="font-mono text-slate-600">MilkLog</span> (Dairy only)
                  </p>
                </div>
              ) : (
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center text-xs text-slate-500">
                  <span>
                    Milk yield logging is not applicable for {form.purpose} purpose cattle.
                  </span>
                </div>
              )}
            </div>
          </div>

          <div className="flex gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => router.back()}
              className="btn-secondary flex-1"
            >
              Cancel
            </button>
            <button
              id="add-cattle-submit"
              type="submit"
              className="btn-primary flex-1 btn-lg justify-center"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Registering...
                </>
              ) : (
                "Add & Generate QR →"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

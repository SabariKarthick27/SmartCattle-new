"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  CATTLE_BREEDS,
  TAMIL_NADU_REGIONS,
  COMMON_VACCINES,
  CATTLE_PURPOSES,
} from "@/lib/constants";

interface CattleData {
  id: string;
  tagId: string;
  name: string;
  breed: string;
  gender: string;
  dob: string;
  approxAge: string;
  purpose: string;
  region: string;
  previousCalvings: number;
  pastVaccinations: string[];
  photoUrl: string;
  isActive: boolean;
}

export default function EditCattleForm({ cattle }: { cattle: CattleData }) {
  const router = useRouter();

  const [form, setForm] = useState({
    tagId: cattle.tagId,
    name: cattle.name,
    breed: cattle.breed,
    gender: cattle.gender,
    ageInputType: (cattle.dob ? "dob" : "approxAge") as "dob" | "approxAge",
    dateOfBirth: cattle.dob,
    approxAge: cattle.approxAge,
    photoUrl: cattle.photoUrl,
    region: cattle.region,
    purpose: cattle.purpose as "dairy" | "breeding" | "draft",
    previousCalvings: cattle.previousCalvings,
    pastVaccinations: [...cattle.pastVaccinations],
    customVaccine: "",
    isActive: cattle.isActive,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

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

  const removeVaccine = (vaccine: string) => {
    setForm((prev) => ({
      ...prev,
      pastVaccinations: prev.pastVaccinations.filter((v) => v !== vaccine),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccessMsg("");

    const payload = {
      tagId: form.tagId.trim(),
      name: form.name.trim() || undefined,
      breed: form.breed,
      gender: form.gender,
      dob: form.ageInputType === "dob" ? form.dateOfBirth : undefined,
      approxAge:
        form.ageInputType === "approxAge" ? parseFloat(form.approxAge) : undefined,
      photoUrl: form.photoUrl.trim() || undefined,
      region: form.region || undefined,
      purpose: form.purpose,
      previousCalvings: Math.max(0, parseInt(String(form.previousCalvings)) || 0),
      pastVaccinations: form.pastVaccinations,
      isActive: form.isActive,
    };

    try {
      const res = await fetch(`/api/cattle/${cattle.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        setError(data.error ?? "Failed to update cattle details.");
        return;
      }

      setSuccessMsg("Cattle details updated successfully!");
      setTimeout(() => {
        router.push(`/farmer/cattle/${cattle.id}`);
        router.refresh();
      }, 1000);
    } catch {
      setLoading(false);
      setError("Network error while updating cattle details.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header breadcrumb & title */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-sm text-slate-500 mb-1">
            <Link href="/farmer/cattle" className="hover:text-slate-800 transition-colors">
              My Cattle
            </Link>
            <span>/</span>
            <Link
              href={`/farmer/cattle/${cattle.id}`}
              className="hover:text-slate-800 transition-colors"
            >
              {cattle.name || cattle.tagId}
            </Link>
            <span>/</span>
            <span className="text-slate-800 font-medium">Edit</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">
            Edit Cattle Details
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Modify identification, physical attributes, breed, and health registration facts
          </p>
        </div>

        <Link
          href={`/farmer/cattle/${cattle.id}`}
          className="btn-secondary text-sm"
        >
          Cancel
        </Link>
      </div>

      <div className="card p-6 md:p-8 bg-white shadow-sm border border-slate-200/80 rounded-2xl">
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center gap-3">
            <svg className="w-5 h-5 flex-shrink-0 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {successMsg && (
          <div className="mb-6 p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm flex items-center gap-3 animate-fade-in">
            <svg className="w-5 h-5 flex-shrink-0 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="font-medium">{successMsg} Redirecting...</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Section 1: Identification */}
          <div>
            <div className="flex items-center gap-2 mb-3 pb-2 border-b border-slate-100">
              <span className="w-6 h-6 rounded-full bg-brand-100 text-brand-700 font-bold text-xs flex items-center justify-center">
                1
              </span>
              <h3 className="text-sm font-semibold text-slate-800">
                Identification & Basic Info
              </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="cattle-tagid" className="label">
                  Tag ID *
                </label>
                <input
                  id="cattle-tagid"
                  type="text"
                  className="input font-mono font-semibold text-brand-900"
                  placeholder="e.g. TN-SC-4891"
                  value={form.tagId}
                  onChange={(e) => setForm({ ...form, tagId: e.target.value })}
                  required
                />
                <p className="text-[11px] text-slate-400 mt-1">
                  Official ear tag identifier. Unique per animal.
                </p>
              </div>

              <div>
                <label htmlFor="cattle-name" className="label">
                  Animal Name / Pet Name
                </label>
                <input
                  id="cattle-name"
                  type="text"
                  className="input"
                  placeholder="e.g. Lakshmi / Kamla"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
                <p className="text-[11px] text-slate-400 mt-1">
                  Optional friendly name to identify the cattle easily.
                </p>
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
            <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200/80">
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
                        ? "bg-brand-950 text-white shadow-sm"
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
                        ? "bg-brand-950 text-white shadow-sm"
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
                    Age group (calf, adult, senior) is updated automatically from birth date.
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
                    Enter approximate age in years (e.g. 0.5 for a 6-month calf, 3 for 3-year adult).
                  </p>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
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

              <div>
                <label htmlFor="cattle-photo" className="label">
                  Photo URL (optional)
                </label>
                <input
                  id="cattle-photo"
                  type="url"
                  className="input"
                  placeholder="https://images.unsplash.com/..."
                  value={form.photoUrl}
                  onChange={(e) => setForm({ ...form, photoUrl: e.target.value })}
                />
              </div>
            </div>
          </div>

          {/* Section 2: Purpose & Reproduction */}
          <div className="pt-2">
            <div className="flex items-center gap-2 mb-3 pb-2 border-b border-slate-100">
              <span className="w-6 h-6 rounded-full bg-brand-100 text-brand-700 font-bold text-xs flex items-center justify-center">
                2
              </span>
              <h3 className="text-sm font-semibold text-slate-800">
                Purpose & History
              </h3>
            </div>

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
                  ? "Dairy: Tracks daily milk yield and milk drops in CHDI scoring."
                  : form.purpose === "breeding"
                  ? "Breeding: Tracks reproductive status, calvings, and health."
                  : "Draft: Tracks activity stamina and physical weight."}
              </p>
            </div>

            <div className="mt-4">
              <label htmlFor="cattle-calvings" className="label">
                Previous Calvings
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
                Number of deliveries prior to or during ownership.
              </p>
            </div>

            {/* Past Vaccinations */}
            <div className="mt-4">
              <label className="label">
                Past Vaccinations Received
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                {COMMON_VACCINES.map((vac) => {
                  const selected = form.pastVaccinations.includes(vac);
                  return (
                    <button
                      key={vac}
                      type="button"
                      onClick={() => toggleVaccine(vac)}
                      className={`text-left text-xs p-2.5 rounded-xl border flex items-center justify-between transition-all ${
                        selected
                          ? "bg-brand-50 border-brand-300 text-brand-900 font-medium"
                          : "bg-slate-50/70 border-slate-200 text-slate-600 hover:bg-slate-100/70"
                      }`}
                    >
                      <span className="truncate pr-2">{vac}</span>
                      <span
                        className={`w-4 h-4 rounded flex items-center justify-center text-[10px] flex-shrink-0 ${
                          selected
                            ? "bg-brand-600 text-white font-bold"
                            : "border border-slate-300 bg-white"
                        }`}
                      >
                        {selected ? "✓" : ""}
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Custom Vaccines Display */}
              {form.pastVaccinations.some(
                (v) => !(COMMON_VACCINES as readonly string[]).includes(v)
              ) && (
                <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-slate-100">
                  {form.pastVaccinations
                    .filter((v) => !(COMMON_VACCINES as readonly string[]).includes(v))
                    .map((cv) => (
                      <span
                        key={cv}
                        className="inline-flex items-center gap-1.5 text-xs bg-brand-100 text-brand-800 px-2.5 py-1 rounded-lg"
                      >
                        {cv}
                        <button
                          type="button"
                          onClick={() => removeVaccine(cv)}
                          className="hover:text-red-600 font-bold"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                </div>
              )}

              {/* Add other vaccine input */}
              <div className="flex gap-2 mt-3">
                <input
                  type="text"
                  className="input text-xs"
                  placeholder="Other vaccine name..."
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
                  className="btn-secondary text-xs px-3 whitespace-nowrap"
                >
                  + Add
                </button>
              </div>
            </div>
          </div>

          {/* Section 3: Status / Activity */}
          <div className="pt-2">
            <div className="flex items-center gap-2 mb-3 pb-2 border-b border-slate-100">
              <span className="w-6 h-6 rounded-full bg-brand-100 text-brand-700 font-bold text-xs flex items-center justify-center">
                3
              </span>
              <h3 className="text-sm font-semibold text-slate-800">
                Status
              </h3>
            </div>

            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50 flex items-center justify-between">
              <div>
                <span className="text-sm font-semibold text-slate-800">
                  Active Herd Member
                </span>
                <p className="text-xs text-slate-500 mt-0.5">
                  Inactive cattle are archived from active monitoring and daily baseline tracking.
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={form.isActive}
                  onChange={(e) =>
                    setForm({ ...form, isActive: e.target.checked })
                  }
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-600"></div>
              </label>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-3 pt-6 border-t border-slate-100">
            <Link
              href={`/farmer/cattle/${cattle.id}`}
              className="btn-secondary py-2.5 px-5"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary py-2.5 px-6 font-semibold shadow-sm flex items-center gap-2 disabled:opacity-60"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                  </svg>
                  <span>Saving Changes...</span>
                </>
              ) : (
                <>
                  <span>Save Changes</span>
                  <span>→</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

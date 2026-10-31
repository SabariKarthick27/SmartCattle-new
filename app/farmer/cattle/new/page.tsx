"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  CATTLE_BREEDS,
  TAMIL_NADU_REGIONS,
  COMMON_VACCINES,
  CATTLE_PURPOSES,
} from "@/lib/constants";
import { IconCow } from "@/components/icons";

export default function AddCattlePage() {
  const router = useRouter();

  // One-time registration fields
  const [form, setForm] = useState({
    tagId: "",
    name: "",
    breed: "",
    gender: "female",
    dateOfBirth: "",
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

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      alert("Image size should be under 5MB");
      return;
    }
    const reader = new FileReader();
    reader.onloadend = () => {
      setForm((prev) => ({ ...prev, photo: reader.result as string }));
    };
    reader.readAsDataURL(file);
  };

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
      dob: form.dateOfBirth,
      photo: form.photo || undefined,
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
        setError(data.error ?? "Failed to add cow.");
        return;
      }

      setQrDataUrl(data.qrDataUrl);
      setCreatedId(data.cattle.id);
    } catch {
      setLoading(false);
      setError("Network error while submitting.");
    }
  };

  if (qrDataUrl && createdId) {
    return (
      <div className="p-4 sm:p-8 max-w-lg mx-auto space-y-6">
        <div className="card p-6 sm:p-8 text-center bg-white border border-slate-300 shadow-lg rounded-xl space-y-4">
          <div className="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-800 font-bold text-2xl mx-auto">
            ✓
          </div>
          <h2 className="text-2xl font-bold text-slate-900 font-display">
            Cow Registered Successfully!
          </h2>
          <p className="text-slate-600 text-xs">
            Tag <strong>{form.tagId}</strong> has been created. Initial weight of {form.initialWeight} kg{" "}
            {form.purpose === "dairy" && form.initialMilkYield ? `and daily milk of ${form.initialMilkYield} L ` : ""}
            recorded.
          </p>

          <div className="bg-slate-50 rounded-xl p-5 inline-block border border-slate-200">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={qrDataUrl} alt="QR Code" className="w-48 h-48 mx-auto" />
            <p className="text-xs text-slate-900 font-mono mt-3 font-bold">
              EAR TAG: {form.tagId}
            </p>
            <p className="text-xs text-emerald-800 font-medium capitalize mt-0.5">
              {form.name ? `${form.name} · ` : ""}{form.breed} ({form.purpose})
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <a
              href={qrDataUrl}
              download={`${form.tagId}-qr.png`}
              className="btn btn-secondary flex-1 justify-center py-2 text-xs"
            >
              Download QR Tag
            </a>
            <button
              onClick={() => router.push(`/farmer/cattle/${createdId}`)}
              className="btn btn-primary flex-1 justify-center py-2 text-xs font-bold"
            >
              View Cow Profile →
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-2xl mx-auto space-y-6">
      <div className="pb-4 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
            Add New Cattle
          </h1>
          <span className="text-xs font-mono font-bold px-2 py-0.5 bg-emerald-100 text-emerald-900 rounded">
            REGISTRATION
          </span>
        </div>
      </div>

      <div className="card p-6 bg-white border border-slate-300 shadow-xs rounded-xl">
        {error && (
          <div className="mb-5 p-3.5 rounded-lg bg-red-50 border border-red-200 text-red-800 text-xs font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Section 1: Identification */}
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">
              1. Tag &amp; Breed Details
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label htmlFor="cattle-tagid" className="label mb-0">
                    Ear Tag ID *
                  </label>
                  <button
                    type="button"
                    onClick={() => setForm((prev) => ({ ...prev, tagId: generateTagId() }))}
                    className="text-xs text-emerald-900 hover:underline font-semibold"
                  >
                    Generate Tag
                  </button>
                </div>
                <input
                  id="cattle-tagid"
                  type="text"
                  className="input font-mono font-bold"
                  placeholder="e.g. TN-SC-4891"
                  value={form.tagId}
                  onChange={(e) => setForm({ ...form, tagId: e.target.value })}
                  required
                />
              </div>

              <div>
                <label htmlFor="cattle-name" className="label">
                  Cow Name (Optional)
                </label>
                <input
                  id="cattle-name"
                  type="text"
                  className="input"
                  placeholder="e.g. Lakshmi / Ganga"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                  <option value="">Select Breed</option>
                  {CATTLE_BREEDS.map((b) => (
                    <option key={b} value={b}>{b}</option>
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
                  <option value="male">Male (Bull / Ox)</option>
                </select>
              </div>
            </div>

            {/* Birthday */}
            <div>
              <label htmlFor="cattle-dob" className="label">
                Birthday / Date of Birth *
              </label>
              <input
                id="cattle-dob"
                type="date"
                className="input bg-white"
                max={new Date().toISOString().split("T")[0]}
                value={form.dateOfBirth}
                onChange={(e) => setForm({ ...form, dateOfBirth: e.target.value })}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="cattle-region" className="label">
                  District / Location
                </label>
                <select
                  id="cattle-region"
                  className="input"
                  value={form.region}
                  onChange={(e) => setForm({ ...form, region: e.target.value })}
                >
                  <option value="">Select District</option>
                  {TAMIL_NADU_REGIONS.map((r) => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="cattle-calvings" className="label">
                  Past Deliveries / Calvings
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
                    setForm({ ...form, previousCalvings: parseInt(e.target.value) || 0 })
                  }
                />
              </div>
            </div>

            {/* Cow Photo Upload */}
            <div>
              <label className="label">Cow Photo (Optional)</label>
              {form.photo ? (
                <div className="flex items-center gap-4 p-3 bg-[#f8faf9] border border-slate-200 rounded-xl">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={form.photo}
                    alt="Uploaded preview"
                    className="w-16 h-16 object-cover rounded-lg border border-slate-300 shadow-xs"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-slate-800 truncate">Photo selected</p>
                    <p className="text-[11px] text-slate-500">Ready to save</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setForm((prev) => ({ ...prev, photo: "" }))}
                    className="text-xs text-red-600 hover:text-red-800 font-semibold px-2.5 py-1.5 rounded-md hover:bg-red-50 transition-colors cursor-pointer"
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <label className="flex flex-col items-center justify-center p-4 border-2 border-dashed border-slate-300 hover:border-emerald-700 hover:bg-emerald-50/40 rounded-xl cursor-pointer transition-all bg-white text-center">
                  <svg className="w-8 h-8 text-slate-400 mb-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
                  </svg>
                  <span className="text-xs font-bold text-slate-700">Click to upload photo from your device</span>
                  <span className="text-[11px] text-slate-500 mt-0.5">PNG, JPG, JPEG or WEBP (Max 5MB)</span>
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handlePhotoUpload}
                  />
                </label>
              )}
            </div>
          </div>

          {/* Section 2: Purpose */}
          <div className="pt-4 border-t border-slate-200 space-y-3">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">
              2. Purpose
            </h3>

            <div>
              <div className="grid grid-cols-3 gap-3">
                {CATTLE_PURPOSES.map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setForm({ ...form, purpose: p })}
                    className={`p-3 rounded-lg border text-center text-xs font-bold capitalize transition-all ${
                      form.purpose === p
                        ? "bg-[#123326] text-white border-[#0b2219] shadow-xs"
                        : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                    }`}
                  >
                    {p === "dairy" ? "🥛 Dairy (Milk)" : p === "breeding" ? "🧬 Breeding" : "🚜 Draft (Work)"}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Section 3: Vaccine History */}
          <div className="pt-4 border-t border-slate-200 space-y-3">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">
              3. Past Vaccines Given
            </h3>

            <div className="space-y-1.5 max-h-40 overflow-y-auto p-3 rounded-lg bg-[#f8faf9] border border-slate-200">
              {COMMON_VACCINES.map((vac) => (
                <label
                  key={vac}
                  className="flex items-center gap-2.5 text-xs text-slate-700 cursor-pointer hover:text-slate-900"
                >
                  <input
                    type="checkbox"
                    checked={form.pastVaccinations.includes(vac)}
                    onChange={() => toggleVaccine(vac)}
                    className="rounded text-emerald-900 focus:ring-emerald-700 w-4 h-4"
                  />
                  <span>{vac}</span>
                </label>
              ))}
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Other vaccine name..."
                className="input text-xs py-1.5 flex-1"
                value={form.customVaccine}
                onChange={(e) => setForm({ ...form, customVaccine: e.target.value })}
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
                className="btn btn-secondary text-xs px-3 py-1.5"
              >
                + Add Vaccine
              </button>
            </div>
          </div>

          {/* Section 4: Initial measurements */}
          <div className="pt-4 border-t border-slate-200 space-y-3">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">
              4. Today&apos;s First Measurements
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="cattle-weight" className="label">
                  Weight Today (kg) *
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
                  onChange={(e) => setForm({ ...form, initialWeight: e.target.value })}
                  required
                />
              </div>

              {form.purpose === "dairy" && (
                <div>
                  <label htmlFor="cattle-milkyield" className="label">
                    Milk Yield Today (Litres/day)
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
                    onChange={(e) => setForm({ ...form, initialMilkYield: e.target.value })}
                  />
                </div>
              )}
            </div>
          </div>

          <div className="flex gap-3 pt-4 border-t border-slate-200">
            <button
              type="button"
              onClick={() => router.back()}
              className="btn btn-secondary flex-1 text-xs"
            >
              Cancel
            </button>
            <button
              id="add-cattle-submit"
              type="submit"
              className="btn btn-primary flex-1 btn-lg justify-center font-bold text-xs"
              disabled={loading}
            >
              {loading ? (
                <span className="inline-flex items-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Saving...
                </span>
              ) : (
                "Save & Generate QR Tag →"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

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
import { IconTrash } from "@/components/icons";

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
    dateOfBirth: cattle.dob ? new Date(cattle.dob).toISOString().split("T")[0] : "",
    photoUrl: cattle.photoUrl || "",
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

  const [deleting, setDeleting] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      alert("Image size should be under 5MB");
      return;
    }
    const reader = new FileReader();
    reader.onloadend = () => {
      setForm((prev) => ({ ...prev, photoUrl: reader.result as string }));
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

  const removeVaccine = (vaccine: string) => {
    setForm((prev) => ({
      ...prev,
      pastVaccinations: prev.pastVaccinations.filter((v) => v !== vaccine),
    }));
  };

  const handleDeleteCattle = async () => {
    setDeleting(true);
    setError("");

    try {
      const res = await fetch(`/api/cattle/${cattle.id}`, {
        method: "DELETE",
      });

      const data = await res.json();
      setDeleting(false);

      if (!res.ok) {
        setError(data.error ?? "Failed to delete cow.");
        setShowDeleteModal(false);
        return;
      }

      router.push("/farmer/cattle");
      router.refresh();
    } catch {
      setDeleting(false);
      setShowDeleteModal(false);
      setError("Network error while deleting cow.");
    }
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
      dob: form.dateOfBirth,
      photoUrl: form.photoUrl || undefined,
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
        setError(data.error ?? "Failed to save changes.");
        return;
      }

      setSuccessMsg("Cow details updated successfully!");
      setTimeout(() => {
        router.push(`/farmer/cattle/${cattle.id}`);
        router.refresh();
      }, 1000);
    } catch {
      setLoading(false);
      setError("Network error while updating details.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header breadcrumb & title */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-slate-500 mb-1">
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
            <span className="text-slate-800 font-bold">Edit</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-950 font-display">
            Edit Cow Details
          </h1>
        </div>

        <Link
          href={`/farmer/cattle/${cattle.id}`}
          className="btn btn-secondary btn-sm text-xs"
        >
          ← Back to Cow Profile
        </Link>
      </div>

      {error && (
        <div className="p-3.5 rounded-lg bg-red-50 text-red-900 border border-red-300 font-medium text-xs">
          {error}
        </div>
      )}

      {successMsg && (
        <div className="p-3.5 rounded-lg bg-emerald-50 text-emerald-900 border border-emerald-300 font-medium text-xs">
          {successMsg}
        </div>
      )}

      <div className="card p-6 sm:p-8 bg-white border border-slate-300 shadow-sm rounded-xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Section 1: Basic identity */}
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">
              1. Basic Identity
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="cattle-tagid" className="label">
                  Tag ID / Ear Tag Number *
                </label>
                <input
                  id="cattle-tagid"
                  type="text"
                  className="input font-mono font-bold"
                  value={form.tagId}
                  onChange={(e) => setForm({ ...form, tagId: e.target.value })}
                  required
                />
              </div>

              <div>
                <label htmlFor="cattle-name" className="label">
                  Cow Name / Nickname (optional)
                </label>
                <input
                  id="cattle-name"
                  type="text"
                  className="input"
                  placeholder="e.g. Lakshmi"
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
                onChange={(e) =>
                  setForm({ ...form, dateOfBirth: e.target.value })
                }
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
              {form.photoUrl ? (
                <div className="flex items-center gap-4 p-3 bg-[#f8faf9] border border-slate-200 rounded-xl">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={form.photoUrl}
                    alt="Uploaded preview"
                    className="w-16 h-16 object-cover rounded-lg border border-slate-300 shadow-xs"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-slate-800 truncate">Photo selected</p>
                    <p className="text-[11px] text-slate-500">Ready to save</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setForm((prev) => ({ ...prev, photoUrl: "" }))}
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
              2. Purpose &amp; Deliveries
            </h3>

            <div>
              <div className="grid grid-cols-3 gap-3">
                {CATTLE_PURPOSES.map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setForm({ ...form, purpose: p })}
                    className={`p-3 rounded-lg border text-center text-xs font-bold capitalize transition-all cursor-pointer ${
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
                    className="rounded text-emerald-900 focus:ring-emerald-700 w-4 h-4 cursor-pointer"
                  />
                  <span>{vac}</span>
                </label>
              ))}
            </div>

            {/* Existing custom vaccines tag list */}
            {form.pastVaccinations.filter((v) => !(COMMON_VACCINES as readonly string[]).includes(v)).length > 0 && (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {form.pastVaccinations
                  .filter((v) => !(COMMON_VACCINES as readonly string[]).includes(v))
                  .map((vac) => (
                    <span
                      key={vac}
                      className="inline-flex items-center gap-1.5 text-xs bg-slate-100 text-slate-800 px-2.5 py-1 rounded-md border border-slate-200"
                    >
                      {vac}
                      <button
                        type="button"
                        onClick={() => removeVaccine(vac)}
                        className="text-slate-400 hover:text-red-600 font-bold ml-1 cursor-pointer"
                        title="Remove vaccine"
                      >
                        ✕
                      </button>
                    </span>
                  ))}
              </div>
            )}

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
                className="btn btn-secondary text-xs px-3 cursor-pointer"
              >
                + Add
              </button>
            </div>
          </div>

          {/* Section 4: Status / Activity */}
          <div className="pt-4 border-t border-slate-200">
            <div className="p-3.5 rounded-lg border border-slate-200 bg-[#f8faf9] flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-slate-900">
                  Active Herd Member
                </span>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  Keep enabled for regular daily tracking and health alerts.
                </p>
              </div>
              <input
                type="checkbox"
                checked={form.isActive}
                onChange={(e) => setForm({ ...form, isActive: e.target.checked })}
                className="w-5 h-5 rounded text-emerald-900 focus:ring-emerald-700 cursor-pointer"
              />
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-between gap-3 pt-4 border-t border-slate-200">
            <button
              type="button"
              onClick={() => setShowDeleteModal(true)}
              className="btn btn-secondary text-red-600 hover:bg-red-50 hover:border-red-300 btn-sm text-xs font-bold flex items-center gap-1.5"
            >
              <IconTrash className="w-3.5 h-3.5" />
              <span>Delete Cow</span>
            </button>
            <div className="flex items-center gap-3">
              <Link
                href={`/farmer/cattle/${cattle.id}`}
                className="btn btn-secondary btn-sm text-xs"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary btn-sm px-5 font-bold text-xs"
              >
                {loading ? "Saving Changes..." : "Save Changes →"}
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs">
          <div className="card max-w-md w-full p-6 bg-white border border-slate-300 shadow-2xl rounded-2xl space-y-4 animate-in fade-in zoom-in-95 duration-150">
            <div className="w-12 h-12 rounded-full bg-red-100 text-red-700 flex items-center justify-center text-xl font-bold mx-auto">
              ⚠️
            </div>
            <div className="text-center space-y-1">
              <h3 className="text-lg font-bold text-slate-950">Delete Cow Record?</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Are you sure you want to permanently delete <strong>{cattle.name || cattle.tagId}</strong> (Tag #{cattle.tagId})? All logged milk, weight, vaccination, and health records for this cow will be permanently removed.
              </p>
            </div>
            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowDeleteModal(false)}
                disabled={deleting}
                className="btn btn-secondary flex-1 text-xs"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDeleteCattle}
                disabled={deleting}
                className="btn bg-red-600 hover:bg-red-700 text-white font-bold flex-1 text-xs justify-center border border-red-700"
              >
                {deleting ? "Deleting..." : "Yes, Delete Cow"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import Link from "next/link";
import { getCHDIBadgeConfig, fmtDate, calcAge } from "@/lib/utils";
import { IconAudit, IconCattle, IconStethoscope } from "@/components/icons";

export default async function HealthRecordsPage() {
  const session = await getServerSession(authOptions);
  if (!session) return null;

  // Fetch all cattle belonging to farmer with logs and cases
  const cattle = await prisma.cattle.findMany({
    where: { farmerId: session.user.id, isActive: true },
    include: {
      chdiHistory: { orderBy: { timestamp: "desc" } },
      weightLogs: { orderBy: { timestamp: "desc" }, take: 5 },
      feedLogs: { orderBy: { timestamp: "desc" }, take: 5 },
      vaccinations: { orderBy: { dueAt: "desc" } },
      vetCases: {
        include: { vet: { select: { name: true, phone: true } } },
        orderBy: { createdAt: "desc" },
      },
    },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="p-8 space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
            <IconAudit className="w-6 h-6 text-brand-700" />
            Health Records & Medical Passports
          </h1>
          <p className="text-slate-500 mt-1">
            Complete digital health history, weight logs, vaccinations, and veterinary reports
          </p>
        </div>
        <div className="flex gap-3">
          <Link href="/farmer/cattle/new" className="btn-primary">
            + Add New Animal
          </Link>
        </div>
      </div>

      {cattle.length === 0 ? (
        <div className="card p-16 text-center">
          <IconCattle className="w-12 h-12 text-slate-400 mx-auto mb-3" />
          <h3 className="text-xl font-bold text-slate-800 mb-2">No Health Records Available</h3>
          <p className="text-slate-500 mb-6">Register your cattle to generate digital health passports and medical logs.</p>
          <Link href="/farmer/cattle/new" className="btn-primary">+ Register First Animal</Link>
        </div>
      ) : (
        <div className="space-y-8">
          {cattle.map((animal) => {
            const latestCHDI = animal.chdiHistory[0];
            const badge = getCHDIBadgeConfig(latestCHDI?.status ?? "abstain");
            const latestWeight = animal.weightLogs[0]?.value;

            return (
              <div key={animal.id} className="card p-6 md:p-8 space-y-6">
                {/* Animal Header */}
                <div className="flex flex-wrap items-start justify-between gap-4 pb-5 border-b border-slate-100">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 bg-brand-100 rounded-2xl flex items-center justify-center font-bold text-brand-700 text-xl">
                      {(animal.name ?? animal.tagId)[0]}
                    </div>
                    <div>
                      <div className="flex items-center gap-3">
                        <h2 className="text-xl font-bold text-slate-900">
                          {animal.name ?? animal.tagId}
                        </h2>
                        <span className={`badge-${latestCHDI?.status ?? "abstain"}`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                          {badge.label}
                        </span>
                      </div>
                      <p className="text-sm text-slate-500 mt-0.5">
                        Tag ID: <span className="font-mono font-semibold text-slate-700">{animal.tagId}</span> · Breed: <span className="font-medium text-slate-700">{animal.breed}</span> · Age: {calcAge(animal.dob)} · District: {animal.region ?? "Tamil Nadu"}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <Link
                      href={`/farmer/cattle/${animal.id}`}
                      className="btn-secondary btn-sm"
                    >
                      View Full Profile →
                    </Link>
                  </div>
                </div>

                {/* Health Metrics Grid */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <p className="text-xs text-slate-500 font-medium">CHDI Health Score</p>
                    <p className={`text-xl font-extrabold mt-1 ${badge.color}`}>
                      {latestCHDI ? `${Math.round(latestCHDI.score)}/100` : "N/A"}
                    </p>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {latestCHDI ? `Updated ${fmtDate(latestCHDI.timestamp)}` : "No history recorded"}
                    </p>
                  </div>

                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <p className="text-xs text-slate-500 font-medium">Body Weight</p>
                    <p className="text-xl font-extrabold text-slate-800 mt-1">
                      {latestWeight ? `${latestWeight} kg` : "Not recorded"}
                    </p>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {animal.weightLogs.length} logs recorded
                    </p>
                  </div>

                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <p className="text-xs text-slate-500 font-medium">Vaccination Status</p>
                    <p className="text-xl font-extrabold text-emerald-700 mt-1">
                      {animal.vaccinations.length > 0 ? animal.vaccinations[0].status.toUpperCase() : "Up to Date"}
                    </p>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {animal.vaccinations.length} records on file
                    </p>
                  </div>

                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <p className="text-xs text-slate-500 font-medium">Vet Consultations</p>
                    <p className="text-xl font-extrabold text-blue-700 mt-1">
                      {animal.vetCases.length} Cases
                    </p>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {animal.vetCases.filter(c => c.status === "open").length} open cases
                    </p>
                  </div>
                </div>

                {/* Veterinary Diagnostic & Treatment History */}
                <div>
                  <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                    <IconStethoscope className="w-4 h-4 text-brand-700" />
                    Veterinary Cases & Prescriptions
                  </h3>
                  {animal.vetCases.length > 0 ? (
                    <div className="overflow-x-auto border border-slate-200 rounded-xl">
                      <table className="w-full text-left text-sm">
                        <thead className="bg-slate-50 text-slate-600 text-xs uppercase font-semibold border-b border-slate-200">
                          <tr>
                            <th className="p-3">Date</th>
                            <th className="p-3">Status</th>
                            <th className="p-3">Symptoms</th>
                            <th className="p-3">Diagnosis</th>
                            <th className="p-3">Treatment / Prescription</th>
                            <th className="p-3">Veterinarian</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 text-slate-700">
                          {animal.vetCases.map((vc) => (
                            <tr key={vc.id} className="hover:bg-slate-50/80">
                              <td className="p-3 text-xs font-mono">{fmtDate(vc.createdAt)}</td>
                              <td className="p-3">
                                <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                                  vc.status === "open" ? "bg-blue-100 text-blue-800" : "bg-emerald-100 text-emerald-800"
                                }`}>
                                  {vc.status}
                                </span>
                              </td>
                              <td className="p-3 text-xs">{vc.symptoms ?? "N/A"}</td>
                              <td className="p-3 text-xs font-medium">{vc.diagnosis ?? "Under Evaluation"}</td>
                              <td className="p-3 text-xs text-emerald-700 font-medium">{vc.treatment ?? "None prescribed"}</td>
                              <td className="p-3 text-xs">{vc.vet?.name ?? "District Vet"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 italic">No veterinary cases reported for this animal.</p>
                  )}
                </div>

                {/* Vaccination History */}
                <div>
                  <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                    <svg className="w-4 h-4 text-brand-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19 14.5M14.25 3.104c.251.023.501.05.75.082M19 14.5a3.75 3.75 0 01-7.5 0" />
                    </svg>
                    Vaccination & Immunization History
                  </h3>
                  {animal.vaccinations.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {animal.vaccinations.map((vac) => (
                        <div key={vac.id} className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                          <div>
                            <p className="font-bold text-slate-900">{vac.vaccineType}</p>
                            <p className="text-slate-500 mt-0.5">Due: {fmtDate(vac.dueAt)}</p>
                          </div>
                          <span className={`px-2.5 py-1 rounded-lg font-bold text-[11px] ${
                            vac.status === "done" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"
                          }`}>
                            {vac.status.toUpperCase()}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 italic">Primary FMD & Brucellosis vaccinations recorded during registration.</p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

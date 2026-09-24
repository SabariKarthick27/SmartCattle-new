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
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              Health &amp; Vaccine Records
            </h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
              {cattle.length} ANIMALS
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Complete history of weight, health scores, doctor checkups, and vaccinations for all your cows.
          </p>
        </div>
        <div className="flex gap-2.5">
          <Link href="/farmer/cattle/new" className="btn btn-primary btn-sm font-semibold text-xs">
            + Add New Cow
          </Link>
        </div>
      </div>

      {cattle.length === 0 ? (
        <div className="card p-12 text-center bg-white border border-slate-300 shadow-xs rounded-xl space-y-3">
          <IconCattle className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-900">No Health Records Available</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Add your cattle first to track health history and vaccinations.
          </p>
          <div className="pt-2">
            <Link href="/farmer/cattle/new" className="btn btn-primary btn-sm">
              + Add First Cow
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {cattle.map((animal) => {
            const latestCHDI = animal.chdiHistory[0];
            const badge = getCHDIBadgeConfig(latestCHDI?.status ?? "abstain");
            const latestWeight = animal.weightLogs[0]?.value;

            return (
              <div key={animal.id} className="card p-5 sm:p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-5">
                {/* Animal Header */}
                <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-slate-100">
                  <div className="flex items-center gap-3.5">
                    <div className="w-12 h-12 bg-[#123326] text-emerald-300 rounded-lg flex items-center justify-center font-bold text-lg font-mono">
                      {(animal.name ?? animal.tagId)[0]}
                    </div>
                    <div>
                      <div className="flex items-center gap-2.5">
                        <h2 className="text-lg font-bold text-slate-950">
                          {animal.name ?? animal.tagId}
                        </h2>
                        <span className={`badge-${latestCHDI?.status ?? "abstain"}`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                          {badge.label}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">
                        Ear Tag: <span className="font-mono font-bold text-slate-800">{animal.tagId}</span> · {animal.breed} · {calcAge(animal.dob)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Link
                      href={`/farmer/cattle/${animal.id}`}
                      className="btn btn-secondary btn-sm text-xs font-semibold"
                    >
                      View Details &amp; History →
                    </Link>
                  </div>
                </div>

                {/* Health Metrics Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="bg-[#f8faf9] p-3 rounded-lg border border-slate-200">
                    <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Health Score</p>
                    <p className={`text-lg font-extrabold mt-0.5 ${badge.color}`}>
                      {latestCHDI && latestCHDI.score !== null ? `${Math.round(latestCHDI.score)}/100` : "Calibrating"}
                    </p>
                    <p className="text-[10px] text-slate-400 font-mono mt-0.5">
                      {latestCHDI ? `Updated ${fmtDate(latestCHDI.timestamp)}` : "No logs yet"}
                    </p>
                  </div>

                  <div className="bg-[#f8faf9] p-3 rounded-lg border border-slate-200">
                    <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Body Weight</p>
                    <p className="text-lg font-extrabold text-slate-900 mt-0.5">
                      {latestWeight ? `${latestWeight} kg` : "—"}
                    </p>
                    <p className="text-[10px] text-slate-400 font-mono mt-0.5">
                      {animal.weightLogs.length} weight checks
                    </p>
                  </div>

                  <div className="bg-[#f8faf9] p-3 rounded-lg border border-slate-200">
                    <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Vaccines</p>
                    <p className="text-lg font-extrabold text-emerald-800 mt-0.5">
                      {animal.vaccinations.length > 0 ? animal.vaccinations[0].status.toUpperCase() : "Up to Date"}
                    </p>
                    <p className="text-[10px] text-slate-400 font-mono mt-0.5">
                      {animal.vaccinations.length} vaccine records
                    </p>
                  </div>

                  <div className="bg-[#f8faf9] p-3 rounded-lg border border-slate-200">
                    <p className="text-[10px] uppercase font-mono text-slate-500 font-bold">Doctor Visits</p>
                    <p className="text-lg font-extrabold text-blue-800 mt-0.5">
                      {animal.vetCases.length} Visits
                    </p>
                    <p className="text-[10px] text-slate-400 font-mono mt-0.5">
                      {animal.vetCases.filter(c => c.status === "open").length} open
                    </p>
                  </div>
                </div>

                {/* Veterinary Diagnostic & Treatment History */}
                <div>
                  <h3 className="text-xs font-bold text-slate-800 uppercase font-mono mb-2 flex items-center gap-1.5">
                    <IconStethoscope className="w-3.5 h-3.5 text-emerald-800" />
                    Doctor Cases &amp; Medicines
                  </h3>
                  {animal.vetCases.length > 0 ? (
                    <div className="overflow-x-auto border border-slate-200 rounded-lg">
                      <table className="w-full text-left text-xs">
                        <thead className="bg-[#f8faf9] text-slate-700 font-mono uppercase font-bold border-b border-slate-200">
                          <tr>
                            <th className="p-2.5">Date</th>
                            <th className="p-2.5">Status</th>
                            <th className="p-2.5">Symptoms</th>
                            <th className="p-2.5">Diagnosis</th>
                            <th className="p-2.5">Medicine / Treatment</th>
                            <th className="p-2.5">Veterinarian</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 text-slate-700">
                          {animal.vetCases.map((vc: any) => (
                            <tr key={vc.id} className="hover:bg-slate-50">
                              <td className="p-2.5 font-mono">{fmtDate(vc.createdAt)}</td>
                              <td className="p-2.5">
                                <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                                  vc.status === "open" ? "bg-blue-100 text-blue-800" : "bg-emerald-100 text-emerald-800"
                                }`}>
                                  {vc.status}
                                </span>
                              </td>
                              <td className="p-2.5">{vc.symptoms ?? "N/A"}</td>
                              <td className="p-2.5 font-semibold">{vc.diagnosis ?? "Evaluating"}</td>
                              <td className="p-2.5 text-emerald-800 font-medium">{vc.treatment ?? "None"}</td>
                              <td className="p-2.5">{vc.vet?.name ?? "District Vet"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 italic">No veterinarian cases for this animal.</p>
                  )}
                </div>

                {/* Vaccination History */}
                <div>
                  <h3 className="text-xs font-bold text-slate-800 uppercase font-mono mb-2 flex items-center gap-1.5">
                    <IconAudit className="w-3.5 h-3.5 text-emerald-800" />
                    Vaccine Schedule
                  </h3>
                  {animal.vaccinations.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                      {animal.vaccinations.map((vac) => (
                        <div key={vac.id} className="p-2.5 rounded-lg bg-[#f8faf9] border border-slate-200 flex items-center justify-between text-xs">
                          <div>
                            <p className="font-bold text-slate-900">{vac.vaccineType}</p>
                            <p className="text-slate-500 text-[11px] mt-0.5">Due: {fmtDate(vac.dueAt)}</p>
                          </div>
                          <span className={`px-2 py-0.5 rounded font-bold text-[10px] font-mono ${
                            vac.status === "done" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"
                          }`}>
                            {vac.status.toUpperCase()}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 italic">No upcoming vaccines scheduled.</p>
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

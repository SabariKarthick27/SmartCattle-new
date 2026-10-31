import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { IconCheckCircle } from "@/components/icons";

export default async function VetAssignedFarmsPage() {
  const session = await getServerSession(authOptions);
  const vetRegion = session?.user?.assignedRegion;

  let farmers: Array<{
    id: string;
    name: string;
    email: string;
    phone: string | null;
    farmId: string | null;
    assignedRegion: string | null;
    cattle: Array<{ id: string; tagId: string; name: string | null; breed: string }>;
  }> = [];

  try {
    farmers = await prisma.user.findMany({
      where: {
        role: "farmer",
        ...(vetRegion && vetRegion !== "Tamil Nadu" && vetRegion !== "All" ? { assignedRegion: vetRegion } : {}),
      },
      include: {
        cattle: {
          where: { isActive: true },
          select: { id: true, tagId: true, name: true, breed: true },
          orderBy: { tagId: "asc" },
        },
      },
    });
  } catch (err) {
    console.error("[Vet Farms DB Error]", err);
  }

  const totalCattleInRegion = farmers.reduce((sum, f) => sum + f.cattle.length, 0);

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-6xl mx-auto">
      {/* Top Header */}
      <div className="pb-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              My Assigned Farms &amp; Herds
            </h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
              REGISTRY
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            District: <span className="font-bold text-slate-800">{vetRegion || "All Regional Coverage"}</span>
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="card p-4 bg-white border border-slate-300 shadow-xs rounded-xl">
          <div className="text-slate-500 text-[10px] font-mono uppercase font-bold">Assigned Farms</div>
          <div className="text-2xl font-extrabold text-slate-950 mt-1 font-display tnum">{farmers.length}</div>
        </div>
        <div className="card p-4 bg-white border border-slate-300 shadow-xs rounded-xl">
          <div className="text-slate-500 text-[10px] font-mono uppercase font-bold">Total Cattle Monitored</div>
          <div className="text-2xl font-extrabold text-emerald-800 mt-1 font-display tnum">{totalCattleInRegion}</div>
        </div>
      </div>

      {/* Farms List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between pb-1 border-b border-slate-100">
          <h2 className="text-xs font-bold uppercase font-mono tracking-wider text-slate-700">
            Registered Farms in {vetRegion || "Salem"} ({farmers.length})
          </h2>
          <span className="text-[11px] font-mono text-slate-400">Total Cattle: {totalCattleInRegion}</span>
        </div>

        {farmers.length === 0 ? (
          <div className="card p-12 text-center bg-white border border-slate-300 shadow-xs rounded-xl text-slate-400 text-xs">
            No registered farms found in {vetRegion || "your assigned region"}.
          </div>
        ) : (
          <div className="space-y-4">
            {farmers.map((farmer) => (
              <div key={farmer.id} className="card p-6 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
                {/* Farmer Header Row */}
                <div className="flex items-start justify-between flex-wrap gap-4 pb-4 border-b border-slate-100">
                  <div className="flex items-center gap-3.5">
                    <div className="w-12 h-12 bg-[#0f3d32] text-emerald-300 rounded-xl flex items-center justify-center font-bold text-base font-mono shrink-0 shadow-xs">
                      {farmer.name[0]?.toUpperCase() ?? "F"}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-bold text-slate-950 text-base">{farmer.name}</h3>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-brand-50 text-brand-900 border border-brand-200">
                          {farmer.farmId || "Farm"}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 font-mono mt-0.5">
                        {farmer.email} · {farmer.phone || "No phone"}
                      </p>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="text-xs font-mono font-bold text-slate-700 block">
                      {farmer.assignedRegion || vetRegion || "Salem"}
                    </span>
                    <span className="text-[11px] text-slate-400 font-mono mt-0.5 block">
                      {farmer.cattle.length} Registered Cattle
                    </span>
                  </div>
                </div>

                {/* Herd Grid (Clean 4-column aligned grid) */}
                <div>
                  <p className="text-[10px] font-mono uppercase tracking-wider font-bold text-slate-500 mb-2.5">
                    Cattle Herd Registry ({farmer.cattle.length})
                  </p>
                  {farmer.cattle.length === 0 ? (
                    <p className="text-xs text-slate-400 italic">No cattle registered yet.</p>
                  ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                      {farmer.cattle.map((animal) => (
                        <div
                          key={animal.id}
                          className="p-3.5 bg-[#f8faf9] border border-slate-200/90 rounded-xl flex flex-col justify-between hover:border-slate-300 transition-colors"
                        >
                          <div>
                            <div className="flex items-center justify-between gap-1 mb-1">
                              <span className="font-mono font-bold text-slate-900 text-xs">{animal.tagId}</span>
                              {animal.name && (
                                <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200/60">
                                  {animal.name}
                                </span>
                              )}
                            </div>
                            <p className="text-[11px] text-slate-600 leading-tight mt-1">{animal.breed}</p>
                          </div>
                          <div className="mt-3 pt-2 border-t border-slate-200/70 flex items-center justify-between text-[10px] font-mono text-slate-400">
                            <span>Status</span>
                            <span className="text-emerald-700 font-bold flex items-center gap-1">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                              Active
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

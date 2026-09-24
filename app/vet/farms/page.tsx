import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { IconCattle, IconUser, IconCheckCircle } from "@/components/icons";

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
    cattle: Array<{ id: string; tagId: string; breed: string }>;
  }> = [];

  try {
    farmers = await prisma.user.findMany({
      where: {
        role: "farmer",
        ...(vetRegion ? { assignedRegion: vetRegion } : {}),
      },
      include: {
        cattle: {
          select: { id: true, tagId: true, breed: true },
        },
      },
    });
  } catch (err) {
    console.error("[Vet Farms DB Error]", err);
  }

  const totalCattleInRegion = farmers.reduce((sum, f) => sum + f.cattle.length, 0);

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-6xl mx-auto">
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
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="card p-4 bg-white border border-slate-300 shadow-xs rounded-xl">
          <div className="text-slate-500 text-[10px] font-mono uppercase font-bold">Assigned Farms</div>
          <div className="text-2xl font-extrabold text-slate-950 mt-1 font-display tnum">{farmers.length}</div>
        </div>
        <div className="card p-4 bg-white border border-slate-300 shadow-xs rounded-xl">
          <div className="text-slate-500 text-[10px] font-mono uppercase font-bold">Total Cattle Monitored</div>
          <div className="text-2xl font-extrabold text-emerald-800 mt-1 font-display tnum">{totalCattleInRegion}</div>
        </div>
        <div className="card p-4 bg-emerald-50 border border-emerald-300 shadow-xs rounded-xl">
          <div className="text-emerald-900 text-[10px] font-mono uppercase font-bold">Doctor Coverage</div>
          <div className="text-xs font-bold text-emerald-900 mt-2 flex items-center gap-1.5">
            <IconCheckCircle className="w-4 h-4 text-emerald-700" /> Active District Doctor Coverage
          </div>
        </div>
      </div>

      {/* Farms List */}
      <div className="space-y-4">
        <h2 className="text-sm font-bold uppercase font-mono text-slate-800">
          Farmers in {vetRegion || "Your District"}
        </h2>

        {farmers.length === 0 ? (
          <div className="card p-12 text-center bg-white border border-slate-300 shadow-xs rounded-xl text-slate-400 text-xs">
            No registered farms found in {vetRegion || "your assigned region"}.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {farmers.map((farmer) => (
              <div key={farmer.id} className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-[#0f3d32] text-emerald-300 rounded-lg flex items-center justify-center font-bold text-sm font-mono">
                      {farmer.name[0]?.toUpperCase() ?? "F"}
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-950 text-sm">{farmer.name}</h3>
                      <p className="text-xs text-slate-500">{farmer.email} · {farmer.phone || "No phone"}</p>
                    </div>
                  </div>
                  <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                    {farmer.farmId || "Farm"}
                  </span>
                </div>

                <div className="border-t border-slate-100 pt-3">
                  <div className="flex items-center justify-between text-xs text-slate-500 mb-2 font-mono">
                    <span>Cattle ({farmer.cattle.length})</span>
                    <span>{farmer.assignedRegion || vetRegion || "Tamil Nadu"}</span>
                  </div>

                  {farmer.cattle.length === 0 ? (
                    <p className="text-xs text-slate-400 italic">No cattle registered yet.</p>
                  ) : (
                    <div className="flex flex-wrap gap-1.5">
                      {farmer.cattle.map((animal: { id: string; tagId: string; breed: string }) => (
                        <div key={animal.id} className="bg-[#f8faf9] border border-slate-200 rounded px-2 py-0.5 text-xs flex items-center gap-1">
                          <span className="font-mono font-bold text-slate-800">{animal.tagId}</span>
                          <span className="text-slate-400">·</span>
                          <span className="text-slate-600">{animal.breed}</span>
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

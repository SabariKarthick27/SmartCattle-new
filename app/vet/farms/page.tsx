import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import Link from "next/link";
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
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
            <IconCattle className="w-6 h-6 text-teal-700" />
            Assigned Farms & Herds
          </h1>
          <p className="text-slate-500 mt-1">
            Region: <span className="font-semibold text-slate-700">{vetRegion || "All Regional Coverage"}</span>
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="card p-5 bg-white">
          <div className="text-slate-500 text-xs font-medium">Assigned Farms</div>
          <div className="text-3xl font-bold text-slate-900 mt-1">{farmers.length}</div>
        </div>
        <div className="card p-5 bg-teal-50/60 border border-teal-200/60">
          <div className="text-teal-700 text-xs font-medium">Total Cattle Monitored</div>
          <div className="text-3xl font-bold text-teal-900 mt-1">{totalCattleInRegion}</div>
        </div>
        <div className="card p-5 bg-emerald-50/60 border border-emerald-200/60">
          <div className="text-emerald-700 text-xs font-medium">Coverage Status</div>
          <div className="text-sm font-bold text-emerald-900 mt-2 flex items-center gap-1.5">
            <IconCheckCircle className="w-4 h-4 text-emerald-600" /> Active Regional Surveillance
          </div>
        </div>
      </div>

      {/* Farms List */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-slate-900">Farmers & Herds in {vetRegion || "Region"}</h2>

        {farmers.length === 0 ? (
          <div className="card p-8 text-center text-slate-500">
            No registered farms found in {vetRegion || "your assigned region"}.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {farmers.map((farmer) => (
              <div key={farmer.id} className="card p-5 hover:shadow-md transition-all">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-teal-100 text-teal-800 rounded-full flex items-center justify-center font-bold text-sm">
                      <IconUser className="w-5 h-5 text-teal-700" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900">{farmer.name}</h3>
                      <p className="text-xs text-slate-500">{farmer.email} · {farmer.phone || "No phone"}</p>
                    </div>
                  </div>
                  <span className="badge-secondary text-xs">{farmer.farmId || "Farm Owner"}</span>
                </div>

                <div className="border-t border-slate-100 pt-3 mt-3">
                  <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
                    <span>Registered Cattle ({farmer.cattle.length})</span>
                    <span>{farmer.assignedRegion || vetRegion || "Tamil Nadu"}</span>
                  </div>

                  {farmer.cattle.length === 0 ? (
                    <p className="text-xs text-slate-400 italic">No cattle registered yet.</p>
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      {farmer.cattle.map((animal: { id: string; tagId: string; breed: string }) => (
                        <div key={animal.id} className="bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 text-xs flex items-center gap-1.5">
                          <span className="font-mono font-medium text-slate-700">{animal.tagId}</span>
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

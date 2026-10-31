import prisma from "@/lib/prisma";
import { notFound, redirect } from "next/navigation";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import Link from "next/link";
import { getCHDIBadgeConfig, calcAge, fmtDate } from "@/lib/utils";
import { IconScan, IconCow, IconSyringe, IconActivity } from "@/components/icons";
import { SmartCattleLogo } from "@/components/SmartCattleLogo";
import DailyHealthLogForm from "@/components/DailyHealthLogForm";

export default async function PublicScanLandingPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;
  const decodedToken = decodeURIComponent(token).trim();
  const session = await getServerSession(authOptions);

  const cattle = await prisma.cattle.findFirst({
    where: {
      OR: [
        { qrToken: decodedToken },
        { tagId: { equals: decodedToken, mode: "insensitive" } },
        { id: decodedToken },
      ],
    },
    include: {
      farmer: { select: { id: true, name: true, phone: true } },
      chdiHistory: { orderBy: { timestamp: "desc" }, take: 1 },
      weightLogs: { orderBy: { timestamp: "desc" }, take: 1 },
      milkLogs: { orderBy: { timestamp: "desc" }, take: 1 },
      feedLogs: { orderBy: { timestamp: "desc" }, take: 1 },
      temperatureLogs: { orderBy: { timestamp: "desc" }, take: 1 },
      activityLogs: { orderBy: { timestamp: "desc" }, take: 1 },
      ruminationLogs: { orderBy: { timestamp: "desc" }, take: 1 },
      vaccinations: { where: { status: "upcoming" }, orderBy: { dueAt: "asc" }, take: 1 },
    },
  });

  if (!cattle) {
    notFound();
  }

  // Log scan telemetry
  await prisma.scanLog.create({
    data: { cattleId: cattle.id },
  }).catch(() => {});

  const latestCHDI = cattle.chdiHistory[0];
  const badge = getCHDIBadgeConfig(latestCHDI?.status ?? "abstain");
  const latestWeight = cattle.weightLogs[0]?.value;
  const latestMilk = cattle.milkLogs[0]?.litres;
  const latestFeed = cattle.feedLogs[0]?.quantity;
  const latestTemp = cattle.temperatureLogs[0]?.value;
  const upcomingVac = cattle.vaccinations[0];

  const isOwner = session?.user?.id === cattle.farmerId;
  const canLogHealth = isOwner || session?.user?.role === "admin" || session?.user?.role === "vet";

  const targetUrl = session?.user?.role === "vet"
    ? `/vet`
    : `/farmer/cattle/${cattle.id}`;

  // Serialize cattle data for client component
  const serializedCattle = {
    id: cattle.id,
    cattleId: cattle.id,
    tagId: cattle.tagId,
    name: cattle.name,
    breed: cattle.breed,
    dob: cattle.dob ? cattle.dob.toISOString() : undefined,
    gender: cattle.gender,
    purpose: cattle.purpose,
    farmer: cattle.farmer,
    chdiHistory: cattle.chdiHistory.map((c) => ({
      score: c.score,
      status: c.status,
      confidence: c.confidence,
      topFactors: (c.topFactors as any[]) || [],
    })),
    weightLogs: cattle.weightLogs.map((w) => ({ value: w.value, timestamp: w.timestamp.toISOString() })),
    milkLogs: cattle.milkLogs.map((m) => ({ litres: m.litres, timestamp: m.timestamp.toISOString() })),
    feedLogs: cattle.feedLogs.map((f) => ({ quantity: f.quantity, feedType: f.feedType, timestamp: f.timestamp.toISOString() })),
    temperatureLogs: cattle.temperatureLogs.map((t) => ({ value: t.value, timestamp: t.timestamp.toISOString() })),
  };

  return (
    <div className="min-h-screen bg-[#0b2219] text-slate-100 flex flex-col justify-between antialiased">
      {/* Top Header */}
      <header className="p-4 border-b border-emerald-900/60 bg-[#071610]/80 backdrop-blur-xs flex items-center justify-between">
        <Link href="/" className="group">
          <SmartCattleLogo variant="light" subtitle="Livestock Passport" />
        </Link>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 bg-emerald-950 text-emerald-300 border border-emerald-700/60 rounded">
          VERIFIED EAR TAG
        </span>
      </header>

      {/* Main Container */}
      <main className="p-4 sm:p-6 max-w-2xl mx-auto w-full my-6 space-y-6">
        {canLogHealth ? (
          /* Authenticated Farm Owner: Direct Daily Health Logging Form */
          <div className="space-y-4">
            <div className="bg-emerald-950/80 border border-emerald-800/80 rounded-xl p-3.5 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
                <span className="text-emerald-200 font-medium">
                  Welcome, <strong>{session?.user?.name || "Farmer"}</strong>! Record today&apos;s vitals below.
                </span>
              </div>
              <Link
                href="/farmer/scan"
                className="btn btn-secondary btn-sm text-[11px] py-1 px-2.5 text-slate-800"
              >
                In-App Scanner
              </Link>
            </div>

            <DailyHealthLogForm cattle={serializedCattle} />
          </div>
        ) : (
          /* Public or Non-Owner View: Cattle Digital Passport */
          <div className="bg-white text-slate-900 rounded-2xl shadow-2xl border border-slate-200 overflow-hidden animate-in zoom-in-95 duration-200">
            {/* Tag Identification Banner */}
            <div className="bg-[#123326] p-5 text-white flex items-center justify-between relative overflow-hidden">
              <div className="relative z-10">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                  <span className="text-[10px] font-mono tracking-widest text-emerald-300 uppercase font-bold">
                    EAR TAG SCANNED
                  </span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-black font-mono tracking-tight mt-1 text-white">
                  {cattle.tagId}
                </h1>
                <p className="text-xs text-emerald-200/90 font-medium mt-0.5">
                  {cattle.name ? `${cattle.name} · ` : ""}{cattle.breed} · {calcAge(cattle.dob)}
                </p>
              </div>

              <div className="w-14 h-14 bg-emerald-800/60 border border-emerald-600/40 rounded-xl flex items-center justify-center text-emerald-300 font-mono font-bold text-xl relative z-10 shrink-0">
                {(cattle.name ?? cattle.tagId)[0]}
              </div>
            </div>

            {/* Cattle Quick Summary Card */}
            <div className="p-5 space-y-4">
              {/* Health Score Pill */}
              <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                <div className="flex items-center gap-2.5">
                  <IconActivity className="w-4 h-4 text-emerald-800" />
                  <div>
                    <p className="text-[10px] font-mono uppercase font-bold text-slate-500">CHDI Health Status</p>
                    <p className="text-xs font-bold text-slate-900">{badge.label}</p>
                  </div>
                </div>
                <span className={`badge-${latestCHDI?.status ?? "abstain"} text-xs py-1 px-3 font-bold`}>
                  {latestCHDI?.score != null ? `${Math.round(latestCHDI.score)} / 100` : "Calibrating"}
                </span>
              </div>

              {/* Vitals Grid */}
              <div className="grid grid-cols-2 gap-2.5 text-xs">
                <div className="p-3 bg-[#f8faf9] rounded-xl border border-slate-200">
                  <span className="text-[10px] font-mono uppercase text-slate-400 block font-semibold">Latest Weight</span>
                  <span className="font-bold text-slate-900 text-sm font-mono">{latestWeight ? `${latestWeight} kg` : "—"}</span>
                </div>
                <div className="p-3 bg-[#f8faf9] rounded-xl border border-slate-200">
                  <span className="text-[10px] font-mono uppercase text-slate-400 block font-semibold">Daily Milk</span>
                  <span className="font-bold text-slate-900 text-sm font-mono">{latestMilk ? `${latestMilk} L` : "—"}</span>
                </div>
              </div>

              {/* Farm & Vaccine Info */}
              <div className="text-xs space-y-1.5 pt-1 text-slate-600 font-medium">
                <p className="flex justify-between border-b border-slate-100 pb-1.5">
                  <span className="text-slate-500">Registered Farm Owner:</span>
                  <span className="font-bold text-slate-900">{cattle.farmer.name}</span>
                </p>
                {upcomingVac && (
                  <p className="flex justify-between border-b border-slate-100 pb-1.5">
                    <span className="text-slate-500">Next Vaccination:</span>
                    <span className="font-mono text-emerald-800 font-bold">{upcomingVac.vaccineType} ({fmtDate(upcomingVac.dueAt)})</span>
                  </p>
                )}
              </div>

              {/* Action Buttons */}
              <div className="pt-3 space-y-2.5">
                <p className="text-center text-xs font-semibold text-slate-700">
                  {session ? "View complete medical profile & health records:" : "Sign in to log daily health vitals:"}
                </p>

                {session ? (
                  <Link
                    href={targetUrl}
                    id="open-scanned-cattle-details-btn"
                    className="btn btn-primary w-full justify-center py-3 text-sm font-bold shadow-md gap-2"
                  >
                    <span>Open Cattle Details &amp; Records →</span>
                  </Link>
                ) : (
                  <Link
                    href={`/login?callbackUrl=/scan/${encodeURIComponent(decodedToken)}`}
                    className="btn btn-primary w-full justify-center py-3 text-sm font-bold shadow-md gap-2"
                  >
                    <span>Sign In to Log Daily Health Details →</span>
                  </Link>
                )}

                <div className="flex gap-2">
                  <Link
                    href="/farmer/scan"
                    className="btn btn-secondary flex-1 justify-center text-xs py-2 text-slate-800"
                  >
                    Scan Another Tag
                  </Link>
                  <Link
                    href="/"
                    className="btn btn-secondary flex-1 justify-center text-xs py-2 text-slate-800"
                  >
                    Home
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Security Note */}
        <p className="text-center text-[11px] font-mono text-emerald-400/80">
          SmartCattle Live Telemetry &bull; Ear Tag Verified &bull; CHDI Health Engine
        </p>
      </main>

      {/* Footer */}
      <footer className="p-4 text-center text-xs font-mono text-emerald-500/70 border-t border-emerald-950">
        SmartCattle Intelligent Livestock Operations
      </footer>
    </div>
  );
}

import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// GET /api/admin/analytics
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const now = new Date();
  const thirtyDaysAgo = new Date(now.getTime() - 30 * 86400000);

  const [
    totalCattle,
    totalFarmers,
    totalVets,
    pendingApprovals,
    openCases,
    resolvedCases,
    recentCHDI,
    regionAlerts,
    chdiByStatus,
  ] = await Promise.all([
    prisma.cattle.count({ where: { isActive: true } }),
    prisma.user.count({ where: { role: "farmer", isVerified: true } }),
    prisma.user.count({ where: { role: "vet", isVerified: true } }),
    prisma.user.count({ where: { isVerified: false } }),
    prisma.vetCase.count({ where: { status: { in: ["open", "in_progress"] } } }),
    prisma.vetCase.count({ where: { status: "resolved", resolvedAt: { gte: thirtyDaysAgo } } }),
    prisma.cHDIEntry.findMany({
      where: { timestamp: { gte: thirtyDaysAgo } },
      select: { score: true, status: true, timestamp: true, cattle: { select: { region: true } } },
      orderBy: { timestamp: "asc" },
    }),
    prisma.regionAlert.findMany({
      where: { status: "active" },
      orderBy: { triggeredAt: "desc" },
      take: 10,
    }),
    prisma.cHDIEntry.groupBy({
      by: ["status"],
      _count: { status: true },
      where: { timestamp: { gte: thirtyDaysAgo } },
    }),
  ]);

  // Aggregate by region
  const regionMap: Record<string, { total: number; avgScore: number; scores: number[] }> = {};
  for (const entry of recentCHDI) {
    const region = entry.cattle?.region ?? "Unknown";
    if (!regionMap[region]) regionMap[region] = { total: 0, avgScore: 0, scores: [] };
    regionMap[region].total++;
    regionMap[region].scores.push(entry.score);
  }
  const regionStats = Object.entries(regionMap).map(([region, data]) => ({
    region,
    animalCount: data.total,
    avgCHDI: data.scores.reduce((a, b) => a + b, 0) / (data.scores.length || 1),
  }));

  // Cases resolved per month (last 6 months)
  const sixMonthsAgo = new Date(now.getTime() - 180 * 86400000);
  const monthlyCases = await prisma.vetCase.findMany({
    where: { status: "resolved", resolvedAt: { gte: sixMonthsAgo } },
    select: { resolvedAt: true },
  });
  const casesByMonth: Record<string, number> = {};
  for (const c of monthlyCases) {
    const key = c.resolvedAt!.toISOString().substring(0, 7);
    casesByMonth[key] = (casesByMonth[key] ?? 0) + 1;
  }

  return NextResponse.json({
    summary: { totalCattle, totalFarmers, totalVets, pendingApprovals, openCases, resolvedCases },
    chdiByStatus,
    regionStats,
    regionAlerts,
    casesByMonth: Object.entries(casesByMonth).map(([month, count]) => ({ month, count })),
  });
}

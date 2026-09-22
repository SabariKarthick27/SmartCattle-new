import prisma from "@/lib/prisma";

export interface WeeklyAnalysisSummary {
  cattleId: string;
  tagId: string;
  name: string | null;
  breed: string;
  region: string | null;
  farmerId: string;
  farmerName: string;
  farmerPhone: string;
  weekStartDate: string;
  weekEndDate: string;
  avgCHDIScore: number;
  healthStatus: "healthy" | "watch" | "at-risk";
  avgMilkYield: number; // L/day
  weightTrendKg: number; // net weight change over week
  avgActivityScore: number;
  totalFeedKg: number;
  topRiskFactors: Array<{ factor: string; contribution: number; direction: string }>;
  vetNotes?: string;
  sentToFarmer?: boolean;
}

export async function generateWeeklyHealthAnalysis(cattleId: string): Promise<WeeklyAnalysisSummary | null> {
  const cattle = await prisma.cattle.findUnique({
    where: { id: cattleId },
    include: {
      farmer: { select: { id: true, name: true, phone: true } },
      chdiHistory: { orderBy: { timestamp: "desc" }, take: 7 },
      weightLogs: { orderBy: { timestamp: "desc" }, take: 7 },
      feedLogs: { orderBy: { timestamp: "desc" }, take: 7 },
      activityLogs: { orderBy: { timestamp: "desc" }, take: 7 },
    },
  });

  if (!cattle) return null;

  const now = new Date();
  const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

  // 1. Weekly CHDI Average
  const scores = cattle.chdiHistory.map((h) => h.score);
  const avgCHDIScore = scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 85;

  let healthStatus: "healthy" | "watch" | "at-risk" = "healthy";
  if (avgCHDIScore < 50) healthStatus = "at-risk";
  else if (avgCHDIScore < 75) healthStatus = "watch";

  // 2. Weekly Milk & Feed
  const feeds = cattle.feedLogs.map((f) => f.quantity);
  const totalFeedKg = feeds.reduce((a, b) => a + b, 0);

  // Estimate milk yield based on feed and activity logs or logs
  const avgMilkYield = Number((totalFeedKg > 0 ? totalFeedKg * 0.85 : 12.5).toFixed(1));

  // 3. Weight Trend
  const weights = cattle.weightLogs.map((w) => w.value);
  const weightTrendKg = weights.length >= 2 ? Number((weights[0] - weights[weights.length - 1]).toFixed(1)) : 0;

  // 4. Activity
  const activities = cattle.activityLogs.map((a) => a.value);
  const avgActivityScore = activities.length > 0 ? Math.round(activities.reduce((a, b) => a + b, 0) / activities.length) : 82;

  // 5. Top Risk Factors from latest CHDI
  const latestCHDI = cattle.chdiHistory[0];
  const topRiskFactors = (latestCHDI?.topFactors as Array<{ factor: string; contribution: number; direction: string }>) || [];

  // 6. Check if weekly report was already sent in the last 7 days
  const lastReport = await prisma.vetCase.findFirst({
    where: {
      cattleId: cattle.id,
      symptoms: { contains: "Weekly Health Analysis" },
      createdAt: { gte: sevenDaysAgo },
    },
    orderBy: { createdAt: "desc" },
  });

  return {
    cattleId: cattle.id,
    tagId: cattle.tagId,
    name: cattle.name,
    breed: cattle.breed,
    region: cattle.region,
    farmerId: cattle.farmer.id,
    farmerName: cattle.farmer.name,
    farmerPhone: cattle.farmer.phone,
    weekStartDate: sevenDaysAgo.toISOString().split("T")[0],
    weekEndDate: now.toISOString().split("T")[0],
    avgCHDIScore,
    healthStatus,
    avgMilkYield,
    weightTrendKg,
    avgActivityScore,
    totalFeedKg,
    topRiskFactors,
    sentToFarmer: Boolean(lastReport),
    vetNotes: lastReport?.treatment || undefined,
  };
}

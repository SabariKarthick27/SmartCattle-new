import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { retrainClassifier, getClassifierMetrics } from "@/lib/chdi/feedback-classifier";

// GET /api/admin/model-stats
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const [feedbackCount, totalCHDI, abstainCount, versions] = await Promise.all([
    prisma.vetFeedback.count(),
    prisma.cHDIEntry.count(),
    prisma.cHDIEntry.count({ where: { status: "abstain" } }),
    prisma.modelVersion.findMany({ orderBy: { trainedAt: "desc" }, take: 10 }),
  ]);

  const abstentionRate = totalCHDI > 0 ? abstainCount / totalCHDI : 0;

  // Confirm vs override ratio
  const feedbacks = await prisma.vetFeedback.findMany({ select: { confirmedOutcome: true, predictedStatus: true } });
  const confirms = feedbacks.filter(f => f.confirmedOutcome === f.predictedStatus).length;

  const stage3Metrics = getClassifierMetrics();

  return NextResponse.json({
    stage1: { method: "moving-average", windowDays: 7 },
    stage2: { abstentionRate, totalScored: totalCHDI, abstainCount },
    stage3: stage3Metrics,
    feedbackCount,
    confirmsCount: confirms,
    overridesCount: feedbacks.length - confirms,
    modelVersions: versions,
  });
}

// POST /api/admin/model-stats — trigger retraining
export async function POST() {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const metrics = await retrainClassifier();

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "admin",
      action: "model_retrain_triggered",
      metadata: JSON.parse(JSON.stringify(metrics)),
    },
  });

  return NextResponse.json({ metrics });
}

import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { generateWeeklyHealthAnalysis } from "@/lib/chdi/weekly-analysis";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || (session.user.role !== "vet" && session.user.role !== "admin")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const vetRegion = session.user.assignedRegion;

  const cattleList = await prisma.cattle.findMany({
    where: vetRegion ? { region: vetRegion } : {},
    select: { id: true },
  });

  const analyses = await Promise.all(
    cattleList.map((c) => generateWeeklyHealthAnalysis(c.id))
  );

  const validAnalyses = analyses.filter(Boolean);

  return NextResponse.json({ reports: validAnalyses });
}

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session || (session.user.role !== "vet" && session.user.role !== "admin")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const { cattleId, vetNotes, healthStatus } = await req.json();

    if (!cattleId) {
      return NextResponse.json({ error: "Cattle ID is required" }, { status: 400 });
    }

    const cattle = await prisma.cattle.findUnique({
      where: { id: cattleId },
      select: { farmerId: true, tagId: true, name: true },
    });

    if (!cattle) {
      return NextResponse.json({ error: "Animal not found" }, { status: 404 });
    }

    // Enforce once-a-week frequency limit (7-day window)
    const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
    const existingReport = await prisma.vetCase.findFirst({
      where: {
        cattleId,
        symptoms: { contains: "Weekly Health Analysis" },
        createdAt: { gte: sevenDaysAgo },
      },
      orderBy: { createdAt: "desc" },
    });

    if (existingReport) {
      const sentDateStr = existingReport.createdAt.toISOString().split("T")[0];
      return NextResponse.json(
        {
          error: `A weekly health report has already been sent for ${cattle.tagId} for this week (sent on ${sentDateStr}). Weekly reports can only be sent once a week.`,
          alreadySent: true,
        },
        { status: 400 }
      );
    }

    // Persist as a Weekly Health Report Vet Case entry for the farmer
    const reportCase = await prisma.vetCase.create({
      data: {
        cattleId,
        farmerId: cattle.farmerId,
        vetId: session.user.id,
        status: "resolved",
        urgency: healthStatus === "at-risk" ? "high" : healthStatus === "watch" ? "medium" : "low",
        chdiSnapshot: {
          reportType: "weekly_health_analysis",
          sentAt: new Date().toISOString(),
          vetNotes: vetNotes || "Weekly health analysis completed. Herd condition is stable.",
        },
        symptoms: `Weekly Health Analysis (${healthStatus.toUpperCase()})`,
        diagnosis: "Weekly Routine Evaluation",
        treatment: vetNotes || "Weekly health check completed.",
      },
    });

    return NextResponse.json({ success: true, reportId: reportCase.id });
  } catch (error: any) {
    console.error("[Weekly Analysis Send Error]", error);
    return NextResponse.json({ error: error.message || "Failed to send report" }, { status: 500 });
  }
}

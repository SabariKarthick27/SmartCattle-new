import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// POST /api/cattle/[id]/vet-request — farmer requests a vet visit
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "farmer") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { symptoms, urgency = "medium" } = body;

  const cattle = await prisma.cattle.findUnique({
    where: { id },
    include: {
      chdiHistory: { orderBy: { timestamp: "desc" }, take: 1 },
    },
  });

  if (!cattle) return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (cattle.farmerId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  // Check for existing open case
  const existing = await prisma.vetCase.findFirst({
    where: { cattleId: id, status: { in: ["open", "in_progress"] } },
  });

  if (existing) {
    return NextResponse.json({ error: "An open case already exists for this animal", caseId: existing.id }, { status: 409 });
  }

  const latestCHDI = cattle.chdiHistory[0];
  const vetCase = await prisma.vetCase.create({
    data: {
      cattleId: id,
      farmerId: session.user.id,
      urgency,
      symptoms: symptoms || null,
      chdiSnapshot: latestCHDI
        ? JSON.parse(JSON.stringify({
            score: latestCHDI.score,
            status: latestCHDI.status,
            confidence: latestCHDI.confidence,
            topFactors: latestCHDI.topFactors,
            timestamp: latestCHDI.timestamp,
          }))
        : {},
    },
  });

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "farmer",
      action: "vet_request_submitted",
      targetId: id,
      metadata: JSON.parse(JSON.stringify({ caseId: vetCase.id, urgency })),
    },
  });

  return NextResponse.json({ vetCase }, { status: 201 });
}

import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// POST /api/vet/cases/[id]/feedback — vet confirms or overrides CHDI flag
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "vet") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { confirmedOutcome } = body;

  if (!confirmedOutcome) {
    return NextResponse.json({ error: "confirmedOutcome is required" }, { status: 400 });
  }

  const vetCase = await prisma.vetCase.findUnique({ where: { id } });
  if (!vetCase) return NextResponse.json({ error: "Not found" }, { status: 404 });

  const snapshot = vetCase.chdiSnapshot as Record<string, unknown>;

  // Upsert feedback (one per case)
  const feedback = await prisma.vetFeedback.upsert({
    where: { caseId: id },
    create: {
      cattleId: vetCase.cattleId,
      vetId: session.user.id,
      caseId: id,
      predictedStatus: String(snapshot.status ?? "unknown"),
      confirmedOutcome,
    },
    update: {
      confirmedOutcome,
      vetId: session.user.id,
    },
  });

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "vet",
      action: "vet_feedback_submitted",
      targetId: id,
      metadata: JSON.parse(JSON.stringify({ confirmedOutcome, predictedStatus: snapshot?.status ?? "unknown" })),
    },
  });

  return NextResponse.json({ feedback });
}

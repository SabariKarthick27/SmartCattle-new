import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// POST /api/vet/cases/[id]/diagnose
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
  const { symptoms, diagnosis, treatment, medication, followUpDate, status } = body;

  const vetCase = await prisma.vetCase.findUnique({ where: { id } });
  if (!vetCase) return NextResponse.json({ error: "Not found" }, { status: 404 });

  const updated = await prisma.vetCase.update({
    where: { id },
    data: {
      vetId: session.user.id,
      symptoms: symptoms ?? vetCase.symptoms,
      diagnosis: diagnosis ?? null,
      treatment: treatment ?? null,
      medication: medication ?? null,
      followUpDate: followUpDate ? new Date(followUpDate) : null,
      status: status ?? "in_progress",
      resolvedAt: status === "resolved" ? new Date() : null,
    },
  });

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "vet",
      action: "case_diagnosed",
      targetId: id,
      metadata: JSON.parse(JSON.stringify({ diagnosis, status })),
    },
  });

  return NextResponse.json({ vetCase: updated });
}

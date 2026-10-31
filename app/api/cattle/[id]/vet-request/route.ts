import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// POST /api/cattle/[id]/vet-request — farmer requests a vet visit with chosen veterinarian
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
  const { symptoms, urgency = "medium", vetId } = body;

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

  // Validate chosen veterinarian or auto-assign according to farm location
  let assignedVetId: string | null = null;
  if (vetId) {
    const chosenVet = await prisma.user.findFirst({
      where: { id: String(vetId), role: "vet", isActive: true },
      select: { id: true, name: true },
    });
    if (chosenVet) {
      assignedVetId = chosenVet.id;
    }
  }

  // If no vet chosen or specified vet not found, automatically pick the nearest veterinarian covering the farm location
  if (!assignedVetId) {
    const farmer = await prisma.user.findUnique({
      where: { id: session.user.id },
      select: { assignedRegion: true },
    });
    const farmRegion = (cattle.region || farmer?.assignedRegion || "").trim();
    if (farmRegion) {
      const localVet = await prisma.user.findFirst({
        where: {
          role: "vet",
          isActive: true,
          assignedRegion: { equals: farmRegion, mode: "insensitive" },
        },
        select: { id: true, name: true },
      });
      if (localVet) {
        assignedVetId = localVet.id;
      }
    }
    // Fallback to any active vet if regional match not found
    if (!assignedVetId) {
      const fallbackVet = await prisma.user.findFirst({
        where: { role: "vet", isActive: true },
        select: { id: true, name: true },
      });
      if (fallbackVet) {
        assignedVetId = fallbackVet.id;
      }
    }
  }

  const latestCHDI = cattle.chdiHistory[0];

  // Check for existing open case — if one exists, update it seamlessly
  const existing = await prisma.vetCase.findFirst({
    where: { cattleId: id, status: { in: ["open", "in_progress"] } },
  });

  if (existing) {
    const updatedCase = await prisma.vetCase.update({
      where: { id: existing.id },
      data: {
        vetId: assignedVetId,
        urgency,
        status: "open",
        createdAt: new Date(),
        symptoms: symptoms || existing.symptoms,
        chdiSnapshot: latestCHDI
          ? JSON.parse(
              JSON.stringify({
                score: latestCHDI.score,
                status: latestCHDI.status,
                confidence: latestCHDI.confidence,
                topFactors: latestCHDI.topFactors,
                timestamp: latestCHDI.timestamp,
              })
            )
          : existing.chdiSnapshot,
      },
      include: {
        vet: { select: { id: true, name: true, phone: true, assignedRegion: true } },
      },
    });

    await prisma.auditLog.create({
      data: {
        actorId: session.user.id,
        actorRole: "farmer",
        action: "vet_request_updated",
        targetId: id,
        metadata: JSON.parse(
          JSON.stringify({
            caseId: updatedCase.id,
            urgency,
            assignedVetId,
            assignedVetName: updatedCase.vet?.name ?? "District Queue",
          })
        ),
      },
    });

    return NextResponse.json({
      vetCase: updatedCase,
      message: `Doctor visit updated! Assigned to ${updatedCase.vet?.name ?? "District Veterinarian"}.`,
    }, { status: 200 });
  }

  const vetCase = await prisma.vetCase.create({
    data: {
      cattleId: id,
      farmerId: session.user.id,
      vetId: assignedVetId,
      urgency,
      symptoms: symptoms || null,
      chdiSnapshot: latestCHDI
        ? JSON.parse(
            JSON.stringify({
              score: latestCHDI.score,
              status: latestCHDI.status,
              confidence: latestCHDI.confidence,
              topFactors: latestCHDI.topFactors,
              timestamp: latestCHDI.timestamp,
            })
          )
        : {},
    },
    include: {
      vet: { select: { id: true, name: true, phone: true, assignedRegion: true } },
    },
  });

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "farmer",
      action: "vet_request_submitted",
      targetId: id,
      metadata: JSON.parse(
        JSON.stringify({
          caseId: vetCase.id,
          urgency,
          assignedVetId,
          assignedVetName: vetCase.vet?.name ?? "District Queue",
        })
      ),
    },
  });

  return NextResponse.json({
    vetCase,
    message: `Doctor visit requested! Assigned to ${vetCase.vet?.name ?? "District Veterinarian"}.`,
  }, { status: 201 });
}

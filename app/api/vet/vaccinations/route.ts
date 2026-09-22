import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || (session.user.role !== "vet" && session.user.role !== "admin")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const vetRegion = session.user.assignedRegion;

  const records = await prisma.vaccinationRecord.findMany({
    where: vetRegion
      ? { cattle: { region: vetRegion } }
      : {},
    include: {
      cattle: {
        select: {
          tagId: true,
          breed: true,
          name: true,
          farmer: { select: { name: true, phone: true } },
        },
      },
    },
    orderBy: { dueAt: "asc" },
  });

  return NextResponse.json({ records });
}

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session || (session.user.role !== "vet" && session.user.role !== "admin")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const { cattleId, vaccineType, dueAt, notes } = await req.json();

    if (!cattleId || !vaccineType || !dueAt) {
      return NextResponse.json({ error: "Animal, vaccine type, and due date are required" }, { status: 400 });
    }

    const record = await prisma.vaccinationRecord.create({
      data: {
        cattleId,
        vaccineType,
        dueAt: new Date(dueAt),
        notes: notes || null,
        status: "upcoming",
      },
    });

    return NextResponse.json({ record });
  } catch (error: any) {
    console.error("[Vaccination Create Error]", error);
    return NextResponse.json({ error: error.message || "Failed to schedule vaccination" }, { status: 500 });
  }
}

export async function PATCH(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session || (session.user.role !== "vet" && session.user.role !== "admin")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const { id, status } = await req.json();
    if (!id || !status) {
      return NextResponse.json({ error: "ID and status are required" }, { status: 400 });
    }

    const record = await prisma.vaccinationRecord.update({
      where: { id },
      data: {
        status,
        administeredAt: status === "done" ? new Date() : null,
      },
    });

    return NextResponse.json({ record });
  } catch (error: any) {
    console.error("[Vaccination Status Error]", error);
    return NextResponse.json({ error: error.message || "Failed to update record" }, { status: 500 });
  }
}

import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// GET /api/cattle/[id]/vaccination-log
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const logs = await prisma.vaccinationLog.findMany({
    where: { cattleId: id },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json({ logs });
}

// POST /api/cattle/[id]/vaccination-log
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = await request.json();
  const { vaccineName, dateGiven, nextDueDate } = body;

  if (!vaccineName || typeof vaccineName !== "string" || vaccineName.trim().length === 0) {
    return NextResponse.json({ error: "vaccineName is required" }, { status: 400 });
  }

  const cattle = await prisma.cattle.findUnique({ where: { id } });
  if (!cattle) return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (session.user.role === "farmer" && cattle.farmerId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const log = await prisma.vaccinationLog.create({
    data: {
      cattleId: id,
      vaccineName: vaccineName.trim(),
      dateGiven: dateGiven ? new Date(dateGiven) : new Date(),
      nextDueDate: nextDueDate ? new Date(nextDueDate) : null,
    },
  });

  // Also maintain VaccinationRecord for veterinary dashboard sync
  await prisma.vaccinationRecord.create({
    data: {
      cattleId: id,
      vaccineType: vaccineName.trim(),
      status: "done",
      administeredAt: dateGiven ? new Date(dateGiven) : new Date(),
      dueAt: nextDueDate ? new Date(nextDueDate) : new Date(),
      notes: "Logged via recurring cattle vaccination log",
    },
  });

  return NextResponse.json({ log }, { status: 201 });
}

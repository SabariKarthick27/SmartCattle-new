import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { runCHDIPipeline } from "@/lib/chdi/pipeline";

// GET /api/cattle/[id]/milk-log
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const logs = await prisma.milkLog.findMany({
    where: { cattleId: id },
    orderBy: { timestamp: "desc" },
    take: 90,
  });

  return NextResponse.json({ logs });
}

// POST /api/cattle/[id]/milk-log
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = await request.json();
  const { litres, source = "manual", timestamp } = body;

  if (litres === undefined || litres === null || isNaN(Number(litres)) || Number(litres) < 0) {
    return NextResponse.json({ error: "litres (L/day) is required and must be non-negative" }, { status: 400 });
  }

  const cattle = await prisma.cattle.findUnique({ where: { id } });
  if (!cattle) return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (session.user.role === "farmer" && cattle.farmerId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const log = await prisma.milkLog.create({
    data: {
      cattleId: id,
      litres: Number(litres),
      source,
      timestamp: timestamp ? new Date(timestamp) : new Date(),
    },
  });

  // Re-run CHDI pipeline
  runCHDIPipeline(id, session.user.id).catch(console.error);

  return NextResponse.json({ log }, { status: 201 });
}

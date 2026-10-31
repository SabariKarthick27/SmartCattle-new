import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { runCHDIPipeline } from "@/lib/chdi/pipeline";

// GET /api/cattle/[id]/rumination-log
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const logs = await (prisma as any).ruminationLog.findMany({
    where: { cattleId: id },
    orderBy: { timestamp: "desc" },
    take: 90,
  });

  return NextResponse.json({ logs });
}

// POST /api/cattle/[id]/rumination-log
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = await request.json();
  const { minutes, source = "manual", timestamp } = body;

  if (minutes === undefined || minutes === null || isNaN(Number(minutes)) || Number(minutes) < 0 || Number(minutes) > 1440) {
    return NextResponse.json({ error: "Rumination minutes must be between 0 and 1440 minutes/day" }, { status: 400 });
  }

  const cattle = await prisma.cattle.findUnique({ where: { id } });
  if (!cattle) return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (session.user.role === "farmer" && cattle.farmerId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const log = await (prisma as any).ruminationLog.create({
    data: {
      cattleId: id,
      minutes: Number(minutes),
      source,
      timestamp: timestamp ? new Date(timestamp) : new Date(),
    },
  });

  // Re-run CHDI pipeline
  runCHDIPipeline(id, session.user.id).catch(console.error);

  return NextResponse.json({ log }, { status: 201 });
}

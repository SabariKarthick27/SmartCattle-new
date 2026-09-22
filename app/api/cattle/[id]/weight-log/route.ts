import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { runCHDIPipeline } from "@/lib/chdi/pipeline";

// POST /api/cattle/[id]/weight-log
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const body = await request.json();
  const { value, source = "manual", timestamp } = body;

  if (!value || typeof value !== "number") {
    return NextResponse.json({ error: "value (kg) is required" }, { status: 400 });
  }

  // Verify cattle belongs to this farmer (or admin/vet bypass)
  const cattle = await prisma.cattle.findUnique({ where: { id } });
  if (!cattle) return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (session.user.role === "farmer" && cattle.farmerId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const log = await prisma.weightLog.create({
    data: {
      cattleId: id,
      value,
      source, // "manual" | "qr_scan" | "sensor"
      timestamp: timestamp ? new Date(timestamp) : new Date(),
    },
  });

  // Trigger CHDI pipeline asynchronously
  runCHDIPipeline(id, session.user.id).catch(console.error);

  return NextResponse.json({ log }, { status: 201 });
}

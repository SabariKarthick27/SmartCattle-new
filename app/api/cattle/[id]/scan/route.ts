import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";

// POST /api/cattle/[id]/scan — log a QR scan (public endpoint, verified by qrToken)
// GET  /api/cattle/[id]/scan — resolve qrToken to cattle profile
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const { qrToken, gps } = body;

    // Verify the token matches this cattle
    const cattle = await prisma.cattle.findFirst({
      where: { id, qrToken },
    });

    if (!cattle) {
      return NextResponse.json({ error: "Invalid QR token" }, { status: 404 });
    }

    const scanLog = await prisma.scanLog.create({
      data: {
        cattleId: id,
        gps: gps || null,
      },
    });

    return NextResponse.json({ scanLog, cattle: { tagId: cattle.tagId, breed: cattle.breed } });
  } catch (err) {
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

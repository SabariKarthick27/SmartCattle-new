import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import QRCode from "qrcode";

// GET /api/scan/[token] — resolve QR token to cattle profile (public)
export async function GET(
  request: Request,
  { params }: { params: Promise<{ token: string }> }
) {
  const { token } = await params;
  const cattle = await prisma.cattle.findUnique({
    where: { qrToken: token },
    select: {
      id: true,
      tagId: true,
      breed: true,
      name: true,
      dob: true,
      farmerId: true,
      chdiHistory: {
        orderBy: { timestamp: "desc" },
        take: 1,
        select: { score: true, status: true, confidence: true, topFactors: true, timestamp: true },
      },
    },
  });

  if (!cattle) {
    return NextResponse.json({ error: "Invalid or expired QR code" }, { status: 404 });
  }

  // Log the scan
  await prisma.scanLog.create({
    data: { cattleId: cattle.id },
  });

  return NextResponse.json({ cattle, cattleId: cattle.id });
}

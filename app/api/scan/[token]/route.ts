import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import QRCode from "qrcode";

// GET /api/scan/[token] — resolve QR token to cattle profile (public/farmer)
export async function GET(
  request: Request,
  { params }: { params: Promise<{ token: string }> }
) {
  const { token } = await params;
  const decodedToken = decodeURIComponent(token).trim();

  const selectFields = {
    id: true,
    tagId: true,
    qrToken: true,
    breed: true,
    name: true,
    dob: true,
    gender: true,
    purpose: true,
    farmerId: true,
    farmer: { select: { id: true, name: true, phone: true } },
    chdiHistory: {
      orderBy: { timestamp: "desc" as const },
      take: 1,
      select: { score: true, status: true, confidence: true, topFactors: true, timestamp: true },
    },
    weightLogs: { orderBy: { timestamp: "desc" as const }, take: 1, select: { value: true, timestamp: true } },
    milkLogs: { orderBy: { timestamp: "desc" as const }, take: 1, select: { litres: true, timestamp: true } },
    feedLogs: { orderBy: { timestamp: "desc" as const }, take: 1, select: { quantity: true, feedType: true, timestamp: true } },
    temperatureLogs: { orderBy: { timestamp: "desc" as const }, take: 1, select: { value: true, timestamp: true } },
    activityLogs: { orderBy: { timestamp: "desc" as const }, take: 1, select: { value: true, timestamp: true } },
    ruminationLogs: { orderBy: { timestamp: "desc" as const }, take: 1, select: { minutes: true, timestamp: true } },
    vaccinations: { where: { status: "upcoming" }, orderBy: { dueAt: "asc" as const }, take: 1, select: { vaccineType: true, dueAt: true } },
  };

  let cattle = await prisma.cattle.findUnique({
    where: { qrToken: decodedToken },
    select: selectFields,
  });

  if (!cattle) {
    cattle = await prisma.cattle.findFirst({
      where: {
        OR: [
          { tagId: { equals: decodedToken, mode: "insensitive" } },
          { id: decodedToken },
        ],
      },
      select: selectFields,
    });
  }

  if (!cattle) {
    return NextResponse.json({ error: "Invalid or expired QR code" }, { status: 404 });
  }

  // Log the scan
  await prisma.scanLog.create({
    data: { cattleId: cattle.id },
  }).catch(() => {});

  return NextResponse.json({ cattle, cattleId: cattle.id });
}

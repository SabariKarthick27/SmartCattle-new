import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// GET /api/vet/queue — vet's case queue sorted by urgency
export async function GET(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "vet") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const region = searchParams.get("region");
  const status = searchParams.get("status");
  const urgency = searchParams.get("urgency");

  const cases = await prisma.vetCase.findMany({
    where: {
      status: status
        ? { equals: status as "open" | "in_progress" | "resolved" | "closed" }
        : { in: ["open", "in_progress"] },
      urgency: urgency ? { equals: urgency as "low" | "medium" | "high" | "critical" } : undefined,
      cattle: region ? { region } : undefined,
      OR: [
        { vetId: session.user.id },
        { vetId: null }, // Unassigned cases in region
      ],
    },
    include: {
      cattle: {
        select: {
          tagId: true,
          breed: true,
          name: true,
          region: true,
          chdiHistory: {
            orderBy: { timestamp: "desc" },
            take: 5,
            select: { score: true, status: true, timestamp: true },
          },
        },
      },
      farmer: { select: { name: true, phone: true } },
    },
    orderBy: [
      { urgency: "desc" },
      { createdAt: "asc" },
    ],
  });

  return NextResponse.json({ cases });
}

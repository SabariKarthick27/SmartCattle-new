import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// GET /api/vets — list all active veterinarians for selection
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const vets = await prisma.user.findMany({
    where: { role: "vet", isActive: true },
    select: {
      id: true,
      name: true,
      email: true,
      phone: true,
      assignedRegion: true,
      isVerified: true,
    },
    orderBy: [{ assignedRegion: "asc" }, { name: "asc" }],
  });

  return NextResponse.json({ vets });
}


import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// GET /api/admin/users — list all users
// POST /api/admin/users — approve/reject/update user
export async function GET(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const role = searchParams.get("role");
  const verified = searchParams.get("verified");

  const users = await prisma.user.findMany({
    where: {
      role: role ? (role as "farmer" | "vet" | "admin") : { in: ["farmer", "vet"] },
      isVerified: verified !== null ? verified === "true" : undefined,
    },
    select: {
      id: true,
      name: true,
      email: true,
      phone: true,
      role: true,
      farmId: true,
      assignedRegion: true,
      isVerified: true,
      isActive: true,
      createdAt: true,
    },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json({ users });
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { userId, action, assignedRegion } = body;

  // action: "approve" | "reject" | "deactivate" | "reactivate"
  if (!userId || !action) {
    return NextResponse.json({ error: "userId and action are required" }, { status: 400 });
  }

  const updateData: Record<string, unknown> = {};
  let auditAction = action;

  switch (action) {
    case "approve":
      updateData.isVerified = true;
      updateData.isActive = true;
      break;
    case "reject":
      updateData.isVerified = false;
      updateData.isActive = false;
      break;
    case "deactivate":
      updateData.isActive = false;
      break;
    case "reactivate":
      updateData.isActive = true;
      break;
    case "assign_region":
      updateData.assignedRegion = assignedRegion;
      break;
    default:
      return NextResponse.json({ error: "Invalid action" }, { status: 400 });
  }

  const user = await prisma.user.update({
    where: { id: userId },
    data: updateData,
    select: { id: true, name: true, email: true, role: true, isVerified: true, isActive: true },
  });

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "admin",
      action: `admin_${auditAction}`,
      targetId: userId,
      metadata: JSON.parse(JSON.stringify(updateData)),
    },
  });

  return NextResponse.json({ user });
}

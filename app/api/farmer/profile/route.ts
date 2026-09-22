import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import bcrypt from "bcryptjs";

// GET /api/farmer/profile — Get farmer's details & statistics
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "farmer") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
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
      _count: {
        select: { cattle: true },
      },
    },
  });

  if (!user) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  return NextResponse.json({ user });
}

// PUT /api/farmer/profile — Update details and/or reset password
export async function PUT(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "farmer") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();
    const { name, phone, farmId, assignedRegion, currentPassword, newPassword } = body;

    const user = await prisma.user.findUnique({
      where: { id: session.user.id },
    });

    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 });
    }

    const updateData: Record<string, unknown> = {};

    // 1. Details update
    if (name) updateData.name = name;
    if (phone) updateData.phone = phone;
    if (farmId !== undefined) updateData.farmId = farmId || null;
    if (assignedRegion !== undefined) updateData.assignedRegion = assignedRegion || null;

    // 2. Password reset if requested
    if (newPassword) {
      if (!currentPassword) {
        return NextResponse.json(
          { error: "Current password is required to set a new password." },
          { status: 400 }
        );
      }

      if (newPassword.length < 8) {
        return NextResponse.json(
          { error: "New password must be at least 8 characters long." },
          { status: 400 }
        );
      }

      const isMatch = await bcrypt.compare(currentPassword, user.passwordHash);
      if (!isMatch) {
        return NextResponse.json(
          { error: "Incorrect current password. Please try again." },
          { status: 400 }
        );
      }

      updateData.passwordHash = await bcrypt.hash(newPassword, 12);
    }

    if (Object.keys(updateData).length === 0) {
      return NextResponse.json({ message: "No changes provided" });
    }

    const updatedUser = await prisma.user.update({
      where: { id: session.user.id },
      data: updateData,
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
    });

    // Audit log
    await prisma.auditLog.create({
      data: {
        actorId: session.user.id,
        actorRole: "farmer",
        action: newPassword ? "profile_and_password_updated" : "profile_updated",
        targetId: session.user.id,
        metadata: { name: updatedUser.name, passwordChanged: Boolean(newPassword) },
      },
    });

    return NextResponse.json({
      user: updatedUser,
      message: newPassword ? "Profile and password updated successfully!" : "Profile updated successfully!",
    });
  } catch (err: any) {
    console.error("[Profile API Error]", err);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

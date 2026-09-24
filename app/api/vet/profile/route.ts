import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import bcrypt from "bcryptjs";

// GET /api/vet/profile — Get veterinarian's profile details & clinical statistics
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "vet") {
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
      assignedRegion: true,
      photoUrl: true,
      isVerified: true,
      isActive: true,
      createdAt: true,
      _count: {
        select: {
          vetCases: true,
        },
      },
    },
  });

  if (!user) {
    return NextResponse.json({ error: "Veterinarian not found" }, { status: 404 });
  }

  return NextResponse.json({ user });
}

// PUT /api/vet/profile — Update details and/or reset password
export async function PUT(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "vet") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();
    const { name, phone, assignedRegion, photoUrl, currentPassword, newPassword } = body;

    const user = await prisma.user.findUnique({
      where: { id: session.user.id },
    });

    if (!user) {
      return NextResponse.json({ error: "Veterinarian not found" }, { status: 404 });
    }

    const updateData: Record<string, unknown> = {};

    // 1. Details update
    if (name) updateData.name = name.trim();
    if (phone) updateData.phone = phone.trim();
    if (assignedRegion !== undefined) updateData.assignedRegion = assignedRegion?.trim() || null;
    if (photoUrl !== undefined) {
      updateData.photoUrl = photoUrl || null;
      updateData.image = photoUrl || null;
    }

    // 2. Password reset if requested
    if (newPassword) {
      if (!currentPassword) {
        return NextResponse.json(
          { error: "Current password is required to change password." },
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
        assignedRegion: true,
        photoUrl: true,
        isVerified: true,
        isActive: true,
        createdAt: true,
      },
    });

    return NextResponse.json({
      success: true,
      message: "Veterinarian profile updated successfully!",
      user: updatedUser,
    });
  } catch (error: any) {
    console.error("Error updating vet profile:", error);
    return NextResponse.json(
      { error: error?.message || "Failed to update profile." },
      { status: 500 }
    );
  }
}

import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import bcrypt from "bcryptjs";

// GET /api/admin/users — list all users with stats & available vets
export async function GET(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const role = searchParams.get("role");
  const verified = searchParams.get("verified");

  const [users, vets] = await Promise.all([
    prisma.user.findMany({
      where: {
        role: role ? (role as "farmer" | "vet" | "admin") : undefined,
        isVerified: verified !== null && verified !== "" ? verified === "true" : undefined,
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
        _count: {
          select: {
            cattle: true,
            vetCases: true,
            farmerCases: true,
          },
        },
      },
      orderBy: { createdAt: "desc" },
    }),
    prisma.user.findMany({
      where: { role: "vet", isActive: true },
      select: {
        id: true,
        name: true,
        email: true,
        phone: true,
        assignedRegion: true,
      },
      orderBy: { name: "asc" },
    }),
  ]);

  return NextResponse.json({ users, vets });
}

// POST /api/admin/users — quick action or create new user
export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { action } = body;

  // Create new user directly from Admin
  if (action === "create") {
    const { name, email, phone, password, role, farmId, assignedRegion, isVerified } = body;

    if (!name || !email || !password || !role) {
      return NextResponse.json({ error: "Name, email, password, and role are required" }, { status: 400 });
    }

    const existing = await prisma.user.findUnique({
      where: { email: email.toLowerCase().trim() },
    });
    if (existing) {
      return NextResponse.json({ error: "A user with this email address already exists" }, { status: 400 });
    }

    const passwordHash = await bcrypt.hash(password, 10);
    const newUser = await prisma.user.create({
      data: {
        name: name.trim(),
        email: email.toLowerCase().trim(),
        phone: phone?.trim() || "",
        passwordHash,
        role: role as "farmer" | "vet" | "admin",
        farmId: farmId?.trim() || null,
        assignedRegion: assignedRegion?.trim() || null,
        isVerified: isVerified !== undefined ? Boolean(isVerified) : true,
        isActive: true,
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
    });

    await prisma.auditLog.create({
      data: {
        actorId: session.user.id,
        actorRole: "admin",
        action: "admin_create_user",
        targetId: newUser.id,
        metadata: { role, email: newUser.email, name: newUser.name, region: newUser.assignedRegion, farmId: newUser.farmId },
      },
    });

    return NextResponse.json({ user: newUser, message: "User account created successfully" }, { status: 201 });
  }

  const { userId, assignedRegion, farmId } = body;
  if (!userId || !action) {
    return NextResponse.json({ error: "userId and action are required" }, { status: 400 });
  }

  const updateData: Record<string, unknown> = {};
  const auditAction = action;

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
    case "assign_farm":
      updateData.farmId = farmId;
      break;
    default:
      return NextResponse.json({ error: "Invalid action" }, { status: 400 });
  }

  const user = await prisma.user.update({
    where: { id: userId },
    data: updateData,
    select: { id: true, name: true, email: true, role: true, isVerified: true, isActive: true, assignedRegion: true, farmId: true },
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

// PUT /api/admin/users — full editable updates for any user (name, email, phone, role, farm, region, verification, status, password)
export async function PUT(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { userId, name, email, phone, role, farmId, assignedRegion, isVerified, isActive, newPassword } = body;

  if (!userId) {
    return NextResponse.json({ error: "userId is required" }, { status: 400 });
  }

  const existingUser = await prisma.user.findUnique({ where: { id: userId } });
  if (!existingUser) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  // Check if email already used by someone else
  if (email && email.toLowerCase().trim() !== existingUser.email.toLowerCase()) {
    const conflict = await prisma.user.findUnique({ where: { email: email.toLowerCase().trim() } });
    if (conflict) {
      return NextResponse.json({ error: "This email address is already in use by another account" }, { status: 400 });
    }
  }

  const updateData: Record<string, unknown> = {};
  if (name !== undefined) updateData.name = name.trim();
  if (email !== undefined) updateData.email = email.toLowerCase().trim();
  if (phone !== undefined) updateData.phone = phone.trim();
  if (role !== undefined) updateData.role = role as "farmer" | "vet" | "admin";
  if (farmId !== undefined) updateData.farmId = farmId ? farmId.trim() : null;
  if (assignedRegion !== undefined) updateData.assignedRegion = assignedRegion ? assignedRegion.trim() : null;
  if (isVerified !== undefined) updateData.isVerified = Boolean(isVerified);
  if (isActive !== undefined) updateData.isActive = Boolean(isActive);

  if (newPassword && newPassword.trim().length >= 6) {
    updateData.passwordHash = await bcrypt.hash(newPassword.trim(), 10);
  }

  const updatedUser = await prisma.user.update({
    where: { id: userId },
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

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "admin",
      action: "admin_update_user_full",
      targetId: userId,
      metadata: {
        name: updatedUser.name,
        email: updatedUser.email,
        role: updatedUser.role,
        farmId: updatedUser.farmId,
        assignedRegion: updatedUser.assignedRegion,
        isVerified: updatedUser.isVerified,
        isActive: updatedUser.isActive,
        passwordUpdated: Boolean(newPassword),
      },
    },
  });

  return NextResponse.json({ user: updatedUser, message: "User account updated successfully" });
}

// DELETE /api/admin/users — safe deletion with cascade cleanup
export async function DELETE(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const userId = searchParams.get("userId");

  if (!userId) {
    return NextResponse.json({ error: "userId query parameter is required" }, { status: 400 });
  }

  if (userId === session.user.id) {
    return NextResponse.json({ error: "You cannot delete your own admin account while logged in." }, { status: 400 });
  }

  const target = await prisma.user.findUnique({
    where: { id: userId },
    include: { cattle: true },
  });

  if (!target) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  // Safe cascading cleanup
  // 1. Delete reset tokens
  await prisma.passwordResetToken.deleteMany({ where: { userId } });

  // 2. Delete audit logs referencing this user as actor
  await prisma.auditLog.deleteMany({ where: { actorId: userId } });

  // 3. Vet feedback
  await prisma.vetFeedback.deleteMany({ where: { vetId: userId } });

  // 4. If vet, unassign from vet cases
  await prisma.vetCase.updateMany({
    where: { vetId: userId },
    data: { vetId: null },
  });

  // 5. If farmer, delete their cattle and related logs
  if (target.cattle && target.cattle.length > 0) {
    for (const cow of target.cattle) {
      await prisma.vetFeedback.deleteMany({ where: { cattleId: cow.id } });
      await prisma.vetCase.deleteMany({ where: { cattleId: cow.id } });
      await prisma.vaccinationRecord.deleteMany({ where: { cattleId: cow.id } });
      await prisma.vaccinationLog.deleteMany({ where: { cattleId: cow.id } });
      await prisma.scanLog.deleteMany({ where: { cattleId: cow.id } });
      await prisma.cHDIEntry.deleteMany({ where: { cattleId: cow.id } });
      await prisma.milkLog.deleteMany({ where: { cattleId: cow.id } });
      await prisma.activityLog.deleteMany({ where: { cattleId: cow.id } });
      await prisma.feedLog.deleteMany({ where: { cattleId: cow.id } });
      await prisma.weightLog.deleteMany({ where: { cattleId: cow.id } });
      await prisma.cattle.delete({ where: { id: cow.id } });
    }
  }

  // 6. Delete cases where user was farmer
  await prisma.vetCase.deleteMany({ where: { farmerId: userId } });

  // 7. Delete the user
  await prisma.user.delete({ where: { id: userId } });

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "admin",
      action: "admin_delete_user",
      targetId: userId,
      metadata: { deletedName: target.name, deletedEmail: target.email, role: target.role },
    },
  });

  return NextResponse.json({ success: true, message: `Account for ${target.name} (${target.email}) deleted successfully.` });
}

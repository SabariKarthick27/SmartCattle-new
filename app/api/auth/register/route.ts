import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import bcrypt from "bcryptjs";

// POST /api/auth/register
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, phone, email, password, role, farmId, assignedRegion } = body;

    if (!name || !phone || !email || !password || !role) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 });
    }

    if (!["farmer", "vet"].includes(role)) {
      return NextResponse.json({ error: "Invalid role. Only farmer or vet can self-register." }, { status: 400 });
    }

    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      return NextResponse.json({ error: "Email already registered" }, { status: 409 });
    }

    const passwordHash = await bcrypt.hash(password, 12);

    const user = await prisma.user.create({
      data: {
        name,
        phone,
        email,
        passwordHash,
        role,
        farmId: farmId || null,
        assignedRegion: assignedRegion || null,
        isVerified: false, // Admin must approve
      },
      select: { id: true, name: true, email: true, role: true, isVerified: true },
    });

    // Audit log
    await prisma.auditLog.create({
      data: {
        actorId: user.id,
        actorRole: role,
        action: "user_registered",
        targetId: user.id,
        metadata: { email, role },
      },
    });

    return NextResponse.json({
      message: "Registration successful. Awaiting admin approval.",
      user,
    }, { status: 201 });
  } catch (err) {
    console.error("[Register API]", err);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

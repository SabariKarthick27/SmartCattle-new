import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// GET /api/cattle/[id] — full cattle profile
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const cattle = await prisma.cattle.findUnique({
    where: { id },
    include: {
      chdiHistory: {
        orderBy: { timestamp: "desc" },
        take: 365,
      },
      weightLogs: { orderBy: { timestamp: "desc" }, take: 90 },
      feedLogs: { orderBy: { timestamp: "desc" }, take: 90 },
      activityLogs: { orderBy: { timestamp: "desc" }, take: 90 },
      scanLogs: { orderBy: { timestamp: "desc" }, take: 30 },
      vaccinations: { orderBy: { dueAt: "asc" } },
      vetCases: {
        orderBy: { createdAt: "desc" },
        take: 10,
        include: { vet: { select: { name: true } } },
      },
    },
  });

  if (!cattle) return NextResponse.json({ error: "Not found" }, { status: 404 });

  // Access control: farmers can only see their own cattle, vets see all
  if (
    session.user.role === "farmer" &&
    cattle.farmerId !== session.user.id
  ) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  return NextResponse.json({ cattle });
}

// PATCH /api/cattle/[id] — update cattle details
export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const cattle = await prisma.cattle.findUnique({
    where: { id },
  });

  if (!cattle) return NextResponse.json({ error: "Not found" }, { status: 404 });

  // Access control: farmers can only edit their own cattle, admin can edit any
  if (session.user.role === "farmer" && cattle.farmerId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  try {
    const body = await request.json();
    const {
      tagId,
      name,
      breed,
      gender,
      dob,
      dateOfBirth,
      approxAge,
      purpose,
      region,
      previousCalvings,
      pastVaccinations,
      photoUrl,
      isActive,
    } = body;

    // Check tagId uniqueness if changed
    if (tagId && tagId.trim() !== cattle.tagId) {
      const existingTag = await prisma.cattle.findUnique({
        where: { tagId: tagId.trim() },
      });
      if (existingTag && existingTag.id !== id) {
        return NextResponse.json(
          { error: `Tag ID "${tagId}" is already assigned to another cattle.` },
          { status: 400 }
        );
      }
    }

    // Determine birthDate and ageGroup if DOB / approxAge provided
    let newDob: Date | undefined = undefined;
    let newAgeGroup: string | undefined = undefined;

    const rawDob = dob || dateOfBirth;
    if (rawDob) {
      newDob = new Date(rawDob);
    } else if (approxAge !== undefined && approxAge !== null && !isNaN(Number(approxAge))) {
      const ageNum = Number(approxAge);
      const months = ageNum <= 25 ? ageNum * 12 : ageNum;
      newDob = new Date(Date.now() - months * 30.4375 * 24 * 60 * 60 * 1000);
    }

    if (newDob) {
      const now = new Date();
      const diffMonths = (now.getTime() - newDob.getTime()) / (1000 * 60 * 60 * 24 * 30.4375);
      newAgeGroup = diffMonths < 12 ? "calf" : diffMonths <= 84 ? "adult" : "senior";
    }

    const updatedCattle = await prisma.cattle.update({
      where: { id },
      data: {
        ...(tagId ? { tagId: tagId.trim() } : {}),
        ...(name !== undefined ? { name: name?.trim() || null } : {}),
        ...(breed ? { breed: breed.trim() } : {}),
        ...(gender ? { gender } : {}),
        ...(newDob ? { dob: newDob } : {}),
        ...(newAgeGroup ? { ageGroup: newAgeGroup } : {}),
        ...(purpose ? { purpose } : {}),
        ...(region !== undefined ? { region: region?.trim() || null } : {}),
        ...(previousCalvings !== undefined
          ? { previousCalvings: Math.max(0, parseInt(String(previousCalvings)) || 0) }
          : {}),
        ...(pastVaccinations !== undefined
          ? { pastVaccinations: Array.isArray(pastVaccinations) ? pastVaccinations : [] }
          : {}),
        ...(photoUrl !== undefined ? { photoUrl: photoUrl?.trim() || null } : {}),
        ...(isActive !== undefined ? { isActive: Boolean(isActive) } : {}),
      },
    });

    return NextResponse.json({ success: true, cattle: updatedCattle });
  } catch (error: any) {
    console.error("Failed to update cattle:", error);
    return NextResponse.json(
      { error: error?.message || "Failed to update cattle details." },
      { status: 500 }
    );
  }
}


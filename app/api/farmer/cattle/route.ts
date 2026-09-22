import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import QRCode from "qrcode";
import { cuid } from "@/lib/utils";

// GET /api/farmer/cattle — list all cattle for the logged-in farmer
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "farmer") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const cattle = await prisma.cattle.findMany({
    where: { farmerId: session.user.id, isActive: true },
    include: {
      chdiHistory: {
        orderBy: { timestamp: "desc" },
        take: 1,
      },
      vaccinations: {
        where: { status: { in: ["upcoming", "overdue"] } },
        orderBy: { dueAt: "asc" },
        take: 1,
      },
    },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json({ cattle });
}

// POST /api/farmer/cattle — add new cattle + generate QR
export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "farmer") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();
    const {
      tagId,
      name,
      breed,
      gender = "female",
      dob,
      dateOfBirth,
      approxAge,
      photo,
      photoUrl,
      region,
      purpose = "dairy",
      previousCalvings = 0,
      pastVaccinations = [],
      initialWeight,
      initialMilkYield,
    } = body;

    // Validate required static fields
    if (!tagId || !breed) {
      return NextResponse.json(
        { error: "tagId and breed are required" },
        { status: 400 }
      );
    }

    // Determine Date of Birth
    let birthDate: Date;
    const rawDob = dob || dateOfBirth;
    if (rawDob) {
      birthDate = new Date(rawDob);
    } else if (approxAge !== undefined && approxAge !== null && !isNaN(Number(approxAge))) {
      const ageNum = Number(approxAge);
      const months = ageNum <= 25 ? ageNum * 12 : ageNum;
      birthDate = new Date(Date.now() - months * 30.4375 * 24 * 60 * 60 * 1000);
    } else {
      return NextResponse.json(
        { error: "dateOfBirth or approxAge is required" },
        { status: 400 }
      );
    }

    // Validate initialWeight (day-1 entry requirement)
    if (initialWeight === undefined || initialWeight === null || isNaN(Number(initialWeight))) {
      return NextResponse.json(
        { error: "initialWeight (kg) is required as a day-1 log entry" },
        { status: 400 }
      );
    }

    // Validate purpose
    const validPurposes = ["dairy", "breeding", "draft"];
    const resolvedPurpose = validPurposes.includes(purpose) ? purpose : "dairy";

    // ── 2. Derive ageGroup ("calf" | "adult" | "senior") ───────
    const now = new Date();
    const diffMonths = (now.getTime() - birthDate.getTime()) / (1000 * 60 * 60 * 24 * 30.4375);
    const ageGroup = diffMonths < 12 ? "calf" : diffMonths <= 84 ? "adult" : "senior";

    // Generate unique QR token
    const qrToken = `SC-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

    // Normalize pastVaccinations array
    const vaccineList: string[] = Array.isArray(pastVaccinations)
      ? pastVaccinations.filter((v): v is string => typeof v === "string" && v.trim().length > 0)
      : typeof pastVaccinations === "string" && pastVaccinations.trim().length > 0
      ? pastVaccinations.split(",").map((s) => s.trim())
      : [];

    // Create cattle record (static fields only)
    const cattle = await prisma.cattle.create({
      data: {
        farmerId: session.user.id,
        tagId,
        qrToken,
        name: name || null,
        breed,
        gender: gender || "female",
        dob: birthDate,
        photoUrl: photo || photoUrl || null,
        region: region || null,
        purpose: resolvedPurpose,
        ageGroup,
        previousCalvings: Number(previousCalvings) || 0,
        pastVaccinations: vaccineList,
      },
    });

    // ── 1. Seed initialWeight into WeightLog (day-1 entry) ─────
    await prisma.weightLog.create({
      data: {
        cattleId: cattle.id,
        value: Number(initialWeight),
        timestamp: now,
        source: "manual",
      },
    });

    // ── 1. Seed initialMilkYield into MilkLog (if dairy) ───────
    if (
      resolvedPurpose === "dairy" &&
      initialMilkYield !== undefined &&
      initialMilkYield !== null &&
      !isNaN(Number(initialMilkYield))
    ) {
      await prisma.milkLog.create({
        data: {
          cattleId: cattle.id,
          litres: Number(initialMilkYield),
          timestamp: now,
          source: "manual",
        },
      });
    }

    // ── Seed pastVaccinations into VaccinationLog & records ───
    if (vaccineList.length > 0) {
      for (const vaccineName of vaccineList) {
        await prisma.vaccinationLog.create({
          data: {
            cattleId: cattle.id,
            vaccineName,
            dateGiven: now,
            nextDueDate: null,
          },
        });
        await prisma.vaccinationRecord.create({
          data: {
            cattleId: cattle.id,
            vaccineType: vaccineName,
            status: "done",
            dueAt: now,
            administeredAt: now,
            notes: "Recorded during initial registration",
          },
        });
      }
    }

    // ── 2. Create one CHDIEntry immediately with abstaining status ──
    // Do NOT run computeBaseline() or computeCHDI() at creation time
    await prisma.cHDIEntry.create({
      data: {
        cattleId: cattle.id,
        status: "abstain",
        confidence: 0,
        score: null,
        topFactors: [],
        timestamp: now,
      },
    });

    // Generate QR image as data URL (encodes qrToken, not raw animal data)
    const qrDataUrl = await QRCode.toDataURL(
      `${process.env.NEXT_PUBLIC_APP_URL}/scan/${qrToken}`,
      { width: 256, margin: 2, color: { dark: "#0F5132", light: "#FFFFFF" } }
    );

    // Audit log
    await prisma.auditLog.create({
      data: {
        actorId: session.user.id,
        actorRole: "farmer",
        action: "cattle_created",
        targetId: cattle.id,
        metadata: {
          tagId,
          breed,
          purpose: resolvedPurpose,
          ageGroup,
          previousCalvings,
          initialWeight,
          initialMilkYield: resolvedPurpose === "dairy" ? initialMilkYield : null,
        },
      },
    });

    return NextResponse.json({ cattle, qrDataUrl }, { status: 201 });
  } catch (err: any) {
    if (err?.code === "P2002") {
      return NextResponse.json({ error: "Tag ID already exists" }, { status: 409 });
    }
    console.error("[Add Cattle API]", err);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

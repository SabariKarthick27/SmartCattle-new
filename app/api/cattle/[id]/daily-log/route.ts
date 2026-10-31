import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { runCHDIPipeline } from "@/lib/chdi/pipeline";

/**
 * POST /api/cattle/[id]/daily-log
 *
 * Saves a consolidated daily health check-in record for cattle directly
 * from the QR scanning workflow. Captures:
 *  - Body Weight (kg)
 *  - Feed Intake (kg) + feedType
 *  - Milk Production (litres)
 *  - Body Temperature (°C)
 *  - Activity (score / index)
 *  - Rumination (minutes/day)
 *
 * Automatically records the source as "qr_scan" and executes the full
 * 3-Stage CHDI analytical engine pipeline in real-time.
 */
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ error: "Unauthorized. Please sign in." }, { status: 401 });
  }

  // 1. Verify cattle existence & ownership permissions
  const cattle = await prisma.cattle.findUnique({
    where: { id },
    select: { id: true, tagId: true, name: true, farmerId: true, purpose: true },
  });

  if (!cattle) {
    return NextResponse.json({ error: "Cattle record not found." }, { status: 404 });
  }

  if (session.user.role === "farmer" && cattle.farmerId !== session.user.id) {
    return NextResponse.json(
      { error: "Forbidden. You are not authorized to log data for this cattle." },
      { status: 403 }
    );
  }

  // 2. Parse & validate request payload
  let body: Record<string, any>;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON payload." }, { status: 400 });
  }

  const {
    weight,
    feedQuantity,
    feedType = "Mixed Green Grass / Fodder",
    milkLitres,
    temperature,
    activity,
    rumination,
    date,
    source = "qr_scan",
  } = body;

  const logTimestamp = date ? new Date(date) : new Date();
  if (isNaN(logTimestamp.getTime())) {
    return NextResponse.json({ error: "Invalid date or timestamp provided." }, { status: 400 });
  }

  // Helper validation parsing
  const parsedWeight =
    weight !== undefined && weight !== null && weight !== "" ? Number(weight) : null;
  const parsedFeed =
    feedQuantity !== undefined && feedQuantity !== null && feedQuantity !== ""
      ? Number(feedQuantity)
      : null;
  const parsedMilk =
    milkLitres !== undefined && milkLitres !== null && milkLitres !== ""
      ? Number(milkLitres)
      : null;
  const parsedTemp =
    temperature !== undefined && temperature !== null && temperature !== ""
      ? Number(temperature)
      : null;
  const parsedActivity =
    activity !== undefined && activity !== null && activity !== ""
      ? Number(activity)
      : null;
  const parsedRumination =
    rumination !== undefined && rumination !== null && rumination !== ""
      ? Number(rumination)
      : null;

  // At least one health vital metric must be supplied
  const hasAtLeastOne =
    parsedWeight !== null ||
    parsedFeed !== null ||
    parsedMilk !== null ||
    parsedTemp !== null ||
    parsedActivity !== null ||
    parsedRumination !== null;

  if (!hasAtLeastOne) {
    return NextResponse.json(
      { error: "Please enter at least one daily health vital metric to save." },
      { status: 400 }
    );
  }

  // Range checks
  if (parsedWeight !== null && (isNaN(parsedWeight) || parsedWeight <= 0 || parsedWeight > 2000)) {
    return NextResponse.json(
      { error: "Body Weight must be a valid number between 1 kg and 2000 kg." },
      { status: 400 }
    );
  }

  if (parsedFeed !== null && (isNaN(parsedFeed) || parsedFeed < 0 || parsedFeed > 150)) {
    return NextResponse.json(
      { error: "Feed Intake must be a valid number between 0 kg and 150 kg." },
      { status: 400 }
    );
  }

  if (parsedMilk !== null && (isNaN(parsedMilk) || parsedMilk < 0 || parsedMilk > 100)) {
    return NextResponse.json(
      { error: "Daily Milk Production must be a valid number between 0 L and 100 L." },
      { status: 400 }
    );
  }

  if (parsedTemp !== null && (isNaN(parsedTemp) || parsedTemp < 30.0 || parsedTemp > 45.0)) {
    return NextResponse.json(
      { error: "Body Temperature must be a realistic reading between 30.0°C and 45.0°C." },
      { status: 400 }
    );
  }

  if (parsedActivity !== null && (isNaN(parsedActivity) || parsedActivity < 0 || parsedActivity > 100)) {
    return NextResponse.json(
      { error: "Activity Score must be a rating between 0 and 100." },
      { status: 400 }
    );
  }

  if (parsedRumination !== null && (isNaN(parsedRumination) || parsedRumination < 0 || parsedRumination > 1440)) {
    return NextResponse.json(
      { error: "Rumination duration must be between 0 and 1440 minutes/day." },
      { status: 400 }
    );
  }

  // 3. Atomically persist all supplied vitals to database
  const createdRecords: Record<string, any> = {};

  try {
    await prisma.$transaction(async (tx) => {
      // Body Weight
      if (parsedWeight !== null) {
        const wLog = await tx.weightLog.create({
          data: {
            cattleId: id,
            value: parsedWeight,
            source,
            timestamp: logTimestamp,
          },
        });
        createdRecords.weight = wLog.value;
      }

      // Feed Intake
      if (parsedFeed !== null) {
        const fLog = await tx.feedLog.create({
          data: {
            cattleId: id,
            quantity: parsedFeed,
            feedType: String(feedType || "Mixed Green Grass / Fodder"),
            source,
            timestamp: logTimestamp,
          },
        });
        createdRecords.feed = fLog.quantity;
      }

      // Milk Yield
      if (parsedMilk !== null) {
        const mLog = await tx.milkLog.create({
          data: {
            cattleId: id,
            litres: parsedMilk,
            source,
            timestamp: logTimestamp,
          },
        });
        createdRecords.milk = mLog.litres;
      }

      // Body Temperature
      if (parsedTemp !== null) {
        const tLog = await (tx as any).temperatureLog.create({
          data: {
            cattleId: id,
            value: parsedTemp,
            source,
            timestamp: logTimestamp,
          },
        });
        createdRecords.temperature = tLog.value;
      }

      // Activity
      if (parsedActivity !== null) {
        const aLog = await tx.activityLog.create({
          data: {
            cattleId: id,
            value: parsedActivity,
            source,
            timestamp: logTimestamp,
          },
        });
        createdRecords.activity = aLog.value;
      }

      // Rumination
      if (parsedRumination !== null) {
        const rLog = await (tx as any).ruminationLog.create({
          data: {
            cattleId: id,
            minutes: parsedRumination,
            source,
            timestamp: logTimestamp,
          },
        });
        createdRecords.rumination = rLog.minutes;
      }

      // Record Scan Telemetry
      await tx.scanLog.create({
        data: {
          cattleId: id,
          timestamp: logTimestamp,
        },
      });

      // Audit trail
      await tx.auditLog.create({
        data: {
          actorId: session.user.id,
          actorRole: session.user.role,
          action: "daily_health_logged",
          targetId: id,
          metadata: {
            source,
            metrics: createdRecords,
            cattleTag: cattle.tagId,
          },
        },
      });
    });

    // 4. Trigger CHDI Health Assessment pipeline
    const chdiAssessment = await runCHDIPipeline(id, session.user.id);

    return NextResponse.json(
      {
        success: true,
        message: `Daily health record for ${cattle.name || cattle.tagId} saved successfully!`,
        cattleId: cattle.id,
        tagId: cattle.tagId,
        name: cattle.name,
        savedMetrics: createdRecords,
        chdi: chdiAssessment,
        timestamp: logTimestamp.toISOString(),
      },
      { status: 201 }
    );
  } catch (dbError: any) {
    console.error("Error saving daily health record:", dbError);
    return NextResponse.json(
      { error: "Database error saving health records. Please try again." },
      { status: 500 }
    );
  }
}


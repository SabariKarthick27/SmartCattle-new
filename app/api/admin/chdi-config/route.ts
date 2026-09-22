import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// PATCH /api/admin/chdi-config — update CHDI thresholds
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const settings = await prisma.settings.findMany({
    where: { key: { startsWith: "chdi_" } },
  });

  return NextResponse.json({ settings });
}

export async function PATCH(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  // body: { key: string, value: string }[]
  const updates: { key: string; value: string }[] = body.updates ?? [];

  const results = await Promise.all(
    updates.map((u) =>
      prisma.settings.upsert({
        where: { key: u.key },
        create: { key: u.key, value: u.value },
        update: { value: u.value },
      })
    )
  );

  await prisma.auditLog.create({
    data: {
      actorId: session.user.id,
      actorRole: "admin",
      action: "chdi_config_updated",
      metadata: { updates },
    },
  });

  return NextResponse.json({ settings: results });
}

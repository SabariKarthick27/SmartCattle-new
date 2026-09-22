import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";

// GET /api/admin/audit-log
export async function GET(request: Request) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const action = searchParams.get("action");
  const actorRole = searchParams.get("role");
  const from = searchParams.get("from");
  const to = searchParams.get("to");
  const page = parseInt(searchParams.get("page") ?? "1");
  const limit = parseInt(searchParams.get("limit") ?? "50");

  const logs = await prisma.auditLog.findMany({
    where: {
      action: action ? { contains: action } : undefined,
      actorRole: actorRole ?? undefined,
      timestamp: {
        gte: from ? new Date(from) : undefined,
        lte: to ? new Date(to) : undefined,
      },
    },
    include: {
      actor: { select: { name: true, email: true } },
    },
    orderBy: { timestamp: "desc" },
    skip: (page - 1) * limit,
    take: limit,
  });

  const total = await prisma.auditLog.count({
    where: {
      action: action ? { contains: action } : undefined,
      actorRole: actorRole ?? undefined,
    },
  });

  return NextResponse.json({ logs, total, page, limit });
}

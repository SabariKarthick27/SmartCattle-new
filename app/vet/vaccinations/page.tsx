import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import VetVaccinationsClient from "./VetVaccinationsClient";

export default async function VetVaccinationsPage() {
  const session = await getServerSession(authOptions);
  const vetRegion = session?.user?.assignedRegion;

  // Fetch cattle available in vet region
  const cattleList = await prisma.cattle.findMany({
    where: (vetRegion && vetRegion !== "Tamil Nadu" && vetRegion !== "All") ? { region: vetRegion } : {},
    select: {
      id: true,
      tagId: true,
      name: true,
      breed: true,
      farmer: { select: { name: true } },
    },
    orderBy: { tagId: "asc" },
  });

  // Fetch existing vaccination and checkup records
  const records = await prisma.vaccinationRecord.findMany({
    where: (vetRegion && vetRegion !== "Tamil Nadu" && vetRegion !== "All") ? { cattle: { region: vetRegion } } : {},
    include: {
      cattle: {
        select: {
          tagId: true,
          breed: true,
          name: true,
          farmer: { select: { name: true, phone: true } },
        },
      },
    },
    orderBy: { dueAt: "asc" },
  });

  const formattedRecords = records.map((r) => ({
    id: r.id,
    cattleTagId: r.cattle.tagId,
    cattleName: r.cattle.name,
    breed: r.cattle.breed,
    farmerName: r.cattle.farmer.name,
    farmerPhone: r.cattle.farmer.phone,
    vaccineType: r.vaccineType,
    dueAt: r.dueAt.toISOString().split("T")[0],
    administeredAt: r.administeredAt ? r.administeredAt.toISOString().split("T")[0] : null,
    status: r.status,
    notes: r.notes,
  }));

  return (
    <div className="p-8 space-y-6 max-w-6xl">
      <VetVaccinationsClient cattleList={cattleList} initialRecords={formattedRecords} vetRegion={vetRegion} />
    </div>
  );
}

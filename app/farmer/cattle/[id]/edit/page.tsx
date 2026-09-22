import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { notFound, redirect } from "next/navigation";
import EditCattleForm from "./EditCattleForm";

export default async function EditCattlePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const session = await getServerSession(authOptions);

  if (!session) {
    redirect("/login");
  }

  const cattle = await prisma.cattle.findUnique({
    where: { id },
  });

  if (!cattle) notFound();

  // Access control: farmers can only edit their own cattle
  if (session.user.role === "farmer" && cattle.farmerId !== session.user.id) {
    notFound();
  }

  // Format DOB to YYYY-MM-DD for date input
  const dobString = cattle.dob ? new Date(cattle.dob).toISOString().split("T")[0] : "";
  const now = new Date();
  const diffMonths = cattle.dob ? (now.getTime() - new Date(cattle.dob).getTime()) / (1000 * 60 * 60 * 24 * 30.4375) : 0;
  const approxYears = Number((diffMonths / 12).toFixed(1));

  return (
    <div className="p-4 sm:p-8 max-w-3xl mx-auto">
      <EditCattleForm
        cattle={{
          id: cattle.id,
          tagId: cattle.tagId,
          name: cattle.name ?? "",
          breed: cattle.breed,
          gender: cattle.gender ?? "female",
          dob: dobString,
          approxAge: approxYears > 0 ? String(approxYears) : "1",
          purpose: cattle.purpose,
          region: cattle.region ?? "",
          previousCalvings: cattle.previousCalvings,
          pastVaccinations: cattle.pastVaccinations,
          photoUrl: cattle.photoUrl ?? "",
          isActive: cattle.isActive,
        }}
      />
    </div>
  );
}

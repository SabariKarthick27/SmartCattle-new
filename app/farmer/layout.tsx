import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";
import prisma from "@/lib/prisma";
import FarmerSidebar from "@/components/FarmerSidebar";
import SessionGuard from "@/components/SessionGuard";

export default async function FarmerLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "farmer") redirect("/login");

  const dbUser = await prisma.user.findUnique({
    where: { id: session.user.id },
    select: { photoUrl: true, image: true },
  });
  const userImage = dbUser?.photoUrl || dbUser?.image || session.user.image || null;

  return (
    <div className="min-h-screen bg-[#f6f8f7] flex">
      <SessionGuard requiredRole="farmer" />
      {/* Sidebar (handles desktop rail and mobile drawer) */}
      <FarmerSidebar
        userName={session.user.name}
        userEmail={session.user.email}
        userImage={userImage}
      />

      {/* Main content */}
      <main className="flex-1 md:ml-60 min-h-screen pt-14 md:pt-0">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}


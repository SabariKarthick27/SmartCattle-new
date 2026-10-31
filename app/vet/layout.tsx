import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";
import prisma from "@/lib/prisma";
import VetSidebar from "@/components/VetSidebar";
import SessionGuard from "@/components/SessionGuard";

export default async function VetLayout({ children }: { children: React.ReactNode }) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "vet") redirect("/login");

  const dbUser = await prisma.user.findUnique({
    where: { id: session.user.id },
    select: { photoUrl: true, image: true },
  });
  const userImage = dbUser?.photoUrl || dbUser?.image || session.user.image || null;

  return (
    <div className="min-h-screen bg-[#f6f8f7] flex">
      <SessionGuard requiredRole="vet" />
      <VetSidebar
        userName={session.user.name}
        userEmail={session.user.email}
        userImage={userImage}
      />
      <main className="flex-1 md:ml-60 min-h-screen pt-14 md:pt-0">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}


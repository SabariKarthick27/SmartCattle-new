import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";
import FarmerSidebar from "@/components/FarmerSidebar";

export default async function FarmerLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "farmer") redirect("/login");

  return (
    <div className="min-h-screen bg-[#f6f8f7] flex">
      {/* Sidebar (handles desktop rail and mobile drawer) */}
      <FarmerSidebar
        userName={session.user.name}
        userEmail={session.user.email}
        userImage={session.user.image}
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


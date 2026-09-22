import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";
import VetSidebar from "@/components/VetSidebar";

export default async function VetLayout({ children }: { children: React.ReactNode }) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "vet") redirect("/login");

  return (
    <div className="min-h-screen bg-slate-50 flex">
      <VetSidebar
        userName={session.user.name}
        userEmail={session.user.email}
      />
      <main className="flex-1 ml-64 min-h-screen">{children}</main>
    </div>
  );
}
